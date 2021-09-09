from django.db import models
from django.urls import reverse
from Store.models.productModel import Product
from django.contrib.auth.models import User


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    # line_total: prezzo totale = prezzo profumo * quantità
    line_total = models.DecimalField(default=1.0, max_digits=1000, decimal_places=2)

    class Meta:
        verbose_name_plural = 'CartItem'

    def __unicode__(self):
        try:
            return str(self.cart.id)
        except:
            return self.product.name


class Cart(models.Model):
    # prezzo totale
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)

    class Meta:
        verbose_name_plural = 'Cart'

    def __unicode__(self):
        return "Cart id: %s" % self.id


class CustomerPayment(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.IntegerField()
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'CustomerPayment'
