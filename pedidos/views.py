import csv
from datetime import datetime, time

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm as LoginForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)

from .forms import (CustomLoginForm, CustomRegisterForm, MaletaFormSet,
                    PedidoForm, PedidoFormCliente, ProductoForm, RegistroForm,
                    TareaForm)
from .models import Maleta, Pedido, Producto, RegistroCliente, Tarea
from .serializers import PedidoSerializer


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy("pedidos:acceso")

    def test_func(self):
        return self.request.user.is_staff


class HomeView(TemplateView):
    """
    Portada pública: sólo muestra la landing.
    No redirigimos aunque el usuario esté logueado; así puede volver
    a la home si quiere. Si prefieres redirigir, dímelo y cambiamos dispatch().
    """

    template_name = "pedidos/home.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(
                "pedidos:pedidos_lista"
                if request.user.is_staff
                else "pedidos:mis_pedidos"
            )
        return super().dispatch(request, *args, **kwargs)


#
#
#
#
#
#
# ========== TAREAS ==========


@require_http_methods(["POST"])
@login_required
def cambiar_estado_tarea(request, tarea_id):
    tarea = Tarea.objects.get(id=tarea_id)
    tarea.completada = not tarea.completada
    tarea.save()
    return JsonResponse({"completada": tarea.completada, "tarea_id": tarea_id})


@method_decorator(ensure_csrf_cookie, name="dispatch")
class TareaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Tarea
    template_name = "pedidos/tareas.html"
    context_object_name = "tareas"

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        try:
            tareas = Tarea.objects.all().order_by("-fecha_creacion")
            return tareas
        except Exception as e:
            # En caso de error, lo capturamos y lo mostramos
            print(f"Error al obtener las tareas: {e}")
            return HttpResponse(f"Error al obtener las tareas: {e}", status=500)


class TareaCreateView(CreateView):
    model = Tarea
    fields = ["titulo", "descripcion", "fecha_especifica", "completada"]
    success_url = reverse_lazy(
        "pedidos:tareas"
    )  # Asegúrate que en urls.py uses name='tareas'
    template_name = "pedidos/tarea_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            data = {
                "id": self.object.id,
                "titulo": self.object.titulo,
                "descripcion": self.object.descripcion,
                "fecha_creacion": self.object.fecha_creacion.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "completada": self.object.completada,
            }
            return JsonResponse(data)

        return response


