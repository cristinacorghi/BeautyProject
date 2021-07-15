from django import forms
from Store.models.product import ProductReview


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ('product', 'user', 'content', 'stars', 'date_added')
