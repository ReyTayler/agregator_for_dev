from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserLoginForm, UserRegistrationForm, AccountSettingsForm


def login_view(request: HttpRequest):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Вход в аккаунт успешен.')
            return redirect('main')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {"form": form})


def logout_view(request: HttpRequest):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта.')
    return redirect('main')


def register_view(request: HttpRequest):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Вы успешно зарегистрировались как {user.email}")
            return redirect('main')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/registration.html', {'form': form})


@login_required
def account_settings_view(request):
    if request.method == 'POST':
        form = AccountSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Настройки сохранены, {request.user.email}')
            return redirect('accounts:settings')
    else:
        form = AccountSettingsForm(instance=request.user)

    return render(request, 'accounts/settings.html', {'form': form})
