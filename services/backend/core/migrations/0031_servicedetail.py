# Generated by Django 5.0.7 on 2024-11-06 03:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_providerinfo_company_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.service', verbose_name='Servicio')),
            ],
        ),
    ]
