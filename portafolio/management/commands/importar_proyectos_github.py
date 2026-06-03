import requests

from django.core.management.base import BaseCommand

from portafolio.models import Proyecto


GITHUB_USER = 'jematti'
GITHUB_API_URL = (
    f'https://api.github.com/users/{GITHUB_USER}/repos?sort=updated&per_page=100'
)

REPOS_DESTACADOS = {
    'web-empresa': {
        'titulo': 'Web Empresa Cafeteria',
        'slug': 'web-empresa-cafeteria',
        'categoria': 'Sitio web empresarial',
        'descripcion_corta': (
            'Sitio web para una empresa de cafeteria, enfocado en presentacion '
            'de marca, productos y contacto comercial.'
        ),
        'descripcion_larga': (
            'Pagina web orientada a presentar una cafeteria de forma profesional, '
            'mostrando identidad visual, productos, informacion comercial y '
            'canales de contacto.'
        ),
        'orden': 2,
    },
    'biblioteca-digital-FCBCB-2024': {
        'titulo': 'Biblioteca Digital FCBCB 2024',
        'slug': 'biblioteca-digital-fcbcb-2024',
        'categoria': 'Biblioteca digital institucional',
        'descripcion_corta': (
            'Biblioteca digital institucional responsive para organizacion y '
            'consulta de recursos culturales y documentales.'
        ),
        'descripcion_larga': (
            'Proyecto orientado a la publicacion y consulta de contenidos '
            'digitales institucionales, con enfoque en accesibilidad, estructura '
            'clara y navegacion responsive.'
        ),
        'orden': 3,
    },
    'tickets-soporte': {
        'titulo': 'Sistema de Tickets de Soporte',
        'slug': 'tickets-soporte',
        'categoria': 'Sistema de soporte TI',
        'descripcion_corta': (
            'Sistema para registro, seguimiento y gestion de solicitudes de '
            'soporte tecnico.'
        ),
        'descripcion_larga': (
            'Aplicacion orientada a organizar incidencias, solicitudes tecnicas '
            'y seguimiento de atencion mediante un flujo administrable de '
            'tickets.'
        ),
        'orden': 4,
    },
    'intranet': {
        'titulo': 'Intranet Institucional',
        'slug': 'intranet-institucional',
        'categoria': 'Sistema interno corporativo',
        'descripcion_corta': (
            'Intranet corporativa con autenticacion, dashboard administrativo y '
            'gestion de archivos institucionales.'
        ),
        'descripcion_larga': (
            'Sistema interno desarrollado para centralizar acceso a informacion, '
            'documentos y herramientas institucionales mediante una plataforma '
            'privada y administrable.'
        ),
        'orden': 5,
    },
    'TiendaVirtual': {
        'titulo': 'Tienda Virtual E-commerce',
        'slug': 'tienda-virtual',
        'categoria': 'E-commerce',
        'descripcion_corta': (
            'Tienda virtual con catalogo, carrito, gestion de pedidos y '
            'administracion de productos.'
        ),
        'descripcion_larga': (
            'Proyecto e-commerce desarrollado como sistema de tienda virtual, '
            'con funcionalidades para clientes y administracion.'
        ),
        'orden': 6,
    },
}

PROYECTO_MANUAL = {
    'repo_nombre': 'plataforma-laboral',
    'titulo': "Plataforma Laboral MANQ'A",
    'slug': 'plataforma-laboral',
    'categoria': 'Sistema web Django',
    'descripcion_corta': (
        'Sistema web para seguimiento laboral, gestion de estudiantes, empresas, '
        'vacantes, postulaciones y reportes.'
    ),
    'descripcion_larga': (
        'Plataforma desarrollada para centralizar el seguimiento laboral de '
        'estudiantes y exalumnos, conectando empresas, oportunidades, '
        'postulaciones y reportes en un sistema administrable.'
    ),
    'problema': (
        'La informacion laboral podia quedar dispersa entre planillas, '
        'formularios y comunicaciones manuales.'
    ),
    'solucion': (
        'Se diseno una plataforma web modular con gestion de estudiantes, '
        'empresas, vacantes, postulaciones, orientacion laboral y reportes.'
    ),
    'resultado': (
        'Sistema preparado para demo institucional, seguimiento centralizado y '
        'futuras mejoras.'
    ),
    'orden': 1,
}


class Command(BaseCommand):
    help = 'Importa o actualiza proyectos destacados del portafolio desde GitHub.'

    def handle(self, *args, **options):
        repos_github = self.obtener_repositorios()

        for repo_nombre, datos in REPOS_DESTACADOS.items():
            repo = repos_github.get(repo_nombre)
            if not repo:
                self.stdout.write(
                    self.style.WARNING(
                        f'Warning: el repositorio "{repo_nombre}" no aparece en GitHub.'
                    )
                )

            self.guardar_proyecto(
                repo_nombre=repo_nombre,
                datos=datos,
                repo=repo,
            )

        # Proyecto adicional creado manualmente aunque todavia no sea publico.
        self.guardar_proyecto(
            repo_nombre=PROYECTO_MANUAL['repo_nombre'],
            datos=PROYECTO_MANUAL,
            repo=None,
        )

        self.stdout.write(
            self.style.SUCCESS('Importacion de proyectos destacados finalizada.')
        )

    def obtener_repositorios(self):
        """Consulta GitHub y devuelve los repositorios indexados por nombre."""
        try:
            response = requests.get(GITHUB_API_URL, timeout=15)
            response.raise_for_status()
        except requests.RequestException as exc:
            self.stdout.write(
                self.style.WARNING(
                    f'Warning: no se pudo consultar GitHub. Detalle: {exc}'
                )
            )
            return {}

        repositorios = response.json()
        return {
            repo.get('name'): repo
            for repo in repositorios
            if repo.get('name')
        }

    def guardar_proyecto(self, repo_nombre, datos, repo=None):
        """Crea o actualiza un Proyecto usando solo campos existentes."""
        defaults = self.construir_defaults(repo_nombre, datos, repo)

        proyecto, creado = Proyecto.objects.update_or_create(
            slug=datos['slug'],
            defaults=defaults,
        )

        accion = 'creado' if creado else 'actualizado'
        self.stdout.write(f'Proyecto {accion}: {proyecto.titulo}')

    def construir_defaults(self, repo_nombre, datos, repo=None):
        """Prepara los valores del modelo y respeta campos opcionales."""
        repo = repo or {}
        campos_modelo = {field.name for field in Proyecto._meta.fields}

        # La descripcion de GitHub solo se usa como apoyo si falta el texto manual.
        descripcion_github = repo.get('description') or ''
        descripcion_corta = datos.get('descripcion_corta') or descripcion_github
        descripcion_larga = datos.get('descripcion_larga') or descripcion_github

        defaults = {
            'titulo': datos['titulo'],
            'descripcion_corta': descripcion_corta,
            'categoria': datos['categoria'],
            'repo_nombre': repo_nombre,
            'repo_url': repo.get('html_url', ''),
            'destacado': True,
            'visible': True,
            'orden': datos['orden'],
        }

        if 'descripcion_profesional' in campos_modelo:
            defaults['descripcion_profesional'] = descripcion_larga

        if 'descripcion_larga' in campos_modelo:
            defaults['descripcion_larga'] = descripcion_larga

        if 'mostrar_en_home' in campos_modelo:
            defaults['mostrar_en_home'] = True

        # Campos de caso de estudio: se agregan solo si existen en el modelo.
        for campo in ('problema', 'solucion', 'resultado'):
            if campo in campos_modelo and campo in datos:
                defaults[campo] = datos[campo]

        return defaults
