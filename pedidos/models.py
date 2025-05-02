from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import admin
from .utils import convertir_fecha

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
    fecha_creacion = models.DateField()
    def __init__(self, *args, **kwargs):
        # Convertir fechas en formato string
        if 'fecha_creacion' in kwargs and isinstance(kwargs['fecha_creacion'], str):
            kwargs['fecha_creacion'] = convertir_fecha(kwargs['fecha_creacion'])
        super().__init__(*args, **kwargs)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    notas = models.TextField(blank=True)
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    productos = models.ManyToManyField(Producto, blank=True, related_name='pedidos')
class Maleta(models.Model):
    stock_control = models.ForeignKey('StockControl', on_delete=models.CASCADE, null=True, blank=True)

    pedido = models.ForeignKey(Pedido, related_name='maletas', on_delete=models.CASCADE)
    cantidad_pax = models.IntegerField()
    guia = models.CharField(max_length=255)
    
class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=20, choices=[('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')])
    completada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha creación"
    )
    fecha_especifica = models.DateTimeField(
        default=timezone.localtime,  # Fecha local
        verbose_name="Fecha programada"
    )


    def __str__(self):
        return self.titulo


class StockControl(models.Model):
    ESTADOS = (
        ('P', 'Pendiente'),
        ('G', 'Pagado'),
    )
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    fecha_inicio = models.DateField( blank=True, null=True)
    fecha_fin = models.DateField(null=True, blank=True)
    excursion = models.CharField(max_length=100,null=True, blank=True)
    empresa = models.CharField(max_length=100,null=True, blank=True)
    lugar_entrega = models.CharField(max_length=200,null=True, blank=True)
    lugar_recogida = models.CharField(max_length=200,null=True, blank=True)
    guia = models.CharField(max_length=255,null=True, blank=True)
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    notas = models.TextField(blank=True,null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    maletas = models.ManyToManyField('Maleta', through='StockMaleta')
    entregado = models.BooleanField(default=False)
    recogido = models.BooleanField(default=False)

def __str__(self):
        return f"Excursión: {self.excursion} ({self.fecha_inicio} - {self.fecha_fin})"
class StockMaleta(models.Model):
    stock = models.ForeignKey(StockControl, on_delete=models.CASCADE)
    maleta = models.ForeignKey(Maleta, on_delete=models.CASCADE)
    guia = models.CharField(max_length=100)
    pax = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('stock', 'maleta')

class StockMaletaAdmin(admin.ModelAdmin):
    ordering = ['fecha_creacion']
    list_display = ('stock', 'maleta', 'guia', 'pax')

admin.site.register(StockMaleta, StockMaletaAdmin)
class RegistroCliente(models.Model):
    nombre_usuario = models.CharField(max_length=150)
    email = models.EmailField()
    empresa = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_usuario} -  {self.empresa}"