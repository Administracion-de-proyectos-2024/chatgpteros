from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

def home(request):  
    return render(request,'core/home.html')

@login_required
def presentaciones(request):  
    return render(request,'core/presentaciones.html')

def exit(request):
    logout(request)
    return redirect('home')