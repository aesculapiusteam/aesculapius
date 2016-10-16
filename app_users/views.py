from app_users.models import Profile, Employee, Visit, Drug, Movement
from app_users.serializers import (
    ProfileSerializer, EmployeeSerializer, VisitSerializer,
    DrugSerializer, MovementSerializer
)
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.decorators import list_route

from app_users.permissions import IsAdminOrOwnerOrReadOnly, IsDoctor
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import django_filters

import app_users.docs as docs


class ProfileViewSet(viewsets.ModelViewSet):
    __doc__ = docs.profiles
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwnerOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('first_name', 'last_name', 'email', 'dni')
    ordering_fields = ('first_name', 'last_name', 'creation_date')
    ordering = ('first_name', 'last_name')


class EmployeeViewSet(viewsets.ModelViewSet):
    __doc__ = docs.employees
    permission_classes = (IsAuthenticated, IsAdminOrOwnerOrReadOnly,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = (
        'profile__first_name', 'profile__last_name', 'profile__email'
    )
    ordering_fields = (
        'profile__first_name', 'profile__last_name', 'charge',
        'profile__creation_date', 'profile__dni'
    )
    ordering = ('profile__first_name', 'profile__last_name')

    def get_object(self):
        if self.kwargs['pk'] == 'me':
            return self.request.user.employee
        else:
            return super(Employee, self).get_object()


class VisitViewSet(viewsets.ModelViewSet):
    __doc__ = docs.visits
    permission_classes = (IsAuthenticated, IsDoctor)
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ("doctor", "pacient")


class DrugViewSet(viewsets.ModelViewSet):
    __doc__ = docs.drugs
    permission_classes = (IsAuthenticated,)
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("name", "description", "quantity")
    filter_fields = ("name", "description", "quantity")


class MovementViewSet(viewsets.ModelViewSet):
    __doc__ = docs.movements
    permission_classes = (IsAuthenticated,)
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer
