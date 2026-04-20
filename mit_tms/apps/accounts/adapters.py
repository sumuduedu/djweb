from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User


class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        email = data.get('email')

        if email:
            user.email = email   # 🔥 ensure email is set

            base_username = email.split('@')[0]
            username = base_username
            counter = 1

            # 🔥 ensure unique username
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            user.username = username

        return user

    def is_auto_signup_allowed(self, request, sociallogin):
        return True   # 🔥 always allow auto signup

    def pre_social_login(self, request, sociallogin):
        """
        🔥 CONNECT EXISTING USERS (VERY IMPORTANT)
        Prevent duplicate accounts
        """

        email = sociallogin.account.extra_data.get('email')

        if not email:
            return

        try:
            user = User.objects.get(email=email)

            # 🔥 connect Google account to existing user
            sociallogin.connect(request, user)

        except User.DoesNotExist:
            pass

# apps/accounts/adapter.py

# apps/accounts/adapter.py

from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect
from django.contrib import messages

class CustomAccountAdapter(DefaultAccountAdapter):

    def respond_user_inactive(self, request, user):
        messages.error(
            request,
            "Your account is inactive. Please check your email or contact admin."
        )

        # 🔥 YOUR CUSTOM REDIRECT HERE
        return redirect('accounts:login')   # or any page you want
