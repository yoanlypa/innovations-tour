from django import forms
from .models import Tarea, Pedido, Producto


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