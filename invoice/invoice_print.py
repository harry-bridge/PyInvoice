from django.views import generic
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from z3c.rml import rml2pdf
from django.utils import timezone

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

        def generate_invoice_info():
            info = list()

            info.append('DATE   {}'.format(invoice.created.date()))
            info.append('INVOICE NO.   {}'.format(invoice.invoice_number()))

            if invoice.utr:
                info.append('UTR NO.   {}'.format(invoice.user.utr))

            if invoice.po_number:
                info.append('PO NO.   {}'.format(invoice.po_number))

            return info

        context = {
            'invoice': invoice,
            'user': user,
            'fonts': {
                'roboto': {
                    'regular': 'invoice/static/fonts/roboto/Roboto-Light.ttf',
                    'bold': 'invoice/static/fonts/roboto/Roboto-Regular.ttf',
                }
            },
            'logo': 'invoice/static/imgs/paperwork/{}'.format(logo_path),
            'invoice_info': generate_invoice_info()
        }

        rml = template.render(context)

        buf = rml2pdf.parseString(rml)

        response = HttpResponse(content_type='application/pdf')

        if invoice.user_invoice_number:
            invoice_number = invoice.user_invoice_number
        else:
            invoice_number = 'N%04d' % invoice.pk

        response['Content-Disposition'] = "filename={}_{}.pdf".format(
            invoice_number,
            str(invoice.company).replace(',', ' ')
        )
        # response['Content-Disposition'] = 'filename=test.pdf'
        response.write(buf.read())
        return response
