# Generated by Django 5.0.7 on 2024-09-26 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_service_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientinfo',
            name='district',
        ),
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
        migrations.DeleteModel(
            name='City',
        ),
    ]
