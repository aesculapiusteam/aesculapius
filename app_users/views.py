from app_users.models import Profile, Employee
from app_users.serializers import ProfileSerializer, EmployeeSerializer
from rest_framework.response import Response
from rest_framework import viewsets

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
