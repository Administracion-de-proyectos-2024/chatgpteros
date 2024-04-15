from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
<<<<<<< HEAD
from .forms import CustomUserCreationForm, DiapositivaFormSet, PresentacionForm
from .models import Diapositiva, Presentacion
=======
from .forms import CustomUserCreationForm, DiapositivaForm
from .models import Diapositiva
>>>>>>> 641247feb2606a343b4839131593dc5d702af4e6
import markdown
from django.http import HttpResponse

import os


def home(request):  
    return render(request, 'core/home.html')
<<<<<<< HEAD

=======


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

>>>>>>> 641247feb2606a343b4839131593dc5d702af4e6

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
<<<<<<< HEAD
<<<<<<< Updated upstream:chatgpteros/core/views.py
    return render(request,'registration/register.html', data)
=======
    return render(request, 'registration/register.html', data)


"____________________________________________________________________________________________"

@login_required
def presentaciones_disponibles(request):
    presentaciones = Presentacion.objects.all()
    return render(request, 'pre/lista_presentaciones.html', {'presentaciones': presentaciones})

def nueva_presentacion(request):
    if request.method == 'POST':
        presentacion_form = PresentacionForm(request.POST)
        diapositiva_formset = DiapositivaFormSet(request.POST)
        
        if presentacion_form.is_valid() and diapositiva_formset.is_valid():
            presentacion = presentacion_form.save()  # Guardar la presentación primero
            
            for form in diapositiva_formset:
                diapositiva = form.save(commit=False)
                diapositiva.presentacion = presentacion  # Asignar la presentación a cada diapositiva
                
                # Imprimir datos de la diapositiva para depuración
                print("Datos de la diapositiva antes de guardarla:", diapositiva)
                print("Contenido de la diapositiva antes de guardarla:", diapositiva.contenido)
                
                diapositiva.save()
                print(f"Contenido de la diapositiva guardada correctamente: {diapositiva.contenido}")
                
            return redirect('core_app:detalle_presentacion', pk=presentacion.pk)
    else:
        presentacion_form = PresentacionForm()
        diapositiva_formset = DiapositivaFormSet(queryset=Diapositiva.objects.none())
    
    return render(request, 'pre/nueva_presentacion.html', {
        'presentacion_form': presentacion_form,
        'diapositiva_formset': diapositiva_formset
    })
=======
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

@login_required
def presentacion_completa(request):
    diapositivas = Diapositiva.objects.all()
    return render(request, 'core/presentacion_completa.html', {'diapositivas': diapositivas})
>>>>>>> 641247feb2606a343b4839131593dc5d702af4e6



@login_required
<<<<<<< HEAD
def detalle_presentacion(request, pk):
    presentacion = get_object_or_404(Presentacion, pk=pk)
    diapositivas = Diapositiva.objects.filter(presentacion=presentacion)
    print("Diapositivas:", diapositivas)  # Agregar este print
    return render(request, 'pre/detalle_presentacion.html', {'presentacion': presentacion, 'diapositivas': diapositivas})




>>>>>>> Stashed changes:chatgpteros/applications/core/views.py
=======
def ver_diapositiva(request, diapositiva_id):
    diapositiva = get_object_or_404(Diapositiva, pk=diapositiva_id)
    return render(request, 'core/ver_diapositiva.html', {'diapositiva': diapositiva})

>>>>>>> 641247feb2606a343b4839131593dc5d702af4e6
