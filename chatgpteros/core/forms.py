from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Diapositiva  # Asegúrate de importar el modelo Presentacion desde tu aplicación

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']



class DiapositivaForm(forms.ModelForm):
    class Meta:
        model = Diapositiva
        fields = ['titulo', 'contenido', 'orden']

