from django.urls import path
from ..views import *

app_name = "authentication"

urlpatterns = [
    path("registration/", RegistrationApiView.as_view(), name="registration"),
    path("password/change/", PasswordChangeApiView.as_view(), name="password-change"),
]