from django.conf.urls import url
from app_users import views

urlpatterns = [
	url(r'^get_users/$', views.get_users, name='get_users'),
]
