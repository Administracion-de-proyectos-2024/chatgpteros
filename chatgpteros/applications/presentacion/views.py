from django.shortcuts import render, get_object_or_404
from .forms import TextForm
from .models import Presentacion
from chatgpteros.settings import BASE_DIR
import string
import random
import os

def nueva(request):
    form = {
        'form': TextForm()
    }
    # Si se envia el formulario
    if request.method == 'POST':
        # Se genera nuevo archivo
        texto_formulario = request.POST.get("texto_pts")
        generar_archivo(texto_formulario)
    return render(request, 'presentacion/nueva_prest.html', form)

def listaPresentaciones(request):
    allPtts = Presentacion.objects.all()
    return render(request, 'presentacion/lista_ptts.html', {'presentaciones': allPtts})

def presentar(request, id=None):
    contenido = ""
    if id:
        presentacion = get_object_or_404(Presentacion, id=id)
        # Construir la ruta completa al archivo utilizando BASE_DIR y el nombre del archivo
        ruta_archivo = os.path.join(BASE_DIR, 'archivos_txt', presentacion.archivoTxt.name)
        try:
            with open(ruta_archivo, 'r') as archivo:
                contenido = archivo.read()
        except FileNotFoundError:
            # Manejar el caso en que el archivo no se encuentre
            contenido = "El archivo no se encontró"
    return render(request, 'presentacion/pag_presentar.html', {'contenido': contenido})

def generar_archivo(data):
    ficheroArchivos = os.path.join(str(BASE_DIR), 'archivos_txt')
    nombreUnico = False
    while not nombreUnico:
        try:
            nombre_archivo = generar_nombre_archivo()
            path_completo = os.path.join(ficheroArchivos, nombre_archivo)
            with open(path_completo, "x") as nuevo_fichero:
                nuevo_fichero.write(data)
            # Crear instancia de Presentacion y asignar la ruta completa del archivo al campo archivoTxt
            nuevaPresentacion = Presentacion.objects.create(archivoTxt=path_completo)
            nombreUnico = True
        except FileExistsError:
            nombreUnico = False


def generar_nombre_archivo():
    # Generar un nombre de archivo aleatorio con un máximo de 5 caracteres
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=5)) + '.txt'