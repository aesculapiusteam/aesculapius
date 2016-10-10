from rest_framework import serializers
from app_users.models import Profile, Employee, Visit
from django.utils import timezone

class ProfileBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'dni', 'email')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    # employee = serializers.ReadOnlyField(required=False, allow_null=True)
    # employee = serializers.HyperlinkedRelatedField(view_name='api:employee-detail', required=False, read_only=True)
    employee = serializers.ReadOnlyField(source="employee.id", required=False, read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'employee', 'first_name', 'last_name', 'email', 'dni', 'birth_date',
        'address', 'phone', 'cellphone', 'creation_date')
        extra_kwargs = {'url': {'view_name': 'api:profile-detail'}}

class EmployeeBriefSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_email(self, employee):
        return employee.profile.email

    def get_full_name(self, employee):
        return employee.__unicode__()

    class Meta:
        model = Employee
        fields = ('id', 'charge', 'full_name', 'email')

class EmployeeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    username = serializers.CharField(source="user.username", required=True)
    password = serializers.CharField(source="user.password", write_only=True,
        required=False, style={'input_type': 'password'}
    )

    class Meta:
        model = Employee
        fields = ('id', 'username', 'password', 'charge', 'assist_ed', 'profile')
        extra_kwargs = {'url': {'view_name': 'api:employee-detail'}}

    def create(self, validated_data):
        profile = validated_data["profile"]
        user = validated_data["user"]
        assist_ed = validated_data['assist_ed']
        employee = Employee().create(
            username = user['username'],
            password = user['password'],
            charge = validated_data['charge'],
            **profile
        )
        employee.save()
        for i in assist_ed:
            employee.set_assist_ed(i)
        return employee

    def update(self, employee, validated_data):
        profile = validated_data["profile"]
        user = validated_data["user"]
        assist_ed = validated_data['assist_ed']
        employee.user.username = user['username']
        if 'password' in user:
            if not (employee.user.password == user['password']):
                employee.user.set_password(user['password'])
        employee.charge = validated_data['charge']
        employee.profile.first_name = profile['first_name']
        employee.profile.last_name = profile['last_name']
        employee.profile.email = profile['email']
        employee.profile.dni = profile['dni']
        employee.profile.birth_date = profile['birth_date']
        employee.profile.address = profile['address']
        employee.profile.phone = profile['phone']
        employee.profile.cellphone = profile['cellphone']
        employee.save()
        employee.assist_ed.clear()
        for i in assist_ed:
            employee.set_assist_ed(i)
        return employee

class VisitBriefSerializer(serializers.ModelSerializer):
    doctor_name = serializers.SerializerMethodField()
    detail_summary = serializers.SerializerMethodField()

    def get_doctor_name(self, visit):
        return Employee.objects.get(id=visit.doctor.id).__unicode__()

    def get_detail_summary(self, visit):
        return (visit.detail[:45] + '..') if len(visit.detail) > 45 else visit.detail

    class Meta:
        model = Visit
        fields = ('id', 'datetime', 'doctor_name', 'detail_summary')

class VisitSerializer(serializers.ModelSerializer):
    doctor = serializers.ReadOnlyField(source="doctor.id")
    datetime = serializers.ReadOnlyField()

    class Meta:
        model = Visit
        fields = ('id', 'pacient', 'doctor', 'datetime', 'detail')

    def create(self, validated_data):
        validated_data['doctor'] = self.context['request'].user.employee
        res = super(VisitSerializer, self).create(validated_data)
        return res

    def update(self, instance, validated_data):
        validated_data['datetime'] = timezone.now()
        validated_data.pop('pacient', None)
        res = super(VisitSerializer, self).update(instance, validated_data)
        return res
