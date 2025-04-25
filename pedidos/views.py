from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Tarea, Pedido, Producto, StockControl
from .forms import TareaForm, PedidoForm, ProductoForm, StockControlFormSet, StockERForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics, serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

from .serializers import PedidoSerializer

# ========== TAREAS ==========

def cambiar_estado_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    tarea.completada = not tarea.completada
    tarea.save()
    return JsonResponse({'completada': tarea.completada})

class TareaListView(ListView):
    model = Tarea
    template_name = 'pedidos/tareas.html'
    context_object_name = 'tareas'

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
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'detail': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)

class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class RegistroAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ========== PEDIDOS ==========
class PedidoListView( ListView):
    model = Pedido
    template_name = 'pedidos/pedidos_lista.html'
    context_object_name = 'pedidos'


class PedidoCreateView(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

# ========== PRODUCTOS ==========
class ProductoListView(ListView):
    model = Producto
    template_name = 'pedidos/productos_lista.html'

class ProductoUpdateView( UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'pedidos/producto_form.html'
    success_url = reverse_lazy('productos_lista')
    
# ========== Control de Stock ==========

def stock_control_view(request):
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
