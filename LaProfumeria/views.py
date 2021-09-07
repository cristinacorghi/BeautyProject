from forms.registerForm import UserForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from forms.loginForm import UserLoginForm
from forms.reviewForm import ReviewForm
from django.contrib.auth.models import User
from Store.models.productModel import Product, ProductReview
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Min, Max
from django.http import JsonResponse
from django.template import RequestContext

from django.contrib import messages  # import messages to show flash message in your page
from forms.profileForm import ProfileForm, \
    form_validation_error  # import the used form and related function to show errors
from Store.models.profileModel import Profile  # import the Profile Model
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# homepage
def Base(request):
    lista_profumi = Product.objects.all()
    recensioni = ProductReview.objects.all()
    profumi_estrapolati = []
    while len(profumi_estrapolati) < 5:
        profumi_estrapolati.append(lista_profumi[num])
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


# sign in
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Base')
    else:
        form = UserForm()

    return render(request, 'register.html', {'form': form})


@method_decorator(login_required(login_url='login'), name='dispatch')
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
            profile.user.save()

            messages.success(request, 'Profile saved successfully')
        else:
            messages.error(request, form_validation_error(form))
        return redirect('profile')


# logout
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


# search bar
def SearchBar(request):
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


# view dei prodotti
class ProductList(DetailView):
    model = Product
    template_name = 'products.html'


# view dei brand
class BrandList(ListView):
    model = Product
    template_name = 'brand.html'


# price
def price(request):
    minMaxPrice = Product.objects.aggregate(Min('price'), Max('price'))
    # {'price__min': 49, 'price__max': 124}
    allProducts = Product.objects.all().order_by('-id').distinct()
    allProducts = allProducts.filter(price__gte=minMaxPrice['price__min'])
    allProducts = allProducts.filter(price__lte=minMaxPrice['price__max'])
    data = {'minMaxPrice': minMaxPrice, 'allProducts': allProducts}
    return render(request, 'price.html', data)


# prezzi filtrati
def filter_price(request):
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    filtered_products = Product.objects.filter(price__gte=minPrice).filter(price__lte=maxPrice).distinct()
    t = render_to_string('ajax/filtered_products_price.html', {'data': filtered_products})
    return JsonResponse({'data': t})


# men's perfumes
class MenPerfumes(ListView):
    model = Product
    template_name = 'men_perfumes.html'


# women's perfumes
class WomenPerfumes(ListView):
    model = Product
    template_name = 'women_perfumes.html'


def recommended_products_view(request):
    model = ProductReview
    template_name = 'recommended_products.html'
    # products = ProductReview.objects.all()
    # star_list = []
    # for item in products:
    # for item.stars in products:
    # total = 0
    # total = (total+item.stars)/2
    # star_list.append(total)
    #  total_score = total_score + item.stars
    #  dict_total_score = [].append(total_score)
    queryset = ProductReview.objects.order_by('-stars')[:5]
    context = {'queryset': queryset}
    return render(request, template_name, context)
