import django_filters
from .models import Pedido

class PedidoFilter(django_filters.FilterSet):
    fecha_inicio = django_filters.DateFilter(field_name='fecha_inicio', lookup_expr='gte', label='Desde')
    fecha_fin    = django_filters.DateFilter(field_name='fecha_fin',    lookup_expr='lte', label='Hasta')

    class Meta:
        model  = Pedido
        fields = ['empresa', 'estado', 'fecha_inicio', 'fecha_fin']
