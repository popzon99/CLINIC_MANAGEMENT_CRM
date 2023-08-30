from django.db import models
from django.utils import timezone
from physiotherapists.models import Therapist
from patients.models import Patient
from appointments.models import Appointment  # Import Appointment model


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]
    
    PAYMENT_MODE_CHOICES = [
        ('cash', 'Cash Payment'),
        ('card', 'Card Payment'),
        ('net', 'Net Banking'),
    ]
    
    invoice_number = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, related_name='invoices', on_delete=models.CASCADE)
    invoice_date = models.DateField(default=timezone.now)
    appointment = models.OneToOneField(Appointment, null=True, blank=True, on_delete=models.SET_NULL, related_name='invoice')  # Added field
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODE_CHOICES)
    therapist = models.ForeignKey(Therapist, related_name='invoices', on_delete=models.SET_NULL, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def recalculate_totals(self):
        self.subtotal = sum(item.amount for item in self.invoice_items.all())
        self.tax = self.subtotal * 0.10  # Assuming a 10% tax rate for now
        self.total_amount = self.subtotal + self.tax

    def save(self, *args, **kwargs):
        self.recalculate_totals()
        
        if not self.invoice_number:
            current_date = timezone.now().strftime('%Y%m%d')
            last_invoice = Invoice.objects.filter(invoice_number__startswith=current_date).order_by('-invoice_number').first()
            
            if last_invoice:
                last_id = int(last_invoice.invoice_number.split('-')[1])
                self.invoice_number = '{}-{:04d}'.format(current_date, last_id + 1)
            else:
                self.invoice_number = '{}-{:04d}'.format(current_date, 1)
                
        super().save(*args, **kwargs)


    def __str__(self):
      return str(self.invoice_number)


# The rest of your models (InvoiceItem, ExportFormat, ExportedInvoice) remain unchanged


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='invoice_items', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.item_name

class ExportFormat(models.Model):
    format_name = models.CharField(max_length=50)

    def __str__(self):
        return self.format_name


class ExportedInvoice(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    export_format = models.ForeignKey(ExportFormat, on_delete=models.SET_NULL, null=True)
    exported_date = models.DateField(auto_now_add=True)
    file_path = models.FileField(upload_to='exported_invoices/')

    def __str__(self):
        return f"Exported {self.invoice}"
