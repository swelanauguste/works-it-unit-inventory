import django_filters
from django import forms
from users.models import Profile

from .models import Ticket, TicketCategory, TicketStatus


class TicketFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=TicketStatus.objects.all(),
        field_name="ticket_status",
        lookup_expr="exact",
        label="Status",
    )
    category = django_filters.ModelChoiceFilter(
        queryset=TicketCategory.objects.all(),
        field_name="ticket_category",
        lookup_expr="exact",
        label="Category",
    )

    assigned_to = django_filters.ModelChoiceFilter(
        queryset=Profile.objects.all(),
        field_name="assigned_to",
        lookup_expr="exact",
        label="Assigned To",
    )
    ticket_id = django_filters.CharFilter(lookup_expr="icontains", label="Ticket ID")

    class Meta:
        model = Ticket
        fields = ["ticket_id", "status", "category", "assigned_to"]
        widgets = {
            "status": forms.CheckboxSelectMultiple(attrs={"class": "select"}),
            "category": forms.CheckboxSelectMultiple(),
        }
