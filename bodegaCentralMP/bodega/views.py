#from django.shortcuts import render

# Create your views here.
import requests, random
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from faker import Faker
from faker.providers import BaseProvider

@login_required
def root(request):
    return redirect('/bodega')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Credenciales inválidas. Inténtalo nuevamente.'
            return render(request, 'core/login.html', {'error_message': error_message})
    return render(request, 'core/login.html')

@login_required
def index(request):
    if request.user.is_authenticated:
        return render(request, 'core/home.html')
    else:
        return redirect('login')

def error404(request):
    return render(request, 'core/404.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def saludo(request):
    
    url = "https://musicpro.bemtorres.win/api/v1/saludo"

    try:
        response = requests.get(url)
        data = response.json()
        respuesta = "Todo bueno, todo correcto"
        print(respuesta)

    except requests.exceptions.RequestException as e:
        respuesta = f'Error: {e}'
    
    return HttpResponse(f"<h1>¡Saludo completado!</h1>\n<h2>{respuesta}</h2>")

@login_required
def solicitud_transporte(request, id_pedido, transporte):
    
    pedido = Pedido.objects.get(id_pedido = id_pedido)
    
    if ("MUSICPRO" or "JV") in pedido.estado:
        return redirect(reverse('pedidos_list') + "?AE")
    
    else:
        
        if transporte == 1:
            
            #MusicPro Bemtorres
            url = 'https://musicpro.bemtorres.win/api/v1/transporte/solicitud'
            
            post = {
                "nombre_origen":"bodegaCentralMP",
                "direccion_origen":"Plaza Sésamo 123",
                "nombre_destino": pedido.sucursal.nombre,
                "direccion_destino": pedido.sucursal.direccion,
                "comentario": f"Envío de Pedido #{pedido.id_pedido} para {pedido.sucursal.nombre}",
                "info": "bodegaCentralMP"
            }
        elif transporte == 2:
            
            #GranJVCorp
            url = 'http://127.0.0.1:8001/pedidos/api/v1/pedidos/'
            
            
            post = {
                "lugar_origen": "Bodega",
                "nombre_origen": "bodegaCentralMP",
                "direccion_origen": "Plaza Sésamo 123",
                "nombre_destino": pedido.sucursal.nombre,
                "direccion_destino": pedido.sucursal.direccion,
                "correo_destino": pedido.sucursal.correo
            }
        
        print(post)
        
        try:
            response = requests.post(url, post)
            data = response.json()
            
            if response.status_code == 201:
                pedido.estado = data['estado']
                pedido.codigo_seguimiento = data['codigo_seguimiento']
                pedido.save()
                print("Solicitud de seguimiento realizada correctamente.")
                return redirect(reverse('pedidos_list') + "?POST") 
            elif response.status_code == 400:
                print("Error en la solicitud de seguimiento.")
                print(data['mensaje'])
                return redirect(reverse('pedidos_list') + "?POSTFAIL")
            else: raise requests.exceptions.RequestException
        except requests.exceptions.RequestException as e:
            respuesta = 'Error: {e}'
            return redirect(reverse('pedidos_list') + "?POSTFAIL")
        except:
            respuesta = 'Error cualquiera.'
            return redirect(reverse('pedidos_list') + "?POSTFAIL")

@login_required
def actualizar_estado(request, id_pedido):
    pedido = Pedido.objects.get(id_pedido = id_pedido)
    codigo_seguimiento = pedido.codigo_seguimiento
    
    if "MUSICPRO" in codigo_seguimiento:
        transporte = 1
        url = f'https://musicpro.bemtorres.win/api/v1/transporte/seguimiento/{codigo_seguimiento}'
    elif "JV" in codigo_seguimiento:
        transporte = 2
        url = f"http://127.0.0.1:8001/pedidos/api/v1/pedidos/{codigo_seguimiento}/"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            if transporte == 1:
                seguimiento = data['result']['estado']
                cod_seg = data['result']['solicitud']['codigo_seguimiento']
            elif transporte == 2:
                seguimiento = data['estado']
                cod_seg = data['codigo_seguimiento']
            
            pedido.estado = seguimiento
            pedido.codigo_seguimiento = cod_seg
            pedido.save()
            print(f"Estado del Pedido: {seguimiento}")
            
            return redirect(reverse('pedidos_list') + "?R")
        
        elif response.status_code == 404:
            
            print(f"Error en actualizar el estado del pedido {id_pedido}.")
            return redirect(reverse('pedidos_list') + "?RF")
        
        else: raise requests.exceptions.RequestException
        
    except requests.exceptions.RequestException as e:
        respuesta = 'Error: {e}'
        return redirect(reverse('pedidos_list') + "?RF")
    except:
            respuesta = 'Error desconocido.'
            return redirect(reverse('pedidos_list') + "?RF")


@login_required
def productos_list(request):
    context = {'productos' : Producto.objects.all()}
    return render(request, 'core/producto/productos.html', context)

@login_required
def productos_new(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            codigo = form.cleaned_data.get("codigo")
            nombre = form.cleaned_data.get("nombre")
            stock = form.cleaned_data.get("stock")
            marca = form.cleaned_data.get("marca")
            descripcion = form.cleaned_data.get("descripcion")
            imagen = form.cleaned_data.get("imagen")
            precio = form.cleaned_data.get("precio")
            obj = Producto.objects.create(
                codigo = codigo,
                nombre = nombre,
                stock = stock,
                marca = marca,
                descripcion = descripcion,
                imagen = imagen,
                precio = precio,
            )
            obj.save()
            return redirect(reverse('productos_list') + "?OK")
        else:
            return redirect(reverse('productos_list') + "?FAIL")
    else:
        form = ProductoForm
    return render(request,'core/producto/producto_new.html',{'form':form})

@login_required
def productos_edit(request, codigo):
    try:
        producto = Producto.objects.get(codigo=codigo)
        if producto:
            form = ProductoForm(instance = producto)
        else:
            return redirect(reverse('productos_list') + "?FAIL")
    
        if request.method == 'POST':
            form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
            if form.is_valid():
                form.save()
                return redirect(reverse('productos_list') + "?OK")
            else:
                return redirect(reverse('productos_edit') + codigo)
        return render(request,'core/producto/producto_edit.html',{'form':form})   
    except:
        return redirect(reverse('productos_list') + "?FAIL")

@login_required
def productos_delete(request, codigo):
    try:
        producto = Producto.objects.get(codigo=codigo)
        producto.delete()
        return redirect(to= 'productos_list')
    except:
        return redirect(reverse('productos_list') + "?FAIL")

@login_required
def sucursal_list(request):
    context = {'sucursales' : Sucursal.objects.all()}
    return render(request, 'core/sucursal/sucursales.html', context)

@login_required
def sucursal_new(request):
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            id_sucursal = form.cleaned_data.get("id_sucursal")
            nombre = form.cleaned_data.get("nombre")
            direccion = form.cleaned_data.get("direccion")
            token = form.cleaned_data.get("token")
            obj = Sucursal.objects.create(
                id_sucursal = id_sucursal,
                nombre = nombre,
                direccion = direccion,
                token = token,
            )
            obj.save()
            return redirect(reverse('sucursal_list') + "?OK")
        else:
            return redirect(reverse('sucursal_list') + "?FAIL")
    else:
        form = SucursalForm
    return render(request,'core/sucursal/sucursal_new.html',{'form':form})

@login_required
def sucursal_edit(request, id_sucursal):
    try:
        sucursal = Sucursal.objects.get(id_sucursal=id_sucursal)
        if sucursal:
            form = SucursalForm(instance = sucursal)
        else:
            return redirect(reverse('sucursal_list') + "?FAIL")
    
        if request.method == 'POST':
            form = SucursalForm(request.POST or None, instance = sucursal)
            if form.is_valid():
                form.save()
                return redirect(reverse('sucursal_list') + "?OK")
            else:
                return redirect(reverse('sucursal_edit') + id_sucursal)
        return render(request,'core/sucursal/sucursal_edit.html',{'form':form})   
    except:
        return redirect(reverse('sucursal_list') + "?FAIL")

@login_required
def sucursal_delete(request, id_sucursal):
    try:
        sucursal = Sucursal.objects.get(id_sucursal=id_sucursal)
        sucursal.delete()
        return redirect(to= 'sucursal_list')
    except:
        return redirect(reverse('sucursal_list') + "?FAIL")

@login_required
def pedidos_list(request):
    context = {'pedidos' : Pedido.objects.all()}
    return render(request, 'core/pedido/pedidos.html', context)

@login_required
def pedidos_new(request):
    if request.method == 'POST':
        try:
            id_pedido = request.POST.get('pedido')
            sucursal_id = request.POST.get('sucursal')
            productos = request.POST.getlist('productos[]')
            estado = request.POST.get('estado')
            total = request.POST.get('total-pedido')
            
            sucursal = Sucursal.objects.get(id_sucursal=sucursal_id)

            pedido = Pedido.objects.create(id_pedido=id_pedido, sucursal=sucursal, estado=estado, total=total)
            pedido.save()
            print(f"Pedido: {pedido}")
            for producto_id in productos:
                producto = Producto.objects.get(codigo=producto_id)
                cantidad = int(request.POST.get('cantidad-' + producto_id))
                subtotal = producto.precio * cantidad

                producto.stock -= cantidad

                if producto.stock < 0:
                    raise forms.ValidationError(f"La cantidad solicitada del producto {producto_id} - {producto_id.nombre} supera la cantidad en stock.")
                else:
                    pedidoProducto = DetallePedido.objects.create(pedido=pedido, producto=producto, cantidad=cantidad, subtotal=subtotal)
                    pedidoProducto.save()
                    print(f"DetallePedido: {pedidoProducto}")
                    producto.save()
                    print(f"Producto: {producto}, Cantidad: {pedidoProducto.cantidad}")
            return redirect(reverse(pedidos_list) + "?OK")
        except:
            print(f"Producto: {producto}")
            pedido.delete()
            return redirect(reverse(pedidos_list) + "?FAIL")
    else:
        productos = Producto.objects.all()
        sucursales = Sucursal.objects.all()
        context = {
            'productos': productos,
            'sucursales': sucursales,
        }
    return render(request, 'core/pedido/pedido_new.html', context)

@login_required
def pedidos_detalle(request, id_pedido):
    try:
        pedido = Pedido.objects.get(id_pedido = id_pedido)
        detalle = DetallePedido.objects.filter(pedido_id = id_pedido)
        productos = Producto.objects.all()
        total = 0
        for p in detalle:
            total += p.subtotal

        return render(request, 'core/pedido/pedido_detalle.html',
        {
            'pedido':pedido,
            'detalle':detalle,
            'productos':productos,
            'total':total,
        })
    except:
        return render(redirect(pedidos_list))

@login_required
def pedidos_edit(request, id_pedido):
    try:
        if request.method == 'POST':
            pedido = Pedido.objects.get(id_pedido = id_pedido)
            estado = request.POST.get('estado')

            pedido.estado = estado
            pedido.save()
            return redirect(reverse('pedidos_list') + "?OK")
    except:
        return redirect(reverse('pedidos_list') + "?FAIL")

@login_required
def pedidos_delete(request, id_pedido):
    try:
        pedido = Pedido.objects.get(id_pedido=id_pedido)
        pedido.delete()
        return redirect(to= 'pedidos_list')
    except:
        return redirect(reverse('pedidos_list') + "?FAIL")

def admin_view(request):
    return redirect('admin/')

# fake = Faker()

# class instrumentoProvider(BaseProvider):
#     def instrumento(self) -> str:
#         LISTA_INSTRUMENTOS = ["Piano", "Guitarra acústica", "Violín", "Flauta travesera", "Batería", "Saxofón", 
#                               "Trompeta", "Bajo eléctrico", "Arpa", "Clarinete", "Trombón", "Violonchelo", "Guitarra eléctrica", 
#                               "Oboe", "Flauta dulce", "Tambor", "Xilófono", "Órgano", "Acordeón", "Cítara", "Banjo", 
#                               "Bongos", "Tuba", "Mandolina", "Tambor africano", "Armónica", "Sitar", "Marimba", "Glockenspiel", 
#                               "Trompa", "Contrabajo", "Celesta", "Bagpipes (Gaita)", "Balalaika", "Violín eléctrico", 
#                               "Cuerno francés", "Teclado electrónico", "Sintetizador", "Tambor de acero (Steel drum)", 
#                               "Laúd", "Gong", "Flauta de pan", "Theremin", "Kalimba", "Ocarina", "Timbales", "Dulcémele", 
#                               "Cuatro venezolano", "Caja de música", "Zampoña", "Bouzouki", "Charango", "Corno inglés", 
#                               "Guitarra española", "Melódica", "Sintetizador modular", "Saxofón alto", "Didgeridoo", 
#                               "Crótalos", "Steel guitar", "Sintetizador de voz", "Fliscorno", "Acordeón diatónico", 
#                               "Cuerno alpino", "Pandero", "Esraj", "Nyckelharpa", "Saz", "Guitarrón mexicano", 
#                               "Pandereta", "Ondas Martenot", "Ukelele", "Tambura", "Pipa", "Cítara china", "Bajo fretless", 
#                               "Tambor taiko", "Piccolo", "Órgano Hammond", "Trompeta de bolsillo", "Batería electrónica", 
#                               "Timple", "Mandolina mandocello", "Cuerno de posta", "Ondas rusas", "Shofar", "Campanas tubulares", 
#                               "Trompeta piccolo", "Clavicordio", "Djembe", "Cencerro", "Gaita de foles", "Tamborín", 
#                               "Konghou", "Koto", "Maracas", "Sarrusófono", "Vibrafón", "Guitarra hawaiana", "Daf"]
#         instrumento = random.choice(LISTA_INSTRUMENTOS)
#         return instrumento

# class marcaProvider(BaseProvider):
#     def marca(self) -> str:
#         LISTA_MARCAS = ["RockSmith", "Yamaha", "Fender", "Gibson", "Steinway & Sons", "Selmer", "Roland", "Pearl", "Martin", "Kong"]
#         marca = random.choice(LISTA_MARCAS)
#         return marca

# fake.add_provider(instrumentoProvider)
# fake.add_provider(marcaProvider)

# @login_required
# def productos_faker_1000(request):
    
#     for i in range(1000):
#         ultimo = Producto.objects.latest('codigo')
#         max_codigo = ultimo.codigo
#         codigo = max_codigo + 1
#         nombre = fake.instrumento()
#         stock = random.randint(5,1200)
#         marca = fake.marca()
#         descripcion = fake.text(300)
#         precio = fake.random_int(30000, 30000000)
                
#         print(codigo)
        
#         pedido = Producto(
#             codigo = codigo,
#             nombre = nombre,
#             stock = stock,
#             marca = marca,
#             descripcion = descripcion,
#             precio = precio,
#         )
#         pedido.save()
#     return redirect(reverse('productos_list'))

# @login_required
# def productos_faker_10000(request):
    
#     for i in range(10000):
#         ultimo = Producto.objects.latest('codigo')
#         max_codigo = ultimo.codigo
#         codigo = max_codigo + 1
#         nombre = fake.instrumento()
#         stock = random.randint(5,1200)
#         marca = fake.marca()
#         descripcion = fake.text(300)
#         precio = fake.random_int(30000, 30000000)
                
#         print(codigo)
        
#         pedido = Producto(
#             codigo = codigo,
#             nombre = nombre,
#             stock = stock,
#             marca = marca,
#             descripcion = descripcion,
#             precio = precio,
#         )
#         pedido.save()
#     return redirect(reverse('productos_list'))

# @login_required
# def productos_faker_100000(request):
    
#     for i in range(100000):
#         ultimo = Producto.objects.latest('codigo')
#         max_codigo = ultimo.codigo
#         codigo = max_codigo + 1
#         nombre = fake.instrumento()
#         stock = random.randint(5,1200)
#         marca = fake.marca()
#         descripcion = fake.text(300)
#         precio = fake.random_int(30000, 30000000)
                
#         print(codigo)
        
#         pedido = Producto(
#             codigo = codigo,
#             nombre = nombre,
#             stock = stock,
#             marca = marca,
#             descripcion = descripcion,
#             precio = precio,
#         )
#         pedido.save()
#     return redirect(reverse('productos_list'))

# @login_required
# def productos_faker_delete(request):
#     productos = Producto.objects.filter(imagen = "")
#     productos.delete()
    
#     return redirect(reverse('productos_list'))
    