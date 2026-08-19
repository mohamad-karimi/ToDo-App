from django.urls import path
from ..views.token import CustomObtainAuthToken, CustomDestroyAuthToken

app_name = "token"

urlpatterns = [
    path("token/login/", CustomObtainAuthToken.as_view(), name="token-login"),
    path(
        "token/logout/", CustomDestroyAuthToken.as_view(), name="token-logout"
    ),
]
