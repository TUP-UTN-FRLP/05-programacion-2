# Capítulo 25. Deploy profesional: Docker, multistage y la nube

*De la máquina local al mundo.*

## ¿Por qué leemos este capítulo?

Todo el manual el sistema bancario corrió en tu computadora, en
http://127.0.0.1:8000/. Eso está bien para desarrollo y para aprender, pero un
banco que solo funciona en tu laptop no le sirve a nadie más.

En este capítulo damos el paso final: **llevar el sistema a internet**. Al
terminar, cualquier persona en el mundo va a poder abrir el navegador, escribir
la URL de tu banco, registrarse, y usar el sistema - exactamente como usarían
un banco real.

El camino tiene tres etapas:

- **Docker**: empaquetar la aplicación en un contenedor portable.
- **Docker Compose**: levantar Django + PostgreSQL juntos localmente.
- **Deploy a Railway**: usar ese contenedor para poner el banco online.

Con estos tres pasos vas a tener el conocimiento fundamental de deploy
moderno. Es una habilidad que multiplica tu valor como desarrollador - hay
muchos que saben programar, los que además saben poner sus sistemas en
producción son más escasos y mejor pagos.

## ¿Por qué Docker?

Antes de meternos con Docker, entendamos qué problema resuelve.

Imaginate esta escena: terminaste el proyecto del banco en tu máquina.
Funciona perfecto. Se lo pasás a un compañero para que lo pruebe. Él lo abre y
le explota:

- "Necesitás Python 3.13, yo tengo 3.11".
- "Instalaste Django 5.2, pero yo tengo 4.2 por otro proyecto".
- "En mi Windows no encuentra psycopg2-binary".
- "¿Cómo instalo PostgreSQL en mi Mac?".

Este es el problema clásico del desarrollo: **funciona en mi máquina, pero no
en la tuya**. Cada máquina tiene su versión de Python, sus librerías, su
sistema operativo, sus configuraciones. Lo que funciona en un lado no siempre
funciona en otro.

**Docker resuelve este problema**. Empaqueta tu aplicación con **todas sus
dependencias** - Python, librerías, configuraciones, hasta el sistema
operativo - dentro de un **contenedor** portable. Ese contenedor funciona
**igual** en cualquier lado: tu máquina, la de tu compañero, un servidor en la
nube.

### La analogía del contenedor de barco

Docker toma su nombre de los contenedores marítimos: cajas metálicas
estandarizadas que se pueden mover entre barcos, camiones y trenes sin importar
qué llevan adentro. No importa si un contenedor tiene autos, alimentos o
electrónica: el mecanismo de transporte es el mismo.

Los contenedores de Docker funcionan igual: no importa qué haya adentro
(Django, Node.js, Java), el mecanismo para crearlos, moverlos y ejecutarlos es
siempre el mismo. Aprender Docker es aprender a manejar contenedores de
software, y ese conocimiento se aplica a cualquier lenguaje y cualquier
framework.

### Contenedores vs máquinas virtuales

Los que ya vieron sistemas operativos conocen las **máquinas virtuales** (VMs):
computadoras enteras corriendo dentro de otra computadora. Docker se parece
pero es distinto:

- **VM**: emula hardware completo. Cada VM tiene su propio kernel de sistema
  operativo. Ocupa gigabytes, tarda minutos en arrancar.
- **Contenedor**: comparte el kernel del host. Solo aísla los procesos,
  archivos y red. Ocupa megabytes, arranca en segundos.

En la práctica: **arrancar un contenedor Docker es tan rápido como abrir un
programa**. Podés levantar, tirar abajo y recrear contenedores decenas de veces
por minuto durante desarrollo.

## Instalando Docker

Antes de meternos con archivos, instalá Docker. Cambia según sistema
operativo:

### Windows / macOS

Descargá **Docker Desktop** desde https://www.docker.com/products/docker-desktop/.
Es una aplicación gráfica que incluye Docker Engine, Docker Compose y una
interfaz visual para gestionar contenedores.

