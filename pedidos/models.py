from django.db import models
from django.urls import reverse

class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', '🟡 Pendiente'),
        ('confirmado', '🟢 Confirmado'),
        ('entregado', '🔵 Entregado'),
    ]
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    empresa = models.CharField(max_length=100)
    lugar_entrega = models.CharField(max_length=200)
    cantidad_radios = models.IntegerField()
    excursion = models.CharField(max_length=100)
    guia = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    
    def get_absolute_url(self):
        return reverse('detalle_pedido', args=[str(self.id)])

class Producto(models.Model):
    ALMACENES = [
        ('principal', 'Almacén Principal'),
        ('secundario', 'Almacén Secundario'),
        ('reserva', 'Almacén de Reserva'),
    ]
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=0)
    almacen = models.CharField(max_length=50, choices=ALMACENES)
    
    def __str__(self):
        return f"{self.nombre} ({self.get_almacen_display()})"

class Tarea(models.Model):
    PRIORIDADES = [
        ('alta', '🔥 Alta'),
        ('media', '⚠️ Media'),
        ('baja', '💤 Baja'),
    ]
    descripcion = models.CharField(max_length=200)
    fecha = models.DateField()
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='media')
    realizada = models.BooleanField(default=False)

class Nota(models.Model):
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)