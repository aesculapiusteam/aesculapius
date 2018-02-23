from __future__ import unicode_literals
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils import timezone


class Aesculapius(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.0))

    def refresh_balance(self):
        for i in MovementItem.objects.filter(movement_type=1):
            self.balance += i.cash if i.is_donation else -(i.cash)

    def save(self, **kwargs):
        "Reads throw all movements and calculates the real balance."
        if self.pk is None: # The object is being saved for the first time (being created)
            self.refresh_balance()
        super(Aesculapius, self).save(**kwargs)

class Profile(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128, null=True, blank=True)
    email = models.CharField(max_length=128, null=True, blank=True)
    dni = models.IntegerField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    cellphone = models.CharField(max_length=50, null=True, blank=True)
    creation_datetime = models.DateTimeField(auto_now_add=True, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)
    healthcare = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        last = ""
        if self.last_name != None:
            last = " " + self.last_name
        return self.first_name + last

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def delete(self):
        """
        Delete the corresponding user of the profile (if it's a employee
        profile) the Employee object is being automatically deleted
        """
        if hasattr(self, 'employee'):  # Is a employee profile
            User.objects.get(pk=self.employee.user.pk).delete()
        super(Profile, self).delete()


class Employee(models.Model):
    CHARGES = (
        #("option", "what will appear on the api page")
        ("doctor", "Doctor"),
        ("secretary", "Secretary"),
    )

    user = models.OneToOneField(User)
    profile = models.OneToOneField(Profile)
    charge = models.CharField(
        choices=CHARGES, default='doctor', max_length=100)
    assist_ed = models.ManyToManyField('self', blank=True)

    def __unicode__(self):
        last = ""
        if self.profile.last_name != None:
            last = " " + self.profile.last_name
        return self.profile.first_name + last

    def set_assist_ed(self, who):
        """
        if employee is a secretary use this function to set a doctor to assist
        or viceversa
        """
        if (self.charge == "doctor" and who.charge == "secretary") or (self.charge == "secretary" and who.charge == "doctor"):
            self.assist_ed.add(who)
            return self.assist_ed
        else:
            print("ERROR: Types of employees for assist relation are not compatible")

    # TODO Use __init__ instead of create. not using init because it makes
    #"profile.employee" or "user.employee" commands to not work
    def create(self, username, password, charge, **kwargs):
        """
        Creates a Employee and its corresponding User and Profile objects
        """
        user = User(username=username)
        user.set_password(password)
        self.user = user
        profile = Profile(**kwargs)
        self.profile = profile
        self.charge = charge
        return self

    def save(self, **kwargs):
        """
        Makes sure that the User and Profile of the employee are saved too
        after using the self.create() method.
        """
        self.profile.save()
        self.user.save()
        self.profile_id = self.profile.id
        self.user_id = self.user.id
        super(Employee, self).save(**kwargs)

    def soft_delete(self):
        self.profile.is_deleted = True
        self.save()

    def delete(self):
        """
        Makes sure the User and the Profile of the employee are deleted too
        """
        User.objects.get(pk=self.user.pk).delete()
        Profile.objects.get(pk=self.profile.pk).delete()
        super(Employee, self).delete()


class Visit(models.Model):
    doctor = models.ForeignKey(Employee, unique=False, related_name='visits')
    patient = models.ForeignKey(Profile, unique=False, related_name='visits')
    datetime = models.DateTimeField(default=timezone.now)
    detail = models.TextField()
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def __unicode__(self):
        return unicode(self.patient) + " visited " + unicode(self.doctor) + " on " + self.datetime.ctime()


class Drug(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name + ': ' + unicode(self.quantity)


class Movement(models.Model):
    employee = models.ForeignKey(Employee, related_name='movements')
    profile = models.ForeignKey(Profile, related_name='movements')
    datetime = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return unicode(self.id) + ' - ' + unicode(self.employee) + ' -> ' + unicode(self.profile)

class MovementItem(models.Model):
    movement = models.ForeignKey(Movement, related_name='items')
    detail = models.TextField(default="", blank=True)
    is_donation = models.BooleanField(default=False)
    movement_type = models.IntegerField(
        choices=[(0, 'Medicamento'), (1, 'Dinero')], default=0
    )
    drug = models.ForeignKey(Drug, related_name='movement_items', null=True)
    drug_quantity = models.PositiveSmallIntegerField(null=True)
    cash = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def save(self, **kwargs):
        if self.movement_type == 0: # Drugs
            # This line is necessary, can't modify self.drug correctly.
            drug = Drug.objects.get(pk=self.drug.pk)
            if self.is_donation:
                drug.quantity += self.drug_quantity
            else:
                drug.quantity -= self.drug_quantity
            drug.save()
        if self.movement_type == 1: # Money
            balance_singleton, new = Aesculapius.objects.get_or_create()
            balance_singleton.balance += self.cash if self.is_donation else -(self.cash)
            balance_singleton.save()
        super(MovementItem, self).save(**kwargs)

class Issue(models.Model):
    employee = models.ForeignKey(Employee, related_name='issues')
    creation_datetime = models.DateTimeField(auto_now_add=True, blank=True)
    title = models.CharField(max_length=256)
    content = models.TextField(default="", blank=True)
