# dashboard/urls.py
from django.urls import path
from . import views  # Importar las vistas de la aplicación

urlpatterns = [
    path('', views.index, name='index'),  # Ruta raíz para la vista 'index'
]
