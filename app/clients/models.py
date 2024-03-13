from django.db import models
from django.urls import reverse


class Department(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name.upper()


class Client(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    job_title = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    ext = models.CharField(max_length=4, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("client-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name
