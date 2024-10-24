from django.contrib import admin
from.models import Votante, Cargo, Candidato, Voto

# Register your models here.
admin.site.register(Votante)
admin.site.register(Cargo)
admin.site.register(Candidato)
admin.site.register(Voto)