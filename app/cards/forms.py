from django import forms

from .models import Card

class CardForm(forms.ModelForm):
    
    class Meta:
        model = Card
        fields = "__all__"
        exclude = ['updated_by', 'created_by']
        widgets = {
            "expires": forms.DateInput(attrs={"type": "date"}),
        }