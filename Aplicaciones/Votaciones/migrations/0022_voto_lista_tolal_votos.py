# Generated by Django 5.1.3 on 2024-11-22 22:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Votaciones', '0021_remove_voto_lista'),
    ]

    operations = [
        migrations.AddField(
            model_name='voto',
            name='lista_tolal_votos',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votos', to='Votaciones.lista'),
        ),
    ]