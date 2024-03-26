import django_filters
from django import forms
from django_filters import DateRangeFilter, NumberFilter

from .models import Sticker


class StickerFilter(django_filters.FilterSet):

    date = DateRangeFilter()

    class Meta:
        model = Sticker
        fields = ["date"]
