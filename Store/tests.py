from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from .views import *


class TestUrls(SimpleTestCase):

    def test_base_url_is_resolved(self):
        url = reverse('Store:Base')
        self.assertEqual(resolve(url).func, Base)

    def test_login_url_is_resolved(self):
        url = reverse('Store:Accedi')
        self.assertEqual(resolve(url).func, login_view)

    def test_register_url_is_resolved(self):
        url = reverse('Store:Registration')
        self.assertEqual(resolve(url).func, register)

    def test_logout_is_resolves(self):
        url = reverse('Store:Logout')
        self.assertEqual(resolve(url).func, logout_view)

    def test_search_url_is_resolves(self):
        url = reverse('Store:SearchBar')
        self.assertEqual(resolve(url).func, search_bar)

    def test_product_review_url_is_resolves(self):
        url = reverse('Store:ProductReview', args=[1])
        self.assertEqual(resolve(url).func, product_review)

    def test_price_url_is_resolves(self):
        url = reverse('Store:price')
        self.assertEqual(resolve(url).func, price)

    def test_filter_price_is_resolves(self):
        url = reverse('Store:filter-price')
        self.assertEqual(resolve(url).func, filter_price)

    def test_recommended_products_url_is_resolves(self):
        url = reverse('Store:recommended-products')
        self.assertEqual(resolve(url).func, recommended_products_view)

