# Generated by Django 5.0.7 on 2024-10-20 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_remove_comment_deslikes_remove_comment_likes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.TextField(blank=True, verbose_name='Descripcion'),
        ),
    ]
