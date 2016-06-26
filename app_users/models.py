from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils import timezone

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
    CHARGES = (
        ("doctor", "Doctor"),
        ("secretary", "Secretary"),
    )

    user = models.OneToOneField(User)
    profile = models.OneToOneField(Profile)
    charge = models.CharField(choices=CHARGES, default='doctor', max_length=100)
    assist_ed = models.ManyToManyField('self', blank=True)

    def __unicode__(self):
        last = ""
        if self.profile.last_name != None:
            last = " " + self.profile.last_name
        return self.profile.first_name + last

    def set_assist_ed(self, who):
        """if it is a secretary use this function to set a doctor to assist"""
        if (self.charge == "doctor" and who.charge == "secretary") or (self.charge == "secretary" and who.charge == "doctor"):
            self.assist_ed.add(who)
            return self.assist_ed
        else:
            print("ERROR: Types of employees for assist relation are not compatible")

    # TODO Use __init__ instead of create. not using init because it makes
    #"profile.employee" or "user.employee" commands to not work
    def create(self, username, password, charge, email, first_name, last_name, **kwargs):
        user = User(username = username)
        user.set_password(password)
        self.user = user
        profile = Profile(first_name=first_name, last_name=last_name, email = email, **kwargs)
        self.profile = profile
        self.charge = charge
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


class Visit(models.Model):
    doctor = models.ForeignKey(Employee, unique=False, related_name='visits')
    pacient = models.ForeignKey(Profile, unique=False, related_name='visits')
    datetime = models.DateTimeField(default=timezone.now)
    detail = models.TextField()

    def __unicode__(self):
        return self.pacient.__unicode__() + " assists " + self.doctor.__unicode__()
