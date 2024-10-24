from typing import Counter
from . models import Cargo, Votante, Candidato, Voto
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages 
# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

#----------CARGO----------
def listarCargos(request):
    cargos = Cargo.objects.all()
    return render(request, 'listarCargos.html', {'cargos': cargos})

def crearCargos(request):
    if request.method == 'POST':
        nom = request.POST['nombre']
        nuevoCargo = Cargo.objects.create(nombre=nom)
        messages.success(request, 'Cargo guardado con éxito')
        return redirect('listarCargos')
    return render(request, 'crearCargos.html')

def eliminarCargos(request, id):
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
        if Votante.objects.filter(ci=ced).exists():
            messages.error(request, 'Ya existe un votante con esta cédula.')
            return render(request, 'crearVotante.html')
        nuevoVotante = Votante.objects.create(ci=ced, nombre=nom, apellido=apell, email=corr, fechaNacimiento=fechNac)
        messages.success(request, 'Votante guardado con éxito')
        return redirect('verVotantes')
    return render(request, 'crearVotante.html')
                                            
def eliminarVotantes(request, id):
    votanteEliminar = get_object_or_404(Votante, id=id)
    votanteEliminar.delete()
    messages.success(request, 'Votante eliminado con éxito')
    return redirect('listarVotantes')

#----------CANDIDATO----------
def listarCandidatos(request):
    candidatos = Candidato.objects.all()
    return render(request, 'listarCandidatos.html', {'candidatos': candidatos})

def verCandidatos(request):
    # Obtener todos los cargos únicos
    cargos = Candidato.objects.values_list('cargo__nombre', flat=True).distinct()
    # Crear un diccionario de candidatos agrupados por cargo
    candidatos_por_cargo = {cargo: Candidato.objects.filter(cargo__nombre=cargo) for cargo in cargos}
    
    return render(request, 'verCandidatos.html', {'candidatos_por_cargo': candidatos_por_cargo})

def crearCandidato(request):
    if request.method == 'POST':
        ced = request.POST['ci']
        nom = request.POST['nombre']
        apell = request.POST['apellido']
        carg = request.POST['cargo']
        corr = request.POST['email']
        fot = request.FILES.get('foto')
        if Candidato.objects.filter(ci=ced).exists():
            messages.error(request, 'Ya existe un candidato con esta cédula.')
            return render(request, 'crearCandidato.html')
        cargo = Cargo.objects.get(id=carg)
        nuevoCandidato = Candidato.objects.create(ci=ced, nombre=nom, apellido=apell, email=corr, foto=fot, cargo=cargo)
        messages.success(request, 'Candidato guardado con éxito')
        return redirect('listarCandidatos')
    cargos = Cargo.objects.all()
    return render(request, 'crearCandidato.html', {'cargos': cargos})

def editarCandidato(request, id):
    candidato = get_object_or_404(Candidato, id=id)
    if request.method == 'POST':
        candidato.ci = request.POST['ci']
        candidato.nombre = request.POST['nombre']
        candidato.apellido = request.POST['apellido']
        cargo_id = request.POST['cargo']
        candidato.cargo = get_object_or_404(Cargo, id=cargo_id)
        candidato.email = request.POST['email']
        candidato.foto = request.FILES.get('foto')
        candidato.save()
        messages.success(request, 'Candidato editado con éxito')
        return redirect('listarCandidatos')
    cargos = Cargo.objects.all()
    return render(request, 'editarCandidato.html', {'candidato': candidato, 'cargos': cargos})
        
    
def eliminarCandidato(request, id):
    candidatoEliminar = get_object_or_404(Candidato, id=id)
    candidatoEliminar.delete()
    messages.success(request, 'Candidato eliminado con éxito')
    return redirect('listarCandidatos')

#----------VOTO----------

def listarVotos(request):
    votos = Voto.objects.all()
    return render(request, 'listarVotos.html', {'votos': votos})

def crearVoto(request):
    if request.method == 'POST':
        candidato_id = request.POST['candidato']
        feVoto = request.POST['fecha']
        cargo = request.POST['cargo']
        votante_id = request.POST['votante']
        
        candidato = get_object_or_404(Candidato, id=candidato_id)
        cargo = get_object_or_404(Cargo, id=cargo)
        votante = get_object_or_404(Votante, id=votante_id)
        
        nuevoVoto = Voto.objects.create(fecha=feVoto, candidato=candidato, cargo=cargo, votante=votante)
        
        messages.success(request, 'Voto guardado con éxito')
        return redirect('inicio')

    cargos = Cargo.objects.all()
    votantes = Votante.objects.all()

    # Filtrar candidatos solo por el cargo seleccionado
    candidatos = Candidato.objects.none()  # Iniciamos con un QuerySet vacío
    if 'cargo' in request.GET:
        cargo = request.GET['cargo']
        candidatos = Candidato.objects.filter(cargo=cargo)

    return render(request, 'crearVoto.html', {'candidatos': candidatos, 'cargos': cargos, 'votantes': votantes})





        



    
