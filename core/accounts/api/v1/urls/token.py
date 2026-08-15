from django.urls import path
from ..views import *

app_name = "token"

urlpatterns = [
    path("token/login/", CustomObtainAuthToken.as_view(), name="token-login"),
    path("token/logout/", CustomDestroyAuthToken.as_view(), name="token-logout"),
]