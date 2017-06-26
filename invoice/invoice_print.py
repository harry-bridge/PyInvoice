from django.views import generic
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from z3c.rml import rml2pdf
from PyPDF2 import PdfFileMerger, PdfFileReader
import re
from io import BytesIO

from invoice import models


class InvoicePrint(generic.View):
    def get(self, request, pk):
        invoice = get_object_or_404(models.Invoice, pk=pk)
        user = get_object_or_404(models.UserDetails, pk=1)
        template = get_template('invoice_print.xml')

        # merger = PdfFileMerger()

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
        # merger.append(PdfFileReader(buffer))
        # buffer.close()
        #
        # terms = urllib2.urlopen(settings.TERMS_OF_HIRE_URL)
        # merger.append(StringIO.StringIO(terms.read()))
        #
        # merged = BytesIO()
        # merger.write(merged)

        response = HttpResponse(content_type='application/pdf')

        # escaped_invoice_name = re.sub('[^a-zA-Z0-9 \n\.]', '', object.company)

        response['Content-Disposition'] = "filename=N%04d | %s.pdf" % (invoice.pk, invoice.company)
        response.write(buf.read())
        return response
