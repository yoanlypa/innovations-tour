from rest_framework import serializers
from .models import Pedido, Tarea, Maleta


class MaletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maleta
        fields = ['cantidad_pax', 'guia']


class PedidoSerializer(serializers.ModelSerializer):
    maletas = MaletaSerializer(many=True)
    usuario = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Pedido
        fields = [
            'id', 'usuario', 'empresa', 'excursion', 'lugar_entrega',
            'lugar_recogida', 'fecha_inicio', 'fecha_fin',
            'estado_cliente', 'estado_equipo',
            'notas', 'maletas'
        ]

    def create(self, validated_data):
        maletas_data = validated_data.pop('maletas')
        pedido = Pedido.objects.create(**validated_data)
        for maleta in maletas_data:
            Maleta.objects.create(pedido=pedido, **maleta)
        return pedido
class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'