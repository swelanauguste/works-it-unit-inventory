from django.db import models
from django.urls import reverse


class Supplier(models.Model):
    supplier = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=255, default="sales")

    def get_absolute_url(self):
        return reverse("supplier-detail", kwargs={"pk": self.pk})

    def __str__(self):
        if self.email:
            return f"{self.supplier} - {self.email} - {self.phone}"
        return f"{self.supplier} - {self.phone}"
