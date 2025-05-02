from django.contrib import admin
from .models import Tarea, StockControl, Maleta, Pedido
from django.utils.html import format_html


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fecha_creacion','fecha_especifica','completada']
    
    def fecha_creacion_formateada(self, obj):
        return obj.fecha_creacion.strftime("%d/%m/%Y")
    fecha_creacion_formateada.short_description = 'Fecha'
    
class StockControlAdmin(admin.ModelAdmin):
    list_display = ('fecha_inicio', 'fecha_fin', 'excursion', 'empresa', 'lugar_entrega', 'lugar_recogida', 'estado', 'guia', 'fecha_creacion', 'entregado', 'recogido', 'mostrar_maletas', 'notas')
    list_filter = ('fecha_creacion', 'entregado', 'recogido')
    search_fields = ('excursion', 'guia')
    ordering = ('fecha_creacion',)

    # Función personalizada para mostrar maletas
    def mostrar_maletas(self, obj):
        return ", ".join([str(maleta) for maleta in obj.maletas.all()])
    mostrar_maletas.short_description = 'Maletas'

admin.site.register(StockControl, StockControlAdmin)
class MaletaInline(admin.TabularInline):
    model = Maleta
    extra = 0

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id','usuario','empresa','fecha_inicio','estado')
    list_filter = ('estado',)
    inlines = [MaletaInline]