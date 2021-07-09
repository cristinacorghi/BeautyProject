from django.shortcuts import render
from .models.product import Product


def index(request):
    prds = Product.get_all_products()
    return render(request, 'base.html', {'products': prds})