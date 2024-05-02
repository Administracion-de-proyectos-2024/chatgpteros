from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.exit, name='exit'),
    path('register/', views.register, name='register'),

    path('presentaciones/disponible/', views.presentaciones_disponibles, name='presentaciones_disponibles'),
    path('presentacion/nueva/', views.nueva_presentacion, name='nueva_presentacion'),
    path('detalle-presentaciones/<int:pk>/', views.detalle_presentacion, name='detalle_presentacion'),

    path('presentacion/<int:pk>/editar/', views.editar_presentacion, name='editar_presentacion'),
    path('presentacion/<int:pk>/eliminar/', views.eliminar_presentacion, name='eliminar_presentacion'),
]
