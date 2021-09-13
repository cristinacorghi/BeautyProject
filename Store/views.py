from forms.registerForm import UserForm
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.views.generic import DetailView, ListView
from forms.loginForm import UserLoginForm
from forms.reviewForm import ReviewForm
from django.contrib.auth.models import User
from Store.models.productModel import Product, ProductReview, CustomerOrders
from django.db.models import Min, Max
from django.http import JsonResponse
from django.contrib import messages  # import messages to show flash message
from forms.profileForm import ProfileForm, \
    form_validation_error  # import the used form and related function to show errors
from Store.models.profileModel import Profile
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import math


def Base(request):
    return render(request, 'homepage.html')


# log in
def login_view(request):
    next = request.GET.get('next')
    title = 'Login'
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    return render(request, 'login.html', {'form': form, 'title': title})


# sign up
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Base')
    else:
        form = UserForm()

    return render(request, 'register.html', {'form': form})


@method_decorator(login_required(login_url='login'),
                  name='dispatch')  # login_required controlla che l'utente corrente sia loggato.
                                    # dispatch() → metodo presente in tutte le class-based view che si occupa di
                                    # gestire le request e le response.
class ProfileView(View):
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'profile': self.profile}
        return render(request, 'profile.html', context)

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=self.profile)

        if form.is_valid():
            profile = form.save()
            # to save user model info
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.last_name = form.cleaned_data.get('last_name')
            profile.user.email = form.cleaned_data.get('email')
            profile.phone = form.cleaned_data.get('phone')
            profile.user.save()

            messages.success(request, 'Profile saved successfully')
        else:
            messages.error(request, form_validation_error(form))
        return redirect('Store:profile')


# logout
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


# search bar
def search_bar(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Product.objects.filter(name__contains=searched)
        return render(request, 'search_bar.html', {'searched': searched, 'venues': venues})
    else:
        return render(request, 'search_bar.html')


# reviews
def product_review(request, id):
    if request.method == 'POST' and request.user.is_authenticated:
        stars = request.POST.get('stars', 3)
        content = request.POST.get('content', '')
        product = Product.objects.get(id=id)
        review = ProductReview.objects.create(product=product, user=request.user, stars=stars,
                                              content=content)
        return render(request, 'review_added.html')
    else:
        return render(request, 'review_added.html')


# class-based view dei prodotti
class ProductList(DetailView):
    model = Product
    template_name = 'products.html'


# price
def price(request):
    minMaxPrice = Product.objects.aggregate(Min('price'),
                                            Max('price'))  # dizionario che contiene il prezzo minimo e massimo tra tutti i profumi
    allProducts = Product.objects.all().order_by('-id').distinct()  # tutti i profumi ordinati per id decrescente
    allProducts = allProducts.filter(price__gte=minMaxPrice['price__min'])
    allProducts = allProducts.filter(price__lte=minMaxPrice['price__max'])
    data = {'minMaxPrice': minMaxPrice, 'allProducts': allProducts}
    return render(request, 'price.html', data)


# prezzi filtrati
def filter_price(request):
    minPrice = request.GET['minPrice']  # prezzo minimo
    maxPrice = request.GET['maxPrice']  # prezzo massimo impostato da interfaccia
    filtered_products = Product.objects.filter(price__gte=minPrice).filter(
        price__lte=maxPrice).distinct()  # tutti i profumi dal prezzo minimo al prezzo massimo
    t = render_to_string('ajax/filtered_products_price.html',
                         {'data': filtered_products})  # pagina html di ogni profumo filtrato
    return JsonResponse({'data': t})


# class-based view dei profumi da uomo
class MenPerfumes(ListView):
    model = Product
    template_name = 'men_perfumes.html'


# class-based view dei profumi da donna
class WomenPerfumes(ListView):
    model = Product
    template_name = 'women_perfumes.html'


def recommended_products_anonymous_helper(obj):
    queryset = ProductReview.objects.all()
    products = {}
    for product in obj:  # per ogni profumo in "profumi_finali"
        stars_splitting = {}
        count = 0  # serve per contare il numero di recensioni presenti in un profumo
        for recensione in queryset:  # per ogni recensione
            if recensione.product == product:  # se il profumo in queryset è uguale al profumo in "profumi_finali"
                if product not in products.keys():  # se il profumo in "profumi_finali" non è nel dizionario "products"
                    products[product] = recensione.stars  # il dizionario "products" con chiave "product" prende come valore il numero di stelle della singola recensione
                else:
                    products[product] = products[product] + recensione.stars  # aggiungo il valore dell'altra recensione
                count += 1
        if count != 0:
            average_stars = float(products[product]) / count  # calcolo la media totale delle recensioni per quel profumo
            frazione, intero = math.modf(average_stars)  # separo la parte frazionaria dall'intero
            stars_splitting['intero'] = intero
            stars_splitting['frazione'] = frazione
            products[product] = stars_splitting  # ora "products" avrà come chiave il profumo e come valore "stars_splitting" (es: {'intero': 4.0, 'frazione': 0.0})
            if intero < 3:  # elimino tutti i profumi < 3 stelle
                del products[product]

    return products


def recommended_products_view(request):

    if request.user.is_authenticated:
        customer_orders = CustomerOrders.objects.filter(user=request.user)
        if customer_orders:  # se l'utente ha effettuato un ordine
            profumi_con_ripetizione = []
            profumi_finali = []
            for order in customer_orders:  # per tutti gli ordini che l'utente ha effettuato
                brand = order.product.brand  # prendo il brand
                prezzo = order.product.price  # prendo il prezzo
                # queryset filtra tutti i profumi presenti nel database per brand=brand degli ordini, e prezzo compreso tra -50 e + 50 rispetto al prezzo totale dell'ordine
                queryset = Product.objects.filter(brand=brand, price__lte=prezzo+50, price__gte=prezzo-50)
                profumi_con_ripetizione.append(queryset)  # lista che contiene tutti i profumi filtrati in base al profumo acquistato

            # questo ciclo innestato permette che per ogni lista di prodotti consigliati per ogni profumo acquistato,
            # aggiunge a "profumi_finali" tutti i profumi di "profumi_con_ripetizione" tranne quelli che si ripetono
            for perfume in profumi_con_ripetizione:
                for x in perfume:
                    if x not in profumi_finali:
                        profumi_finali.append(x)

            context = {'products': recommended_products_anonymous_helper(profumi_finali)}

            return render(request, 'recommended_products.html', context)
        else:  # se l'utente non ha effettuato alcun ordine, allora viene mostrata una lista di profumi con le recensioni più alte
            context = {'products': recommended_products_anonymous_helper(Product.objects.all())}
    else:
        context = {'products': recommended_products_anonymous_helper(Product.objects.all())}
    template_name = 'recommended_products.html'
    return render(request, template_name, context)
