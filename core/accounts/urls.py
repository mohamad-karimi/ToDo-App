from django.urls import path, include
from .views import (
    UserLoginView,
    Register,
    PasswordResetSendEmailView,
    PasswordResetSentView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path(
        "logout",
        LogoutView.as_view(next_page="accounts:login"),
        name="logout",
    ),
    path("register/", Register.as_view(), name="register"),
    path("api/v1/", include("accounts.api.v1.urls")),
    path(
        "password/reset/",
        PasswordResetSendEmailView.as_view(),
        name="password-reset-send-email",
    ),
    path(
        "password/reset/sent/",
        PasswordResetSentView.as_view(),
        name="password-reset-sent",
    ),
    path(
        "password/reset/<str:uid>/<str:token>/",
        PasswordResetView.as_view(),
        name="password-reset",
    ),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
]
