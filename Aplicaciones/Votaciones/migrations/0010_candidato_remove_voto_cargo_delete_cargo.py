# Generated by Django 4.0.6 on 2024-11-21 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Votaciones', '0009_cargo_cargo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('rol', models.CharField(choices=[('PRESIDENTE', 'Presidente'), ('VICEPRESIDENTE', 'Vicepresidente'), ('SECRETARIO', 'Secretario'), ('TESORERO', 'Tesorero'), ('1ER VOCAL PRINCIPAL', '1er Vocal Principal'), ('2DO VOCAL PRINCIPAL', '2do Vocal Principal'), ('3ER VOCAL PRINCIPAL', '3er Vocal Principal'), ('1ER VOCAL SUPLENTE', '1er Vocal Suplente'), ('2ER VOCAL SUPLENTE', '1er Vocal Suplente'), ('3ER VOCAL SUPLENTE', '1er Vocal Suplente')], max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='voto',
            name='cargo',
        ),
        migrations.DeleteModel(
            name='Cargo',
        ),
    ]
