from django.urls import path
from . import views
from .views import UserLoginView, Register
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(next_page="accounts:login"), name="logout"),
    path("register/", Register.as_view(), name="register"),
]