from django.contrib import admin
from .models import *
    
class ProductoAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        """
        Verifica si el usuario no es superusuario.
        """
        return  not request.user.is_superuser or request.user.is_superuser

    def has_add_permission(self, request):
        """
        Permite agregar nuevos registros a la tabla "productos" para los usuarios que no son superusuarios.
        """
        return  not request.user.is_superuser or request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        """
        Permite modificar registros existentes en la tabla "productos" para los usuarios que no son superusuarios.
        """
        return  not request.user.is_superuser or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """
        Permite eliminar registros de la tabla "productos" para los usuarios que no son superusuarios.
        """
        return  not request.user.is_superuser or request.user.is_superuser
 
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Pedido)
admin.site.register(Sucursal)