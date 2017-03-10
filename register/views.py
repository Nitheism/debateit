from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import (login, authenticate, logout)


# This is the login and registration page logic and it is pretty straight forward
def registration(request):
    if request.user.is_authenticated():
        return redirect('/profile')
    form = RegisterForm
    context = {
        'form': form
    }
    return render(request, 'registration/registration_form.html', context)


def user_login(request):
    if request.user.is_authenticated():
        return redirect('/profile' + request.user.username)

    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile/' + username)

    context = {
        'form': form
    }
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')
