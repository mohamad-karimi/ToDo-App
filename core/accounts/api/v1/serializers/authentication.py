from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    '''
    Serializer for registering a new user.
    Validates password confirmation and Django password requirements.
    '''

    password2 = serializers.CharField(max_length=120, write_only = True)
    class Meta():
        '''
        Define the user model and fields required for registration.
        '''
                
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
        ]

    def validate(self, attrs):
        '''
        Validate password confirmation and password strength.
        '''
                
        if attrs.get("password") != attrs.get("password2"):
            raise serializers.ValidationError(
                {
                    "detail":"passwords not match"
                }
            )
        
        try:
             validators.validate_password(password=attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs
    
    def create(self, validated_data):
        '''
        Create a new user using the custom user manager.
        '''
                
        validated_data.pop("password2", None)

        return User.objects.create_user(**validated_data)
    
class PasswordChangeSerializer(serializers.Serializer):
    '''
    Serializer for changing the user's password.
    Validates the old password and confirms the new password.
    '''
        
    old_password = serializers.CharField(
        required=True,
        write_only=True
    )

    new_password = serializers.CharField(
        required=True,
        write_only=True
    )

    new_password2 = serializers.CharField(
        required=True,
        write_only=True
    )

    def validate(self, attrs):
        '''
        Validate that the new password and its confirmation match.
        '''
        
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({
                "new_password2": "Passwords do not match."
            })

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
