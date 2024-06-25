# your_app/management/commands/transfer_departments.py
from django.core.management.base import BaseCommand
from assets.models import Department as SourceDepartment
from ...models import Department as TargetDepartment

class Command(BaseCommand):
    help = 'Transfer Department objects from one model to another'

    def handle(self, *args, **kwargs):
        # Get all departments from the source model
        source_departments = SourceDepartment.objects.all()

        # Iterate over each department and create a new department in the target model
        for dept in source_departments:
            # Check if the department already exists in the target model to avoid duplicates
            if not TargetDepartment.objects.filter(name=dept.name).exists():
                new_dept = TargetDepartment(name=dept.name)
                new_dept.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully transferred department: {dept.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Department already exists: {dept.name}'))

        self.stdout.write(self.style.SUCCESS('Transfer completed!'))
