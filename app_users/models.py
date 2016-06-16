from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
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
    user = GenericForeignKey("user_type", "user_id")
    content_object = generic.GenericForeignKey()

    def save(self, *args, **kwargs):
        self.create_date = datetime.now()
        super(Profile, self).save(*args, **kwargs)

class Comment(models.Model):#TODO
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

class Post(models.Model):
  comments = generic.GenericRelation('Comment')

class Picture(models.Model):
  comments = generic.GenericRelation('Comment')

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
