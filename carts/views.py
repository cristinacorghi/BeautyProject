from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from Store.models.productModel import Product
from .forms import CustomerPaymentForm
from .models import *
from Store.models.productModel import CustomerOrders


def cart_view(request):
    try:
        the_id = request.session['cart_id']  # prende l'id del profumo
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None

    if the_id is None:
        empty_message = "Your cart is empty, please keep shopping"
        context = {"empty": True, 'empty_message': empty_message}

    else:
        new_total = 0.00  # prezzo totale
        for item in cart.cartitem_set.all():
            line_total = float(item.product.price) * item.quantity  # prezzo * quantità
            new_total += line_total

        request.session['items_total'] = cart.cartitem_set.count()
        cart.total = new_total  # prezzo totale
        cart.save()
        context = {"cart": cart}

    template = "cart.html"
    return render(request, template, context)


def add_to_cart(request, pk):
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
        qty = request.POST['qty']  # quantità aggiunta al carello del singolo profumo
        for item in request.POST:
            key = item
            val = request.POST[key]

        if product.quantity >= int(qty):
            qty_rimasta = product.quantity - int(qty)
            cart_item = CartItem.objects.create(cart=cart, product=product)
            cart_item.quantity = int(qty)
            cart_item.save()
        else:
            quantità = product.quantity
            name = product.name
            context = {'quantità': quantità, 'name': name}
            return render(request, 'finished_perfumes.html', context)

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
        form = CustomerPaymentForm(request.POST, instance=request.user)
        if not form.is_valid():
            return render(request, 'payment.html', {'form': form})
        else:
            form.save()
            product = Product.objects.all()
            cartitem = CartItem.objects.all()
            prodotto = CartItem.objects.get(product_id__in=product)
            agg = Product.objects.get(id=prodotto.product_id)

            for item in cartitem:
                orderdetail = CustomerOrders(user=request.user, product=item.product)
                orderdetail.save()
                qty_rimasta = agg.quantity - item.quantity
                agg = Product.objects.filter(id=item.product_id).update(quantity=qty_rimasta)

            cartitem.delete()  # quando procedo al pagamento il carrello torna vuoto
            request.session['items_total'] = 0
            template = "success_payment.html"
            context = {"empty": True, 'form': form, 'cartitem': cartitem}

            return render(request, template, context)

    form = CustomerPaymentForm()
    return render(request, 'payment.html', {'form': form})


def success_payment(request):
    return render(request, 'success_payment.html')
