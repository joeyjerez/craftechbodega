from django.db import models

class Producto(models.Model):
    codigo = models.IntegerField(primary_key=True, null=False, unique=True, verbose_name='Codigo')
    nombre = models.CharField(max_length=50, null=False, verbose_name='Nombre')
    stock = models.IntegerField(null=False, default=0, verbose_name='Stock')
    descripcion = models.CharField(max_length=400, verbose_name='Descripción')
    marca = models.CharField(max_length=80, verbose_name='Marca')
    precio = models.IntegerField(null=False, default=0, verbose_name='Precio')
    imagen = models.ImageField(null=True, blank=True, upload_to='productos/', verbose_name='Imagen')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')

    class Meta:
        verbose_name='producto'
        verbose_name_plural='productos'
        ordering=['codigo']

    def __str__(self):
        return self.nombre + " - ${:0,.0f}".format(self.precio)

class Sucursal(models.Model):
    id_sucursal = models.PositiveIntegerField(primary_key=True, verbose_name='ID Sucursal', unique=True)
    nombre = models.CharField(verbose_name='Nombre', null=False, max_length=150)
    direccion = models.CharField(verbose_name='Dirección', null=False, max_length=120)
    correo = models.EmailField(verbose_name='Correo', default="quetransitamen@gmail.com")
    token = models.CharField(verbose_name="Token", max_length=12, unique=True, default='secret')

    class Meta:
        verbose_name='sucursal'
        verbose_name_plural='sucursales'
        ordering=['id_sucursal']

    def __str__(self):
        return self.nombre

class Pedido(models.Model):

    pend = "Pendiente"
    envi = "En reparto"
    compl = "Completado"

    id_pedido = models.PositiveIntegerField(primary_key=True, unique=True)
    fecha_pedido = models.DateTimeField(verbose_name='Fecha del Pedido', auto_now_add=True)
    sucursal = models.ForeignKey(Sucursal, on_delete= models.CASCADE, null=False)
    productos = models.ManyToManyField(Producto, through='DetallePedido')
    estado = models.CharField(max_length=10, verbose_name='Estado', default=pend, null=False)
    codigo_seguimiento = models.CharField(max_length=16, verbose_name="Código de Seguimiento", default=pend)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0, verbose_name='Total del Pedido')
    class Meta:
        verbose_name='pedido'
        verbose_name_plural='pedidos'
        ordering=['id_pedido']
    
    def __str__(self):
        return f"Pedido #{self.id_pedido} - {self.sucursal}"

class DetallePedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.pedido.id_pedido} {self.pedido.id_pedido}"
