from django import forms

from .models import Profile, User


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "is_tech",
            "is_manager",
        ]


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            "photo",
            "first_name",
            "last_name",
            "post",
            "gender",
            "phone",
        ]
