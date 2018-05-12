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
        ('Payment Details', {
            'fields': ('utr', 'bank', 'sort_code', 'account_number')}),
        ('Invoice Customisation', {
            'fields': ('invoice_primary_color', 'invoice_secondary_color', 'invoice_accent_color', 'invoice_background_color', 'invoice_logo')}),
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


@admin.register(models.Expense)
class ExpenseAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ExpenseGroup)
class ExpenseGroupAdmin(admin.ModelAdmin):
    pass
