from django.conf.urls import include, url
from django.contrib import admin
from .views import shop_list, shop_detail, shop_create, merchant_list, merchant_detail, merchant_alt


urlpatterns = [
    url(r'^list/$', shop_list, name='shop_list'),
    url(r'^create/$', shop_create, name='shop_create'),
    #url(r'^bogger/$', shop_create, name='shop_bogger'),
    url(r'^merchants/$', merchant_list, name='merchant_list'),
    url(r'^merchant/(?P<id>\d+)/$', merchant_detail, name='merchant_detail'),
    url(r'^merchants/(?P<id>\d+)/$', merchant_alt, name='merchant_detail_alt'),

    url(r'^(?P<id>\d+)/$', shop_detail, name='shop_edit'),
    #url(r'^(?P<id>\d+)/$', item_detail, name='edit'),
]

