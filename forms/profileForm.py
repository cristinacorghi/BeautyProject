from django import forms
from django.forms import ModelForm
from Store.models.profileModel import Profile
from django.contrib.auth.forms import UserChangeForm
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
    Form Validation Error
    If any error happened in your form, this function returns the error message.
    """
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg


'''class EditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')'''
