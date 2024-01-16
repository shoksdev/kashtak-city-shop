# Generated by Django 5.0.1 on 2024-01-10 13:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0005_alter_order_apartment_alter_order_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='gender',
            field=models.CharField(choices=[('M', 'Man'), ('W', 'Woman')], default='M', max_length=1,
                                   verbose_name='Пол'),
        ),
        migrations.DeleteModel(
            name='Gender',
        ),
    ]
