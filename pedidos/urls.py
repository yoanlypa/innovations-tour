from django.urls import path, include 
from . import views
from django.views.decorators.csrf import ensure_csrf_cookie

from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import (
    TareaListView, TareaCreateView, TareaUpdateView, TareaDeleteView, LoginAPIView, RegistroAPIView,
    PedidoListView, PedidoCreateView,ProductoListView, ProductoUpdateView,PasswordResetConfirmAPIView, PasswordResetRequestAPIView, SincronizarUsuarioAPIView, stock_control_view, agregar_stock,cambiar_estado_tarea,
)
app_name = 'pedidos'
urlpatterns = [
    # Tareas
    path('tareas/', TareaListView.as_view(), name='tareas'),
    path('tareas/nueva/', TareaCreateView.as_view(), name='tarea_nueva'),
    path('tareas/editar/<int:pk>/', TareaUpdateView.as_view(), name='tarea_editar'),
    path('tareas/eliminar/<int:pk>/', TareaDeleteView.as_view(), name='tarea_eliminar'),
    path('tareas/cambiar-estado/<int:tarea_id>/', cambiar_estado_tarea, name='cambiar_estado_tarea'),    # Pedidos
    path('pedidos/', PedidoListView.as_view(),  name='pedidos_lista'),
    path('api/pedidos/', PedidoCreateView.as_view(), name='api_pedidos'),
    path('pedidos/nuevo/', PedidoCreateView.as_view(), name='pedido_nuevo'),
    
    # Productos
    path('productos/', ProductoListView.as_view(), name='productos_lista'),
    path('productos/editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto_editar'),
    
    # Calendario
    #path('calendario/', CalendarioView.as_view(), name='calendario'),
    
    path('api/login/',    LoginAPIView.as_view(),               name='api_login'),
    path('api/registro/', RegistroAPIView.as_view(),            name='api_registro'),
    path('api/password-reset/',        PasswordResetRequestAPIView.as_view(), name='api_password_reset'),
    path('api/password-reset-confirm/',PasswordResetConfirmAPIView.as_view(), name='api_password_reset_confirm'),
    path('api/logout/', views.logout_view, name='logout_view'),
    path('api/pedidos/<int:pedido_id>/', views.datos_pedido_api, name='datos_pedido_api'),


    path('login/', auth_views.LoginView.as_view(template_name='pedidos/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='pedidos/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='pedidos/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='pedidos/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='pedidos/password_reset_complete.html'), name='password_reset_complete'),
    
    #Usuario
    path('api/sincronizar-usuario/', SincronizarUsuarioAPIView.as_view(), name='sincronizar_usuario'),
    # Stock Control
    path('stock/cargar_datos_pedido/',views.cargar_datos_pedido,name='cargar_datos_pedido'),
    path('stock/', views.stock_control_view, name='stock_control'),
    path('stock/agregar/', views.agregar_stock, name='agregar_stock'),
    path('stock/editar/<int:pk>/', views.editar_stock, name='editar_stock'),
    path('stock/eliminar/<int:pk>/', views.eliminar_stock, name='eliminar_stock'),
    path('stock/toggle-estado/<int:pk>/', views.toggle_estado_stock, name='toggle_estado_stock'),
    path('stock/exportar-csv/',        views.exportar_csv,     name='exportar_csv'),

]