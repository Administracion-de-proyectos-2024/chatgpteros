from django.urls import path
from .views import nueva, listaPresentaciones, presentar

urlpatterns = [
    path('', listaPresentaciones, name='lista_presentaciones'),
    path('nueva/', nueva, name='nueva'),
    path('<int:id>',presentar, name='presentar')
]