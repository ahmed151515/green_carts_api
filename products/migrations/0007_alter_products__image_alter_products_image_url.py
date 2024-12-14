# Generated by Django 5.1.4 on 2024-12-14 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_products__image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='_image',
            field=models.ImageField(blank=True, null=True, upload_to='img/'),
        ),
        migrations.AlterField(
            model_name='products',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]