from rest_framework import serializers
from app_users.models import Profile, Employee
from django.contrib.auth.models import User


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    # employee = serializers.ReadOnlyField(source='employee')
    class Meta:
        model = Profile
        fields = ('url', 'employee', 'first_name', 'last_name', 'email', 'dni', 'birth_date',
            'adress', 'phone', 'cellphone', 'creation_date')

class EmployeeSerializer(serializers.ModelSerializer):
    profile = serializers.HyperlinkedRelatedField(view_name='profile-detail', read_only=True)
    class Meta:
        model = Employee
        fields = ('url', 'user', 'profile')
        # ('url','username', 'first_name', 'last_name', 'email', 'dni', 'birth_date',
        #     'adress', 'phone', 'cellphone', 'creation_date')
