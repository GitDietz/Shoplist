from django.urls import path, re_path

from .views import *

app_name = 'invitation'

urlpatterns = [
    # path('invite/', invite, name='invitation_invite'),
    re_path(r'test/$', simple, name='simple'),
    ]

# urlpatterns = [
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<group>[0-9A-Za-z_\-]+)/$', activate, name='activate'),
    # url(r'^activation_sent/$', account_activation_sent, name='account_activation_sent'),
    # url(r'^complete/.*', complete, name='complete'),
    # url(r'^confirm/(?P<group_id>[0-9]+)(?P<group_name>\w+)', compile_confirmation, name='compile_confirmation'),
    # url(r'^invite/$', invite, name='invitation_invite'),
    # url(r'^invite_select_view/$', invite_select_view, name='invite_select_view'),
    # url(r'^invite_test/(?P<key>[0-9a-zA-Z]{40})/$', invite_test, name='invite_test'),
    # url(r'^invited/(?P<key>[0-9a-zA-Z]{40})/$', invited, name='invitation_invited'),
    # url(r'^select/$', invite_select_view, name='invite_select'),
    # url(r'^test/$', simple, name='simple'),
    # ]