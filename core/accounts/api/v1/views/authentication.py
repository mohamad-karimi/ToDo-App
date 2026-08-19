from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers.authentication import (
    RegistrationSerializer,
    PasswordChangeSerializer,
    ActivationResendSerializer,
    PasswordResetRequestSerializer,
    PasswordResetTokenSerializer,
)
from rest_framework.views import APIView
from mail_templated import EmailMessage
from ...utility import EmailThreading
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


@extend_schema(tags=["Authentication"])
class RegistrationApiView(GenericAPIView):
    """
    API view for registering a new user.
    Creates an email verification JWT and sends it to the user.
    """

    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        """
        Validate the registration data, create the user,
        generate an email verification token, and send the verification email.
        """

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            username = user.username
            user_email = user.email

            token = RefreshToken.for_user(user)
            token["type"] = "email_verification"

            email = EmailMessage(
                "email/email_verified.tpl",
                {
                    "username": username,
                    "user_email": user_email,
                    "token": str(token.access_token),
                },
                settings.DEFAULT_FROM_EMAIL,
                to=[user_email],
            )
            EmailThreading(email).start()

            detail = {
                "username": username,
                "user_email": user_email,
                "token": str(token.access_token),
            }

            return Response(
                detail,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Authentication"])
class PasswordChangeApiView(GenericAPIView):
    """
    API view for changing the authenticated user's password.
    """

    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Return the currently authenticated user.
        """

        return self.request.user

    def put(self, request, *args, **kwargs):
        """
        Validate the old password and update it with the new password.
        """

        user = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"old_password": ["Wrong password."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"detail": "Password changed successfully."},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Authentication"])
class ActivationConfirmApiView(APIView):
    """
    API view for confirming a user's email address.
    Validates the JWT and activates the associated user account.
    """

    def get(self, request, token):
        """
        Validate the activation token and mark the user's email as verified.
        """

        try:
            access_token = AccessToken(token)

            if access_token.get("type") != "email_verification":
                return Response(
                    {"detail": "Invalid token type."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user_id = access_token["user_id"]

        except TokenError:
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user.is_verified = True
        user.save(update_fields=["is_verified"])

        return Response(
            {"detail": "Email successfully verified."},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Authentication"])
class ActivationResendApiView(GenericAPIView):
    """
    API view for resending the email activation link.
    Generates a new verification JWT for an unverified user.
    """

    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        """
        Validate the user's email, generate a new activation token,
        and send the verification email again.
        """

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            user_email = user.email

            token = RefreshToken.for_user(user)
            token["type"] = "email_verification"

            email = EmailMessage(
                "email/email_verified.tpl",
                {"token": str(token.access_token)},
                settings.DEFAULT_FROM_EMAIL,
                to=[user_email],
            )

            EmailThreading(email).start()

            return Response(
                {"user_email": user_email, "token": str(token.access_token)},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Authentication"])
class PasswordResetView(GenericAPIView):
    """
    Handle password reset requests.

    Receives the user's email address, generates a secure password
    reset token, creates the reset URL, and sends it to the user.
    """

    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Process the password reset request.

        Validates the submitted email address, generates a password
        reset token, creates the reset URL, and sends the reset email.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.pk))

        token = default_token_generator.make_token(user)

        reset_url = (
            f"http://localhost:8000/api/v1/password/reset/" f"{uid}/{token}/"
        )

        send_mail(
            subject="Reset Password",
            message=f"""
            For change the password click in that link:

            {reset_url}

            If the request was not sent by you, ignore this message.
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response(
            {
                "detail": (
                    "Link for changing your password has been "
                    "sent to your email."
                )
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Authentication"])
class PasswordResetTokenView(GenericAPIView):
    """
    Handle password reset confirmation.

    Receives the encoded user ID and password reset token,
    validates the submitted password data, and updates the
    user's password.
    """

    serializer_class = PasswordResetTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request, uid, token):
        """
        Validate the reset token and change the user's password.

        The UID and token are passed to the serializer through
        the serializer context for validation.
        """
        serializer = self.get_serializer(
            data=request.data,
            context={
                "uid": uid,
                "token": token,
            },
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "The password is successfully changed."},
            status=status.HTTP_200_OK,
        )
