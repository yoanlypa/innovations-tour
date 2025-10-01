from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import HomeView, acceso_view, logout_view, pedido_editar_cliente_view, pedido_nuevo_cliente_view, PedidoOpsViewSet, me_view

app_name = "pedidos"
router = DefaultRouter()
router.register(r"ops/pedidos", PedidoOpsViewSet, basename="ops-pedidos")

urlpatterns = [
    # TAREAS

    path("tareas/", views.TareaListView.as_view(), name="tareas"),
    path("tareas/nueva/", views.TareaCreateView.as_view(), name="tarea_nueva"),
    path("tareas/editar/<int:pk>/", views.TareaUpdateView.as_view(), name="tarea_editar"),
    path("tareas/eliminar/<int:pk>/",views.TareaDeleteView.as_view(),name="tarea_eliminar",),
    path("tareas/cambiar-estado/<int:tarea_id>/",views.cambiar_estado_tarea,name="cambiar_estado_tarea",),
    
    # PEDIDOS 
    path("", HomeView.as_view(), name="home"),
    
   
    # Staff: lista de pedidos + eliminar
    path("pedidos/", views.pedidos_lista_view, name="pedidos_lista"),
    path("nuevo/", views.pedido_nuevo_view, name="pedido_nuevo"),
    path("editar/<int:pk>/", views.pedido_editar_view, name="pedido_editar"),
    path("cargar_datos/", views.cargar_datos_pedido, name="cargar_datos_pedido"),
    path("pedidos/eliminar/<int:pk>/", views.pedido_eliminar_view, name="pedido_eliminar"),
    path("pedidos/eliminar-multiple/", views.pedido_eliminar_masivo_view, name="pedido_eliminar_masivo"),
    path('pedidos/ajax/cambiar-estado/<int:pk>/',views.cambiar_estado,name='cambiar_estado'),
    path('bulk-delete/',       views.bulk_delete,         name='bulk_delete'),
    path('bulk-change-estado/', views.bulk_change_estado, name='bulk_change_estado'),

    # Cliente: mis pedidos
    path("mis-pedidos/", views.pedidos_mios_view, name="mis_pedidos"),
    path("mis-pedidos/nuevo/",views.pedido_nuevo_cliente_view,name="pedido_nuevo_cliente",),
    path('mis-pedidos/editar/<int:pk>/', views.pedido_editar_cliente_view, name='pedido_editar_cliente'),    
    # LOGIN / REGISTRO
    path("acceso/", views.acceso_view, name="acceso"),
    path("logout/", views.logout_view, name="logout"),
    path("me/", me_view, name="me"),
  
    
    # PASSWORD RESET
    path("password_reset/",auth_views.PasswordResetView.as_view(template_name="pedidos/password_reset.html"),name="password_reset",),
    path("password_reset_done/",auth_views.PasswordResetDoneView.as_view(template_name="pedidos/password_reset_done.html"),name="password_reset_done",),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="pedidos/password_reset_confirm.html"),name="password_reset_confirm",),
    path("reset/done/",auth_views.PasswordResetCompleteView.as_view(template_name="pedidos/password_reset_complete.html"),name="password_reset_complete",),
    
    # API / Sincronización
    # path('api/sincronizar-usuario/', views.SincronizarUsuarioAPIView.as_view(), name='sincronizar_usuario'),
    #
]
urlpatterns += router.urls
