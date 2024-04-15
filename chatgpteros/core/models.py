from django.db import models
from django.contrib.auth.models import User
<<<<<<< HEAD

from django.db import models

class Presentacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

class Diapositiva(models.Model):
    presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE)
    contenido = models.TextField()
=======

class Diapositiva(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    orden = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo
>>>>>>> 641247feb2606a343b4839131593dc5d702af4e6
