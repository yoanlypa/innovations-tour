

from .models import Pedido, Tarea
from .serializers import PedidoSerializer, TareaSerializer
from rest_framework import viewsets, generics

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    
class PedidoCreateAPI(generics.CreateAPIView):

    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    