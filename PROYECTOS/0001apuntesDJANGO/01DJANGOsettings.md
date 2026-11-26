# settings.py de Django: desarrollo y producción
Explicación de cada parte del `settings.py` que genera `startproject`. Cada ítem muestra qué trae por defecto (**DESARROLLO**) y cómo se deja en **PRODUCCIÓN**. Los ejemplos suponen el dominio `biblioteca.midominio.com`, PostgreSQL y un servidor con Nginx + Gunicorn.

## Idea general
| | Desarrollo | Producción |
|---|---|---|
| Quién lo usa | El programador, en su computadora | Usuarios reales, en internet |
| Servidor | `runserver` | Gunicorn + Nginx |
| `DEBUG` | `True` | `False` |
| Base de datos | SQLite | PostgreSQL (o MySQL) |
| Secretos (clave, contraseñas) | Escritos en el archivo | Variables de entorno |
| HTTPS | No | Obligatorio |

Django genera el archivo pensado para desarrollo: cómodo, pero inseguro si se expone. Antes de publicar hay que revisar los ítems de abajo. Arriba de todo en `settings.py` hay que agregar `import os`.

## BASE_DIR
```python
BASE_DIR = Path(__file__).resolve().parent.parent
```
Carpeta raíz del proyecto, donde está `manage.py`. **No cambia** entre desarrollo y producción. Sirve para armar rutas: `BASE_DIR / 'templates'`.

## SECRET_KEY
```python
# DESARROLLO (lo que genera Django)
SECRET_KEY = 'django-insecure-...'

# PRODUCCIÓN
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']  # si falta, no arranca
```
Firma sesiones, cookies y tokens. El prefijo `django-insecure-` avisa que es solo para desarrollo. Se usan corchetes y no `.get()` para que el servidor falle si falta la variable. Generar una clave nueva:
```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Con archivo `.env` (`python -m pip install python-dotenv`):
```python
from dotenv import load_dotenv
load_dotenv(BASE_DIR / '.env')   # antes de leer las variables
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
```
El `.env` va en `.gitignore`, nunca en Git.

## DEBUG
```python
DEBUG = True                                  # DESARROLLO
DEBUG = False                                 # PRODUCCIÓN
DEBUG = os.environ.get('DJANGO_DEBUG') == 'True'   # según el entorno
```
Con `True`, Django muestra el código y las variables en cada error y expone información sensible. En producción es **siempre** `False`. La última forma queda en `False` si la variable no existe (valor seguro).

## ALLOWED_HOSTS
```python
ALLOWED_HOSTS = []        # DESARROLLO: acepta localhost y 127.0.0.1

ALLOWED_HOSTS = [         # PRODUCCIÓN
    'biblioteca.midominio.com',
    'www.biblioteca.midominio.com',
]
```
Dominios desde los que Django acepta peticiones. Con `DEBUG = False` y la lista vacía, el sitio responde error 400 a todo. Leída del entorno:
```python
hosts = os.environ.get('DJANGO_ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h for h in hosts.split(',') if h]
```

## CSRF_TRUSTED_ORIGINS
No viene por defecto. En producción casi siempre hace falta:
```python
CSRF_TRUSTED_ORIGINS = ['https://biblioteca.midominio.com']
```
Orígenes que pueden enviar formularios (POST) al sitio. Si hay un proxy con HTTPS y falta, los formularios dan error 403 de CSRF. Incluye el esquema (`https://`).

## INSTALLED_APPS
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'libros',   # app propia
]
```
Lista de apps activas del proyecto. Las seis `django.contrib` vienen con Django:

| App | Qué es | Qué aporta |
|---|---|---|
| `admin` | Panel de administración | Interfaz web en `/admin/` para crear, editar y borrar registros de los modelos registrados en `admin.py` |
| `auth` | Autenticación y permisos | Modelos `User`, `Group` y `Permission`, login/logout, hash de contraseñas, `AUTH_PASSWORD_VALIDATORS` |
| `contenttypes` | Registro de modelos | Tabla `django_content_type` con todos los modelos. La usan `auth` (permisos por modelo) y `admin` (historial) |
| `sessions` | Sesiones | Guarda datos de cada visitante en el servidor (tabla `django_session`) y le deja una cookie con el identificador |
| `messages` | Mensajes de una sola vez | `messages.success(request, '...')` y se muestran en la plantilla ("Libro guardado") |
| `staticfiles` | Archivos estáticos | `{% static %}` en plantillas, servir CSS/JS con `runserver` y el comando `collectstatic` |

- **Dependencias:** `admin` necesita `auth`, `contenttypes`, `sessions` y `messages`, más sus middlewares y context processors. Si se saca alguna, `check` marca errores.
- **Apps propias:** al crear una con `startapp libros` hay que sumarla acá, o Django no ve sus modelos ni sus plantillas.
- **Tablas:** `python manage.py migrate` crea las tablas de estas apps.
- **Desarrollo:** se pueden sumar herramientas como `debug_toolbar`. **Producción:** se dejan afuera, solo lo que realmente se usa.

## MIDDLEWARE
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # solo PRODUCCIÓN
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```
Capas por las que pasa cada petición (de arriba hacia abajo) y cada respuesta (de abajo hacia arriba).

