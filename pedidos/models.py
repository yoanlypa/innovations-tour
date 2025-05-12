from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import admin
from django import forms
from .utils import convertir_fecha
from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    nombre = models.CharField("Nombre", max_length=100)
    cantidad = models.IntegerField("Cantidad", default=0)
    almacen = models.CharField("Almacén", max_length=100)

    def __str__(self):
        return f"{self.nombre} ({self.cantidad})"


class Pedido(models.Model):
    ESTADO_CLIENTE = [
        ('pendiente', '🟡 Pendiente'),
        ('pagado', '🟢 Pagado'),
        ('entregado', '🔵 Entregado'),
    ]

    ESTADO_EQUIPO = [
        ('por_revisar', '🔍 Por revisar'),
        ('aprobado', '✅ Aprobado'),
        ('entregado', '📦 Entregado'),
        ('recogido', '📥 Recogido'),
    ]

    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateField(null=True, blank=True)

    lugar_entrega = models.CharField(max_length=100, blank=True, default='')
    lugar_recogida = models.CharField(max_length=100, blank=True, default='')
    empresa = models.CharField(max_length=100)
    excursion = models.CharField(max_length=255, blank=True, null=True)
    guia_general = models.CharField(max_length=100, default='Sin asignar')
    notas = models.TextField(blank=True)

    fecha_creacion = models.DateField()
    fecha_modificacion = models.DateTimeField(auto_now=True)

    estado_cliente = models.CharField(max_length=20, choices=ESTADO_CLIENTE, default='pagado')
    estado_equipo = models.CharField(max_length=20, choices=ESTADO_EQUIPO, default='aprobado')

    entregado = models.BooleanField(default=False)
    recogido = models.BooleanField(default=False)

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    productos = models.ManyToManyField('Producto', blank=True, related_name='pedidos')

    def __str__(self):
        return f"{self.empresa} - {self.excursion} ({self.fecha_inicio.date()})"

class Maleta(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='maletas', on_delete=models.CASCADE)
    cantidad_pax = models.IntegerField()
    guia = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.guia} ({self.cantidad_pax} pax)"

class Tarea(models.Model):
    PRIORIDADES = [('alta','Alta'),('media','Media'),('baja','Baja')]
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    prioridad = models.CharField("Prioridad", max_length=20, choices=PRIORIDADES)
    completada      = models.BooleanField("Completada", default=False)
    fecha_creacion  = models.DateTimeField("Creada", auto_now_add=True)
    fecha_especifica= models.DateTimeField("Para", default=models.timezone.localtime)


    def __str__(self):
        return self.titulo

class RegistroCliente(models.Model):
    nombre_usuario  = models.CharField("Usuario", max_length=150)
    email           = models.EmailField("Email")
    empresa         = models.CharField("Empresa", max_length=255, blank=True, null=True)
    telefono        = models.CharField("Teléfono", max_length=50, blank=True, null=True)
    fecha_registro  = models.DateTimeField("Registrado", auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_usuario} – {self.empresa}"