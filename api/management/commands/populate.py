from django.core.management.base import BaseCommand
from api.models import Profile, Employee, Visit
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Populate the database with some initial entries for Profile, Employees and Visits'

    def handle(self, *args, **options):
        # Admin
        a = Employee().create(
            username="admin",
            password="admin",
            charge="secretary",
            first_name="Administrador",
            last_name="de Aesculapius"
        )
        a.user.is_superuser = True
        a.user.is_staff = True
        a.save()
        a.user.save()

        # Employees
        s = Employee().create(
            username="secretaria",
            password="secretaria",
            charge="secretary",
            first_name="Secretaria Marta",
            last_name="Mocha",
            email=None
        )
        s1 = Employee().create(
            username="secretaria1",
            password="secretaria1",
            charge="secretary",
            first_name="Secretaria Olga",
            last_name="Mora",
            email=None
        )

        d = Employee().create(
            username="doctor",
            password="doctor",
            charge="doctor",
            first_name="Medica Romina",
            last_name="Valestrini",
            email=None
        )
        d1 = Employee().create(
            username="doctor1",
            password="doctor1",
            charge="doctor",
            first_name="Medico Ricardo",
            last_name="Morales",
            email=None
        )
        d5 = Employee().create(
            username="nomUser",
            password="contra",
            charge="doctor",
            first_name="Medico Ricardao",
            last_name="Moraleas",
            email=None
        )

        d5.save()
        s.save()
        s1.save()
        d.save()
        d1.save()

        s.set_assist_ed(d)
        d1.set_assist_ed(s1)

        # Pacients
        p = Profile(first_name="Diego", last_name="Velinsky")
        p1 = Profile(first_name="Maria", last_name="de la Fuente")
        p2 = Profile(first_name="Pedro", last_name="Pitaria")
        p.save()
        p1.save()
        p2.save()

        # Visits
        v = Visit(doctor=d, pacient=p, detail="Tenia gripe y le di antibiotico")
        v1 = Visit(doctor=d, pacient=p1, detail="Tenia fiebre y lo deje en cuarentena")
        v2 = Visit(doctor=d, pacient=p2, detail="Le dolia la cabeza y le di bayaspirina")
        v3 = Visit(doctor=d1, pacient=p, detail="Seguia con gripe y le di mas antibiotico")
        v4 = Visit(doctor=d1, pacient=p, detail="La gripe no ceso y lo mande al hospital")
        v5 = Visit(doctor=d1, pacient=p1, detail="Luego de la cuarentena murio")
        v.save()
        v1.save()
        v2.save()
        v3.save()
        v4.save()
        v5.save()