| Middleware | Qué hace | Se configura con |
|---|---|---|
| `SecurityMiddleware` | Medidas de seguridad generales: redirige a HTTPS, agrega HSTS y el encabezado `nosniff` | `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS` |
| `WhiteNoiseMiddleware` | (Opcional) Sirve los estáticos desde Django, sin configurar Nginx para eso | `STORAGES`, `STATIC_ROOT` |
| `SessionMiddleware` | Lee la cookie de sesión y deja los datos en `request.session`; al responder guarda los cambios | `SESSION_COOKIE_SECURE` |
| `CommonMiddleware` | Tareas varias: agrega la `/` final a las URL (`/libros` → `/libros/`) y puede bloquear user agents | `APPEND_SLASH`, `DISALLOWED_USER_AGENTS` |
| `CsrfViewMiddleware` | Protege contra CSRF: en POST exige el token de `{% csrf_token %}`; si falta, error 403 | `CSRF_COOKIE_SECURE`, `CSRF_TRUSTED_ORIGINS` |
| `AuthenticationMiddleware` | Agrega `request.user` (el usuario logueado o uno anónimo) | — |
| `MessageMiddleware` | Habilita los mensajes de una sola vez | — |
| `XFrameOptionsMiddleware` | Agrega `X-Frame-Options: DENY`: impide que otro sitio muestre la página en un `<iframe>` (clickjacking) | `X_FRAME_OPTIONS` |

**El orden importa:**
- `SecurityMiddleware` va primero para redirigir a HTTPS antes que todo.
- `SessionMiddleware` va antes de `AuthenticationMiddleware` y `MessageMiddleware`, porque ambos usan la sesión.
- `WhiteNoise` va justo después de `SecurityMiddleware`.

`WhiteNoise` se instala con `python -m pip install whitenoise`. En desarrollo no hace falta.

## ROOT_URLCONF y WSGI_APPLICATION
```python
ROOT_URLCONF = 'biblioteca.urls'
WSGI_APPLICATION = 'biblioteca.wsgi.application'
```
`ROOT_URLCONF` es el módulo con las URL principales del proyecto. `WSGI_APPLICATION` es el objeto que usa el servidor de producción. **No cambian** en producción. Gunicorn arranca así:
```
gunicorn biblioteca.wsgi:application --bind 127.0.0.1:8000 --workers 3
```
`asgi.py` es el equivalente asíncrono (WebSockets), con Uvicorn o Daphne. Para una app tradicional alcanza con WSGI.

## TEMPLATES
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
Configura el motor de plantillas HTML. Cada clave:

| Clave | Qué es | Valor |
|---|---|---|
| `BACKEND` | Motor de plantillas | `DjangoTemplates` (el propio de Django; la alternativa es Jinja2) |
| `DIRS` | Carpetas de plantillas del proyecto | **Desarrollo:** viene `[]`, hay que agregar `BASE_DIR / 'templates'` |
| `APP_DIRS` | Busca también en la carpeta `templates/` de cada app instalada | `True` |
| `OPTIONS` | Opciones del motor | Contiene `context_processors` |

Un **context processor** es una función que agrega variables a **todas** las plantillas, sin pasarlas desde cada vista:

| Context processor | Variables que agrega |
|---|---|
| `request` | `request` (por ejemplo `request.path`, `request.user`) |
| `auth` | `user` (usuario actual) y `perms` (sus permisos) |
| `messages` | `messages` (mensajes de una sola vez) |
| `debug` | `debug` y `sql_queries`. Aparece en versiones anteriores de Django y solo funciona con `DEBUG = True` |

`admin` necesita los tres primeros. **Producción:** no se cambia nada importante. Desde Django 4.1 las plantillas compiladas se guardan en caché también en desarrollo, así que no hay nada que activar.

## DATABASES
```python
# DESARROLLO
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PRODUCCIÓN
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': 60,
    }
}
```
SQLite es un solo archivo, ideal para desarrollar. En producción se usa PostgreSQL (o MySQL), que soporta muchos usuarios a la vez. Necesita el driver: `python -m pip install "psycopg[binary]"`. Las credenciales van en variables de entorno, nunca en el código. `CONN_MAX_AGE` mantiene las conexiones abiertas 60 segundos.

