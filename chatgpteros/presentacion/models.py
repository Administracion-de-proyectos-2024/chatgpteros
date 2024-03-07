from django.db import models

class Presentacion(models.Model):
    archivoTxt = models.FileField()