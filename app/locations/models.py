from django.db import models

# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name.upper()
