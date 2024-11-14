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
    email = models.EmailField(max_length=100, null=True)
    fechaNacimiento = models.DateTimeField(null=True)
    password = models.CharField(max_length=128, null=False, default='temporary_password')

    USERNAME_FIELD = 'ci'  # Define que el campo ci será el campo de login
    REQUIRED_FIELDS = ['nombre', 'apellido', 'email']

    def __str__(self):
        fila = "{0}: {1} - {2} - {3} - {4} - {5}"
        return fila.format(self.id, self.nombre, self.apellido, self.email, self.fechaNacimiento)

# Modelo Cargo
class Cargo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True)

    def __str__(self):
        fila = "{0}: {1}"
        return fila.format(self.id, self.nombre)

# Modelo Candidato
class Candidato(models.Model):
    id = models.AutoField(primary_key=True)
    ci = models.CharField(max_length=10, null=True, unique=True)
    nombre = models.CharField(max_length=100, null=True)
    apellido = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    foto = models.FileField(upload_to='fotoCandidato' ,null=True,blank=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, null=True)

    def __str__(self):
        fila = "{0}: {1} - {2} - {3} - {4} - {5} - {6}"
        return fila.format(self.id, self.ci, self.nombre, self.apellido, self.email, self.foto, self.cargo)

# Modelo Voto    
class Voto(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    votante = models.ForeignKey(Votante, on_delete=models.CASCADE, null=True)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, default='')

    def __str__(self):
        fila = "{0}: {1} - {2} - {3}"
        return fila.format(self.id, self.fecha, self.votante, self.candidato)
    
# Modelo administrador 
class RegistroAdministradorForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_staff = True  # Marca al usuario como staff (administrador)
        if commit:
            user.save()
        return user

