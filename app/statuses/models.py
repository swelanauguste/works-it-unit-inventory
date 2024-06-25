from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Statuses"
        ordering = ["name"]

    def __str__(self):
        return self.name.upper()
