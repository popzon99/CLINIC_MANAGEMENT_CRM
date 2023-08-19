from django import forms


def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        # Custom phone number validation logic if needed
        return phone_number

class BranchForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    address = forms.CharField(label='Address', widget=forms.Textarea)
    phone_number = forms.CharField(label='Phone Number', max_length=15)
    is_working = forms.BooleanField(label='Is Working', required=False)

