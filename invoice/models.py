from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    address = models.TextField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    utr = models.IntegerField(blank=True, null=True)

    bank = models.CharField(max_length=180, blank=True, null=True)
    sort_code = models.CharField(max_length=50, blank=True, null=True)
    account_number = models.IntegerField(blank=True, null=True)


class Company(models.Model):
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    name = models.CharField(max_length=200)
    address = models.TextField()
    email = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    person = models.CharField(max_length=80)
    phone = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True)
    paid = models.BooleanField(default=False)
    utr = models.BooleanField(default=False)
    user_invoice_number = models.TextField(max_length=15, blank=True, null=True)

    def invoice_number(self):
        if not self.user_invoice_number:
            return 'N%04d' % self.pk
        else:
            return self.user_invoice_number

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
            self.created = timezone.now()

        super(Invoice, self).save(*args, **kwargs)


class InvoiceItem(models.Model):
    class Meta:
        ordering = ['id']

    invoice = models.ForeignKey(Invoice, related_name='items')
    description = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
