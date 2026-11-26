<!-- FRAGMENTO: el PDF recibido empieza en la sección "Otras opciones"; falta el comienzo del capítulo 15 (portada, introducción y primeras secciones). -->

# Capítulo 15. Introducción a Django y el mundo web

### Otras opciones

Django no es el único framework de Python para web. También existen:

- **Flask**: mucho más chico, deja más decisiones al programador. Bueno para
  APIs y microservicios.
- **FastAPI**: moderno, especializado en APIs, muy rápido, con soporte de type
  hints y async nativo.
- **Pyramid**, **Bottle**, y otros más chicos.

En este manual usamos Django porque es **el estándar** para aplicaciones web
completas en Python. Es el que más se pide en trabajos, el que tiene la
documentación más completa, y el que mejor se conecta con todo lo que
aprendieron en POO. Aprender Django primero es la mejor puerta de entrada,
después pueden explorar los otros si les interesa.

## El modelo cliente-servidor

Antes de meternos con Django, entendamos **cómo funciona el mundo web** en
general. Todas las páginas web, todas las apps móviles, todos los servicios en
línea funcionan bajo el mismo modelo básico: **cliente-servidor**.

- El **cliente** es tu navegador (Chrome, Firefox, Safari) o tu app móvil. Es
  quien **pide** información.
- El **servidor** es una computadora conectada a internet que **tiene** la
  información y sabe qué responder ante cada pedido. Es donde vive Django.

Cuando escribís mercadolibre.com.ar en tu navegador, esto es lo que pasa
(simplificado):

![Diagrama del modelo cliente-servidor. A la izquierda, una caja "NAVEGADOR (cliente)" con el ícono de una ventana de navegador con un globo terráqueo; a la derecha, una caja "SERVIDOR (Django)" con el ícono de un servidor. Una flecha rotulada "PEDIDO" va del navegador al servidor y otra rotulada "RESPUESTA" vuelve del servidor al navegador. Debajo, cuatro pasos numerados: 1, el navegador pide la página principal; 2, el servidor procesa, consulta datos y arma el HTML; 3, el navegador recibe el HTML y lo muestra; 4, cada click repite el ciclo. Al pie: "Toda la web funciona así: pedido → procesamiento → respuesta".](images/cap15-modelo-cliente-servidor.jpg)

Todo el mundo web funciona así. Las diferencias entre aplicaciones son qué tan
sofisticado es el pedido, qué información necesita el servidor, cómo arma la
respuesta.

### Los actores en detalle

En el mundo web hay tres componentes principales que conviene distinguir:

![Diagrama "Arquitectura Web Simplificada" con tres columnas. CLIENTE (inicia siempre): navegador (99% de los casos), app móvil, programa de consola (curl) y otro servidor (pedidos automáticos). SERVIDOR (Django): ícono de servidor con el logo de Django; escucha pedidos 24/7, procesa la lógica, genera respuestas y se conecta a la base de datos. BASE DE DATOS (servicio aparte): ícono de base de datos; almacena la información de forma persistente, Django se conecta para leer y escribir datos, en este manual se usa SQLite (archivo en disco) y en el capítulo 24 se migra a PostgreSQL. Una flecha "Pedido (HTTP)" va del cliente al servidor y otra "Respuesta (HTML / JSON, etc.)" vuelve; entre el servidor y la base de datos hay flechas "Consulta / Escritura" y "Resultados". Debajo, tres recuadros explicativos: "El cliente" (siempre es quien inicia; en el 99% de los casos es un navegador, pero también puede ser una app móvil, un programa de consola como curl o incluso otro servidor haciendo pedidos automáticos), "El servidor" (una computadora conectada a internet, escuchando pedidos las 24 horas; en desarrollo, tu propia máquina hace de servidor con Django corriendo local; en producción, es un servicio en la nube como AWS, DigitalOcean o Railway, o un servidor físico) y "La base de datos" (donde persiste la información; no es un componente del servidor, es un servicio aparte al que Django se conecta; en este manual se usa SQLite, un archivo en tu disco, que es el más simple; en el capítulo 24 se migra a PostgreSQL).](images/cap15-arquitectura-web-simplificada.jpg)

