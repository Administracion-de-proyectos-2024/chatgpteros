from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, DiapositivaFormSet, PresentacionForm
from .models import Diapositiva, Presentacion
from django.core.files.storage import FileSystemStorage
from markdown.inlinepatterns import SimpleTagPattern
from .models import Diapositiva
import markdown
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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


def elegir_metodo_creacion(request):
    return render(request, 'pre/elegir_metodo_creacion.html')


def subir_archivo(request):
    if request.method == 'POST':
        if 'archivo' in request.FILES:  # Verifica si se ha seleccionado un archivo
            archivo = request.FILES['archivo']
            contenido = archivo.read().decode('utf-8')

            # Verifica que el contenido del archivo tenga las etiquetas correctas
            if not validar_etiquetas(contenido):
                messages.error(request, 'El archivo no tiene el formato correcto. Por favor, asegúrate de que contiene las etiquetas correctas.')
                return redirect('subir_archivo')

            fs = FileSystemStorage(location='C:\\Users\\asael\\OneDrive\\Documentos\\Pc\\Escritorio\\ProyectoAdmin\\chatgpteros\\chatgpteros\\archivos_.txt\\')  # Especifica la ruta donde quieres guardar los archivos
            nombre_archivo = fs.save(archivo.name, archivo)
            ruta_archivo = fs.path(nombre_archivo)
            
            # Aquí puedes llamar a la función que genera la presentación a partir del archivo
            generar_presentacion_desde_archivo(ruta_archivo, nombre_archivo)
            
            return redirect('presentaciones_disponibles')
        else:
            messages.error(request, 'Por favor, selecciona un archivo.')
    
    return render(request, 'pre/subir_archivo.html')


def validar_etiquetas(contenido):
    # Lista de las etiquetas que deben estar en el archivo
    etiquetas = ['# ', '## ', '####']

    # Verifica si cada etiqueta está en el contenido del archivo
    for etiqueta in etiquetas:
        if etiqueta not in contenido:
            print(f"La etiqueta {etiqueta} no se encontró en el contenido.")
            return False

    return True



def generar_presentacion_desde_archivo(ruta_archivo, nombre_archivo):
    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()
        
        # Extrae el nombre de la presentación del archivo y elimina las etiquetas
        nombre = lineas[0].strip().replace('# ', '')  
        
        # Extrae la descripción de la presentación del archivo y elimina las etiquetas
        descripcion = lineas[1].strip().replace('## ', '')  
        
        # Crea un nuevo objeto Presentacion
        presentacion = Presentacion(nombre=nombre, descripcion=descripcion, nombre_archivo=nombre_archivo)
        presentacion.save()  # Guarda la presentación en la base de datos
        
        # Extrae las diapositivas de la presentación del archivo
        diapositivas = []
        for linea in lineas[2:]:
            linea = linea.strip()  # Elimina los espacios en blanco al principio y al final de la línea
            if linea:  # Si la línea no está vacía
                if '\\newpage ' in linea:
                    diapositiva = {'contenido': linea.replace('\\newpage ', '')}
                    diapositivas.append(diapositiva)
        
        # Crea un nuevo objeto Diapositiva para cada diapositiva en el archivo
        for diapositiva in diapositivas:
            Diapositiva.objects.create(nombre=nombre, contenido=diapositiva['contenido'], presentacion=presentacion)




