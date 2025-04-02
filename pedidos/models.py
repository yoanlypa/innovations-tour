from django.db import models
from django.contrib.auth.models import User

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
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    empresa = models.CharField(max_length=100)
    productos = models.ManyToManyField(Producto)
    estado = models.CharField(max_length=20, choices=ESTADOS,)
    notas = models.TextField(blank=True)

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
    pax = models.CharField("PAX", max_length=100)  # Nombre o número de PAX
    lugar_er = models.CharField("Lugar de E/R", max_length=200)  # Lugar de entrega/recogida
    excursion = models.CharField("Excursión", max_length=200)  # Nombre de la excursión
    guia = models.CharField("Guía", max_length=100)  # Nombre del guía
    fecha_er = models.DateField("Fecha de E/R")  # Fecha de entrega/recogida
    entregado = models.BooleanField("E", default=False)  # Checkbox para Entrega
    recogido = models.BooleanField("R", default=False)  # Checkbox para Recogida

    def __str__(self):
        return f"{self.excursion} - {self.pax}"