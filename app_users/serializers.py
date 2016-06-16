from rest_framework import serializers
from app_users.models import Profile, Secretary, Pacient, Employe, Doctor


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('dni', 'birth_date', 'adress', 'phone_number', 'create_date', 'user_type', 'user_id', 'content_object')

class PacientSerializer(models.Model):
    class Meta:
        model = Pacient
        fields = ('clinic_history')

class EmployeeSerializer(models.Model):
    class Meta:
        model = Employe
        fields =

class DoctorSerializer(models.Model):
    class Meta:
        model = Doctor
        fields =

class SecretarySerializer(models.Model):
    class Meta:
        model = Secretary
        fields =
