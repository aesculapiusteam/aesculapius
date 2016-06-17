from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('app_main.urls', namespace='app_main')),
    url(r'^users/', include('app_users.urls', namespace='app_users')),
    ]
urlpatterns.append(url(r'^admin/', admin.site.urls))

# if settings.DEBUG: #TODO Remove
    # urlpatterns.append(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
    # urlpatterns.append(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
