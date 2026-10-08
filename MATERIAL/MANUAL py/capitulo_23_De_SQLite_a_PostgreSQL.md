# Capítulo 23. De SQLite a PostgreSQL

*Cambiando el motor sin cambiar el auto.*

## ¿Por qué leemos este capítulo?

Todo el manual usó **SQLite** como base de datos. Cuando corriste el primer
migrate, Django creó un archivo db.sqlite3 en la raíz del proyecto, y ahí
quedaron las tablas y los datos. Nunca configuraste nada - funcionaba desde el
minuto uno.

Eso es una de las razones por las que Django elige SQLite como default para
desarrollo: **cero configuración**. No hay servidor de base de datos que
instalar, ni credenciales que configurar, ni servicios que arrancar. Un
archivo, y listo.

Pero SQLite tiene límites. En producción, con múltiples usuarios concurrentes,
con grandes volúmenes de datos, con exigencias de integridad y seguridad,
SQLite deja de ser adecuado. Ahí entra **PostgreSQL**: el motor de base de
datos más usado en producción en el mundo Python. Robusto, potente, gratuito,
con años de desarrollo detrás.

En este capítulo vamos a hacer el cambio. Vas a ver una de las mejores
promesas del ORM cumplida: **migrar de motor sin cambiar una línea del código
de la aplicación**. Todo lo que escribiste - modelos, vistas, formularios,
tests - sigue funcionando idéntico contra PostgreSQL.

## Diferencias entre SQLite y PostgreSQL

Antes del cambio, entendamos qué estamos ganando y qué estamos cambiando.

| SQLite | PostgreSQL |
|---|---|
| ► **Archivo**: toda la base es un archivo .sqlite3 en el disco. | ► **Servidor**: es un proceso separado que corre continuamente. Las apps se conectan a él por red (o socket local). |
| ► **Sin servidor**: la biblioteca de Python lee y escribe directamente el archivo. | ► **Concurrencia real**: miles de escrituras simultáneas sin bloqueos generalizados. |
| ► **Concurrencia limitada**: una sola escritura a la vez. Múltiples lecturas simultáneas, sí, pero una sola escritura bloquea todo. | ► **Tipos estrictos**: si una columna es INTEGER, no acepta strings. Errores tempranos. |
| ► **Tipos flexibles**: SQLite es "type-flexible" - podés guardar un string en una columna INTEGER y no protesta. | ► **Usuarios y permisos**: cada aplicación se conecta con credenciales, tiene permisos específicos. |
| ► **Sin usuarios**: no hay control de acceso a la base. Quien tenga acceso al archivo, lee todo. | ► **Transacciones robustas**: garantiza consistencia bajo fallas. |
| ► **Ideal para**: desarrollo, prototipos, aplicaciones desktop, tests, aplicaciones con pocos usuarios concurrentes. | ► **Features avanzadas**: tipos JSON nativos, búsqueda de texto completo, replicación, particionado. |
| | ► **Ideal para**: producción, aplicaciones web con muchos usuarios, sistemas donde la integridad de datos es crítica. |

Cuando Django migra el proyecto de SQLite a PostgreSQL, no cambia **cómo
escribís** el código - cambia **cómo se guarda** por debajo. Los modelos, las
queries del ORM, todo lo demás sigue igual.

### ¿Cuándo migrar?

Regla práctica:

| Desarrollo local | Tests automáticos | Producción |
|---|---|---|
| SQLite. Simple, rápido, no requiere setup. | SQLite. Los tests corren en memoria, ultra rápido. | PostgreSQL. Punto. |

Muchos proyectos serios mantienen **SQLite en desarrollo y PostgreSQL en
producción**, con una configuración distinta según el entorno. Al final del
capítulo mostramos cómo hacerlo.

## Instalando PostgreSQL

Antes de tocar Django, hay que instalar el servidor PostgreSQL. Los pasos
varían según el sistema operativo.

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

El servicio queda arrancado automáticamente. Verificalo:

```bash
sudo systemctl status postgresql
```

### macOS

Con Homebrew:

```bash
brew install postgresql@16
brew services start postgresql@16
```

### Windows

