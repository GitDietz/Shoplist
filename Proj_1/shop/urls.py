from django.conf.urls import include, url
from django.contrib import admin
from .views import shop_list, shop_detail, shop_create


urlpatterns = [
    url(r'^list/$', shop_list, name='shop_list'),
    url(r'^create/$', shop_create, name='shop_create'),
    url(r'^(?P<id>\d+)/$', shop_detail, name='shop_edit'),
    #url(r'^(?P<id>\d+)/$', item_detail, name='edit'),
]

