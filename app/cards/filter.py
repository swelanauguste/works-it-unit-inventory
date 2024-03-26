import django_filters
from django import forms

from .models import Card


class CardFilter(django_filters.FilterSet):

    class Meta:
        model = Card
        fields = [
            "licence",
            "category",
        ]


