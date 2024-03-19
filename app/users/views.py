from django.shortcuts import render
from django.views.generic import ListView, UpdateView

from .forms import ProfileForm, UserForm
from .models import Profile, User



class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    
    
class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    # template_name = "users/profile_update_form.html"

    # def get_object(self):
    #     return self.request.user.profile

    # def get_success_url(self):
    #     return reverse("users:profile-update")