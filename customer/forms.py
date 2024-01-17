from django import forms
from .models import Customer,CustomerTableOrders,CustomerFoodOrders
from django.forms.utils import ErrorList
from django.forms.widgets import DateTimeInput


class CustomerCUForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['mobile_number','pic']
    
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('mobile_number'):
            self._errors['mobile_number'] = ErrorList(['Please Enter Mobile Number'])
        
        if not cleaned_data.get('pic'):
            self._errors['pic'] = ErrorList(['Please Upload the Profile Pic.']) 


class CustomerTableOrdersForm(forms.ModelForm):
    class Meta:
        model = CustomerTableOrders
        fields = ['check_in','check_out']
        widgets = {
            'check_in': DateTimeInput(attrs={'type': 'datetime-local'}),
            'check_out': DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data.get('check_in'):
            self._errors['check_in'] = ErrorList(['Please Enter your Check In Time.'])

        if not cleaned_data.get('check_out'):
            self._errors['check_out'] = ErrorList(['Please Enter your Check Out Time.'])