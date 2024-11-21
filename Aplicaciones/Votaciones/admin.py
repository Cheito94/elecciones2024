from django.contrib import admin
from.models import Votante, Voto, Lista, Candidato

# Register your models here.
admin.site.register(Votante)
admin.site.register(Candidato)
admin.site.register(Voto)
admin.site.register(Lista)