from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import (login_view, register_view, logout_view, home_view, temp_register_view)
# from shop.views import merchant_list
# complaining about the absolute import

urlpatterns = [


    url(r'^admin/', admin.site.urls),
    #url(r'^comments/', include("comments.urls", namespace='comments')),
    # this is the future register view: url(r'register/',register_view, name='register'),

    url(r'login/',login_view, name='login'),
    url(r'logout/',logout_view, name='logout'),
    url(r'^shop/',include("shop.urls", namespace='shop')),
    # url(r'shop/merchant',merchant_list),
    url(r'^',home_view ,name='home'),
    url(r'register/',temp_register_view, name='register'),
    #url(r'^', include("work_posts.urls")),
    # this includes the urls file under the work_post folder, but only the part after "posts/"
    # in work_posts.urls you will only see the remaining part so posts/delete is split and routed
    ]

if settings.DEBUG:      # ensures that this will only be done in DEV
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns += [
#     url(r'robot/', include('work_posts.robot_urls')),
#
#     ]

