from django.shortcuts import HttpResponse, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from datetime import datetime
from django.urls import reverse
# import simplejson as json
import json
from invoice import models


@login_required()
def get_items_for_table(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        item_pk = request.POST.get('item_pk', '0')

        if item_pk == '0':
            context['description'] = ''
            context['cost'] = ''
            context['quantity'] = ''
            context['item_pk'] = 0

        else:
            item = get_object_or_404(models.InvoiceItem, pk=item_pk)
            context['description'] = item.description
            context['cost'] = item.cost
            context['quantity'] = item.quantity
            context['item_pk'] = item_pk

    return HttpResponse(
        json.dumps(context),
        content_type="application/json"
    )


@login_required()
def get_company_for_modal(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        company_pk = request.POST.get('company_pk', '0')

        if company_pk != '0':
            company = get_object_or_404(models.Company, pk=company_pk)
            context['company_pk'] = company.pk
            context['name'] = company.name
            context['address'] = company.address
            context['email'] = company.email

    return HttpResponse(json.dumps(context), content_type='application/json')


@login_required()
def invoice_photo_upload(request):
    pass


@login_required()
def get_expense_items_for_modal(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        # 0: expense_pk, 1: group_pk
        expense_pks = request.POST.getlist('pk_array[]')

        context['invoices'] = models.Invoice.objects.all()
        context['groups'] = models.ExpenseGroup.objects.all()

        if expense_pks[0] != '0':
            context['expense'] = get_object_or_404(models.Expense, pk=expense_pks[0])
        else:
            context['add'] = True
            context['add_invoice_pk'] = int(expense_pks[1])

        if expense_pks[1] != '0':
            context['invoice'] = get_object_or_404(models.Invoice, pk=expense_pks[1])
            context['invoices'] = None

        if expense_pks[2] != '0':
            context['expense_group'] = get_object_or_404(models.ExpenseGroup, pk=expense_pks[2])
            context['groups'] = None

        html = render_to_string('expense_form.html', context=context)

        return HttpResponse(html)
        # return HttpResponse(json.dumps(pk_array), content_type='application/json')


@login_required()
def mark_invoice_sent(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        invoice_pk = request.POST.get('invoice_pk', '0')

        invoice = models.Invoice.objects.update_or_create(pk=invoice_pk, defaults={
            'sent_date': timezone.now(),
        })

        context['sent_date'] = datetime.strftime(invoice[0].sent_date.date(), '%d %b %Y')

    return HttpResponse(json.dumps(context, cls=DjangoJSONEncoder), content_type='application/json')


@login_required()
def get_items_for_delete_modal(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        item_pk = request.POST.get('item_pk', '0')
        context['type'] = request.POST.get('type')

        if context['type'] == 'invoice':
            context['object'] = get_object_or_404(models.Invoice, item_pk)
        elif context['type'] == 'expense':
            context['object'] = get_object_or_404(models.Expense, item_pk)

        html = render_to_string('delete_modal.html', context)

        return HttpResponse(json.dumps(html), content_type='application/json')


@login_required()
def delete_item(request):
    context = dict()
    data = dict()
    if request.method == 'POST' and request.is_ajax():
        item_pk = request.POST.get('item_pk', '0')
        data['type'] = request.POST.get('type').lower().replace(' ', '_')
        context['edit'] = True

        if data['type'] == 'expense':
            expense_item = get_object_or_404(models.Expense, pk=item_pk)
            context['expense_list'] = expense_item.invoice.expenses
            context['invoice'] = expense_item.invoice
            context['expense_view'] = 'invoice'
            expense_item.delete()
            data['html'] = render_to_string('expense_table.html', context)

        if data['type'] == 'invoice':
            get_object_or_404(models.Invoice, pk=item_pk).delete()
            data['url'] = reverse('invoice_list')

        if data['type'] == 'invoice_item':
            invoice_item = get_object_or_404(models.InvoiceItem, pk=item_pk)
            context['invoice'] = invoice_item.invoice
            invoice_item.delete()
            data['html'] = render_to_string('item_table.html', context)

        if data['type'] == 'company':
            company = get_object_or_404(models.Company, pk=item_pk)

            if company.invoice_set:
                for invoice in company.invoice_set.all():
                    invoice.company = None
                    invoice.save()
            company.delete()
            data['url'] = reverse('company_list')

        return HttpResponse(json.dumps(data), content_type='application/json')
