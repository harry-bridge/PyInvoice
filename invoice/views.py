from django.views import generic
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
import json

from invoice import models


def login_view(request, **kwargs):
    if request.user.is_authenticated():
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)
    else:
        return login(request)


def logout_view(request):
    logout(request)
    return render_to_response('registration/logout.html')


class Index(LoginRequiredMixin, generic.TemplateView):
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


class InvoiceList(LoginRequiredMixin, generic.ListView):
    model = models.Invoice
    template_name = 'invoice_list.html'
    ordering = '-created'


class InvoiceDetail(LoginRequiredMixin, generic.DetailView):
    model = models.Invoice
    template_name = 'invoice_form.html'


class InvoiceCreate(LoginRequiredMixin, generic.TemplateView):
    template_name = 'invoice_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreate, self).get_context_data(**kwargs)
        context['companies'] = models.Company.objects.all()

        context['edit'] = True
        return context


class InvoiceEdit(LoginRequiredMixin, generic.TemplateView):
    template_name = 'invoice_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceEdit, self).get_context_data(**kwargs)
        context['companies'] = models.Company.objects.all()
        context['invoice'] = get_object_or_404(models.Invoice, pk=self.kwargs['pk'])
        context['edit'] = True

        return context


@login_required()
def invoice_update(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        defaults = dict()
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


@login_required()
def invoice_item_update(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        defaults = dict()
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


@login_required()
def invoice_item_delete(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        invoice_pk = request.POST['invoice_pk']
        item_pk = request.POST['item_pk']
        item = get_object_or_404(models.InvoiceItem, pk=item_pk)
        item.delete(keep_parents=True)

        context['invoice'] = get_object_or_404(models.Invoice, pk=invoice_pk)
        context['edit'] = True

        return render_to_response('item_table.html', context)


@login_required()
def invoice_delete(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        invoice_pk = request.POST['invoice_pk']

        invoice = get_object_or_404(models.Invoice, pk=invoice_pk)
        invoice.delete()

        context['deleted'] = True
        context['url'] = '/invoice/list/'

    return HttpResponse(json.dumps(context), content_type='application/json')


class CompanyList(LoginRequiredMixin, generic.ListView):
    model = models.Company
    template_name = 'company_list.html'


class CompanyDetail(LoginRequiredMixin, generic.DetailView):
    model = models.Company
    template_name = 'company_update.html'


class CompanyCreate(LoginRequiredMixin, generic.TemplateView):
    template_name = 'company_update.html'


class CompanyEdit(LoginRequiredMixin, generic.TemplateView):
    template_name = 'company_update.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyEdit, self).get_context_data(**kwargs)
        context['company'] = get_object_or_404(models.Company, pk=self.kwargs['pk'])
        context['edit'] = True

        return context


@login_required()
def company_update(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        defaults = dict()
        context['company_pk'] = int(request.POST.get('company_pk', '0'))
        context['redirect'] = bool(int(request.POST.get('redirect_on_save', '0')))

        defaults['name'] = request.POST['name']
        defaults['address'] = request.POST['address']
        defaults['email'] = request.POST['email']

        if context['company_pk'] == 0:
            company = models.Company.objects.create(**defaults)
            context['company_pk'] = company.pk
            context['company_name'] = company.name

        else:
            company, created = models.Company.objects.update_or_create(pk=context['company_pk'], defaults=defaults)

            context['name'] = company.name

        if context['redirect']:
            context['url'] = '/company/' + str(context['company_pk'])

    return HttpResponse(json.dumps(context), content_type='application/json')


@login_required()
def company_delete(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        company_pk = request.POST['company_pk']

        company = get_object_or_404(models.Company, pk=company_pk)
        company.delete()

        context['deleted'] = True
        context['url'] = '/company/list/'

    return HttpResponse(json.dumps(context), content_type='application/json')


class ProfileDetail(LoginRequiredMixin, generic.TemplateView):
    template_name = 'registration/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        context['user'] = get_object_or_404(models.Profile, pk=self.kwargs['pk'])


class ProfileEdit(LoginRequiredMixin, generic.TemplateView):
    template_name = 'registration/profile_form.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileEdit, self).get_context_data(**kwargs)
        context['user'] = get_object_or_404(models.Profile, pk=self.kwargs['pk'])


def profile_update(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        form = QueryDict(request.POST['profile_form'].encode('ASCII')).dict()
        form.pop('csrfmiddlewaretoken')
        pk = form.pop('pk')

        if pk:
            models.Profile.objects.update_or_create(pk=pk, defaults=form)
            context['url'] = reverse('profile_detail', args=[pk])

    return HttpResponse(json.dumps(context), content_type='application/json')
