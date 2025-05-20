from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone  # Import correcto de timezone


class Producto(models.Model):
    nombre = models.CharField("Nombre", max_length=100)
    cantidad = models.IntegerField("Cantidad", default=0)
    almacen = models.CharField("Almacén", max_length=100)

    def __str__(self):
        return f"{self.nombre} ({self.cantidad})"


class Pedido(models.Model):
    ESTADOS= [
        ('pendiente_pago', 'Pendiente de pago'),
        ('pagado',         'Pagado'),
        ('aprobado',       'Aprobado'),
        ('entregado',      'Entregado'),
        ('recogido',       'Recogido'),
    ]

    fecha_inicio = models.DateTimeField("Fecha inicio", default=timezone.now)
    fecha_fin = models.DateTimeField("Fecha fin", null=True, blank=True)
    fecha_creacion = models.DateField(default=timezone.now, editable=False)
    fecha_modificacion = models.DateTimeField("Última modificación", auto_now=True)

    empresa = models.CharField("Empresa", max_length=100)
    excursion = models.CharField("Excursión", max_length=255, blank=True, null=True)
    lugar_entrega = models.CharField(
        "Lugar entrega", max_length=100, blank=True, default=""
    )
    lugar_recogida = models.CharField(
        "Lugar recogida", max_length=100, blank=True, default=""
    )
    notas = models.TextField("Notas", blank=True)

    estado = models.CharField("Estado", max_length=20, choices=ESTADOS, default='pagado')
    
    entregado = models.BooleanField("Entregado", default=False)
    recogido = models.BooleanField("Recogido", default=False)

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pedidos")
    productos = models.ManyToManyField(Producto, blank=True, related_name="pedidos")

    def __str__(self):
        return f"{self.empresa} – {self.excursion or 'Sin excursión'} ({self.fecha_inicio.date()})"


class Maleta(models.Model):
    pedido = models.ForeignKey(Pedido, related_name="maletas", on_delete=models.CASCADE)
    guia = models.CharField("Guía", max_length=255)
    cantidad_pax = models.PositiveIntegerField("PAX")

    def __str__(self):
        return f"{self.guia} ({self.cantidad_pax} pax)"


class Tarea(models.Model):
    PRIORIDADES = [
        ("alta", "Alta"),
        ("media", "Media"),
        ("baja", "Baja"),
    ]

    titulo = models.CharField("Título", max_length=200)
    descripcion = models.TextField("Descripción")
    prioridad = models.CharField("Prioridad", max_length=20, choices=PRIORIDADES)
    completada = models.BooleanField("Completada", default=False)
    fecha_creacion = models.DateTimeField("Creada", auto_now_add=True)
    fecha_especifica = models.DateTimeField("Para", default=timezone.now)

    def __str__(self):
        return self.titulo


class RegistroCliente(models.Model):
    nombre_usuario = models.CharField("Usuario", max_length=150)
    email = models.EmailField("Email")
    empresa = models.CharField("Empresa", max_length=255, blank=True, null=True)
    telefono = models.CharField("Teléfono", max_length=50, blank=True, null=True)
    fecha_registro = models.DateTimeField("Registrado", auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_usuario} – {self.empresa}"
