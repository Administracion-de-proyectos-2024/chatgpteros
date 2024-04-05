from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, DiapositivaForm
from .models import Diapositiva
import markdown
from django.http import HttpResponse

import os


def home(request):  
    return render(request, 'core/home.html')


@login_required
def presentaciones(request):
    directorio_de_archivos_txt = 'core/archivos_txt'
    txt_files = [f for f in os.listdir(directorio_de_archivos_txt) if f.endswith('.txt')]

    presentaciones = []
    for txt_file in txt_files:
        with open(os.path.join(directorio_de_archivos_txt, txt_file), 'r') as file:
            titulo = os.path.splitext(txt_file)[0]  # Obtener el nombre del archivo sin la extensión .txt
            contenido = file.read()
            presentaciones.append({'titulo': titulo, 'contenido': contenido})

    return render(request, 'core/presentaciones.html', {'presentaciones': presentaciones})


@login_required
def presentaciones_archivos_txt(request):
    directorio_de_archivos_txt = 'core/archivos_txt'

    # Verificar que el directorio exista
    if not os.path.exists(directorio_de_archivos_txt):
        return HttpResponse("El directorio de archivos de presentación no existe", status=404)

    # Leer todos los archivos .txt en el directorio
    txt_files = [f for f in os.listdir(directorio_de_archivos_txt) if f.endswith('.txt')]

    # Procesar los archivos de presentación
    presentaciones = []
    for txt_file in txt_files:
        with open(os.path.join(directorio_de_archivos_txt, txt_file), 'r') as file:
            titulo = os.path.splitext(txt_file)[0]  # Obtener el nombre del archivo sin la extensión .txt
            contenido = file.read()
            presentaciones.append({'titulo': titulo, 'contenido': contenido})

    return render(request, 'core/presentaciones_archivos_txt.html', {'presentaciones': presentaciones})


def exit(request):
    logout(request)
    return redirect('home')


def register(request):
    data = {'form': CustomUserCreationForm()}
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            return redirect('home')
    return render(request, 'registration/register.html', data)


@login_required
def crear_diapositiva(request):
    if request.method == 'POST':
        form = DiapositivaForm(request.POST)
        if form.is_valid():
            diapositiva = form.save(commit=False)
            diapositiva.usuario = request.user
            diapositiva.save()
            return redirect('lista_diapositivas')
    else:
        form = DiapositivaForm()
    return render(request, 'core/crear_diapositiva.html', {'form': form})


@login_required
def lista_diapositivas(request):
    diapositivas = Diapositiva.objects.all()
    for diapositiva in diapositivas:
        diapositiva.contenido_html = markdown.markdown(diapositiva.contenido)
    return render(request, 'core/lista_diapositivas.html', {'diapositivas': diapositivas})


@login_required
def actualizar_diapositiva(request, diapositiva_id):
    diapositiva = get_object_or_404(Diapositiva, pk=diapositiva_id)
    if request.method == 'POST':
        form = DiapositivaForm(request.POST, instance=diapositiva)
        if form.is_valid():
            form.save()
            return redirect('lista_diapositivas')  # Redirección actualizada a lista_diapositivas
    else:
        form = DiapositivaForm(instance=diapositiva)
    return render(request, 'core/actualizar_diapositiva.html', {'form': form})


@login_required
def borrar_diapositiva(request, diapositiva_id):
    diapositiva = get_object_or_404(Diapositiva, pk=diapositiva_id)
    diapositiva.delete()
    return redirect('lista_diapositivas')


def presentacion_completa(request):
    diapositivas = Diapositiva.objects.all()
    return render(request, 'core/presentacion_completa.html', {'diapositivas': diapositivas})

