from rest_framework import serializers
from app_users.models import Profile, Employee

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    # employee = serializers.ReadOnlyField(required=False, allow_null=True)
    employee = serializers.HyperlinkedRelatedField(view_name='employee-detail', required=False, read_only=True)
    class Meta:
        model = Profile
        fields = ('url', 'employee', 'first_name', 'last_name', 'email', 'dni', 'birth_date',
        'adress', 'phone', 'cellphone', 'creation_date')

class EmployeeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    # username = serializers.CharField(source="user.username", required=True)
    class Meta:
        model = Employee
        fields = ('url', 'profile')
