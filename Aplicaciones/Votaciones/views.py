from typing import Counter
from . models import Votante, Voto, Lista, Candidato
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import login

# Create your views here.z
def inicio(request):
    return render(request, 'inicio.html')

#----------------Listas-------------------
def verListas(request):
    listas = Lista.objects.all()
    return render(request, 'verListas.html', {'listas': listas})

def listarListas(request):
    listas = Lista.objects.all()
    return render(request, 'listarListas.html', {'listas': listas})

def crearLista(request):
    if request.method == 'POST':
        # Datos de la lista
        nom = request.POST['nombre']
        col = request.POST['color']
        num = request.POST['numero']
        fot = request.FILES.get('foto')

        # Verificar si ya existe una lista con el mismo nombre
        if Lista.objects.filter(nombre=nom).exists():
            messages.error(request, 'Ya existe una Lista con este nombre')
            return render(request, 'crearLista.html')

        # Crear la nueva lista
        nueva_lista = Lista.objects.create(nombre=nom, color=col, numero=num, foto=fot)

        # Procesar los candidatos
        candidatos = request.POST.getlist('candidatos[]')
        roles = request.POST.getlist('roles[]')

        for nombre_candidato, rol_candidato in zip(candidatos, roles):
            if nombre_candidato and rol_candidato:
                Candidato.objects.create(lista=nueva_lista, nombre=nombre_candidato, rol=rol_candidato)

        messages.success(request, 'Lista y candidatos guardados con éxito')
        return redirect('listarListas')

    return render(request, 'crearLista.html')

def editarLista(request, lista_id):
    lista = get_object_or_404(Lista, id=lista_id)
    if request.method == 'POST':
        lista.nombre = request.POST['nombre']
        lista.color = request.POST['color']
        lista.numero = request.POST['numero']
        if 'foto' in request.FILES:
            lista.foto = request.FILES['foto']
        lista.save()
        candidatos = request.POST.getlist('candidatos[]')
        roles = request.POST.getlist('roles[]')
        lista.candidatos.all().delete() 
        for nombre_candidato, rol_candidato in zip(candidatos, roles):
            if nombre_candidato and rol_candidato:
                Candidato.objects.create(lista=lista, nombre=nombre_candidato, rol=rol_candidato)
        messages.success(request, 'Lista y candidatos actualizados con éxito')
        return redirect('listarListas')
    candidatos = lista.candidatos.all()

    context = {
        'lista': lista,
        'candidatos': candidatos
    }
    return render(request, 'editarLista.html', context)

def eliminarLista(request, lista_id):
    lista = get_object_or_404(Lista, id=lista_id)
    lista.delete()
    messages.success(request, 'Lista eliminada con éxito')
    return redirect('listarListas')

#----------VOTANTE----------
def listarVotantes(request):
    votantes = Votante.objects.all()
    return render(request, 'listarVotantes.html', {'votantes': votantes})

def verVotantes(request):
    votantes = Votante.objects.all()
    return render(request, 'verVotantes.html', {'votantes': votantes})

def crearVotante(request):
    if request.method == 'POST':
        ced = request.POST['ci']
        nom = request.POST['nombre']
        apell = request.POST['apellido']
        corr = request.POST['email']
        fechNac = request.POST.get('fechaNacimiento')
        password = request.POST['password']  # Obtén la contraseña del formulario
        
        if Votante.objects.filter(ci=ced).exists():
            messages.error(request, 'Ya existe un votante con esta cédula.')
            return render(request, 'crearVotante.html')
        nuevoVotante = Votante.objects.create(
            ci=ced, nombre=nom, apellido=apell, email=corr, fechaNacimiento=fechNac, password=make_password(password))
        messages.success(request, 'Votante guardado con éxito')
        return redirect('verVotantes')
    return render(request, 'crearVotante.html')
                                            
def eliminarVotante(request, id):
    votanteEliminar = get_object_or_404(Votante, id=id)
    votanteEliminar.delete()
    messages.success(request, 'Votante eliminado con éxito')
    return redirect('listarVotantes')

#----------VOTO----------
def listarVotos(request):
    votos = Voto.objects.all()
    return render(request, 'listarVotos.html', {'votos': votos})
    
def votante_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            votante = Votante.objects.get(ci=username)
        except Votante.DoesNotExist: 
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return render(request, 'login.html')

        # Verificar la contraseña
        if check_password(password, votante.password):
            # Verificar si el votante ya ha votado
            if votante.ha_votado:
                messages.warning(request, 'Ya has realizado tu voto y no puedes votar de nuevo.')
                return redirect('inicio')  # Redirige al inicio si ya ha votado
            # Iniciar sesión y redirigir a la página de votar
            request.session['votante_id'] = votante.id
            request.session['ha_votado'] = votante.ha_votado
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('crearVoto')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return render(request, 'login.html')

#------------------------------ADMINISTRADOR------------------------------

# Registro del administrador
def registro_administrador(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
    
        errors = []

        if not username or not password or not password_confirm:
            errors.append('Todos los campos son obligatorios.')
        elif password != password_confirm:
            errors.append('Las contraseñas no coinciden.')
        elif User.objects.filter(username=username).exists():
            errors.append('El nombre de usuario ya existe.')

        if not errors:
            user = User.objects.create_user(username=username, password=password)
            user.is_staff = True  # Marcar como administrador
            user.save()
            
            login(request, user)
            
            return redirect('loginAdmin')
        return render(request, 'registroAdmin.html', {'errors': errors})
    
    return render(request, 'registroAdmin.html')

# Login de administrador
def login_administrador(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff: 
            login(request, user)
            return redirect('paginaAdmin')  
        else:
            messages.error(request, 'Credenciales no válidas o no tienes permisos de administrador.')

    return render(request, 'loginAdmin.html')

def pagina_administrador(request):
    if request.user.is_staff:  
        return render(request, 'paginaAdmin.html')  
    else:
        messages.error(request, 'No tienes permiso para acceder a esta página.')  
        return redirect('loginAdmin')

def logout_administrador(request):
    logout(request)
    return redirect('loginAdmin')

@login_required
def listadoAdmin(request):
    if request.user.is_staff:
        administradores = User.objects.filter(is_staff=True)
        return render(request, 'listarAdmin.html', {'administradores': administradores})
    else:
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('loginAdmin')


@login_required
def eliminar_admin(request, admin_id):
    if request.user.is_staff:
        administrador = get_object_or_404(User, id=admin_id)
        administrador.delete()
        messages.success(request, f'Administrador {administrador.username} eliminado exitosamente.')
        return redirect('listarAdmin')
    else:
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('loginAdmin')

