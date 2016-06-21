from rest_framework import serializers
from app_users.models import Profile, Employee

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    # employee = serializers.ReadOnlyField(required=False, allow_null=True)
    employee = serializers.HyperlinkedRelatedField(view_name='api:employee-detail', required=False, read_only=True)
    class Meta:
        model = Profile
        fields = ('url', 'employee', 'first_name', 'last_name', 'email', 'dni', 'birth_date',
        'address', 'phone', 'cellphone', 'creation_date')
        extra_kwargs = {'url': {'view_name': 'api:profile-detail'}}

class EmployeeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    username = serializers.CharField(source="user.username", required=True)
    password = serializers.CharField(source="user.password", write_only=True, required=True, style={'input_type': 'password'})
    class Meta:
        model = Employee
        fields = ('url', 'username', 'password', 'profile')
        extra_kwargs = {'url': {'view_name': 'api:employee-detail'}}

    def create(self, validated_data):
        profile = validated_data["profile"]
        user = validated_data["user"]

        employee = Employee().create(
            username = user['username'],
            password = user['password'],
            first_name = profile['first_name'],
            last_name = profile['last_name'],
            email = profile['email'],
            dni = profile['dni'],
            birth_date = profile['birth_date'],
            address = profile['address'],
            phone = profile['phone'],
            cellphone = profile['cellphone'],
        )
        employee.save()
        return employee

    def update(self, employee, validated_data):
        profile = validated_data["profile"]
        user = validated_data["user"]
        employee.user.username = user['username']
        if not employee.user.password == user['password']:
            employee.user.set_password(user['password'])
        employee.profile.first_name = profile['first_name']
        employee.profile.last_name = profile['last_name']
        employee.profile.email = profile['email']
        employee.profile.dni = profile['dni']
        employee.profile.birth_date = profile['birth_date']
        employee.profile.address = profile['address']
        employee.profile.phone = profile['phone']
        employee.profile.cellphone = profile['cellphone']
        employee.save()
        return employee