class TareaUpdateView(UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = "pedidos/tarea_form.html"
    success_url = reverse_lazy("pedidos:tareas")


class TareaDeleteView(DeleteView):
    model = Tarea
    success_url = reverse_lazy("pedidos:tareas")


from django.contrib.auth import authenticate, login, logout
#
#
#
#
#
#
#
#
# ========== LOGIN Y REGISTRO==========
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import redirect, render


@csrf_protect
def acceso_view(request):
    # Formularios vacíos para la primera carga
    login_form = CustomLoginForm()
    register_form = CustomRegisterForm()
    mode = request.POST.get("mode", "login")  # modo activo (login / register / reset)

    if request.method == "POST":
        # ---------- LOGIN ----------
        if mode == "login":
            login_form = CustomLoginForm(request, data=request.POST)
            if login_form.is_valid():
                login(request, login_form.get_user())

                next_url = request.POST.get("next") or request.GET.get("next")
                if next_url:
                    return redirect(next_url)

                return redirect(
                    "pedidos:pedidos_lista"
                    if request.user.is_staff
                    else "pedidos:mis_pedidos"
                )
            messages.error(request, "Credenciales inválidas.")
    # ---------- REGISTRO ----------
    elif mode == "register":
        register_form = CustomRegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            RegistroCliente.objects.create(
                nombre_usuario=user.username, email=user.email
            )
            login(request, user)
            return redirect("pedidos:mis_pedidos")
        messages.error(request, "Corrige los errores del formulario.")

    # ---------- RESET ----------
    elif mode == "reset":
        email = request.POST.get("email")
        # … lógica de envío de enlace (omitida aquí) …
        messages.success(request, "Te enviamos un enlace a tu correo.")

    context = {
        "login_form": login_form,
        "register_form": register_form,
        "mode": mode,  # para que la plantilla sepa qué pestaña mostrar
    }
    return render(request, "pedidos/acceso.html", context)


def logout_view(request):
    logout(request)
    return redirect("pedidos:acceso")


#
#
#
#
#
# ========== PEDIDOS ==========


@staff_member_required
def pedidos_lista_view(request):
    pedidos = Pedido.objects.all().order_by("-fecha_inicio")
    return render(request, "pedidos/pedidos_lista.html", {"pedidos": pedidos})


# ---------- NUEVO PEDIDO CLIENTE ----------

from .forms import MaletaFormSet, PedidoFormCliente
from .models import Pedido


@login_required
def pedido_nuevo_cliente_view(request):
    if request.method == "POST":
        form = PedidoFormCliente(request.POST)
        formset = MaletaFormSet(request.POST, prefix="maleta")
        if form.is_valid() and formset.is_valid():
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            pedido.save()
            formset.instance = pedido
            formset.save()

            if request.GET.get("embed") == "1":
                # recarga la ventana padre y cierra modal
                return HttpResponse("<script>window.parent.location.reload();</script>")

            messages.success(request, "✅ Pedido creado correctamente.")
            return redirect("pedidos:mis_pedidos")
        messages.error(request, "Corrige los errores del formulario.")
    else:
        form = PedidoFormCliente()
        formset = MaletaFormSet(prefix="maleta")

    template = (
        "pedidos/pedido_nuevo_cliente_modal.html"
        if request.GET.get("embed") == "1"
        else "pedidos/pedido_nuevo_cliente.html"
    )
    return render(request, template, {"form": form, "formset": formset})


@login_required
def pedido_editar_cliente_view(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if pedido.usuario != request.user:
        raise Http404()

    if request.method == "POST":
        form = PedidoFormCliente(request.POST, instance=pedido)
        formset = MaletaFormSet(request.POST, instance=pedido, prefix="maleta")
        if form.is_valid() and formset.is_valid():
            pedido = form.save(commit=False)
            pedido.save()
            formset.save()
            print("── POST ──", request.POST.dict())
            # views.py – dentro del branch POST de pedido_editar_cliente_view
            print("VALID?", form.is_valid(), formset.is_valid())
            print("Form errors:", form.errors)
            print("Formset errors:", formset.non_form_errors(), [f.errors for f in formset])
            messages.success(request, "✅ Pedido actualizado correctamente.")
            return redirect("pedidos:mis_pedidos")
        messages.error(request, "Corrige los errores del formulario.")
    else:
        form = PedidoFormCliente(instance=pedido)
        formset = MaletaFormSet(instance=pedido, prefix="maleta")

    return render(
        request,
        "pedidos/pedido_nuevo_cliente.html",
        {"form": form, "formset": formset, "es_edicion": True, "pedido": pedido},
    )


@login_required
def pedido_nuevo_view(request):
    form = PedidoForm(request.POST or None)
    formset = MaletaFormSet(request.POST or None, prefix="maleta")

    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            pedido.save()
            form.save_m2m()
            formset.instance = pedido
            formset.save()

            # Enlace directo para editar
            enlace_edicion = request.build_absolute_uri(
                reverse("pedidos:pedido_editar", args=[pedido.id])
            )

            # Enviar correo
            detalles = [
                f"📢 *Nuevo pedido registrado*",
                f"🏢 Empresa: {pedido.empresa}",
                f"📅 Fecha inicio: {pedido.fecha_inicio.strftime('%d/%m/%Y')}",
                f"🧭 Excursión: {pedido.excursion or '—'}",
                f"👤 Usuario: {pedido.usuario.username}",
                f"🔗 Editar pedido: {enlace_edicion}",
            ]

            send_mail(
                subject=f"Nuevo pedido #{pedido.id}",
                message="\n".join(detalles),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["pyoanly@gmail.com"],  # Puedes agregar más emails aquí
                fail_silently=True,
            )
            messages.success(request, "Pedido registrado satisfactoriamente.")
            # redirección según botón
            if request.POST.get("action") == "guardar_otro":
                return redirect("pedidos:pedido_nuevo")
            return redirect("pedidos:mis_pedidos")
        else:
            messages.error(request, "Hay errores en el formulario.")

    return render(
        request,
        "pedidos/pedido_form.html",
        {
            "form": form,
            "formset": formset,
            "pedido": None,
        },
    )


@staff_member_required
def pedido_editar_view(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == "POST":
        print(
            "📥 LLEGÓ POST A pedido_editar_view con data:", request.POST
        )  # <<-- DEBUG
        form = PedidoForm(request.POST, instance=pedido)
        formset = MaletaFormSet(request.POST, instance=pedido, prefix="maleta")

        if form.is_valid() and formset.is_valid():
            print("✅ form válido, guardando pedido...")
            form.save()
            formset.save()
            messages.success(request, "Pedido actualizado correctamente.")
            return redirect("pedidos:pedidos_lista")
        else:
            print("❌ ERRORES FORM:", form.errors, formset.errors)
            messages.error(request, "Hay errores al guardar los cambios.")

    else:
        form = PedidoForm(instance=pedido)
        formset = MaletaFormSet(instance=pedido, prefix="maleta")

    return render(
        request,
        "pedidos/pedido_form.html",
        {"form": form, "formset": formset, "pedido": pedido},
    )


@require_GET
@staff_member_required
def cargar_datos_pedido(request):
    pedido_id = request.GET.get("pedido_id")
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    maletas = pedido.maletas.all()

    data = {
        "empresa": pedido.empresa,
        "usuario": pedido.usuario.username,
        "excursion": pedido.excursion or "",
        "lugar_entrega": pedido.lugar_entrega or "",
        "lugar_recogida": pedido.lugar_recogida or "",
        "fecha_inicio": pedido.fecha_inicio.isoformat() if pedido.fecha_inicio else "",
        "fecha_fin": pedido.fecha_fin.isoformat() if pedido.fecha_fin else "",
        "estado_cliente": pedido.estado_cliente,
        "estado_equipo": pedido.estado_equipo,
        "notas": pedido.notas or "",
        "maletas": [{"guia": m.guia, "cantidad_pax": m.cantidad_pax} for m in maletas],
    }
    return JsonResponse(data)


@login_required
def pedidos_mios_view(request):
    pedidos = (
        Pedido.objects.filter(usuario=request.user)
        .prefetch_related("maletas")  # evita consultas N+1
        .order_by("-fecha_inicio")
    )
    return render(request, "pedidos/pedidos_mios.html", {"pedidos": pedidos})


#
#
#
#
