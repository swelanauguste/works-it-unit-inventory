# your_app/management/commands/add_os.py
from django.core.management.base import BaseCommand

from ...models import Department


class Command(BaseCommand):
    help = "Add a list of makes to the Department model"

    def handle(self, *args, **options):
        departments = ['building', 'communciation']

        for department in departments:
            department_instance, created = Department.objects.get_or_create(name=department)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added Department: {department}")
                )
            else:
                self.stdout.write(self.style.WARNING(f"Department already exists: {department}"))