# Generated by Django 4.0.6 on 2024-11-19 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Votaciones', '0008_remove_votante_email_remove_voto_candidato_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cargo',
            name='cargo',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