## HTTP: el idioma de la web

**HTTP** (*HyperText Transfer Protocol*) es el "idioma" que hablan el cliente y
el servidor entre ellos. Es un conjunto de reglas: cómo se formatea un pedido,
cómo se formatea una respuesta, qué código significa qué. Cada pedido HTTP
incluye: un **método**, una **URL**, un Encabezados y opcionalmente un
**cuerpo**.

![Diagrama "Un pedido HTTP está compuesto por las siguientes partes". A la izquierda, un ícono de computadora rotulado "CLIENTE" con una flecha punteada hacia un recuadro "PEDIDO HTTP". El recuadro tiene tres bloques: la línea de pedido "GET /productos/123?categoria=notebooks HTTP/1.1"; "Encabezados (Headers)" con "Host: mercadolibre.com.ar", "User-Agent: Mozilla/5.0" y "Accept: text/html"; y "Cuerpo (Body) - opcional" con un JSON de ejemplo {"nombre": "Producto", "precio": 1000}. A la derecha, cuatro círculos con flechas punteadas: 1. Un método (GET), qué quiere hacer el cliente; 2. Un recurso y query string, sobre qué dato, con parámetros opcionales; 3. Encabezados, información extra sobre el cliente; 4. Un cuerpo (opcional), datos enviados, usado en POST. Al pie, el recuadro "En Django": método → request.method | recurso → urls.py | query string → request.GET | body → request.POST | headers → request.headers.](images/cap15-pedido-http-partes.jpg)

### Los métodos más importantes (cliente ➡ servidor)

| Método | Significa | Ejemplo |
|---|---|---|
| **GET** | "Dame información" | Cargar una página, ver un perfil |
| **QUERY*** | "Dame una información, pero con una consulta compleja" | Filtrar resultados con criterios que no entran cómodos en una URL (ejemplo: búsquedas avanzadas con muchos filtros) |
| **POST** | "Toma esta información y hacé algo" | Enviar un formulario, crear una cuenta |
| **PUT / PATCH** | "Actualizá este recurso" | Editar tu perfil |
| **DELETE** | "Borrá este recurso" | Eliminar un post |

Cuando escribís google.com en el navegador, mandás un GET /. Cuando llenás un
formulario de contacto y hacés click en "Enviar", mandás un POST con los datos
del formulario.

#### Método QUERY

El IETF publicó RFC 10008 el 15 de junio de 2026, estandarizando el método
QUERY. Es el primer método HTTP genuinamente nuevo desde que PATCH se
incorporó como RFC 5789 en marzo de 2010, es decir, un vacío de 16 años.

**¿Qué resuelve?** Cierra un vacío que existía en HTTP desde el principio: un
request seguro e idempotente como GET, pero que puede llevar un body como
POST. Sirve para el caso típico de un endpoint GET con query string que "se
quedó chico" - filtros, claves de orden, cursores de paginación, un JSON
metido a la fuerza en un parámetro porque el framework no dejaba otra opción.

Tomalo con calma, recién se incorporó y todavía no corre nativo en Django. Pero
pronto será un estándar.

### La respuesta y sus códigos (servidor ➡ cliente)

Cada respuesta HTTP incluye un **código de estado**, un número de 3 dígitos que
resume qué pasó:

| Rango | Significa |
|---|---|
| **1xx** | Informativo (rara vez lo verás) |
| **2xx** | Éxito. El más común: **200 OK** |
| **3xx** | Redirección. Ej: **301** (mudanza permanente), **302** (temporal) |
| **4xx** | Error del cliente. **404** (no encontrado), **403** (prohibido), **401** (no autorizado) |
| **5xx** | Error del servidor. **500** (algo se rompió en Django) |

