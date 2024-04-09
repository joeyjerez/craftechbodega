from rest_framework import serializers
from bodega.models import *

class ProductoSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class DetallePedidoSerializer(serializers.ModelSerializer):
    codigo = serializers.ReadOnlyField(source='producto.codigo')
    class Meta:
        model = DetallePedido
        fields = ['codigo','cantidad']

class PedidoSerializer(serializers.ModelSerializer):
    productos = DetallePedidoSerializer(source='detallepedido_set', many=True)
    class Meta:
        model = Pedido
        fields = [
            'id_pedido',
            'fecha_pedido',
            'sucursal',
            'productos',
            'estado',
            'total',
        ]