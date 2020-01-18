from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import (
        login_view,
        register_view,
        logout_view,
        home_view,
        set_group,
        temp_register_view)
# from shop.views import merchant_list
# complaining about the absolute import

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    # this is the future register view: url(r'register/',register_view, name='register'),
    # url(r'^accounts/',include('invitation.urls'),
    url(r'^invite/', include("invitation.urls", namespace='invitations')),
    url(r'login/', login_view, name='login'),
    url(r'logout/', logout_view, name='logout'),
    url(r'set_group/', set_group, name='set_group'),
    url(r'^shop/', include("shop.urls", namespace='shop')),
    # url(r'shop/merchant',merchant_list),
    url(r'register/', temp_register_view, name='register'),
    url(r'register_new/', register_view, name='register_new'),
    url(r'^', home_view ,name='home'),

    ]

if settings.DEBUG:      # ensures that this will only be done in DEV
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns += [
#     url(r'robot/', include('work_posts.robot_urls')),
#
#     ]

