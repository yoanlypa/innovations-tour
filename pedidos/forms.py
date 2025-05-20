from datetime import datetime, time

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.utils import timezone

from .models import Maleta, Pedido, Producto, Tarea
from .utils import convertir_fecha


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Usuario"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña"})
    )


class RegistroForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Nombre de usuario"}),
            "email": forms.EmailInput(attrs={"placeholder": "Correo electrónico"}),
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Usuario",
            "autocomplete": "username"
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Contraseña",
            "autocomplete": "current-password",
            "id": "id_login_password"
        })
    )

class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Usuario",
            "autocomplete": "username"
        })
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Correo electrónico",
            "autocomplete": "email"
        })
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Contraseña",
            "autocomplete": "new-password",
            "id": "id_register_password1"
        })
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Repite la contraseña",
            "autocomplete": "new-password",
            "id": "id_register_password2"
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo ya está en uso.")
        return email

    def save(self, commit=True):
        # Super guarda username y password, pero no siempre email
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
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
        fields = ["titulo", "descripcion", "prioridad", "completada"]


#
#
#
#
#
#
# ========== FORMULARIO DE PEDIDOS ==========
class PedidoForm(forms.ModelForm):
    # Para staff: permite editar también el estado
    class Meta:
        model = Pedido
        fields = [
            'empresa',
            'excursion',
            'lugar_entrega',
            'lugar_recogida',
            'fecha_inicio',
            'fecha_fin',
            'estado',   # unificado
        ]
        widgets = {
            'empresa':       forms.TextInput(attrs={'class': 'form-control'}),
            'excursion':     forms.TextInput(attrs={'class': 'form-control'}),
            'lugar_entrega': forms.TextInput(attrs={'class': 'form-control'}),
            'lugar_recogida':forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio':  forms.DateInput(attrs={'type': 'date',  'class': 'form-control'}),
            'fecha_fin':     forms.DateInput(attrs={'type': 'date',  'class': 'form-control'}),
            'estado':        forms.Select(attrs={'class': 'form-select'}),
        }

from .models import Maleta, Pedido


from django import forms
from .models import Pedido
# pedidos/forms.py

from django import forms
from .models import Pedido

class PedidoFormCliente(forms.ModelForm):
    # El cliente elige aquí sólo entre “Pagado” y “Pendiente de pago”
    estado = forms.ChoiceField(
        label="Estado de pago",
        choices=[
            ('pagado', 'Pagado'),
            ('pendiente_pago', 'Pendiente de pago'),
        ],
        widget=forms.RadioSelect,
        initial='pagado',
    )

    class Meta:
        model = Pedido
        fields = [
            'empresa',
            'excursion',
            'lugar_entrega',
            'lugar_recogida',
            'fecha_inicio',
            'fecha_fin',
            'estado',     # tu único campo de estado
        ]
        widgets = {
            'empresa':        forms.TextInput(attrs={'class': 'form-control'}),
            'excursion':      forms.TextInput(attrs={'class': 'form-control'}),
            'lugar_entrega':  forms.TextInput(attrs={'class': 'form-control'}),
            'lugar_recogida': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio':   forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin':      forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class PedidoForm(forms.ModelForm):
    # Para staff: puede editar cualquier estado
    class Meta:
        model = Pedido
        fields = [
            'empresa',
            'excursion',
            'lugar_entrega',
            'lugar_recogida',
            'fecha_inicio',
            'fecha_fin',
            'estado',     # mismo campo unificado
        ]
        widgets = {
            'empresa':        forms.TextInput(attrs={'class': 'form-control'}),
            'excursion':      forms.TextInput(attrs={'class': 'form-control'}),
            'lugar_entrega':  forms.TextInput(attrs={'class': 'form-control'}),
            'lugar_recogida': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio':   forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin':      forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'estado':         forms.Select(attrs={'class': 'form-select'}),
        }

    # ──────────────────── Limpieza de campos individuales ────────────────────
    def _make_aware(self, date_obj):
        """Convierte un date en datetime aware (00:00)."""
        dt = datetime.combine(date_obj, time())
        return timezone.make_aware(dt, timezone.get_current_timezone())

    def clean_fecha_inicio(self):
        date = self.cleaned_data["fecha_inicio"]
        return self._make_aware(date)

    def clean_fecha_fin(self):
        date = self.cleaned_data.get("fecha_fin")
        return self._make_aware(date) if date else None

    # ──────────────────── Validación cruzada ────────────────────
    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get("fecha_inicio")
        fin = cleaned.get("fecha_fin")

        if inicio and fin and inicio > fin:
            raise ValidationError(
                {
                    "fecha_fin": "La fecha de fin debe ser igual o posterior a la fecha de inicio."
                }
            )
        return cleaned


# ──────────────────── Formset de maletas ────────────────────
MaletaFormSet = inlineformset_factory(
    Pedido,
    Maleta,
    fields=("guia", "cantidad_pax"),
    widgets={
        "guia": forms.TextInput(attrs={"class": "form-control"}),
        "cantidad_pax": forms.NumberInput(
            attrs={"class": "form-control", "min": 1}
        ),
    },
    extra=1,
    can_delete=True,
)

class MaletaForm(forms.ModelForm):
    class Meta:
        model = Maleta
        fields = ["guia", "cantidad_pax"]
        widgets = {
            "guia": forms.TextInput(attrs={"class": "form-control"}),
            "cantidad_pax": forms.NumberInput(attrs={"class": "form-control"}),
        }


#
#
#
#
# ========== FORMULARIO DE PRODUCTOS ==========
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "cantidad", "almacen"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control"}),
            "almacen": forms.TextInput(attrs={"class": "form-control"}),
        }
