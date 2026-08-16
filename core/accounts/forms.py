from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    ReadOnlyPasswordHashField,
)

User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


# class LoginForm(AuthenticationForm):
#     """
#     This class for make form for user who want to
#     login in his/her account
#     """
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)


class CustomUserCreationForm(forms.ModelForm):
    """
    This class for make a specefic form for admin panel
    for make a new user
    """

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput
    )

    """
    This class for add field that you want show in the admin panel
    """

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "is_staff",
            "is_active",
            "is_superuser",
            "is_verified",
            "groups",
            "user_permissions",
        )

    """
    This function for check tha password1 and password2 are the same and
    check the value of them
    """

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")

        return password2

    """
    This function for set the password1 for the password of the user
    and save the user in the DB
    """

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class CustomUserChangeForm(forms.ModelForm):
    """
    This class for specefic form for change the user information
    in the admin panel
    """

    password = ReadOnlyPasswordHashField()

    """
    This class for add field that you want show in the admin panel
    """

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_verified",
            "groups",
            "user_permissions",
            "last_login",
        )

    def clean_password(self):
        return self.initial["password"]
