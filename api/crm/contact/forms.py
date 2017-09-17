from django import forms
from .models import Contact, ContactPhone, ContactEmail


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude=['uid', 'seq']


class ContactPhoneForm(forms.ModelForm):
    class Meta:
        model = ContactPhone
        exclude = ['contact']


class ContactEmailForm(forms.ModelForm):
    class Meta:
        model = ContactEmail
        exclude = ['contact']
