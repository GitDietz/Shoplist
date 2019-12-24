from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
    )

from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm
from Proj_1.shop.models import ShopGroup


def login_view(request):
    next = request.GET.get('next')  # this is available when the login required redirected to user to log in
    form = UserLoginForm(request.POST or None)
    title = 'Login'
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        print('Loginview, Is the user ok? ' + str(request.user.is_authenticated()))
        list_choices = ShopGroup.objects.filter(members=request.user)
        if list_choices.count() > 1:
            return redirect('shop:group_select')
        else:
            # also set the session with the value
            select_item = list_choices.first().id
            print(f'The default list {select_item}')
            request.session['list'] = select_item
            if next:
                return redirect(next)
            return redirect('/')

        # this may be useful for another workflow but not in this case, after login user must select the list, if there is more than 1
        # if next:
        #     return redirect(next)
        # return redirect('/')
    context = {'form': form,
               'title': title}
    return render(request, "login_form.html", context=context)

def register_view(request):
    next = request.GET.get('next')
    print('Register view,Is the user auth? ' + str(request.user.is_authenticated()) + ' ' + request.user.username)
    title = 'Register'
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        target_group = form.cleaned_data.get('joining')
        # to be valid it was checked to not exist

        user = form.save(commit=False)

        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_group = ShopGroup.objects.create_group(target_group, user)
        new_group.save()
        new_group.members.add(user)
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
