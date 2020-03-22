from django.conf import settings
from django.contrib.sites.models import Site
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging
import socket


def mail_config_tester():
    the_key = getattr(settings, "EMAIL_KEY", None)
    print(f'Mail key {the_key}')
    return the_key


def url_domain():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        if ip == '127.0.0.1':
            return 'http://' + ip + ':8000/'
        elif ip == '192.168.1.118':
            return 'http://127.0.0.1:8000/'
        else:
            return 'http://' + ip + '/'
    except:
        return 'http://127.0.0.1:8000/'


def url_builder(key):
    return url_domain() + 'invite/invited/' + key + '/'


def url_builder_existing_user():
    return url_domain() + 'login/'


def url_builder_confirmation(uidb64, token, shopgroup):
    return url_domain() + 'invite/activate/' + uidb64 + '/' + token + '/' + shopgroup + '/'
    # r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<group>[0-9A-Za-z_\-]+)/$'


def body_builder(url, invitee, user_name, group_name):
    body = f'Dear {invitee}, {user_name} invites you to become a member of the group "{group_name}" <br>'
    body += 'To do this, click on the link below'
    body += '<br>' + url + '<br>We hope to see you soon!'
    body += '<br>From the team at YourList'
    return body


def body_builder_confirm_email(url, user_name, group_name):
    body = f'Dear {user_name} <br> Great that you\'ve signed up with group - "{group_name}" <br>'
    body += 'As the final step, click on the link below to return to the site to confirm your email<br> and start using it!'
    body += '<br>' + url + '<br><br>We hope to see you soon!'
    body += '<br>From the team at YourList'
    return body


def test_send_email():
    message = Mail(
        from_email='asharpsystems@gmail.com',
        to_emails='africanmeats@gmail.com',
        subject='Sending test from mailhelper',
        html_content='<strong>HTML body content</strong>')
    try:
        sg = SendGridAPIClient(getattr(settings, "EMAIL_KEY", None))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

    return None


def send_email(body, destination, subject):

    try:
        sg = SendGridAPIClient(getattr(settings, "EMAIL_KEY", None))
        sender = getattr(settings, "EMAIL_FROM", None)
        message = Mail(
            from_email=sender,
            to_emails=destination,
            subject=subject,
            html_content=body)
        response = sg.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
        return 0
    except Exception as e:
        logging.getLogger("info_logger").info("str(e)")
        return body


def email_main(existing_user, **email_kwargs):
    '''  Main code to build the components from key, invitee, user_name, group_name, destination, subject     '''
    if not existing_user:
        url = url_builder(email_kwargs.get('key'))
    else:
        url = url_builder_existing_user()
    body = body_builder(url, email_kwargs.get('invitee'), email_kwargs.get('user_name'), email_kwargs.get('group_name'))
    force_fail = False
    if force_fail:
        result = body
    else:
        result = send_email(body, email_kwargs.get('destination'), email_kwargs.get('subject'))
    # result will be 0 if success or the body if failed
    return result


def email_confirmation(user_id, **email_kwargs):
    url = url_builder_confirmation(email_kwargs.get('coded_user'), email_kwargs.get('token'), email_kwargs.get('coded_group'))
    body = body_builder_confirm_email(url, email_kwargs.get('user'), email_kwargs.get('group_name'))
    force_fail = False
    if force_fail:
        result = body
    else:
        result = send_email(body, email_kwargs.get('destination'), email_kwargs.get('subject'))
    # result will be 0 if success or the body if failed
    return result
