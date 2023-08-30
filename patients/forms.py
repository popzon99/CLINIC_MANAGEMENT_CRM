from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Patient, GENDER_CHOICES, BLOOD_GROUP_CHOICES, Tag
from branches.models import Branch
from physiotherapists.models import Speciality

class RegisterPatientForm(UserCreationForm):
    # Basic Details
    address = forms.CharField(widget=forms.Textarea)
    phone = forms.CharField(max_length=15)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    
    # Medical Information
    height = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    weight = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    blood_group = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES, required=False)
    notes = forms.CharField(widget=forms.Textarea, required=False)
    
    # Additional Details
    specialities = forms.ModelMultipleChoiceField(queryset=Speciality.objects.all(), required=False)
    location = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False)
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = Patient
        fields = ['username', 'email', 'password1', 'password2', 'address', 'phone', 'date_of_birth', 'gender', 'height', 
                  'weight', 'blood_group', 'notes', 'specialities', 'location', 'profile_photo']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        
        patient = Patient(user=user, **{field: self.cleaned_data[field] for field in self.Meta.fields if field not in ['username', 'email', 'password1', 'password2']})
        if commit:
            patient.save()
        
        return user




class PatientFilterForm(forms.Form):
    name = forms.CharField(label='Patient Name', required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter patient name'}))
    phone = forms.CharField(label='Phone', required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}))
    gender = forms.ChoiceField(label='Gender', choices=[('', 'All')] + list(GENDER_CHOICES), required=False, widget=forms.Select(attrs={'class': 'custom-select'}))
    location = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False)
    speciality = forms.ModelMultipleChoiceField(queryset=Speciality.objects.all(), required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    date_added_from = forms.DateField(label='Date Added From', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    date_added_to = forms.DateField(label='Date Added To', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    order_by = forms.ChoiceField(label='Order By', choices=[('date_added', 'Date Added'), ('user__first_name', 'Name')], required=False, widget=forms.Select(attrs={'class': 'custom-select'}))

    def filter_queryset(self, queryset):
        name = self.cleaned_data.get('name')
        phone = self.cleaned_data.get('phone')
        gender = self.cleaned_data.get('gender')
        location = self.cleaned_data.get('location')
        speciality = self.cleaned_data.get('speciality')
        tags = self.cleaned_data.get('tags')
        date_added_from = self.cleaned_data.get('date_added_from')
        date_added_to = self.cleaned_data.get('date_added_to')
        order_by = self.cleaned_data.get('order_by')

        if name:
            queryset = queryset.filter(user__first_name__icontains=name) | queryset.filter(user__last_name__icontains=name)
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
        if gender:
            queryset = queryset.filter(gender=gender)
        if location:
            queryset = queryset.filter(location=location)
        if speciality:
            queryset = queryset.filter(specialities__in=speciality)
        if tags:
            queryset = queryset.filter(tags__in=tags)
        if date_added_from:
            queryset = queryset.filter(date_added__gte=date_added_from)
        if date_added_to:
            queryset = queryset.filter(date_added__lte=date_added_to)
        if order_by:
            queryset = queryset.order_by(order_by)

        return queryset.distinct()  # We add .distinct() to ensure that we don't get duplicate entries

