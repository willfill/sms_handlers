# coding: utf-8

from django import forms
from django.core.validators import RegexValidator

from handlers.gates import registry


phone_validator = RegexValidator(
    regex=r'^\d{11}$',
    message='Invalid number format'
)


class MessageForm(forms.Form):
    phone = forms.CharField(widget=forms.widgets.TextInput(), validators=[phone_validator])
    message = forms.CharField(min_length=1, widget=forms.widgets.Textarea())
    gateway = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields['gateway'].choices = [(gw, gw) for gw in registry.keys()]
