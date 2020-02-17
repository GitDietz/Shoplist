import logging
from django.conf import settings
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
    """
    the view only handles the login and then hands off to invite select or group select views

    """
    logging.getLogger("info_logger").info(f'entry to view')
    next = request.GET.get('next')  # this is available when the login required redirected to user to log in
    form = UserLoginForm(request.POST or None)
    title = 'Login'
    if form.is_valid():
        logging.getLogger("info_logger").info(f'form submitted')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        logging.getLogger("info_logger").info(f'new user authenticated ? {str(request.user.is_authenticated())}')
        has_invites = InvitationKey.objects.key_for_email(user.email)
        if has_invites:
            logging.getLogger("info_logger").info(f'divert to invite selection')
            return redirect('invitations:invite_select_view')
        else:
            logging.getLogger("info_logger").info(f'divert to set group')
            return redirect('set_group')

    context = {'form': form,
               'title': title}
    return render(request, "login_form.html", context=context)


def set_group(request):
    """ Sets group choice if there is only 1
    divert to select view if more
    """
    list_choices = ShopGroup.objects.filter(members=request.user)
    if list_choices is None:
        # if request.user.username == 'SuperAdmin':
        logging.getLogger("info_logger").info(f'rare case - no groups for user')
        return redirect('/')
    elif list_choices.count() > 1:
        logging.getLogger("info_logger").info(f'user {request.user} is member to >1 group')
        return redirect('shop:group_select')
    else:
        # also set the session with the value
        select_item = list_choices.first().id
        logging.getLogger("info_logger").info(f'default list {select_item}')
        request.session['list'] = select_item
        return redirect('/')


def register_view(request):
    """
    register as a complete unknown and uninvited visitor
    settings can disable the view
    """
    logging.getLogger("info_logger").info(f'Enter')
    next = request.GET.get('next')
    if 'REGISTRATIONS' in dir(settings) and settings.REGISTRATIONS:
        logging.getLogger("info_logger").info(f'Registration allowed')
        title = 'Register'
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            target_group = form.cleaned_data.get('joining')
            # to be valid it was checked to not exist

            user = form.save(commit=False)

            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            logging.getLogger("info_logger").info(f'Saved user')
            new_group = ShopGroup.objects.create_group(target_group, user)
            new_group.save()
            new_group.members.add(user)
            new_group.leaders.add(user)
            logging.getLogger("info_logger").info(f'Added user to group')
            new_user = authenticate(username=user.username, password=password)
            login(request, new_user)
            logging.getLogger("info_logger").info(f'user logged in (authenticated)')
            user_list = new_group.id
            request.session['list'] = user_list
            logging.getLogger("info_logger").info(f'user list set in session')
            if next:
                return redirect(next)
            return redirect('/')

        logging.getLogger("info_logger").info(f'Form unbound')
        context = {'form': form,
                   'title': title}

        return render(request, "login_form.html", context)
    else:
        logging.getLogger("info_logger").info(f'Registration disabled')
        return render(request, "temp_register.html", {})


def logout_view(request):
    logout(request)
    return render(request, "home.html", {})

def home_view(request):
    return render(request, "home.html", {})


# def temp_register_view(request):
#     return render(request, "temp_register.html", {})
