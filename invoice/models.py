from __future__ import unicode_literals

from django.db import models
from datetime import datetime


class UserDetails(models.Model):
    class Meta:
        verbose_name = 'User Details'
        verbose_name_plural = 'User Details'

    address = models.TextField()
    email = models.CharField(max_length=150)
    phone = models.IntegerField()
    utr = models.IntegerField()

    bank = models.CharField(max_length=180)
    sort_code = models.CharField(max_length=50)
    account_number = models.IntegerField()

    def __str__(self):
        return self.email


class Company(models.Model):
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    name = models.CharField(max_length=200)
    address = models.TextField()
    email = models.CharField(max_length=150)

    def list_invoices(self):
        return self.invoice_set.all()

    def total_invoices(self):
        return self.invoice_set.all().count()

    def latest_invoice(self):
        return self.invoice_set.all().last()

    def not_paid_count(self):
        return self.invoice_set.all().filter(paid=False).count()

    def all_invoices(self):
        return self.invoice_set.all().order_by('-created')

    def __str__(self):
        return self.name


class Invoice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    person = models.CharField(max_length=80)
    phone = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True)
    paid = models.BooleanField(default=False)
    utr = models.BooleanField(default=False)

    def invoice_number(self):
        return 'N%04d' % self.pk

    def get_items(self):
        return self.items.all()

    def total(self):
        total = 0
        for item in self.get_items():
            total += item.cost
        return total

    def __str__(self):
        return self.company.name

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.now()

        super(Invoice, self).save(*args, **kwargs)


class InvoiceItem(models.Model):
    class Meta:
        ordering = ['id']

    invoice = models.ForeignKey(Invoice, related_name='items')
    description = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
