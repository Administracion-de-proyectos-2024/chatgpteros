from django.urls import path
from .views import nueva, listaPresentaciones, presentar

app_name = "presentacion_app"
urlpatterns = [
    path('presentacion/', listaPresentaciones, name='lista_presentaciones'),
    path('nueva/', nueva, name='nueva'),
    path('<int:id>',presentar, name='presentar')
]