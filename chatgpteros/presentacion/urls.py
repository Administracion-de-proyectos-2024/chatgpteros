from django.urls import path
from .views import nueva

urlpatterns = [
    path('nueva/', nueva, name='nueva'),
]