from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Tarea, Pedido, Producto
from .forms import TareaForm, PedidoForm, ProductoForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
import json

# ========== TAREAS ==========

def cambiar_estado_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    tarea.completada = not tarea.completada
    tarea.save()
    return JsonResponse({'completada': tarea.completada})
class TareaListView( ListView):
    model = Tarea
    template_name = 'pedidos/tareas.html'
    context_object_name = 'tareas'
    
    def get_queryset(self):
        return Tarea.objects.all().order_by('-fecha_creacion')
    
class TareaCreateView(CreateView):
    model = Tarea
    fields = ['titulo', 'descripcion','fecha_especifica', 'completada']
    success_url = reverse_lazy('pedidos:tareas')
    def form_valid(self, form):
        form.save()
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
        return super().form_invalid(form)
    
class TareaUpdateView( UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'pedidos/tarea_form.html'
    success_url = reverse_lazy('tareas')

class TareaDeleteView( DeleteView):
    model = Tarea
    success_url = reverse_lazy('tareas')

# ========== PEDIDOS ==========
class PedidoListView( ListView):
    model = Pedido
    template_name = 'pedidos/pedidos_lista.html'
    context_object_name = 'pedidos'
class PedidoCreateView( CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedidos/pedido_form.html'
    success_url = reverse_lazy('pedidos:pedidos_lista')

# ========== PRODUCTOS ==========
class ProductoListView(ListView):
    model = Producto
    template_name = 'pedidos/productos_lista.html'

class ProductoUpdateView( UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'pedidos/producto_form.html'
    success_url = reverse_lazy('productos_lista')
    
# ========== Calendario ==========
class CalendarioView(TemplateView):
    template_name = 'pedidos/calendario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        eventos = []
        for tarea in Tarea.objects.all():
            if tarea.fecha_especifica:  
                eventos.append({
                    'title': tarea.titulo,
                    'start': tarea.fecha_especifica.isoformat(),
                    'description': tarea.descripcion,
                })
        context['eventos'] = json.dumps(eventos)
        return context