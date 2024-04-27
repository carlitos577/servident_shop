from django.shortcuts import render, get_object_or_404
from django.db import models
from .models import Product, ProductPhoto
# Create your views here.

def index(request):
    # Obtener todos los productos con su primera imagen
    productos_con_imagen = []
    productos = Product.objects.all()
    for producto in productos:
        primera_imagen = producto.productphoto_set.first()
        productos_con_imagen.append({'producto': producto, 'imagen': primera_imagen})

    context = {'productos_con_imagen': productos_con_imagen}
    return render(request, 'index.html', context)

def detalle_producto(request, producto_id):
    # Obtener el producto desde la base de datos
    producto = get_object_or_404(Product, pk=producto_id)
    
    # Obtener todas las fotos relacionadas al producto
    fotos_producto = ProductPhoto.objects.filter(product=producto)
    
    # Renderizar la plantilla de detalle_producto.html con el producto y las fotos
    return render(request, 'detalle_producto.html', {'producto': producto, 'fotos_producto': fotos_producto})






def HelloWord(request):
    return render(request, 'HelloWord.html')
