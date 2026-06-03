# Deploy en PythonAnywhere

Guia para desplegar el portafolio Django CMS `portafolio_jematti` en PythonAnywhere.

## 1. Subir el proyecto a GitHub

```bash
git status
git add .
git commit -m "Preparar portafolio CMS para produccion"
git push origin main
```

## 2. Abrir PythonAnywhere

1. Crear cuenta o iniciar sesion en PythonAnywhere.
2. Abrir una consola Bash.

## 3. Clonar el repositorio

```bash
git clone URL_DEL_REPO
cd portafolio_jematti
```

## 4. Crear y activar entorno virtual

```bash
python -m venv venv
source venv/bin/activate
```

## 5. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 6. Migraciones y superusuario

```bash
python manage.py migrate
python manage.py createsuperuser
```

## 7. Recolectar archivos estaticos

```bash
python manage.py collectstatic
```

## 8. Configurar Web App

En PythonAnywhere:

1. Ir a la pestaña **Web**.
2. Crear una nueva Web App.
3. Elegir **Manual configuration**.
4. Elegir una version de Python compatible con el proyecto.
5. Configurar:
   - Source code: `/home/USUARIO/portafolio_jematti`
   - Working directory: `/home/USUARIO/portafolio_jematti`
   - Virtualenv path: `/home/USUARIO/portafolio_jematti/venv`

## 9. Configurar WSGI

Editar el archivo WSGI de PythonAnywhere y dejar una configuracion similar:

```python
import os
import sys

path = '/home/USUARIO/portafolio_jematti'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 10. Configurar Static files

En la seccion **Static files**:

```text
URL: /static/
Path: /home/USUARIO/portafolio_jematti/staticfiles
```

## 11. Configurar Media files

En la seccion **Static files** agregar tambien:

```text
URL: /media/
Path: /home/USUARIO/portafolio_jematti/media
```

Las imagenes del CMS se cargan desde Django Admin y se guardan en `media/`.

## 12. Variables de entorno

Configurar estas variables en PythonAnywhere o en el WSGI antes de cargar Django:

```bash
SECRET_KEY=CAMBIAR_POR_UNA_CLAVE_SEGURA
DEBUG=False
ALLOWED_HOSTS=usuario.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://usuario.pythonanywhere.com
SITE_URL=https://usuario.pythonanywhere.com/
```

Si usas dominio propio, reemplazar `usuario.pythonanywhere.com` por el dominio final.

## 13. Recargar Web App

En la pestaña **Web**, presionar **Reload**.

## 14. Probar admin y cargar contenido

Entrar a:

```text
https://usuario.pythonanywhere.com/admin/
```

Cargar o revisar:

- Perfil
- Redes sociales
- Tecnologias
- Servicios
- Proyectos
- Imagenes de proyectos

## 15. Probar sitio publico

Revisar:

```text
https://usuario.pythonanywhere.com/
https://usuario.pythonanywhere.com/robots.txt
https://usuario.pythonanywhere.com/sitemap.xml
```

Confirmar que el home, imagenes, carruseles y enlaces carguen correctamente.
