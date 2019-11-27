from django.shortcuts import redirect
from .models import Invite


class InviteMiddleware(object):
    def process_request(self, req):
        if req.path == '/i.auth':
            return None
        if not req.user.is_authenticated():
            if 'token' in req.COOKIES:
                return redirect('invitation.views.login_user')
        return None

    def process_response(self, req, resp):
        if req.user.is_authenticated():
            if req.user.is_staff:
                return resp
            if 'token' in req.COOKIES:
                token = req.COOKIES['token']
            else:
                invite = Invite.objects.get(user=req.user)
                token = invite.cookie
            resp.set_cookie('token', token, max_age=1209600)
            return resp
