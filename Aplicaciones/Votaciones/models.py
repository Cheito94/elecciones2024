from django import forms
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User

# Modelo Votante
class Votante(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    ci = models.CharField(max_length=10, null=True, unique=True)
    nombre = models.CharField(max_length=100, null=True)
    apellido = models.CharField(max_length=100, null=True)
    fechaNacimiento = models.DateTimeField(null=True)
    password = models.CharField(max_length=128, null=False, default='temporary_password')
    ha_votado = models.BooleanField(default=False)

    USERNAME_FIELD = 'ci'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'email']

    def __str__(self):
        return f"{self.id}: {self.nombre} - {self.apellido} - {self.email} - {self.fechaNacimiento}"

# Modelo Voto
class Voto(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    votante = models.ForeignKey(Votante, on_delete=models.CASCADE, null=True)

    def __str__(self):
        fila = "{0}: {1} - {2} - {3}"
        return fila.format(self.id, self.fecha, self.votante)
    
class Lista(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True)
    color = models.CharField(max_length=50, null=True)
    numero = models.CharField(max_length=25, null=True)
    foto = models.FileField(upload_to='fotoLista', null=True, blank=True)
    
    def __str__(self):
        return f"{self.id}: {self.nombre} - {self.color}"
    
class Candidato(models.Model):
    lista = models.ForeignKey(Lista, on_delete=models.CASCADE, related_name='candidatos')
    nombre = models.CharField(max_length=100)
    ROLES = [
        ('PRESIDENTE', 'Presidente'),
        ('VICEPRESIDENTE', 'Vicepresidente'),
        ('SECRETARIO', 'Secretario'),
        ('TESORERO', 'Tesorero'),
        ('1ER VOCAL PRINCIPAL', '1er Vocal Principal'),
        ('2DO VOCAL PRINCIPAL', '2do Vocal Principal'),
        ('3ER VOCAL PRINCIPAL', '3er Vocal Principal'),
        ('1ER VOCAL SUPLENTE', '1er Vocal Suplente'),
        ('2DO VOCAL SUPLENTE', '2do Vocal Suplente'),
        ('3ER VOCAL SUPLENTE', '3er Vocal Suplente'),
    ]
    rol = models.CharField(max_length=25, choices=ROLES)

    def __str__(self):
        return f"{self.nombre} - {self.rol}"


