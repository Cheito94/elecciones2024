# Generated by Django 5.1.3 on 2024-11-22 21:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Votaciones', '0017_remove_votante_lista_remove_voto_lista_votada_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='voto',
            name='lista_votada',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Votaciones.lista'),
        ),
    ]
