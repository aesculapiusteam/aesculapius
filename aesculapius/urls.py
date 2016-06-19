from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('app_users.urls', namespace='api')),
    url(r'^', include('app_main.urls')),
]
