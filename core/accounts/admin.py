from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


# Register your models here.
class CustomUserAdmin(UserAdmin):
    """
    This class for making custome admin panel for the user
    """

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
        "is_superuser",
        "is_verified",
    )
    list_filter = ("is_staff", "is_active", "is_superuser", "is_verified")
    readonly_fields = ("create_date", "update_date")
    fieldsets = (
        ("Authentication", {"fields": ("username", "email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                )
            },
        ),
        (
            "Groups and Permissions",
            {"fields": ("groups", "user_permissions")},
        ),
        ("Important Dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            "Authentication",
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
        (
            "Permissions",
            {
                "classes": ("wide",),
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
        (
            "Groups and Permissions",
            {
                "classes": ("wide",),
                "fields": ("groups", "user_permissions"),
            },
        ),
    )

    search_fields = ("username",)
    ordering = ("username",)


admin.site.register(User, CustomUserAdmin)
