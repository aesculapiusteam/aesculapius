from __future__ import unicode_literals
from django.db import models
from datetime import datetime

# Create your models here.

class Profile(models.Model):
    dni = models.IntegerField()
    birth_date = models.DateField()
    adress = models.CharField()
    phone_num = models.CharField()
    enroll_date = models.CharField()
    def __init__(self, dni, birth_date, adress, phone_num, enroll_date):
        self.dni = dni
        self.birth_date = birth_date
        self.adress = adress
        self.phone_num = phone_num
        self.enroll_date = enroll_date

class Doctor(models.Model):
    profile = models.ForeignKey(Profile, related_name = "doctor")
    def __init__(self, profile)
        self.profile = Profile.objects.get(pk=profile)
