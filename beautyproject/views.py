from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView
from forms.loginForm import UserLoginForm
from forms.profileForm import ProfileForm
from django.contrib.auth.models import User
from Store.models.product import Product
from django.views import generic


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
    form = ProfileForm(request.POST or None)
    title = 'profilo'

    if form.is_valid():
        fullName = form.cleaned_data.get('fullName')
        email = form.cleaned_data.get('email')
        mobilePhone = form.cleaned_data.get('mobilePhone')
        address = form.cleaned_data.get('address')
        '''
        in questo modo estraggo univocamente l'utente
        
        ----> DA FARE:
        - estrapolare attuale utente loggato, prenderne l'ID e estrarre tutti i suoi dati salvati nel db
        filtrando l'oggetto user (qua sotto).
        user = User.objects.filter(id="(id attuale loggato)")
        '''

        user = User.objects.filter(username="cristina")

        '''in questo modo ho elencato tutti i campi dell'oggetto user'''
        print(user.values_list())
        '''a questo punto andare a modificare i campi estratti e memorizzare l'oggetto modificato nel db
        sovrascrivendo quello vecchio (vedere su internet)'''

    else:
        print("sono il GET")
    return render(request, 'profile.html', {'form': form, 'title': title})


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


class Products(generic.ListView):
    model = Product
    template_name = 'products.html'

    def get(self, request, id):
        id = request.GET.get('id', '')
    obj = Product.objects.filter(id)
