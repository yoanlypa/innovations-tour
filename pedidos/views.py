from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db import IntegrityError
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.utils import timezone
from .models import Tarea, Pedido, Producto, StockControl, RegistroCliente
from .forms import TareaForm, PedidoForm, ProductoForm, StockControlFormSet, StockERForm
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .serializers import PedidoSerializer



class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'login'
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser



# ========== TAREAS ==========



@login_required
@require_http_methods(["POST"])
@ensure_csrf_cookie  # ← Asegura que la cookie CSRF esté presente
def cambiar_estado_tarea(request, tarea_id):
    try:
        tarea = Tarea.objects.get(id=tarea_id)
        # Verificar permisos del usuario
        if not request.user.is_staff and tarea.responsable != request.user:
            return JsonResponse(
                {'error': 'No tienes permiso para esta acción'}, 
                status=403
            )
        
        # Cambiar estado
        tarea.completada = not tarea.completada
        tarea.save()
        
        return JsonResponse({
            'completada': tarea.completada,
            'tarea_id': tarea_id
        })
        
    except Tarea.DoesNotExist:
        return JsonResponse({'error': 'Tarea no encontrada'}, status=404)
@method_decorator(ensure_csrf_cookie, name='dispatch')
class TareaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Tarea
    template_name = 'pedidos/tareas.html'
    context_object_name = 'tareas'
    
    def test_func(self):
        return self.request.user.is_staff
    def get_queryset(self):
        try:
            tareas = Tarea.objects.all().order_by('-fecha_creacion')
            return tareas
        except Exception as e:
            # En caso de error, lo capturamos y lo mostramos
            print(f"Error al obtener las tareas: {e}")
            return HttpResponse(f"Error al obtener las tareas: {e}", status=500)

    
class TareaCreateView(CreateView):
    model = Tarea
    fields = ['titulo', 'descripcion','fecha_especifica', 'completada']
    success_url = reverse_lazy('pedidos:tareas')  # Asegúrate que en urls.py uses name='tareas'
    template_name = 'pedidos/tarea_form.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'id': self.object.id,
                'titulo': self.object.titulo,
                'descripcion': self.object.descripcion,
                'fecha_creacion': self.object.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
                'completada': self.object.completada,
            }
            return JsonResponse(data)
        
        return response
    
