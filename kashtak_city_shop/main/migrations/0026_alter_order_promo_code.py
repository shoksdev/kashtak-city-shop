# Generated by Django 5.0.1 on 2024-03-15 14:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_order_promo_code_order_total_sum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='promo_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.promocode', verbose_name='Промокод'),
        ),
    ]
