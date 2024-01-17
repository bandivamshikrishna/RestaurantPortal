from django import forms
from django.forms.utils import ErrorList
from .models import RestUsers



class RestUsersCUForm(forms.ModelForm):
    class Meta:
        model = RestUsers
        fields = ['mobile_number','pic','user_type']
    
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('mobile_number'):
            self._errors['mobile_number'] = ErrorList(['Please Enter Mobile Number'])
        
        if not cleaned_data.get('pic'):
            self._errors['pic'] = ErrorList(['Please Upload the Profile Pic.']) 
        
        if not cleaned_data.get('user_type'):
            self._errors['user_type'] = ErrorList(['Please Select the User Type'])


