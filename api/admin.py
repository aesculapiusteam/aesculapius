from django.contrib import admin
from api.models import Aesculapius, Profile, Employee, Visit, Drug, Movement, MovementItem

admin.site.register(Aesculapius)
admin.site.register(Profile)
admin.site.register(Employee)
admin.site.register(Visit)
admin.site.register(Drug)
admin.site.register(Movement)
admin.site.register(MovementItem)