Después de instalar, abrí Docker Desktop y esperá a que se inicialice (aparece
un ícono de ballena en la barra de tareas cuando está listo).

### Linux (Ubuntu/Debian)

En Linux, Docker se instala directamente:

```bash
sudo apt update
sudo apt install docker.io docker-compose-plugin
sudo usermod -aG docker $USER
```

El `usermod` agrega tu usuario al grupo docker para que puedas ejecutar
comandos sin `sudo`. **Cerrá sesión y volvé a entrar** para que el cambio tenga
efecto.

### Verificar la instalación

Con Docker corriendo, en la terminal:

```bash
docker --version
# Docker version 27.x.x, build ...

docker run hello-world
```

`hello-world` es una imagen de prueba minúscula que solo imprime un mensaje. Si
ves algo como *"Hello from Docker!"*, todo está funcionando.

## El Dockerfile

Un **Dockerfile** es un archivo de texto que describe cómo construir una
**imagen** de tu aplicación. La imagen es una plantilla, cada vez que la
ejecutás, obtenés un contenedor.

Vamos a crear un Dockerfile para el banco. En la raíz del proyecto (junto a
`manage.py`), creá el archivo `Dockerfile` (sin extensión):

**`dockerfile`**

```dockerfile
# Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Recolectar archivos estáticos
RUN python manage.py collectstatic --noinput

# Exponer puerto
EXPOSE 8000

# Comando por defecto: arranca gunicorn
CMD ["gunicorn", "banco_utn.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Vamos línea por línea:

**`FROM python:3.13-slim`**: la imagen base. Docker Hub tiene miles de
imágenes públicas. `python:3.13-slim` es la imagen oficial de Python 3.13,
versión "slim" (más chica que la completa, sin herramientas innecesarias).

**`WORKDIR /app`**: el directorio de trabajo dentro del contenedor. Todos los
comandos siguientes se ejecutan desde ahí.

**`ENV`**: variables de entorno. `PYTHONDONTWRITEBYTECODE=1` evita que Python
genere archivos `.pyc` (no los necesitamos en el contenedor).
`PYTHONUNBUFFERED=1` hace que los `print()` aparezcan en los logs
inmediatamente.

**`RUN apt-get update && apt-get install ...`**: instala paquetes del sistema
operativo. `postgresql-client` sirve para hacer backups y conexiones a la
base. El `rm -rf` libera espacio limpiando el caché de apt.

**`COPY requirements.txt .`**: copia el archivo de dependencias al contenedor.
Solo copiamos `requirements.txt` primero (no todo el código) para aprovechar
el sistema de caché de Docker: si `requirements.txt` no cambió, esta capa no se
rearma.

**`RUN pip install ...`**: instala las dependencias de Python. `--no-cache-dir`
no guarda archivos temporales, achica la imagen.

**`COPY . .`**: copia todo el resto del proyecto al contenedor.

**`RUN python manage.py collectstatic --noinput`**: recolecta archivos
estáticos. `--noinput` evita que pida confirmación.

**`EXPOSE 8000`**: documenta que el contenedor escucha en el puerto 8000. Es
informativo - el mapeo real de puertos se hace al ejecutar.

**`CMD ["gunicorn", ...]`**: el comando que se ejecuta cuando arranca el
contenedor. Reemplazamos `runserver` (que es solo para desarrollo) por
**Gunicorn**, el servidor de aplicación real.

### Creando requirements.txt

Si todavía no lo tenés, generalo con:

```bash
pip freeze > requirements.txt
```

Editá el archivo resultante para que quede algo así (limpio, sin dependencias
transitivas innecesarias):

**`requierements.txt`**

```text
Django==5.2

psycopg2-binary==2.9.9

gunicorn==22.0.0

