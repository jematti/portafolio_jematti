from datetime import datetime

import requests

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from .models import Perfil, Proyecto, RedSocial, Servicio, Tecnologia


def robots_txt(request):
    """Archivo robots.txt simple para permitir indexacion del portafolio."""
    contenido = (
        'User-agent: *\n'
        'Allow: /\n\n'
        'Sitemap: /sitemap.xml\n'
    )
    return HttpResponse(contenido, content_type='text/plain')


def sitemap_xml(request):
    """Sitemap basico con la URL principal; cambiar SITE_URL al dominio final."""
    site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000/')
    site_url = site_url if site_url.endswith('/') else f'{site_url}/'
    contenido = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{site_url}</loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>
'''
    return HttpResponse(contenido, content_type='application/xml')


def formatear_fecha_github(fecha_github):
    """Convierte la fecha tecnica de GitHub en una fecha legible."""
    if not fecha_github:
        return 'Sin fecha'

    try:
        fecha = datetime.strptime(fecha_github, '%Y-%m-%dT%H:%M:%SZ')
        return fecha.strftime('%d %b %Y')
    except ValueError:
        return 'Fecha no disponible'


def home(request):
    """
    Vista principal del portafolio.

    Carga informacion editable desde Django Admin y agrega metadatos publicos
    de GitHub cuando un proyecto tiene un repositorio asociado.
    """
    perfil = Perfil.objects.first()
    redes_sociales = RedSocial.objects.filter(visible=True)
    tecnologias = Tecnologia.objects.filter(visible=True)
    servicios = Servicio.objects.filter(visible=True)

    # Filtro base de la vitrina: solo proyectos visibles y destacados.
    filtros_proyectos = {
        'destacado': True,
        'visible': True,
    }

    # Si el modelo incluye mostrar_en_home, se usa para controlar el home.
    campos_proyecto = {field.name for field in Proyecto._meta.fields}
    if 'mostrar_en_home' in campos_proyecto:
        filtros_proyectos['mostrar_en_home'] = True

    proyectos_destacados = list(
        Proyecto.objects.filter(**filtros_proyectos).prefetch_related(
            'tecnologias',
            'imagenes',
        )
    )

    repos_github = {}
    error_github = None
    github_usuario = getattr(perfil, 'github_usuario', None) or 'jematti'

    try:
        # La consulta se hace en backend para controlar errores de red/API.
        response = requests.get(
            (
                f'https://api.github.com/users/{github_usuario}/repos'
                '?sort=updated&per_page=100'
            ),
            timeout=10,
        )
        response.raise_for_status()

        repositorios = [
            repo for repo in response.json()
            if not repo.get('fork')
        ]

        # Se agrega una fecha legible por si el template la necesita.
        for repo in repositorios:
            repo['updated_at_formatted'] = formatear_fecha_github(
                repo.get('updated_at')
            )

        # Diccionario por nombre para cruzar rapidamente con repo_nombre.
        repos_github = {
            repo.get('name'): repo
            for repo in repositorios
            if repo.get('name')
        }
    except requests.RequestException:
        # El home debe seguir funcionando aunque GitHub no responda.
        error_github = 'No se pudieron cargar los repositorios de GitHub.'

    # Metadatos dinamicos usados por el template de proyectos destacados.
    for proyecto in proyectos_destacados:
        repo = repos_github.get(proyecto.repo_nombre)

        if repo:
            proyecto.github_stars = repo.get('stargazers_count', 0)
            proyecto.github_language = repo.get('language', '')
            proyecto.github_url = repo.get('html_url') or proyecto.repo_url
            proyecto.github_updated_at = repo.get(
                'updated_at_formatted',
                'Sin fecha',
            )
        else:
            proyecto.github_stars = 0
            proyecto.github_language = ''
            proyecto.github_url = proyecto.repo_url
            proyecto.github_updated_at = 'Sin fecha'

    context = {
        'perfil': perfil,
        'redes_sociales': redes_sociales,
        'tecnologias': tecnologias,
        'servicios': servicios,
        'proyectos_destacados': proyectos_destacados,
        'error_github': error_github,
    }

    return render(request, 'portafolio/home.html', context)