Descargá el instalador desde https://www.postgresql.org/download/windows/.
Durante la instalación te va a pedir una contraseña para el usuario postgres -
guardala, la vamos a necesitar.

El instalador también incluye **pgAdmin**, una interfaz gráfica para
administrar bases de datos. Es útil para ver las tablas directamente, sin línea
de comandos.

### Verificar la instalación

Después de instalar, deberías tener el comando psql:

```bash
psql --version
# psql (PostgreSQL) 16.x
```

psql es el cliente de línea de comandos de PostgreSQL. Lo vamos a usar para
crear la base y el usuario del banco.

## Creando la base de datos y el usuario

PostgreSQL, a diferencia de SQLite, gestiona usuarios y bases de datos como
recursos separados. Antes de que Django pueda conectarse, hay que:

1. Crear una base de datos vacía para el proyecto.
2. Crear un usuario con permisos sobre esa base.
3. Configurar Django para que se conecte.

### Entrando a psql

En Linux/Mac, PostgreSQL crea un usuario del sistema llamado postgres.
Entramos como ese usuario:

```bash
sudo -u postgres psql
```

En Windows, desde el menú de PostgreSQL, abrí "SQL Shell (psql)". Te pedirá
host (Enter para localhost), database (Enter para postgres), port (Enter para
5432), username (Enter para postgres), password (la que definiste en la
instalación).

Ya adentro de psql, vas a ver un prompt como:

```text
postgres=#
```

### Creando la base y el usuario

Ejecutamos tres comandos SQL:

```sql
CREATE DATABASE banco_utn;
CREATE USER banco_user WITH PASSWORD 'clave_segura_del_banco';
GRANT ALL PRIVILEGES ON DATABASE banco_utn TO banco_user;
```

Y en PostgreSQL 15+ hay que hacer un paso adicional (permisos sobre el
schema):

```text
\c banco_utn
GRANT ALL ON SCHEMA public TO banco_user;
```

\c banco_utn cambia a la base recién creada. GRANT ALL ON SCHEMA public le da
permisos completos sobre el schema por defecto.

Salimos:

```text
\q
```

Ya tenemos:

- Una base banco_utn vacía.
- Un usuario banco_user con contraseña clave_segura_del_banco (usá una real,
  no esta).
- Permisos para que ese usuario opere en esa base.

## Instalando el driver de PostgreSQL

Django habla con la base de datos a través de un **driver**: una biblioteca de
Python que traduce los comandos del ORM a instrucciones del motor específico.
Para PostgreSQL, el driver estándar es psycopg2.

Con el entorno virtual activo:

```bash
pip install psycopg2-binary
```

**Nota sobre psycopg2-binary vs psycopg2:** el paquete -binary viene
pre-compilado y es más fácil de instalar. El paquete psycopg2 (sin -binary) se
compila desde código C y es la recomendación para producción (mejor
rendimiento en algunos casos). Para desarrollo y para el manual,
psycopg2-binary es más que suficiente.

Existe también psycopg[binary] (versión 3), más moderna y con soporte async.
En Django 5.2 se puede usar. Para consistencia y compatibilidad, seguimos con
psycopg2-binary en el manual.

## Configurando Django

Editá banco_utn/settings.py. Buscá la sección DATABASES, que actualmente tiene
esto:

**`banco_utn/settings.py`**

```python
# Configuración actual: SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Reemplazala por:

```python
# Configuración para PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'banco_utn',
        'USER': 'banco_user',
        'PASSWORD': 'clave_segura_del_banco',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Cambios:

- **ENGINE**: pasamos de sqlite3 a postgresql.
- **NAME**: ahora es el nombre de la base, no un archivo.
- **USER, PASSWORD**: credenciales del usuario que creamos.
- **HOST**: localhost porque el PostgreSQL corre en la misma máquina. En
  producción sería la IP o dominio del servidor de base de datos.
- **PORT**: 5432 es el puerto default de PostgreSQL.

Guardá y probemos.

## Aplicando las migraciones

La base banco_utn está vacía. Django tiene que crear todas las tablas. Es el
mismo comando que usamos siempre:

```bash
python manage.py migrate
```

