from django.urls import path
from .views import home, presentaciones, exit, register, crear_diapositiva, borrar_diapositiva, actualizar_diapositiva, lista_diapositivas, presentacion_completa, presentaciones_archivos_txt

urlpatterns = [
    path('', home, name='home'),
    path('presentaciones/', presentaciones, name='presentaciones'),
    path('logout/', exit, name='exit'),
    path('register/', register, name='register'),
    path('crear_diapositiva/', crear_diapositiva, name='crear_diapositiva'),
    path('lista_diapositivas/', lista_diapositivas, name='lista_diapositivas'),
    path('borrar_diapositiva/<int:diapositiva_id>/', borrar_diapositiva, name='borrar_diapositiva'),
    path('actualizar_diapositiva/<int:diapositiva_id>/', actualizar_diapositiva, name='actualizar_diapositiva'),
    path('presentacion-completa/', presentacion_completa, name='presentacion_completa'),
    path('presentaciones-archivos-txt/', presentaciones_archivos_txt, name='presentaciones_archivos_txt'),
]

