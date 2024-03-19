from django.db import models
from django.contrib.auth.models import User

class Diapositiva(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    orden = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo
