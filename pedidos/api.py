

from .models import Pedido, Tarea
from .serializers import PedidoSerializer, TareaSerializer
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    
class PedidoListCreateAPI(generics.ListCreateAPIView):
    """
    GET  /api/pedidos/  → devuelve la lista de pedidos
    POST /api/pedidos/  → crea un nuevo pedido
    """
    queryset = Pedido.objects.all().order_by('-fecha_creacion')
    serializer_class = PedidoSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)