from django import forms
from .models import Invoice, InvoiceItem, ExportFormat
from patients.models import Patient
from physiotherapists.models import Therapist
from appointments.models import Appointment  # Import Appointment model

# Form for searching invoices
class SearchInvoiceForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search invoices based on name, id, patient ID, therapist name, appointment date...'}),
    )

# Form for selecting export format
class ExportFormatForm(forms.Form):
    export_format = forms.ModelChoiceField(
        queryset=ExportFormat.objects.all(),
        widget=forms.Select(attrs={'class': 'select2'}),
    )
# Main Invoice Form
class InvoiceForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class': 'select2'}),
    )
    invoice_date = forms.DateField(
        widget=forms.SelectDateWidget(),
    )
    appointment_date = forms.DateField(
        widget=forms.SelectDateWidget(),
    )
    appointment_time = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M'),
    )
    status = forms.ChoiceField(choices=Invoice.STATUS_CHOICES)
    payment_mode = forms.ChoiceField(choices=Invoice.PAYMENT_MODE_CHOICES)
    therapist = forms.ModelChoiceField(
        queryset=Therapist.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'select2'}),
    )
    appointment = forms.ModelChoiceField(  # Add this field
        queryset=Appointment.objects.all(),
        required=False,  # Make it optional
        widget=forms.Select(attrs={'class': 'select2'}),
    )
    
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'patient', 'invoice_date', 'appointment_date', 'appointment_time', 'status', 'payment_mode', 'therapist', 'appointment']  # Add 'appointment' to fields list

    def clean(self):
        cleaned_data = super().clean()
        # Additional validations can be added here
        return cleaned_data

# Invoice Item Form
class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['item_name', 'description', 'amount']

    def clean_amount(self):
        data = self.cleaned_data['amount']
        if data <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return data

# Formset for Invoice Items
InvoiceItemFormset = forms.inlineformset_factory(
    Invoice, InvoiceItem, 
    form=InvoiceItemForm, 
    extra=1, 
    can_delete=True
)
