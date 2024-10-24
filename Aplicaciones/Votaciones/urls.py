#configurando redireccionamiento
from django.urls import path
from . import views
urlpatterns = [
    path('',views.inicio, name='inicio'),

    #----------CARGO----------
    path('listarCargos/', views.listarCargos, name='listarCargos'),
    path('crearCargos/', views.crearCargos, name='crearCargos'),
    path('eliminarCargos/<int:id>/', views.eliminarCargos, name='eliminarCargos'),

    #----------VOTANTE----------
    path('listarVotantes/', views.listarVotantes, name='listarVotantes'),
    path('verVotantes/', views.verVotantes, name='verVotantes'),
    path('crearVotante/', views.crearVotante, name='crearVotante'),
    path('eliminarVotantes/<int:id>/', views.eliminarVotantes, name='eliminarVotantes'),    

    #----------CANDIDATO----------
    path('listarCandidatos/', views.listarCandidatos, name='listarCandidatos'),
    path('verCandidatos/', views.verCandidatos, name='verCandidatos'),
    path('crearCandidato/', views.crearCandidato, name='crearCandidato'),
    path('editarCandidato/<int:id>/', views.editarCandidato, name='editarCandidato'),
    path('eliminarCandidato/<int:id>/', views.eliminarCandidato, name='eliminarCandidato'),

    #----------VOTO----------
    path('listarVotos/', views.listarVotos, name='listarVotos'),
    path('crearVoto/', views.crearVoto, name='crearVoto'),


    ]