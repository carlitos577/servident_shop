from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio en Bolivianos (Bs)

    def __str__(self):
        return self.title

class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    photo_url = models.ImageField(upload_to='producto_pictures/', null=True, blank=True)

    def __str__(self):
        return f"Photo of {self.product.title}"
# Create your models here.
