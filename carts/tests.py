from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from .models import *
from .views import *


# uso SimpleTestCase per verificare l'uguaglianza di due url
class TestUrls(SimpleTestCase):

    def test_cart_view_url_is_resolved(self):
        url = reverse('carts:cart_view')
        self.assertEqual(resolve(url).func, cart_view)

    def test_add_to_cart_url_is_resolved(self):
        url = reverse('carts:AddToCart', args=[1])
        self.assertEqual(resolve(url).func, add_to_cart)

    def test_remove_from_cart_url_is_resolved(self):
        url = reverse('carts:remove_from_cart', args=[1])
        self.assertEqual(resolve(url).func, remove_from_cart)

    def test_customer_payment_url_is_resolves(self):
        url = reverse('carts:customer-payment')
        self.assertEqual(resolve(url).func, customer_payment)

    def test_success_payment_url_is_resolves(self):
        url = reverse('carts:success_payment')
        self.assertEqual(resolve(url).func, success_payment)

    def test_send_mail_url_is_resolves(self):
        url = reverse('carts:send-email', args=[1])
        self.assertEqual(resolve(url).func, send_email)


class TestModelsCarts(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='user')
        self.cart_item = CartItem.objects.create(
            quantity=5,
            line_total=50.0
        )

        self.cart = Cart.objects.create(
            total=self.cart_item.line_total
        )

    def test_aggiunta_prodotto(self):
        self.assertEqual(self.cart.total, 50.0)
