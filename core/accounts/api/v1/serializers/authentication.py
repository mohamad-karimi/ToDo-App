from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    Validates password confirmation and Django password requirements.
    """

    password2 = serializers.CharField(max_length=120, write_only=True)

    class Meta:
        """
        Define the user model and fields required for registration.
        """

        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
        ]

    def validate(self, attrs):
        """
        Validate password confirmation and password strength.
        """

        if attrs.get("password") != attrs.get("password2"):
            raise serializers.ValidationError(
                {"detail": "passwords not match"}
            )

        try:
            validators.validate_password(password=attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs

    def create(self, validated_data):
        """
        Create a new user using the custom user manager.
        """

        validated_data.pop("password2", None)

        return User.objects.create_user(**validated_data)


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing the user's password.
    Validates the old password and confirms the new password.
    """

    old_password = serializers.CharField(required=True, write_only=True)

    new_password = serializers.CharField(required=True, write_only=True)

    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """
        Validate that the new password and its confirmation match.
        """

        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError(
                {"new_password2": "Passwords do not match."}
            )

        return attrs


class ActivationResendSerializer(serializers.Serializer):
    """
    Serializer for requesting a new email activation link.
    Checks that the user exists and has not already verified their email.
    """

    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        """
        Validate the user's email and check their verification status.
        """

        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "User with this email does not exist."}
            )

        if user.is_verified:
            raise serializers.ValidationError(
                {"email": "Email is already verified."}
            )

        attrs["user"] = user
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for validating password reset requests.

    Validates that the submitted email address belongs to
    an existing user account.
    """
        
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Validate that a user exists with the submitted email address.

        Args:
            value: The email address submitted by the user.

        Returns:
            The validated email address.

        Raises:
            serializers.ValidationError:
                If no user exists with the submitted email address.
        """
                
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "The user with that email address does not exist."
            )

        return value


class PasswordResetTokenSerializer(serializers.Serializer):
    """
    Serializer for validating a password reset token and
    setting a new password for the associated user.
    """
        
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        """
        Validate the reset token and retrieve the associated user.

        The encoded user ID and reset token are received through
        the serializer context.

        Args:
            attrs: Validated serializer data.

        Returns:
            Updated validated data containing the associated user.

        Raises:
            serializers.ValidationError:
                If the reset link is invalid or the token is expired.
        """
                
        uid = self.context["uid"]
        token = self.context["token"]

        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid reset link.")

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError("Token is invalid or expired.")

        attrs["user"] = user

        return attrs

    def save(self):
        """
        Set the new password for the validated user.

        Returns:
            The updated user instance.
        """
                
        user = self.validated_data["user"]

        user.set_password(self.validated_data["new_password"])

        user.save()

        return user
