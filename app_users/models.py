from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, UserManager

class Profile(models.Model):
    #TODO hacer que firstname, lastname y email se repliquen de user
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
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    # TODO Use __init__ instead of create. using init normally makes
    #"profile.employee" or "user.employee" commands to not work properly
    def create(self, username, password, email, first_name, last_name, **kwargs):
        super(Employee, self).__init__(**kwargs)
        user = User(username = username, email = email)
        user.set_password(password)
        self.user = user
        profile = Profile(first_name=first_name, last_name=last_name, **kwargs)
        self.profile = profile
        return self

    def save(self, **kwargs):
        self.user.save()
        self.user_id = self.user.id
        self.profile.save()
        self.profile_id = self.profile.id
        super(Employee, self).save(**kwargs)

class Doctor(Employee):
    hours = 3 #TODO Add working shifts

class Secretary(Employee):
    doctors = models.ManyToManyField(Doctor, related_name="secretary")
