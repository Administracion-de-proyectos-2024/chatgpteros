from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, DiapositivaForm
from .models import Diapositiva
import markdown

def home(request):  
    return render(request, 'core/home.html')

@login_required
def presentaciones(request):
    presentaciones = Diapositiva.objects.filter(usuario=request.user).order_by('orden')
    return render(request, 'core/presentaciones.html', {'presentaciones': presentaciones})

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
            return redirect('presentaciones')
    else:
        form = DiapositivaForm(instance=diapositiva)
    return render(request, 'core/actualizar_diapositiva.html', {'form': form})

@login_required
def borrar_diapositiva(request, diapositiva_id):
    diapositiva = get_object_or_404(Diapositiva, pk=diapositiva_id)
    diapositiva.delete()
    return redirect('lista_diapositivas')