## AUTH_PASSWORD_VALIDATORS
```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.'
             'UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.'
             'MinimumLengthValidator',
     'OPTIONS': {'min_length': 10}},          # PRODUCCIÓN (por defecto 8)
    {'NAME': 'django.contrib.auth.password_validation.'
             'CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.'
             'NumericPasswordValidator'},
]
```
| Validador | Rechaza |
|---|---|
| `UserAttributeSimilarityValidator` | Contraseñas parecidas al usuario, nombre o email |
| `MinimumLengthValidator` | Contraseñas cortas (por defecto, menos de 8) |
| `CommonPasswordValidator` | Contraseñas de la lista de las más comunes (`123456`, `password`) |
| `NumericPasswordValidator` | Contraseñas formadas solo por números |

## Internacionalización
```python
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True
```
Idioma, zona horaria y traducciones. **No cambia** entre desarrollo y producción (por defecto Django trae `en-us` y `UTC`). Con `USE_TZ = True` las fechas se guardan en UTC y se convierten a la zona local al mostrarlas, lo que evita problemas con servidores en otros husos horarios.

## Archivos estáticos (CSS, JS, imágenes)
```python
STATIC_URL = 'static/'                         # DESARROLLO (viene por defecto)

STATIC_URL = 'static/'                         # PRODUCCIÓN
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.'
                   'CompressedManifestStaticFilesStorage'},
}
```
- `STATIC_URL`: prefijo de la dirección web de los estáticos.
- `STATICFILES_DIRS`: carpetas con los estáticos propios (la carpeta `static/` debe existir, si no Django avisa).
- `STATIC_ROOT`: carpeta a la que se copian **todos** los estáticos al desplegar, con `python manage.py collectstatic`. El servidor web (o WhiteNoise) sirve esa carpeta.
- Desarrollo: `runserver` sirve los estáticos solo, sin `collectstatic`.
- `CompressedManifest...` comprime los archivos y les agrega un hash al nombre, para que el navegador no use versiones viejas. Si falta correr `collectstatic`, la página falla con `Missing staticfiles manifest entry`.

## Archivos subidos por usuarios (media)
```python
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```
Para portadas de libros, PDFs y todo lo que suban los usuarios.
- **Desarrollo:** se agrega al final de `urls.py` para verlos con `runserver`:
```python
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
- **Producción:** Nginx sirve esa carpeta, o se usa un almacenamiento externo como S3.

## DEFAULT_AUTO_FIELD
```python
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```
Tipo de la clave primaria (`id`) de los modelos. **No cambia** en producción.

## Seguridad HTTPS (solo PRODUCCIÓN, se agrega al final)
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```
- `SECURE_SSL_REDIRECT`: redirige todo el tráfico HTTP a HTTPS.
- `SESSION_COOKIE_SECURE` y `CSRF_COOKIE_SECURE`: las cookies viajan solo por HTTPS.
- `SECURE_HSTS_SECONDS`: el navegador usa siempre HTTPS con el dominio durante ese tiempo (un año). Conviene empezar con un valor bajo (`3600`) y subirlo cuando todo funcione, porque el navegador lo recuerda.
- `SECURE_PROXY_SSL_HEADER`: se usa cuando Nginx termina el HTTPS y le habla a Django por HTTP. Configurarlo solo si el proxy envía ese encabezado, o habrá bucles de redirección.

## LOGGING (opcional, muy útil)
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'errores.log',
        },
    },
    'loggers': {
        'django': {'handlers': ['file'], 'level': 'WARNING'},
    },
}
```
Con `DEBUG = False` los errores ya no se ven en pantalla, así que hay que registrarlos. Este ejemplo guarda en un archivo los avisos y errores de Django.

## Antes de desplegar
```
python manage.py check --deploy
```
Revisa la configuración y marca lo que falte: `SECRET_KEY` insegura, `DEBUG` activo, cookies sin `Secure`, HSTS sin configurar.

| Ítem | Desarrollo | Producción |
|---|---|---|
| `SECRET_KEY` | En el archivo | Variable de entorno |
| `DEBUG` | `True` | `False` |
| `ALLOWED_HOSTS` | `[]` | Dominios reales |
| `CSRF_TRUSTED_ORIGINS` | No hace falta | `https://dominio` |
| `DATABASES` | SQLite | PostgreSQL |
| Estáticos | `runserver` los sirve | `collectstatic` + WhiteNoise o Nginx |
| Seguridad HTTPS | No | Activada |
