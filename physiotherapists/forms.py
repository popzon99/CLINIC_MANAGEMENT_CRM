from django import forms
from .models import Speciality, WorkingDay
from branches.models import Branch
from django.utils.translation import gettext_lazy as _

class AddTherapistForm(forms.Form):
    name = forms.CharField(max_length=100, label=_('Name'))
    address = forms.CharField(widget=forms.Textarea, label=_('Address'))
    specialities = forms.ModelMultipleChoiceField(queryset=Speciality.objects.all(), label=_('Select Specialities'))
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), label=_('Select Branch'))
    phone = forms.CharField(max_length=15, label=_('Phone Number'))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label=_('Date of Birth'))
    GENDER_CHOICES = [
        ('male', _('Male')),
        ('female', _('Female')),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, label=_('Gender'))
    slots_per_minute = forms.IntegerField(label=_('Slots per Minute'))
    working_days = forms.ModelMultipleChoiceField(queryset=WorkingDay.objects.all(), widget=forms.CheckboxSelectMultiple, label=_('Working Days'))
    
    # Add time slot fields for each working day
    for day in WorkingDay.objects.all():
        field_name = f'time_slot_{day.day_name}'
        label = _('Time Slot for ') + day.day_name
        widget = forms.TextInput(attrs={'placeholder': _('e.g. 09:00-12:00, 14:00-18:00')})
        locals()[field_name] = forms.CharField(label=label, widget=widget)
    
    email = forms.EmailField(label=_('Email'))
    password = forms.CharField(widget=forms.PasswordInput, label=_('Set Password'))
    confirm_password = forms.CharField(widget=forms.PasswordInput, label=_('Confirm Password'))
    profile_photo = forms.ImageField(required=False, label=_('Upload Photo'))
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(_("Passwords do not match."))
        return confirm_password


class AddSpecialityForm(forms.ModelForm):
    class Meta:
        model = Speciality
        fields = ['name', 'description']
        labels = {
            'name': _('Name'),
            'description': _('Description'),
        }
