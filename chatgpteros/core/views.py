from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from .models import Diapositiva


# Create your views here.

def home(request):  
    return render(request,'core/home.html')

@login_required
def presentaciones(request):  
    return render(request,'core/presentaciones.html')

def exit(request):
    logout(request)
    return redirect('home')

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            return redirect('home')
    return render(request,'registration/register.html', data)

@login_required
def presentaciones(request):
    presentaciones = Diapositiva.objects.filter(usuario=request.user).order_by('orden')
    return render(request, 'core/presentaciones.html', {'presentaciones': presentaciones})


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


def borrar_presentacion(request, presentacion_id):
    presentacion = Presentacion.objects.get(pk=presentacion_id)
    presentacion.delete()
    return redirect('lista_presentaciones')


