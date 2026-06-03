from django.db import models


class Perfil(models.Model):
    """Información principal que aparece en el hero y la identidad del sitio."""

    nombre = models.CharField(max_length=150)
    titulo_profesional = models.CharField(max_length=180)
    # Textos configurables para personalizar la seccion hero desde el admin.
    subtitulo_hero = models.CharField(max_length=220, blank=True)
    ubicacion = models.CharField(max_length=120, default='Bolivia')
    email = models.EmailField()
    descripcion_corta = models.CharField(max_length=280)
    descripcion_larga = models.TextField()
    avatar = models.ImageField(upload_to='perfil/', blank=True, null=True)
    github_url = models.URLField(blank=True)
    texto_boton_principal = models.CharField(max_length=80, default='Ver proyectos')
    texto_boton_secundario = models.CharField(max_length=80, default='Contactarme')
    cv_url = models.URLField(blank=True)
    telefono_whatsapp = models.CharField(max_length=40, blank=True)
    disponible = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class RedSocial(models.Model):
    """Enlaces externos del portafolio, como GitHub, LinkedIn o correo."""

    nombre = models.CharField(max_length=80)
    url = models.URLField()
    icono = models.CharField(
        max_length=80,
        help_text='Clase de icono, por ejemplo: bi bi-github.',
    )
    orden = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Red social'
        verbose_name_plural = 'Redes sociales'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre


class Tecnologia(models.Model):
    """Tecnologías y herramientas que se muestran en el stack técnico."""

    nombre = models.CharField(max_length=80)
    categoria = models.CharField(max_length=80)
    icono = models.CharField(
        max_length=80,
        blank=True,
        help_text='Clase de icono o identificador visual.',
    )
    color = models.CharField(
        max_length=20,
        blank=True,
        help_text='Color hexadecimal opcional, por ejemplo: #00e5ff.',
    )
    orden = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Tecnología'
        verbose_name_plural = 'Tecnologías'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    """Servicios profesionales ofrecidos en la página."""

    titulo = models.CharField(max_length=120)
    descripcion = models.TextField()
    icono = models.CharField(
        max_length=80,
        blank=True,
        help_text='Clase de icono, por ejemplo: bi bi-braces.',
    )
    orden = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['orden', 'titulo']

    def __str__(self):
        return self.titulo


class Proyecto(models.Model):
    """Proyecto destacado o repositorio enriquecido para la vitrina principal."""

    titulo = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    descripcion_corta = models.CharField(max_length=280)
    descripcion_profesional = models.TextField()
    # Campos de caso de estudio para contar el contexto, la solucion y el impacto.
    problema = models.TextField(blank=True)
    solucion = models.TextField(blank=True)
    resultado = models.TextField(blank=True)
    categoria = models.CharField(max_length=100)
    fecha = models.CharField(max_length=80, blank=True)
    cliente = models.CharField(max_length=120, blank=True)
    tecnologias = models.ManyToManyField(
        Tecnologia,
        blank=True,
        related_name='proyectos',
    )
    repo_nombre = models.CharField(max_length=150, blank=True)
    repo_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    destacado = models.BooleanField(default=False)
    mostrar_en_home = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['orden', 'titulo']

    def __str__(self):
        return self.titulo


class ProyectoImagen(models.Model):
    """Capturas asociadas a un proyecto; permite crear carruseles desde admin."""

    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name='imagenes',
    )
    imagen = models.ImageField(upload_to='proyectos/')
    titulo = models.CharField(max_length=120)
    descripcion = models.CharField(max_length=240, blank=True)
    # Marca una imagen como portada principal del proyecto.
    es_portada = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Imagen de proyecto'
        verbose_name_plural = 'Imágenes de proyecto'
        ordering = ['orden', 'titulo']

    def __str__(self):
        return f'{self.proyecto} - {self.titulo}'
