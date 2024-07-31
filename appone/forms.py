from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from . models import *
from django.core.exceptions import ValidationError

class SignupForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=[('consumer', 'Consumer'), ('seller', 'Seller'), ('employee', 'Employee')], required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class WasteRequestForm(forms.ModelForm):
    class Meta:
        model = WasteRequest
        fields = ['name', 'organization_name', 'phone_number', 'email_id', 'waste_type', 'amount_needed']
        widgets = {
            'waste_type': forms.Select(choices=WasteRequest.WASTE_TYPE_CHOICES),
            'amount_needed': forms.NumberInput(attrs={'min': 0}),
            'phone_number': forms.TextInput(attrs={
                'pattern': '[0-9]{10}',  # Ensure 10-digit phone number
                'title': 'Please enter a 10-digit phone number'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isalpha():
            raise ValidationError("Name should only contain alphabetic characters.")
        return name

    def clean_organization_name(self):
        organization_name = self.cleaned_data.get('organization_name')
        if not organization_name.isalpha():
            raise ValidationError("Organization Name should only contain alphabetic characters.")
        return organization_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        waste_type = cleaned_data.get('waste_type')
        amount_needed = cleaned_data.get('amount_needed')

        if waste_type and amount_needed is not None:
            # Get the current month's PlasticItem
            year, month = PlasticItem.get_current_month()
            try:
                plastic_item = PlasticItem.objects.get(date__year=year, date__month=month)
            except PlasticItem.DoesNotExist:
                plastic_item = PlasticItem(date=f"{year}-{month}-01")  # Create a default instance if not found

            # Check if there is enough available for the requested amount
            if waste_type == 'PET' and amount_needed > plastic_item.pet:
                self.add_error('amount_needed', 'Not enough PET waste available for this month.')
            elif waste_type == 'HDPE' and amount_needed > plastic_item.hdpe:
                self.add_error('amount_needed', 'Not enough HDPE waste available for this month.')
            elif waste_type == 'PVC' and amount_needed > plastic_item.pvc:
                self.add_error('amount_needed', 'Not enough PVC waste available for this month.')
            elif waste_type == 'Organic' and amount_needed > plastic_item.organic:
                self.add_error('amount_needed', 'Not enough Organic waste available for this month.')
            elif waste_type == 'Others' and amount_needed > plastic_item.other:
                self.add_error('amount_needed', 'Not enough Other waste available for this month.')

        return cleaned_data
    


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'subject', 'message']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isalpha():
            raise ValidationError("Name should contain only alphabetic characters.")
        return name