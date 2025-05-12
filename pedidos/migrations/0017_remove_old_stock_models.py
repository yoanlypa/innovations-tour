# pedidos/migrations/00XX_remove_old_stock_models.py
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0016_pedido_excursion'),  # Ajusta al nombre de tu última migración aplicada
    ]

    operations = [
        migrations.DeleteModel(name='StockControl'),
        migrations.DeleteModel(name='StockMaleta'),
    ]
