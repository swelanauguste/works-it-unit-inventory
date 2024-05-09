from django.contrib import admin

from .models import Licence, Category, Card, StaffCard


admin.site.register(Licence)
admin.site.register(Category)
admin.site.register(Card)
admin.site.register(StaffCard)
