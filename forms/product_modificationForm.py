from django import forms
from Store.models.productModel import Product


class ModificaProdotto(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
