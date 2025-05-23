# Generated by Django 5.0.7 on 2024-11-02 06:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_rename_reservations_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Activo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.service', verbose_name='Servicio'),
        ),
    ]
