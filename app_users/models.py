from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, UserManager

class Profile(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128, null=True)
    email = models.CharField(max_length=128, null=True)
    dni = models.IntegerField(null=True)
    birth_date = models.DateField(null=True)
    adress = models.CharField(max_length=256, null=True)
    phone = models.CharField(max_length=50, null=True)
    cellphone = models.CharField(max_length=50, null=True)
    creation_date = models.DateField(auto_now_add = True)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_employee")

class Doctor(Employee):
    hours = 3 #TODO Add working shifts

class Secretary(Employee):
    doctors = models.ManyToManyField(Doctor, related_name="secretary")
