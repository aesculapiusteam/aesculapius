from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from datetime import datetime

class Profile(models.Model):
    dni = models.IntegerField()
    birth_date = models.DateField()
    adress = models.CharField(max_length=256)
    phone_num = models.CharField(max_length=50)
    create_date = models.DateField()
    user_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
        related_name="profile")
    user_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("user_type", "user_id")

    def save(self, *args, **kwargs):
        self.create_date = datetime.now()
        super(Profile, self).save(*args, **kwargs)

class Pacient(models.Model):
    clinic_history = None #TODO

class Employe(models.Model):
    #TODO Importar de django auth
    user = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

class Doctor(models.Model):
    horario = None # TODO

class Secretary(models.Model):
    doctors = models.ManyToManyField(Doctor, related_name="doctor")
