from django import forms

from django.contrib.auth import (
    get_user_model
)

from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm
)

from django.db import transaction


User = get_user_model()


# =========================================================
# COMMON STYLES
# =========================================================

INPUT_CLASS = (
    'w-full px-4 py-3 '
    'border border-gray-300 '
    'rounded-lg bg-gray-50 '
    'focus:bg-white '
    'focus:ring-2 '
    'focus:ring-blue-500 '
    'focus:outline-none '
    'transition text-sm'
)


# =========================================================
# LOGIN FORM
# =========================================================

class CustomLoginForm(
    AuthenticationForm
):

    username = forms.CharField(
        label='Username or Email',
        widget=forms.TextInput(
            attrs={
                'class': INPUT_CLASS,
                'placeholder': (
                    'Enter username or email'
                ),
                'autocomplete': 'username'
            }
        )
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': INPUT_CLASS,
                'placeholder': (
                    'Enter password'
                ),
                'autocomplete': (
                    'current-password'
                )
            }
        )
    )

    def confirm_login_allowed(
        self,
        user
    ):

        if not user.is_active:

            raise forms.ValidationError(
                (
                    'Your account is inactive. '
                    'Please activate your account '
                    'or contact administrator.'
                ),
                code='inactive'
            )


# =========================================================
# SIGNUP FORM
# =========================================================

class CustomSignupForm(
    UserCreationForm
):

    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': INPUT_CLASS,
                'placeholder': (
                    'Choose username'
                ),
                'autocomplete': 'username'
            }
        )
    )

    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(
            attrs={
                'class': INPUT_CLASS,
                'placeholder': (
                    'Enter email'
                ),
                'autocomplete': 'email'
            }
        )
    )

    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': INPUT_CLASS,
                'placeholder': (
                    'Enter password'
                ),
                'autocomplete': (
                    'new-password'
                )
            }
        ),
        help_text=(
            'Use a strong password.'
        )
    )

    password2 = forms.CharField(
        label='Confirm Password',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': INPUT_CLASS,
                'placeholder': (
                    'Confirm password'
                ),
                'autocomplete': (
                    'new-password'
                )
            }
        )
    )

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

    # =====================================================
    # EMAIL VALIDATION
    # =====================================================

    def clean_email(self):

        email = (
            self.cleaned_data
            .get('email')
        )

        if not email:

            raise forms.ValidationError(
                'Email is required.'
            )

        email = (
            email
            .lower()
            .strip()
        )

        exists = User.objects.filter(
            email__iexact=email
        ).exists()

        if exists:

            raise forms.ValidationError(
                (
                    'An account with this '
                    'email already exists.'
                )
            )

        return email

    # =====================================================
    # USERNAME VALIDATION
    # =====================================================

    def clean_username(self):

        username = (
            self.cleaned_data
            .get('username')
        )

        if not username:

            raise forms.ValidationError(
                'Username is required.'
            )

        username = username.strip()

        exists = User.objects.filter(
            username__iexact=username
        ).exists()

        if exists:

            raise forms.ValidationError(
                (
                    'Username already taken.'
                )
            )

        return username

    # =====================================================
    # SAVE USER
    # =====================================================

    @transaction.atomic
    def save(
        self,
        commit=True
    ):

        user = super().save(
            commit=False
        )

        user.email = (
            self.cleaned_data['email']
            .lower()
            .strip()
        )

        user.username = (
            self.cleaned_data['username']
            .strip()
        )

        if commit:

            user.save()

        return user


# =========================================================
# ADMIN USER CREATE FORM
# =========================================================

class UserCreateForm(
    UserCreationForm
):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': INPUT_CLASS
            }
        )
    )

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


# =========================================================
# ADMIN USER UPDATE FORM
# =========================================================

class UserUpdateForm(
    forms.ModelForm
):

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'first_name',
            'last_name'
        ]

        widgets = {

            'username': forms.TextInput(
                attrs={
                    'class': INPUT_CLASS
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': INPUT_CLASS
                }
            ),

            'first_name': forms.TextInput(
                attrs={
                    'class': INPUT_CLASS
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': INPUT_CLASS
                }
            ),
        }
