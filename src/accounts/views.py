from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import UserLoginForm


def login_view(request: HttpRequest):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')

    else:
        form = UserLoginForm()
        return render(request, 'accounts/login.html', {"form": form})


def logout_view(request: HttpRequest):
    logout(request)
    return redirect('main')
