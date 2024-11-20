#configurando redireccionamiento
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.inicio, name='inicio'),

    #----------VOTOS POR CARGO----------
    path('votos-por-cargo/', views.votos_por_cargo, name='votos_por_cargo'),

    #----------CARGO----------
    path('listarCargos/', views.listarCargos, name='listarCargos'),
    path('crearCargo/', views.crearCargo, name='crearCargo'),
    path('editarCargo/<int:id>/', views.editarCargo, name='editarCargo'),
    path('eliminarCargo/<int:id>/', views.eliminarCargo, name='eliminarCargo'),

    #----------VOTANTE----------
    path('listarVotantes/', views.listarVotantes, name='listarVotantes'),
    path('verVotantes/', views.verVotantes, name='verVotantes'),
    path('crearVotante/', views.crearVotante, name='crearVotante'),
    path('eliminarVotante/<int:id>/', views.eliminarVotante, name='eliminarVotante'),    

    #-------------------------------------LISTAS-----------------------------------------------------------
    path('verListas/', views.verListas, name='verListas'),
    path('listarListas/', views.listarListas, name='listarListas'),
    path('crearLista/', views.crearLista, name='crearLista'),
    path('editarLista/<int:lista_id>/', views.editarLista, name='editarLista'),
    path('eliminarLista/<int:lista_id>/', views.eliminarLista, name='eliminarLista'),

    #--------------------------------------VOTO------------------------------------------------------------
    path('listarVotos/', views.listarVotos, name='listarVotos'),
    path('crearVoto/', views.crearVoto, name='crearVoto'),

    path('login/', views.votante_login, name='login'),

    #-------ADMINISTRADOR------------

    path('registro_admin/', views.registro_administrador, name='registroAdmin'),
    path('login_admin/', views.login_administrador, name='loginAdmin'),
    path('pagina_admin/', views.pagina_administrador, name='paginaAdmin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('listadoAdmin/', views.listadoAdmin, name='listarAdmin'),
    path('eliminarAdmin/<int:admin_id>/', views.eliminar_admin, name='eliminarAdmin'),


    ]