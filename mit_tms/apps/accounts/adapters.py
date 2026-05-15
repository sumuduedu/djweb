import uuid
import logging

from django.contrib.auth import (
    get_user_model
)

from django.db import transaction

from django.shortcuts import redirect

from django.contrib import messages

from allauth.socialaccount.adapter import (
    DefaultSocialAccountAdapter
)

from allauth.account.adapter import (
    DefaultAccountAdapter
)

from .models import Profile


User = get_user_model()

logger = logging.getLogger(__name__)


# =========================================================
# SOCIAL ACCOUNT ADAPTER
# =========================================================

class MySocialAccountAdapter(
    DefaultSocialAccountAdapter
):

    # =====================================================
    # POPULATE USER
    # =====================================================

    def populate_user(
        self,
        request,
        sociallogin,
        data
    ):

        user = super().populate_user(
            request,
            sociallogin,
            data
        )

        email = data.get('email')

        if email:

            # =============================================
            # NORMALIZE EMAIL
            # =============================================

            email = (
                email
                .lower()
                .strip()
            )

            user.email = email

            # =============================================
            # CREATE SAFE BASE USERNAME
            # =============================================

            base_username = (
                email
                .split('@')[0]
                .replace(' ', '')
                .replace('.', '_')
            )

            # fallback safety
            if not base_username:
                base_username = 'user'

            # =============================================
            # GENERATE UNIQUE USERNAME
            # =============================================

            while True:

                username = (
                    f'{base_username}_'
                    f'{uuid.uuid4().hex[:6]}'
                )

                if not User.objects.filter(
                    username=username
                ).exists():

                    break

            user.username = username

        return user
    # =====================================================
    # AUTO SIGNUP
    # =====================================================

    def is_auto_signup_allowed(
        self,
        request,
        sociallogin
    ):

        return True

    # =====================================================
    # PRE SOCIAL LOGIN
    # =====================================================

    @transaction.atomic
    def pre_social_login(
        self,
        request,
        sociallogin
    ):

        if sociallogin.is_existing:
            return

        email = (
            sociallogin.account
            .extra_data
            .get('email')
            or sociallogin.user.email
        )

        if not email:
            return

        email = (
            email
            .lower()
            .strip()
        )

        # ================================================
        # SECURITY CHECK
        # ================================================

        email_verified = (
            sociallogin.account
            .extra_data
            .get(
                'email_verified',
                False
            )
        )

        if not email_verified:

            logger.warning(
                (
                    'Unverified social '
                    f'login attempt: {email}'
                )
            )

            return

        try:

            user = User.objects.get(
                email__iexact=email
            )

            # ============================================
            # CONNECT SOCIAL ACCOUNT
            # ============================================

            sociallogin.connect(
                request,
                user
            )

            logger.info(
                (
                    'Connected social '
                    f'account for {email}'
                )
            )

        except User.DoesNotExist:

            logger.info(
                (
                    'New social signup '
                    f'for {email}'
                )
            )

    # =====================================================
    # SAVE USER
    # =====================================================

    @transaction.atomic
    def save_user(
        self,
        request,
        sociallogin,
        form=None
    ):

        user = super().save_user(
            request,
            sociallogin,
            form
        )

        Profile.objects.get_or_create(
            user=user,
            defaults={
                'role': (
                    Profile.ROLE_GUEST
                )
            }
        )

        return user


# =========================================================
# ACCOUNT ADAPTER
# =========================================================

class CustomAccountAdapter(
    DefaultAccountAdapter
):

    # =====================================================
    # INACTIVE USER
    # =====================================================

    def respond_user_inactive(
        self,
        request,
        user
    ):

        messages.error(
            request,
            (
                'Your account is inactive. '
                'Please activate your '
                'account or contact admin.'
            )
        )

        return redirect(
            'accounts:login'
        )