Django detecta que la base está vacía y aplica **todas las migraciones desde
cero**:

```text
Operations to perform:
  Apply all migrations: admin, auth, banco, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  ...
  Applying banco.0001_initial... OK
  Applying banco.0002_persona_usuario... OK
  ...
```

Todas las tablas quedan creadas en PostgreSQL, con la misma estructura que
tenían en SQLite. La misma migración generó el mismo esquema en otro motor.

### Verificando con psql

Podés inspeccionar las tablas creadas:

```bash
sudo -u postgres psql banco_utn
```

O si preferís, entrando como banco_user:

```bash
psql -U banco_user -d banco_utn -h localhost
```

Adentro:

```text
\dt         -- lista todas las tablas
```

Deberías ver:

```text
                     List of relations
 Schema |             Name             | Type  |   Owner
--------+------------------------------+-------+------------
 public | auth_group                   | table | banco_user
 public | auth_user                    | table | banco_user
 public | banco_cuenta                 | table | banco_user
 public | banco_cuentaahorro           | table | banco_user
 ...
```

Todas las tablas que definimos en models.py, más las que trae Django
(usuarios, sesiones, admin).

### Creando un superusuario nuevo

Como la base es nueva, no tiene el superusuario que habías creado en SQLite.
Creá uno:

```bash
python manage.py createsuperuser
```

Y arrancá el servidor:

```bash
python manage.py runserver
```

Abrí http://127.0.0.1:8000/. **Todo funciona igual que antes**. La única
diferencia: los datos ahora viven en PostgreSQL en vez de SQLite. Ninguna
vista, ningún modelo, ningún template cambió.

**Esa es la promesa del ORM en acción**: cambio de motor sin cambio de código.

## Migrando datos de SQLite a PostgreSQL

Si tenías datos importantes en db.sqlite3 que querés preservar, Django trae
comandos para transferirlos.

### Paso 1: exportar de SQLite

Con la configuración vieja apuntando a SQLite:

```bash
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > datos_backup.json
```

Explicación:

- **dumpdata**: exporta todos los datos a formato JSON.
- **--natural-foreign y --natural-primary**: usan referencias "naturales" en
  lugar de IDs, evitando conflictos al importar.
- **-e contenttypes -e auth.Permission**: excluye tablas internas de Django que
  se recrean automáticamente.

Se genera datos_backup.json con todo el contenido de la base.

### Paso 2: importar a PostgreSQL

Después de configurar PostgreSQL y correr migrate (que crea las tablas
vacías):

```bash
python manage.py loaddata datos_backup.json
```

Django lee el JSON y carga los datos en PostgreSQL. **Los objetos aparecen
exactamente como estaban** en SQLite: mismas cuentas, mismos movimientos,
mismas relaciones.

Este proceso es útil para:

- Migrar un proyecto de desarrollo a producción.
- Copiar datos entre entornos.
- Hacer backups portables.

## psycopg2: qué hay debajo

Todo lo que hicimos en el ORM se traduce a SQL para PostgreSQL a través de
psycopg2. Nunca lo vas a usar directamente, pero es útil saber que existe.

Cuando hacés:

```python
Cuenta.objects.filter(saldo__gt=10000)
```

Django (a través de psycopg2) le manda a PostgreSQL:

```sql
SELECT * FROM banco_cuenta WHERE saldo > 10000;
```

Cuando querés inspeccionar el SQL que Django genera, hay dos formas:

### 1. .query en un queryset:

```python
qs = Cuenta.objects.filter(saldo__gt=10000).order_by('-saldo')
print(qs.query)
# SELECT "banco_cuenta"."id", ...  FROM "banco_cuenta"
# WHERE "banco_cuenta"."saldo" > 10000 ORDER BY "banco_cuenta"."saldo" DESC
```

### 2. Configurando logging en settings.py:

```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
```

Con eso, cada query se imprime en la consola. Útil para debugging de
performance: si una vista ejecuta 50 queries, se ve al instante.

> **Regla:** No toques psycopg2 a menos que tengas una razón muy específica. El
> ORM te da el 99% de lo que necesitás. Bajar a SQL crudo es una excepción, no
> la norma.

