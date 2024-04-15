from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Diapositiva, Presentacion
from .models import Diapositiva


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class PresentacionForm(forms.ModelForm):
    class Meta:
        model = Presentacion
        fields = ['nombre', 'descripcion']


class DiapositivaForm(forms.ModelForm):
    class Meta:
        model = Diapositiva
        fields = ['contenido']

DiapositivaFormSet = forms.inlineformset_factory(Presentacion, Diapositiva, form=DiapositivaForm, extra=1, can_delete=False)


