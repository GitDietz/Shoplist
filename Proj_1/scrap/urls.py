from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import (login_view, register_view, logout_view, temp_register_view)

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    # url(r'^comments/', include("comments.urls", namespace='comments')),
    url(r'register/',register_view, name='register'),
    url(r'login/',login_view, name='login'),
    url(r'logout/',logout_view, name='logout'),
    url(r'logout/', logout_view, name='logout'),
    url(r'^shop/', include("shop.urls", namespace='shop')),
    # url(r'shop/merchant',merchant_list),
    url(r'register/', temp_register_view, name='register'),
    url(r'register_new/', register_view, name='register_new'),
    url(r'^', home_view, name='home'),

]

if settings.DEBUG:      # ensures that this will only be done in DEV
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



