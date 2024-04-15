from django.contrib import admin

from applications.core.models import Diapositiva, Presentacion

# Register your models here.
admin.site.register(Presentacion)
admin.site.register(Diapositiva)