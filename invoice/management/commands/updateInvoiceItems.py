from django.core.management.base import BaseCommand
from invoice import models


class Command(BaseCommand):
    help = 'Updates invoice items by calling their save method'

    def handle(self, *args, **options):
        items = models.InvoiceItem.objects.all()

        for item in items:
            item.save()
