# Generated by Django 5.1.7 on 2025-05-12 21:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pedidos", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pedido",
            name="fecha_creacion",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Fecha creación"
            ),
        ),
        migrations.AlterField(
            model_name="pedido",
            name="fecha_fin",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Fecha fin"),
        ),
    ]
