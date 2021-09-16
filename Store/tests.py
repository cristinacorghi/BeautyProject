from django.test import TestCase, SimpleTestCase
from django.test.client import Client
from django.urls import reverse, resolve
from .views import *
from .models.productModel import Product, ProductReviewModel


# uso SimpleTestCase per verificare l'uguaglianza di due url
class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
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


# Il client di test è una classe Python che funge da browser Web fittizio, consentendo di testare le visualizzazioni
# e interagire con l'applicazione basata su Django a livello di programmazione.
class StoreViewsTestCase(TestCase):

    def setUp(self):
        self.clientLogged = Client()
        self.clientUnlogged = Client()
        self.usrLogin = User.objects.create(username='user', password='user')
        self.clientLogged.login(username=self.usrLogin.username, password=self.usrLogin.password)
        self.url_risultati_ricerca = reverse('Store:SearchBar')
        self.url_registrazione = reverse('Store:Registration')
        self.url_recensioni = reverse('Store:ProductReview', args=[1])

    def test_risultati_ricerca(self):
        response = self.clientLogged.get(self.url_risultati_ricerca)  # invia una richiesta GET
        self.assertEqual(response.status_code, 200)  # Verifica che la risposta sia 200 OK.

    def test_registrazione(self):
        resp = self.clientUnlogged.get(self.url_registrazione)
        self.assertEqual(resp.status_code, 200)

    def test_recensioni(self):
        respAnonimo = self.clientUnlogged.get(self.url_recensioni)
        self.assertEqual(respAnonimo.status_code, 200)

        respLogged = self.clientLogged.get(self.url_recensioni)
        self.assertEqual(respLogged.status_code, 200)


class TestUser(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@test.test', password='12test34')

    def test_username(self):
        self.assertEqual(self.user.username, 'testuser')

    def test_email(self):
        self.assertEqual(self.user.email, 'testuser@test.test')


class TestModelsStore(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='user')
        self.prodotto = Product.objects.create(
            name='Montale',
            price=150,
            brand='Montale',
            description='test',
            quantity=10
        )

        self.recensione = ProductReviewModel.objects.create(
            product=self.prodotto,
            user=self.user,
            content='Very good',
            stars=5
        )

    def test_aggiunta_recensione(self):
        self.assertEqual(self.recensione.product.name, 'Montale')
