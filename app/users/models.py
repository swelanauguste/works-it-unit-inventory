import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class User(AbstractUser):
    is_tech = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)

    def get_user_roles(self):
        roles = []
        if self.is_tech:
            roles.append("is_tech")
        if self.is_manager:
            roles.append("is_manager")

        return roles if roles else ["user"]

    def __str__(self):
        return self.username


class Profile(models.Model):
    GENDER_LIST = [
        ("F", "Female"),
        ("M", "Male"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    post = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_LIST)
    phone = models.CharField(max_length=25, null=True, default="+1")

    # def get_absolute_url(self):
    #     return reverse("user-profile-detail", kwargs={"slug": self.slug})
    
    # def get_absolute_update_url(self):
    #     return reverse("user-profile-update", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            # Newly created object, so set slug
            self.slug = slugify(self.uid)
        super(Profile, self).save(*args, **kwargs)

    def get_profile_initials(self):
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}"
        return self.user.email[0].upper()

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return f"{self.user}"