## Configuración por entornos

En proyectos reales, **cada entorno tiene su configuración**: desarrollo local,
staging, producción. La regla es que **las credenciales nunca se hardcodean**
en settings.py - se leen de **variables de entorno**.

### El problema

Si en settings.py tenés:

```python
'PASSWORD': 'clave_segura_del_banco',
```

Y hacés git commit de ese archivo, tu contraseña queda **pública en el
repositorio**. Aunque solo tu equipo tenga acceso, es una mala práctica que
puede convertirse en fuga de credenciales.

### La solución: variables de entorno

Las **variables de entorno** son valores que el sistema operativo expone a los
procesos. Podés setearlas en la terminal antes de correr Django:

```bash
export DB_NAME=banco_utn
export DB_USER=banco_user
export DB_PASSWORD=clave_segura_del_banco
export DB_HOST=localhost
python manage.py runserver
```

Y en settings.py:

**`banco_utn/settings.py`**

```python
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'banco_utn'),
        'USER': os.environ.get('DB_USER', 'banco_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

os.environ.get('DB_NAME', 'banco_utn') lee la variable DB_NAME. Si no está
seteada, usa 'banco_utn' como default.

Ahora settings.py no tiene secretos. Cada entorno setea sus propias variables.

### .env con python-dotenv

Setear variables cada vez que abrís la terminal es tedioso. La convención
moderna es usar un archivo .env en la raíz del proyecto:

```ini
# .env (este archivo NO se commitea)
DB_NAME=banco_utn
DB_USER=banco_user
DB_PASSWORD=clave_segura_del_banco
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=una_clave_larga_y_secreta_para_django
DEBUG=True
```

Instalás python-dotenv:

```bash
pip install python-dotenv
```

Y al principio de settings.py:

**`banco_utn/settings.py`**

```python
from dotenv import load_dotenv
load_dotenv()

# Ahora os.environ tiene todo lo del .env
```

Y el .env **se agrega a .gitignore** para que no se suba al repositorio:

**`.gitignore`**

```text
.env
db.sqlite3
__pycache__/
.venv/
```

En producción, las variables se configuran directamente en el servidor (o en
servicios como Heroku, Railway, AWS) sin necesidad de archivo .env.

### Alternando entre SQLite y PostgreSQL

Con este esquema, es fácil tener **SQLite en desarrollo y PostgreSQL en
producción**. En settings.py:

**`banco_utn/settings.py`**

```python
import os

USE_POSTGRES = os.environ.get('USE_POSTGRES', 'False') == 'True'

if USE_POSTGRES:
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
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

En el .env de producción:

**`banco /.env`**

```ini
USE_POSTGRES=True
DB_NAME=banco_utn_prod
...
```

En desarrollo, sin variable, usa SQLite. Cada uno con lo que le sirve.

## Consideraciones para deploy

Este capítulo cierra la parte técnica del manual. El paso siguiente - poner el
sistema en un servidor real, accesible desde internet - se llama **deploy** y
merece su propio curso. Anticipamos los conceptos:

### Servidores de aplicación

El servidor runserver que usamos durante todo el manual **no es apto para
producción**. Es un servidor de desarrollo: no maneja muchas conexiones
simultáneas, no es seguro, no está optimizado.

En producción se usan servidores como:

- **Gunicorn**: el más usado. Aloja la aplicación Django y responde a los
  pedidos.
- **uWSGI**: alternativa clásica, potente pero más compleja.

Adelante de Gunicorn se suele poner un servidor web como **Nginx**, que sirve
archivos estáticos (CSS, imágenes) y hace de intermediario con Gunicorn para
las requests dinámicas.

Esquema típico:

Internet ➡ Nginx (archivos estáticos + proxy) ➡ Gunicorn ➡ Django ➡ PostgreSQL

### Variables de entorno críticas

En producción, además de las credenciales de base:

- **SECRET_KEY**: la clave criptográfica de Django. **Nunca la de desarrollo.**
  Debe ser larga y aleatoria.
- **DEBUG = False**: Django deja de mostrar páginas de error detalladas (que
  podrían filtrar información sensible).
