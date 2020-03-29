# # DJANGO IMPORTS
# from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, Http404, HttpResponse, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


# # GLOBAL IMPORTS
import datetime
import logging
import uuid
from hashlib import sha1 as sha_constructor

# # LOCAL IMPORTS
from .email import email_main, url_builder_confirmation, email_confirmation
from .models import InvitationKey
# from .forms import *
# from Proj_1.shop.models import ShopGroup
# from .token import account_activation_token
# from Proj_1.proj_base.utils import in_post

# is_key_valid = InvitationKey.objects.is_key_valid
# send_result = ''
#
#
# @login_required()
# def invite(request):
#     form = InvitationKeyForm(request.user, request.POST or None)
#
#     template_name = 'invitation_form.html'
#     invite_selection = ShopGroup.objects.managed_by(request.user) # to do add this!
#     logging.getLogger("info_logger").info(f'can select from {invite_selection}')
#
#     if request.method == 'POST':
#         logging.getLogger("info_logger").info('Post section | user={request.user}')
#         # form = InvitationKeyForm(request.POST)
#         if form.is_valid():
#             InvitationKey = form.save(commit=False)
#             data = request.POST.copy()
#             email = data.get('email')
#             # print(f'form Data is {data}')
#
#             InvitationKey.key = create_key()
#             InvitationKey.from_user = request.user
#             InvitationKey.invited_email = email
#             logging.getLogger("info_logger").info('going to save invitation key')
#             InvitationKey.save()
#             send_status=''
#             if not is_existing_user(email):
#                 # not an existing user, attempt to email
#                 email_kwargs = {"key": InvitationKey.key,
#                                 "invitee": data.get('invite_name'),
#                                 "user_name": request.user.username,
#                                 "group_name": InvitationKey.invite_to_group,
#                                 "destination": data.get('email'),
#                                 "subject": "Your invitation to join"}
#                 send_result = email_main(False, **email_kwargs)
#                 # result can be 0 if success or a string if failed
#                 if send_result == 0:
#                     send_status = 'pass'
#                 else:
#                     send_status = 'fail'
#                     send_result = ('<p>Automatic sending failed.<br>Please copy the text below, paste'
#                                    ' it into a new email and send it to your friend.<br><br></p>') + send_result
#             else:
#                 # 3rd case not sending an email
#                 send_status = 'not sent'
#                 send_result = ('<p>The person you invited is already a member on the site<br>'
#                                'Next time they log on, they will be able to join the group</p>')
#
#             if send_result != 0:
#                 logging.getLogger("info_logger").info('there is a send_result')
#                 #  send_result contains the body. The below creates a custom url to contain the invite text
#                 base_url = reverse('invitations:complete')
#                 query_string = urlencode({'send_result': send_result})
#                 url = f'{base_url}?{query_string}'
#                 return redirect(url)
#             else:
#                 logging.getLogger("info_logger").info("email sent")
#                 return redirect('invitations:complete')
#                 # format redirect to contain the send_result
#                 # return HttpResponseRedirect(reverse('invitations:invitation_completed', kwargs={'send_result': send_result}))
#                 # return redirect('invitations:complete', kwargs={'send_result': send_result})
#
#         else:
#             logging.getLogger("info_logger").info("errors on form, return to form")
#             print(f'Form errors: {form.errors}')
#
#     logging.getLogger("info_logger").info('Outside Post section')
#     if not invite_selection:
#         logging.getLogger("info_logger").info('no invite possible - not a manager')
#         form_option = 'refer'
#     else:
#         form_option = 'fill'
#     context = {
#         'title': 'Send invite to join the group',
#         'form': form,
#         'form_option': form_option,
#     }
#     return render(request, template_name, context)
#


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
