# Capítulo 18. Django: URLs y vistas

*Del pedido a la respuesta.*

## ¿Por qué leemos este capítulo?

En el capítulo anterior vimos que el admin de Django resuelve
automáticamente el ABM para nuestros modelos. Con seis líneas de código
teníamos una interfaz web completa para empleados del banco.

Pero el admin es para eso: **para empleados**. Ana, cuando quiere ver el saldo
de su cuenta, no va a entrar al admin de Django. Va a entrar al **home
banking**: una interfaz pensada para ella, que le muestre solo sus cuentas, con
el diseño que le hace sentir que está en un banco.

Ese home banking lo vamos a construir nosotros. Es donde Django deja de
"generar" y empezamos a **programar la aplicación que queremos**. En este
capítulo damos los primeros dos pasos:

- **URL**: cómo definimos qué direcciones responde nuestro sitio.
- **Vistas**: qué código se ejecuta cuando alguien entra a cada dirección.

En el capítulo 20 (Templates) vamos a agregar el HTML lindo con Bootstrap. Por
ahora, respuestas simples - pero ya con la lógica bien organizada.

## Recordando: cómo Django procesa un pedido

Cuando el navegador manda un pedido HTTP a Django, este es el flujo:

![Flujo de ida y vuelta entre navegador, servidor web y Django. Tres columnas:
NAVEGADOR (cliente), SERVIDOR WEB (runserver / Gunicorn) y DJANGO. Flecha azul
de ida del navegador al servidor rotulada "HTTP: GET /cuentas/001-100/"; flecha
azul del servidor a Django rotulada "request (objeto Python)". Flecha verde de
vuelta de Django al servidor rotulada "HttpResponse (objeto Python)" y del
servidor al navegador rotulada "HTTP: 200 OK + HTML". Pasos numerados: 1. En el
navegador, escribís /cuentas/001-100/ y presionás Enter. 2. El servidor web
acepta la conexión. 3. El servidor parsea el HTTP y arma el objeto request. 4.
Django lee urls.py del proyecto. 5. Encuentra la ruta que coincide con la URL.
6. Ejecuta la vista, pasándole el request. 7. La vista devuelve un
HttpResponse. 8. El servidor traduce la HttpResponse a HTTP. 9. El navegador
lee el HTML y lo renderiza en pantalla. Al pie, un recuadro "En resumen":
navegador → servidor web → Django → servidor web →
navegador.](images/cap18-flujo-navegador-servidor-django.jpg)

Los dos protagonistas: `urls.py` (el mapa) y las **vistas** (el código que
ejecuta cada mapeo). Vamos con ambos.

## Términos para recordar

### runserver / Gunicorn

Son **servidores web**: programas que escuchan pedidos que llegan por internet
y se los entregan a Django. `runserver` es el servidor simple que viene con
Django, pensado solo para desarrollo local. Gunicorn es el servidor "de verdad"
que se usa en producción, más robusto y capaz de atender a muchos usuarios a la
vez.

### HTTP: GET /cuentas/001-100/

HTTP es el "idioma" que hablan el navegador y el servidor entre ellos. GET es
el tipo de pedido: significa "dame información" (como ya vimos otros tipos son
POST para enviar datos, DELETE para borrar, etc.). /cuentas/001-100/ es la
URL, que identifica qué recurso se pide: la parte /cuentas/ señala la sección o
categoría, y 001-100 identifica el elemento específico dentro de esa sección.
Todo junto se lee: *"de la sección de cuentas, dame la que tiene número
001-100"*

### Parsear

Del inglés *parse*, significa **analizar un texto para extraer su estructura**.
El HTTP llega al servidor como un montón de texto crudo con encabezados,
direcciones, cookies. Parsearlo es descomponerlo en partes ordenadas: *"esto es
el método, esto es la URL, esto es un encabezado, esto son los datos
enviados"*. Es traducir texto sin forma a información utilizable.

### Request

Es el **objeto Python** que representa el pedido del navegador dentro de
Django. Contiene toda la información sobre lo que se pidió: qué URL, qué método
(GET/POST), qué datos vienen adjuntos, quién es el usuario, qué navegador usa.
Django le pasa este objeto a la vista para que decida cómo responder.

### vista (view)

Es una **función de Python** que decide qué hacer con un pedido y qué
responder. Recibe el request, consulta lo que necesite (una base de datos, un
cálculo), y devuelve una respuesta. Es el "cerebro" de cada página: cuando
alguien pide /cuentas/001-100/, hay una vista específica que responde ese
pedido.

### HttpResponse

