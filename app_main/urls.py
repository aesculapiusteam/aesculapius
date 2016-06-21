from django.conf.urls import url
import app_main.views
urlpatterns = [
    url(r'^', app_main.views.home, name='home'),
    ]
