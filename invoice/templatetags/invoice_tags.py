from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.safestring import SafeData, mark_safe
from django.utils.text import normalize_newlines
from django.utils.html import escape
from django.shortcuts import get_object_or_404

from invoice import models

register = Library()


@register.filter(is_safe=True, needs_autoescape=True)
@stringfilter
def linebreaksn(value, autoescape=True):
    """
    Convert all newlines in a piece of plain text to jQuery line breaks
    (`\n`).
    """
    autoescape = autoescape and not isinstance(value, SafeData)
    value = normalize_newlines(value)
    if autoescape:
        value = escape(value)
    return mark_safe(value.replace('\n', '\\n'))


@register.filter(is_safe=True)
@stringfilter
def dash_if_none(value):
    """
    Converts a None value into a -
    """
    if value in 'None':
        return '-'
    else:
        return value


@register.simple_tag()
def total_invoices_user(company, user):
    company = get_object_or_404(models.Company, pk=company.pk)

    return company.invoice_set.filter(user=user).count()


@register.simple_tag()
def latest_invoice_user(company, user):
    company = get_object_or_404(models.Company, pk=company.pk)

    return company.invoice_set.filter(user=user).last()
