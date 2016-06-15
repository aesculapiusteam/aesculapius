from __future__ import unicode_literals
from django.db import models
from datetime import datetime

# Create your models here.

class Profile(models.Model):
    dni = models.IntegerField()
    birth_date = models.DateField()
    adress = models.CharField(max_length=256)
    phone_num = models.CharField(max_length=50)
    enroll_date = models.DateField()
    
    def __init__(self, dni, birth_date, adress, phone_num):
        self.dni = dni
        self.birth_date = birth_date
        self.adress = adress
        self.phone_num = phone_num
        self.enroll_date = datetime.now()

class Doctor(models.Model):
    profile = models.ForeignKey(Profile, related_name = "doctor")
    def __init__(self, profile)
        self.profile = Profile.objects.get(pk=profile)
