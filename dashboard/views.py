# dashboard/views.py
from django.shortcuts import render
import requests
from django.conf import settings

# Vista para renderizar la plantilla 'index.html'
def index(request):
    response = requests.get(settings.API_URL)  # URL de la API
    posts = response.json()  # Convertir la respuesta a JSON

    # Número total de respuestas
    total_responses = len(posts)
    data = {
        'title': "Dashboard",
        'total_responses': total_responses,
        
    }

    return render(request, 'dashboard/index.html', data)
