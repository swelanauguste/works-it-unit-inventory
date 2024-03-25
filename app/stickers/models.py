from django.db import models
from users.models import Profile, User


class Sticker(models.Model):
    name = models.CharField(max_length=100, blank=True)
    sticker = models.CharField(max_length=100)
    no_plate = models.CharField("number plate", max_length=100, blank=True)
    expires = models.DateField(null=True)
    receipt = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sticker_created_by",
    )
    updated_by = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sticker_updated_by",
    )
    
    class Meta:
        ordering = ["-created_at"]
        # unique_together = ("sticker", "no_plate")

    # def __str__(self):
    #     return f"{self.sticker}/{self.expires}/{self.name}/{self.no_plate}"
