import django_filters
from django import forms
from users.models import User

from .models import (
    Computer,
    ComputerModel,
    ComputerType,
    Department,
    Location,
    OperatingSystem,
    Printer,
    Project,
    Status,
)


class ComputerFilter(django_filters.FilterSet):
    project = django_filters.ModelChoiceFilter(
        queryset=Project.objects.all(),
        field_name="project",
        lookup_expr="exact",
        label="Project",
    )

    serial_number = django_filters.CharFilter(
        lookup_expr="icontains", label="Serial Number"
    )
    computer_name = django_filters.CharFilter(
        lookup_expr="icontains", label="Computer Name"
    )
    model = django_filters.ModelChoiceFilter(
        queryset=ComputerModel.objects.all(),
        field_name="model",
        lookup_expr="exact",
        label="Model",
    )
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        field_name="status",
        lookup_expr="exact",
        label="Status",
    )
    os = django_filters.ModelChoiceFilter(
        queryset=OperatingSystem.objects.all(),
        field_name="os",
        lookup_expr="exact",
        label="Operating System",
    )
    location = django_filters.ModelChoiceFilter(
        queryset=Location.objects.all(),
        field_name="location",
        lookup_expr="exact",
        label="Location",
    )
    department = django_filters.ModelChoiceFilter(
        queryset=Department.objects.all(),
        field_name="department",
        lookup_expr="exact",
        label="Department",
    )
    created_by = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(is_tech=True)
    )
    updated_by = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(is_tech=True)
    )

    class Meta:
        model = Computer
        fields = [
            "project",
            "serial_number",
            "computer_name",
            "model",
            "status",
            "os",
            "location",
            "department",
            "created_by",
            "updated_by",
        ]


class PrinterFilter(django_filters.FilterSet):

    class Meta:
        model = Printer
        fields = [
            "model",
            "status",
            "location",
            "department",
            "date_received",
            "date_installed",
        ]
