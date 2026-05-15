from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.views import View

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    TemplateView
)

from django.contrib.auth import (
    login,
    logout,
    update_session_auth_hash,
    get_user_model
)

from django.contrib.auth.views import (
    LoginView
)

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.contrib import messages

from django.urls import reverse_lazy

from django.db import transaction

from django.core.mail import send_mail

from django.conf import settings

from django.contrib.sites.shortcuts import (
    get_current_site
)

from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode
)

from django.utils.encoding import (
    force_bytes,
    force_str
)

from django.contrib.auth.tokens import (
    default_token_generator
)

from .forms import (
    CustomSignupForm,
    CustomLoginForm,
    UserCreateForm,
    UserUpdateForm
)

from .models import (
    Profile
)

from .permissions import (
    AdminRequiredMixin
)

from .services.role_service import (
    assign_role
)


User = get_user_model()


# =========================================================
# LOGIN VIEW
# =========================================================

class CustomLoginView(LoginView):

    template_name = 'auth/pages/login.html'

    authentication_form = (
        CustomLoginForm
    )

    redirect_authenticated_user = True

    def form_invalid(self, form):

        messages.error(
            self.request,
            'Invalid credentials.'
        )

        return super().form_invalid(form)

    def get_success_url(self):

        return reverse_lazy(
            'core:dashboard'
        )


# =========================================================
# LOGOUT VIEW
# =========================================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        'Logged out successfully.'
    )

    return redirect(
        'accounts:login'
    )


# =========================================================
# SIGNUP VIEW
# =========================================================

class SignupView(View):

    template_name = 'auth/signup.html'

    def get(self, request):

        form = CustomSignupForm()

        return render(
            request,
            self.template_name,
            {
                'form': form
            }
        )

    @transaction.atomic
    def post(self, request):

        form = CustomSignupForm(
            request.POST
        )

        if not form.is_valid():

            return render(
                request,
                self.template_name,
                {
                    'form': form
                }
            )

        user = form.save(
            commit=False
        )

        user.is_active = False

        user.save()

        Profile.objects.get_or_create(
            user=user
        )

        uid = (
            urlsafe_base64_encode(
                force_bytes(user.pk)
            )
        )

        token = (
            default_token_generator
            .make_token(user)
        )

        protocol = (
            'https'
            if request.is_secure()
            else 'http'
        )

        domain = (
            get_current_site(
                request
            ).domain
        )

        activation_link = (
            f'{protocol}://{domain}'
            f'/accounts/activate/'
            f'{uid}/{token}/'
        )

        send_mail(
            subject='Activate Your Account',
            message=(
                f'Click the link below '
                f'to activate your account:\n\n'
                f'{activation_link}'
            ),
            from_email=(
                settings.DEFAULT_FROM_EMAIL
            ),
            recipient_list=[user.email],
            fail_silently=False
        )

        return render(
            request,
            'auth/signup_success.html',
            {
                'email': user.email
            }
        )


# =========================================================
# ACTIVATE ACCOUNT
# =========================================================

class ActivateAccountView(View):

    def get(
        self,
        request,
        uidb64,
        token
    ):

        user = None

        try:

            uid = force_str(
                urlsafe_base64_decode(
                    uidb64
                )
            )

            user = User.objects.get(
                pk=uid
            )

        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist
        ):

            user = None

        if (
            user
            and
            default_token_generator.check_token(
                user,
                token
            )
        ):

            user.is_active = True

            user.save()

            login(
                request,
                user
            )

            messages.success(
                request,
                'Account activated successfully.'
            )

            return redirect(
                'core:dashboard'
            )

        return render(
            request,
            'auth/activation_failed.html'
        )


# =========================================================
# PROFILE VIEW
# =========================================================

class ProfileView(
    LoginRequiredMixin,
    TemplateView
):

    template_name = (
        'accounts/profile.html'
    )

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        user = self.request.user

        context.update({

            'profile': getattr(
                user,
                'profile',
                None
            ),

            'student': getattr(
                user,
                'student',
                None
            ),

            'teacher': getattr(
                user,
                'teacher',
                None
            ),

            'staff': getattr(
                user,
                'staff',
                None
            ),

            'parent': getattr(
                user,
                'parent',
                None
            ),

            'alumni': getattr(
                user,
                'alumni',
                None
            ),
        })

        return context


