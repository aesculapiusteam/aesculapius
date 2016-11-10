from django.conf.urls import url, include
from django.contrib import admin
from aesculapius import views
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^api/session-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/token-auth/', views.obtain_auth_token),
    url(r'^$', RedirectView.as_view(url='/api/'), name='home'),
]
