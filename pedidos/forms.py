from django import forms
from .models import Tarea, Pedido, Producto, StockControl
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .utils import convertir_fecha




class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'prioridad', 'completada']  # ✅ Campos existentes

class PedidoForm(forms.ModelForm):
    fecha_creacion = forms.CharField(
        label="Fecha (dd/mm/aaaa)",
        widget=forms.DateInput(attrs={
            'placeholder': 'dd/mm/aaaa',
            'pattern': '\d{2}/\d{2}/\d{4}'
        })
    )

    class Meta:
        model = Pedido
        fields = '__all__'

    def clean_fecha_creacion(self):
        fecha_str = self.cleaned_data['fecha_creacion']
        return convertir_fecha(fecha_str)

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
