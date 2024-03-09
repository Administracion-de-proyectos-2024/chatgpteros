from django.urls import path
from .views import nueva, listaPresentaciones

urlpatterns = [
    path('', listaPresentaciones, name='lista_presentaciones'),
    path('nueva/', nueva, name='nueva'),
]