from django.contrib import admin
from .models import Tarea, StockControl
from django.utils.html import format_html


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fecha_creacion','fecha_especifica','completada']
    
    def fecha_creacion_formateada(self, obj):
        return obj.fecha_creacion.strftime("%d/%m/%Y")
    fecha_creacion_formateada.short_description = 'Fecha'
    
@admin.register(StockControl)
class StockControlAdmin(admin.ModelAdmin):
    list_display = ('pax', 'lugar_er', 'excursion', 'guia', 'fecha_er', 'entregado', 'recogido')
    list_filter = ('fecha_er', 'entregado', 'recogido')
    search_fields = ('excursion', 'guia')
    ordering = ('fecha_er',)