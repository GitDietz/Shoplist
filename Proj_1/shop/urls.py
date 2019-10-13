from django.conf.urls import include, url
from django.contrib import admin
from .views import (
    shop_list,
    shop_detail,
    shop_create,
    merchant_list,
    merchant_detail,
    merchant_alt,
    merchant_create,
    merchant_update,
    merchant_delete,
    )


urlpatterns = [
    url(r'^list/$', shop_list, name='shop_list'),
    url(r'^create/$', shop_create, name='shop_create'),
    #url(r'^bogger/$', shop_create, name='shop_bogger'),
    url(r'^merchants/$', merchant_list, name='merchant_list'),
    url(r'^merchants/create$', merchant_create, name='merchant_create'),
    url(r'^merchants/(?P<pk>\d+)$', merchant_update, name='merchant_update'),
    url(r'^merchants/delete/(?P<pk>\d+)$', merchant_delete, name='merchant_delete'),
    url(r'^(?P<id>\d+)/$', shop_detail, name='shop_edit'),
    #url(r'^(?P<id>\d+)/$', item_detail, name='edit'),
]

