from django.contrib import admin
from .models.productModel import *
from .models.categoryModel import Category
from .models.profileModel import Profile


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
admin.site.register(ProductReviewModel)
admin.site.register(Profile)
admin.site.register(CustomerOrders)
admin.site.register(WaitingListModel)
