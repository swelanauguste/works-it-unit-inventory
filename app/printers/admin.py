from django.contrib import admin

from .models import Printer, PrinterModel, PrinterSupply

# Register your models here.


admin.site.register(Printer)
admin.site.register(PrinterModel)
admin.site.register(PrinterSupply)
