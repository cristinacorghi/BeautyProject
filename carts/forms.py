from django import forms
from .models import CustomerPayment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from crispy_forms.bootstrap import FormActions


class CustomerPaymentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta:
        model = CustomerPayment
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # FormHelper è una classe che definisce il comportamento di rendering del modulo. In questo modo si scrive
        # meno HTML possibile e tutta la logica rimane nei moduli e nei file di visualizzazione.
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {
            'novalidate': ''
        }
        self.helper.layout = Layout(
            Row(
                Column('first_name'),
                Column('last_name'),
            ),
            Row(
                Column('email'),
                Column('phone'),
            ),
            Row(
                Column('address'),
                Column('city'),
            ),
            FormActions(
                Submit('pay', 'Pay')
            )
        )
