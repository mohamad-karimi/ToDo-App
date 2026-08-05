from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account is created")
            return redirect("accounts:login")
        else:
            messages.error(request, "The information is incorrect")
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Your login is successful")
            return redirect("/")
        else:
            messages.error(request, "The information is incorrect")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})