from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
<<<<<<< HEAD
from .models import Diapositiva, Presentacion
=======
from .models import Diapositiva  # Asegúrate de importar el modelo Presentacion desde tu aplicación
>>>>>>> 641247feb2606a343b4839131593dc5d702af4e6

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


<<<<<<< HEAD
class PresentacionForm(forms.ModelForm):
    class Meta:
        model = Presentacion
        fields = ['nombre', 'descripcion']
=======
>>>>>>> 641247feb2606a343b4839131593dc5d702af4e6

class DiapositivaForm(forms.ModelForm):
    class Meta:
        model = Diapositiva
<<<<<<< HEAD
        fields = ['contenido']

DiapositivaFormSet = forms.inlineformset_factory(Presentacion, Diapositiva, form=DiapositivaForm, extra=1, can_delete=False)
=======
        fields = ['titulo', 'contenido', 'orden']
>>>>>>> 641247feb2606a343b4839131593dc5d702af4e6

