# # DJANGO IMPORTS
from django.conf import settings
# from django.views.generic.simple import direct_to_template
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, Http404, HttpResponse, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from urllib.parse import urlencode

# # GLOBAL IMPORTS
import datetime
import logging
import uuid
from hashlib import sha1 as sha_constructor

# # LOCAL IMPORTS
from .email import email_main, url_builder_confirmation, email_confirmation
from invitation.models import InvitationKey
from .forms import InvitationKeyForm
from shop.models import ShopGroup
from .token import account_activation_token
from Proj_1.utils import in_post

is_key_valid = InvitationKey.objects.is_key_valid
send_result = ''


def create_key():
    salt = uuid.uuid4().hex
    key = sha_constructor(salt.encode()).hexdigest()
    logging.getLogger("info_logger").info(f'created key is {key}')
    return key


def is_existing_user(email):
    if User.objects.filter(email=email).exists():
        return True
    else:
        return False


class InvitationUsedCallback(object):
    """
    Callable to mark InvitationKey as used, by way of profile_callback.
    """

    def __init__(self, invitation_key, profile_callback):
        self.invitation_key = invitation_key
        self.profile_callback = profile_callback

    def __call__(self, user):
        """Mark the key used, and then call the real callback (if any)."""
        key = InvitationKey.objects.get_key(self.invitation_key)
        if key:
            key.mark_used(user)

        if self.profile_callback:
            self.profile_callback(user)


def account_activation_sent(request):
    content_body = ('<p>Thank you for registering!<br>'
                   'To complete the process, check your mailbox for an email from us, then '
                    '<br> Click on the link that will bring you back to the site to do so<br><br>'
                    'See you soon ....</p>')
    context = {'title': 'Sent email',
               'content_body': content_body}
    return render(request, 'activation_sent.html', context)


