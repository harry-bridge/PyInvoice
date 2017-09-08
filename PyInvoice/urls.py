"""PyInvoice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

from invoice import views, api, invoice_print

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout_view, name='logout'),
    url(r'^accounts/(?P<pk>\d+)/$', views.ProfileDetail.as_view(), name='profile_detail'),
    url(r'^accounts/(?P<pk>\d+)/edit/$', views.ProfileEdit.as_view(), name='profile_edit'),
    url(r'^accounts/update/$', views.profile_update, name='profile_update'),
    url(r'^accounts/password-reset/$', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html', success_url='/'), name='password_reset'),

    url(r'^$', views.Index.as_view(), name='index'),

    url(r'^invoice/list', views.InvoiceList.as_view(), name='invoice_list'),
    url(r'^invoice/(?P<pk>\d+)/$', views.InvoiceDetail.as_view(), name='invoice_detail'),
    url(r'^invoice/(?P<pk>\d+)/edit/$', views.InvoiceEdit.as_view(), name='invoice_edit'),
    url(r'^invoice/create/$', views.InvoiceCreate.as_view(), name='invoice_create'),
    url(r'^invoice/update/$', views.invoice_update, name='invoice_update'),
    url(r'^invoice/delete/$', views.invoice_delete, name='invoice_delete'),
    url(r'^invoice/(?P<pk>\d+)/print/$', invoice_print.InvoicePrint.as_view(), name='invoice_print'),

    url(r'invoice/item/update/$', views.invoice_item_update, name='invoice_item_update'),
    url(r'invoice/item/delete/$', views.invoice_item_delete, name='invoice_item_delete'),

    url(r'^company/list/$', views.CompanyList.as_view(), name='company_list'),
    url(r'^company/(?P<pk>\d+)/$', views.CompanyDetail.as_view(), name='company_detail'),
    url(r'^company/(?P<pk>\d+)/edit/$', views.CompanyEdit.as_view(), name='company_edit'),
    url(r'^company/create/$', views.CompanyCreate.as_view(), name='company_create'),
    url(r'^company/update/$', views.company_update, name='company_update'),
    url(r'^company/delete/$', views.company_delete, name='company_delete'),

    url(r'^api/get_items_for_table/$', api.get_items_for_table, name='get_items_for_table'),
    url(r'^api/get_company_for_modal/$', api.get_company_for_modal, name='get_company_for_modal'),
    url(r'^api/invoice_logo_upload/$', api.invoice_photo_upload, name='invoice_photo_upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
