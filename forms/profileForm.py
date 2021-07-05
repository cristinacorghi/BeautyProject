from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
)

User = get_user_model()


class ProfileForm(forms.Form):
    fullName = forms.CharField(max_length=150)
    email = forms.EmailField(widget=forms.EmailInput)
    mobilePhone = forms.CharField(max_length=10)
    address = forms.CharField(max_length=150)