python-dotenv==1.0.1
```

Si no tenías gunicorn instalado, agregalo al `requirements.txt` - es el
servidor que va a usar el contenedor.

### .dockerignore

Igual que `.gitignore`, Docker tiene su propio archivo para excluir cosas del
build. Creá `.dockerignore` en la raíz:

**`.dockerignore`**

```text
.venv/
__pycache__/
*.pyc
*.pyo
.git/
.gitignore
db.sqlite3
.env
.env.local
staticfiles/
media/
*.log
.DS_Store
.vscode/
.idea/
```

Sin esto, Docker copiaría el venv (cientos de MB), la base SQLite, secretos
del `.env`, y cosas que no queremos en la imagen. El `.dockerignore` mantiene
la imagen pequeña y segura.

## Construyendo y ejecutando el contenedor

Con el Dockerfile y `.dockerignore` listos, construimos la imagen:

```bash
docker build -t banco-utn .
```

Explicación:

- **`build`**: comando para construir imagen.
- **`-t banco-utn`**: etiqueta (nombre) que le damos a la imagen.
- **`.`**: contexto de build (la carpeta actual, donde está el Dockerfile).

Docker va a ejecutar cada línea del Dockerfile en orden. La primera vez tarda
unos minutos (descarga la imagen base, instala dependencias). Las próximas
veces es mucho más rápido porque usa capas cacheadas.

Al terminar:

```text
Successfully built abc123def456
Successfully tagged banco-utn:latest
```

Ejecutá el contenedor:

```bash
docker run -p 8000:8000 banco-utn
```

**`-p 8000:8000`** mapea el puerto 8000 del contenedor al puerto 8000 de tu
máquina. Sin esto, el contenedor escuchaba en su propio puerto interno, pero
nadie de afuera podía acceder.

Vas a ver la salida de Gunicorn arrancando. En el navegador, andá a
http://127.0.0.1:8000/.

...y **va a fallar**. ¿Por qué? Porque el contenedor no tiene base de datos.
Django intenta conectarse a PostgreSQL en localhost, pero **localhost dentro
del contenedor es el propio contenedor**, no tu máquina.

Ahí es donde entra Docker Compose.

## Docker Compose: múltiples servicios juntos

**Docker Compose** permite definir múltiples contenedores en un solo archivo y
levantarlos todos juntos con un solo comando. Es lo que se usa en desarrollo
para replicar el entorno completo: aplicación + base + caché + workers + lo que
necesites.

Creá `docker-compose.yml` en la raíz del proyecto:

**`docker-compose.yml`**

```yaml
services:
  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: banco_utn
      POSTGRES_USER: banco_user
      POSTGRES_PASSWORD: clave_dev
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U banco_user"]
      interval: 5s
      timeout: 5s
      retries: 5

  web:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             gunicorn banco_utn.wsgi:application --bind 0.0.0.0:8000 --reload"
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      DEBUG: "True"
      SECRET_KEY: "clave_dev_no_usar_en_produccion"
      DB_NAME: banco_utn
      DB_USER: banco_user
      DB_PASSWORD: clave_dev
      DB_HOST: db
      DB_PORT: 5432
    depends_on:
      db:
        condition: service_healthy

volumes:
  postgres_data:
```

Descomponemos el archivo:

### services:

los contenedores a levantar. Cada uno tiene un nombre (`db`, `web`) que también
es su hostname dentro de la red Docker.

#### Servicio db:

- **`image: postgres:16`**: usa la imagen oficial de PostgreSQL 16 desde Docker
  Hub.
- **`volumes: postgres_data:/var/lib/postgresql/data`**: los datos se guardan
  en un **volumen** persistente. Sin volumen, si tirás abajo el contenedor
  perdés todo. Con volumen, los datos sobreviven entre reinicios.
- **`environment`**: configura la base con las variables que PostgreSQL
  espera.
- **`healthcheck`**: verifica que PostgreSQL esté aceptando conexiones antes de
  considerarlo listo.

#### Servicio web:

- **`build: .`**: en vez de usar una imagen prehecha, construye desde el
  Dockerfile local.
- **`command`**: sobrescribe el CMD del Dockerfile. Corre migraciones antes de
  arrancar Gunicorn. El `--reload` hace que Gunicorn detecte cambios en el
  código (útil para desarrollo).
- **`volumes: .:/app`**: monta la carpeta del proyecto dentro del contenedor.
  Con esto, editar código en tu editor se refleja al instante en el
  contenedor. **Solo para desarrollo** - en producción no se hace.
- **`ports: "8000:8000"`**: mapeo de puertos.
- **`environment`**: variables que Django lee al arrancar.
- **`depends_on`**: no arrancar `web` hasta que `db` esté sano (por el
  healthcheck).

### volumes:

- **`postgres_data`**: declara el volumen que usa `db`. Docker lo gestiona
  internamente.

### Ajustando settings.py

Para que Django use las variables de entorno del `docker-compose.yml`, revisá
que `settings.py` tenga (como preparamos en el capítulo 24):

**`Banco_utn/settings.py`**

```python
import os

DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_desarrollo_solo')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

Notá que `DB_HOST` es `db` en el `docker-compose.yml`. Docker Compose crea una
red interna donde cada servicio es accesible por su nombre.

### Levantando todo

Con Docker Desktop corriendo:

```bash
docker compose up
```

La primera vez descarga la imagen de PostgreSQL, construye la imagen del
banco, arranca ambos contenedores. Vas a ver logs de los dos servicios
mezclados en la terminal.

Después de unos segundos, Django arranca. En el navegador,
http://127.0.0.1:8000/. **El banco funciona con PostgreSQL real, sin haber
instalado PostgreSQL en tu máquina**.

Para detener todo: Ctrl+C. Para relanzar en background:

```bash
docker compose up -d                 # -d = detached (background)
docker compose logs -f               # ver logs en vivo
docker compose down                  # detener y eliminar contenedores
docker compose down -v               # además, borrar volumen (los datos se pierden)
```

### Ejecutando comandos dentro del contenedor

Para correr comandos `manage.py` dentro del contenedor:

```bash
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py shell
docker compose exec web python manage.py test
```

`exec web` significa "ejecutá este comando en el servicio `web`". Los comandos
usan el Python del contenedor, con todas sus dependencias.

## Multistage builds: imágenes más pequeñas y seguras

El Dockerfile que armamos funciona, pero tiene problemas para producción:

- **Es grande**. Incluye `postgresql-client`, herramientas de build, todo el
  pip cache. Puede pesar 500 MB o más.
- **Incluye el código fuente completo**. En producción, con `DEBUG=False`, no
  necesitás archivos que solo sirven para desarrollo (`.git`, tests,
  migraciones vacías...).
- **Puede contener secretos**. Si accidentalmente copiaste un `.env` en algún
  paso, queda en la imagen.

La solución profesional se llama **multistage build**: dividir el Dockerfile en
varias etapas, y en la imagen final solo copiar lo mínimo necesario.

### Estructura de un multistage

Reescribí `Dockerfile`:

**`dockerfile`**

```dockerfile
# Dockerfile - versión multistage

# ==============================================================================
# ETAPA 1: builder - instala dependencias
# ==============================================================================
FROM python:3.13-slim AS builder

WORKDIR /app

# Instalar herramientas de build (necesarias para compilar algunas libs de Python)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias en una carpeta específica
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ==============================================================================
# ETAPA 2: runtime - imagen final, mínima
# ==============================================================================
FROM python:3.13-slim

WORKDIR /app

# Solo dependencias de runtime, no de build
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copiar las dependencias instaladas desde el builder
COPY --from=builder /install /usr/local

# Crear usuario no privilegiado
RUN useradd --create-home --shell /bin/bash django

# Copiar código de la aplicación
COPY --chown=django:django . .

# Cambiar a usuario no root
USER django

# Recolectar estáticos
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "banco_utn.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
```

> **Cambios clave.** Dos etapas separadas con `FROM`, la primera se llama
> `builder`, la segunda es la imagen final, empieza limpia desde cero.

