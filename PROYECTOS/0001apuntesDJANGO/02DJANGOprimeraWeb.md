# Guía: mi primera página web con Django
Guía paso a paso para alumnos que recién empiezan con Django. Dos etapas:
1. **Etapa 1:** una página sencilla, con `render`, que muestra las partes de una página web (header, nav, body, footer) con colores y bordes.
2. **Etapa 2:** una plantilla base (`base.html`) que se extiende con `{% extends %}` para no repetir código.

**Punto de partida:** el proyecto `biblioteca` ya está creado, el servidor corre con `python manage.py runserver` y existe un archivo `views.py`. No hace falta ninguna app, modelo ni base de datos.

**Objetivos de la clase:**
- Reconocer las cuatro zonas de una página web: **header**, **nav**, **body** y **footer**.
- Entender qué hace `render` y en qué se diferencia de abrir un archivo HTML directamente.
- Entender para qué sirve la herencia de plantillas (`base.html` + `extends`).

# ETAPA 1: Una página sencilla con `render`

## Paso 1: crear la carpeta `templates`
En la raíz del proyecto, junto a `manage.py`:
```
biblioteca/
├── manage.py
├── biblioteca/
│   ├── settings.py
│   ├── urls.py
│   └── views.py
└── templates/        <- carpeta nueva
```
Ojo: hay **dos carpetas `biblioteca`**. La externa es la que tiene `manage.py`; la interna tiene `settings.py`, `urls.py` y `views.py`. `templates` va en la **externa**, junto a `manage.py`, nunca dentro de la interna. Esa carpeta externa es el `BASE_DIR` de `settings.py`.

## Paso 2: avisarle a Django dónde están las plantillas
En `biblioteca/settings.py`, buscar `TEMPLATES` y completar la línea `'DIRS'` (viene vacía, `[]`):
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
`BASE_DIR` es la carpeta raíz del proyecto. Con esa línea, Django busca las plantillas en `templates/`. **Guardar `settings.py`**: el servidor se reinicia solo al guardar.

