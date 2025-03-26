from django import forms
from .models import Pedido, Tarea, Nota

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'fecha_inicio', 
            'fecha_fin',
            'empresa', 
            'lugar_entrega', 
            'cantidad_radios', 
            'estado', 
            'guia'
        ]
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['descripcion', 'fecha', 'prioridad']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'})
        }

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['contenido']