from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Presentacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    contenido = models.TextField()
    nombre_archivo = models.CharField(max_length=200, blank=True, null=True)
    vista_previa = models.ImageField(upload_to='vistas_previas/', blank=True, null=True)

class Diapositiva(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    subtitulo = models.CharField(max_length=200, blank=True, null=True)
    presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE)
    contenido = models.TextField()