### Etapa builder:

- Instala `build-essential` y `libpq-dev` (necesarios para compilar
  `psycopg2`).
- Instala dependencias en `/install` con `--prefix`.

### Etapa final:

- Solo instala `libpq5` (runtime de PostgreSQL, no headers de desarrollo).
- **`COPY --from=builder /install /usr/local`**: trae solo lo que se instaló,
  sin las herramientas de build.
- Crea un usuario `django` no privilegiado. **Nunca correr contenedores como
  root en producción** - si hay una vulnerabilidad, un proceso comprometido con
  permisos de root es mucho peor que uno con permisos limitados.
- **`USER django`**: cambia el usuario que corre la aplicación.
- Gunicorn con `--workers 3` (procesos paralelos para manejar más requests).

### Comparando tamaños

```bash
docker build -t banco-utn:simple -f Dockerfile.simple .
docker build -t banco-utn:multistage .

docker images | grep banco-utn
```

Vas a ver algo como:

```text
banco-utn     multistage      234 MB
banco-utn     simple          587 MB
```

La imagen multistage pesa la mitad o menos. En producción, esto significa:

- **Deploy más rápido**: menos datos que subir.
- **Menor superficie de ataque**: no hay herramientas de build para que un
  atacante aproveche.
- **Menor costo**: los servicios de nube cobran por espacio de imagen.

### ¿Cuándo vale la pena?

Multistage es la práctica estándar para producción. Para desarrollo local con
docker-compose, un Dockerfile simple alcanza. La regla:

- **Desarrollo**: Dockerfile simple con `docker-compose up` para iteración
  rápida.
- **Producción**: Dockerfile multistage, optimizado para tamaño, seguridad y
  velocidad.

Muchos proyectos tienen dos archivos: `Dockerfile` (multistage para prod) y
`Dockerfile.dev` (simple para desarrollo).

## Preparando para deploy: settings de producción

Antes de subir el banco a Railway, hay algunos ajustes que faltan.

### 1. DEBUG=False en producción

En producción, `DEBUG=True` **muestra el código fuente y las variables** cuando
hay un error. Es un agujero de seguridad crítico. Ya usamos variables de
entorno para controlarlo - solo hay que asegurarse de que en producción
`DEBUG=False`.

### 2. ALLOWED_HOSTS

Cuando `DEBUG=False`, Django exige que `ALLOWED_HOSTS` contenga los dominios
que van a servir la app. Sin esto, cualquier request es rechazada:

**`banco_utn/settings.py`**

```python
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

En Railway lo vamos a setear a `banco-utn.up.railway.app` (o el dominio que
asigne).

### 3. Archivos estáticos con Whitenoise

En desarrollo, Django sirve los archivos estáticos (CSS, JS de Bootstrap)
automáticamente. En producción, no. La solución tradicional es Nginx sirviendo
los estáticos por fuera. Pero para deploys simples (Railway, Heroku), hay una
biblioteca llamada **Whitenoise** que hace que Django sirva estáticos
eficientemente. Instalación:

```bash
pip install whitenoise
```

**`requirements.txt`**

```text
Django==5.2
psycopg2-binary==2.9.9
gunicorn==22.0.0
python-dotenv==1.0.1
whitenoise==6.7.0
```

**`banco_utn/settings.py`**

```python
MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',    # agregar acá, apenas después de Security

    'django.contrib.sessions.middleware.SessionMiddleware',

    # ... resto del middleware ...

]


STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

**`STATIC_ROOT`**: dónde `collectstatic` deja los archivos.
**`STATICFILES_STORAGE`**: usa Whitenoise con compresión gzip + hashing (para
caching efectivo).

### 4. SECRET_KEY de producción

En `settings.py`:

**`banco_utn/settings.py`**

```python
SECRET_KEY = os.environ.get('SECRET_KEY')

if not SECRET_KEY:
    raise ValueError("SECRET_KEY debe estar definida en el entorno")
```

