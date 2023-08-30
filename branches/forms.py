from django import forms
from .models import Branch

class BranchForm(forms.Form):
    name = forms.CharField(max_length=100, label="Branch Name")
    email = forms.EmailField(label="Email")
    address = forms.CharField(widget=forms.Textarea, label="Address")
    phone_number = forms.CharField(max_length=20, label="Phone Number")
    is_active = forms.BooleanField(required=False, initial=True, label="Active")

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone_number

class AddBranchForm(forms.Form):
    name = forms.CharField(max_length=100, label="Branch Name")
    email = forms.EmailField(label="Email")
    address = forms.CharField(widget=forms.Textarea, label="Address")
    phone_number = forms.CharField(max_length=20, label="Phone Number")

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone_number

