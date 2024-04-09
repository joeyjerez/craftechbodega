import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status, generics
from rest_framework.decorators import api_view
from bodega.models import *
from .serializers import *

# Create your views here.

def root(request):
    return redirect(producto_list)

@api_view(['GET', 'POST', 'DELETE'])
def producto_list(request, format=None):
    if request.method == 'GET':
        productos = Producto.objects.all()

        if productos:
            productos_serializer = ProductoSerializerList(productos,many=True)
            return Response(productos_serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'mensaje':'No hay productos registrados.'},status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        producto_data = JSONParser().parse(request)
        producto_serializer = ProductoSerializerList(data=producto_data)
        if producto_serializer.is_valid():
            producto_serializer.save()
            return Response(producto_serializer.data, status=status.HTTP_201_CREATED)
        return Response(producto_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        cantidad = Producto.objects.all().delete()
        return Response({'mensaje':'¡{} productos han sido eliminados de la base de datos!'.format(cantidad[0])},status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def producto_detail(request, codigo, format=None):
    try:
        producto = Producto.objects.get(codigo=codigo)
    except:
        return Response({'mensaje':'El producto con código {} no existe'.format(codigo)},status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        producto_serializer = ProductoSerializer(producto)
        return Response(producto_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        producto_data = JSONParser().parse(request)
        producto_serializer = ProductoSerializer(producto,data=producto_data)
        if producto_serializer.is_valid():
            producto_serializer.save()
            return Response(producto_serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(producto_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        producto.delete()
        return Response({'mensaje':'¡El producto con el código {} ha sido eliminado satisfactoriamente!'.format(codigo)},status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def pedido_list(request, format = None):
    if request.method == 'GET':
        pedidos = Pedido.objects.all()

        if pedidos:
            pedidos_serializer = PedidoSerializer(pedidos, many=True)
            return Response(pedidos_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'mensaje':'No hay pedidos registrados.'}, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'POST':
        pedido_data = JSONParser().parse(request)
        pedido_serializer = PedidoSerializer(data=pedido_data)
        if pedido_serializer.is_valid():
            pedido_serializer.save()
            return Response(pedido_serializer.data, status=status.HTTP_201_CREATED)
        return Response(pedido_serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def pedido_detail(request, id_pedido, format = None):
    try:
        pedido = Pedido.objects.get(id_pedido=id_pedido)
    except:
        return Response({'mensaje':'El pedido con id {} no existe'.format(id_pedido)},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        pedido_serializer = PedidoSerializer(pedido)
        return Response(pedido_serializer.data, status=status.HTTP_200_OK)
