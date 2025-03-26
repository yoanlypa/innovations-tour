from django.shortcuts import render, redirect, get_object_or_404
from .models import Pedido, Producto, Tarea, Nota
from .forms import PedidoForm, TareaForm, NotaForm
from django.views.decorators.http import require_POST
from django.utils import timezone

def lista_pedidos(request):
    pedidos = Pedido.objects.all().order_by('fecha_inicio')
    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos})

# Vista para editar pedidos
def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('pedidos:lista_pedidos')
    else:
        form = PedidoForm(instance=pedido)
    return render(request, 'pedidos/editar_pedido.html', {'form': form})

@require_POST
def cambiar_estado(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = request.POST.get('estado')
    pedido.save()
    return redirect('pedidos_list')

def calendario_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedidos/calendario.html', {'pedidos': pedidos})

def control_stock(request):
    productos = Producto.objects.all()
    return render(request, 'pedidos/stock.html', {'productos': productos})

@require_POST
def ajustar_stock(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    accion = request.POST.get('accion')
    if accion == 'sumar':
        producto.cantidad += 1
    elif accion == 'restar' and producto.cantidad > 0:
        producto.cantidad -= 1
    producto.save()
    return redirect('control_stock')

def tareas(request):
    tareas_hoy = Tarea.objects.filter(fecha=timezone.now().date(), realizada=False)
    tareas_futuras = Tarea.objects.filter(fecha__gt=timezone.now().date())
    return render(request, 'pedidos/tareas.html', {
        'tareas_hoy': tareas_hoy,
        'tareas_futuras': tareas_futuras
    })
def agregar_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedidos:lista_tareas')
    else:
        form = TareaForm()
    return render(request, 'pedidos/agregar_tarea.html', {'form': form})

def lista_tareas(request):
    tareas = Tarea.objects.all().order_by("-fecha")
    return render(request, 'pedidos/tareas.html', {'tareas': tareas})