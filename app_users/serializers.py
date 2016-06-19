from rest_framework import serializers
from app_users.models import Profile, Secretary, Employee, Doctor
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    # employee = serializers.ReadOnlyField(source='employee')
    class Meta:
        model = Profile
        fields = ('url', 'employee', 'first_name', 'last_name', 'email', 'dni', 'birth_date',
            'adress', 'phone', 'cellphone', 'creation_date')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # employee = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    class Meta:
        model = User
        fields = ('url', 'username', 'email')

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('url', 'user', 'profile')

class DoctorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Doctor
        fields = ('url', 'user', 'profile', 'hours')

class SecretarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Secretary
        fields = ('url', 'user', 'profile', 'doctors')
