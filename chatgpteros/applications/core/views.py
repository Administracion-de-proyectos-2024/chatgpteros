from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
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
