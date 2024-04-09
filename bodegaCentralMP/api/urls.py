from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('', root),
    path('v1/productos/', producto_list),
    path('v1/productos/<int:codigo>', producto_detail),
    path('v1/pedidos/', pedido_list),
    path('v1/pedidos/<int:id_pedido>/', pedido_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)