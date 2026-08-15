from django.urls import path, include
from .views import UserLoginView, Register
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(next_page="accounts:login"), name="logout"),
    path("register/", Register.as_view(), name="register"),
    path("api/v1/", include("accounts.api.v1.urls")),
]