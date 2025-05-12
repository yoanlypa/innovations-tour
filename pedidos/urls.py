from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'pedidos'

urlpatterns = [
    # TAREAS
    path('tareas/', views.TareaListView.as_view(), name='tareas'),
    path('tareas/nueva/', views.TareaCreateView.as_view(), name='tarea_nueva'),
    path('tareas/editar/<int:pk>/', views.TareaUpdateView.as_view(), name='tarea_editar'),
    path('tareas/eliminar/<int:pk>/', views.TareaDeleteView.as_view(), name='tarea_eliminar'),
    path('tareas/cambiar-estado/<int:tarea_id>/', views.cambiar_estado_tarea, name='cambiar_estado_tarea'),

    # PEDIDOS (nuevo flujo unificado)
    path('', views.pedidos_lista_view, name='pedidos_lista'),
    path('nuevo/', views.pedido_nuevo_view, name='pedido_nuevo'),
    path('editar/<int:pk>/', views.pedido_editar_view, name='pedido_editar'),
    path('cargar_datos/', views.cargar_datos_pedido, name='cargar_datos_pedido'),
    path('mis-pedidos/', views.pedidos_mios_view, name='mis_pedidos'),

    # LOGIN / REGISTRO
    path('acceso/', views.auth_combined_view, name='login'),
    
    # ————— Productos —————
    path('productos/', views.ProductoListView.as_view(), name='productos_lista'),
    path('productos/editar/<int:pk>/', views.ProductoUpdateView.as_view(), name='producto_editar'),
    
    # PASSWORD RESET
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='pedidos/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='pedidos/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='pedidos/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='pedidos/password_reset_complete.html'), name='password_reset_complete'),

    # API / Sincronización
    # path('api/sincronizar-usuario/', views.SincronizarUsuarioAPIView.as_view(), name='sincronizar_usuario'),
    # 
    
]
