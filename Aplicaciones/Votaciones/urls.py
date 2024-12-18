#configurando redireccionamiento
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.inicio, name='inicio'),
    #-----Otras rutas----
    path('reporte-listas/', views.reporte_listas, name='reporteListas'),

    #----------------------------------------VOTANTE-------------------------------------------
    path('listarVotantes/', views.listarVotantes, name='listarVotantes'),
    path('verVotantes/', views.verVotantes, name='verVotantes'),
    path('eliminarVotante/<int:id>/', views.eliminarVotante, name='eliminarVotante'),    
    path('crearVotante/', views.crearVotante, name='crearVotante'),
    path('votacion/<int:votante_id>/', views.votacion, name='votacion'),
    path('eliminarVoto/<int:voto_id>/', views.eliminarVoto, name='eliminarVoto'),
    path('eliminar-todos-los-votantes/', views.eliminar_todos_los_votantes, name='eliminar_todos_los_votantes'),
    #-------------------------------------LISTAS-----------------------------------------------------------
    path('verListas/', views.verListas, name='verListas'),
    path('listasParaUsuario/', views.listasParaUsuario, name='listasParaUsuario'),
    path('listarListas/', views.listarListas, name='listarListas'),
    path('crearLista/', views.crearLista, name='crearLista'),
    path('editarLista/<int:lista_id>/', views.editarLista, name='editarLista'),
    path('eliminarLista/<int:lista_id>/', views.eliminarLista, name='eliminarLista'),

    #--------------------------------------VOTO------------------------------------------------------------
    path('listarVotos/', views.listarVotos, name='listarVotos'),
    
    path('login/', views.votante_login, name='login'),

    #--------------------------------------ADMINISTRADOR---------------------------------------------------
    path('registro_admin/', views.registro_administrador, name='registroAdmin'),
    path('login_admin/', views.login_administrador, name='loginAdmin'),
    path('pagina_admin/', views.pagina_administrador, name='paginaAdmin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('listadoAdmin/', views.listadoAdmin, name='listarAdmin'),
    path('eliminarAdmin/<int:admin_id>/', views.eliminar_admin, name='eliminarAdmin'),

    #---------------------------PDF-----------------------------------------------
    path('generar_pdf_votantes/', views.generar_pdf_votantes, name='generar_pdf_votantes'),
    path('generar_pdf_listas/', views.generar_pdf_listas, name='generar_pdf_listas'),

]