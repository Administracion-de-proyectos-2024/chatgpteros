from django.shortcuts import render
from .forms import TextForm
from .models import Presentacion

def nueva(request):
    form = {
        'form': TextForm()
    }
    # Si se envia el formulario
    if request.method == 'POST':
        # Se genera nuevo archivo
        generar_archivo(request.POST.get("texto_pts"))
    return render(request, 'nueva_prest.html', form)

def generar_archivo(data):
    pass
