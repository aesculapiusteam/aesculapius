from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from datetime import datetime


class Profile(models.Model):
    dni = models.IntegerField()
    birth_date = models.DateField()
    adress = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=50)
    create_date = models.DateField()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    user = generic.GenericForeignKey("content_type", "object_id")

    def save(self, *args, **kwargs):
        self.create_date = datetime.now()
        super(Profile, self).save(*args, **kwargs)

class Pacient(models.Model):
    profile = generic.GenericRelation('Profile')
    clinic_history = None #TODO

class Employee(models.Model):
    #TODO Importar de django auth
    user = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    profile = generic.GenericRelation('Profile')

class Doctor(models.Model):
    horario = None # TODO

class Secretary(models.Model):
    doctors = models.ManyToManyField(Doctor, related_name="doctor")
