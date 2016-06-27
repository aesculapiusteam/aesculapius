from app_users.models import Profile, Employee, Visit
from app_users.serializers import ProfileSerializer, EmployeeSerializer, VisitSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from app_users.permissions import IsAdminOrOwnerOrReadOnly, IsDoctor
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class ProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwnerOrReadOnly, )


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    permission_classes = (IsAuthenticated, IsAdminOrOwnerOrReadOnly,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class VisitViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    permission_classes = (IsAuthenticated, IsDoctor)
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
