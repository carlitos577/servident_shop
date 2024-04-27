from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from .models import Usuario
from venta_productos.models import Product
from venta_productos.models import ProductPhoto
import os
from django.conf import settings


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Realizar una consulta a la base de datos para verificar las credenciales
        try:
            user = Usuario.objects.get(username=username, password=password)
        except Usuario.DoesNotExist:
            user = None
        
        if user is not None:
            # Autenticar al usuario manualmente
            request.session['user_id'] = user.id
            return redirect('dashboard')
        else:
            # Si las credenciales no son válidas, puedes mostrar un mensaje de error
            error_message = "Credenciales inválidas. Por favor, inténtelo de nuevo."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def user_logout(request):
    logout(request)
    return redirect('login')

#-------------------------CRUD Usuarios-------------------------
def usuario_create(request):
    if request.method == 'POST':
        # Procesar el formulario de creación si se ha enviado
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        profile_picture = request.FILES.get('profile_picture')
        
        # Crear un nuevo objeto Usuario
        usuario = Usuario(
            full_name=full_name,
            username=username,
            password=password,
            phone_number=phone_number,
            profile_picture=profile_picture
        )

        # Verificar si se proporciona una nueva imagen
        if 'profile_picture' in request.FILES:
            # Eliminar la imagen anterior si existe
            if usuario.profile_picture:
                usuario.profile_picture = None
            # Guardar la nueva imagen
            profile_picture = request.FILES['profile_picture']
            usuario.profile_picture = profile_picture.read() if profile_picture else None
        usuario.save()
        # Redirigir a alguna página después de crear el usuario (por ejemplo, al dashboard)
        return redirect('usuarios_list')
    else:
        # Mostrar el formulario de creación si la solicitud es GET
        return render(request, 'Usuarios/usuario_create.html')

def usuario_edit(request, usuario_id):
    # Obtener el usuario a editar
    usuario = Usuario.objects.get(pk=usuario_id)
    if request.method == 'POST':
        # Procesar el formulario de edición si se ha enviado
        usuario.full_name = request.POST.get('full_name')
        usuario.username = request.POST.get('username')
        usuario.password = request.POST.get('password')
        usuario.phone_number = request.POST.get('phone_number')
        # Verificar si se proporciona una nueva imagen
        if 'profile_picture' in request.FILES:
            # Eliminar la imagen anterior si existe
            if usuario.profile_picture:
                usuario.profile_picture = None
            # Guardar la nueva imagen
            profile_picture = request.FILES['profile_picture']
            usuario.profile_picture = profile_picture.read() if profile_picture else None
        usuario.save()
        return redirect('usuarios_list')
    else:
        # Mostrar el formulario de edición con los datos actuales del usuario
        return render(request, 'Usuarios/usuario_edit.html', {'usuario': usuario})

def usuario_delete(request, usuario_id):
    # Obtener el usuario a eliminar
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    # Eliminar el usuario de la base de datos
    usuario.delete()
    return redirect('usuarios_list')

def usuarios_list(request):
    # Obtener todos los objetos Usuario de la base de datos
    usuarios = Usuario.objects.all()
    # Pasar los usuarios a la plantilla para renderizar la tabla
    return render(request, 'Usuarios/usuarios_list.html', {'usuarios': usuarios})

#-------------------------CRUD Productos-------------------------
def producto_create(request):
    if request.method == 'POST':
        # Procesar el formulario de creación si se ha enviado
        title = request.POST.get('title')
        price = request.POST.get('price')
        
        # Crear un nuevo objeto Product
        product = Product(title=title, price=price)
        product.save()
        # Redirigir a alguna página después de crear el producto
        return redirect('producto_list')
    else:
        # Mostrar el formulario de creación si la solicitud es GET
        return render(request, 'Productos/producto_create.html')

def producto_edit(request, producto_id):
    # Obtener el producto a editar
    producto = Product.objects.get(pk=producto_id)

    if request.method == 'POST':
        # Procesar el formulario de edición si se ha enviado
        producto.title = request.POST.get('title')
        producto.price = request.POST.get('price')

        producto.save()
        return redirect('producto_list')
    else:
        # Mostrar el formulario de edición con los datos actuales del producto
        return render(request, 'Productos/producto_edit.html', {'producto': producto})

def producto_delete(request, producto_id):
    # Obtener el producto a eliminar
    producto = get_object_or_404(Product, pk=producto_id)

    # Eliminar las fotos asociadas al producto
    product_photos = ProductPhoto.objects.filter(product=producto)
    for photo in product_photos:
        # Eliminar la foto de la carpeta de medios
        if photo.photo_url:
            photo_path = os.path.join(settings.MEDIA_ROOT, str(photo.photo_url))
            if os.path.exists(photo_path):
                os.remove(photo_path)
        # Eliminar la instancia de ProductPhoto de la base de datos
        photo.delete()

    # Eliminar el producto de la base de datos
    producto.delete()

    return redirect('producto_list')

def producto_list(request):
    productos = Product.objects.all()
    return render(request, 'Productos/producto_list.html', {'productos': productos})
#-------------------------CRUD Productos Fotos-------------------------
def productphoto_create(request, product_id):
    # Obtener el producto asociado al product_id
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        # Procesar el formulario de creación si se ha enviado
        photo_url = request.FILES.get('photo_url')
        # Crear un nuevo objeto ProductPhoto
        product_photo = ProductPhoto(product=product, photo_url=photo_url)
        # Verificar si se proporciona una nueva imagen
        if 'photo_url' in request.FILES:
            # Eliminar la imagen anterior si existe
            if product_photo.photo_url:
                product_photo.photo_url = None
            # Guardar la nueva imagen
            photo_url = request.FILES['photo_url']
            product_photo.photo_url = photo_url.read() if photo_url else None
        product_photo.save()
        # Redirigir a alguna página después de crear la foto de producto
        return redirect('producto_list')
    else:
        # Mostrar el formulario de creación si la solicitud es GET
        return render(request, 'Productos/productphoto_create.html', {'product': product})   

def productphoto_edit(request, productphoto_id):
    # Obtener la foto de producto a editar
    productphoto = get_object_or_404(ProductPhoto, pk=productphoto_id)
    
    if request.method == 'POST':
        # Procesar el formulario de edición si se ha enviado
        photo_url = request.FILES.get('photo_url')
        
        if 'photo_url' in request.FILES:
            # Eliminar la imagen anterior si existe
            if productphoto.photo_url:
                productphoto.photo_url = None
            # Guardar la nueva imagen
            photo_url = request.FILES['photo_url']
            productphoto.photo_url = photo_url.read() if photo_url else None
        
        productphoto.save()
        return redirect('producto_list')
    else:
        # Mostrar el formulario de edición con los datos actuales de la foto de producto
        return render(request, 'Productos/productphoto_edit.html', {'productphoto': productphoto})

def productphoto_delete(request, productphoto_id):
    # Obtener la foto de producto a eliminar
    productphoto = get_object_or_404(ProductPhoto, pk=productphoto_id)
    
    # Eliminar la foto de producto de la base de datos
    productphoto.delete()

    return redirect('producto_list')
    
