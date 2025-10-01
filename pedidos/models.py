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
    ESTADOS = [
        ("pendiente_pago", "Pendiente de pago"),
        ("pagado", "Pagado"),
        ("aprobado", "Aprobado"),
        ("entregado", "Entregado"),
        ("recogido", "Recogido"),
    ]

    fecha_inicio = models.DateTimeField("Fecha inicio", default=timezone.now)
    fecha_fin = models.DateTimeField("Fecha fin", null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    excursion = models.CharField("Excursión", max_length=100, blank=True, default="")
    empresa = models.CharField("Empresa", max_length=100)
    servicios = models.CharField("Servicio", max_length=100, blank=True, default="")
    lugar_entrega = models.CharField("Lugar entrega", max_length=100, blank=True, default="")
    lugar_recogida = models.CharField("Lugar recogida", max_length=100, blank=True, default="")
    notas = models.TextField("Notas", blank=True)
    estado = models.CharField("Estado", max_length=20, choices=ESTADOS, default="pagado")
    entregado = models.BooleanField("Entregado", default=False)
    recogido = models.BooleanField("Recogido", default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pedidos")
    updates = models.JSONField(default=list, blank=True, editable=False)

    def __str__(self):
        return f"{self.empresa} – {self.excursion or 'Sin excursión'} ({self.fecha_inicio.date()})"

    def _log_update(self, event, user=None, note=None):
            """Añade un evento al historial 'updates'."""
            entry = {
                "ts": timezone.now().isoformat(),  # ISO 8601
                "event": event,                    # p.ej. 'created', 'delivered', 'collected'
            }
            if user:
                entry["user_id"] = user.pk
                entry["user"] = getattr(user, "username", "") or getattr(user, "email", "")
            if note:
                entry["note"] = str(note)
            self.updates = (self.updates or []) + [entry]
    
        def save(self, *args, **kwargs):
            is_new = self.pk is None
            # si es nuevo y no hay updates, añade 'created' ANTES de guardar
            if is_new and not self.updates:
                self.updates = [{"ts": timezone.now().isoformat(), "event": "created"}]
            super().save(*args, **kwargs)
    
        def set_delivered(self, user=None, note=None):
            self.estado = "entregado"
            self.entregado = True
            self._log_update("delivered", user=user, note=note)
            self.save(update_fields=["estado", "entregado", "updates", "fecha_modificacion"])
    
        def set_collected(self, user=None, note=None):
            self.estado = "recogido"
            self.recogido = True
            self._log_update("collected", user=user, note=note)
            self.save(update_fields=["estado", "recogido", "updates", "fecha_modificacion"])
    
    
    class Servicio(models.Model):
        pedido = models.ForeignKey(
            "Pedido", related_name="servicios_linea", on_delete=models.CASCADE
        )
        excursion = models.CharField("Excursión", max_length=120)
        pax = models.PositiveIntegerField("PAX")
        emisores = models.PositiveSmallIntegerField("Emisores", default=1)
        guia = models.CharField("Guía", max_length=120, blank=True)
        lugar_entrega = models.CharField("Lugar de entrega", max_length=120, blank=True)
        bono = models.CharField("Bono", max_length=60, blank=True)
    
        class Meta:
            ordering = ["excursion"]
    
        def __str__(self):
            return f"{self.excursion} – {self.pax} pax"


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
