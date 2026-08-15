from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    '''
    Custom JWT serializer that adds user information to the token response
    and prevents unverified users from obtaining JWT tokens.
    '''
    
    def validate(self, attrs):
        '''
        Validate credentials and return JWT tokens with user information.
        '''
                
        validate_data = super().validate(attrs)
        validate_data["username"] = self.user.username
        validate_data["user_id"] = self.user.id
    
        return validate_data