# pedidos/tests.py
from django.test import TestCase

from .models import Pedido


class PedidoTestCase(TestCase):
    def test_creacion_pedido(self):
        pedido = Pedido.objects.create(
            empresa="Test Corp", fecha_inicio="2025-03-25", cantidad_radios=10
        )
        self.assertEqual(pedido.estado, "pendiente")
