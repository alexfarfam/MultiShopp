# Generated by Django 5.0.7 on 2024-10-19 20:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_remove_providerinfo_show_whatsapp_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='service',
            name='price',
        ),
        migrations.RemoveField(
            model_name='service',
            name='reference_price',
        ),
        migrations.RemoveField(
            model_name='service',
            name='show_offerts',
        ),
        migrations.AlterField(
            model_name='comment',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.product', verbose_name='Producto'),
        ),
        migrations.DeleteModel(
            name='ServiceOffer',
        ),
    ]
