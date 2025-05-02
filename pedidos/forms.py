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
        fields = [
            'fecha_inicio', 'fecha_fin', 'lugar_entrega', 'lugar_recogida',
            'empresa', 'cantidad', 'guia', 'usuario', 'productos', 'estado', 'notas'
        ]

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'cantidad', 'almacen']
        

class StockControlForm(forms.ModelForm):
    class Meta:
        model = StockControl
        fields = '__all__'
        widgets = {
            'fecha_creacion': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'step': '300'  # Intervalos de 5 minutos
                },
                format='%d/%m/%Y %H:%M'  # Formato español
            )
        }

    class Meta:
        model = StockControl
        fields = '__all__'
        widgets = {
            'fecha_er': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
