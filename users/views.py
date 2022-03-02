from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.contrib import messages

from users.forms import UserLoginForms, UserRegistrationForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForms(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForms()
    context = {'title': 'Store - Авторизация', 'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'title': 'Store - Регистрация', 'form': form}
    return render(request, 'users/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