@login_required
def detalle_presentacion(request, pk):
    presentacion = Presentacion.objects.get(pk=pk)

    nombre_archivo = presentacion.nombre

    if nombre_archivo is not None:
        # Ruta del directorio donde se guardan los archivos
        ruta_directorio = os.path.join(BASE_DIR, "archivos_.md")
    
        # Ruta completa del archivo
        ruta_archivo = os.path.join(ruta_directorio, f"{presentacion.nombre}.md")
    
        # Leer el archivo
        with open(ruta_archivo, 'r') as archivo:
            lineas = archivo.readlines()

        # Procesar las líneas del archivo
        diapositivas = []
        diapositiva_actual = None
        for linea in lineas:
            if linea.startswith("# "):
                if diapositiva_actual:
                    diapositivas.append(diapositiva_actual)
                        
                diapositiva_actual = {'nombre': '', 'descripcion': '', 'subtitulo': '', 'contenido': ''}
                diapositiva_actual['nombre'] = linea.strip()
                
            elif linea.startswith("## "):
                
                diapositiva_actual['descripcion'] = linea.strip()
                diapositivas.append(diapositiva_actual)
                diapositiva_actual = {'nombre': '', 'descripcion': '', 'subtitulo': '', 'contenido': ''}
                
            elif linea.startswith("### "):
                
                if diapositiva_actual and diapositiva_actual['contenido']:
                    diapositivas.append(diapositiva_actual)
                    
                diapositiva_actual = {'nombre': '', 'descripcion': '', 'subtitulo': '', 'contenido': ''}
                diapositiva_actual['subtitulo'] = linea.strip()
                
            else:
                
                diapositiva_actual['contenido'] += linea.strip() + "\n"
                
        # Guardar la última diapositiva
        if diapositiva_actual and diapositiva_actual['contenido']:
            diapositivas.append(diapositiva_actual)
            
        # Convertir contenido Markdown a HTML
        for diapositiva in diapositivas:
            diapositiva['nombre'] = markdown.markdown(diapositiva['nombre'])
            diapositiva['descripcion'] = markdown.markdown(diapositiva['descripcion'])
            diapositiva['subtitulo'] = markdown.markdown(diapositiva['subtitulo'])
            diapositiva['contenido'] = markdown.markdown(diapositiva['contenido'])

        return render(request, 'pre/detalle_presentacion.html', {'diapositivas': diapositivas})
    else:
        nombre = presentacion.nombre
        descripcion = presentacion.descripcion
        diapositivas = Diapositiva.objects.filter(presentacion=presentacion)
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


def guardar_presentacion(presentacion):
    if presentacion.nombre_archivo is not None:
        # Ruta completa del archivo
        ruta_archivo  = os.path.join(BASE_DIR, "archivos_.txt", presentacion.nombre_archivo)
        
        # Verifica si el archivo ya existe
        if os.path.exists(ruta_archivo):
            modo = 'w'  # Si el archivo existe, abre en modo de escritura
        else:
            modo = 'x'  # Si el archivo no existe, crea un nuevo archivo
        
        # Guarda la presentación en el archivo
        with open(ruta_archivo, modo) as archivo:
            archivo.write('<titulo>' + presentacion.nombre + '</titulo>\n')
            archivo.write('<descripcion>' + presentacion.descripcion + '</descripcion>\n')
            archivo.write('<diapositivas>\n')
            for diapositiva in presentacion.diapositiva_set.all():
                archivo.write('    <diapositiva>' + diapositiva.contenido + '</diapositiva>\n')
                if diapositiva.subtitulo:
                    archivo.write('    <subtitulo>' + diapositiva.subtitulo + '</subtitulo>\n')
            archivo.write('</diapositivas>\n')
    else:
        print("No hay un archivo asociado con la presentación", presentacion.nombre)




def eliminar_presentacion(request, pk):
    presentacion = get_object_or_404(Presentacion, pk=pk)
    
    if request.method == 'POST':
        # Ruta del directorio donde se guardan los archivos
        ruta_directorio  = os.path.join(BASE_DIR, "archivos_.txt")
        
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
    nombre_archivo = f"{presentacion.nombre}.md"
    
    # Ruta del directorio donde deseas guardar los archivos
    ruta_directorio  = os.path.join(BASE_DIR, "archivos_.md")
    
    # Si la ruta no existe, crea el directorio
    if not os.path.exists(ruta_directorio):
        os.makedirs(ruta_directorio)
    
    # Ruta completa del archivo
    ruta_archivo = os.path.join(ruta_directorio, nombre_archivo)
    
    # Contenido del archivo
    contenido = f"# {presentacion.nombre}\n"
    contenido += f"## {presentacion.descripcion}\n"

    for diapositiva in presentacion.diapositiva_set.all():
        if diapositiva.subtitulo:
            contenido += f"### {diapositiva.subtitulo}\n"
        contenido += f" {diapositiva.contenido}\n"
    
    # Escribir en el archivo
    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(contenido)

        