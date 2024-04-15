from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Presentacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

class Diapositiva(models.Model):
    presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE)
    contenido = models.TextField()
