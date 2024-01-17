from django import forms
from .models import Restaurant
from django.forms.utils import ErrorList
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('name'):
            self._errors['name'] = ErrorList(['Please Enter Restaurant Name'])

        if not cleaned_data.get('address'):
            self._errors['address'] = ErrorList(['Please Enter Restaurant Address'])

        if not cleaned_data.get('pic'):
            self._errors['pic'] = ErrorList(['Please Upload Restaurant Picture'])



#User Form
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','username']
    
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('email'):
            self._errors['email'] = ErrorList(['Please Enter Email ID'])
        if self._errors.get('username'):
            if 'This field is required.' in str(self._errors.get('username')):
                self._errors['username'] = ErrorList(['Please Enter User Name'])
            else:
                self._errors['username'] = ErrorList([self._errors.get('username')])

        if self._errors.get('password1'):
            if 'This field is required.' in str(self._errors.get('password1')):
                self._errors['password1'] = ErrorList(['Please Enter Password'])
            else:
                self._errors['password1'] = ErrorList([self._errors.get('password1')])

        if self._errors.get('password2'):
            if 'This field is required.' in str(self._errors.get('password2')):
                self._errors['password2'] = ErrorList(['Please Enter Confirmation Password'])
            else:
                self._errors['password2'] = ErrorList([self._errors.get('password2')])


#User Update Form
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email'] 
    
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('email'):
            self._errors['email'] = ErrorList(['Please Enter Email ID'])

        if self._errors.get('username'):
            if 'This field is required.' in str(self._errors.get('username')):
                self._errors['username'] = ErrorList(['Please Enter User Name'])
            else:
                self._errors['username'] = ErrorList([self._errors.get('username')])