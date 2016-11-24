from api.models import Profile, Employee, Visit, Drug, Movement
from api.serializers import (
    ProfileSerializer, EmployeeSerializer, VisitSerializer,
    DrugSerializer, MovementSerializer
)
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.decorators import list_route

from api.permissions import (
    IsAdminOrOwnerOrReadOnly, IsDoctor, IsReadOnlyOrPost, IsNotDeleted, IsLTOneWeekOld
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import django_filters

import api.docs as docs


class ProfileViewSet(viewsets.ModelViewSet):
    # __doc__ = docs.profiles
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwnerOrReadOnly, IsNotDeleted)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, filters.DjangoFilterBackend)
    filter_fields = ('is_deleted',)
    search_fields = ('first_name', 'last_name', 'email', 'dni')
    ordering_fields = ('first_name', 'last_name', 'creation_date')
    ordering = ('first_name', 'last_name')

    def get_queryset(self):
        if self.action == 'list': # If listing, show only non deleted records
            show_deleted = self.request.query_params.get('is_deleted', False)
            return Profile.objects.filter(is_deleted=show_deleted)
        return super(ProfileViewSet, self).get_queryset()

    def perform_destroy(self, profile):
        profile.soft_delete()

class EmployeeViewSet(viewsets.ModelViewSet):
    # __doc__ = docs.employees
    permission_classes = (IsAuthenticated, IsAdminOrOwnerOrReadOnly, IsNotDeleted)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, filters.DjangoFilterBackend,)
    search_fields = (
        'profile__first_name', 'profile__last_name', 'profile__email'
    )
    ordering_fields = (
        'profile__first_name', 'profile__last_name', 'charge',
        'profile__creation_date', 'profile__dni'
    )
    ordering = ('profile__first_name', 'profile__last_name')
    filter_fields = ('profile__is_deleted',)

    def get_object(self):
        if self.kwargs['pk'] == 'me':
            return self.request.user.employee
        else:
            return super(EmployeeViewSet, self).get_object()

    def get_queryset(self):
        if self.action == 'list': # If listing, show only non deleted records
            show_deleted = self.request.query_params.get('is_deleted', False)
            return Employee.objects.filter(profile__is_deleted=show_deleted)
        return super(EmployeeViewSet, self).get_queryset()

    def perform_destroy(self, employee):
        employee.profile.soft_delete()

class VisitViewSet(viewsets.ModelViewSet):
    # __doc__ = docs.visits
    permission_classes = (IsAuthenticated, IsDoctor, IsNotDeleted, IsLTOneWeekOld)
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('doctor', 'patient', 'is_deleted')

    def get_queryset(self):
        if self.action == 'list': # If listing, show only non deleted records
            show_deleted = self.request.query_params.get('is_deleted', False)
            return Visit.objects.filter(is_deleted=show_deleted)
        return super(VisitViewSet, self).get_queryset()

    def perform_destroy(self, visit):
        visit.soft_delete()


class DrugViewSet(viewsets.ModelViewSet):
    # __doc__ = docs.drugs
    permission_classes = (IsAuthenticated, IsNotDeleted)
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    filter_backends = (
        filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter
    )
    search_fields = ('name', 'description', 'quantity')
    filter_fields = ('name', 'description', 'quantity')
    ordering_fields = ('name', 'description', 'quantity')
    ordering = ('name', 'description', 'quantity')


class MovementViewSet(viewsets.ModelViewSet):
    # __doc__ = docs.movements
    permission_classes = (IsAuthenticated, IsReadOnlyOrPost, IsNotDeleted)
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer
    filter_backends = (
        filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter
    )
    search_fields = ('employee__profile__first_name', 'profile__first_name',
    'employee__profile__last_name', 'profile__last_name','items__drug__name', 'datetime')
    filter_fields = ('employee', 'profile')
    ordering = ('-datetime',)
