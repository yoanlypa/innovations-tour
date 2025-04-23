from rest_framework import serializers
from .models import Pedido, Tarea

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        extra_kwargs = {
            'fecha_inicio': {'required': True},
            'estado': {'required': False},
            
        }

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'