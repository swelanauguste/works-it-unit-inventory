from django.contrib import admin

from .models import Client, Department

admin.site.register(Department)
admin.site.register(Client)
