from django.urls import path
from . import views

app_name = 'your_app_name'  # replace 'your_app_name' with the name of your Django app

urlpatterns = [
    # Map the URL to the create_invoice view
    path('create_invoice/', views.create_invoice, name='create_invoice'),
    # Map the URL to the create_invoice view with an appointment ID
    path('create_invoice/<int:appointment_id>/', views.create_invoice, name='create_invoice_with_appointment'),

    # Map the URL for searching patients
    path('search_patients/', views.search_patients, name='search_patients'),

    # Map the URL to the invoice_list view
    path('invoice_list/', views.invoice_list, name='invoice_list'),

    # Map the URL to update the invoice status; It is AJAX based
    path('update_invoice_status/<int:invoice_id>/', views.update_invoice_status, name='update_invoice_status'),

    # Map the URL to export invoices; It is AJAX based
    path('export_invoices/', views.export_invoices, name='export_invoices'),

    # Map the URL to show all paid invoices
    path('paid_invoices/', views.paid_invoices, name='paid_invoices'),

    # Map the URL to show all unpaid invoices
    path('unpaid_invoices/', views.unpaid_invoices, name='unpaid_invoices'),

    # Map the URL to view a single paid invoice in detail
    path('view_paid_invoice/<int:invoice_id>/', views.view_paid_invoice, name='view_paid_invoice'),

    # Map the URL to view a single unpaid invoice in detail
    path('view_unpaid_invoice/<int:invoice_id>/', views.view_unpaid_invoice, name='view_unpaid_invoice'),
]

