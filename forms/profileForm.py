from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import (
    authenticate,
    get_user_model,
)

User = get_user_model()


class EditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
