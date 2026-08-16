from django.urls import path
from ..views.authentication import (
    RegistrationApiView,
    PasswordChangeApiView,
    PasswordResetView,
    PasswordResetTokenView,
    ActivationConfirmApiView,
    ActivationResendApiView
)

app_name = "authentication"

urlpatterns = [
    path("registration/", RegistrationApiView.as_view(), name="registration"),
    path(
        "password/change/",
        PasswordChangeApiView.as_view(),
        name="password-change",
    ),
    path(
        "password/reset/", PasswordResetView.as_view(), name="password-reset"
    ),
    path(
        "password/reset/<uid>/<token>/",
        PasswordResetTokenView.as_view(),
        name="password-reset-token",
    ),
    path(
        "activation/confirm/<str:token>",
        ActivationConfirmApiView.as_view(),
        name="activation-confirm",
    ),
    path(
        "activation/resend/",
        ActivationResendApiView.as_view(),
        name="activation-resend",
    ),
]
