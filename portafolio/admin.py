from django.contrib import admin

from .models import (
    Perfil,
    Proyecto,
    ProyectoImagen,
    RedSocial,
    Servicio,
    Tecnologia,
)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    """Configuracion principal del perfil profesional en el admin."""

    list_display = (
        'nombre_completo',
        'titulo_profesional',
        'ubicacion',
        'disponible',
        'actualizado',
    )
    search_fields = ('nombre', 'titulo_profesional', 'email', 'ubicacion')
    list_filter = ('disponible', 'ubicacion')
    list_editable = ('disponible',)
    readonly_fields = ('actualizado',)
    fieldsets = (
        (
            'Datos principales',
            {
                'fields': (
                    'nombre',
                    'titulo_profesional',
                    'ubicacion',
                    'descripcion_corta',
                    'descripcion_larga',
                    'avatar',
                )
            },
        ),
        (
            'Hero',
            {
                'fields': (
                    'subtitulo_hero',
                    'texto_boton_principal',
                    'texto_boton_secundario',
                )
            },
        ),
        (
            'Contacto',
            {
                'fields': (
                    'email',
                    'telefono_whatsapp',
                    'cv_url',
                )
            },
        ),
        (
            'GitHub',
            {
                'fields': (
                    'github_url',
                )
            },
        ),
        (
            'Estado',
            {
                'fields': (
                    'disponible',
                    'actualizado',
                )
            },
        ),
    )

    # Alias visible para que la lista del admin tenga una etiqueta mas clara.
    @admin.display(description='Nombre completo', ordering='nombre')
    def nombre_completo(self, obj):
        return obj.nombre

    # Campo de solo lectura compatible aunque el modelo aun no tenga auditoria.
    @admin.display(description='Actualizado')
    def actualizado(self, obj):
        return getattr(obj, 'actualizado', None) or '-'


@admin.register(RedSocial)
class RedSocialAdmin(admin.ModelAdmin):
    """Permite ordenar y activar redes sociales desde la lista."""

    list_display = ('nombre', 'url', 'icono', 'orden', 'visible')
    search_fields = ('nombre', 'url', 'icono')
    list_filter = ('visible',)
    list_editable = ('orden', 'visible')
    ordering = ('orden', 'nombre')


@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    """Admin del stack tecnico usado por proyectos y secciones."""

    list_display = ('nombre', 'categoria', 'icono', 'color', 'orden', 'visible')
    search_fields = ('nombre', 'categoria', 'icono')
    list_filter = ('categoria', 'visible')
    list_editable = ('categoria', 'color', 'orden', 'visible')
    ordering = ('orden', 'nombre')


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    """Servicios visibles en la pagina principal."""

    list_display = ('titulo', 'icono', 'orden', 'visible')
    search_fields = ('titulo', 'descripcion', 'icono')
    list_filter = ('visible',)
    list_editable = ('orden', 'visible')
    ordering = ('orden', 'titulo')


class ProyectoImagenInline(admin.TabularInline):
    """Inline para subir varias capturas dentro de cada proyecto."""

    model = ProyectoImagen
    extra = 1
    fields = ('titulo', 'imagen', 'descripcion', 'es_portada', 'orden', 'visible')


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    """Admin de proyectos destacados y repositorios enriquecidos."""

    list_display = (
        'titulo',
        'categoria',
        'repo_nombre',
        'destacado',
        'mostrar_en_home',
        'visible',
        'orden',
        'actualizado',
    )
    search_fields = (
        'titulo',
        'slug',
        'categoria',
        'repo_nombre',
        'descripcion_corta',
        'descripcion_profesional',
    )
    list_filter = ('categoria', 'destacado', 'mostrar_en_home', 'visible', 'tecnologias')
    list_editable = ('destacado', 'mostrar_en_home', 'visible', 'orden')
    prepopulated_fields = {'slug': ('titulo',)}
    filter_horizontal = ('tecnologias',)
    inlines = (ProyectoImagenInline,)
    readonly_fields = ('creado', 'actualizado')
    fieldsets = (
        (
            'Informacion principal',
            {
                'fields': (
                    'titulo',
                    'slug',
                    'descripcion_corta',
                    'descripcion_profesional',
                    'categoria',
                    'fecha',
                    'cliente',
                    'tecnologias',
                )
            },
        ),
        (
            'Caso de estudio',
            {
                'fields': (
                    'problema',
                    'solucion',
                    'resultado',
                )
            },
        ),
        (
            'Enlaces',
            {
                'fields': (
                    'repo_nombre',
                    'repo_url',
                    'demo_url',
                )
            },
        ),
        (
            'Configuracion de visualizacion',
            {
                'fields': (
                    'destacado',
                    'mostrar_en_home',
                    'visible',
                    'orden',
                    'creado',
                    'actualizado',
                )
            },
        ),
    )
    ordering = ('orden', 'titulo')

    # Campo de solo lectura compatible aunque el modelo aun no tenga auditoria.
    @admin.display(description='Creado')
    def creado(self, obj):
        return getattr(obj, 'creado', None) or '-'

    # Campo de solo lectura compatible aunque el modelo aun no tenga auditoria.
    @admin.display(description='Actualizado')
    def actualizado(self, obj):
        return getattr(obj, 'actualizado', None) or '-'


@admin.register(ProyectoImagen)
class ProyectoImagenAdmin(admin.ModelAdmin):
    """Gestion directa de capturas, ademas del inline en proyectos."""

    list_display = ('proyecto', 'titulo', 'es_portada', 'orden', 'visible')
    search_fields = ('titulo', 'descripcion', 'proyecto__titulo')
    list_filter = ('es_portada', 'visible', 'proyecto')
    list_editable = ('es_portada', 'orden', 'visible')
    ordering = ('proyecto', 'orden', 'titulo')
