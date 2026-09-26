from django.core.management.base import BaseCommand
from django.core.management import call_command
from delivery.models import Restaurant
from pathlib import Path


class Command(BaseCommand):
    help = "Load restaurant and menu data"

    def handle(self, *args, **kwargs):

        if Restaurant.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Restaurant data already exists. Skipping import."
                )
            )
            return

        data_file = Path("restaurant_data.json")

        if not data_file.exists():
            self.stdout.write(
                self.style.ERROR("restaurant_data.json not found.")
            )
            return

        call_command("loaddata", str(data_file))

        self.stdout.write(
            self.style.SUCCESS(
                "Restaurant and menu data loaded successfully!"
            )
        )