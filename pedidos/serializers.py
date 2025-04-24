from rest_framework import serializers
from .models import Pedido, Tarea, Maleta
class MaletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maleta
        fields = ['cantidad_pax', 'guia']

class PedidoSerializer(serializers.ModelSerializer):
    # Hacemos usuario de solo lectura
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)
    maletas = MaletaSerializer(many=True)

    class Meta:
        model = Pedido
        fields = ['id', 'empresa', 'lugar_entrega', 'lugar_recogida', 'fecha_inicio', 'fecha_fin', 'estado', 'notas', 'maletas']

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