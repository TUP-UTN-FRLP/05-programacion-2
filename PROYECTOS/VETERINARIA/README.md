TUP13 - Grupo 5
Proyecto: Veterinaria

Integrantes:

CASTRO Sanchez Liliana - 37099 - sanchezlylyana

GRONDA Anabella - 36718 - AnaGronda

MONLEZUN Neilen - 36734 - NeilenC

ZOPPOLI Luciano - 37105 - luchozoppo


Sistema de gestión para una veterinaria (clientes, mascotas y citas), hecho con Django.

## Requisitos

| Herramienta | Versión | Verificar con |
|-------------|---------|---------------|
| Python      | 3.12 o superior | `python --version` |
| Git         | cualquiera | `git --version` |

## Instalación

1. Clonar el repositorio y entrar a la carpeta:

   ```powershell
   git clone <URL-DEL-REPO>
   cd veterinaria
   ```

2. Crear y activar el entorno virtual:

   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

   En macOS/Linux: `source venv/bin/activate`

3. Instalar Django:

   ```powershell
   pip install "django==6.1.3"
   ```

4. Crear la base de datos (SQLite, no requiere instalar nada más):

   ```powershell
   python manage.py migrate
   ```

5. Crear un usuario administrador:

   ```powershell
   python manage.py createsuperuser
   ```

6. Levantar el servidor:

   ```powershell
   python manage.py runserver
   ```

   Abrir http://127.0.0.1:8000/admin/ e iniciar sesión.

## Estructura

| Carpeta     | Contenido |
|-------------|-----------|
| `config/`   | Configuración del proyecto (settings, urls) |
| `clientes/` | App de clientes |
| `mascotas/` | App de mascotas |
| `citas/`    | App de citas |

## Problemas comunes

- **`python` no se reconoce:** reinstalar Python marcando "Add Python to PATH".
- **No se puede ejecutar `activate` en PowerShell:** correr una vez
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
- **`No module named django`:** el entorno virtual no está activado (debe verse `(venv)` en la terminal).
