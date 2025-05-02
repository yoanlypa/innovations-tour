from django import forms
from .models import Tarea, Pedido, Producto, StockControl, Maleta
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
            'pattern': r'\d{2}/\d{2}/\d{4}' 
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
        fields = [
            'fecha_inicio', 'fecha_fin', 'excursion', 
            'empresa', 'lugar_entrega', 'lugar_recogida', 'fecha_entrega',
            'entregado', 'recogido', 'usuario', 
            'estado', 'notas'
        ]
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'notas': forms.Textarea(attrs={'rows': 3}),
        }

class MaletaForm(forms.ModelForm):
    class Meta:
        model = Maleta
        fields = ['guia', 'pax']

MaletaFormSet = forms.inlineformset_factory(
    StockControl,
    Maleta,
    form=MaletaForm,
    extra=1,  # 1 maleta por defecto
    can_delete=True
)