def activate(request, uidb64, token, group):
    try:
        logging.getLogger("info_logger").info(f'new user url decode start')
        uid = force_text(urlsafe_base64_decode(uidb64))
        new_user = User.objects.get(pk=uid)
        group_id = force_text(urlsafe_base64_decode(group))
        new_group = ShopGroup.objects.get(pk=group_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        logging.getLogger("info_logger").info(f'user decode failed')
        new_user = None

    if new_user is not None and account_activation_token.check_token(new_user, token):
        logging.getLogger("info_logger").info(f'update user and group')
        new_user.is_active = True
        new_user.save()
        login(request, new_user)
        uname = new_user.username
        pword = new_user.password #this create a problem due to the hashing of the password and compar pw hashes it before comparison!
        Session.objects.all().delete() # try to clear the session before loggin in again
        # user = authenticate(username=new_user.username, password=new_user.password)
        user = authenticate(username=uname, password=pword)
        # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        login(request, user)
        new_group.disabled = False
        new_group.save()
        new_group.members.add(user)
        new_group.leaders.add(user)
        # activate the group and set the properties required

        request.session['list'] = new_group.id
        logging.getLogger("info_logger").info(f'user list set in session')
        return redirect('set_group')
    else:
        return render(request, 'activation_invalid.html')



def compile_confirmation(request, group_id, group_name):
    """
    17/3/20 test the generation of the confirmation
    20/3 now part of another view - remove
    :param request:
    :return:
    in newer django versions >=2.2 remove force_text
    """
    coded_user = force_text(urlsafe_base64_encode(force_bytes(request.user.pk)))
    coded_group = force_text(urlsafe_base64_encode(force_bytes(group_id)))
    token = account_activation_token.make_token(request.user)
    domain = get_current_site(request)
    # message = render_to_string('activation_invalid.html', {
    #     'user': request.user,
    #     'domain': domain,
    #     'uid': strurlstr,
    #     'token': token,
    # })
    # url = url_builder_confirmation(coded_user, token)
    email_kwargs = {"user": request.user.first_name,
                    "coded_user": coded_user,
                    'coded_group': coded_group,
                    "token": token,
                    "group_name": group_name,
                    "destination": request.user.email,
                    "subject": "Confirm your registration"}
    send_result = email_confirmation(request.user.pk, **email_kwargs)
    return redirect('invitations:account_activation_sent')


@login_required()
def complete(request):
    template_name = 'invitation_complete.html'
    mail_body = request.GET.get('send_result')
    logging.getLogger("info_logger").info(f'Invite Complete|parameter = {mail_body} ')
    context = {
        'title': 'Sent invite',
        'mail_body': mail_body}

    return render(request, template_name, context)


@login_required()
def invite(request):
    form = InvitationKeyForm(request.user, request.POST or None)

    template_name = 'invitation_form.html'
    invite_selection = ShopGroup.objects.managed_by(request.user) # to do add this!
    logging.getLogger("info_logger").info(f'can select from {invite_selection}')

    if request.method == 'POST':
        logging.getLogger("info_logger").info('Post section | user={request.user}')
        # form = InvitationKeyForm(request.POST)
        if form.is_valid():
            InvitationKey = form.save(commit=False)
            data = request.POST.copy()
            email = data.get('email')
            # print(f'form Data is {data}')

            InvitationKey.key = create_key()
            InvitationKey.from_user = request.user
            InvitationKey.invited_email = email
            logging.getLogger("info_logger").info('going to save invitation key')
            InvitationKey.save()
            send_status=''
            if not is_existing_user(email):
                # not an existing user, attempt to email
                email_kwargs = {"key": InvitationKey.key,
                                "invitee": data.get('invite_name'),
                                "user_name": request.user.username,
                                "group_name": InvitationKey.invite_to_group,
                                "destination": data.get('email'),
                                "subject": "Your invitation to join"}
                send_result = email_main(False, **email_kwargs)
                # result can be 0 if success or a string if failed
                if send_result == 0:
                    send_status = 'pass'
                else:
                    send_status = 'fail'
                    send_result = ('<p>Automatic sending failed.<br>Please copy the text below, paste'
                                   ' it into a new email and send it to your friend.<br><br></p>') + send_result
            else:
                # 3rd case not sending an email
                send_status = 'not sent'
                send_result = ('<p>The person you invited is already a member on the site<br>'
                               'Next time they log on, they will be able to join the group</p>')

            if send_result != 0:
                logging.getLogger("info_logger").info('there is a send_result')
                #  send_result contains the body. The below creates a custom url to contain the invite text
                base_url = reverse('invitations:complete')
                query_string = urlencode({'send_result': send_result})
                url = f'{base_url}?{query_string}'
                return redirect(url)
            else:
                logging.getLogger("info_logger").info("email sent")
                return redirect('invitations:complete')
                # format redirect to contain the send_result
                # return HttpResponseRedirect(reverse('invitations:invitation_completed', kwargs={'send_result': send_result}))
                # return redirect('invitations:complete', kwargs={'send_result': send_result})

        else:
            logging.getLogger("info_logger").info("errors on form, return to form")
            print(f'Form errors: {form.errors}')

    logging.getLogger("info_logger").info('Outside Post section')
    if not invite_selection:
        logging.getLogger("info_logger").info('no invite possible - not a manager')
        form_option = 'refer'
    else:
        form_option = 'fill'
    context = {
        'title': 'Send invite to join the group',
        'form': form,
        'form_option': form_option,
    }
    return render(request, template_name, context)


def invited(request, key=None, extra_context=None):
    '''
    The view when the user clicks on the link in the email
    if no valid invite key divert to the registration view
    '''
    if 'INVITE_MODE' in dir(settings) and settings.INVITE_MODE:
        logging.getLogger("info_logger").info('Able to invite')
        if key and is_key_valid(key):
            template_name = 'invitation/invited.html'
            logging.getLogger("info_logger").info("Valid key")
        else:
            template_name = 'invitation/wrong_invitation_key.html'
        extra_context = extra_context is not None and extra_context.copy() or {}
        extra_context.update({'invitation_key': key})
        return None
    else:
        return HttpResponseRedirect(reverse('registration_register'))


@login_required()
def invite_select_view(request):
    '''
    when an existing user logs in - check if there are invites
        no invites - send to set_group
        invites - show list to accept or decline the invite
        No more invites - send to set_group
    :return:
    '''
    title = 'Select to join group/s'
    open_invites = InvitationKey.objects.filter(invite_used=False).filter(invited_email=request.user.email)

    if open_invites.count() == 0:
        logging.getLogger("info_logger").info("redirect to select a group")
        return redirect('set_group')
    else:
        if request.POST:
            accept_item = in_post(request.POST, 'accept_item')
            reject_item = in_post(request.POST, 'reject_item')
            if accept_item !=0 or reject_item !=0:
                item_to_update = max(accept_item, reject_item)
                instance = get_object_or_404(InvitationKey, id=item_to_update)
                if accept_item != 0:
                    logging.getLogger("info_logger").info(f'to accept item {accept_item}')
                    group_instance = get_object_or_404(ShopGroup, name=instance.invite_to_group.name)
                    group_instance.members.add(request.user)
                    instance.invite_used = True
                elif reject_item != 0:
                    logging.getLogger("info_logger").info(f'to mark as reject item {reject_item}')
                    instance.invite_used = True

                instance.save()

    open_invites = InvitationKey.objects.filter(invite_used=False).filter(invited_email=request.user.email)

    if open_invites.count() == 0:
        # redirect to the other form
        return redirect('set_group')

    context = {'objects': open_invites,
               'title': title}

    return render(request, "invite_select_list.html", context=context)


@login_required()
def simple(request):
    # just to test the delivery of  a safe string to the browser
    template_name = 'invitation_complete.html'
    mail_body = ('The person you invited is already a member on the site<br>'
                 'Next time they log on, they will be able to join the group')

    context = {
        'title': 'Sent invite',
        'mail_body': mail_body}

    return render(request, template_name, context)




