from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers.authentication import *

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

            detail = {
                "email":username,
            }

            return Response(detail, status=status.HTTP_201_CREATED)
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