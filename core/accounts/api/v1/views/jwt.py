from ..serializers.jwt import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from drf_spectacular.utils import extend_schema

@extend_schema(tags=["jwt"])
class CustomTokenObtainPairView(TokenObtainPairView):
    '''
    Custom JWT token view that uses the custom token serializer.
    '''
        
    serializer_class = CustomTokenObtainPairSerializer

@extend_schema(tags=["jwt"])
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=["jwt"])
class CustomTokenVerifyView(TokenVerifyView):
    pass