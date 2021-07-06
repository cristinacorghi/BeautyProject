from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
)

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # controlla che la password per quel nome utente sia corretta e che l'utente non sia stato
    # disabilitato
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            # restituisce un oggetto User se la coppia username e password è corretta
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Controlla di aver scritto correttamente la password. Se "
                                            "la password è corretta allora l'utente è inesistente")
        return super(UserLoginForm, self).clean(*args, **kwargs)
