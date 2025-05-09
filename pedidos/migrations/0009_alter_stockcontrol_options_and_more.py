# Generated by Django 5.1.7 on 2025-05-01 23:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0008_registrocliente'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stockcontrol',
            options={'ordering': ['-fecha_creacion'], 'verbose_name': 'Control de Stock', 'verbose_name_plural': 'Controles de Stock'},
        ),
        migrations.AddField(
            model_name='stockcontrol',
            name='fecha_creacion',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Fecha de registro (modificable)', verbose_name='Fecha de Creación'),
        ),
        migrations.AlterField(
            model_name='stockcontrol',
            name='entregado',
            field=models.BooleanField(default=True, verbose_name='Entregado'),
        ),
        migrations.AlterField(
            model_name='stockcontrol',
            name='excursion',
            field=models.CharField(max_length=100, verbose_name='Excursión'),
        ),
        migrations.AlterField(
            model_name='stockcontrol',
            name='fecha_er',
            field=models.DateField(verbose_name='Fecha E/R'),
        ),
        migrations.AlterField(
            model_name='stockcontrol',
            name='guia',
            field=models.CharField(max_length=100, verbose_name='Guía'),
        ),
        migrations.AlterField(
            model_name='stockcontrol',
            name='lugar_er',
            field=models.CharField(max_length=100, verbose_name='Lugar E/R'),
        ),
        migrations.AlterField(
            model_name='stockcontrol',
            name='pax',
            field=models.IntegerField(verbose_name='PAX'),
        ),
        migrations.AlterField(
            model_name='stockcontrol',
            name='recogido',
            field=models.BooleanField(default=False, verbose_name='Recogido'),
        ),
    ]
