from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, FileResponse
from django.db import transaction
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from .forms import InvoiceForm, InvoiceItemFormset, SearchInvoiceForm, ExportFormatForm
from .models import Invoice,STATUS_CHOICES,InvoiceItem 
from patients.models import Patient
from appointments.models import Appointment
from django.db import transaction

import logging
import io



logger = logging.getLogger(__name__)

# Optional parameter for appointment ID
@transaction.atomic
def create_invoice(request, appointment_id=None):
    # Check if an appointment_id is passed and if it exists
    if appointment_id:
        appointment = get_object_or_404(Appointment, id=appointment_id)
    else:
        appointment = None

    if request.method == "POST":
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormset(request.POST, prefix='items')

        if form.is_valid() and formset.is_valid():
            try:
                invoice = form.save(commit=False)
                if appointment:
                    invoice.appointment = appointment  # Set appointment if available
                invoice.save()  # This will also call recalculate_totals
                
                formset.instance = invoice
                formset.save()
                
                # Recalculate totals and save again
                invoice.recalculate_totals()
                invoice.save()

                logger.info(f"Invoice {invoice.invoice_number} created successfully.")
                messages.success(request, 'Invoice created successfully.')
                return redirect('invoice_list')  # Replace with the name of your invoice list view

            except Exception as e:
                logger.error(f"Failed to create invoice: {e}")
                messages.error(request, 'Failed to create invoice.')
                return redirect('create_invoice')  # Replace with the name of your invoice create view
        else:
            messages.warning(request, 'There are errors in the submitted form.')
    else:
        # Pre-fill the form with appointment data if available
        form = InvoiceForm(initial={'appointment': appointment}) if appointment else InvoiceForm()
        formset = InvoiceItemFormset(prefix='items')

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'invoices/create_invoice.html', context)


def search_patients(request):
    query = request.GET.get('q', '')
    patients = Patient.objects.filter(name__icontains=query)[:5]  # Limit to 5 results
    patient_list = list(patients.values('name'))
    return JsonResponse({'patients': patient_list})



def invoice_list(request):
    search_form = SearchInvoiceForm(request.GET)
    query = request.GET.get('query', '')
    
    invoices_qs = Invoice.objects.all().order_by('-invoice_date')
    
    if query:
        invoices_qs = invoices_qs.filter(
            Q(invoice_number__icontains=query) |
            Q(patient__patient_id__icontains=query) |
            Q(therapist__name__icontains=query) |
            Q(appointment__appointment_date__icontains=query)
        )
    
    paginator = Paginator(invoices_qs, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    export_form = ExportFormatForm()

    context = {
        'search_form': search_form,
        'page_obj': page_obj,
        'export_form': export_form,
    }

    return render(request, 'invoice_list.html', context)



def update_invoice_status(request, invoice_id):
    if request.is_ajax():  # Check if it's an AJAX request
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return JsonResponse({"error": "Invoice not found"}, status=404)

        new_status = request.POST.get('status')
        valid_statuses = [choice[0].lower() for choice in STATUS_CHOICES]
        if new_status.lower() in valid_statuses:
            with transaction.atomic():
                invoice.status = new_status
                invoice.save()
            return JsonResponse({"message": "Status updated successfully"})
        else:
            return JsonResponse({"error": "Invalid status"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)



def export_invoices(request):
    if request.is_ajax():  # Check if it's an AJAX request
        export_form = ExportFormatForm(request.POST)
        
        if export_form.is_valid():
            export_format = export_form.cleaned_data['export_format']
            selected_invoices = request.POST.getlist('selected_invoices')
            
            # Error handling for non-existent invoices
            missing_invoices = [inv for inv in selected_invoices if not Invoice.objects.filter(id=inv).exists()]
            if missing_invoices:
                return JsonResponse({"error": f"Could not find invoices with IDs: {', '.join(missing_invoices)}"}, status=404)

            if export_format.format_name == 'PDF':
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="invoices.pdf"'
                
                # Create the PDF object
                pdf = SimpleDocTemplate(
                    response,
                    pagesize=letter
                )

                # Create the table
                data = [['Invoice No', 'Patient ID', 'Name', 'Doctor', 'Appointment Date', 'Time', 'Status']]
                for invoice_id in selected_invoices:
                    invoice = Invoice.objects.get(id=invoice_id)
                    data.append([
                        invoice.invoice_number,
                        invoice.patient.patient_id,
                        invoice.patient.name,
                        invoice.therapist.name,
                        invoice.appointment.appointment_date,
                        invoice.appointment.time,  # Modify based on your actual model
                        invoice.status
                    ])

                # Add Table Style
                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))

                # Add table to elements to build
                elements = []
                elements.append(table)

                # Generate PDF
                pdf.build(elements)

                return response
            
            return JsonResponse({"message": f"Invoices exported in {export_format.format_name} format."})
            
    return JsonResponse({"error": "Invalid request"}, status=400)


def paid_invoices(request):
    # Only filter invoices with 'paid' status
    invoices_qs = Invoice.objects.filter(status='paid').order_by('-invoice_date')
    
    # Paginator and other logic can remain similar to invoice_list()
    paginator = Paginator(invoices_qs, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'paid_invoices.html', context)


def unpaid_invoices(request):
    # Only filter invoices with 'unpaid' status
    invoices_qs = Invoice.objects.filter(status='unpaid').order_by('-invoice_date')
    
    # Paginator and other logic can remain similar to invoice_list()
    paginator = Paginator(invoices_qs, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'unpaid_invoices.html', context)


 # Make sure to import InvoiceItem

def view_paid_invoice(request, invoice_id):
    try:
        invoice = Invoice.objects.get(invoice_number=invoice_id, status='paid')  # Fetch the invoice by its number and status
        invoice.recalculate_totals()  # Update totals in case they are outdated
        invoice.save()  # Persist the changes
        items = InvoiceItem.objects.filter(invoice=invoice)  # Fetch the related items
    except Invoice.DoesNotExist:
        return redirect('paid_invoices')  # Redirect if the invoice does not exist or is not paid

    context = {
        'invoice': invoice,
        'items': items,
        'subtotal': invoice.subtotal,
        'tax': invoice.tax,
        'total': invoice.total_amount,
    }
    
    return render(request, 'view_paid_invoice.html', context)




def view_unpaid_invoice(request, invoice_id):
    try:
        invoice = Invoice.objects.get(invoice_number=invoice_id, status='unpaid')  # Fetch the invoice by its number and status
        invoice.recalculate_totals()  # Update totals in case they are outdated
        invoice.save()  # Persist the changes
        items = InvoiceItem.objects.filter(invoice=invoice)  # Fetch the related items
    except Invoice.DoesNotExist:
        return redirect('unpaid_invoices')  # Redirect if the invoice does not exist or is not unpaid

    context = {
        'invoice': invoice,
        'items': items,
        'subtotal': invoice.subtotal,
        'tax': invoice.tax,
        'total': invoice.total_amount,
    }
    
    return render(request, 'view_unpaid_invoice.html', context)

