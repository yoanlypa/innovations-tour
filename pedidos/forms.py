from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from .models import Pedido, Producto, Tarea, Maleta
from .utils import convertir_fecha
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone
from datetime import datetime, time

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



from .models import Pedido, Maleta
class PedidoFormCliente(forms.ModelForm):
    # Campos de fecha siguen siendo DateField (reciben date)
    fecha_inicio = forms.DateField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'dd/mm/aaaa',
            'autocomplete': 'off',
        }),
        # Aceptamos tanto el ISO de Flatpickr como dd/mm/aaaa
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        error_messages={
            'invalid': 'Introduce una fecha válida (dd/mm/aaaa)',
            'required': 'Este campo es obligatorio',
        },
    )
    fecha_fin = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'dd/mm/aaaa',
            'autocomplete': 'off',
        }),
        input_formats=['%Y-%m-%d', '%d/%m/%Y', ''],
        error_messages={
            'invalid': 'Introduce una fecha válida (dd/mm/aaaa)',
        },
    )

    class Meta:
        model = Pedido
        fields = [
            'fecha_inicio',
            'fecha_fin',
            'empresa',
            'excursion',
            'lugar_entrega',
            'lugar_recogida',
            'estado_cliente',
            'notas',
        ]
        widgets = {
            'empresa':        forms.TextInput(attrs={'class': 'form-control'}),
            'excursion':      forms.TextInput(attrs={'class': 'form-control'}),
            'lugar_entrega':  forms.TextInput(attrs={'class': 'form-control'}),
            'lugar_recogida': forms.TextInput(attrs={'class': 'form-control'}),
            'estado_cliente': forms.Select(attrs={'class': 'form-select'}),
            'notas':          forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Valor por defecto para estado_cliente
        self.fields['estado_cliente'].initial = 'pagado'

        # Al editar, mostramos dd/mm/aaaa para la pantalla
        if self.instance and self.instance.pk:
            if self.instance.fecha_inicio:
                local_i = timezone.localtime(self.instance.fecha_inicio)
                self.initial['fecha_inicio'] = local_i.strftime('%d/%m/%Y')
            if self.instance.fecha_fin:
                local_f = timezone.localtime(self.instance.fecha_fin)
                self.initial['fecha_fin'] = local_f.strftime('%d/%m/%Y')

    def clean_fecha_inicio(self):
        """Convierte la date a datetime aware antes de asignar al modelo."""
        date = self.cleaned_data['fecha_inicio']
        # Combina con hora 00:00 y haz aware
        dt = datetime.combine(date, time())
        return timezone.make_aware(dt, timezone.get_current_timezone())

    def clean_fecha_fin(self):
        """Mismo para fecha_fin, permitiendo vacío."""
        date = self.cleaned_data.get('fecha_fin')
        if date:
            dt = datetime.combine(date, time())
            return timezone.make_aware(dt, timezone.get_current_timezone())
        return None
MaletaFormSet = inlineformset_factory(
    Pedido,
    Maleta,
    fields=('guia', 'cantidad_pax'),
    widgets={
        'guia':         forms.TextInput(attrs={'class': 'form-control'}),
        'cantidad_pax': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
    },
    extra=0,
    can_delete=True,
)
class MaletaForm(forms.ModelForm):
    class Meta:
        model  = Maleta
        fields = ['guia', 'cantidad_pax']
        widgets = {
            'guia':         forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_pax': forms.NumberInput(attrs={'class': 'form-control'}),
        }



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


