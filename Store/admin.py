from django.contrib import admin
from .models.productModel import Product, ProductReview
from .models.categoryModel import Category
from .models.userModel import Profile


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
admin.site.register(ProductReview)
admin.site.register(Profile)
