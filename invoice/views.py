from django.views import generic
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
import json

from invoice import models


class Index(generic.TemplateView):
    template_name = 'index.html'

    def not_paid_count(self):
        return models.Invoice.objects.all().filter(paid=False).count()

    def not_paid_total(self):
        total = 0
        for invoice in models.Invoice.objects.all().filter(paid=False):
            total += invoice.total()
        return total

    def last_invoice(self):
        return models.Invoice.objects.all().last()

    def latest_invoices(self):
        return models.Invoice.objects.all().order_by('-created')[:10]


class InvoiceList(generic.ListView):
    model = models.Invoice
    template_name = 'invoice_list.html'
    ordering = '-created'


class InvoiceDetail(generic.DetailView):
    model = models.Invoice
    template_name = 'invoice_form.html'


class InvoiceCreate(generic.TemplateView):
    template_name = 'invoice_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreate, self).get_context_data(**kwargs)
        context['companies'] = models.Company.objects.all()

        context['edit'] = True
        return context


def invoice_edit(request, pk):
    invoice = get_object_or_404(models.Invoice, pk=pk)
    companies = models.Company.objects.all()

    context = {
        'invoice': invoice,
        'edit': True,
        'companies': companies,
    }

    return render_to_response('invoice_form.html', context)


def invoice_update(request):
    context = {}
    if request.method == 'POST' and request.is_ajax():
        defaults = {}
        invoice_pk = request.POST['invoice_pk']
        defaults['company'] = get_object_or_404(models.Company, pk=int(request.POST['company']))
        defaults['person'] = request.POST['person']

        if request.POST['phone'] == '':
            defaults['phone'] = None
        else:
            defaults['phone'] = request.POST['phone']

        defaults['paid'] = json.loads(request.POST['paid'])
        defaults['utr'] = json.loads(request.POST['utr'])

        if invoice_pk == '0':
            invoice = models.Invoice.objects.create(**defaults)
            invoice_pk = str(invoice.pk)
            context['url'] = '/invoice/' + invoice_pk + '/edit/'
        else:
            models.Invoice.objects.update_or_create(pk=invoice_pk, defaults=defaults)

            context['url'] = '/invoice/' + invoice_pk

        return HttpResponse(json.dumps(context), content_type='application/json')


def invoice_item_update(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        defaults = {}
        item_pk = request.POST.get('item_pk', '0')
        invoice_pk = request.POST.get('invoice_pk', '0')

        defaults['description'] = request.POST['description']
        defaults['cost'] = request.POST['cost']

        if item_pk == '0':
            defaults['invoice'] = get_object_or_404(models.Invoice, pk=invoice_pk)
            models.InvoiceItem.objects.create(**defaults)

        else:
            models.InvoiceItem.objects.update_or_create(pk=item_pk, defaults=defaults)

            # context['pk'] = item_pk
            # context['description'] = defaults['description']
            # context['cost'] = defaults['cost']

        context['invoice'] = get_object_or_404(models.Invoice, pk=invoice_pk)
        context['edit'] = True

    return render_to_response('item_table.html', context)


def invoice_item_delete(request):
    context = {}
    if request.method == 'POST' and request.is_ajax():
        invoice_pk = request.POST['invoice_pk']
        item_pk = request.POST['item_pk']
        item = get_object_or_404(models.InvoiceItem, pk=item_pk)
        item.delete(keep_parents=True)

        context['invoice'] = get_object_or_404(models.Invoice, pk=invoice_pk)
        context['edit'] = True

        return render_to_response('item_table.html', context)


def invoice_delete(request):
    context = {}
    if request.method == 'POST' and request.is_ajax():
        invoice_pk = request.POST['invoice_pk']

        invoice = get_object_or_404(models.Invoice, pk=invoice_pk)
        invoice.delete()

        context['deleted'] = True
        context['url'] = '/invoice/list/'

    return HttpResponse(json.dumps(context), content_type='application/json')


class CompanyList(generic.ListView):
    model = models.Company
    template_name = 'company_list.html'


class CompanyDetail(generic.DetailView):
    model = models.Company
    template_name = 'company_update.html'


class CompanyCreate(generic.TemplateView):
    template_name = 'company_update.html'


def company_edit(request, pk):
    company = get_object_or_404(models.Company, pk=pk)

    context = {
        'edit': True,
        'company': company,
    }

    return render_to_response('company_update.html', context)


def company_update(request):
    context = {}
    if request.method == 'POST' and request.is_ajax():
        defaults = {}
        company_pk = request.POST.get('company_pk', '0')
        redirect = bool(request.POST.get('redirectOnSave', '0'))

        defaults['name'] = request.POST['name']
        defaults['address'] = request.POST['address']
        defaults['email'] = request.POST['email']

        if company_pk == '0':
            company = models.Company.objects.create(**defaults)
            context['company_pk'] = company.pk
            context['company_name'] = company.name

            if redirect:
                context['url'] = '/company/' + str(company.pk) + '/edit/'
        else:
            company = models.Company.objects.update_or_create(pk=company_pk, defaults=defaults)

            if redirect:
                context['url'] = '/company/' + str(company_pk)

            context['name'] = company.name

    return HttpResponse(json.dumps(context), content_type='application/json')


def company_delete(request):
    context = {}
    if request.method == 'POST' and request.is_ajax():
        company_pk = request.POST['company_pk']

        company = get_object_or_404(models.Company, pk=company_pk)
        company.delete()

        context['deleted'] = True
        context['url'] = '/company/list/'

    return HttpResponse(json.dumps(context), content_type='application/json')
