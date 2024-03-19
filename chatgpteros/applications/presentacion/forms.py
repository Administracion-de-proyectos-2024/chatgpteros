from django import forms

# Formulario para la cajar de texto para nueva presentacion
class TextForm(forms.Form):
    texto_pts = forms.CharField(label='Ingrese el texto para la presentación', widget=forms.Textarea())
