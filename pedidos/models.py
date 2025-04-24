from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=0)
    almacen = models.CharField(max_length=50)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.get_almacen_display()})"
    
class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', '🟡 Pendiente'),
        ('confirmado', '🟢 Confirmado'),
        ('entregado', '🔵 Entregado'),
    ]

    fecha_inicio = models.DateTimeField(null=False)
    fecha_fin = models.DateField(null=True, blank=True)
    lugar_entrega = models.CharField(max_length=100, blank=True, default='')
    lugar_recogida = models.CharField(max_length=100, blank=True, default='')
    empresa = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=0, help_text="Cantidad de productos a entregar")
    guia = models.CharField(max_length=100, default='Sin asignar')  # 🛠 Valor por defecto para migrar
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    notas = models.TextField(blank=True)

    productos = models.ManyToManyField(Producto, blank=True, related_name='pedidos')
class Maleta(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='maletas', on_delete=models.CASCADE)
    cantidad_pax = models.IntegerField()
    guia = models.CharField(max_length=255)
    
class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=20, choices=[('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')])
    completada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_especifica = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.titulo
class StockControl(models.Model):
    pax = models.IntegerField()
    lugar_er = models.CharField(max_length=255)
    excursion = models.CharField(max_length=255)
    guia = models.CharField(max_length=255)
    fecha_er = models.DateField()
    entregado = models.BooleanField(default=False)
    recogido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pax} - {self.excursion}"