- **ALLOWED_HOSTS**: lista de dominios permitidos para servir la app.

```python
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

SECRET_KEY = os.environ.get('SECRET_KEY')
```

Si en producción DEBUG=True queda activado por accidente, Django **muestra el
código fuente y las variables** cuando ocurre un error. Es un agujero de
seguridad enorme.

### Archivos estáticos en producción

En desarrollo, Django sirve los archivos estáticos (CSS, imágenes, JS)
automáticamente. En producción, **no**. Hay que:

1. Correr python manage.py collectstatic - recoge todos los estáticos de todas
   las apps en una carpeta central.
2. Configurar Nginx (o el servidor web) para servir esa carpeta.

Es un cambio de configuración, no de código.

### HTTPS

En producción **siempre** se usa HTTPS. Se consigue con certificados SSL, hoy
en día gratuitos vía Let's Encrypt. Django detecta la conexión segura y ajusta
cookies, redirecciones, etc.

### Servicios de deploy modernos

Hoy hay plataformas que automatizan gran parte del deploy:

- **Railway** (https://railway.app): sube el código, se encarga del resto. Muy
  simple.
- **Render** (https://render.com): similar a Railway. Free tier decente.
- **Fly.io**: enfocado en performance y bajo costo.
- **Heroku** (histórico): el pionero, ahora pago.
- **DigitalOcean App Platform**: parte del ecosistema DigitalOcean.
- **AWS, Google Cloud, Azure**: gigantes, más complejos, más poder.

Para un proyecto de curso o portfolio personal, **Railway o Render** son
ideales: en 15 minutos tenés el banco público en internet con PostgreSQL
incluido. Detrás usan settings.py con variables de entorno, exactamente como
preparamos en este capítulo.

## Buenas prácticas

1. **SQLite en desarrollo, PostgreSQL en producción.** Es el patrón estándar en
   Python.
2. **Nunca commitees credenciales.** Usá variables de entorno. Agregá .env al
   .gitignore.
3. **Corré los tests después del cambio.** python manage.py test verifica que
   todo el sistema sigue funcionando con la nueva base.
4. **Backups regulares en producción.** PostgreSQL tiene pg_dump para backups.
   Configuralo desde el día uno.
5. **Migraciones son versionadas.** Los archivos en banco/migrations/ se
   commitean junto con el código. Nunca los borres a mano.
6. **DEBUG = False en producción, siempre.** Incluso si sos el único que va a
   usarlo. Es una regla sin excepciones.
7. **Un usuario de base por aplicación.** No uses el usuario postgres
   (superusuario) para conectar tu app. Creá un usuario específico con solo los
   permisos necesarios.
8. **Monitoreá la base.** En producción, ejecutá EXPLAIN sobre las queries
   lentas, revisá los índices, mirá los logs. Herramientas como
   django-debug-toolbar en desarrollo ayudan a detectar problemas antes.

## Lo que ganamos con PostgreSQL

Con el cambio hecho, el sistema bancario ahora corre sobre una base de datos
**de nivel de producción**:

- **Concurrencia real**: cientos de clientes operando simultáneamente sin
  bloqueos.
- **Integridad garantizada**: las validaciones a nivel de motor (unique, not
  null, foreign keys) se aplican estrictamente.
- **Escalabilidad**: PostgreSQL puede manejar bases de gigabytes sin problemas.
- **Herramientas profesionales**: pgAdmin, respaldos, replicación, monitoreo -
  todo disponible.
- **Estándar de la industria**: cualquier proyecto Python serio corre sobre
  PostgreSQL (o MySQL). Aprender este stack es aprender lo que se usa en el
  mundo real.

Y todo esto **sin modificar una línea del código de la aplicación**. Ese es el
poder del ORM: capa de abstracción tan sólida que la base de datos se vuelve un
detalle intercambiable.

En el último capítulo **Puentes hacia adelante**, vamos a hacer una recorrida
panorámica: qué queda por aprender después del manual, qué tecnologías conviene
incorporar según el rumbo que quieran tomar, y cómo el conocimiento que
construyeron acá se conecta con lo que viene. No es un tutorial, es un mapa de
rutas.
