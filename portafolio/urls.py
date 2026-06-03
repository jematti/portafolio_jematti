from django.urls import path
from . import views


urlpatterns = [
    # Ruta principal del portafolio
    path('', views.home, name='home'),
    # Archivos publicos basicos para SEO tecnico.
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
]
