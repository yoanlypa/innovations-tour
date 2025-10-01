# pedidos/views.py
import csv
from datetime import datetime, time

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from django_filters.views import FilterView
from .filters import PedidoFilter

from .forms import (
    CustomLoginForm,
    CustomRegisterForm,
    ServicioFormSet,
    PedidoForm,
    PedidoFormCliente,
    TareaForm,
)
from .models import Pedido, RegistroCliente, Tarea, Servicio

#
# 
# 
# 
# ——————— Vistas back-end para acciones masivas ———————
@staff_member_required
@require_POST
def bulk_delete(request):
    ids = request.POST.getlist('ids[]') or request.POST.getlist('ids')
    Pedido.objects.filter(pk__in=ids).delete()
    return JsonResponse({'ok': True})

@staff_member_required
@require_POST
def bulk_change_estado(request):
    ids    = request.POST.getlist('ids[]') or request.POST.getlist('ids')
    estado = request.POST['estado']
    # valida que 'estado' sea uno de los permitidos
    if estado not in dict(Pedido.ESTADOS):
        return JsonResponse({'error':'Estado inválido'}, status=400)
    Pedido.objects.filter(pk__in=ids).update(estado=estado)
    return JsonResponse({'ok': True})

# 
# 
# 
# 
# 
# 
# ——————— Home ———————

class HomeView(TemplateView):
    template_name = "pedidos/home.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("pedidos:pedidos_lista" if request.user.is_staff else "pedidos:mis_pedidos")
        return super().dispatch(request, *args, **kwargs)


# 
# 
# 
# 
# 
# ——————— Tareas ———————

@require_http_methods(["POST"])
@login_required
def cambiar_estado_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
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
        return Tarea.objects.all().order_by("-fecha_creacion")


class TareaCreateView(CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = "pedidos/tarea_form.html"
    success_url = reverse_lazy("pedidos:tareas")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "id": self.object.id,
                "titulo": self.object.titulo,
                "descripcion": self.object.descripcion,
                "fecha_creacion": self.object.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
                "completada": self.object.completada,
            })
        return response


