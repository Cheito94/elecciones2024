# Generated by Django 4.0.6 on 2024-10-22 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Votaciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidato',
            name='ci',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='votante',
            name='ci',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
