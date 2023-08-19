from django import forms
from django.core.exceptions import ValidationError
from .models import Patient
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Patient
from .models import GENDER_CHOICES, BLOOD_GROUP_CHOICES
from branches.models import Branch
from physiotherapists.models import Speciality
from django.utils.translation import gettext_lazy as _


class AddPatientForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    specialities = forms.ModelMultipleChoiceField(queryset=Speciality.objects.all())
    location = forms.ModelChoiceField(queryset=Branch.objects.all())
    phone = forms.CharField(max_length=15)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)

    # Medical Information
    height = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    weight = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    blood_group = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES, required=False)
    notes = forms.CharField(widget=forms.Textarea, required=False)

    # Login Information
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    profile_photo = forms.ImageField(required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        if Patient.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Email already exists."))
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(_("Passwords do not match."))

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        exclude = ['user', 'email']  # Exclude user-related fields from the form


GENDER_CHOICES = [ 
    ('', 'All'),
    ('male', 'Male'),
    ('female', 'Female'),
]

class PatientFilterForm(forms.Form):
    name = forms.CharField(label='Patient Name', required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Enter patient name'}))
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, required=False,
                               widget=forms.Select(attrs={'class': 'custom-select'}))
    # Add more filter fields as needed

    def filter_queryset(self, queryset):
        name = self.cleaned_data.get('name')
        gender = self.cleaned_data.get('gender')

        if name:
            queryset = queryset.filter(name__icontains=name)
        
        if gender:
            queryset = queryset.filter(gender=gender)

        # ... Add more filter criteria as needed ...

        return queryset
