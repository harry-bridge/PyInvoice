from django.views import generic
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from z3c.rml import rml2pdf

from invoice import models


class InvoicePrint(generic.View):
    def get(self, request, pk):
        invoice = get_object_or_404(models.Invoice, pk=pk)
        user = self.request.user

        if invoice.user != user:
            raise PermissionDenied()

        if user.username == 'harry':
            logo_path = 'hb-invoice-logo.png'
        else:
            logo_path = 'default-logo.png'

        template = get_template('invoice_print.xml')

        context = {
            'invoice': invoice,
            'user': user,
            'fonts': {
                'roboto': {
                    'regular': 'invoice/static/fonts/roboto/Roboto-Light.ttf',
                    'bold': 'invoice/static/fonts/roboto/Roboto-Regular.ttf',
                }
            },
            'logo': 'invoice/static/imgs/paperwork/{}'.format(logo_path)
        }

        rml = template.render(context)

        buf = rml2pdf.parseString(rml)

        response = HttpResponse(content_type='application/pdf')

        if invoice.user_invoice_number:
            invoice_number = invoice.user_invoice_number
        else:
            invoice_number = 'N%04d' % invoice.pk

        response['Content-Disposition'] = "filename=%s | %s.pdf" % (invoice_number, str(invoice.company).replace(',', ''))
        response.write(buf.read())
        return response
