from django.db import models
from django.core.exceptions import ValidationError
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
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    notas = models.TextField(blank=True)
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
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
    pax = models.IntegerField(verbose_name="PAX")
    lugar_er = models.CharField(verbose_name="Lugar E/R", max_length=100)
    excursion = models.CharField(verbose_name="Excursión", max_length=100)
    guia = models.CharField(verbose_name="Guía", max_length=100)
    fecha_er = models.DateField(verbose_name="Fecha E/R")
    fecha_creacion = models.DateTimeField(
        verbose_name="Fecha de Creación",
        default=timezone.now,
        help_text="Fecha de registro (modificable)"
    )
    entregado = models.BooleanField(verbose_name="Entregado", default=True)
    recogido = models.BooleanField(verbose_name="Recogido", default=False)

    def clean(self):
        # Validar que no tenga ambos estados activos
        if self.entregado and self.recogido:
            raise ValidationError("Un registro no puede estar entregado y recogido simultáneamente")
        
        # Validar fecha de creación no futura
        if self.fecha_creacion > timezone.now():
            raise ValidationError("La fecha de creación no puede ser futura")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.excursion} - {self.fecha_er}"

    class Meta:
        verbose_name = "Control de Stock"
        verbose_name_plural = "Controles de Stock"
        ordering = ['-fecha_creacion']

class RegistroCliente(models.Model):
    nombre_usuario = models.CharField(max_length=150)
    email = models.EmailField()
    empresa = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_usuario} -  {self.empresa}"