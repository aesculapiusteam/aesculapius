from app_users.models import Profile, Employee, Visit
from app_users.serializers import ProfileSerializer, EmployeeSerializer, VisitSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from app_users.permissions import IsAdminOrOwnerOrReadOnly, IsDoctor
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters



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
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwnerOrReadOnly, )
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('first_name', 'last_name', 'email')
    ordering_fields = ('first_name', 'last_name')
    ordering = ('first_name',)


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
    """
    permission_classes = (IsAuthenticated, IsAdminOrOwnerOrReadOnly,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('profile__first_name', 'profile__last_name', 'profile__email')
    ordering_fields = ('profile__first_name', 'profile__last_name', 'charge')
    ordering = ('profile__first_name',)


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
    serializer_class = VisitSerializer
