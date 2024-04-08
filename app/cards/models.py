from django.db import models
from django.shortcuts import reverse
from users.models import User


class Licence(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name.upper()} LICENCE"


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name.upper()


class Card(models.Model):
    photo = models.FileField(upload_to="photos", blank=True)
    signature = models.FileField(upload_to="signatures", blank=True)
    name = models.CharField(max_length=200)
    licence = models.ForeignKey(Licence, on_delete=models.CASCADE)
    licence_no = models.CharField(max_length=5, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    expires = models.DateField(blank=True)
    is_printed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="licence_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="licence_updated_by",
    )

    def get_absolute_url(self):
        return reverse("card-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.name.upper()}/{self.licence_no}/{self.category}"
