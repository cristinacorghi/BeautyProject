from django.shortcuts import render
from .models import *


def cart_view(request):
    cart = Cart.objects.all()[0]
    context = {"cart": cart}
    template = "cart.html"
    return render(request, template, context)