Es el **objeto Python** que representa la respuesta que Django le manda al
navegador. Contiene el contenido a mostrar (usualmente HTML), un código de
estado (200 si todo salió bien, 404 si no se encontró la página) y algunos
encabezados. Es la respuesta de Django, todavía en formato Python, antes de que
el servidor la convierta en HTTP.

### Renderizar

Es la acción del **navegador de "dibujar" el HTML en la pantalla**. El servidor
le manda al navegador un texto con etiquetas HTML (`<h1>`, `<table>`, `<div>`,
etc.), el navegador interpreta esas etiquetas y las convierte en algo visual:
títulos, tablas, imágenes, botones. Renderizar es transformar código HTML en la
página que el usuario ve.

## URLs: el mapa del sitio

Es lo más crucial de todo, ¿Cómo encontrar un recurso?

![Diagrama horizontal de seis pasos del recorrido de un pedido. 1: El
navegador envía el pedido (ícono de navegador con un globo, debajo "GET /"). 2:
El servidor lo recibe (ícono de servidor). 3: Django lee urls.py del proyecto
(ícono de archivo urls.py). 4: Busca el path que matchea la URL (cuadro
"urlpatterns" con dos filas: 'admin/' → admin.site.urls y '' (vacío) →
views.home; un recuadro punteado debajo dice "Coincide: '' (vacío) con la URL
/"). 5: Ejecuta la vista asociada (cuadro views.py con def home(request):). 6:
La vista devuelve un HttpResponse (HTML). Una línea punteada rotulada
"Respuesta HTTP (HTML)" vuelve desde el último paso hasta el
navegador.](images/cap18-recorrido-pedido-urls-views.jpg)

Cuando llega una petición, el servidor se la entrega a Django, que abre su
"guía telefónica" (el archivo **urls.py**) y busca **quién atiende ese
pedido**. Cada ruta apunta a una vista específica en **views.py**, que arma la
respuesta y la devuelve al navegador, casi siempre en forma de HTML.

El recorrido es siempre el mismo:

![Tres tarjetas unidas por flechas. A la izquierda, "urls.py" (azul, ícono de
mapa con un punto de destino): "Define la ruta". Flecha rotulada "llama a la
vista". En el centro, "views.py" (verde, logo de Python y una ventana con
código): "Procesa el pedido". Flecha rotulada "renderiza". A la derecha, "HTML"
(naranja, ícono de página web): "Muestra la
respuesta".](images/cap18-urls-views-html.jpg)

Por ejemplo, cuando el navegador pide /, Django encuentra en **urls.py** que
ruta corresponde y esta indica donde está la **vista home** en **views.py**.

**`banco_utn/urls.py`**

```python
from django.contrib import admin
from django.urls import path
from banco import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),            # ruta '' (raíz) llama función home() del
                                     # archivo views.py de la app 'banco'
]
```

`urlpatterns` es una lista. Cada elemento es un `path()` que **mapea una URL a
una vista específica** en **views.py**. por ejemplo views,home dice:
"Encuentra en archivo views, no pone la extensión porque se sobreentiende, a la
función home, que es la responsable de responder"

En **views.py** encontras a esa función:

**`banco/views.py`**

```python
from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>Bienvenido al Banco UTN</h1>")
```

Resumiendo:

![Esquema "Resumiendo" con flechas dibujadas a mano. A la izquierda el rótulo
SERVIDOR con una flecha hacia el bloque "# banco_utn/urls.py" que contiene
"urlpatterns = [ ... path('', views.home), ]". Desde la línea path('',
views.home) una flecha baja y otra sube hacia el bloque "# banco/views.py", que
contiene "def home(request): ...". Desde ese bloque una flecha sale hacia un
segundo rótulo SERVIDOR a la derecha.](images/cap18-resumiendo-urls-views.png)

## Anatomía de `path()`

```python
path('cuentas/<str:numero>/', views.detalle_cuenta, name='detalle_cuenta')
```

Cuatro cosas:

- **La ruta**: `'cuentas/<str:numero>/'`. El fragmento entre `<` y `>` es una
  **captura**: cualquier valor que aparezca ahí se pasa como parámetro a la
  vista.
- **La vista**: `views.detalle_cuenta`. La función que se ejecuta.
- **Name**: un nombre único para esta ruta. Sirve para generar URLs desde el
  código sin hardcodearlas.
- **/**: La ruta termina con `/`. Es la convención de Django: todas las URLs
  terminan con barra.

### Nota, ¿Qué es harcodear?

Del inglés *hard-coded*, literalmente "escrito duro en el código". Significa
poner un valor fijo directamente en el código fuente, en lugar de calcularlo,
leerlo de una configuración, o generarlo dinámicamente.

**El problema:** si mañana cambiás la ruta en urls.py de /cuentas/<numero>/ a
/mis-cuentas/<numero>/, tenés que buscar y modificar a mano cada lugar donde
escribiste esa URL. En un proyecto grande pueden ser cientos de archivos.

La alternativa (no hardcodear)

**Regla mental:** cada vez que copiás un valor fijo en tu código (URLs,
credenciales, rutas de archivos, textos que se repiten), preguntate: "¿qué
pasa si mañana esto cambia?". Si la respuesta es "tengo que buscar y
reemplazar en 20 lugares", estás hardcodeando cuando no deberías.

| Cuando sí | Cuando no |
|---|---|
| Valores que son estructurales y no van a cambiar (por ejemplo, la constante `math.pi`, o el número 100 en porcentaje / 100). Cuando cambiar el valor no rompería nada. | URLs, contraseñas, claves de API, rutas de servidores, nombres de bases de datos, direcciones de email. Todo eso va a cambiar entre desarrollo y producción, o con el tiempo. Se leen de configuración o de variables de entorno. |

## Tipos de captura de la RUTA

Django trae **convertidores** que validan el formato del parámetro:

| Convertidor | Acepta | Ejemplo |
|---|---|---|
| **str** | Cualquier string sin barras | `<str:numero>` |
| **int** | Entero positivo | `<int:id>` |
| **slug** | Letras, números, guiones y underscores | `<slug:categoria>` |
| **uuid** | UUID válido | `<uuid:token>` |
| **path** | Cualquier cosa, incluidas barras | `<path:archivo>` |

Si el URL no matchea el tipo, Django ni siquiera llama a la vista: prueba con
la siguiente ruta.

```python
path('cuentas/<int:id>/', views.detalle_cuenta_por_id)
path('cuentas/<str:numero>/', views.detalle_cuenta_por_numero)
```

Con esta configuración:

- `/cuentas/42/` ➡ `detalle_cuenta_por_id(request, id=42)`
- `/cuentas/001-100/` ➡ `detalle_cuenta_por_numero(request, numero='001-100')`

Django elige la primera ruta que matchea. **El ORDEN IMPORTA.**

## Organizando con `include`

En un proyecto real, dejar todas las URLs en banco_utn/urls.py se vuelve
incontrolable. La convención es que **cada app tenga su propio urls.py**, y el
proyecto los **incluya**:

**`banco_utn/urls.py`** (URLs del proyecto)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('banco.urls')),     # incluye las URLs de la app banco
]
```

**`banco/urls.py`** (URLs de la app, hay que crear el archivo):

```python
from django.urls import path
from banco import views

app_name = 'banco'      # namespace para las URLs de esta app

urlpatterns = [
    path('', views.home, name='home'),
    path('cuentas/', views.listar_cuentas, name='listar_cuentas'),
    path('cuentas/<str:numero>/', views.detalle_cuenta, name='detalle_cuenta'),
]
```

Con `app_name = 'banco'`, todas las URLs de esta app quedan bajo el namespace
`banco:`. Para referirte a la vista home desde código o templates, usás
`'banco:home'`. Esto evita colisiones si mañana agregás otra app con una vista
también llamada home.

### Nota: Namespace (o *espacio de nombres*)

Un **contenedor de nombres** que agrupa identificadores para evitar que dos
cosas con el mismo nombre se confundan entre sí. Es como el apellido de una
persona: en un grupo puede haber varias "Ana", pero "Ana Pérez" y "Ana López"
quedan claramente distinguidas.

En Django, cada app puede definir su propio namespace de URLs con
`app_name = 'banco'`. Después, para referirse a una URL de esa app se usa la
sintaxis `namespace:nombre` - por ejemplo `'banco:home'`. Así, si mañana otra
app también define una vista llamada home, no hay conflicto: son `'banco:home'`
y `'otra_app:home'`, dos identificadores distintos.

## Vistas: la lógica detrás de cada URL

Una **vista** de Django, en su forma más simple, es una función que:

1. Recibe un objeto `HttpRequest` como primer parámetro.
2. Devuelve un objeto `HttpResponse` (o alguna de sus subclases).

```python
from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>Bienvenido al banco</h1>")
```

Eso es todo. Todo lo demás (consultar modelos, procesar datos, renderizar HTML,
redirigir a otra URL) pasa entre esas dos líneas.

### El objeto request

Cuando Django llama a la vista, le pasa un objeto que representa el pedido
HTTP. Atributos útiles:

```python
def mi_vista(request):
    request.method         # 'GET', 'POST', 'PUT', 'DELETE'
    request.GET            # parámetros de la query string (?nombre=Ana)
    request.POST           # datos del formulario enviado con POST
    request.path           # '/cuentas/001-100/'
    request.user           # el usuario logueado (o AnonymousUser)
    request.META           # info del servidor y del navegador
    request.session        # variables de sesión del usuario
    request.headers        # encabezados HTTP
```

Casi todas las vistas usan al menos `request.method` (para distinguir GET de
POST) y `request.user` (para saber quién está pidiendo).

### Tipos de `HttpResponse`

Django trae varias respuestas específicas:

```python
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseRedirect, JsonResponse

# Respuesta con HTML
return HttpResponse("<h1>Hola</h1>")

# Con código de estado personalizado
return HttpResponse("Error", status=500)

# 404 explícito
return HttpResponseNotFound("No existe")

# Redirección a otra URL
return HttpResponseRedirect('/cuentas/')

# JSON (útil para APIs)
return JsonResponse({'saldo': 5000})
```

Los atajos más usados:

```python
from django.shortcuts import render, redirect, get_object_or_404

# Renderizar un template (lo vemos en el capítulo 20)
return render(request, 'banco/home.html', {'cuentas': cuentas})

# Redireccionar por nombre de URL
return redirect('banco:home')

# Buscar un objeto o 404 automático
cuenta = get_object_or_404(Cuenta, numero='001-100')
```

Estos atajos hacen el 90% del trabajo. Vamos a ver los tres en detalle.

## Primera vista con lógica real

Nuestro home actual solo muestra un texto pelado. Hagámoslo interesante: que
muestre estadísticas del banco.

**`banco/views.py`**

```python
from django.http import HttpResponse
from banco.models import PersonaFisica, PersonaJuridica, Cuenta


def home(request):
    total_personas = PersonaFisica.objects.count() + PersonaJuridica.objects.count()
    total_cuentas = Cuenta.objects.filter(activa=True).count()
    saldo_total = sum(c.saldo for c in Cuenta.objects.filter(activa=True))

    html = f"""
    <h1>Banco UTN</h1>
    <p><strong>Clientes:</strong> {total_personas}</p>
    <p><strong>Cuentas activas:</strong> {total_cuentas}</p>
    <p><strong>Saldo total:</strong> ${saldo_total:,.2f}</p>
    """

    return HttpResponse(html)
```

Cuando entrás a /, la vista consulta la base y devuelve HTML con las
estadísticas actuales. Cambiá cualquier cosa desde el admin, refrescá la
página, y los números se actualizan.

**Notá algo importante:** estamos generando HTML como string en Python. **Esto
no se hace en un proyecto real** es feo, propenso a errores y mezcla lógica con
presentación. En el próximo capítulo (Templates) vamos a separar el HTML del
código Python. Por ahora es un puente pedagógico: queremos ver primero cómo
funciona la vista, después le agregamos el HTML lindo.

## Parámetros de URL

Ahora una vista que reciba un parámetro. Queremos ver el detalle de una cuenta
por su número:

**`banco/urls.py`**:

```python
urlpatterns = [
    path('', views.home, name='home'),
    path('cuentas/<str:numero>/', views.detalle_cuenta, name='detalle_cuenta'),
]
```

**`banco/views.py`**

```python
from django.http import HttpResponse, HttpResponseNotFound
from banco.models import Cuenta


def detalle_cuenta(request, numero):
    try:
        cuenta = Cuenta.objects.get(numero=numero)
    except Cuenta.DoesNotExist:
        return HttpResponseNotFound(f"<h1>Cuenta {numero} no existe</h1>")

    html = f"""
    <h1>Cuenta {cuenta.numero}</h1>
    <p><strong>Titular:</strong> {cuenta.titular}</p>
    <p><strong>Saldo:</strong> ${cuenta.saldo:,.2f}</p>
    <p><strong>Estado:</strong> {'Activa' if cuenta.activa else 'Cerrada'}</p>
    <a href="/cuentas/">⬅ Volver</a>
    """
    return HttpResponse(html)
```

Notá dos cosas:

- **El parámetro `numero`** llega desde la URL y aparece en la firma de la
  vista. El nombre tiene que coincidir entre `<str:numero>` en la URL y
  `numero` en la vista.
- **`Cuenta.DoesNotExist`** es una excepción que Django genera cuando `.get()`
  no encuentra nada. Es el equivalente a nuestras `CuentaNoEncontrada` del
  capítulo 15, pero viene incluido en Django.

## `get_object_or_404`: el atajo idiomático

El patrón "buscar objeto, si no existe devolver 404" es tan común que Django
tiene un atajo:

```python
from django.shortcuts import get_object_or_404
from banco.models import Cuenta


def detalle_cuenta(request, numero):
    cuenta = get_object_or_404(Cuenta, numero=numero)
    # si no existe, Django ya devolvió un 404
    html = f"""
    <h1>Cuenta {cuenta.numero}</h1>
    <p><strong>Titular:</strong> {cuenta.titular}</p>
    <p><strong>Saldo:</strong> ${cuenta.saldo:,.2f}</p>
    """
    return HttpResponse(html)
```

Reemplaza el try/except por una línea. Si la cuenta no existe, Django devuelve
automáticamente una página 404 (en desarrollo, la típica de "página no
encontrada", en producción la que hayas configurado).

Usá `get_object_or_404` siempre que quieras "traer un objeto o dar 404". Es el
idiom estándar.

## Listado con filtros y ordenamiento

Una vista un poco más real: listar todas las cuentas activas, ordenadas por
saldo descendente.

**`banco/views.py`**

```python
def listar_cuentas(request):
    cuentas = Cuenta.objects.filter(activa=True).order_by('-saldo')

    filas = ""
    for c in cuentas:
        filas += f"""
        <tr>
            <td>{c.numero}</td>
            <td>{c.titular}</td>
            <td>${c.saldo:,.2f}</td>
            <td><a href="/cuentas/{c.numero}/">Ver</a></td>
        </tr>
        """

    html = f"""
    <h1>Cuentas activas del banco</h1>
    <table border="1" cellpadding="5">
        <tr><th>Número</th><th>Titular</th><th>Saldo</th><th></th></tr>
        {filas}
    </table>
    <p><a href="/">⬅ Volver</a></p>
    """
    return HttpResponse(html)
```

Ya duele leer ese código. La mezcla de HTML y Python es prácticamente
ilegible. Confirmemos algo antes de seguir: **este código es un ejemplo
pedagógico, no producción**. En el próximo capítulo esto se convierte en:

```python
def listar_cuentas(request):
    cuentas = Cuenta.objects.filter(activa=True).order_by('-saldo')
    return render(request, 'banco/listar_cuentas.html', {'cuentas': cuentas})
```

Y todo el HTML vive en un archivo aparte.

## Query strings: parámetros opcionales

A veces querés parámetros que **no van en la URL** sino como *query string*, la
parte después del ?. Ejemplo:

```text
/cuentas/?tipo=ahorro&activa=1
```

Estos parámetros llegan en `request.GET` como diccionario:

```python
def listar_cuentas(request):
    cuentas = Cuenta.objects.all()

    tipo = request.GET.get('tipo')
    if tipo == 'ahorro':
        cuentas = CuentaAhorro.objects.all()
    elif tipo == 'corriente':
        cuentas = CuentaCorriente.objects.all()

    solo_activas = request.GET.get('activa') == '1'
    if solo_activas:
        cuentas = cuentas.filter(activa=True)

    # ... generar HTML ...
```

`request.GET.get('tipo')` devuelve el valor del parámetro `tipo` o `None` si no
está. Nunca da error por parámetros faltantes, es seguro.

Query strings son para **filtros opcionales**. Parámetros de URL
(`<str:numero>`) son para **identificadores obligatorios**. La distinción es
importante:

| URL | Uso |
|---|---|
| **/cuentas/001-100/** | El ID es parte del recurso - captura de URL |
| **/cuentas/?tipo=ahorro** | Filtro opcional sobre un listado - query string |
| **/buscar/?q=perez** | Búsqueda con término libre - query string |

## Redirecciones

Muchas veces, después de procesar algo, querés mandar al usuario a otra
página. Se hace con `redirect`:

```python
from django.shortcuts import redirect


def cerrar_cuenta(request, numero):
    cuenta = get_object_or_404(Cuenta, numero=numero)
    cuenta.cerrar()
    return redirect('banco:listar_cuentas')
```

`redirect` puede recibir:

- **El nombre de una URL**: `redirect('banco:home')`.
- **Una URL absoluta**: `redirect('/cuentas/')`.
- **Un objeto con `get_absolute_url()`**: `redirect(cuenta)`, si el modelo
  tiene ese método.

El navegador recibe una respuesta 302 (redirección temporal) y automáticamente
pide la nueva URL.

## `get_absolute_url` en el modelo

Un idiom útil: en cada modelo, definir un método `get_absolute_url` que
devuelva su URL canónica.

**`banco/models.py`**

```python
from django.urls import reverse


class Cuenta(models.Model):
    # ... campos ...

    def get_absolute_url(self):
        return reverse('banco:detalle_cuenta', kwargs={'numero': self.numero})
```

`reverse` es el opuesto de `path`: recibe el **nombre** de una URL y devuelve
la URL construida. Con `kwargs` pasás los parámetros de captura.

Con esto podés hacer `redirect(cuenta)` y Django ya sabe adónde ir. El admin
también lo usa: el botón "Ver en el sitio" aparece automáticamente si tus
modelos tienen `get_absolute_url`.

## Manejando POST: acciones que modifican datos

Hasta ahora todas las vistas responden a GET: consultan datos y muestran algo.
Pero cuando querés que el usuario **haga algo** (transferir dinero, cambiar su
email), la operación viene por POST.

Ejemplo minimalista: una vista que reciba `numero` y `monto`, y haga un
depósito.

**`banco/views.py`**

```python
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from banco.models import Cuenta


def depositar_en_cuenta(request, numero):
    cuenta = get_object_or_404(Cuenta, numero=numero)

    if request.method == 'POST':
        monto = float(request.POST.get('monto', 0))
        try:
            cuenta.depositar(monto, descripcion="Depósito web")
            messages.success(request, f"Depósito de ${monto:,.2f} realizado")
        except Exception as e:
            messages.error(request, f"Error: {e}")

        return redirect('banco:detalle_cuenta', numero=numero)

    # Si es GET, mostramos el formulario
    html = f"""
    <h1>Depositar en {cuenta.numero}</h1>
    <form method="post">
        <input type="hidden" name="csrfmiddlewaretoken" value="TODO">
        <input type="number" name="monto" step="0.01" required>
        <button type="submit">Depositar</button>
    </form>
    """
    return HttpResponse(html)
```

Puntos importantes:

- **La misma vista maneja GET y POST.** Con GET, muestra el formulario, con
  POST, procesa los datos.
- **Después de un POST exitoso, redirigimos** con `redirect`. Es un patrón
  fundamental que evita que el usuario "recargue" y duplique la operación.
- **`messages.success` / `messages.error`** guardan un mensaje que la próxima
  vista puede mostrar. Es la forma idiomática de dar feedback tras una acción.
- **`csrfmiddlewaretoken`**: Django protege contra ataques CSRF (*Cross-Site
  Request Forgery*) exigiendo un token en todos los POST. En un template real
  Django genera el token automáticamente con `{% csrf_token %}`. En este
  ejemplo minimalista dejé un placeholder, el formulario no va a funcionar
  hasta que arreglemos esto, tema del próximo capítulo.

## El patrón "`Post-Redirect-Get`"

El idiom que aplicamos arriba tiene nombre: **Post-Redirect-Get (PRG)**.
Después de procesar un POST, siempre redirigís (a la misma vista con GET o a
otra). Beneficios:

- Si el usuario recarga la página, no se duplica la operación.
- La URL en la barra queda "limpia" (sin la marca de haber hecho POST).
- Los mensajes de éxito/error se muestran en la nueva página, no en la
  respuesta al POST.

**Nunca respondas a un POST con HTML directamente** (salvo casos muy
específicos). Siempre `redirect` al final.

## Vistas basadas en clases: mención breve

Django ofrece dos formas de escribir vistas:

- **Function-Based Views (FBV)**: las que hicimos hasta acá. Funciones que
  reciben `request` y devuelven `HttpResponse`.
- **Class-Based Views (CBV)**: clases que heredan de `View` y definen métodos
  como `get()` y `post()`.

Ejemplo equivalente en **CBV**:

```python
from django.views import View
from django.http import HttpResponse


class HomeView(View):
    def get(self, request):
        return HttpResponse("<h1>Bienvenido al banco</h1>")
```

**`urls.py`**:

```python
path('', HomeView.as_view(), name='home')
```

Django trae **vistas genéricas** que resuelven casos comunes con muy poco
código:

```python
from django.views.generic import ListView, DetailView


class ListaCuentasView(ListView):
    model = Cuenta
    template_name = 'banco/listar_cuentas.html'


class DetalleCuentaView(DetailView):
    model = Cuenta
    template_name = 'banco/detalle_cuenta.html'
```

Con estas dos clases, Django genera automáticamente vistas de listado y
detalle. **Muy poderoso, muy corto**, cuando la vista hace exactamente lo que
la genérica ofrece.

## ¿Por qué usamos FBV en el manual?

Dos motivos:

- **Legibilidad para principiantes.** Una función es un concepto que ya
  dominan. Una CBV requiere entender la herencia de vistas genéricas, los
  mixins, los métodos que se sobrescriben. Es una capa extra que oscurece qué
  está pasando.
- **Flexibilidad.** Cuando la vista hace algo específico (validaciones
  cruzadas, procesamiento complejo, condicionales que dependen de varios
  modelos), una FBV es más directa.

En proyectos reales se mezclan: **FBV para vistas particulares, CBV genéricas
para casos estándar** (listar todos los usuarios, ver detalle de un producto).
En este manual usamos **solo FBV** para no sobrecargar. Cuando aprendan Django
avanzado, van a poder incorporar CBV donde tenga sentido.

## URLs del banco: el mapa completo

Con lo visto, así queda el mapa de URLs de nuestro proyecto. En el próximo
capítulo cada vista va a tener su template por ahora, es la estructura:

**`banco/urls.py`**

```python
from django.urls import path
from banco import views

app_name = 'banco'

urlpatterns = [
    path('', views.home, name='home'),

    # Listados
    path('cuentas/', views.listar_cuentas, name='listar_cuentas'),
    path('personas/', views.listar_personas, name='listar_personas'),

    # Detalles
    path('cuentas/<str:numero>/', views.detalle_cuenta, name='detalle_cuenta'),
    path('personas/<int:persona_id>/', views.detalle_persona, name='detalle_persona'),

    # Operaciones (POST)
    path('cuentas/<str:numero>/depositar/', views.depositar_en_cuenta, name='depositar'),
    path('cuentas/<str:numero>/extraer/', views.extraer_de_cuenta, name='extraer'),
    path('cuentas/<str:numero>/transferir/', views.transferir_desde_cuenta, name='transferir'),
]
```

**`banco/views.py`** (versión que vamos a expandir con templates):

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages

from banco.models import (
    PersonaFisica,
    PersonaJuridica,
    Cuenta,
    Movimiento,
)


def home(request):
    total_personas = PersonaFisica.objects.count() + PersonaJuridica.objects.count()
    total_cuentas = Cuenta.objects.filter(activa=True).count()

    contexto = {
        'total_personas': total_personas,
        'total_cuentas': total_cuentas,
    }
    return HttpResponse(f"<h1>Banco UTN - {total_personas} clientes, {total_cuentas} cuentas</h1>")


def listar_cuentas(request):
    cuentas = Cuenta.objects.filter(activa=True).order_by('-saldo')
    lineas = [f"<li>{c.numero} - {c.titular} - ${c.saldo:,.2f}</li>" for c in cuentas]
    html = f"<h1>Cuentas activas</h1><ul>{''.join(lineas)}</ul>"
    return HttpResponse(html)


def listar_personas(request):
    fisicas = PersonaFisica.objects.all()
    juridicas = PersonaJuridica.objects.all()

    lineas_fisicas = [f"<li>{p.apellido}, {p.nombre} (DNI {p.dni})</li>" for p in fisicas]
    lineas_juridicas = [f"<li>{p.nombre} (CUIT {p.cuit})</li>" for p in juridicas]

    html = f"""
    <h1>Clientes</h1>
    <h2>Personas Físicas</h2>
    <ul>{''.join(lineas_fisicas)}</ul>
    <h2>Personas Jurídicas</h2>
    <ul>{''.join(lineas_juridicas)}</ul>
    """
    return HttpResponse(html)


def detalle_cuenta(request, numero):
    cuenta = get_object_or_404(Cuenta, numero=numero)
    movimientos = cuenta.movimientos.order_by('-fecha')[:10]

    lineas_mov = [
        f"<li>{m.fecha:%d/%m/%Y %H:%M} - {m.tipo} - ${m.monto:,.2f}</li>"
        for m in movimientos
    ]
    html = f"""
    <h1>Cuenta {cuenta.numero}</h1>
    <p>Titular: {cuenta.titular}</p>
    <p>Saldo: ${cuenta.saldo:,.2f}</p>
    <p>CBU: {cuenta.cbu}</p>
    <h2>Últimos movimientos</h2>
    <ul>{''.join(lineas_mov) or '<li>Sin movimientos</li>'}</ul>
    """
    return HttpResponse(html)


def detalle_persona(request, persona_id):
    persona = get_object_or_404(PersonaFisica, id=persona_id)
    cuentas = persona.cuentas.all()

    lineas_cuentas = [
        f"<li><a href='/cuentas/{c.numero}/'>{c.numero}</a> - ${c.saldo:,.2f}</li>"
        for c in cuentas
    ]
    html = f"""
    <h1>{persona.nombre_completo()}</h1>
    <p>DNI: {persona.dni}</p>
    <h2>Cuentas</h2>
    <ul>{''.join(lineas_cuentas) or '<li>Sin cuentas</li>'}</ul>
    """
    return HttpResponse(html)


def depositar_en_cuenta(request, numero):
    cuenta = get_object_or_404(Cuenta, numero=numero)

    if request.method == 'POST':
        monto = float(request.POST.get('monto', 0))
        try:
            cuenta.depositar(monto, descripcion="Depósito web")
            messages.success(request, f"Depósito realizado: ${monto:,.2f}")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect('banco:detalle_cuenta', numero=numero)

    # GET: mostrar formulario (versión provisoria hasta el capítulo de templates)
    return HttpResponse(f"""
    <h1>Depositar en {numero}</h1>
    <form method="post">
        Monto: <input type="number" name="monto" step="0.01" required>
        <button type="submit">Depositar</button>
    </form>
    """)


def extraer_de_cuenta(request, numero):
    cuenta = get_object_or_404(Cuenta, numero=numero)

    if request.method == 'POST':
        monto = float(request.POST.get('monto', 0))
        try:
            cuenta.extraer(monto, descripcion="Extracción web")
            messages.success(request, f"Extracción realizada: ${monto:,.2f}")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect('banco:detalle_cuenta', numero=numero)

    return HttpResponse(f"""
    <h1>Extraer de {numero}</h1>
    <form method="post">
        Monto: <input type="number" name="monto" step="0.01" required>
        <button type="submit">Extraer</button>
    </form>
    """)


def transferir_desde_cuenta(request, numero):
    origen = get_object_or_404(Cuenta, numero=numero)

    if request.method == 'POST':
        numero_destino = request.POST.get('destino')
        monto = float(request.POST.get('monto', 0))

        try:
            destino = Cuenta.objects.get(numero=numero_destino)
            origen.extraer(monto, descripcion=f"Transferencia a {numero_destino}")
            destino.depositar(monto, descripcion=f"Transferencia de {numero}")
            messages.success(request, f"Transferencia de ${monto:,.2f} realizada")
        except Cuenta.DoesNotExist:
            messages.error(request, f"La cuenta {numero_destino} no existe")
        except Exception as e:
            messages.error(request, f"Error: {e}")

        return redirect('banco:detalle_cuenta', numero=numero)

    return HttpResponse(f"""
    <h1>Transferir desde {numero}</h1>
    <form method="post">
        Cuenta destino: <input type="text" name="destino" required><br>
        Monto: <input type="number" name="monto" step="0.01" required>
        <button type="submit">Transferir</button>
    </form>
    """)
```

Es feo, pero funcional. Todas las vistas del banco están hechas: listar, ver
detalle, hacer operaciones. Con el navegador podés recorrer todo el sistema.

## Falta un detalle importante

Estos formularios **no van a funcionar todavía** porque falta el
`{% csrf_token %}` de Django. En vistas hechas con HTML manual como estas, no
hay una forma limpia de agregarlo. En el próximo capítulo, cuando usemos
templates y `render`, el CSRF se resuelve con una línea. Por ahora, si querés
probar los formularios, podés agregar `@csrf_exempt` como decorador sobre las
vistas de depósito/extracción/transferencia, **solo para experimentar y solo en
desarrollo. Nunca en producción**.

```python
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def depositar_en_cuenta(request, numero):
    ...
```

En el próximo capítulo esto queda resuelto de forma limpia y segura.

## Ejercicio: navegar el sistema

Con el servidor corriendo, andá a http://127.0.0.1:8000/ y hacé el recorrido:

1. `/` ➡ home con estadísticas.
2. `/cuentas/` ➡ listado.
3. `/cuentas/001-100/` ➡ detalle de una cuenta específica.
4. `/personas/` ➡ listado de clientes.

Es un sitio web feo pero completo, generado con menos de 100 líneas de código
útiles. Todo el trabajo de modelado del capítulo 15 y del capítulo 17 sostiene
esto.

En el próximo capítulo esas vistas van a devolver HTML profesional, con
Bootstrap, con navegación, con menús. Esperá un poco más, y prometo que el
dolor de leer HTML en strings termina.

## Anticipando el próximo capítulo

En **Templates**, vamos a separar el HTML del código Python usando el **Django
Template Language** (DTL). Las vistas van a quedar limpias, dedicadas solo a la
lógica. El HTML va a vivir en archivos .html propios, con marcadores especiales
para insertar datos.

Además:

- Vamos a definir un **layout base** con Bootstrap 5, del que todas las páginas
  heredan.
- Vamos a resolver el problema del CSRF de forma limpia con `{% csrf_token %}`.
- Vamos a agregar navegación consistente, mensajes de éxito/error visuales, y
  un diseño mínimamente decente.

Cuando termines el próximo capítulo, el banco va a tener aspecto de banco, no
de página en construcción de 1995.
