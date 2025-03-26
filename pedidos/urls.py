from django.urls import path, include
from . import views

app_name = 'pedidos'

urlpatterns = [
    # Pedidos 
    path('', views.lista_pedidos, name='lista_pedidos'), 
    path('editar/<int:pk>/', views.editar_pedido, name='editar_pedido'),

    # Tareas
    path('tareas/', views.lista_tareas, name='lista_tareas'),
    path('tareas/agregar/', views.agregar_tarea, name='agregar_tarea'),
    
    # Stock
    path('stock/', views.control_stock, name='control_stock'),    
    
    # Agenda path('agenda/', views.agenda, name='agenda'),
    path('calendario/', views.calendario_pedidos, name='calendario'),

]