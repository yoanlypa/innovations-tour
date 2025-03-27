from django.urls import path, include 
from . import views
from .views import (
    TareaListView, TareaCreateView, TareaUpdateView, TareaDeleteView,
    PedidoListView, PedidoCreateView,
    ProductoListView, ProductoUpdateView, CalendarioView
)
app_name = 'pedidos'
urlpatterns = [
    # Tareas
    path('tareas/', TareaListView.as_view(), name='tareas'),
    path('tareas/nueva/', TareaCreateView.as_view(), name='tarea_nueva'),
    path('tareas/editar/<int:pk>/', TareaUpdateView.as_view(), name='tarea_editar'),
    path('tareas/eliminar/<int:pk>/', TareaDeleteView.as_view(), name='tarea_eliminar'),
    path('tareas/cambiar-estado/<int:tarea_id>/', views.cambiar_estado_tarea, name='cambiar_estado'),

    # Pedidos
    
    path('pedidos/', PedidoListView.as_view(), name='pedidos_lista'),
    path('pedidos/nuevo/', PedidoCreateView.as_view(), name='pedido_nuevo'),
    
    # Productos
    path('productos/', ProductoListView.as_view(), name='productos_lista'),
    path('productos/editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto_editar'),
    
    # Calendario
    path('calendario/', CalendarioView.as_view(), name='calendario'),
]