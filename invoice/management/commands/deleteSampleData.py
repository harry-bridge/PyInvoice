from django.core.management.base import BaseCommand

from invoice import models


class Command(BaseCommand):
    help = 'Creates some sample data to use for testing'

    def handle(self, *args, **options):
        from django.conf import settings

        if not (settings.DEBUG or settings.STAGING):
            raise CommandError('You cannot run this command in production')

        self.delete_companies()
        self.delete_invoices()

    def delete_companies(self):
        for company in models.Company.objects.all():
            company.delete()

    def delete_invoices(self):
        for invoice in models.Invoice.objects.all():
            invoice.delete()
