# Generated by Django 5.0.3 on 2024-04-10 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_order_delivery_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='delivery_address',
            new_name='delivery_addrss',
        ),
    ]
