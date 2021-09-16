from django import forms
from Store.models.productModel import ProductReviewModel


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReviewModel
        fields = ('product', 'user', 'content', 'stars', 'date_added')
