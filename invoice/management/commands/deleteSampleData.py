from django.core.management.base import BaseCommand, CommandError

from invoice import models


class Command(BaseCommand):
    help = 'Creates some sample data to use for testing'

    def handle(self, *args, **options):
        from django.conf import settings

        if not (settings.DEBUG or settings.STAGING):
            raise CommandError('You cannot run this command in production')

        self.delete_companies()
        self.delete_invoices()
        self.delete_expenses()
        self.delete_expense_groups()

    def delete_companies(self):
        for company in models.Company.objects.all():
            company.delete()

    def delete_invoices(self):
        for invoice in models.Invoice.objects.all():
            invoice.delete()

    def delete_expenses(self):
        for expense in models.Expense.objects.all():
            expense.delete()

    def delete_expense_groups(self):
        for group in models.ExpenseGroup.objects.all():
            group.delete()
