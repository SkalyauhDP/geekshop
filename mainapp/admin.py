from django.contrib import admin

# Register your models here.
from mainapp.models import ProductCategory, Product
from mainapp.views import products

admin.site.register(ProductCategory)
admin.site.register(Product)