## Paso 3: crear `inicio.html`
Dentro de `templates/`, crear `inicio.html`. **Conviene crearlo desde VS Code** (clic derecho en `templates`, "New File"): el Explorador de Windows suele ocultar las extensiones y el archivo puede quedar como `inicio.html.txt`, que Django no encuentra.
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Inicio | Biblioteca</title>
    <style>
        div {
            border: 4px solid black;
            padding: 20px;
            margin: 10px;
            font-family: Arial, sans-serif;
        }
        .header { background-color: #00bcd4; }  /* celeste fuerte */
        .nav    { background-color: #4caf50; }  /* verde fuerte */
        .body   { background-color: #ffeb3b; }  /* amarillo fuerte */
        .footer { background-color: #ff5722; }  /* naranja fuerte */
    </style>
</head>
<body>
    <div class="header">
        <h1>HEADER</h1>
        <p>Es la cabecera: el título del sitio, el logo.</p>
    </div>
    <div class="nav">
        <h2>NAV</h2>
        <p>Es la navegación: el menú con los links a otras páginas.</p>
    </div>
    <div class="body">
        <h2>BODY</h2>
        <p>Es el cuerpo: el contenido principal, lo que cambia en cada página.</p>
    </div>
    <div class="footer">
        <h2>FOOTER</h2>
        <p>Es el pie de página: datos de contacto, derechos, etc.</p>
    </div>
</body>
</html>
```
Cada `div` tiene su **borde** y su **color de fondo** para distinguirse a simple vista.

## Paso 4: escribir la vista
En `views.py`:
```python
from django.shortcuts import render

def inicio(request):
    return render(request, 'inicio.html')
```
- `request` es la petición que llega del navegador.
- `render(request, 'inicio.html')` busca la plantilla en `templates/`, la procesa y devuelve la respuesta al navegador.

## Paso 5: conectar la URL
En `biblioteca/urls.py`:
```python
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
]
```
`path('', ...)` es la dirección raíz del sitio. Si `views.py` está dentro de una app y no en la carpeta del proyecto, cambiar la importación por `from nombre_de_la_app import views`.

## Paso 6: probar
```
python manage.py runserver
```
Abrir `http://127.0.0.1:8000/`. Deben verse cuatro bloques (celeste, verde, amarillo y naranja), cada uno con su borde negro.

## Para explicar en clase: ¿qué hace `render`?

### Experimento 1: abrir el archivo directamente vs. verlo a través de Django
1. Abrir `inicio.html` con doble clic desde el explorador de archivos. La dirección empieza con `file:///...`. Acá **no interviene Django**: el navegador lee un archivo del disco.
2. Abrir `http://127.0.0.1:8000/`. Se ve igual, pero ahora **Django recibió una petición, ejecutó la vista y devolvió el HTML**.

Con una plantilla fija se ven idénticas. La diferencia aparece en el experimento siguiente.

### Experimento 2: pasar datos a la plantilla
En `views.py`:
```python
def inicio(request):
    contexto = {'nombre_biblioteca': 'Biblioteca Municipal'}
    return render(request, 'inicio.html', contexto)
```
En `inicio.html`, cambiar el título del header:
```html
<h1>{{ nombre_biblioteca }}</h1>
```
| Cómo se abre | Qué se ve en el header |
|---|---|
| Doble clic al archivo (`file:///`) | `{{ nombre_biblioteca }}` tal cual, como texto |
| A través de Django (`127.0.0.1:8000`) | `Biblioteca Municipal` |

**Conclusión:** el navegador no entiende `{{ }}`. Django lo procesa en el servidor, reemplaza la variable por su valor y recién entonces manda HTML común al navegador. A eso se le llama **renderizar**.

### Experimento 3: `render` vs. `HttpResponse`
Agregar en `views.py`:
```python
from django.http import HttpResponse

def inicio_directo(request):
    return HttpResponse("<h1>Hola desde Django</h1>")
```
Y en `urls.py`, dentro de `urlpatterns`: `path('directo/', views.inicio_directo),`. Abrir `http://127.0.0.1:8000/directo/`: funciona, pero el HTML está escrito como texto dentro del código Python.

| | `HttpResponse` | `render` |
|---|---|---|
| Dónde está el HTML | Dentro del código Python, como texto | En un archivo `.html` aparte |
| Páginas grandes | Incómodo, imposible de mantener | Ordenado |
| Datos dinámicos | Hay que armar el texto a mano | `{{ variable }}` y etiquetas de plantilla |

`render` carga la plantilla, la procesa con los datos y devuelve un `HttpResponse`: es una forma cómoda de armarlo.

### Ver lo que recibe el navegador
Con la página abierta: clic derecho, **Ver código fuente de la página** (o F12). El navegador recibe HTML común, sin ninguna llave `{{ }}`: Django ya hizo su trabajo antes de enviarlo.

# ETAPA 2: Una base y su extensión

## El problema que resuelve
Para una segunda página ("Contacto") habría que copiar todo el HTML: header, nav, footer y estilos. Con diez páginas, diez copias; si cambia el menú, hay que modificar diez archivos. **Solución:** una plantilla base con la estructura común, y cada página define solo lo que cambia.

**Importante:** el menú de `base.html` usa `{% url 'contacto' %}`. Si esa URL no existe todavía, Django da error `NoReverseMatch`. Por eso primero se crea la ruta de contacto (Paso 7) y recién después la base. **No recargar la página hasta el Paso 11.**

## Paso 7: vista y URL de contacto
En `views.py`:
```python
def contacto(request):
    return render(request, 'contacto.html')
```
En `urls.py`, dentro de `urlpatterns`:
```python
path('contacto/', views.contacto, name='contacto'),
```

## Paso 8: crear `base.html`
En `templates/`, crear `base.html`. Es el HTML de `inicio.html`, con el contenido del body reemplazado por un **bloque** y el menú completo:
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{% block titulo %}Biblioteca{% endblock %}</title>
    <style>
        div {
            border: 4px solid black;
            padding: 20px;
            margin: 10px;
            font-family: Arial, sans-serif;
        }
        .header { background-color: #00bcd4; }
        .nav    { background-color: #4caf50; }
        .body   { background-color: #ffeb3b; }
        .footer { background-color: #ff5722; }
        .nav a  { color: black; font-weight: bold; margin-right: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Biblioteca Municipal</h1>
    </div>
    <div class="nav">
        <a href="{% url 'inicio' %}">Inicio</a>
        <a href="{% url 'contacto' %}">Contacto</a>
    </div>
    <div class="body">
        {% block contenido %}
        {% endblock %}
    </div>
    <div class="footer">
        <p>&copy; 2026 Biblioteca Municipal</p>
    </div>
</body>
</html>
```
Hay dos **bloques**, `titulo` y `contenido`: son los huecos que cada página hija completa. `{% url 'inicio' %}` genera la dirección a partir del `name` definido en `urls.py`.

## Paso 9: extender la base en `inicio.html`
Reemplazar **todo** el contenido de `inicio.html` por:
```html
{% extends 'base.html' %}

{% block titulo %}Inicio | Biblioteca{% endblock %}

{% block contenido %}
    <h2>BODY de la página de inicio</h2>
    <p>Esta zona es la única que cambia entre una página y otra.</p>
{% endblock %}
```
- `{% extends 'base.html' %}` tiene que ser **la primera línea** del archivo.
- Todo lo que se escriba fuera de un `{% block %}` se ignora.
- Header, nav y footer vienen de la base: no hace falta repetirlos.

## Paso 10: crear `contacto.html`
En `templates/contacto.html`:
```html
{% extends 'base.html' %}

{% block titulo %}Contacto | Biblioteca{% endblock %}

{% block contenido %}
    <h2>BODY de la página de contacto</h2>
    <p>Dirección: Calle Falsa 123.</p>
    <p>Teléfono: 0221 000-0000.</p>
{% endblock %}
```

## Paso 11: probar
Recargar `http://127.0.0.1:8000/` y navegar con el menú entre **Inicio** y **Contacto**. Header, nav y footer son los mismos en las dos páginas; solo cambia el cuerpo.

**Demostración final:** cambiar el texto del footer **solo en `base.html`** y recargar las dos páginas. El cambio aparece en ambas: eso es la herencia de plantillas.

## Cómo leer el error `TemplateDoesNotExist`
Es el error más común de la clase. La pantalla amarilla tiene una sección **"Django tried loading these templates"** que lista, en orden, las rutas donde Django buscó la plantilla:
- **Solo aparecen rutas de `admin` y `auth`** (dentro de `.venv\Lib\site-packages\django\contrib\...`): `'DIRS'` está vacío o `settings.py` no se guardó. Volver al Paso 2.
- **Aparece una ruta tuya** (`django.template.loaders.filesystem.Loader: C:\...\templates\inicio.html`): `DIRS` está bien. Ir a esa carpeta y comprobar que el archivo esté exactamente ahí y se llame `inicio.html` (sin `.txt` al final).

Esa lista dice exactamente dónde busca Django: sirve para enseñar a leer los errores en lugar de adivinar.

### Si el error sigue igual después de modificar `settings.py`
1. **Confirmar que el servidor no tomó el cambio.** En la misma pantalla de error, bajar hasta la sección **Settings** y buscar `TEMPLATES`. Si dice `'DIRS': []`, el servidor sigue con la configuración vieja.
2. **Abrir el `settings.py` correcto**: el que está dentro de la carpeta **interna** `biblioteca` (la que también tiene `urls.py` y `views.py`), por ejemplo `...\proyectos\biblioteca\biblioteca\biblioteca\settings.py`. Si hay otra copia del proyecto en otra carpeta, modificarla no cambia nada.
3. **Corregir la línea.** Con Ctrl+F buscar `'DIRS'` y cambiar:
   ```python
   # ANTES (como lo genera Django)
   'DIRS': [],

   # DESPUÉS
   'DIRS': [BASE_DIR / 'templates'],
   ```
   Errores típicos al escribirla: olvidar la coma final, escribir `Base_Dir` en vez de `BASE_DIR`, o dejar `templates` sin comillas.
4. **Guardar con Ctrl+S.** En VS Code, el punto blanco en la pestaña del archivo indica cambios sin guardar.
5. **Mirar la terminal de `runserver`.** Debe aparecer un aviso de que el archivo cambió y el servidor se reinició. Si no aparece, detener el servidor con Ctrl+C y volver a correr `python manage.py runserver`.
6. **Recargar la página.** Si quedó bien, en la sección **Settings** se ve `'DIRS': [WindowsPath('C:/.../templates')]` y la lista de rutas del error suma `django.template.loaders.filesystem.Loader: C:\...\templates\inicio.html`.

## Errores comunes
| Error | Causa probable |
|---|---|
| `TemplateDoesNotExist: inicio.html` | `'DIRS'` vacío o sin guardar, `templates` fuera de la carpeta de `manage.py` (por ejemplo dentro de la `biblioteca` interna), o el archivo quedó como `inicio.html.txt`. Ver la sección de arriba |
| `NoReverseMatch: 'contacto'` | Falta `name='contacto'` en `urls.py`, o se recargó antes de crear la ruta (Paso 7) |
| Se ve el HTML pero sin colores | Falta el `<style>` o hay un error de tipeo en los nombres de las clases |
| La página de contacto se ve vacía | El texto está fuera del `{% block contenido %}` |
| Error con `extends` | `{% extends %}` no es la primera línea del archivo |
| `ImportError` en `urls.py` | La importación de `views` no corresponde a dónde está el archivo |

## Ideas para seguir
- Reemplazar los `div` por las etiquetas semánticas `<header>`, `<nav>`, `<main>` y `<footer>` y ver qué cambia (para el navegador y para los lectores de pantalla).
- Mover el CSS a un archivo propio en `static/css/` y enlazarlo con `{% load static %}`.
- Crear una tercera página ("Catálogo") para repetir el ejercicio sin ayuda.
- Más adelante: crear una app `libros`, un modelo `Libro` y mostrar los datos reales en la plantilla.
