# Generated by Django 5.1.3 on 2024-11-22 21:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Votaciones', '0016_votante_lista'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='votante',
            name='lista',
        ),
        migrations.RemoveField(
            model_name='voto',
            name='lista_votada',
        ),
        migrations.AddField(
            model_name='voto',
            name='lista',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votos', to='Votaciones.lista'),
        ),
    ]
