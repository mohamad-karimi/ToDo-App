from django.urls import path, include

app_name = "api-v1"

urlpatterns = [
    path("", include('accounts.api.v1.urls.authentication')),
    path("", include('accounts.api.v1.urls.token')),
    path("", include('accounts.api.v1.urls.jwt')),
]