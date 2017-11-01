from wtforms_alchemy import ModelForm

from .models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
