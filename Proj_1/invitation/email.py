from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def mail_config_tester():
    the_key = getattr(settings, "EMAIL_KEY", None)
    print(f'Mail key {the_key}')
    return the_key


def url_builder(key):
    return 'http://127.0.0.1:8000/invite/invited/' + key


def body_builder(url, invitee, user_name, group_name):
    body = f'Dear {invitee}, {user_name} invites you to become a member of the group "{group_name}"" <br>'
    body += 'To do this, click on the link below'
    body += '<br>' + url + '<br>We hope to see you soon!'
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


def send_email(html, destination, subject):

    try:
        sg = SendGridAPIClient(getattr(settings, "EMAIL_KEY", None))
        sender = getattr(settings, "EMAIL_FROM", None)
        message = Mail(
            from_email=sender,
            to_emails=destination,
            subject=subject,
            html_content=html)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return 0
    except Exception as e:
        print(str(e))
        return 1


def email_main(**kwargs):
    '''
    key, invitee, user_name, group_name, destination, subject
    :param key:
    :param invitee:
    :param user_name:
    :param group_name:
    :param destination:
    :param subject:
    :return:
    '''
    url = url_builder(**kwargs.get('key'))
    body = body_builder(url, **kwargs.get('invitee'), **kwargs.get('user_name'), **kwargs.get('group_name'))
    result = send_email(body, **kwargs.get('destination'), **kwargs.get('subject'))

