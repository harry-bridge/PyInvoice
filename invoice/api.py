from django.shortcuts import HttpResponse, get_object_or_404
import simplejson as json

from invoice import models


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
