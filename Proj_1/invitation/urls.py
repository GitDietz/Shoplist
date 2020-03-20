from django.conf.urls import include, url

from .views import invite, invited, complete, invite_select_view, simple, compile_confirmation

urlpatterns = [
    url(r'^invite/$', invite, name='invitation_invite'),
    url(r'^invited/(?P<key>[0-9a-zA-Z]{40})/$', invited, name='invitation_invited'),
    url(r'^invite_select_view/$', invite_select_view, name='invite_select_view'),
   # url(r'^complete/(?P<send_result>).*', complete, name='complete'),
    url(r'^confirm/', compile_confirmation, name='compile_confirmation'),
    url(r'^complete/.*', complete, name='complete'),
    url(r'^select/$', invite_select_view, name='invite_select'),
    url(r'^test/$', simple, name='simple'),
    ]

