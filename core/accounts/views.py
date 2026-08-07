from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm

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
    

