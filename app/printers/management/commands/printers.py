# your_app/management/commands/transfer_printers.py
from django.core.management.base import BaseCommand
from assets.models import Printer as SourcePrinter
from ...models import Printer as TargetPrinter
from ...models import PrinterModel as TargetPrinterModel
from locations.models import Location as TargetLocation
from departments.models import Department as TargetDepartment
from statuses.models import Status as TargetStatus
from users.models import User as TargetUser

class Command(BaseCommand):
    help = 'Transfer Printer objects from one model to another, maintaining foreign keys'

    def handle(self, *args, **kwargs):
        # Get all printers from the source model
        source_printers = SourcePrinter.objects.all()

        for printer in source_printers:
            # Find corresponding foreign key instances in the target model
            try:
                target_model = TargetPrinterModel.objects.get(id=printer.model.id)
            except TargetPrinterModel.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Model does not exist in target: {printer.model}'))
                continue

            try:
                target_location = TargetLocation.objects.get(id=printer.location.id) if printer.location else None
            except TargetLocation.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Location does not exist in target: {printer.location}'))
                continue

            try:
                target_department = TargetDepartment.objects.get(id=printer.department.id) if printer.department else None
            except TargetDepartment.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Department does not exist in target: {printer.department}'))
                continue

            try:
                target_status = TargetStatus.objects.get(id=printer.status.id) if printer.status else None
            except TargetStatus.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Status does not exist in target: {printer.status}'))
                continue

            try:
                target_created_by = TargetUser.objects.get(id=printer.created_by.id) if printer.created_by else None
            except TargetUser.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Created by user does not exist in target: {printer.created_by}'))
                continue

            try:
                target_updated_by = TargetUser.objects.get(id=printer.updated_by.id) if printer.updated_by else None
            except TargetUser.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Updated by user does not exist in target: {printer.updated_by}'))
                continue

            # Check if the printer already exists in the target model to avoid duplicates
            if not TargetPrinter.objects.filter(serial_number=printer.serial_number).exists():
                new_printer = TargetPrinter(
                    serial_number=printer.serial_number,
                    printer_name=printer.printer_name,
                    model=target_model,
                    ip_addr=printer.ip_addr,
                    location=target_location,
                    department=target_department,
                    status=target_status,
                    date_received=printer.date_received,
                    date_installed=printer.date_installed,
                    notes=printer.notes,
                    created_at=printer.created_at,
                    updated_at=printer.updated_at,
                    created_by=target_created_by,
                    updated_by=target_updated_by,
                )
                new_printer.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully transferred printer: {printer.serial_number}'))
            else:
                self.stdout.write(self.style.WARNING(f'Printer already exists: {printer.serial_number}'))

        self.stdout.write(self.style.SUCCESS('Transfer completed!'))
