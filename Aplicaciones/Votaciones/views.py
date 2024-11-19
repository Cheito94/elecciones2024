from typing import Counter
from . models import Cargo, Votante, Voto, Lista
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
        nom = request.POST['nombre']
        col = request.POST['color']
        num = request.POST['numero']
        fot = request.FILES.get('foto')
        if Lista.objects.filter(nombre=nom).exists():
            messages.error(request, 'Ya existe una Lista con este nombre')
            return render(request, 'crearLista.html')
        nuevoLista = Lista.objects.create(nombre=nom,color=col,numero=num,foto=fot)
        messages.success(request, 'Lista guardado con éxito')
        return redirect('listarListas')
    return render(request, 'crearLista.html')

def editarLista(request, lista_id):
    lista = get_object_or_404(Lista, id=lista_id)  # Obtenemos la lista por ID
    if request.method == 'POST':
        lista.nombre = request.POST['nombre']
        lista.color = request.POST['color']
        lista.numero = request.POST['numero']
        if 'foto' in request.FILES:
            lista.foto = request.FILES['foto']
        lista.save()
        messages.success(request, 'Lista actualizada con éxito')
        return redirect('listarListas')  # Redirige a la vista de listas
    return render(request, 'editarLista.html', {'lista': lista})

def eliminarLista(request, lista_id):
    lista = get_object_or_404(Lista, id=lista_id)
    lista.delete()
    messages.success(request, 'Lista eliminada con éxito')
    return redirect('listarListas')

#----------CARGO----------
def listarCargos(request):
    cargos = Cargo.objects.all()
    return render(request, 'listarCargos.html', {'cargos': cargos})

def crearCargo(request):
    if request.method == 'POST':
        car = request.POST.get('cargo')
        nom = request.POST.get('nombre')
        if car and nom:
            Cargo.objects.create(cargo=car, nombre=nom)
            messages.success(request, 'Candidato guardado con éxito')
            return redirect('listarCargos')
    return render(request, 'crearCargos.html')

def editarCargo(request, id):  # Cambié la vista para que reciba 'id' como argumento
    cargo = get_object_or_404(Cargo, id=id)  # Obtenemos el objeto Cargo basado en el id
    if request.method == 'POST':
        car = request.POST.get('cargo')
        nom = request.POST.get('nombre')
        if car and nom:
            cargo.cargo = car
            cargo.nombre = nom
            cargo.save()  # Agregué los paréntesis a save para que guarde el cambio
            messages.success(request, 'Candidato actualizado con éxito')
            return redirect('listarCargos')
    return render(request, 'editarCargo.html', {'cargo': cargo})
    
def eliminarCargo(request, id):
    cargoEliminar = get_object_or_404(Cargo, id=id)
    cargoEliminar.delete()
    messages.success(request, 'Cargo eliminado con éxito')
    return redirect('listarCargos')

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

def crearVoto(request):
    votante_id = request.session.get('votante_id')  # Obtener el votante actual de la sesión
    votante = get_object_or_404(Votante, id=votante_id)

    if request.method == 'POST':
        candidato_id = request.POST['candidato']
        feVoto = request.POST['fecha']
        cargo_id = request.POST['cargo']
        cargo = get_object_or_404(Cargo, id=cargo_id)

        # Verificar si el votante ya ha votado para el cargo seleccionado
        if Voto.objects.filter(votante=votante, cargo=cargo).exists():
            messages.error(request, f"Ya has votado para el cargo de {cargo.nombre}.")
        else:
            # Si no ha votado, registrar el voto
            Voto.objects.create(fecha=feVoto, cargo=cargo, votante=votante)
            messages.success(request, f"Voto registrado exitosamente para el cargo de {cargo.nombre}.")

        return redirect('crearVoto')  # Mantener en la página de crear voto

    # Obtener los cargos disponibles para votar excluyendo aquellos ya votados por el votante
    cargos_votados = Voto.objects.filter(votante=votante).values_list('cargo', flat=True)
    cargos = Cargo.objects.exclude(id__in=cargos_votados)
    
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

        # Si no hay errores, crear al usuario
        if not errors:
            user = User.objects.create_user(username=username, password=password)
            user.is_staff = True  # Asegura que es un administrador
            user.save()
            
            # Iniciar sesión automáticamente después de registrar
            login(request, user)
            
            return redirect('loginAdmin')  # Redirige al login del administrador
        
        # Si hay errores, volver a mostrar el formulario con los errores
        return render(request, 'registroAdmin.html', {'errors': errors})
    
    return render(request, 'registroAdmin.html')

# Login de administrador
def login_administrador(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:  # Verificar que el usuario es un administrador
            login(request, user)
            return redirect('paginaAdmin')  # Redirigir al dashboard de administrador o página específica
        else:
            # Si las credenciales no son válidas o no es un administrador
            messages.error(request, 'Credenciales no válidas o no tienes permisos de administrador.')

    return render(request, 'loginAdmin.html')
    
@login_required
def pagina_administrador(request):
    # Verificar si el usuario tiene permisos de administrador
    if request.user.is_staff or (hasattr(request.user, 'is_staff') and request.user.is_admin):
        return render(request, 'paginaAdmin.html')  # Renderiza la página exclusiva del admin
    else:
        return redirect('loginAdmin')  # Redirige al login si no es admin

def logout_administrador(request):
    logout(request)
    return redirect('loginAdmin') 

def listadoAdmin(request):
    administradores = User.objects.filter(is_staff=True)
    return render(request, 'listarAdmin.html', {'administradores': administradores})

def eliminar_admin(request, admin_id):
    administrador = get_object_or_404(User, id=admin_id)
    administrador.delete()
    messages.success(request, f'Administrador {administrador.username} eliminado exitosamente.')
    return redirect('listarAdmin')


