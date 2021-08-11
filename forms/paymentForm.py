from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class PaymentForm(ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=300)
    phone_number = forms.IntegerField
    address = forms.CharField(max_length=500)
    city = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
