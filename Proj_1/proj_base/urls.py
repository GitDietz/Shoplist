from django.urls import include, path, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from Proj_1.accounts.views import (
        login_email,
        register_view,
        logout_view,
        home_view,
        set_group)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('invite/', include(('invitation.urls', 'invitation'), namespace='invitations')),
    path('login/', login_email, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('set_group/', set_group, name='set_group'),
    path('shop/', include(('shop.urls', 'shop'), namespace='shop')),
    path('', home_view, name='home'),
    ]

if settings.DEBUG:      # ensures that this will only be done in DEV
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



