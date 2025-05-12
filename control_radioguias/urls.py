from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    # Panel de administración
    path('admin/', admin.site.urls),

    # Todas las URLs de la app “pedidos”
    path('pedidos/', include('pedidos.urls', namespace='pedidos')),

    # Login de la API (DRF)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Redirección raíz al acesso
    path('', RedirectView.as_view(url='/acceso/')),
]