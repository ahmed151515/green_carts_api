# Generated by Django 5.1.4 on 2024-12-14 10:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_products_price_alter_products_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0, 'the value must be greater than 0')]),
        ),
        migrations.AlterField(
            model_name='products',
            name='stock',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, 'the value must be greater than 0')]),
        ),
    ]
