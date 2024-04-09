"""
URL configuration for bodegaCentralMP project.

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
from django.urls import path

from .views import *

urlpatterns = [
    path('', root),
    path('bodega/login/', login_view, name="login"),
    path('bodega/404/', error404, name="error404"),
    path('bodega/', index, name="index"),
    path('bodega/saludo/', saludo, name="saludo"),
    path('bodega/productos/', productos_list, name="productos_list"),
    path('bodega/productos/new', productos_new, name="productos_new"),
    path('bodega/productos/<int:codigo>/edit', productos_edit, name="productos_edit"),
    path('bodega/productos/<int:codigo>/delete', productos_delete, name="productos_delete"),
    path('bodega/pedidos/', pedidos_list, name="pedidos_list"),
    path('bodega/pedidos/<int:id_pedido>', pedidos_detalle, name="pedidos_detalle"),
    path('bodega/pedidos/new', pedidos_new, name="pedidos_new"),
    path('bodega/pedidos/<int:id_pedido>/edit', pedidos_edit, name="pedidos_edit"),
    path('bodega/pedidos/<int:id_pedido>/delete', pedidos_delete, name="pedidos_delete"),
    path('bodega/pedidos/<int:id_pedido>/solicitud/<int:transporte>', solicitud_transporte, name="solicitud_transporte"),
    path('bodega/pedidos/<int:id_pedido>/actualizar', actualizar_estado, name="actualizar_estado"),
    path('bodega/sucursales/', sucursal_list, name="sucursal_list"),
    path('bodega/sucursales/new', sucursal_new, name="sucursal_new"),
    path('bodega/sucursales/<int:id_sucursal>/edit', sucursal_edit, name="sucursal_edit"),
    path('bodega/sucursales/<int:id_sucursal>/delete', sucursal_delete, name="sucursal_delete"),
    path('bodega/admin', admin_view, name="admin_view"),
    # path('bodega/productos/faker1000', productos_faker_1000, name="productos_faker_1000"),
    # path('bodega/productos/faker10000', productos_faker_10000, name="productos_faker_10000"),
    # path('bodega/productos/faker100000', productos_faker_100000, name="productos_faker_100000"),
    # path('bodega/productos/fakerdelete', productos_faker_delete, name="productos_faker_delete"),
]
