from django import forms
from django.forms import ModelForm
from carts.models import Payment


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'city')
