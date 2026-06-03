from django.urls import path
from . import views


urlpatterns = [
    # Ruta principal del portafolio
    path('', views.home, name='home'),
]