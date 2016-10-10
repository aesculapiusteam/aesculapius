from app_users.models import Profile, Employee, Visit
from app_users.serializers import (
    ProfileSerializer, EmployeeSerializer, VisitSerializer, EmployeeMoreSerializer,
    VisitBriefSerializer, ProfileBriefSerializer
)
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.decorators import list_route

from app_users.permissions import IsAdminOrOwnerOrReadOnly, IsDoctor
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import django_filters



class ProfileViewSet(viewsets.ModelViewSet):
    """
    # Permissions for Profile
    *All permissions listed below have to be true in order to give access to the
    client*

    ### IsAuthenticated
    - All permissions are allowed if the user is not anonymous (is authenticated)

    ### IsAdminOrOwnerOrReadOnly
    - All read permissions are allowed to any user for any object
    - All write permissions are allowed to Admin users for any object
    - All write permissions are allowed to any user for objects that are not
        related to system users
    - Object write permissions are allowed only to the user that owns that
        profile or employee object for objects **related to/that are** employees


    # Profile Serializer
    - id (IntegerField)
    - **first_name** (CharField) This field is the only required for having a
        profile in the system
    - last_name (CharField)
    - email (CharField)
    - dni (IntegerField)
    - birth_date (TimestampField)
    - address (CharField)
    - phone (CharField)
    - cellphone (CharField)
    - creation_date (TimestampField)
    - **employee** (IntegerField) If this profile is from an employee, this is
        the employee id
    # Profile SearchFilter and OrderingFilter
    - **filter_backends** Filters that the API  will be using
    - search_fields
    - ordering_fields
    - **ordering** Default ordering that the API will use for the view
    # Pagination
    - **limit** Sets a limit of items in a page, (USAGE: /api/somelist?limit=5 (sets 5 item pages))
    - **offset** Goes to the number given of the item (USAGE: /api/somelist?limit=5&offset=10 (sets 5 item pages and goes to the 10th item))
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileBriefSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwnerOrReadOnly, )
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('first_name', 'last_name', 'email', 'dni')
    ordering_fields = ('first_name', 'last_name', 'creation_date')
    ordering = ('first_name', 'last_name')

    @detail_route()
    def more(self, request, pk):
        profile = self.get_object()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    # Permissions for Employee
    *All permissions listed below have to be true in order to give access to the
    client*

    ### IsAuthenticated
    - All permissions are allowed if the user is not anonymous (is authenticated)

    ### IsAdminOrOwnerOrReadOnly
    - All read permissions are allowed to any user for any object
    - All write permissions are allowed to Admin users for any object
    - All write permissions are allowed to any user for objects that are not
        related to system users
    - Object write permissions are allowed only to the user that owns that
        profile or employee object for objects **related to/that are** employees

    # Employee Serializer
    - id (IntegerField)
    - **username** (CharField) Comes from user.username
    - **charge** (CharField) Can be either 'doctor' or 'secretary'
    - **assist_ed** (ManyToManyField)
        - If employee.charge == 'doctor' assist_ed represents which secretaries
            assist this doctor (secretaries employee id), it can be empty.
        - If employee.charge == 'secretary' assist_ed represents which doctors
            this secretary attends (doctors employee id), it can be empty,
            but shouldn't.
    - **profile** (OneToOneField) Is a copy of the profile that corresponds to
        this employee, it can be accessed from /profile/<employee.profile.id>
    # Employee SearchFilter and OrderingFilter
    - **filter_backends** Filters that the API  will be using
    - search_fields
    - ordering_fields
    - **ordering** Default ordering that the API will use for the view
    # Pagination
    - **limit** Sets a limit of items in a page, (USAGE: /api/somelist?limit=5 (sets 5 item lists))
    - **offset** Goes to the number given of the item (USAGE: /api/somelist?limit=5&offset=10 (sets 5 item lists and goes to the 10th item))
    """
    permission_classes = (IsAuthenticated, IsAdminOrOwnerOrReadOnly,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('profile__first_name', 'profile__last_name', 'profile__email')
    ordering_fields = ('profile__first_name', 'profile__last_name', 'charge',
        'profile__creation_date', 'profile__dni'
    )
    ordering = ('profile__first_name', 'profile__last_name')

    # @detail_route()
    # def brief(self, request, pk):
    #     employee = self.get_object()
    #     serializer = EmployeeBriefSerializer(employee)
    #     return Response(serializer.data)

    @list_route()
    def more(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeMoreSerializer(employees, many=True)
        return Response(serializer.data)

class VisitViewSet(viewsets.ModelViewSet):
    """
    # Permissions for Visit
    *All permissions listed below have to be true in order to give access to the
    client*

    ### IsAuthenticated
    - All permissions are allowed if the user is not anonymous (is authenticated)

    ### IsDoctor
    - All read permissions are allowed to any user for any object
    - All write permissions are allowed to admin users for any object
    - All write permissions are allowed to doctor users for any non Visit object
    - All write permissions are allowed to doctor users only for Visits that the
        same doctor generated.

    # Visit Serializer
    - **doctor** (IntegerField) Id that represents the doctor of the visit
    - **pacient** (IntegerField) Id that represents the pacient of the visit
    - datetime (TimestampField)
    - detail (TextField)
    """
    permission_classes = (IsAuthenticated, IsDoctor)
    queryset = Visit.objects.all()
    serializer_class = VisitBriefSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ("doctor", "pacient")

    @detail_route()
    def more(self, request, pk):
        visit = self.get_object()
        serializer = VisitSerializer(visit)
        return Response(serializer.data)