class TareaUpdateView(UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = "pedidos/tarea_form.html"
    success_url = reverse_lazy("pedidos:tareas")


class TareaDeleteView(DeleteView):
    model = Tarea
    success_url = reverse_lazy("pedidos:tareas")


#
# 
# 
# 
# 
# ——————— Acceso / Registro ———————

@csrf_protect
def acceso_view(request):
    mode = request.POST.get("mode") or request.GET.get("mode", "login")
    login_form = CustomLoginForm()
    register_form = CustomRegisterForm()

    if request.method == "POST":
        if mode == "login":
            login_form = CustomLoginForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                next_url = request.POST.get("next") or request.GET.get("next")
                return redirect(next_url) if next_url else redirect(
                    "pedidos:pedidos_lista" if user.is_staff else "pedidos:mis_pedidos"
                )
            messages.error(request, "Credenciales inválidas.")

        elif mode == "register":
            register_form = CustomRegisterForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                RegistroCliente.objects.create(
                    nombre_usuario=user.username,
                    email=user.email
                )
                login(request, user)
                return redirect("pedidos:mis_pedidos")
            messages.error(request, "Corrige los errores del formulario.")

        elif mode == "reset":
            # lógica envío enlace…
            messages.success(request, "Te enviamos un enlace a tu correo.")

    return render(request, "pedidos/acceso.html", {
        "login_form": login_form,
        "register_form": register_form,
        "mode": mode,
    })


def logout_view(request):
    logout(request)
    return redirect("pedidos:acceso")


#
# 
# 
# 
# 
# ——————— Pedidos ———————

class PedidoListView(FilterView):
    model = Pedido
    template_name = 'pedidos/pedidos_lista.html'
    context_object_name = 'pedidos'
    filterset_class = PedidoFilter
    paginate_by = 25

@staff_member_required
@require_POST
def cambiar_estado(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    # Define el orden de la máquina de estados
    siguiente = {
        'pendiente_pago': 'pagado',
        'pagado':         'aprobado',
        'aprobado':       'entregado',
        'entregado':      'recogido',
        'recogido':       'recogido',  # permanece en recogido si ya está en el último
    }[pedido.estado]
    pedido.estado = siguiente
    pedido.save()
    return JsonResponse({
        'nuevo':    siguiente,
        'display':  pedido.get_estado_display(),
        # opcional: clases para el badge o el botón
        'badge_class': {
            'pendiente_pago': 'btn-outline-secondary',
            'pagado':         'btn-success',
            'aprobado':       'btn-primary',
            'entregado':      'btn-info text-dark',
            'recogido':       'btn-dark',
        }[siguiente]
    })
    
@staff_member_required
def pedidos_lista_view(request):
    pedidos = Pedido.objects.all().order_by("-fecha_inicio")
    return render(request, "pedidos/pedidos_lista.html", {"pedidos": pedidos})


@staff_member_required
@require_POST
def pedido_eliminar_view(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    pedido.delete()
    messages.success(request, "Pedido eliminado correctamente.")
    return redirect("pedidos:pedidos_lista")


@staff_member_required
@require_POST
def pedido_eliminar_masivo_view(request):
    ids = request.POST.getlist("selected_ids")
    if not ids:
        messages.error(request, "No seleccionaste ningún pedido.")
    else:
        qs = Pedido.objects.filter(pk__in=ids)
        count = qs.count()
        qs.delete()
        messages.success(request, f"Se eliminaron {count} pedidos seleccionados.")
    return redirect("pedidos:pedidos_lista")


@login_required
def pedidos_mios_view(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by("-fecha_inicio")
    return render(request, "pedidos/pedidos_mios.html", {"pedidos": pedidos})


@staff_member_required
def pedidos_lista_view(request):
    pedidos = Pedido.objects.all().order_by("-fecha_inicio")
    return render(request, "pedidos/pedidos_lista.html", {"pedidos": pedidos})


@login_required
def pedido_nuevo_cliente_view(request):
    # Detecta si estamos en modo modal (embed)
    embed = request.GET.get('embed') == '1' or request.POST.get('embed') == '1'

    # Instanciamos formulario y formset de servicios
    form = PedidoFormCliente(request.POST or None)
    servicio_formset = ServicioFormSet(request.POST or None, prefix='servicio')

    if request.method == "POST":
        if form.is_valid() and servicio_formset.is_valid():
            # 1) Guardamos el pedido
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            pedido.save()

            # 2) Asociamos y guardamos los servicios
            servicio_formset.instance = pedido
            servicio_formset.save()

            # 3) Si estamos en el modal, recarga la ventana padre
            if embed:
                return HttpResponse(
                    "<script>window.parent.location.reload();</script>"
                )

            # 4) modo normal: mensaje y redirect
            messages.success(request, "✅ Pedido creado correctamente.")
            return redirect("pedidos:mis_pedidos")
        else:
            messages.error(request, "Por favor corrige los errores.")

    # Elegimos plantilla según embed
    template = (
        "pedidos/pedido_nuevo_cliente_modal.html"
        if embed
        else "pedidos/pedido_nuevo_cliente.html"
    )
    return render(request, template, {
        "form": form,
        "formset": servicio_formset,
        "es_edicion": False,
        # Pasamos embed al template para incluir hidden si hace falta
        "embed": embed,
    })

@login_required
def pedido_editar_cliente_view(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if pedido.usuario != request.user:
        raise Http404()

    # Aquí siempre usamos PedidoFormCliente, con sólo dos estados
    FormClass = PedidoFormCliente
    if request.method == "POST":
        form    = FormClass(request.POST, instance=pedido)
        formset = ServicioFormSet(request.POST, instance=pedido, prefix='servicio')
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "✅ Pedido actualizado correctamente.")
            return redirect("pedidos:mis_pedidos")
        messages.error(request, "Corrige los errores del formulario.")
    else:
        form    = FormClass(instance=pedido)
        formset = ServicioFormSet(instance=pedido, prefix='servicio')

    return render(request, "pedidos/pedido_nuevo_cliente.html", {
        "form": form,
        "formset": formset,
        "es_edicion": True,
        "pedido": pedido, 
    })

@staff_member_required
def pedido_nuevo_view(request):
    form = PedidoForm(request.POST or None)
    formset = ServicioFormSet(
        request.POST or None, prefix="servicio"
    )
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        pedido = form.save(commit=False)
        pedido.usuario = request.user
        pedido.save()
        form.save_m2m()
        formset.instance = pedido
        formset.save()

        enlace = request.build_absolute_uri(reverse("pedidos:pedido_editar", args=[pedido.id]))
        send_mail(
            subject=f"Nuevo pedido #{pedido.id}",
            message=f"Nuevo pedido registrado. Editar: {enlace}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["pyoanly@gmail.com"],
            fail_silently=True,
        )
        messages.success(request, "Pedido registrado satisfactoriamente.")
        if request.POST.get("action") == "guardar_otro":
            return redirect("pedidos:pedido_nuevo")
        return redirect("pedidos:mis_pedidos")

    return render(request, "pedidos/pedido_form.html", {"form": form, "formset": formset, "pedido": None})


@login_required
def pedido_editar_view(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == "POST":
        form = PedidoForm(request.POST, instance=pedido)
        formset = ServicioFormSet(request.POST, instance=pedido, prefix="servicio")
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Pedido actualizado correctamente.")
            return redirect("pedidos:pedidos_lista")
        messages.error(request, "Hay errores al guardar los cambios.")
    else:
        form = PedidoForm(instance=pedido)
        formset = ServicioFormSet(instance=pedido, prefix="servicio")

    return render(request, "pedidos/pedido_form.html", {"form": form, "formset": formset, "pedido": pedido})


@require_GET
@login_required
def cargar_datos_pedido(request):
    pedido_id = request.GET.get("pedido_id")
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    servicios = pedido.servicios_linea.all()
    data = {
        "empresa": pedido.empresa,
        "usuario": pedido.usuario.username,
        "lugar_entrega": pedido.lugar_entrega or "",
        "lugar_recogida": pedido.lugar_recogida or "",
        "fecha_inicio": pedido.fecha_inicio.isoformat() if pedido.fecha_inicio else "",
        "fecha_fin": pedido.fecha_fin.isoformat() if pedido.fecha_fin else "",
        "estado": pedido.ESTADOS[pedido.estado],
        "notas": pedido.notas or "",
        "servicios": [{"excursion": s.excursion, "pax": s.pax, "emisores": s.emisores, "guia": s.guia, "lugar_entrega": s.lugar_entrega, "bono": s.bono} for s in servicios],
    }
    return JsonResponse(data)


@login_required
def pedidos_mios_view(request):
    pedidos = (
        Pedido.objects.filter(usuario=request.user)
        .prefetch_related("servicios_linea")
        .order_by("-fecha_inicio")
    )
    return render(request, "pedidos/pedidos_mios.html", {"pedidos": pedidos})

def _parse_dt(value: str):
    if not value:
        return None
    try:
        # ISO → aware
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt)
        return dt
    except Exception:
        return None

class IsAuthenticatedAndOwnerOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return getattr(obj, "usuario_id", None) == request.user.id

class PedidoOpsViewSet(viewsets.ModelViewSet):
    """
    /api/ops/pedidos/ → listado para operaciones de trabajadores
    Staff: ve todos; no staff: ve los propios (usuario=request.user)
    Filtros: ?status=pagado,entregado&date_from=ISO&date_to=ISO
    """
    serializer_class = PedidoOpsSerializer
    permission_classes = [IsAuthenticatedAndOwnerOrStaff]

    def get_queryset(self):
        qs = Pedido.objects.all().order_by("-fecha_modificacion")
        user = self.request.user
        if not user.is_staff:
            qs = qs.filter(usuario=user)

        status_param = self.request.query_params.get("status")
        if status_param:
            parts = [p.strip() for p in status_param.split(",") if p.strip()]
            if parts:
                qs = qs.filter(estado__in=parts)

        date_from = _parse_dt(self.request.query_params.get("date_from"))
        date_to = _parse_dt(self.request.query_params.get("date_to"))
        if date_from:
            qs = qs.filter(fecha_inicio__gte=date_from)
        if date_to:
            qs = qs.filter(fecha_inicio__lte=date_to)

        return qs

    @action(detail=True, methods=["post"])
    def delivered(self, request, pk=None):
        obj = self.get_object()
        obj.estado = "entregado"
        obj.entregado = True
        obj.save(update_fields=["estado", "entregado", "fecha_modificacion"])
        return Response({"ok": True, "status": "entregado", "id": obj.id})

    @action(detail=True, methods=["post"])
    def collected(self, request, pk=None):
        obj = self.get_object()
        obj.estado = "recogido"
        obj.recogido = True
        obj.save(update_fields=["estado", "recogido", "fecha_modificacion"])
        return Response({"ok": True, "status": "recogido", "id": obj.id})

# ---- Perfil sencillo para saber si es staff ----
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def me_view(request):
    u = request.user
    return Response({
        "id": u.id,
        "username": getattr(u, "username", ""),
        "email": getattr(u, "email", ""),
        "is_staff": getattr(u, "is_staff", False),
    })
