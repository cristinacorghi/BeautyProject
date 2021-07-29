from django.contrib.auth.forms import UserCreationForm
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
from forms.profileForm import EditProfileForm
from django.contrib.auth.models import User
from Store.models.productModel import Product, ProductReview
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Min, Max
from django.http import JsonResponse
from django.template import RequestContext


# homepage
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


# sign in
class UserCreationView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('Base')


# profile
def Profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('Base')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'profile.html', args)


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


# cart
def update_cart(request, slug):
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
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        pass
    except:
        pass

    # ("model object", "true/false")
    cart_item, created = CartItem.objects.get_or_create(product=product)
    if created:
        print("yeah")

    if not cart_item in cart.items.all():
        cart.items.add(cart_item)
    else:
        cart.items.remove(cart_item)

    new_total = 0.00
    for item in cart.items.all():
        line_total = float(item.product.price) * item.quantity
        new_total += line_total

    request.session['items_total'] = cart.items.count()
    cart.total = new_total
    cart.save()

    return HttpResponseRedirect(reverse("cart"))
