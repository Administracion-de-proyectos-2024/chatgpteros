from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Presentacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    contenido = models.TextField()

class Diapositiva(models.Model):
    nombre = models.CharField(max_length=100)
    presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE)
    contenido = models.TextField()


# Model que representa las notificaciones que se envían a los usuarios dentro de aplicación
class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)