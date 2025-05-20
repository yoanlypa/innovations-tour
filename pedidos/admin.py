from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone
from datetime import timedelta
from django_object_actions import DjangoObjectActions, action

from .models import Maleta, Pedido, Producto, RegistroCliente, Tarea


class MaletaInline(admin.TabularInline):
    model = Maleta
    extra = 0
    readonly_fields = ["guia", "cantidad_pax"]
    can_delete = False


class PedidoAdmin(DjangoObjectActions,admin.ModelAdmin):
    list_display = (
        "id",
        "empresa",
        "fecha_inicio",
        "fecha_fin",
        "estado",
        "usuario",
        "acciones",
    )
    readonly_fields = ("fecha_creacion",)
    list_editable = ("estado",)  # permite cambiar el estado directamente desde la lista
    list_filter = ( "fecha_inicio")
    search_fields = ("empresa", "excursion", "usuario__username")
    ordering = ["-fecha_inicio"]
    inlines = [MaletaInline]
    change_actions = ('borrar_directo',)
    actions = ['delete_selected','borrar_antiguos']
    list_per_page = 20
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("usuario")
    
    def usuario(self, obj):
        return obj.usuario.username
    usuario.short_description = "Usuario"

    def acciones(self, obj):
        """
        Botones de Editar y Eliminar en cada fila.
        """
        editar_url = reverse("admin:pedidos_pedido_change", args=[obj.pk])
        borrar_url = reverse("admin:pedidos_pedido_delete", args=[obj.pk])
        return format_html(
            '<a class="button btn-sm btn-warning me-1" href="{}">✏️</a>'
            '<a class="button btn-sm btn-danger" href="{}" '
            'onclick="return confirm(\'¿Eliminar este pedido?\');">🗑️</a>',
            editar_url,
            borrar_url,
        )
    acciones.short_description = "Acciones"
    def borrar_antiguos(self, request, queryset):
        limite = timezone.now() - timedelta(days=60)
        antiguos = queryset.filter(fecha_inicio__lt=limite)
        count = antiguos.count()
        antiguos.delete()
        self.message_user(request, f"Eliminados {count} pedidos con más de 60 días.")
    borrar_antiguos.short_description = "Eliminar pedidos con más de 60 días"

    def borrar_directo(self, request, obj):
        obj.delete()
        self.message_user(request, "Pedido eliminado.")
    borrar_directo.label = "🗑️ Borrar"
    borrar_directo.short_description = "Eliminar este pedido"
        
    def accion_eliminar(self, obj):
        url = reverse('admin:pedidos_pedido_delete', args=[obj.pk])
        return format_html(
            '<a class="button" style="color:red;" href="{}">🗑️</a>',
            url
        )
    accion_eliminar.short_description = 'Eliminar'
    accion_eliminar.allow_tags = True

class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "cantidad", "almacen")
    search_fields = ("nombre",)


class TareaAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "prioridad",
        "completada",
        "fecha_creacion",
        "fecha_especifica",
    )
    list_filter = ("completada", "prioridad")
    search_fields = ("titulo",)


admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Tarea, TareaAdmin)
admin.site.register(RegistroCliente)
admin.site.site_header = "Control Radioguías Admin"
