from django.views import generic
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from z3c.rml import rml2pdf

from invoice import models


class InvoicePrint(generic.View):
    def get(self, request, pk):
        invoice = get_object_or_404(models.Invoice, pk=pk)
        user = get_object_or_404(models.Profile, pk=1)
        template = get_template('invoice_print.xml')

        context = {
            'invoice': invoice,
            'user': user,
            'fonts': {
                'roboto': {
                    'regular': 'static/fonts/roboto/Roboto-Thin.ttf',
                    'bold': 'static/fonts/roboto/Roboto-Light.ttf',
                }
            },
        }

        rml = template.render(context)

        buf = rml2pdf.parseString(rml)

        response = HttpResponse(content_type='application/pdf')

        response['Content-Disposition'] = "filename=N%04d | %s.pdf" % (invoice.pk, invoice.company)
        response.write(buf.read())
        return response
