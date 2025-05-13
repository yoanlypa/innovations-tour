from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from .models import Pedido, Producto, Tarea, Maleta
from .utils import convertir_fecha
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ya está en uso.')
        return email
# 
# 
# 
# 
# 
# 
# ========== FORMULARIO DE TAREAS ==========
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'prioridad', 'completada']


# 
# 
# 
# 
# 
# 
# ========== FORMULARIO DE PEDIDOS ==========
class PedidoForm(forms.ModelForm):

    class Meta:
        model = Pedido
        exclude = ['fecha_creacion']
        fields = [
            'empresa', 'excursion', 'lugar_entrega', 'lugar_recogida',
            'fecha_inicio', 'fecha_fin',
            'estado_cliente', 'estado_equipo', 'notas', 'productos'
        ]
        widgets = {
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la empresa'}),
            'excursion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la excursión'}),
            'lugar_entrega': forms.TextInput(attrs={'class': 'form-control'}),
            'lugar_recogida': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'estado_cliente': forms.Select(attrs={'class': 'form-select'}),
            'estado_equipo': forms.Select(attrs={'class': 'form-select'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'productos': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def clean_fecha_creacion(self):
        fecha_str = self.cleaned_data['fecha_creacion']
        return convertir_fecha(fecha_str)

class PedidoFormCliente(forms.ModelForm):
    class Meta:
        model  = Pedido
        fields = [
            'fecha_inicio', 'fecha_fin',
            'empresa', 'excursion',
            'lugar_entrega', 'lugar_recogida',
            'notas', 'estado_cliente'

        ]
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin':    forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'empresa':      forms.TextInput(attrs={'class': 'form-control'}),
            'excursion':    forms.TextInput(attrs={'class': 'form-control'}),
            'lugar_entrega': forms.TextInput(attrs={'class': 'form-control'}),
            'lugar_recogida': forms.TextInput(attrs={'class': 'form-control'}),
            'notas':        forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado_cliente': forms.Select(attrs={'class': 'form-select'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si quisieras asegurarte que todos los campos usen form-control:
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

class MaletaForm(forms.ModelForm):
    class Meta:
        model  = Maleta
        fields = ['guia', 'cantidad_pax']
        widgets = {
            'guia':         forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_pax': forms.NumberInput(attrs={'class': 'form-control'}),
        }


MaletaFormSet = inlineformset_factory(
    Pedido, Maleta,
    fields=("guia", "cantidad_pax"),
    widgets={
        "guia": forms.TextInput(attrs={"class": "form-control"}),
        "cantidad_pax": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
    },
    extra=0,
    can_delete=True
)
# 
# 
# 
# 
# ========== FORMULARIO DE PRODUCTOS ==========
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'cantidad', 'almacen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'almacen': forms.TextInput(attrs={'class': 'form-control'}),
        }


#
# 
# 
# 
# ========== FORMULARIO DE MALETAS ==========
class MaletaForm(forms.ModelForm):
    class Meta:
        model = Maleta
        fields = ['guia', 'cantidad_pax']
        widgets = {
            'guia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del guía'}),
            'cantidad_pax': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad de pax'}),
        }


class BaseMaletaFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        total = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                total += 1
        if total < 1:
            raise ValidationError('Debe incluir al menos una maleta.')


# Inline formset entre Pedido y Maleta
MaletaFormSet = inlineformset_factory(
    parent_model=Pedido,
    model=Maleta,
    form=MaletaForm,
    formset=BaseMaletaFormSet,
    extra=1,
    can_delete=True
)
