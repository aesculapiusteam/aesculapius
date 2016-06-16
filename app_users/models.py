from __future__ import unicode_literals
from django.db import models
# from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
# from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, UserManager
from datetime import datetime

class Profile(models.Model):
    first_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    email = models.CharField(max_length=128, null=True)

    dni = models.IntegerField(null=True)
    birth_date = models.DateField(null=True)
    adress = models.CharField(max_length=256, null=True)
    phone = models.CharField(max_length=50, null=True)
    cellphone = models.CharField(max_length=50, null=True)
    creation_date = models.DateField(auto_now_add = True)

    # content_type = models.ForeignKey(ContentType, null=True)
    # object_id = models.PositiveIntegerField(null=True)
    # user = GenericForeignKey("content_type", "object_id")

    # def save(self, *args, **kwargs):
    #     self.creation_date = datetime.now()
    #     super(Profile, self).save(*args, **kwargs)

class Pacient(Profile):
    #Es una clase separada por que va a tener funciones especiales como getHC
    # profile = GenericRelation('Profile', related_query_name='profile')
    def __str__():
        return "Pacient: " + this.name

class Employee(Profile):
    #TODO Importar de django auth
    user = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    def __str__():
        return "Pacient: " + this.name
    # profile = GenericRelation('Profile', related_query_name='profile')

class Doctor(Employee):
    hours = None # TODO

class Secretary(Employee):
    doctors = models.ManyToManyField(Doctor, related_name="doctor")

# paciente = Pacient()
# paciente.profile.create(dni=40987366, adress="Duarte quiros 5647")
# paciente.save()
