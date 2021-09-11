from django import forms
from django.forms import ModelForm
from Store.models.profileModel import Profile
from django.contrib.auth import (
    authenticate,
    get_user_model,
)

User = get_user_model()


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


def form_validation_error(form):
    """
    Form Validation Error: per qualsiasi errore che succede al form, questa funzione restituisce un messaggio d'errore
    """
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg
