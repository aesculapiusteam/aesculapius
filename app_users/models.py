from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, UserManager

class Profile(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128, null=True)
    email = models.CharField(max_length=128, null=True)
    dni = models.IntegerField(null=True)
    birth_date = models.DateField(null=True)
    address = models.CharField(max_length=256, null=True)
    phone = models.CharField(max_length=50, null=True)
    cellphone = models.CharField(max_length=50, null=True)
    creation_date = models.DateField(auto_now_add = True)

    def __unicode__(self):
        last = ""
        if self.last_name != None:
            last = " " + self.last_name
        return self.first_name + last

    def delete(self):
        if hasattr(self, 'employee'): # Is a employee profile
            User.objects.get(pk=self.employee.user.pk).delete()
        super(Profile, self).delete()

class Employee(models.Model):
    user = models.OneToOneField(User)
    profile = models.OneToOneField(Profile)

    # TODO Use __init__ instead of create. using init normally makes
    #"profile.employee" or "user.employee" commands to not work
    def __unicode__(self):
        last = ""
        if self.profile.last_name != None:
            last = " " + self.profile.last_name
        return self.profile.first_name + last

    def create(self, username, password, email, first_name, last_name, **kwargs):
        # super(Employee, self).__init__(**kwargs)
        user = User(username = username)
        user.set_password(password)
        self.user = user
        profile = Profile(first_name=first_name, last_name=last_name, email = email, **kwargs)
        self.profile = profile
        return self

    def save(self, **kwargs):
        self.profile.save()
        self.user.save()
        self.profile_id = self.profile.id
        self.user_id = self.user.id
        super(Employee, self).save(**kwargs)

    def delete(self):
        User.objects.get(pk=self.user.pk).delete()
        Profile.objects.get(pk=self.profile.pk).delete()
        super(Employee, self).delete()

class Doctor(Employee):
    hours = 3 #TODO Add working shifts

class Secretary(Employee):
    doctors = models.ManyToManyField(Doctor, related_name="secretary")
