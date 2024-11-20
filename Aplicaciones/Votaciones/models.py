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

# Modelo Cargo (quitar la segunda definición)
class Cargo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.nombre}"

# Modelo Candidato
class Candidato(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.id}: {self.nombre}"

# Modelo Voto
class Voto(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    votante = models.ForeignKey(Votante, on_delete=models.CASCADE, null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, default='')

    def __str__(self):
        fila = "{0}: {1} - {2} - {3}"
        return fila.format(self.id, self.fecha, self.votante)

# Modelo Lista
class Lista(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True)
    color = models.CharField(max_length=50, null=True)
    numero = models.CharField(max_length=25, null=True)
    foto = models.FileField(upload_to='fotoLista' ,null=True,blank=True)

    def __str__(self):
        fila = "{0}: {1} - {2} - {3}"
        return fila.format(self.id, self.nombre, self.nombre, self.color)
