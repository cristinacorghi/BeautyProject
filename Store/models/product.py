from django.db import models
from .category import Category


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=500, default='')
    image = models.ImageField(upload_to='static/img/products')

    @staticmethod
    def get_all_products():
        return Product.objects.all()
