from django.contrib import admin

# Register your models here.
    
from django.contrib import admin
from .models import Product, ProductPhoto

admin.site.register(Product)
admin.site.register(ProductPhoto)
