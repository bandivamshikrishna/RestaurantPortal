from django import forms
from .models import Table,Food
from django.forms.utils import ErrorList
from subadmin.models import SubAdmin



class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number','seater','pic']

    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data.get('number'):
            self._errors['number'] = ErrorList(['Please Enter Table Number.'])
        if not cleaned_data.get('seater'):
            self._errors['seater'] = ErrorList(['Please Enter Table Seater.'])
        if not cleaned_data.get('pic'):
            self._errors['pic'] = ErrorList(['Please Upload the Table Pic.'])


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name','category','pic','price']

    def clean(self):
        cleaned_data = super().clean()
        
        if not cleaned_data.get('name'):
            self._errors['name'] =  ErrorList(['Please Enter Food Name.'])
        if not cleaned_data.get('category'):
            self._errors['category'] = ErrorList(['Please Enter Food Category.'])
        if not cleaned_data.get('pic'):
            self._errors['pic'] = ErrorList(['Please Upload Food Pic.'])
        if not cleaned_data.get('price'):
            self._errors['price'] = ErrorList(['Please Enter Food Price.'])


class SubAdminForm(forms.ModelForm):
    class Meta:
        model = SubAdmin
        fields = ['mobile_number','pic','restaurant']
    
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('mobile_number'):
            self._errors['mobile_number'] = ErrorList(['Please Enter Mobile Number'])
        
        if not cleaned_data.get('pic'):
            self._errors['pic'] = ErrorList(['Please Upload the Profile Pic.'])
        
        if self._errors.get('restaurant'):
            if 'This field is required.' in str(self._errors.get('restaurant')):
                self._errors['restaurant'] = ErrorList(['Please Enter Restaurant'])
            else:
                self._errors['restaurant'] = ErrorList([self._errors.get('restaurant')])
    

class SubAdminUpdateForm(forms.ModelForm):
    class Meta:
        model = SubAdmin
        fields = ['mobile_number','pic']
    
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('mobile_number'):
            self._errors['mobile_number'] = ErrorList(['Please Enter Mobile Number'])
        
        if not cleaned_data.get('pic'):
            self._errors['pic'] = ErrorList(['Please Upload the Profile Pic.'])
    
