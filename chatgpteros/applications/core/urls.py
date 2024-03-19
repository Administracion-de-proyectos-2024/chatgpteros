from django.urls import path
from .views import home, presentaciones,exit,register
app_name = "core_app"
urlpatterns = [
    path('', home, name='home'),
    path('presentaciones/', presentaciones, name='presentaciones'),
    path('logout/', exit, name='exit'),
    path('register/', register, name='register'),

]
