from django import forms
from .models import Tarea, Pedido, Producto, StockControl
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone




class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'prioridad', 'completada']  # ✅ Campos existentes

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['empresa', 'productos', 'estado', 'notas']
        widgets = {
            'productos': forms.CheckboxSelectMultiple,
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'cantidad', 'almacen']
        

class StockControlForm(forms.ModelForm):
    class Meta:
        model = StockControl
        fields = ['pax', 'lugar_er', 'excursion', 'guia', 'fecha_er', 'entregado', 'recogido']

# Formset para edición múltiple
StockControlFormSet = forms.modelformset_factory(
    StockControl,
    fields=('pax', 'lugar_er', 'excursion', 'guia', 'fecha_er', 'entregado', 'recogido'),
    extra=0,
    widgets={
        'entregado': forms.CheckboxInput(),
        'recogido': forms.CheckboxInput(),
    }
)
class StockERForm(forms.ModelForm):
    class Meta:
        model = StockControl
        fields = ['entregado', 'recogido']