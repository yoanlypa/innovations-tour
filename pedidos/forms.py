from django import forms
from .models import Tarea, Pedido, Producto, StockControl, Maleta
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.core.exceptions import ValidationError
from .utils import convertir_fecha
from pedidos.models import Pedido 



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
        fields = ['pedido','excursion', 'empresa', 'lugar_entrega', 'lugar_recogida', 'fecha_inicio', 'fecha_fin', 'estado', 'notas']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pedido'].queryset = Pedido.objects.filter(estado='confirmado')
class BaseMaletaFormSet(BaseInlineFormSet):
    def save_new(self, form, commit=True):
        form.instance.pedido = self.instance.pedido
        return super().save_new(form, commit=commit)

    def clean(self):
        super().clean()
        if any(self.errors):
            return
        total = 0
        for form in self.forms:
            # Solo cuenta formularios no vacíos y no eliminados
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                total += 1
        if total < 1:
            raise ValidationError('Debe haber al menos una maleta activa.')
class MaletaForm(forms.ModelForm):
    class Meta:
        model = Maleta
        fields = ['guia', 'cantidad_pax']  # usa el nombre real del campo

# Creamos el inlineformset con nuestro BaseMaletaFormSet
MaletaFormSet = inlineformset_factory(
    parent_model=StockControl,
    model=Maleta,
    form=MaletaForm,
    formset=BaseMaletaFormSet,
    extra=1,
    can_delete=True,
)