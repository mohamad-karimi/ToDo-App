from django.urls import path
from ..views.jwt import (
    CustomTokenRefreshView,
    CustomTokenObtainPairView,
    CustomTokenVerifyView
)

app_name = "jwt"

urlpatterns = [
    path(
        "token/create/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "token/verify/", CustomTokenVerifyView.as_view(), name="token_verify"
    ),
]
