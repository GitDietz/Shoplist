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
    group_detail,
    group_list,
    group_delete,
    group_maintenance,
    group_remove_member,
    search,
    simple_item_list,
    user_group_select
    )


urlpatterns = [
    url(r'^list/$', shop_list, name='shop_list'),
    url(r'^create/$', shop_create, name='shop_create'),
    #url(r'^bogger/$', shop_create, name='shop_bogger'),
    url(r'^groups/(?P<pk>\d+)$', group_detail, name='group_update'),
    url(r'^groups/create$', group_detail, name='group_create'),
    url(r'^groups/delete/(?P<pk>\d+)$', group_delete, name='group_delete'),
    url(r'^groups/maintain/(?P<pk>\d+)$', group_maintenance, name='group_maintenance'),
    url(r'^groups/remove/(?P<pk>\d+)$', group_remove_member, name='group_remove_member'),
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

