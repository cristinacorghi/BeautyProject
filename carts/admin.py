from django.contrib import admin
from .models import *


class CartAdmin(admin.ModelAdmin):
    class Meta:
        model = Cart


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(CustomerPayment)
