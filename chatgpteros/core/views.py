from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, DiapositivaFormSet, PresentacionForm
from .models import Diapositiva, Presentacion
import markdown
from django.http import HttpResponse

import os


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



@login_required
def detalle_presentacion(request, pk):
    presentacion = get_object_or_404(Presentacion, pk=pk)
    diapositivas = Diapositiva.objects.filter(presentacion=presentacion)
    print("Diapositivas:", diapositivas)  # Agregar este print
    return render(request, 'pre/detalle_presentacion.html', {'presentacion': presentacion, 'diapositivas': diapositivas})




>>>>>>> Stashed changes:chatgpteros/applications/core/views.py
