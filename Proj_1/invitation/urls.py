from django.conf.urls import include, url

from .views import invite, invited, completed, invite_select_view

urlpatterns = [
    url(r'^invite/$', invite, name='invitation_invite'),
    url(r'^invited/(?P<key>[0-9a-zA-Z]{40})/$', invited, name='invitation_invited'),
    url(r'^invite_select_view/$', invite_select_view, name='invite_select_view'),
    url(r'^complete/$', completed, name='invitation_completed'),
    url(r'^select/$', invite_select_view, name='invite_select'),
    ]

    #    url(r'^invite/complete/$', direct_to_template,
    # 'template': 'invitation/invitation_complete.html'},name='invitation_complete'),
    #
    #  url(r'^register/$', register, { 'backend': 'registration.backends.default.DefaultBackend' },
    #              name='registration_register'),