Cuando entrás a una URL que no existe y ves "404", es literalmente el servidor
diciéndote *"lo que pediste no está acá"*. Cuando algo explota en el backend,
verás "500 Internal Server Error".

### URLs: los recursos del servidor

Una **URL** identifica un recurso en el servidor. Por ejemplo:

```text
https://banco.utn.edu.ar/cuentas/1234/movimientos/
```

Se compone de:

- **https://**: protocolo (HTTPS = HTTP seguro).
- **banco.utn.edu.ar**: dominio (identifica el servidor).
- **/cuentas/1234/movimientos/**: ruta del recurso.

En Django vas a diseñar las rutas de tu aplicación: qué URL corresponde a qué
vista. Es una decisión de diseño importante, **buenas rutas hacen la
aplicación más fácil de usar y de mantener**.

## Arquitectura y modelo de software

Antes de meternos con Django específicamente, vale la pena hablar de dos
conceptos que va a acompañarte durante todo lo que sigue: **arquitectura de
software** y **modelo de software**.

### Arquitectura de software

Cuando construís una casa, no arrancás poniendo ladrillos. Antes hay un plano:
dónde van los cimientos, qué paredes son estructurales, por dónde pasan las
cañerías, cuáles son las habitaciones y cómo se conectan. Ese plano no es la
casa, pero define **cómo se organiza** la casa. Sin plano, terminás con un
cuarto sin puerta o un baño sin cañería.

En software pasa lo mismo. La **arquitectura de software** es la organización
de alto nivel de un sistema: qué partes tiene, qué hace cada una, y cómo se
comunican entre sí. No es el código concreto, es el plano que define cómo se
estructura ese código.

Ejemplos de decisiones arquitectónicas:

*"El sistema va a tener una base de datos, un servidor web, y un frontend".*

*"La lógica de negocio vive separada de la interfaz".*

*"Las validaciones se hacen en el servidor, no en el cliente".*

*"Cada módulo se comunica con los otros solo a través de interfaces
definidas".*

Estas decisiones no dicen **qué** hace exactamente cada línea de código. Dicen
**cómo se organiza** el sistema para que las líneas de código convivan bien.

Todos los sistemas tienen arquitectura, aunque no se piense conscientemente.
Un script de 20 líneas tiene una arquitectura trivial: todo pasa en un
archivo. Un sistema como Instagram tiene una arquitectura compleja: miles de
servicios distintos, bases de datos distribuidas, capas de caché, servicios de
imágenes. Entre uno y otro hay un continuo.

**La arquitectura importa cuando el sistema crece.** Un proyecto chico tolera
mala arquitectura, es fácil arreglarlo. Un proyecto grande con mala
arquitectura es imposible de mantener: cada cambio rompe cinco cosas no
relacionadas, agregar features cuesta cada vez más, los bugs se multiplican.
La calidad arquitectónica es lo que separa a sistemas que sobreviven años de
sistemas que se abandonan a los seis meses.

En el proyecto del banco, ya venimos tomando decisiones arquitectónicas sin
nombrarlas:

- Separamos los modelos en archivos por familia (personas.py, cuentas.py,
  movimientos.py).
- Las validaciones viven en un módulo aparte (validaciones.py).
- Las excepciones tienen su propio archivo (errores.py).
- La clase Banco no sabe cómo se persisten las cuentas - delega en un
  repositorio.

Cada una de esas fue una decisión arquitectónica. Al pasar a Django, vamos a
heredar una arquitectura que el framework nos impone. Vamos a ver que muchas
de esas decisiones ya las habíamos anticipado con SOLID.

### Modelo de software

Un **modelo de software** es un **patrón conceptual** que describe cómo
estructurar un tipo de sistema. Es una arquitectura probada, con nombre, que
otros desarrolladores ya usaron y encontraron efectiva. Cuando decís *"mi
sistema sigue el modelo X"*, otros que conocen el modelo entienden
inmediatamente cómo está organizado.

Es como cuando un arquitecto habla de *"estilo colonial"* o *"estilo
minimalista"*, no describe una casa específica, describe una familia de casas
con características comunes.

Ejemplos de modelos de software populares:

- **Monolito**: todo el sistema es una sola aplicación grande. Un solo
  servidor, una sola base de datos, un solo repositorio de código. Simple de
  arrancar, se vuelve complejo con el tamaño.
- **Microservicios**: el sistema se divide en muchos servicios independientes
  que se comunican por red. Cada servicio tiene su base, su equipo, su ritmo.
  Complejo de arrancar, escala mejor.
- **Cliente-servidor**: separación clara entre el cliente (navegador, app) y
  el servidor. Es el modelo dominante para web.
- **Serverless**: no tenés servidores propios, el código corre en la
  infraestructura de un proveedor (AWS Lambda, Google Cloud Functions) que
  ejecuta funciones cuando llegan pedidos.
- **MVC (Model-View-Controller)**: separa el sistema en tres capas: datos,
  lógica de presentación, y coordinación entre ellas. Muy usado en
  aplicaciones con interfaz.
- **MVT (Model-View-Template)**: variante de MVC, específica de Django y
  algunos frameworks similares. Es la que vamos a ver en detalle en la
  próxima sección.

Los modelos no son leyes: son **guías**. Un sistema real casi siempre mezcla
ideas de varios modelos. Pero conocer los modelos te da vocabulario para
pensar y comunicar arquitectura.

### Por qué importa esto ahora

Django implementa un modelo específico: **MVT**. Cuando escriban código
Django, van a estar aplicando este modelo, a veces conscientemente, a veces
sin darse cuenta. Entender el modelo antes de meter mano al código hace que el
framework tenga sentido: cada archivo, cada convención, cada nombre estará
ubicado en un mapa mental claro.

Sin este marco, Django parece un montón de reglas arbitrarias:

*¿por qué los modelos van en models.py y las vistas en views.py?*

*¿Por qué las URLs se separan en su propio archivo?*

Con el marco, todo tiene lógica: **cada archivo corresponde a una capa
distinta del modelo MVT**, y las capas están separadas porque tienen
responsabilidades distintas, exactamente el mismo principio de SRP que vimos
con SOLID.

### El patrón MVT: Model-View-Template

Django organiza el código en **tres capas**, con responsabilidades bien
separadas. Este patrón se llama **MVT** (Model-View-Template):

![Diagrama "Cómo se organizan los componentes principales de una aplicación Django". Tres cajas apiladas con flechas hacia abajo. MODEL: "Los datos y la lógica del negocio", clases como Cuenta, Persona, Movimiento. VIEW: "Recibe el pedido y decide qué hacer", consulta modelos y elige qué mostrar, con la etiqueta "Es el coordinador". TEMPLATE: "HTML con huecos que se llenan con datos", "Es la capa visual que ve el usuario". Debajo, tres recuadros: Model (modelo), representa el dominio y contiene la lógica de negocio, en Django son clases Python que heredan de models.Model; View (vista), recibe un pedido HTTP y devuelve una respuesta, decide qué modelos consultar, qué template usar y qué datos enviar; Template (plantilla), es un archivo HTML con marcadores especiales donde se insertan los datos.](images/cap15-patron-mvt.jpg)

### Comparación con MVC

Si ya viste MVC (Model-View-Controller) en Java, PHP o similares, MVT es
prácticamente lo mismo con nombres distintos:

| En MVC | En Django MVT |
|---|---|
| Model | Model |
| View (lo visual) | Template |
| Controller (la lógica) | View |

Es solo terminología. En Django, "view" es lo que otros llaman "controller",
"template" es lo que otros llaman "view". Lo importante es la **separación de
responsabilidades**: datos, lógica y presentación en capas distintas.

## Instalación

Antes de seguir, instalá Django. Necesitás tener Python instalado (ya lo
tenés).

### Crear un entorno virtual

Un **entorno virtual** (o *venv*) es una instalación aislada de Python
específica para un proyecto. Sirve para que las librerías que instales para el
banco no se mezclen con las de otros proyectos. Es una práctica estándar de
Python.

Abrí una terminal, andá a la carpeta donde vas a tener el proyecto, y creá el
entorno:

```bash
python -m venv .venv
```

Esto crea una carpeta **.venv/** con una instalación aislada de Python. Ahora
hay que **activarlo**:

**En Linux/Mac:**

```bash
source .venv/bin/activate
```

**En Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

Cuando el entorno está activo, tu prompt de terminal muestra (.venv) al
principio. Todo lo que instales con pip va a quedar solo en este entorno, no
en el Python global de la máquina.

Para desactivarlo cuando termines:

```bash
deactivate
```

### Instalar Django

Con el entorno virtual activo:

```bash
pip install django==5.2
```

Fijamos la versión 5.2 (LTS, *Long Term Support*) para que todo el manual sea
consistente. Al escribir esto, es la versión estable soportada por varios
años.

Para verificar que quedó instalado:

```bash
python -m django --version
```

Debería imprimir 5.2 (o similar).

## Estructura de un proyecto Django

Django distingue dos conceptos:

- **Proyecto**: la aplicación web completa. En nuestro caso, "banco".
- **App**: una unidad funcional dentro del proyecto. Un proyecto puede tener
  varias apps.

![Diagrama "Django distingue dos conceptos principales". Arriba, una caja "PROYECTO: La aplicación web completa", con el ejemplo "banco". De ella salen flechas ("Un proyecto puede tener varias apps") hacia tres cajas APP: "cuentas" (maneja cuentas y movimientos), "clientes" (maneja personas físicas y jurídicas) y "usuarios" (maneja login y perfiles), bajo el rótulo "Por ejemplo, en nuestro banco podríamos tener". Debajo, dos recuadros: "Proyecto", es el sitio o sistema completo, contiene la configuración general y puede agrupar varias apps; y "App", es un módulo funcional dentro del proyecto, cada app resuelve una parte del sistema.](images/cap15-proyecto-y-apps.jpg)

Cada app es un módulo Python autocontenido, con sus propios modelos, vistas y
templates. Se pueden reutilizar entre proyectos. Para nuestro banco, vamos a
arrancar con una sola app llamada banco, y si más adelante conviene, la
dividimos.

### 1. Crear el proyecto

```bash
django-admin startproject banco_utn .
```

El **.** al final es importante: crea el proyecto **en el directorio actual**,
no dentro de una subcarpeta con el mismo nombre. Sin el punto, Django creaba
una carpeta anidada, decisión histórica que confunde a todos los principiantes.

Después de correr eso, tu carpeta tiene esta estructura:

![Árbol de archivos del proyecto. La carpeta raíz "banco" contiene: ".venv" (entorno virtual, no se toca), "banco_utn" (configuración del proyecto) y "manage.py" (herramienta de comando). La carpeta "banco_utn" contiene: "__init__.py" (marca a esta carpeta como paquete Python), "settings.py" (configuración principal), "urls.py" (URLs raíz del proyecto), "asgi.py" (para despliegue asincrónico) y "wsgi.py" (para despliegue tradicional).](images/cap15-estructura-proyecto-django.png)

Qué es cada cosa:

**banco_utn/**: la carpeta de configuración del proyecto (no confundir con las
apps, que vienen después).

**settings.py**: el corazón de la configuración. Base de datos, apps
instaladas, idioma, zona horaria, seguridad. Vas a tocarlo varias veces.

**urls.py**: define qué URL corresponde a qué vista. Es el "mapa" del
proyecto.

**asgi.py** y **wsgi.py**: interfaces para conectar Django con servidores web
reales. Los tocaremos solo al final.

**manage.py**: script que te da acceso a todos los comandos de Django
(`runserver`, `makemigrations`, `migrate`, `createsuperuser`, etc.).

### 2. Crear la primera app

```bash
python manage.py startapp banco
```

Ahora hay una nueva carpeta banco/:

![Árbol de archivos del proyecto con la app creada. La carpeta raíz "banco" contiene ".venv", "banco_utn" (con __init__.py, setting.py, urls.py, asgi.py y wsgi.py), "manage.py" y la nueva carpeta "banco", la primera app del proyecto. La carpeta "banco" contiene: "__init__.py" (marca a esta carpeta como paquete Python), "admin,py" (configuración del admin para esta app), "apps.py" (metadatos de la app), "models.py" (modelos de datos), "tests.py" (tests de la app), "views.py" (vistas, lo que se muestra) y "migrations" (migraciones de la BD) que a su vez contiene un "__init__.py".](images/cap15-estructura-app-banco.png)

### 3. Registrar la app en el proyecto

Django necesita saber que existe nuestra app. Editá `banco_utn/settings.py` y
buscá la lista `INSTALLED_APPS`:

**banco_utn/settings.py**

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'banco',                            # agregar esta línea
]
```

Django viene con varias apps built-in (admin, auth, sessions...). Nosotros
agregamos la nuestra al final de la lista.

### 4. Configurar idioma y zona horaria

Un paso más de setup, no obligatorio pero útil. En `settings.py`, buscá:

```python
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
```

Y cambialo por:

```python
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
```

Con esto, Django muestra los mensajes en español y las fechas en horario
local. Importante para un sistema bancario argentino.

### 5. Correr el servidor de desarrollo

Django viene con un servidor web integrado para desarrollo (**no** para
producción). Lo iniciás con:

```bash
python manage.py runserver
```

Vas a ver algo como:

```text
Watching for file changes with StatReloader

Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly
until you apply the migrations for app(s): admin, auth, contenttypes,
sessions.
Run 'python manage.py migrate' to apply them.

November 20, 2026 - 15:32:41
Django version 5.2, using settings 'banco_utn.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Ignorá el warning sobre migraciones (lo resolvemos en el próximo capítulo). Lo
importante es la línea:

```text
Starting development server at http://127.0.0.1:8000/
```

Eso significa: **el servidor está corriendo en tu propia computadora, en el
puerto 8000.**

#### Direcciones IP y localhost

127.0.0.1 es una dirección IP especial que significa "esta misma computadora".
También se puede escribir como localhost. Cuando entrás a
http://127.0.0.1:8000/ desde tu navegador, estás pidiéndole a tu propia
máquina que actúe como servidor.

En producción, la dirección sería la IP pública del servidor (ejemplo:
banco.utn.edu.ar con IP 200.16.100.42). En desarrollo, todo pasa localmente.

El :8000 es el **puerto**: un número que distingue distintos servicios en la
misma máquina. Django por defecto usa el 8000. Podés cambiarlo con python
manage.py runserver 9000.

### 6. Abrir el navegador

Con el servidor corriendo, abrí Chrome (o Firefox) y andá a:

```text
http://127.0.0.1:8000/
```

Vas a ver la página de bienvenida de Django: un cohete verde, algunos enlaces a
documentación, y un mensaje que dice *"The install worked successfully!"*,
literalmente, la instalación funcionó.

Esa es **tu primera aplicación web** servida desde tu computadora.

Para detener el servidor, volvé a la terminal y presioná `Ctrl+C`.

## Un primer "Hola mundo" propio

La página de bienvenida está bien, pero es la que Django trae por defecto.
Vamos a reemplazarla por una propia, para ver el ciclo completo pedido ➡ vista
➡ respuesta.

### 1. escribir la vista

Editá `banco/views.py` y reemplazá su contenido:

**banco/views.py**

```python
from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>Bienvenido al Banco UTN</h1>")
```

Explicación línea por línea:

- **`from django.http import HttpResponse`**: importamos la clase
  HttpResponse, que representa una respuesta HTTP. Es lo que vamos a
  devolver.
- **`def home(request):`**: definimos una función llamada home que recibe un
  objeto request (el pedido del cliente). Por convención, siempre se llama
  request, aunque técnicamente es como self: solo un nombre.
- **`return HttpResponse(...)`**: devolvemos una respuesta con HTML dentro.

Una **view** de Django es, en su forma más simple, esto: una función que
recibe un request y devuelve una HttpResponse. Nada más.

### 2. mapear la URL

Django todavía no sabe que existe esta vista. Hay que decirle: *"cuando alguien
pida la URL raíz (/), llamá a home"*. Eso se configura en
`banco_utn/urls.py`.

Editá el archivo:

**banco_utn/urls.py**

```python
from django.contrib import admin
from django.urls import path
from banco import views     # importamos nuestras views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),      # esta línea es nueva
]
```

Explicación:

- **`from banco import views`**: importamos el módulo views de nuestra app.
- **`path('', views.home)`**: definimos una URL. El primer argumento es la
  ruta (vacía = raíz), el segundo es la vista que responde.

urlpatterns es una lista. Cada elemento asocia una URL con una vista.

### 3. probar

Volvé a la terminal (con el venv activo) y arrancá el servidor:

```bash
python manage.py runserver
```

En el navegador, actualizá http://127.0.0.1:8000/. Ya no ves el cohete verde:
ahora ves "Bienvenido al Banco UTN".

**Eso es todo.** El ciclo completo de una app web mínima:

1. El navegador manda un GET /.
2. Django recibe el pedido, mira urls.py, encuentra la ruta ''.
3. Django ejecuta views.home(request).
4. La vista devuelve una HttpResponse con HTML.
5. Django manda esa respuesta al navegador.
6. El navegador la muestra.

Cada página web que existe funciona con este ciclo. Lo demás son variaciones -
pedidos más complejos, más datos, respuestas más elaboradas - pero el esquema
básico es siempre este.

## Recarga automática

Un detalle práctico: Django detecta cuando modificás archivos y **recarga el
servidor automáticamente**. No hace falta detenerlo y reiniciarlo cada vez que
cambiás algo. Solo tenés que actualizar el navegador para ver los cambios.

Probalo: cambiá el texto de HttpResponse a otra cosa, guardá el archivo,
actualizá el navegador. Vas a ver el cambio inmediatamente.

Esto vale **solo para el servidor de desarrollo**. En producción no funciona
así (por buenas razones que veremos al final del manual).

## Anticipando el próximo capítulo

Con esto ya tenés:

- Un proyecto Django creado.
- Una app registrada.
- El servidor de desarrollo corriendo.
- Una vista que responde a la URL raíz.

Pero todavía no hay modelos, ni base de datos, ni nada de lo que armamos en el
capítulo 15. En el próximo capítulo de **Modelos y ORM**, vamos a hacer que
nuestras clases Cuenta, Persona, Movimiento renazcan como modelos Django. Van
a ser prácticamente iguales a las clases Python que ya escribimos, pero con
dos diferencias mágicas:

- Se **persisten automáticamente** en una base de datos.
- Vienen con **muchos métodos gratis**: .objects.create(), .objects.filter(),
  .save(), .delete().

Cuando lleguemos al final del capítulo 17, van a haber "traducido" todo el
sistema bancario del capítulo 15 a Django, sin cambiar la lógica, solo la
forma. Y el capítulo 18 va a mostrar la promesa que veníamos haciendo desde el
capítulo 12: **el ABM completo, con interfaz web incluida, generado
automáticamente por Django**.

Ese momento, cuando ven que varias semanas de trabajo escribiendo
`Banco.abrir_cuenta`, `Banco.buscar_cuenta`, `Banco.cerrar_cuenta` se
reemplaza por una configuración de tres líneas en Django, es donde POO cobra
sentido pleno. Todo lo que hiciste a mano no fue en vano: fue el entrenamiento
que te permitió entender por qué Django está diseñado como está
