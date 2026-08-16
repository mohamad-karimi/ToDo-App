from django.urls import path
from ..views import *

app_name = "authentication"

urlpatterns = [
    path("registration/", RegistrationApiView.as_view(), name="registration"),
    path("password/change/", PasswordChangeApiView.as_view(), name="password-change"),
    path(
        "activation/confirm/<str:token>",
        ActivationConfirmApiView.as_view(),
        name="activation-confirm",
    ),
    # Reset Activation
    path(
        "activation/resend/",
        ActivationResendApiView.as_view(),
        name="activation-resend",
    ),
]