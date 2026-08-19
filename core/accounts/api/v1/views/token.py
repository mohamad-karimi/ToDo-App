from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from ..serializers.token import CustomAuthTokenSerializer
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework import status


@extend_schema(tags=["Token"])
class CustomObtainAuthToken(ObtainAuthToken):
    """
    API view for obtaining a DRF authentication token.
    Authenticates the user using email and password.
    """

    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        Validate the user's credentials and return an authentication token.
        """

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "username": user.username,
            }
        )


@extend_schema(tags=["Token"])
class CustomDestroyAuthToken(APIView):
    """
    API view for deleting the authenticated user's DRF token.
    """

    def post(self, request):
        """
        Delete the current user's authentication token.
        """

        request.user.auth_token.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
