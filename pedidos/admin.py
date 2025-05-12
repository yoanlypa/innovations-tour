from django.contrib import admin
from .models import Pedido, Maleta, Producto, Tarea, RegistroCliente

class MaletaInline(admin.TabularInline):
    model = Maleta
    extra = 0
    readonly_fields = ['guia', 'cantidad_pax']
    can_delete = False

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'excursion', 'fecha_inicio', 'estado_cliente', 'estado_equipo')
    readonly_fields = ('fecha_creacion',)
    list_filter = ('estado_cliente', 'estado_equipo', 'fecha_inicio')
    search_fields = ('empresa', 'excursion', 'usuario__username')
    ordering = ['-fecha_inicio']
    inlines = [MaletaInline]

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad', 'almacen')
    search_fields = ('nombre',)

class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'prioridad', 'completada', 'fecha_creacion', 'fecha_especifica')
    list_filter = ('completada', 'prioridad')
    search_fields = ('titulo',)

admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Tarea, TareaAdmin)
admin.site.register(RegistroCliente)
admin.site.site_header = "Control Radioguías Admin"