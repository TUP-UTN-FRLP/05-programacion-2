# Alquiler-de-Canchas

Integrantes:

Tisera Camila - Líder Técnica
Lorea Manuel
Tovio Joaquin

# Descripcion

Sistema web de gestión y alquiler de canchas deportivas desarrollado con Python y Django. Permite administrar canchas, usuarios, reservas, disponibilidad y pagos. Proyecto final de Programación.

## Módulo de Usuarios

El sistema cuenta con un modelo de usuario personalizado de Django. Cada usuario tiene una cuenta de acceso con email y contraseña cifrada, además de sus datos personales.

### Operaciones disponibles

- Listar usuarios registrados.
- Registrar un usuario.
- Editar los datos de un usuario.
- Eliminar un usuario, previa confirmación.
- Asignar un rol al crear o editar un usuario.

Las pantallas del CRUD solo pueden ser utilizadas por cuentas con acceso al panel de administración. No se implementaron filtros ni búsquedas.

### Datos de cada usuario

| Campo | Característica |
|-------|----------------|
| Nombre | Obligatorio. Solo permite letras y espacios. |
| Apellido | Obligatorio. Solo permite letras y espacios. |
| DNI | Obligatorio, único y compuesto por 7 u 8 dígitos. |
| Teléfono | Obligatorio, único y compuesto por 8 a 15 dígitos sin espacios. |
| Correo electrónico | Obligatorio, con formato válido, único y utilizado para iniciar sesión. |
| Fecha de nacimiento | Obligatoria. Se ingresa en formato `dd/mm/aaaa`. Debe ser anterior al día actual y no superar 120 años de antigüedad. |
| Contraseña | Obligatoria al crear la cuenta. Django la guarda cifrada y solicita confirmación. |
| Estado | Se representa mediante `is_active`. Por defecto, un usuario está activo; si se desactiva, no podrá iniciar sesión. |
| Rol | Obligatorio. Se selecciona entre Administrador, Empleado o Cliente. |

El botón para guardar un usuario permanece deshabilitado hasta que los campos obligatorios estén completos y cumplan las validaciones básicas del navegador. Django realiza nuevamente las validaciones en el servidor para proteger los datos.

### Roles y permisos

Los roles se implementan con los grupos provistos por Django. La migración inicial crea los grupos Administrador, Empleado y Cliente. En el futuro se podrán asignar permisos concretos a cada grupo, por ejemplo permitir que un empleado gestione reservas sin modificar usuarios.

El primer usuario administrador es un superusuario de Django. Tiene control total del sistema, independientemente de su grupo.

### Acceso actual

Actualmente, el acceso administrativo se realiza desde `/admin/login/` con el superusuario creado mediante `createsuperuser`. Solo las cuentas marcadas como personal administrativo pueden acceder al panel y al CRUD de usuarios.

Las cuentas con rol Cliente ya cuentan con email y contraseña cifrada, pero la pantalla pública para iniciar sesión será implementada en una etapa posterior. Un Cliente no puede ingresar al panel `/admin/`.

### Rutas

| Ruta | Acción |
|------|--------|
| `/usuarios/` | Listar usuarios. |
| `/usuarios/nuevo/` | Registrar un usuario. |
| `/usuarios/<id>/editar/` | Editar un usuario. |
| `/usuarios/<id>/eliminar/` | Confirmar y eliminar un usuario. |

Los usuarios también se administran desde el panel de Django, en `/admin/`. Allí se pueden asignar grupos, permisos y acceso al panel.

### Migración del módulo

El módulo incluye una única migración inicial en `usuarios/migrations/0001_initial.py`. Después de configurar la base de datos, aplicarla con:

```bash
python manage.py migrate
```

Luego se crea el primer administrador mediante el comando:

```bash
python manage.py createsuperuser
```

El comando solicita el correo electrónico, nombre, apellido, DNI, teléfono, fecha de nacimiento y contraseña. No se crea mediante una migración para evitar guardar una contraseña en el código fuente.

### Ejecución del proyecto

Con las migraciones aplicadas y el superusuario creado, iniciar el servidor con:

```bash
python manage.py runserver
```

Rutas principales:

| Dirección | Uso |
|-----------|-----|
| `http://127.0.0.1:8000/` | Página de inicio. |
| `http://127.0.0.1:8000/admin/` | Panel de administración e inicio de sesión administrativo. |
| `http://127.0.0.1:8000/usuarios/` | CRUD de usuarios para personal administrativo. |

### Pruebas automatizadas

El módulo Usuarios cuenta con pruebas para el CRUD, las validaciones, la contraseña, los roles y el acceso restringido. Para ejecutarlas:

```bash
python manage.py test usuarios
```


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

