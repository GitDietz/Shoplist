from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout)

from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm
from invitation.models import InvitationKey
from shop.models import ShopGroup


def login_view(request):
    next = request.GET.get('next')  # this is available when the login required redirected to user to log in
    form = UserLoginForm(request.POST or None)
    title = 'Login'
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        print('Login_view, Is the user ok? ' + str(request.user.is_authenticated()))
        has_invites = InvitationKey.objects.key_for_email(user.email)
        if has_invites:
            return redirect('invitations:invite_select_view')
        else:
            return redirect('set_group')
            # list_choices = ShopGroup.objects.filter(members=request.user)
            # if list_choices is None:
            #     # if request.user.username == 'SuperAdmin':
            #     return redirect('/')
            # elif list_choices.count() > 1:
            #     return redirect('shop:group_select')
            # else:
            #     # also set the session with the value
            #     select_item = list_choices.first().id
            #     print(f'The default list {select_item}')
            #     request.session['list'] = select_item
            #     if next:
            #         return redirect(next)
            #     return redirect('/')

    context = {'form': form,
               'title': title}
    return render(request, "login_form.html", context=context)


def set_group(request):
    list_choices = ShopGroup.objects.filter(members=request.user)
    if list_choices is None:
        # if request.user.username == 'SuperAdmin':
        return redirect('/')
    elif list_choices.count() > 1:
        return redirect('shop:group_select')
    else:
        # also set the session with the value
        select_item = list_choices.first().id
        print(f'The default list {select_item}')
        request.session['list'] = select_item
        return redirect('/')


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
        new_group.leaders.add(user)
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        # setting the group for the user
        user_list = new_group.id
        request.session['list'] = user_list

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
