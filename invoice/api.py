from django.shortcuts import HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
import simplejson as json

from invoice import models


@login_required()
def get_items_for_table(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        item_pk = request.POST.get('item_pk', '0')

        if item_pk == '0':
            context['description'] = ''
            context['cost'] = ''
            context['item_pk'] = 0

        else:
            item = get_object_or_404(models.InvoiceItem, pk=item_pk)
            context['description'] = item.description
            context['cost'] = item.cost
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
