from django import forms

from .models import Card, StaffCard


class StaffCardForm(forms.ModelForm):

    class Meta:
        model = StaffCard
        fields = "__all__"
        exclude = ["updated_by", "created_by", 'is_printed']


class CardForm(forms.ModelForm):

    class Meta:
        model = Card
        fields = "__all__"
        exclude = ["updated_by", "created_by"]
        widgets = {
            "expires": forms.DateInput(attrs={"type": "date"}),
        }
