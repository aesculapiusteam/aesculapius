from rest_framework import serializers
from api.models import Profile, Employee, Visit, Drug, Movement, MovementItem
from django.utils import timezone


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    # employee = serializers.ReadOnlyField(required=False, allow_null=True)
    # employee = serializers.HyperlinkedRelatedField(view_name='api:employee-detail', required=False, read_only=True)
    employee = serializers.ReadOnlyField(
        source="employee.id", required=False, read_only=True
    )

    class Meta:
        model = Profile
        fields = (
            'id', 'employee', 'first_name', 'last_name', 'email', 'dni', 'birth_date',
            'address', 'phone', 'cellphone', 'creation_date'
        )
        extra_kwargs = {'url': {'view_name': 'api:profile-detail'}}


class EmployeeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    username = serializers.CharField(source="user.username", required=True)
    password = serializers.CharField(
        source="user.password", write_only=True,
        required=False, style={'input_type': 'password'}
    )

    class Meta:
        model = Employee
        fields = (
            'id', 'username', 'password', 'charge', 'assist_ed', 'profile'
        )
        extra_kwargs = {'url': {'view_name': 'api:employee-detail'}}

    def create(self, validated_data):
        profile = validated_data["profile"]
        user = validated_data["user"]
        assist_ed = validated_data['assist_ed']
        employee = Employee().create(
            username=user['username'],
            password=user['password'],
            charge=validated_data['charge'],
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


class VisitSerializer(serializers.ModelSerializer):
    doctor = serializers.ReadOnlyField(source="doctor.id")
    doctor_name = serializers.ReadOnlyField(source="doctor.__unicode__")
    patient_name = serializers.ReadOnlyField(source="patient.__unicode__")
    datetime = serializers.ReadOnlyField()

    class Meta:
        model = Visit
        fields = (
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name', 'datetime', 'detail'
        )

    def create(self, validated_data):
        validated_data['doctor'] = self.context['request'].user.employee
        res = super(VisitSerializer, self).create(validated_data)
        return res

    def update(self, instance, validated_data):
        validated_data['datetime'] = timezone.now()
        validated_data.pop('patient', None)
        res = super(VisitSerializer, self).update(instance, validated_data)
        return res


class DrugSerializer(serializers.ModelSerializer):

    class Meta:
        model = Drug
        fields = ('id', 'name', 'description', 'quantity')


class MovementItemSerializer(serializers.ModelSerializer):
    drug_name = serializers.CharField(source='drug.name', read_only=True)

    class Meta:
        model = MovementItem
        fields = (
            'id', 'detail', 'is_donation', 'movement_type',
            'drug', 'drug_name', 'drug_quantity', 'cash'
        )


class MovementSerializer(serializers.ModelSerializer):
    items = MovementItemSerializer(many=True)
    datetime = serializers.ReadOnlyField()
    employee = serializers.ReadOnlyField(source="employee.id")
    employee_name = serializers.ReadOnlyField(source="employee.__unicode__")
    profile_name = serializers.ReadOnlyField(source="profile.__unicode__")

    class Meta:
        model = Movement
        fields = (
            'id', 'employee', 'employee_name', 'profile',
            'profile_name', 'datetime', 'items'
        )

    def create(self, validated_data):
        movement = Movement(
            employee=self.context['request'].user.employee,
            profile=validated_data['profile']
        )
        items_toadd = []

        if not (validated_data['items'] and len(validated_data['items']) > 0):
            print("\n\n\tYou should pass at least one item\n\n")
            return

        for i in validated_data['items']:
            item = MovementItem()
            item.detail = i.get('detail', '')
            item.is_donation = i.get('is_donation', False)
            item.movement_type = i.get('movement_type', 0)
            if not item.movement_type:
                if not ('drug' in i and 'drug_quantity' in i):
                    print("\n\n\tYou should pass drug and drug_quantity properties\n\n")
                    return
                item.drug = i['drug']
                item.drug_quantity = i['drug_quantity']
            else:
                if not ('cash' in i):
                    print("\n\n\tYou should pass cash property\n\n")
                    return
                item.cash = i['cash']
            items_toadd.append(item)

        movement.save()
        for item in items_toadd:
            item.movement = movement
            item.save()

        return movement

    def update(self, movement, validated_data):
        # Don't allow updates on movements
        return movement
