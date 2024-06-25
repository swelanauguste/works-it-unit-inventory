from assets.models import Project as Source
from django.core.management.base import BaseCommand

from ...models import Project as Target


class Command(BaseCommand):
    help = "Transfer objects from one model to another"

    def handle(self, *args, **kwargs):
        # Get all objects from the source model
        source_objects = Source.objects.all()

        # Iterate over each object and create a new object in the target model
        for _ in source_objects:
            # Check if the object already exists in the target model to avoid duplicates
            if not Target.objects.filter(name=_.name).exists():
                new_ = Target(name=_.name)
                new_.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully transferred object: {_.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Object already exists: {_.name}")
                )

        self.stdout.write(self.style.SUCCESS("Transfer completed!"))
