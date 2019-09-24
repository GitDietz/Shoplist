from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
    )

from django.shortcuts import render,redirect
from .forms import UserLoginForm, UserRegisterForm


def login_view(request):
    next = request.GET.get('next') # this is available when the login required redirected to user to log in
    form = UserLoginForm(request.POST or None)
    title = 'Login'
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        print('Loginview, Is the user ok? ' + str(request.user.is_authenticated()))
        if next:
            return redirect(next)
        return redirect('/')
    context = {'form':form,
               'title':title}
    return render(request, "login_form.html", context=context)

def register_view(request):
    next = request.GET.get('next')
    print('Regview,Is the user auth? ' + str(request.user.is_authenticated()) + request.user.username)
    title = 'Register'
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request,new_user)
        print('after valid/login. Is the user ok? ' + str(request.user.is_authenticated()) + request.user.username)
        if next:
            return redirect(next)
        return redirect('/')

    context = {'form': form,
               'title': title}

    return render(request, "login_form.html", context)

def logout_view(request):
    logout(request)
    return render(request, "home.html", {})

def home_view(request):
    return render(request, "home.html",{})

def temp_register_view(request):
    return render(request, "temp_register.html",{})
