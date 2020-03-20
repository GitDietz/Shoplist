import logging
import re
from django.conf import settings
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout)

from django.db.models import Q
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm, UserLoginEmailForm
from invitation.models import InvitationKey
from shop.models import ShopGroup

User = get_user_model()

def create_next_increment_name(name):
    pattern = r"(^[a-zA-Z '-]+)([0-9]+)"
    match = re.match(pattern, name)
    if match:
        increment = match.group(2)
        new_inc = int(increment) + 1
        new_name = match.group(1) + str(new_inc)
        name_length = len(match.group(1))

        if len(new_name) > 30:
            new_name = match.group(1)[:name_length-1] + str(new_inc)
        return new_name
    else:
        return name + '1'


def create_username(first_name, last_name):
    logging.getLogger("info_logger").info(f'no username yet')

    new_username = first_name[:15] + last_name[:10]
    new_username.replace(' ', '')
    this_user = User.objects.all().filter(Q(username__iexact=new_username))

    while this_user.exists():
        new_username = create_next_increment_name(new_username)
        this_user = User.objects.all().filter(Q(username__iexact=new_username))
    return new_username


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


def login_email(request):
    """
    the view only handles the login and then hands off to invite select or group select views
    this method uses the email address and not the username
    """
    logging.getLogger("info_logger").info(f'entry to view')
    next = request.GET.get('next')  # this is available when the login required redirected to user to log in
    form = UserLoginEmailForm(request.POST or None)
    title = 'Login'
    if request.method == 'POST' and form.is_valid():
        logging.getLogger("info_logger").info(f'form submitted')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        username = form.cleaned_data.get('username')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            logging.getLogger("info_logger").info(f'new user authenticated')
            has_invites = InvitationKey.objects.key_for_email(user.email)
            if has_invites:
                logging.getLogger("info_logger").info(f'divert to invite selection')
                return redirect('invitations:invite_select_view')
            else:
                logging.getLogger("info_logger").info(f'divert to set group')
                return redirect('set_group')
    else:
        print(form.errors)

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
            # user.is_active = False # part of email confirmation
            user.username = create_username(user.first_name, user.last_name)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user.save()
            logging.getLogger("info_logger").info(f'Saved user')
            # temporary break out to test the register/confirm email
            return redirect('invitations:compile_confirmation')
            # will have to save the target group to the user?
            # or make the group inactive until the user creating it is active
            new_group = ShopGroup.objects.create_group(target_group, user)
            new_group.purpose = form.cleaned_data.get('purpose')
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
            return redirect('set_group')

        logging.getLogger("info_logger").info(f'Form unbound')
        context = {'form': form,
                   'title': title}

        return render(request, "login_form.html", context)
    else:
        logging.getLogger("info_logger").info(f'Registration disabled')
        return render(request, "temp_register.html", {})


def logout_view(request):
    logging.getLogger("info_logger").info(f'logging out {request.user}')
    logout(request)
    return render(request, "home.html", {})

def home_view(request):
    return render(request, "home.html", {})


# def temp_register_view(request):
#     return render(request, "temp_register.html", {})
