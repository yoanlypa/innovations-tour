# Generated by Django 5.1.7 on 2025-05-21 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pedidos", "0007_remove_pedido_productos_pedido_servicios_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="servicio",
            name="cantidad_pax",
        ),
    ]
