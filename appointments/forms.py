from django import forms
from .models import Appointment, TimeSlot
from physiotherapists.models import Therapist, TherapistWorkingDay
from patients.models import Patient

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'therapist', 'appointment_date', 'time_slot', 'status']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'therapist': forms.Select(attrs={'class': 'form-control'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'time_slot': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        

        error_messages = {
            'appointment_date': {
                'required': 'Please select a valid date for the appointment.',
            },
            'time_slot': {
                'required': 'Please select a valid time slot.',
            },
        }




    def __init__(self, *args, **kwargs):
        patient = kwargs.pop('patient', None)  # Extract the 'patient' keyword argument if available
        super().__init__(*args, **kwargs)

        if patient:
            self.fields['patient'].initial = patient
            self.fields['patient'].queryset = Patient.objects.filter(id=patient.id)
            self.fields['patient'].disabled = True  # Disable this field if patient is already known

        if 'therapist' in self.data:
            try:
                therapist_id = int(self.data.get('therapist'))
                therapist = Therapist.objects.get(id=therapist_id)
                self.fields['time_slot'].queryset = TimeSlot.objects.filter(therapist=therapist)
            except (ValueError, Therapist.DoesNotExist):
                pass

