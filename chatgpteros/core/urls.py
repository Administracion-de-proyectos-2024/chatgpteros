
from django.urls import path
from .views import home, presentaciones,exit,register
from .views import (
    home,
    presentaciones,
    crear_diapositiva,
    borrar_diapositiva,
    actualizar_diapositiva,
    lista_diapositivas,
)

urlpatterns = [
    path('', home, name='home'),
    path('presentaciones/', presentaciones, name='presentaciones'),
    path('logout/', exit, name='exit'),
    path('register/', register, name='register'),
    path('crear_diapositiva/', crear_diapositiva, name='crear_diapositiva'),
    path('lista_diapositivas/', lista_diapositivas, name='lista_diapositivas'),
    path('borrar_presentacion/<int:presentacion_id>/', borrar_diapositiva, name='borrar_presentacion'),
    path('actualizar_diapositiva/<int:diapositiva_id>/', actualizar_diapositiva, name='actualizar_diapositiva'),
   

]
