from os.path import basename
from django.db import models

class Presentacion(models.Model):
    archivoTxt = models.FileField()

    def __str__(self):
        return basename(self.archivoTxt.name)
