# Generated by Django 5.1.7 on 2025-03-10 10:20

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+1234567890', max_length=128, region=None),
        ),
    ]
