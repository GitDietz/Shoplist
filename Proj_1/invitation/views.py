from django.conf import settings
# from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, Http404, HttpResponse, redirect

import uuid
from hashlib import sha1 as sha_constructor
# from registration.views import register as registration_register
# from registration.forms import RegistrationForm

from .email import mail_config_tester, test_send_email, email_main
from invitation.models import InvitationKey
from invitation.forms import InvitationKeyForm
from shop.models import ShopGroup

is_key_valid = InvitationKey.objects.is_key_valid
# remaining_invitations_for_user = InvitationKey.objects.remaining_invitations_for_user

send_result = ''

def create_key():
    salt = uuid.uuid4().hex
    key = sha_constructor(salt.encode()).hexdigest()
    print(f'create key is {key}')
    return key

# TODO: move the authorization control to a dedicated decorator

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


def invited(request, key=None, extra_context=None):
    if 'INVITE_MODE' in dir(settings) and settings.INVITE_MODE:
        if key and is_key_valid(key):
            template_name = 'invitation/invited.html'
        else:
            template_name = 'invitation/wrong_invitation_key.html'
        extra_context = extra_context is not None and extra_context.copy() or {}
        extra_context.update({'invitation_key': key})
        return None
            # direct_to_template(request, template_name, extra_context)
    else:
        return HttpResponseRedirect(reverse('registration_register'))


# def register(request, backend=None, success_url=None,
#              form_class=RegistrationForm, profile_callback=None,
#              template_name='registration/registration_form.html',
#              extra_context=None):
#     extra_context = extra_context is not None and extra_context.copy() or {}
#     if 'INVITE_MODE' in dir(settings) and settings.INVITE_MODE:
#         if 'invitation_key' in request.REQUEST:
#             invitation_key = request.REQUEST['invitation_key']
#             extra_context.update({'invitation_key': invitation_key})
#             if is_key_valid(invitation_key):
#                 profile_callback = InvitationUsedCallback(invitation_key,
#                                                           profile_callback)
#                 return registration_register(request, backend, success_url, form_class,
#                                              profile_callback, template_name, extra_context)
#             else:
#                 extra_context.update({'invalid_key': True})
#         else:
#             extra_context.update({'no_key': True})
#         template_name = 'invitation/wrong_invitation_key.html'
#         return direct_to_template(request, template_name, extra_context)
#     else:
#         return registration_register(request, success_url, form_class,
#                                      profile_callback, template_name, extra_context)
#
@login_required()
def invite(request):
    form = InvitationKeyForm(request.user, request.POST or None)
    # the_key = test_send_email()

    template_name = 'invitation_form.html'
    invite_selection = ShopGroup.objects.managed_by(request.user) # to do add this!
    print(f'can select from {invite_selection}')

    if request.method == 'POST':
        print(f'Invite| Post section |{request.user}')
        # form = InvitationKeyForm(request.POST)
        if form.is_valid():
            InvitationKey = form.save(commit=False)
            data = request.POST.copy()
            email = data.get('email')
            print(f'form Data is {data}')

            # invite_for = ShopGroup.objects.filter_by_instance(form.clean_invite_to_group)
            #invitation = InvitationKey.objects.create_invitation(request.user, InvitationKey.invite_to_group)
            InvitationKey.key = create_key()
            InvitationKey.from_user = request.user
            print('goin to save invitation key')
            InvitationKey.save()
            email_kwargs = {"key": InvitationKey.key,
                            "invitee": data.get('invite_name'),
                            "user_name": request.user.username,
                            "group_name": InvitationKey.invite_to_group,
                            "destination": data.get('email'),
                            "subject": "Your invitation to join"}
            print(email_kwargs)
            send_result = email_main(**email_kwargs)
            if send_result != 0:
                print('email send failed')
                print(send_result)
            return HttpResponseRedirect(reverse('invitations:invitation_completed'))
        else:
            print(f'Form errors: {form.errors}')

    print('Invite | Outside Post section')
    if not invite_selection:
        print('no invite possible - not a manager')
        form_option = 'refer'
    else:
        form_option = 'fill'
    context = {
        'title': 'Send invite to join the group',
        'form': form,
        'form_option': form_option,
    }
    return render(request, template_name, context)


@login_required()
def completed(request, send_result=None):
    template_name = 'invitation_complete.html'
    print(f'Invite Complete|parameter = {send_result} ')
    context = {
        'title': 'Sent invite',
        'invite':send_result,
            }
    return render(request, template_name, context)


# def invite_draft(request, success_url=None,
#            form_class=InvitationKeyForm,
#            template_name='invitation/invitation_form.html',
#            extra_context=None):
#     extra_context = extra_context is not None and extra_context.copy() or {}
#     remaining_invitations = remaining_invitations_for_user(request.user)
#     if request.method == 'POST':
#         form = form_class(data=request.POST, files=request.FILES)
#         if remaining_invitations > 0 and form.is_valid():
#             invitation = InvitationKey.objects.create_invitation(request.user)
#             invitation.send_to(form.cleaned_data["email"])
#             # success_url needs to be dynamically generated here; setting a
#             # a default value using reverse() will cause circular-import
#             # problems with the default URLConf for this application, which
#             # imports this file.
#             return HttpResponseRedirect(success_url or reverse('invitation_complete'))
#     else:
#         form = form_class()
#     extra_context.update({
#         'form': form,
#         'remaining_invitations': remaining_invitations,
#     })
#     return None # direct_to_template(request, template_name, extra_context)


