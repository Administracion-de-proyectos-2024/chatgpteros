from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, DiapositivaFormSet, PresentacionForm
from .models import Diapositiva, Presentacion
from .forms import CustomUserCreationForm, DiapositivaForm
from .models import Diapositiva
import markdown
from django.http import HttpResponse
import os
from chatgpteros.settings import BASE_DIR


def home(request):  
    return render(request, 'core/home.html')


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

    return render(request,'registration/register.html', data)


"____________________________________________________________________________________________"

@login_required
def presentaciones_disponibles(request):
    presentaciones = Presentacion.objects.all()
    return render(request, 'pre/lista_presentaciones.html', {'presentaciones': presentaciones})

@login_required
def nueva_presentacion(request):
    if request.method == 'POST':
        presentacion_form = PresentacionForm(request.POST)
        diapositiva_formset = DiapositivaFormSet(request.POST)
        
        if presentacion_form.is_valid() and diapositiva_formset.is_valid():
            presentacion = presentacion_form.save()  # Guardar la presentación primero
            
            for form in diapositiva_formset:
                diapositiva = form.save(commit=False)
                diapositiva.presentacion = presentacion  # Asignar la presentación a cada diapositiva
                diapositiva.save()
            
            # Llamar a la función para generar el archivo de texto
            generar_archivo_presentacion(presentacion)
            
            return redirect('presentaciones_disponibles')
    else:
        presentacion_form = PresentacionForm()
        diapositiva_formset = DiapositivaFormSet(queryset=Diapositiva.objects.none())
    
    return render(request, 'pre/nueva_presentacion.html', {
        'presentacion_form': presentacion_form,
        'diapositiva_formset': diapositiva_formset
    })

@login_required
def detalle_presentacion(request, pk):
    presentacion = Presentacion.objects.get(pk=pk)
    
    # Ruta del directorio donde se guardan los archivos
    ruta_directorio  = os.path.join(BASE_DIR, 'archivos_.txt')

    # Ruta completa del archivo
    ruta_archivo = os.path.join(ruta_directorio, f"{presentacion.nombre}.txt")
    
    # Leer el archivo
    with open(ruta_archivo, 'r') as archivo:
        contenido = archivo.read()
    
    # Dividir el contenido en líneas
    lineas = contenido.split('\n')
    
    # Extraer el nombre y la descripción de la presentación
    nombre = lineas[0].replace('<titulo>', '').replace('</titulo>', '')
    descripcion = lineas[1].replace('<descripcion>', '').replace('</descripcion>', '')
    
    # Extraer las diapositivas
    diapositivas = []
    for linea in lineas[2:]:
        if '<diapositiva>' in linea and '</diapositiva>' in linea:
            diapositiva = linea.replace('<diapositiva>', '').replace('</diapositiva>', '')
            diapositivas.append(diapositiva)
    
    return render(request, 'pre/detalle_presentacion.html', {'nombre': nombre, 'descripcion': descripcion, 'diapositivas': diapositivas})




def editar_presentacion(request, pk):
    presentacion = get_object_or_404(Presentacion, pk=pk)
    
    if request.method == 'POST':
        presentacion_form = PresentacionForm(request.POST, instance=presentacion)
        diapositiva_formset = DiapositivaFormSet(request.POST, instance=presentacion)
        
        if presentacion_form.is_valid() and diapositiva_formset.is_valid():
            presentacion_form.save()
            diapositiva_formset.save()

            # Actualizar el archivo .txt
            generar_archivo_presentacion(presentacion)

            return redirect('presentaciones_disponibles')
    else:
        presentacion_form = PresentacionForm(instance=presentacion)
        diapositiva_formset = DiapositivaFormSet(instance=presentacion)
    
    return render(request, 'pre/editar_presentacion.html', {'presentacion_form': presentacion_form, 'diapositiva_formset': diapositiva_formset})



def eliminar_presentacion(request, pk):
    presentacion = get_object_or_404(Presentacion, pk=pk)
    
    if request.method == 'POST':
        # Ruta del directorio donde se guardan los archivos
        ruta_directorio  = os.path.join(BASE_DIR, 'chatgpteros', 'archivos_.txt')
        
        # Ruta completa del archivo
        ruta_archivo = os.path.join(ruta_directorio, f"{presentacion.nombre}.txt")
        
        # Eliminar el archivo .txt
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)
        
        # Eliminar la presentación de la base de datos
        presentacion.delete()
        
        return redirect('presentaciones_disponibles')
    
    return render(request, 'pre/eliminar_presentacion.html', {'presentacion': presentacion})

def generar_archivo_presentacion(presentacion):
    # Nombre del archivo
    nombre_archivo = f"{presentacion.nombre}.txt"
    
    # Ruta del directorio donde deseas guardar los archivos
    ruta_directorio  = os.path.join(BASE_DIR, 'chatgpteros', 'archivos_.txt')

    # Si la ruta no existe, crea el directorio
    if not os.path.exists(ruta_directorio):
        os.makedirs(ruta_directorio)
    
    # Ruta completa del archivo
    ruta_archivo = os.path.join(ruta_directorio, nombre_archivo)
    
    # Contenido del archivo
    contenido = f"<titulo>{presentacion.nombre}</titulo>\n"
    contenido += f"<descripcion>{presentacion.descripcion}</descripcion>\n"
    contenido += "<diapositivas>\n"
    for diapositiva in presentacion.diapositiva_set.all():
        contenido += f"\t<diapositiva>{diapositiva.contenido}</diapositiva>\n"
    
    # Escribir en el archivo
    with open(ruta_archivo, 'w') as archivo:
        archivo.write(contenido)
        