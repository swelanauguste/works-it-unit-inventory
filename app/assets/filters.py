import django_filters
from django import forms

from .models import Computer, Printer


class ComputerFilter(django_filters.FilterSet):
   

    class Meta:
        model = Computer
        fields = [
            "project",
            "model",
            "status",
            "os",
            "location",
            "department",
        ]
     


class PrinterFilter(django_filters.FilterSet):

    class Meta:
        model = Printer
        fields = [
            "serial_number",
            "printer_name",
            "ip_addr",
            "status",
            "location",
            "department",
            "date_received",
            "date_installed",
        ]