import random
import string

from clients.models import Client
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from users.models import Profile, User


def generate_short_id():
    length = 8  # You can adjust the length as needed
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for i in range(length)).upper()


class TicketStatus(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Ticket Statuses"

    def __str__(self):
        return f"{self.name.upper()}"


class TicketCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Ticket Categories"

    def __str__(self):
        return self.name


class Ticket(models.Model):
    user = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    summary = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_closed = models.BooleanField(default=False)
    ticket_id = models.CharField(
        default=generate_short_id, editable=False, unique=True, max_length=8
    )
    ticket_status = models.ForeignKey(
        TicketStatus,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="status",
        default=1,
    )
    ticket_category = models.ForeignKey(
        TicketCategory, on_delete=models.SET_NULL, null=True, verbose_name="category"
    )
    slug = models.SlugField(max_length=8, unique=True, blank=True, null=True)
    file = models.FileField(upload_to="tickets/", blank=True, null=True)
    assigned_to = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_to",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = models.ForeignKey(
    #     User,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="ticket_created_by",
    # )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ticket_updated_by",
    )

    class Meta:
        ordering = ["-is_closed", "updated_at"]

    def get_absolute_url(self):
        return reverse("ticket-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            # Newly created object, so set slug
            self.slug = slugify(self.ticket_id)
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_id}"


class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="comments"
    )
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ticket_comment_created_by",
    )
    # updated_by = models.ForeignKey(
    #     User,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="ticket_comment_updated_by",
    # )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.comments[:50]}"
