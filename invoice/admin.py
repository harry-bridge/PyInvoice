from django.contrib import admin

from models import *


class UserDetailsAdmin(admin.ModelAdmin):
    pass


class CompanyAdmin(admin.ModelAdmin):
    pass


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 2


class InvoiceAdmin(admin.ModelAdmin):
    list_display = (str, 'invoice_number')

    inlines = [
        InvoiceItemInline
    ]


admin.site.register(UserDetails, UserDetailsAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Invoice, InvoiceAdmin)
