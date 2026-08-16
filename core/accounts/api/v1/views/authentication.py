from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers.authentication import *
from rest_framework.views import APIView
from mail_templated import EmailMessage
from ...utility import EmailThreading
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError

@extend_schema(tags=["Authentication"])
class RegistrationApiView(GenericAPIView):
    '''
    API view for registering a new user.
    Creates an email verification JWT and sends it to the user.
    '''
        
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        '''
        Validate the registration data, create the user,
        generate an email verification token, and send the verification email.
        '''
                
        serializer = self.serializer_class(data = request.data)

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
                "username":username,
                "user_email": user_email,
                "token": str(token.access_token)
            }

            return Response(detail, status=status.HTTP_201_CREATED,)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@extend_schema(tags=["Authentication"])
class PasswordChangeApiView(GenericAPIView):
    '''
    API view for changing the authenticated user's password.
    '''
        
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        '''
        Return the currently authenticated user.
        '''
                
        return self.request.user

    def put(self, request, *args, **kwargs):
        '''
        Validate the old password and update it with the new password.
        '''
                
        user = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
    
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