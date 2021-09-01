from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from Store.models.userModel import Profile
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


class ProfilePicForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic',)
