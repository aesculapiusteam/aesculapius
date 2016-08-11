from django.conf.urls import url, include
from app_users import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter(trailing_slash=False)
router.register(r'profile', views.ProfileViewSet)
router.register(r'employee', views.EmployeeViewSet)
router.register(r'visit', views.VisitViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]
