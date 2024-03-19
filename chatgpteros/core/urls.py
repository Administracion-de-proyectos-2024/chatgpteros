
from django.urls import path
from .views import home, presentaciones,exit,register
from .views import borrar_presentacion

urlpatterns = [
    path('', home, name='home'),
    path('presentaciones/', presentaciones, name='presentaciones'),
    path('logout/', exit, name='exit'),
    path('register/', register, name='register'),
    path('borrar_presentacion/<int:presentacion_id>/', borrar_presentacion, name='borrar_presentacion'),
   

]
