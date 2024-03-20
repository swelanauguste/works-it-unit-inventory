from django import forms
from users.models import User

from .models import Comment, Ticket


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = "__all__"
        exclude = [
            "slug",
            "user",
            "created_by",
            "updated_by",
        ]
        # widgets = {
        #     "status": forms.Select(attrs={"class": "form-control"}),
        #     "technician": forms.Select(attrs={"class": "form-control"}),
        # }


class TicketAssignTechnicianForm(forms.Form):
    technician_id = forms.ModelChoiceField(
        queryset=User.objects.filter(is_tech=True), empty_label="Select Technician"
    )


class TicketCreateForm(forms.ModelForm):
    email = forms.EmailField(max_length=100)
    
    class Meta:
        model = Ticket
        fields = ['summary', 'file', 'description']
    # summary = forms.CharField(max_length=100)
    # file = forms.FileField(required=False, widget=forms.ClearableFileInput())
    # email = forms.EmailField(max_length=100)
    # description = forms.CharField(widget=forms.Textarea)

# class TicketCreateForm(forms.Form):
#     summary = forms.CharField(max_length=100)
#     file = forms.FileField(required=False, widget=forms.ClearableFileInput())
#     email = forms.EmailField(max_length=100)
#     description = forms.CharField(widget=forms.Textarea)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comments"]

        widgets = {
            "comments": forms.Textarea(attrs={"rows": 3, "cols": 30}),
        }
