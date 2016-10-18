from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^api/session-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/token-auth/', views.obtain_auth_token),
]
