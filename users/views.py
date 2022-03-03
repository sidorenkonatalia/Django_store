from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.contrib import messages

from users.forms import UserLoginForms, UserRegistrationForm
from users.models import User, EmailVerification


def login(request):
    if request.method == 'POST':
        form = UserLoginForms(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_verified_email:
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


def email_verification(request, email, code):
    user = User.objects.get(email=email)
    email_verification = EmailVerification.objects.filter(user=user, code=code)
    if email_verification.exists() and not email_verification.last().is_expired():
        user.is_verified_email = True
        user.save()
        context = {'title': 'Store - Подтверждение электронной почты'}
        return render(request, 'users/email_verification.html', context)
    else:
        return HttpResponseRedirect(reverse('index'))
