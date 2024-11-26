from typing import Counter
from . models import Votante, Voto, Lista, Candidato, Lista  
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
from django.utils import timezone
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Create your views here.z
def inicio(request):
    return render(request, 'inicio.html')

#----------------Reporte de Listas-------------------
def reporte_listas(request):
    listas = Lista.objects.prefetch_related('votos_recibidos', 'candidatos')  
    listas_con_votos = [
        {
            'lista': lista,
            'num_votos': lista.votos_recibidos.count(),  # Usando el related_name personalizado
            'candidatos': lista.candidatos.all()  
        }
        for lista in listas
    ]

    context = {'listas_con_votos': listas_con_votos}
    return render(request, 'reporteListas.html', context)
#-------------------------------------Listas-------------------
def verListas(request):
    listas = Lista.objects.all()
    return render(request, 'verListas.html', {'listas': listas})

def listasParaUsuario(request):
    listas = Lista.objects.all()
    return render(request, 'listasParaUsuario.html', {'listas': listas})

def eliminarVoto(request, voto_id):
    if request.method == 'POST':
        voto = get_object_or_404(Voto, id=voto_id)
        voto.delete()
        messages.success(request, 'Voto eliminado con éxito.')
        return redirect('verListas')
    return redirect('verListas')

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
        nueva_lista = Lista.objects.create(nombre=nom, color=col, numero=num, foto=fot)
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

#------------------------------------------------VOTANTE---------------------------------------------
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
        if Votante.objects.filter(ci=ced).exists():
            messages.error(request, 'Ya existe un votante con esta cédula.')
            return render(request, 'crearVotante.html')
        nuevoVotante = Votante.objects.create(ci=ced, nombre=nom)
        messages.success(request, 'Votante guardado con éxito')
        return redirect('votacion', votante_id=nuevoVotante.id)

    return render(request, 'crearVotante.html')
                                            
def eliminarVotante(request, id):
    votanteEliminar = get_object_or_404(Votante, id=id)
    votanteEliminar.delete()
    messages.success(request, 'Votante eliminado con éxito')
    return redirect('listarVotantes')

def eliminar_todos_los_votantes(request):
    if request.method == 'POST':
        Votante.objects.all().delete()  
        messages.success(request, "Todos los votantes han sido eliminados.")
        return redirect('paginaAdmin') 

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
        if check_password(password, votante.password):
            if votante.ha_votado:
                messages.warning(request, 'Ya has realizado tu voto y no puedes votar de nuevo.')
                return redirect('inicio')  
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
            user.is_staff = True
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

#-----------------------------VOTO-----------------------------------------------------------

def votacion(request, votante_id):
    votante = Votante.objects.get(id=votante_id)
    listas = Lista.objects.all()

    if request.method == 'POST':
        lista_id = request.POST.get('lista_id')  
        lista_votada = Lista.objects.get(id=lista_id)
        Voto.objects.create(votante=votante, lista_votada=lista_votada, fecha=timezone.now())
        messages.success(request, f'Voto registrado con éxito por {votante.ci} en la lista {lista_votada.nombre}')
        return redirect('inicio')
    return render(request, 'votacion.html', {'votante': votante, 'listas': listas})

def verListas(request):
    listas = Lista.objects.all()
    for lista in listas:
        lista.votos = Voto.objects.filter(lista_votada=lista)  
    return render(request, 'verListas.html', {'listas': listas})

#-----------------------------------PDF Votante--------------------------

def generar_pdf_votantes(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="REPORTE DE LOS VOTANTES.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elementos = []

    styles = getSampleStyleSheet()
    titulo = "Lista de Votantes"
    elementos.append(Paragraph(f"<b>{titulo}</b>", styles['Title']))

    encabezados = ('ID', 'CI', 'Nombre')
    datos = [encabezados]

    votantes = Votante.objects.all()
    for votante in votantes:
        datos.append([str(votante.id), votante.ci, votante.nombre])

    tabla = Table(datos)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elementos.append(tabla)

    total_votantes = len(votantes)
    total_texto = f"<b>Total de Votantes:</b> {total_votantes}"
    elementos.append(Paragraph(total_texto, styles['Normal']))

    doc.build(elementos)

    return response


#------------------------PDFLista----------------------------------------------------------
def generar_pdf_listas(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="REPORTE DE LISTAS.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elementos = []

    styles = getSampleStyleSheet()
    titulo = "Reporte de Listas"
    elementos.append(Paragraph(f"<b>{titulo}</b>", styles['Title']))

    encabezados = ('Nombre de la Lista', 'Número de Votos')
    datos = [encabezados]

    listas = Lista.objects.all()

    for lista in listas:
        num_votos = lista.votos_recibidos.count()  
        datos.append([lista.nombre, str(num_votos)])

    tabla = Table(datos)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elementos.append(tabla)

    doc.build(elementos)

    return response