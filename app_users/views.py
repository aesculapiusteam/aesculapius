from django.contrib.auth.models import User
from app_users.models import Profile, Employee
from app_users.serializers import ProfileSerializer, UserSerializer, EmployeeSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import renderers
from rest_framework.decorators import detail_route

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class EmployeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
