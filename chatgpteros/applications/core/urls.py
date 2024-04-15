from django.urls import path
from . import views
from .views import home, exit, register

app_name = "core_app"

urlpatterns = [
    path('', home, name='home'),
    path('logout/', exit, name='exit'),
    path('register/', register, name='register'),

    path('presentaciones/disponible/', views.presentaciones_disponibles, name='presentaciones_disponibles'),
    path('presentacion/nueva/', views.nueva_presentacion, name='nueva_presentacion'),
    path('detalle-presentaciones/<int:pk>/', views.detalle_presentacion, name='detalle_presentacion'),
]

