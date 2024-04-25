"""
URL configuration for AppWebServiDent project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gestion_usuarios import views as usuarios_views
from venta_productos import views as productos_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', productos_views.index, name='index'),
    path('HelloWord/', productos_views.HelloWord),
    path('login/', usuarios_views.user_login, name='login'),
    path('dashboard/', usuarios_views.dashboard, name='dashboard'),
    path('logout/', usuarios_views.user_logout, name='logout'),
    #-------------------------CRUD Usuarios-------------------------
    path('dashboard/usuarios/create/', usuarios_views.usuario_create, name='usuario_create'),
    path('dashboard/usuarios/<int:usuario_id>/edit/', usuarios_views.usuario_edit, name='usuario_edit'),
    path('dashboard/usuarios/<int:usuario_id>/delete/', usuarios_views.usuario_delete, name='usuario_delete'),
    path('dashboard/usuarios/', usuarios_views.usuarios_list, name='usuarios_list'),
    #-------------------------CRUD Productos-------------------------
    path('dashboard/productos/create/', usuarios_views.producto_create, name='producto_create'),
    path('dashboard/producto/<int:producto_id>/edit/', usuarios_views.producto_edit, name='producto_edit'),
    path('producto/<int:producto_id>/delete/', usuarios_views.producto_delete, name='producto_delete'),

    path('producto/<int:producto_id>/', productos_views.detalle_producto, name='detalle_producto'),

    #-------------------------CRUD Productos Fotos-------------------------
    path('dashboard/productos/<int:product_id>/photos/create/', usuarios_views.productphoto_create, name='productphoto_create'),
    path('dashboard/productos/<int:productphoto_id>/edit/', usuarios_views.productphoto_edit, name='productphoto_edit'),
    path('dashboard/productos/<int:productphoto_id>/delete/', usuarios_views.productphoto_delete, name='productphoto_delete'),
    path('dashboard/productos/', usuarios_views.producto_list, name='producto_list'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
