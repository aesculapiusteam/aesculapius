from django.conf.urls import url, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'visits', views.VisitViewSet)
router.register(r'drugs', views.DrugViewSet)
router.register(r'movements', views.MovementViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
