from clients.models import Client, Department
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from suppliers.models import Supplier
from users.models import User


class Project(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="project_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="project_updated_by",
    )

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name.upper()


class Maker(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name.upper()


class Status(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Statuses"
        ordering = ["name"]

    def __str__(self):
        return self.name.upper()


class OperatingSystem(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class MonitorModel(models.Model):
    name = models.CharField(max_length=100)
    maker = models.ForeignKey(Maker, on_delete=models.CASCADE)
    image = models.FileField(upload_to="monitor_models/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="monitor_model_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="monitor_model_updated_by",
    )

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("monitor-model-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.maker} - {self.name}"


class Monitor(models.Model):
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    model = models.ForeignKey(
        MonitorModel, on_delete=models.CASCADE, related_name="monitors"
    )
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
        related_name="monitor_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="monitor_updated_by",
    )

    class Meta:
        ordering = ["model__name"]

    def get_absolute_url(self):
        return reverse("monitor-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.model.name} - {self.serial_number}"


class ComputerType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name.upper()


class ComputerModel(models.Model):
    name = models.CharField(max_length=100)
    computer_type = models.ForeignKey(ComputerType, on_delete=models.CASCADE)
    maker = models.ForeignKey(Maker, on_delete=models.CASCADE)
    processor = models.CharField(
        max_length=100, blank=True, null=True, help_text="In GHz(e.g.:i5 2.9 GHz)"
    )
    ram = models.IntegerField("RAM", help_text="In GB")
    hdd = models.IntegerField("HDD/Storage", help_text="In GB")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="computer_model_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="computer_model_updated_by",
    )

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("computer-model-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.maker} - {self.name} - {self.processor}"


class Computer(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="projects",
        null=True,
        blank=True,
    )
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    warranty_info = models.CharField("Warranty", max_length=100, default="N/A")
    computer_name = models.CharField(
        max_length=100, blank=True, null=True, default="MCWT"
    )
    model = models.ForeignKey(
        ComputerModel, on_delete=models.CASCADE, related_name="computers"
    )
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=2)
    monitor = models.ManyToManyField(Monitor, related_name="monitors", blank=True)
    os = models.ForeignKey(
        OperatingSystem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Operating System",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="computer_locations",
        default=1,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="computer_departments",
        default=1,
    )
    user = models.CharField(max_length=100, blank=True, null=True)
    date_received = models.DateField(blank=True, null=True, default=timezone.now)
    date_installed = models.DateField(blank=True, null=True)
    image = models.FileField(upload_to="system_audit/", blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="computer_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="computer_updated_by",
    )
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ["created_at"]

    def get_absolute_url(self):
        return reverse("computer-detail", kwargs={"pk": self.pk})

    def get_last_computer_name(self):
        last_computer_name = Computer.objects.last()
        if last_computer_name:
            return last_computer_name.computer_name
        return "MCWT0000"

    def __str__(self):
        if self.serial_number:
            return self.serial_number
        return self.computer_name


class ComputerComment(models.Model):
    computer = models.ForeignKey(
        Computer, on_delete=models.CASCADE, related_name="comments"
    )
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="computer_comment_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="computer_comment_updated_by",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.computer.computer_name} - comment {self.pk}"


class PrinterModel(models.Model):
    name = models.CharField(max_length=100)
    maker = models.ForeignKey(Maker, on_delete=models.CASCADE)
    image = models.FileField(upload_to="printer_models/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="printer_model_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="printer_model_updated_by",
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
        PrinterModel, on_delete=models.CASCADE, related_name="printers"
    )
    ip_addr = models.GenericIPAddressField("IP Address", blank=True, null=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="printer_locations",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="printer_departments",
    )
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
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
        related_name="printer_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="printer_updated_by",
    )

    class Meta:
        ordering = ["ip_addr"]

    def get_absolute_url(self):
        return reverse("printer-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.model.maker} - {self.model.name}"


class PrinterSupply(models.Model):
    printer = models.ForeignKey(
        Printer, on_delete=models.SET_NULL, null=True, related_name="supplies"
    )
    item = models.CharField(max_length=50)
    part_number = models.CharField(max_length=60, null=True, blank=True)
    count = models.PositiveIntegerField(default=1)
    min_count = models.PositiveIntegerField(default=2)
    supplier = models.ManyToManyField(Supplier)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "printer supplies"

    def get_absolute_url(self):
        return reverse("supply-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.item} {self.printer} ({self.count})"


class MicrosoftOfficeVersion(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="version_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="version_updated_by",
    )

    def __str__(self):
        return f"Microsoft Office {self.name}"


class MicrosoftOffice(models.Model):
    version = models.ForeignKey(
        MicrosoftOfficeVersion,
        on_delete=models.CASCADE,
        related_name="versions",
        default=1,
    )
    product_key = models.CharField(max_length=30, unique=True)
    computer = models.ForeignKey(
        Computer,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="serial number",
        related_name="office_installations",
    )
    date_installed = models.DateField(null=True, blank=True)
    comments = models.TextField(blank=True, null=True)
    is_installed = models.BooleanField(default=False)
    has_failed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ms_office_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ms_office_updated_by",
    )

    class Meta:
        ordering = ["-date_installed"]

    def get_absolute_url(self):
        return reverse("microsoft-office-detail", kwargs={"pk": self.pk})

    def remove_hyphens(self):
        return self.product_key.replace("-", "")

    def __str__(self):
        return f"{self.version} - XXXXX-XXXXX-XXXXX-{self.product_key[-11:]}"
