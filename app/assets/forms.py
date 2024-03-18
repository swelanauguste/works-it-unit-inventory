from django import forms

from .models import ComputerComment  # ComputerName,
from .models import (
    Computer,
    ComputerModel,
    MicrosoftOffice,
    Monitor,
    Printer,
    PrinterModel,
)

# class GetComputerNameForm(forms.ModelForm):

#     class Meta:
#         model = ComputerName
#         fields = ["computer_name"]


class MicrosoftOfficeUpdateForm(forms.ModelForm):
    class Meta:
        model = MicrosoftOffice
        fields = ["computer", "date_installed", "has_failed", "comments"]
        widgets = {
            "date_installed": forms.DateInput(attrs={"type": "date"}),
            "comments": forms.Textarea(attrs={"rows": 2}),
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = ComputerComment
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "rows": 2,
                }
            )
        }


class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = "__all__"
        exclude = ["created_by", "updated_by"]
        widgets = {
            "date_received": forms.DateInput(attrs={"type": "date"}),
            "date_installed": forms.DateInput(attrs={"type": "date"}),
        }
class PrinterModelForm(forms.ModelForm):
    class Meta:
        model = PrinterModel
        fields = "__all__"
        exclude = ["created_by", "updated_by"]


class MonitorForm(forms.ModelForm):
    class Meta:
        model = Monitor
        fields = "__all__"
        widgets = {
            "date_received": forms.DateInput(attrs={"type": "date"}),
            "date_installed": forms.DateInput(attrs={"type": "date"}),
        }


class ComputerForm(forms.ModelForm):
    class Meta:
        model = Computer
        fields = "__all__"
        exclude = ["created_by", "updated_by"]
        widgets = {
            "date_received": forms.DateInput(attrs={"type": "date"}),
            "date_installed": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class ComputerModelForm(forms.ModelForm):
    class Meta:
        model = ComputerModel
        fields = "__all__"
        exclude = ["created_by", "updated_by"]
        widgets = {
            "date_received": forms.DateInput(attrs={"type": "date"}),
            "date_installed": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
