from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.views import View
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import TemplateView
from mail_templated import EmailMessage

User = get_user_model()


class UserLoginView(LoginView):
    """
    Handles user authentication and login functionality.

    This view displays the login form, authenticates users,
    and redirects successfully authenticated users to the todo page.
    """

    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        """
        Returns the URL where users are redirected after successful login.
        """
        return reverse_lazy("todo:index")


class Register(FormView):
    """
    Handles user registration.

    This view displays the registration form, creates a new user account,
    automatically logs the user in after successful registration,
    and redirects them to the todo page.
    """

    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("todo:index")

    def form_valid(self, form):
        """
        Saves the registration form and logs in the newly created user.

        If the form data is valid, a new user is created and authenticated
        automatically.
        """

        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)

    def get(self, *args, **kwargs):
        """
        Prevents authenticated users from accessing the registration page.

        If the user is already logged in, they are redirected to the todo page.
        Otherwise, the registration page is displayed.
        """

        if self.request.user.is_authenticated:
            return redirect("todo:index")
        return super(Register, self).get(*args, **kwargs)


class PasswordResetSentView(TemplateView):
    """
    Display a page informing the user that the password reset
    email has been sent successfully.
    """

    template_name = "accounts/password_reset_sent.html"


class PasswordResetSendEmailView(View):
    """
    Handle password reset email requests.

    Displays a form where the user enters their email address,
    generates a password reset token, and sends the reset link.
    """

    template_name = "accounts/password_reset_send_email.html"

    def get(self, request):
        """
        Display the password reset email form.
        """

        return render(request, self.template_name)

    def post(self, request):
        """
        Process the password reset email request.

        Finds the user by email, generates a secure password reset token,
        creates the reset URL, and sends the reset email.
        """
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(
                request,
                self.template_name,
                {"error": "No account found with this email."},
            )

        uid = urlsafe_base64_encode(force_bytes(user.pk))

        token = default_token_generator.make_token(user)

        reset_url = request.build_absolute_uri(
            reverse(
                "accounts:password-reset",
                kwargs={
                    "uid": uid,
                    "token": token,
                },
            )
        )

        message = EmailMessage(
            "email/password_reset_email.tpl",
            {
                "username": user.username,
                "user_email": user.email,
                "reset_url": reset_url,
            },
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )

        message.send()

        return redirect("accounts:password-reset-sent")


class PasswordResetView(View):
    """
    Handle password reset link validation and password changing.

    Validates the encoded user ID and reset token before allowing
    the user to set a new password.
    """

    template_name = "accounts/password_reset.html"

    def get(self, request, uid, token):
        """
        Validate the password reset link and display the reset form.
        """

        try:
            uid_decoded = force_str(urlsafe_base64_decode(uid))

            user = User.objects.get(pk=uid_decoded)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return render(
                request,
                self.template_name,
                {"error": "Invalid password reset link."},
                status=400,
            )

        if not default_token_generator.check_token(user, token):
            return render(
                request,
                self.template_name,
                {"error": "This password reset link is invalid or expired."},
                status=400,
            )

        return render(
            request,
            self.template_name,
            {
                "uid": uid,
                "token": token,
            },
        )

    def post(self, request, uid, token):
        """
        Process the new password submitted by the user.

        Validates the password fields and reset token before
        updating the user's password.
        """
        new_password = request.POST.get("new_password")

        confirm_password = request.POST.get("confirm_password")

        if not new_password:
            return render(
                request,
                self.template_name,
                {
                    "error": "Password is required.",
                    "uid": uid,
                    "token": token,
                },
            )

        if new_password != confirm_password:
            return render(
                request,
                self.template_name,
                {
                    "error": "Passwords do not match.",
                    "uid": uid,
                    "token": token,
                },
            )

        try:
            uid_decoded = force_str(urlsafe_base64_decode(uid))

            user = User.objects.get(pk=uid_decoded)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return render(
                request,
                self.template_name,
                {"error": "Invalid password reset link."},
                status=400,
            )

        if not default_token_generator.check_token(user, token):
            return render(
                request,
                self.template_name,
                {"error": "This password reset link is invalid or expired."},
                status=400,
            )

        user.set_password(new_password)
        user.save()

        return redirect("accounts:password-reset-confirm")


class PasswordResetConfirmView(TemplateView):
    """
    Display the password reset completion page.
    """

    template_name = "accounts/password_reset_confirm.html"
