from django.db import models

class Presentacion(models.Model):
    archivoTxt = models.FileField()

    def __str__(self):
        return self.archivoTxt.name