class TareaUpdateView( UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'pedidos/tarea_form.html'
    success_url = reverse_lazy('pedidos:tareas')

class TareaDeleteView( DeleteView):
    model = Tarea
    success_url = reverse_lazy('pedidos:tareas')


# ========== LOGIN Y REGISTRO==========

User = get_user_model()

class RegistroAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '').strip()
        email    = request.data.get('email', '').strip()
        password = request.data.get('password', '')
        empresa  = request.data.get('empresa', '').strip()
        telefono = request.data.get('telefono', '').strip()

        # 1) Campos obligatorios
        if not username or not email or not password:
            return Response(
                {'detail': 'username, email y password son requeridos.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2) Validar longitud de contraseña
        if len(password) < 8:
            return Response(
                {'detail': 'La contraseña debe tener al menos 8 caracteres.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3) Validar unicidad manual
        if User.objects.filter(username=username).exists():
            return Response(
                {'detail': 'El nombre de usuario ya existe.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(email=email).exists():
            return Response(
                {'detail': 'El email ya está registrado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4) Intentar crear usuario y atrapar cualquier duplicado residual
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
        except IntegrityError:
            return Response(
                {'detail':'No se pudo crear el usuario. Username o email duplicado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 5) Guardar en tu modelo RegistroCliente
        RegistroCliente.objects.create(
            nombre_usuario=username,
            email=email,
            empresa=empresa,
            telefono=telefono
        )

        # 6) Generar token
        token = Token.objects.create(user=user)

        # 7) Enviar correo de notificación al admin
        send_mail(
            subject="🎉 Nuevo registro en Innovations Tours",
            message=(
                f"Nuevo usuario registrado:\n\n"
                f"Nombre: {username}\n"
                f"Email: {email}\n"
                f"Empresa: {empresa}\n"
                f"Teléfono: {telefono}\n"
                f"Fecha: {user.date_joined.strftime('%Y-%m-%d %H:%M')}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['pyoanly@gmail.com'],
            fail_silently=True,
        )

        # 8) Responder con token
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'detail': 'Faltan datos'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'detail': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)
        
def logout_view(request):
    logout(request)  
    return redirect('pedidos:tareas')

class PasswordResetRequestAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'detail':'Email requerido'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # No decimos si existe o no, por seguridad
            return Response({'detail':'Si el email existe, recibirás un enlace'}, status=status.HTTP_200_OK)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"{settings.FRONTEND_URL}/new-password/?uid={uid}&token={token}"
        subject = "🔑 Restablece tu contraseña"
        message = (
            f"Hola {user.username},\n\n"
            "Solicitaste restablecer tu contraseña. "
            f"Pulsa este enlace para crear una nueva:\n\n{reset_link}\n\n"
            "Si no lo solicitaste, ignora este correo."
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
        return Response({'detail':'En breve recibirás un email con instrucciones'}, status=status.HTTP_200_OK)

class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.data.get('uid')
        token  = request.data.get('token')
        new_password = request.data.get('new_password')
        if not uidb64 or not token or not new_password:
            return Response({'detail':'Faltan datos'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({'detail':'Enlace inválido'}, status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(user, token):
            return Response({'detail':'Token inválido o caducado'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({'detail':'Contraseña restablecida correctamente'}, status=status.HTTP_200_OK)
        
# ========== PEDIDOS ==========

class PedidoListView(StaffRequiredMixin, ListView):
    model = Pedido
    template_name = 'pedidos/pedidos_lista.html'
    context_object_name = 'pedidos'
    ordering = ['-fecha_inicio']

class PedidoCreateView(generics.ListCreateAPIView):
    queryset = Pedido.objects.all().order_by('-fecha_inicio')
    serializer_class = PedidoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 1) Guardamos en BD
        pedido = serializer.save(usuario=self.request.user)

        # 2) (Opcional) Enviar correo con datos del pedido
        details = [
            f"Empresa: {pedido.empresa}",
            f"Lugar entrega: {pedido.lugar_entrega}",
            f"Lugar recogida: {pedido.lugar_recogida or 'N/A'}",
            f"Fecha inicio: {pedido.fecha_inicio}",
            f"Fecha fin: {pedido.fecha_fin or 'N/A'}",
            f"Notas: {pedido.notas or 'Ninguna'}",
            "Maletas:"
        ]
        for m in pedido.maletas.all():
            details.append(f"  - Pax: {m.cantidad_pax}, Guía: {m.guia}")

        send_mail(
            subject=f"Nuevo pedido #{pedido.id}",
            message="\n".join(details),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['pyoanly@gmail.com'],
            fail_silently=True,
        )

# ========== PRODUCTOS ==========

class ProductoListView(StaffRequiredMixin,ListView):
    model = Producto
    template_name = 'pedidos/productos_lista.html'

class ProductoUpdateView( UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'pedidos/producto_form.html'
    success_url = reverse_lazy('productos_lista')
    
# ========== Control de Stock ==========

def stock_control_view(StaffRequiredMixin,request):
        stocks = StockControl.objects.all()  # o un filtrado específico
        return render(request, 'pedidos/stock_control.html', {'pedidos': stocks})

def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = StockControlFormSet(queryset=StockControl.objects.all())
        return context

def post(self, request, *args, **kwargs):
        formset = StockControlFormSet(request.POST)
        if formset.is_valid():
            formset.save()
        return self.get(request, *args, **kwargs)
    
def agregar_stock(request):
        if request.method == 'POST':
            StockControl.objects.create(
                pax=request.POST['pax'],
                lugar_er=request.POST['lugar_er'],
                excursion=request.POST['excursion'],
                guia=request.POST['guia'],
                fecha_er=request.POST['fecha_er'],
            )
        return redirect('pedidos:stock_control')

def editar_stock(request, pk):
    registro = get_object_or_404(StockControl, pk=pk)
    if request.method == "POST":
        form = StockERForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('pedidos:stock_control')
    else:
        form = StockERForm(instance=registro)
    return render(request, 'pedidos/editar_stock.html', {'form': form, 'registro': registro})

@csrf_exempt
def ajax_update_checklist(request):
    if request.method == "POST":
        record_id = request.POST.get("id")
        field = request.POST.get("field")
        value = request.POST.get("value") == "true"

        registro = get_object_or_404(StockControl, id=record_id)
        if field == "entregado":
            registro.entregado = value
        elif field == "recogido":
            registro.recogido = value
        else:
            return JsonResponse({"success": False, "error": "Campo no válido"})

        registro.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Método no permitido"})

@csrf_exempt
def eliminar_stock(request, pk):
    if request.method == "POST":
        registro = get_object_or_404(StockControl, pk=pk)
        try:
            registro.delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Método no permitido"})



class SincronizarUsuarioAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        nombre = data.get('nombre', '')

        if not username or not email:
            return Response({'error': 'Faltan datos requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(username=username, defaults={
            'email': email,
            'first_name': nombre
        })

        if not created:
            user.email = email
            user.first_name = nombre
            user.save()

        return Response({'mensaje': 'Usuario sincronizado correctamente'}, status=status.HTTP_200_OK)
# ========== login y registro django ==========
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cuenta creada correctamente. Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'pedidos/register.html', {'form': form})