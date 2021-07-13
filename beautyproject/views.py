from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from forms.loginForm import UserLoginForm
from forms.profileForm import EditProfileForm
from django.contrib.auth.models import User
from Store.models.product import Product
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Min, Max


def Base(request):
    return render(request, 'homepage.html')


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


class UserCreationView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('Base')


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


def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


def SearchBar(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Product.objects.filter(name__contains=searched)
        return render(request, 'search_bar.html', {'searched': searched, 'venues': venues})
    else:
        return render(request, 'search_bar.html')


class ProductList(DetailView):
    model = Product
    template_name = 'products.html'


class BrandList(ListView):
    model = Product
    template_name = 'brand.html'


def price(request):
    minMaxPrice = Product.objects.aggregate(Min('price'), Max('price'))
    data = {'minMaxPrice': minMaxPrice}
    return render(request, 'price.html', data)


class MenPerfumes(ListView):
    model = Product
    template_name = 'men_perfumes.html'
