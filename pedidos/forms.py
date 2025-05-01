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
    fecha_creacion = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'max': timezone.localtime().strftime('%Y-%m-%dT%H:%M')
            }
        ),
        initial=timezone.now
    )

    class Meta:
        model = StockControl
        fields = '__all__'
        widgets = {
            'fecha_er': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_fecha_creacion(self):
        fecha = self.cleaned_data['fecha_creacion']
        if fecha > timezone.now():
            raise forms.ValidationError("¡No se permiten fechas futuras!")
        return fecha