# =========================================================
# ACCOUNT SETTINGS
# =========================================================

class AccountSettingsView(
    LoginRequiredMixin,
    UpdateView
):

    model = Profile

    fields = ['image']

    template_name = (
        'accounts/settings.html'
    )

    success_url = reverse_lazy(
        'accounts:profile'
    )

    def get_object(self):

        return self.request.user.profile

    def form_valid(self, form):

        messages.success(
            self.request,
            'Settings updated successfully.'
        )

        return super().form_valid(form)


# =========================================================
# USER LIST
# =========================================================

class UserListView(
    LoginRequiredMixin,
    AdminRequiredMixin,
    ListView
):

    model = User

    template_name = (
        'accounts/user_list.html'
    )

    context_object_name = 'users'

    paginate_by = 10

    def get_queryset(self):

        return (
            User.objects
            .select_related('profile')
            .order_by('-date_joined')
        )


# =========================================================
# USER DETAIL
# =========================================================

class UserDetailView(
    LoginRequiredMixin,
    AdminRequiredMixin,
    DetailView
):

    model = User

    template_name = (
        'accounts/user_detail.html'
    )

    context_object_name = 'user_obj'


# =========================================================
# USER CREATE
# =========================================================

class UserCreateView(
    LoginRequiredMixin,
    AdminRequiredMixin,
    CreateView
):

    model = User

    form_class = UserCreateForm

    template_name = (
        'accounts/user_form.html'
    )

    success_url = reverse_lazy(
        'accounts:user_list'
    )

    @transaction.atomic
    def form_valid(self, form):

        user = form.save(
            commit=False
        )

        password = (
            form.cleaned_data.get(
                'password'
            )
        )

        if password:

            user.set_password(
                password
            )

        user.save()

        Profile.objects.get_or_create(
            user=user
        )

        role = self.request.POST.get(
            'role'
        )

        if role:

            assign_role(
                user=user,
                role=role
            )

        messages.success(
            self.request,
            'User created successfully.'
        )

        return super().form_valid(form)


# =========================================================
# USER UPDATE
# =========================================================

class UserUpdateView(
    LoginRequiredMixin,
    AdminRequiredMixin,
    UpdateView
):

    model = User

    form_class = UserUpdateForm

    template_name = (
        'accounts/user_form.html'
    )

    success_url = reverse_lazy(
        'accounts:user_list'
    )

    @transaction.atomic
    def form_valid(self, form):

        user = form.save()

        role = (
            self.request.POST.get(
                'role'
            )
        )

        allowed_roles = [
            choice[0]
            for choice in (
                Profile.ROLE_CHOICES
            )
        ]

        if role in allowed_roles:

            assign_role(
                user=user,
                role=role
            )

        profile = user.profile

        image = (
            self.request.FILES.get(
                'image'
            )
        )

        if image:

            profile.image = image

            profile.save()

        password = (
            self.request.POST.get(
                'password'
            )
        )

        if password:

            user.set_password(
                password
            )

            user.save()

            update_session_auth_hash(
                self.request,
                user
            )

        messages.success(
            self.request,
            'User updated successfully.'
        )

        return super().form_valid(form)


# =========================================================
# USER DEACTIVATE
# =========================================================

class UserDeactivateView(
    LoginRequiredMixin,
    AdminRequiredMixin,
    View
):

    def post(
        self,
        request,
        pk
    ):

        user = get_object_or_404(
            User,
            pk=pk
        )

        if user == request.user:

            messages.error(
                request,
                (
                    'You cannot '
                    'deactivate yourself.'
                )
            )

            return redirect(
                'accounts:user_list'
            )

        user.is_active = (
            not user.is_active
        )

        user.save()

        if user.is_active:

            messages.success(
                request,
                f'{user.username} activated.'
            )

        else:

            messages.warning(
                request,
                f'{user.username} deactivated.'
            )

        return redirect(
            'accounts:user_list'
        )
