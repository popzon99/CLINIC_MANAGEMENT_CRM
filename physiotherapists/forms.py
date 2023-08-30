from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from .models import Speciality, WorkingDay, Therapist, TherapistWorkingDay, TimeSlot,Prescription
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Speciality, WorkingDay, Therapist, TherapistWorkingDay, TimeSlot, Prescription
from branches.models import Branch
from appointments.models import Appointment
from patients.models import Patient



class AddTherapistForm(forms.ModelForm):
    email = forms.EmailField(label=_('Email'))
    password1 = forms.CharField(widget=forms.PasswordInput, label=_('Set Password'))
    password2 = forms.CharField(widget=forms.PasswordInput, label=_('Confirm Password'))
    working_days = forms.ModelMultipleChoiceField(
        queryset=WorkingDay.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=_('Working Days')
    )

    class Meta:
        model = Therapist
        fields = [
            'name',
            'address',
            'qualification',
            'specialities',
            'branch',
            'phone',
            'date_of_birth',
            'gender',
            'appointment_interval',
            'is_active',
            'profile_photo',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for day in WorkingDay.objects.all():
            field_name = f'time_slot_{day.day_name}'
            label = _('Time Slot for ') + day.day_name
            widget = forms.TextInput(attrs={'placeholder': _('e.g. 09:00-12:00, 14:00-18:00')})
            self.fields[field_name] = forms.CharField(label=label, widget=widget, required=False)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords do not match."))
        validate_password(password2)
        return password2


class AddSpecialityForm(forms.ModelForm):
    class Meta:
        model = Speciality
        fields = ['name', 'description']
        labels = {
            'name': _('Name'),
            'description': _('Description'),
        }


class PrescriptionForm(forms.ModelForm):
    appointment = forms.ModelChoiceField(
        queryset=Appointment.objects.all(),
        widget=forms.Select(attrs={'class': 'selectpicker'}),
        label=_('Appointment'),
    )
    therapist = forms.ModelChoiceField(
        queryset=Therapist.objects.all(),
        widget=forms.Select(attrs={'class': 'selectpicker'}),
        label=_('Therapist'),
        disabled=True,  # disable this if it should be automatically filled
    )
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class': 'selectpicker'}),
        label=_('Patient'),
        disabled=True,  # disable this if it should be automatically filled
    )
    medication = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label=_('Medication'),
    )
    dosage = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label=_('Dosage'),
    )
    frequency = forms.ChoiceField(
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
        widget=forms.RadioSelect,
        label=_('Frequency'),
    )
    additional_notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label=_('Additional Notes'),
    )

    class Meta:
        model = Prescription
        fields = [
            'appointment',
            'therapist',
            'patient',
            'medication',
            'dosage',
            'frequency',
            'additional_notes',
        ]

    def clean(self):
        cleaned_data = super().clean()
        # Add custom validations here.
        # Example: Ensure the therapist and patient match the appointment
        therapist = cleaned_data.get('therapist')
        patient = cleaned_data.get('patient')
        appointment = cleaned_data.get('appointment')
        
        if appointment:
            if therapist and therapist != appointment.therapist:
                self.add_error('therapist', ValidationError(_('Therapist does not match with the appointment.')))
            
            if patient and patient != appointment.patient:
                self.add_error('patient', ValidationError(_('Patient does not match with the appointment.')))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamic initial data or queryset can be set here
        # self.fields['appointment'].queryset = ...