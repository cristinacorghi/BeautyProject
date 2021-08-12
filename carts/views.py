from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from Store.models.productModel import Product
from forms.paymentForm import PaymentForm
from .models import *


def cart_view(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
    if the_id:
        new_total = 0.00
        for item in cart.cartitem_set.all():
            line_total = float(item.product.price) * item.quantity
            new_total += line_total

        request.session['items_total'] = cart.cartitem_set.count()
        cart.total = new_total
        cart.save()
        context = {"cart": cart}
    else:
        empty_message = "Your cart is empty, please keep shopping"
        context = {"empty": True, 'empty_message': empty_message}
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

        return HttpResponseRedirect(reverse("cart_view"))

    return HttpResponseRedirect(reverse("cart_view"))


def remove_from_cart(request, id):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        return HttpResponseRedirect(reverse("cart_view"))

    cartitem = CartItem.objects.get(id=id)
    cartitem.delete()
    # cartitem.cart = None
    # cartitem.save()
    return HttpResponseRedirect(reverse("cart_view"))


def payment_view(request):
    form = PaymentForm(request.POST or None)
    if form.is_valid():
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        phone_number = form.cleaned_data.get('phone_number')
        address = form.cleaned_data.get('address')
        city = form.cleaned_data.get('city')
    '''if request.method == 'POST' and request.user.is_authenticated:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        city = request.POST.get('city')
        payment = Payment.objects.create(user=request.user, first_name=first_name, last_name=last_name,
                                         email=email, phone_number=phone_number, address=address, city=city)
        context = {'payment': payment}'''
    return render(request, 'cart.html', {'form': form})


def success_payment(request):
    return render(request, 'success_payment.html')
