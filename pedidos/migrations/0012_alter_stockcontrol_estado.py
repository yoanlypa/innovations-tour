# Generated by Django 5.1.7 on 2025-05-04 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0011_alter_stockcontrol_entregado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockcontrol',
            name='estado',
            field=models.CharField(choices=[('P', 'Pendiente'), ('G', 'Pagado')], default='G', max_length=1),
        ),
    ]
