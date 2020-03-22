from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import (
        login_view,
        login_email,
        register_view,
        logout_view,
        home_view,
        set_group)
# from shop.views import merchant_list
# complaining about the absolute import

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^invite/', include(("invitation.urls",'invitation'), namespace='invitations')),
    url(r'login/', login_email, name='login'),
    url(r'logout/', logout_view, name='logout'),
    url(r'set_group/', set_group, name='set_group'),
    url(r'^shop/', include(("shop.urls",'shop'), namespace='shop')),
    url(r'register/', register_view, name='register'),
    url(r'^', home_view, name='home'),
    ]

if settings.DEBUG:      # ensures that this will only be done in DEV
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



