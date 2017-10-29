from django.contrib.auth.models import User
from .models import Contacts,Numbers
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = [
            'contact_name',
            'email',
            'photo',
        ]

class NumbersForm(forms.ModelForm):
    class Meta:
        model = Numbers
        fields = [
            'phone_number',
            'number_type'
        ]