En producción, si la variable no está seteada, la app se niega a arrancar. Es
la forma de asegurar que **nunca** se use una clave débil por accidente.

Para generar una clave nueva, Python trae la herramienta:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copiá la salida y usala como valor de `SECRET_KEY` en Railway (más adelante).

### 5. Seguridad extra

En `settings.py`, para producción es recomendable:

**`banco_utn/settings.py`**

```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True           # forzar HTTPS
    SESSION_COOKIE_SECURE = True         # cookies solo por HTTPS
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000       # HSTS: fuerza HTTPS por 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

Estas configuraciones se aplican solo en producción (`DEBUG=False`). En
desarrollo local, HTTPS forzado rompería el flujo.

## Deploy a Railway paso a paso

**Railway** es una plataforma de deploy moderna. Un `git push` alcanza para que
el sistema se actualice. Tiene tier gratuito generoso, incluye PostgreSQL, y
detecta automáticamente proyectos con Docker.

### Paso 1: crear cuenta y proyecto

Andá a https://railway.app y creá cuenta (podés usar tu GitHub para logueo
rápido).

Una vez adentro:

1. Click en **"New Project"**.
2. Elegí **"Deploy from GitHub repo"**.
3. Autorizá a Railway para acceder a tus repositorios.
4. Seleccioná el repo del banco.

**Si tu código no está en GitHub todavía**, subilo primero. Los pasos básicos.
En la raíz del proyecto:

```bash
git init
git add .
git commit -m "Proyecto banco listo para deploy"
```

Crear repo vacío en GitHub y después:

```bash
git remote add origin git@github.com:tu-usuario/banco-utn.git
git branch -M main
git push -u origin main
```

Recordá agregar `.env`, `db.sqlite3`, y `staticfiles/` a `.gitignore` antes de
commitear.

### Paso 2: agregar PostgreSQL

Con el proyecto creado en Railway, click en **"+ New"** ➡ **"Database"** ➡
**"Add PostgreSQL"**.

Railway crea una base PostgreSQL y expone variables de entorno automáticamente
al proyecto: `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`, entre
otras.

### Paso 3: configurar variables de entorno

En Railway, andá al servicio del banco (tu app, no la base). Buscá la pestaña
**"Variables"** y agregá:

```text
SECRET_KEY = (la clave que generaste antes)
DEBUG = False
ALLOWED_HOSTS = *.up.railway.app,tu-dominio-custom.com
DB_NAME = ${{ Postgres.PGDATABASE }}
DB_USER = ${{ Postgres.PGUSER }}
DB_PASSWORD = ${{ Postgres.PGPASSWORD }}
DB_HOST = ${{ Postgres.PGHOST }}
DB_PORT = ${{ Postgres.PGPORT }}
```

La sintaxis **`${{ Postgres.VAR }}`** es la forma de Railway de referenciar
variables de otros servicios. Con esto, tu app y la base están conectadas.

### Paso 4: comando de arranque

Railway detecta el Dockerfile automáticamente y usa el CMD que definimos. Pero
necesitamos correr migraciones antes de arrancar. Railway lo permite
configurando un **release command**.

En **"Settings"** de tu servicio, buscá **"Deploy"** ➡ **"Custom Start
Command"** y poné:

```bash
python manage.py migrate --noinput && gunicorn banco_utn.wsgi:application --bind 0.0.0.0:$PORT
```

Notá el **`$PORT`**: Railway asigna un puerto dinámico al contenedor y lo
expone en esa variable. No es siempre 8000 como en desarrollo.

### Paso 5: deploy

En la pestaña **"Deployments"**, hacé click en **"Deploy"** o simplemente
pusheá un commit a la rama main:

```bash
git add .
git commit -m "Configuración de deploy"
git push
```

Railway detecta el push, construye la imagen Docker, ejecuta las migraciones,
arranca Gunicorn. En 3-5 minutos, el banco está online.

### Paso 6: acceder a tu banco

En **"Settings"** ➡ **"Networking"** ➡ **"Generate Domain"**, Railway te da una
URL pública, algo como `banco-utn-production.up.railway.app`.

Abrí esa URL en el navegador. **El banco está en internet**. Cualquiera con la
URL puede acceder, registrarse, operar.

### Paso 7: crear un superusuario

Para acceder al admin, necesitás un superusuario. Railway permite ejecutar
comandos en el contenedor:

Instalar Railway CLI

```bash
npm install -g @railway/cli
```

Loguearse

```bash
railway login
```

Vincular al proyecto

```bash
railway link
```

Ejecutar comando en el contenedor

```bash
railway run python manage.py createsuperuser
```

Otra opción: usar la consola web de Railway (**"Settings"** ➡ **"Custom
Terminal"** o similar según versión).

## Configurando HTTPS y dominio propio

Railway asigna automáticamente un dominio con HTTPS incluido
(`*.up.railway.app`). Si querés usar un dominio propio:

1. **"Settings"** ➡ **"Networking"** ➡ **"Custom Domain"**.
2. Railway te da un valor CNAME para configurar en tu DNS.
3. En tu proveedor de dominio (Cloudflare, GoDaddy, NIC.ar, etc.), agregá el
   registro CNAME apuntando a Railway.
4. Esperá unos minutos hasta que se propague.
5. Railway configura automáticamente HTTPS con Let's Encrypt.

**Tu banco ahora corre en https://banco.tudominio.com con certificado SSL
válido**. Actualizá `ALLOWED_HOSTS` para incluir el dominio.

## Logs y monitoreo

Railway muestra los logs en tiempo real en **"Deployments"** ➡ click en el
deploy activo ➡ pestaña **"Logs"**. Podés filtrar, buscar, ver errores.

Para proyectos más serios, integrar herramientas específicas:

- **Sentry** (https://sentry.io): captura excepciones y bugs en producción con
  detalle completo. Django tiene integración con dos líneas de configuración.
  Tier gratuito generoso.
- **BetterStack Logs** o **Logtail**: agregación de logs con búsqueda.
- **Uptime Robot** o **Better Uptime**: monitorean que el sitio siga
  respondiendo.

Para el manual, los logs de Railway alcanzan. Cuando lleguen a proyectos serios
en el trabajo, Sentry es lo primero que hay que agregar.

## Backups de PostgreSQL

Un banco sin backups es un desastre esperando ocurrir. Los backups son
responsabilidad del desarrollador, incluso si Railway ofrece copias
automáticas de sus bases.

### Backup manual

Con `pg_dump`, la herramienta oficial de PostgreSQL.

#### Desde el contenedor local:

```bash
docker compose exec db pg_dump -U banco_user banco_utn > backup_$(date +%Y%m%d).sql
```

#### Desde Railway:

```bash
railway run pg_dump $DATABASE_URL > backup.sql
```

El archivo `.sql` contiene todo el esquema y los datos. Se puede restaurar
con:

```bash
psql -U banco_user banco_utn < backup.sql
```

### Backup automatizado

Para producción, se automatizan con cron jobs o servicios externos:

- **Neon**, **Supabase**, **Railway Postgres**: incluyen backups automáticos
  diarios en tiers pagos.
- **Simple Backups** (https://simplebackups.com): servicios dedicados a hacer
  backups y guardarlos en la nube.
- **Cron en el servidor** que corre `pg_dump` y sube a S3 o similar.

Regla mínima: **al menos un backup diario, guardado fuera del servidor de
producción**. Un incendio, un ataque, un error humano - cualquiera puede
destruir la base. El backup remoto es la única garantía real.

## Costos y tiers gratuitos

Railway ofrece **$5 USD de crédito mensual gratis** - suficiente para el banco
de este manual y proyectos personales chicos. Cuando se agote, se pausa el
servicio o se puede cargar más crédito.

Otras alternativas gratuitas o baratas:

- **Render** (https://render.com): tier gratuito con web service + PostgreSQL.
  La base free se borra cada 90 días si no se usa.
- **Fly.io**: 3 VMs pequeñas gratis, PostgreSQL barato. Docker-native.
- **Vercel / Netlify**: buenos para frontends, no ideales para Django (más
  pensados para JAMstack).
- **Google Cloud Run**: tier gratuito generoso, pero configuración más
  compleja.
- **VPS clásicos** (DigitalOcean, Hetzner): $5-6/mes por servidor completo,
  todo bajo tu control.

Para portfolios de estudiantes, Railway o Render alcanzan. Para proyectos que
generan ingresos, VPS clásicos suelen ser más económicos a largo plazo.

## Checklist final de deploy

Antes de considerar terminado un deploy, verificá:

- `DEBUG = False` en producción.
- `SECRET_KEY` seteada como variable de entorno, no en el código.
- `ALLOWED_HOSTS` configurado con el dominio real.
- Base de datos PostgreSQL configurada y funcionando.
- Archivos estáticos servidos correctamente (Whitenoise o Nginx).
- HTTPS activo con certificado válido.
- Superusuario creado.
- Migraciones aplicadas.
- Backups configurados.
- Logs revisables desde el panel del servicio.
- Tests corriendo bien contra el entorno.
- Errores monitoreados (Sentry o similar).

Con esta checklist en verde, tenés un sistema en producción a nivel
profesional.

## Buenas prácticas resumidas

1. **Un Dockerfile funcional en desarrollo, multistage para producción.**
   Optimizá cuando importe, mantené la simplicidad cuando no.
2. **`docker-compose.yml` para desarrollo local.** Replica el entorno de
   producción sin instalar servicios en tu máquina.
3. **Variables de entorno para toda configuración sensible.** Nunca commitees
   `.env`, `SECRET_KEY`, credenciales de base.
4. **HTTPS obligatorio en producción.** Sin excepciones. Los servicios modernos
   lo dan gratis.
5. **Backups automatizados desde el día uno.** No esperes a que pase un
   desastre.
6. **`.dockerignore` y `.gitignore` actualizados.** Excluí `venv/`,
   `__pycache__/`, `db.sqlite3`, `.env`, `staticfiles/`.
7. **Correr migraciones automáticamente en el deploy.** No confiar en hacerlas
   a mano después.
8. **Contenedores como usuarios no root.** En producción, siempre `USER app` (o
   cualquier usuario no privilegiado).
9. **Monitoreá los errores en producción.** Sentry o similar. Sin monitoreo,
   los bugs son invisibles hasta que se quejan los usuarios.
10. **Documentá el proceso de deploy.** Un `README.md` con los pasos ayuda a tu
    yo del futuro y a quien tome el proyecto después.

## Un cierre parcial

Con este capítulo, el banco pasa de ser un proyecto local a ser un **sistema en
producción accesible en internet**. Aprendieron los tres pilares del deploy
moderno:

- **Docker**: empaquetado portable y reproducible.
- **Docker Compose**: composición de servicios para desarrollo.
- **Deploy en la nube**: Railway como puerta de entrada, extrapolable a Fly.io,
  Render, y otros.

Este conocimiento es una de las divisiones más marcadas en el mercado laboral:
hay muchos desarrolladores que saben programar, los que además saben deployar
profesionalmente son menos, y mejor pagos. Habilidad rentable para toda la
carrera.

En el capítulo final del manual **Desarrollo asistido por IA: agentes en el
flujo de trabajo**, vamos a abordar la tecnología que está transformando la
forma de programar en este momento histórico: los **agentes de IA para
código**. Cómo integrarlos productivamente, cómo elegir modelos según tarea y
costo, y cómo trabajar con datos sensibles sin comprometer la privacidad
usando **modelos locales**.

Es un capítulo especial: no es sobre Python ni sobre Django, sino sobre **cómo
trabajar en 2026 y adelante**. Los que sepan usar bien estas herramientas van a
tener una ventaja enorme. Los que las ignoren, van a quedar atrás.
