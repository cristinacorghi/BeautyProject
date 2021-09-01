from django import forms
from .models import CustomerPayment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from crispy_forms.bootstrap import FormActions


class CustomerPaymentForm(forms.ModelForm):
    class Meta:
        model = CustomerPayment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
