from django.urls import path
from . import views
from .views import *

app_name = 'carts'

urlpatterns = [
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/success_payment/', views.success_payment, name='success_payment'),
    path('cart/<int:pk>/', views.add_to_cart, name='AddToCart'),
    path('cart/(<int:id>)/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/payment/', views.customer_payment, name='customer-payment'),
]
