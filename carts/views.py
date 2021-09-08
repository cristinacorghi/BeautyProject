from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from Store.models.productModel import Product
from .forms import CustomerPaymentForm
from .models import *


def cart_view(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None

    if the_id is None:
        empty_message = "Your cart is empty, please keep shopping"
        context = {"empty": True, 'empty_message': empty_message}

    else:
        new_total = 0.00  # prezzo totale
        for item in cart.cartitem_set.all():
            line_total = float(item.product.price) * item.quantity
            new_total += line_total

        request.session['items_total'] = cart.cartitem_set.count()
        cart.total = new_total
        cart.save()
        context = {"cart": cart}

    template = "cart.html"
    return render(request, template, context)


def add_to_cart(request, pk):
    # Imposta l'ora di scadenza per la sessione. In questo caso, la sessione scade dopo 120000 secondi di
    # inattività.
    request.session.set_expiry(120000)
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id

    cart = Cart.objects.get(id=the_id)

    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        pass
    except:
        pass

    if request.method == 'POST':
        qty = request.POST['qty']
        for item in request.POST:
            key = item
            val = request.POST[key]

        # ("model object", "true/false")
        cart_item = CartItem.objects.create(cart=cart, product=product)

        cart_item.quantity = qty
        cart_item.save()

        # request.session['item'] = cart_item.id

        return HttpResponseRedirect(reverse("carts:cart_view"))

    return HttpResponseRedirect(reverse("carts:cart_view"))


def remove_from_cart(request, id):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
        return HttpResponseRedirect(reverse("carts:cart_view"))

    cartitem = CartItem.objects.get(id=id)
    cartitem.delete()
    return HttpResponseRedirect(reverse("carts:cart_view"))


def customer_payment(request):
    if request.method == 'POST':
        form = CustomerPaymentForm(request.POST)

        if not form.is_valid():
            return render(request, 'payment.html', {'form': form})

        else:
            form.save()
            cartitem = CartItem.objects.all()
            cartitem.delete()
            request.session['items_total'] = 0
            template = "success_payment.html"
            context = {"empty": True, 'form': form, 'cartitem': cartitem}
            return render(request, template, context)

    form = CustomerPaymentForm()
    return render(request, 'payment.html', {'form': form})


def success_payment(request):
    return render(request, 'success_payment.html')
