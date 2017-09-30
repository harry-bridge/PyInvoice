from django.views import generic
from django.shortcuts import get_object_or_404, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse, QueryDict
from django.contrib.auth import views
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.db.models import Q
import json

from invoice import models, forms


class Login(views.LoginView):
    template_name = 'registration/login.html'


class Logout(views.LogoutView):
    template_name = 'registration/logout.html'


class PasswordChange(views.PasswordChangeView):
    template_name = 'registration/password_change.html'

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'pk': self.request.user.id})


class Index(LoginRequiredMixin, generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        invoice = models.Invoice.objects.filter(user=self.request.user)
        context['not_paid_count'] = invoice.filter(paid=False).count()
        context['last_invoice'] = invoice.last()
        context['latest_invoices'] = invoice.order_by('-created')[:5]
        context['pending_invoices'] = invoice.filter(paid=False).order_by('created')

        context['not_paid_total'] = 0
        for invoice in models.Invoice.objects.filter(user=self.request.user, paid=False):
            context['not_paid_total'] += invoice.total()

        return context


class InvoiceList(LoginRequiredMixin, generic.ListView):
    model = models.Invoice
    template_name = 'invoice_list.html'
    ordering = '-created'

    def get_queryset(self):
        q = Q()
        q &= Q(user=self.request.user)
        paid = self.request.GET.get('paid')
        if paid:
            q &= Q(paid=paid in 'true')

        return models.Invoice.objects.filter(q).order_by('-created')


class InvoiceDetail(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = models.Invoice
    template_name = 'invoice_form.html'

    def test_func(self):
        obj = super(InvoiceDetail, self).get_object()
        return self.request.user == obj.user


class InvoiceCreate(LoginRequiredMixin, generic.TemplateView):
    template_name = 'invoice_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreate, self).get_context_data(**kwargs)
        context['companies'] = models.Company.objects.all()

        context['edit'] = True
        return context


class InvoiceEdit(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'invoice_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceEdit, self).get_context_data(**kwargs)
        context['companies'] = models.Company.objects.all()
        context['invoice'] = get_object_or_404(models.Invoice, pk=self.kwargs['pk'])
        context['edit'] = True

        return context

    def test_func(self):
        return self.request.user == self.get_context_data()['invoice'].user


@login_required()
def invoice_update(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        defaults = QueryDict(request.POST['invoice_form'].encode('ASCII')).dict()
        defaults.pop('csrfmiddlewaretoken')
        invoice_pk = int(defaults.pop('pk'))

        defaults['company'] = get_object_or_404(models.Company, pk=int(defaults.pop('company')))
        defaults['user'] = get_object_or_404(models.Profile, pk=int(defaults.pop('user')))

        phone = defaults.pop('phone')
        defaults['phone'] = int(phone) if phone.strip() else None

        defaults['utr'] = bool(defaults.pop('utr', None))
        defaults['paid'] = bool(defaults.pop('paid', None))
        defaults['is_quote'] = bool(defaults.pop('is_quote', None))

        if invoice_pk == 0:
            invoice = models.Invoice.objects.create(**defaults)
            context['url'] = reverse('invoice_edit', args=[invoice.pk])
        else:
            models.Invoice.objects.update_or_create(pk=invoice_pk, defaults=defaults)
            context['url'] = reverse('invoice_detail', args=[invoice_pk])

        return HttpResponse(json.dumps(context), content_type='application/json')


@login_required()
def invoice_item_update(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        defaults = QueryDict(request.POST['invoice_item_form'].encode('ASCII')).dict()
        defaults.pop('csrfmiddlewaretoken')

        defaults['invoice'] = models.Invoice.objects.get(pk=request.POST['invoice_pk'])
        item_pk = defaults.pop('item_pk')
        defaults['quantity'] = float(defaults.pop('quantity'))

        if item_pk == '0':
            models.InvoiceItem.objects.create(**defaults)

        else:
            models.InvoiceItem.objects.update_or_create(pk=item_pk, defaults=defaults)

        context['invoice'] = defaults['invoice']
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

    def get_context_data(self, **kwargs):
        context = super(CompanyDetail, self).get_context_data(**kwargs)
        invoice = models.Invoice.objects.filter(user=self.request.user, company=self.object)
        context['not_paid_count'] = invoice.filter(paid=False).count()
        context['all_invoices'] = invoice.order_by('-created')

        return context


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


@login_required()
def profile_update(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        form = QueryDict(request.POST['profile_form'].encode('ASCII')).dict()
        form.pop('csrfmiddlewaretoken')
        pk = form.pop('pk')

        for key, value in form.items():
            if not value:
                form[key] = None

        if pk:
            models.Profile.objects.update_or_create(pk=pk, defaults=form)
            context['url'] = reverse('profile_detail', args=[pk])

    return HttpResponse(json.dumps(context), content_type='application/json')


# class ProfileUpdate(generic.View):
#     def post(self, request):
#         form = forms.PhotoForm(self.request.POST, self.request.FILES)
#         if form.is_valid():
#             photo = form.save()
#             data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
#         else:
#             data = {'is_valid': False}
#         return JsonResponse(data)


class ExpenseList(LoginRequiredMixin, generic.ListView):
    model = models.Expense
    template_name = 'expense_list.html'


class ExpenseDetail(LoginRequiredMixin, generic.DetailView):
    model = models.Expense
    template_name = 'expense_update.html'

    def get_context_data(self, **kwargs):
        context = super(ExpenseDetail, self).get_context_data(**kwargs)
        context['expense_list'] = self.object.invoice.expenses

        return context


class ExpenseCreate(LoginRequiredMixin, generic.TemplateView):
    template_name = 'expense_update.html'

    def get_context_data(self, **kwargs):
        context = super(ExpenseCreate, self).get_context_data(**kwargs)
        context['edit'] = True
        context['invoices'] = models.Invoice.objects.all()
        context['redirect_on_save'] = 1

        return context


@login_required()
def expense_update(request):
    context = dict()
    if request.method == 'POST' and request.is_ajax():
        defaults = QueryDict(request.POST['expense_form'].encode('ASCII')).dict()
        defaults.pop('csrfmiddlewaretoken')
        defaults['invoice'] = models.Invoice.objects.get(pk=defaults.pop('invoice'))
        context['expense_pk'] = defaults.pop('expense_pk')
        redirect = defaults.pop('redirect_on_save')

        if context['expense_pk'] != '0':
            expense, created = models.Expense.objects.update_or_create(pk=context['expense_pk'], defaults=defaults)

        else:
            expense = models.Expense.objects.create(**defaults)

        if redirect == '1':
            context['url'] = reverse('expense_detail', args=[expense.pk])

            return HttpResponse(json.dumps(context), content_type='application/json')
        else:
            context['expense_list'] = expense.invoice.expenses
            html = render_to_string('expense_table.html', context=context)
            return HttpResponse(html)
