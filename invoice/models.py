from __future__ import unicode_literals

from django.db import models


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
    invoice_prefix = models.CharField(max_length=4)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=10)

    def __str__(self):
        return self.company.name


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.IntegerField()
