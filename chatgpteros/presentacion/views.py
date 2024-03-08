from django.shortcuts import render
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
    return render(request, 'nueva_prest.html', form)

def generar_archivo(data):
    ficheroArchivos = os.path.join(str(BASE_DIR), 'archivos_txt')
    nombreUnico = False
    while not nombreUnico:
        try:
            nombre_archivo = generar_nombre_archivo()
            path_completo = os.path.join(ficheroArchivos, nombre_archivo)
            with open(path_completo, "x") as nuevo_fichero:
                nuevo_fichero.write(data)
            # Crear instancia de Presentacion y asignar el nombre del archivo al campo archivoTxt
            nuevaPresentacion = Presentacion.objects.create(archivoTxt=nombre_archivo)
            nombreUnico = True
        except FileExistsError:
            nombreUnico = False

def generar_nombre_archivo():
    # Generar un nombre de archivo aleatorio con un máximo de 5 caracteres
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=5)) + '.txt'