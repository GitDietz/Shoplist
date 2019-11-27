from django.conf.urls import include, url

from invitation.views import invite, invited
urlpatterns = [
    url(r'^invite/$', invite, name='invitation_invite'),
    url(r'^invited/(?P<invitation_key>\w+)/$', invited, name='invitation_invited'),

]
    #    url(r'^invite/complete/$', direct_to_template,
    # 'template': 'invitation/invitation_complete.html'},name='invitation_complete'),
    #
    #  url(r'^register/$', register, { 'backend': 'registration.backends.default.DefaultBackend' },
    #              name='registration_register'),
