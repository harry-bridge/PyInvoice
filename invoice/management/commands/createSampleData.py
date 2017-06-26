from django.core.management.base import BaseCommand
import random

from invoice import models


class Command(BaseCommand):
    help = 'Creates some sample data to use for testing'

    def handle(self, *args, **options):
        from django.conf import settings

        if not (settings.DEBUG or settings.STAGING):
            raise CommandError('You cannot run this command in production')

        random.seed('Some object to seed the random number generator')  # otherwise it is done by time, which could lead to inconsistant tests

        self.create_companies()
        self.create_invoices()

    def create_companies(self):
        company_names = ['Dodgey Dave\'s DJs', 'The Man In A Van', 'A Shitty Hotel']
        company_addresses = ['Somewhere in Birmingham', 'The Moon', 'My Mate\'s Garage']
        company_emails = ['test@test.com']

        for i in range(5):
            models.Company.objects.create(
                name=company_names[i%len(company_names)],
                address=company_addresses[i%len(company_addresses)],
                email=company_emails[i%len(company_emails)]
                )

    def create_invoices(self):
        invoice_items = ['Some lights and PA', 'Get-out in a muddy field', 'Boring show call', 'Corproate job in Manchester', 'Dealing in child actors', 'Literal waste of my time']
        amounts = [0.00, 100.00, 5.99, 600, 130.34]

        for i in range(10):  # Create 10 random invoices
            company = random.choice(models.Company.objects.all())

            invoice = models.Invoice.objects.create(
                company=company,
            )

            for j in range(random.randint(1, 5)):  # Create a random number of items
                models.InvoiceItem.objects.create(
                    invoice=invoice,
                    description=random.choice(invoice_items),
                    amount=int(random.choice(amounts))
                )
