from rest_framework import serializers
from .models import Servicio, Pedido, Tarea


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = [ "excursion", "cantidad_pax", "emisores", "guia", "lugar_entrega", "bono" ]


class PedidoSerializer(serializers.ModelSerializer):
    servicios = ServicioSerializer(many=True)
    usuario = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Pedido
        fields = [
            "id",
            "usuario",
            "empresa",
            "excursion",
            "lugar_entrega",
            "lugar_recogida",
            "fecha_inicio",
            "fecha_fin",
            "estado",
            "notas",
            "servicios",
        ]

    def create(self, validated_data):
        servicios_data = validated_data.pop("servicios")
        pedido = Pedido.objects.create(**validated_data)
        for servicio in servicios_data:
            Servicio.objects.create(pedido=pedido, **servicio)
        return pedido


class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = "__all__"
    