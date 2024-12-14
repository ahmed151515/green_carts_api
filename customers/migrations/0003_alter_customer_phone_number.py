# Generated by Django 5.1.4 on 2024-12-14 10:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_customer_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator('^01[0125]\\d{8}$', 'the phone number must be a valid Egyptian phone number')]),
        ),
    ]
