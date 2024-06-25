from departments.models import Department
from django.db import models
from locations.models import Location
from makers.models import Maker
from statuses.models import Status
from suppliers.models import Supplier
from users.models import User


class PrinterModel(models.Model):
    name = models.CharField(max_length=100)
    maker = models.ForeignKey(Maker, on_delete=models.CASCADE, null=True)
    image = models.FileField(upload_to="printer_models/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        # related_name="printer_model_updated_by",
    )

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("printer-model-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.maker} - {self.name}"


class Printer(models.Model):
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    printer_name = models.CharField(max_length=100, blank=True, null=True)
    model = models.ForeignKey(
        PrinterModel,
        on_delete=models.CASCADE,
    )
    ip_addr = models.GenericIPAddressField("IP Address", blank=True, null=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="printer_departments",
    )
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    date_received = models.DateField(blank=True, null=True)
    date_installed = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        # related_name="printer_updated_by",
    )

    class Meta:
        ordering = ["ip_addr"]

    def get_absolute_url(self):
        return reverse("printer-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.model.maker} - {self.model.name}"


class PrinterSupply(models.Model):
    printer = models.ForeignKey(Printer, on_delete=models.SET_NULL, null=True)
    item = models.CharField(max_length=50)
    part_number = models.CharField(max_length=60, null=True, blank=True)
    count = models.PositiveIntegerField(default=1)
    min_count = models.PositiveIntegerField(default=3)
    supplier = models.ManyToManyField(Supplier, blank=True, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "printer supplies"

    def get_absolute_url(self):
        return reverse("supply-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.item} {self.printer} ({self.count})"
