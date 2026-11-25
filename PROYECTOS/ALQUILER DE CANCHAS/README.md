# Alquiler-de-Canchas

Integrantes:

Tisera Camila - Lider Tecnica
Lorea Manuel
Tovio Joaquin

# Descripcion

Sistema web de gestión y alquiler de canchas deportivas desarrollado con Python y Django. Permite administrar canchas, clientes, reservas, disponibilidad y pagos. Proyecto final de Programación.


## Configuración del entorno de desarrollo

### Tecnologías utilizadas

| Tecnología | Versión |
|------------|---------|
| Python | 3.8.10 |
| Django | 4.2.30 |
| MySQL | 8.0.46 |
| mysqlclient | 2.2.7 |
| django-environ | 0.11.2 |

### Configuración implementada

- Integración de MySQL como motor de base de datos.
- Reemplazo de la configuración predeterminada de SQLite.
- Incorporación de mysqlclient como conector de MySQL.
- Incorporación de django-environ para gestionar variables de entorno.
- Centralización de dependencias en requirements.txt.
- Externalización de credenciales y configuraciones sensibles.
- Configuración de .gitignore para excluir archivos locales y privados.
- Validación de la configuración y conexión a MySQL.

### Instalación y configuración

Todos los comandos deben ejecutarse desde la carpeta
de la aplicación, donde se encuentra manage.py.

#### 1. Acceder al proyecto

Desde la raíz del repositorio:

```bash
cd "PROYECTOS/ALQUILER DE CANCHAS"
```

#### 2. Crear y activar el entorno virtual

Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

#### 3. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

#### 4. Configurar la base de datos

Contar con una instancia activa de MySQL 8.

Si la base de datos todavía no existe, crearla:

```sql
CREATE DATABASE IF NOT EXISTS alquiler_de_canchas
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

#### 5. Configurar las variables de entorno

Crear un archivo .env utilizando .env.example
como referencia.

```env
SECRET_KEY=clave_secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_NAME=alquiler_de_canchas
DATABASE_USER=usuario_local
DATABASE_PASSWORD=contraseña_local
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306
```

Para generar una clave secreta:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Cada integrante deberá configurar sus propias credenciales.

#### 6. Verificar la configuración

```bash
python manage.py check
```

#### 7. Verificar la conexión a MySQL

```bash
python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); cursor.execute('SELECT VERSION(), DATABASE()'); print(cursor.fetchone())"
```

Resultado obtenido en el entorno de referencia:

```text
('8.0.46', 'alquiler_de_canchas')
```

### Archivos de configuración

| Archivo | Descripción |
|---------|-------------|
| requirements.txt | Dependencias del proyecto |
| config/settings.py | Configuración de Django |
| .env.example | Plantilla de variables de entorno |
| .env | Configuración local y privada |
| .gitignore | Exclusión de archivos del repositorio |

Los archivos .env y .venv no deben subirse al repositorio.

### Consideraciones

- Cada integrante debe utilizar su propio entorno virtual.
- No es necesario modificar settings.py para configurar las
  credenciales locales.
- Las versiones indicadas corresponden al entorno de referencia.
- Python 3.8 y Django 4.2 ya no cuentan con soporte oficial.

