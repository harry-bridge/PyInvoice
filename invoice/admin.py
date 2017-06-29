from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from invoice import models, forms


@admin.register(models.Profile)
class ProfileAdmin(UserAdmin):
    form = forms.ProfileChangeForm
    add_form = forms.UserCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'address', 'phone')}),
        ('payment details', {
            'fields': ('utr', 'bank', 'sort_code', 'account_number')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


class InvoiceItemInline(admin.TabularInline):
    model = models.InvoiceItem
    extra = 2


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (str, 'invoice_number')

    inlines = [
        InvoiceItemInline
    ]

