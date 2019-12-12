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
    body = f'Dear {invitee}, {user_name} invites you to become a member of the group "{group_name}" <br>'
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
        print(str(e))
        return body


def email_main(**email_kwargs):
    '''  Main code to build the components from key, invitee, user_name, group_name, destination, subject     '''
    url = url_builder(email_kwargs.get('key'))
    body = body_builder(url, email_kwargs.get('invitee'), email_kwargs.get('user_name'), email_kwargs.get('group_name'))
    result = send_email(body, email_kwargs.get('destination'), email_kwargs.get('subject'))
    return result

