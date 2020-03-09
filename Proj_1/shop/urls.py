from django.conf.urls import include, url
from django.contrib import admin
from .views import (
    shop_list,
    shop_detail,
    shop_create,
    merchant_list,
    merchant_detail,
    merchant_create,
    merchant_update,
    merchant_delete,
    group_add_member,
    group_detail_rb,
    group_delete,
    group_maintenance,
    group_list,
    group_make_leader,
    group_remove_member,
    group_remove_leader,
    group_remove_self,
    search,
    simple_item_list,
    user_group_select
    )


urlpatterns = [
    url(r'^list/$', shop_list, name='shop_list'),
    url(r'^create/$', shop_create, name='shop_create'),
    #url(r'^bogger/$', shop_create, name='shop_bogger'),
    #url(r'^groups/(?P<pk>\d+)$', group_detail, name='group_update'),
    url(r'^groups/create$', group_detail_rb, name='group_create'),
    url(r'^groups/delete/(?P<pk>\d+)$', group_delete, name='group_delete'),
    url(r'^groups/maintain/(?P<pk>\d+)$', group_maintenance, name='group_maintenance'),
    url(r'^groups/make_leader/(?P<pk>\d+)(?P<user_id>\d+)$', group_make_leader, name='group_make_leader'),
    url(r'^groups/add_member/(?P<pk>\d+)(?P<user_id>\d+)$', group_add_member, name='group_add_member'),
    url(r'^groups/remove_self/(?P<pk>\d+)$', group_remove_self, name='group_remove_self'),
    url(r'^groups/remove_leader/(?P<pk>\d+)(?P<user_id>\d+)$', group_remove_leader, name='group_remove_leader'),
    url(r'^groups/remove_member/(?P<pk>\d+)(?P<user_id>\d+)$', group_remove_member, name='group_remove_member'),
    url(r'^groups/$', group_list, name='group_list'),
    url(r'^group_select/$', user_group_select, name='group_select'),
    url(r'^merchants/$', merchant_list, name='merchant_list'),
    url(r'^merchants/create$', merchant_create, name='merchant_create'),
    url(r'^merchants/(?P<pk>\d+)$', merchant_update, name='merchant_update'),
    url(r'^merchants/delete/(?P<pk>\d+)$', merchant_delete, name='merchant_delete'),
    url(r'^(?P<pk>\d+)/$', shop_detail, name='shop_edit'),
    url(r'^users/$', search, name='user_list'),
    url(r'^filter/$', simple_item_list, name='filter_list'),
    #url(r'^(?P<id>\d+)/$', item_detail, name='edit'),
]

