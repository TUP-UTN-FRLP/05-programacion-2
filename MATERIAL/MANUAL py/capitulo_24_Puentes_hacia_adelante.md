# Capítulo 24. Puentes hacia adelante

*Adónde seguir después de este manual.*

## ¿Por qué leemos este capítulo?

Llegaste al final del manual. Repasemos rápido lo que construiste:

- **Python de cero a nivel profesional**: sintaxis, tipos, colecciones,
  funciones, comprensiones, manejo de errores.
- **Programación orientada a objetos completa**: encapsulamiento, herencia,
  polimorfismo, composición, SOLID.
- **Estructura de proyectos**: módulos, imports, organización profesional en
  archivos.
- **Biblioteca estándar de Python**: math, random, datetime, pathlib, csv,
  json, re, collections.
- **Django completo**: modelos, admin, URLs, vistas, templates, formularios,
  autenticación, testing.
- **Producción**: PostgreSQL, configuración por entornos, deploy.

Con eso, ya son desarrolladores Python capaces de construir aplicaciones web
reales. No lo digo con generosidad - lo digo con seriedad. El conjunto de
habilidades que tienen ahora es el que muchas empresas piden para sus
posiciones de Python Backend Junior o SSR.

Pero el ecosistema de Python es enorme, y hay muchos caminos posibles hacia
adelante. Este último capítulo es un **mapa de rutas**: qué existe más allá del
manual, cuándo tiene sentido explorarlo, y qué se conecta con qué.

No es un tutorial. No hay código extenso, no hay ejercicios. Es una guía para
saber **hacia dónde ir** cuando el próximo problema aparezca.

## APIs REST con Django REST Framework

Todo el manual trabajamos con Django clásico: vistas que devuelven HTML,
templates, formularios que el navegador procesa. Es lo que se usa para
**aplicaciones web tradicionales**.

Pero hay otro mundo: el de las **APIs REST**. Una API REST es un servidor que,
en vez de devolver HTML, devuelve datos crudos (usualmente JSON). Un cliente -
que puede ser una app móvil, un frontend React, otro servidor - consume esos
datos y los muestra a su manera.

Ejemplo: el banco actual devuelve una página HTML con los movimientos. Como
API REST, devolvería algo como:

```json
{
  "cuenta": "001-100",
  "saldo": 65000.00,
  "movimientos": [
    {"tipo": "deposito", "monto": 15000, "fecha": "2026-07-26T15:45:00"},
    {"tipo": "apertura", "monto": 50000, "fecha": "2026-07-26T15:42:00"}
  ]
}
```

Y una app móvil (Android/iOS) o un frontend React consumirían ese JSON.

**Django REST Framework** (DRF) es la biblioteca estándar para exponer APIs
REST desde Django. Sus conceptos clave:

- **Serializers**: convierten objetos del modelo a JSON y viceversa. Son el
  equivalente de los Form que ya conocen.
- **ViewSets**: vistas especializadas que exponen automáticamente los
  endpoints CRUD (GET, POST, PUT, DELETE).
- **Routers**: generan URLs automáticamente a partir de los ViewSets.
- **Authentication**: soporte para tokens, JWT, OAuth.
- **Permissions**: sistema de permisos análogo al @login_required.

Con DRF, exponer el banco como API REST toma pocas líneas por modelo. Es una
de las bibliotecas más maduras del ecosistema Python.

### Cuando aprenderlo:

- Si van a trabajar con **frontend separado** (React, Vue, Angular).
- Si van a construir **apps móviles** que necesitan un backend.
- Si van a **integrar** un sistema con otros (dos empresas que comparten
  datos).
- Si les piden "una API" en un proyecto.

**Recurso recomendado:** la documentación oficial
(https://www.django-rest-framework.org/) es excelente, con tutorial paso a
paso. En español, el libro *Django for APIs* de William Vincent es una buena
introducción.

## Async views y programación asíncrona

Django, desde la versión 4.x, soporta **vistas asíncronas**. La sintaxis es
familiar si conocen async/await de JavaScript:

```python
async def mi_vista(request):
    datos = await consultar_api_externa()
    return HttpResponse(f"Datos: {datos}")
```

**¿Para qué sirve?** Para operaciones I/O-bound: cuando la vista está esperando
algo externo (una consulta HTTP a otra API, una operación de disco lenta, un
mensaje de otra máquina). Sin async, mientras una vista espera, el proceso está
bloqueado. Con async, puede atender otras requests durante la espera.

Para aplicaciones CRUD normales (consultar la base de datos y devolver HTML),
async **no aporta**. La base de datos es rápida, no vale la pena la
complejidad extra.

### Cuando interesa aprender:

- APIs que consumen múltiples servicios externos en paralelo.
- Sistemas de alto tráfico donde optimizar cada milisegundo importa.
- Aplicaciones en tiempo real (chats, notificaciones push, dashboards que se
  actualizan solos).

**Precaución:** async cambia mucho el estilo del código. No todo se traduce
naturalmente. Antes de meterse en async, hay que dominar sync primero - cosa
que ya hicieron.

**Recurso recomendado:** la documentación oficial de Django sobre async views
(https://docs.djangoproject.com/en/stable/topics/async/).

## Channels y WebSockets: tiempo real

HTTP tradicional es pedido ➡ respuesta ➡ chau. Una vez que el servidor
respondió, la conexión se cierra. Para actualizar la pantalla con datos nuevos,
el navegador tiene que volver a pedir.

Para aplicaciones donde el servidor necesita **empujar** información al cliente
(chat en vivo, notificaciones instantáneas, dashboards con métricas), esto no
alcanza. Ahí entran los **WebSockets**: una conexión persistente entre servidor
y cliente, bidireccional.

**Django Channels** es la biblioteca que agrega soporte de WebSockets (y otros
protocolos asíncronos) a Django. Le suma al ORM y las vistas un sistema de
"consumers" que manejan conexiones persistentes.

Casos de uso típicos:

- **Chat**: los usuarios mandan mensajes y aparecen al instante en todos los
  conectados.
- **Notificaciones push**: cuando algo pasa en el servidor (una transferencia
  recibida), aparece un pop-up sin recargar.
- **Colaboración en tiempo real**: como Google Docs, varios usuarios editando
  un documento a la vez.
- **Dashboards**: gráficos que se actualizan solos con datos nuevos del
  servidor.

**Cuando aprenderlo:** cuando el proyecto necesite alguno de esos casos
específicos. Antes, no. Es una tecnología potente pero compleja, y agregar
Channels a un proyecto que no lo necesita es sobredimensionar.

## Celery: tareas en background

Algunas operaciones toman tiempo: enviar un email, procesar un archivo grande,
generar un reporte pesado, comunicarse con una API externa lenta. Si estas
operaciones bloquean la vista, el usuario espera 20 segundos frente a un
navegador con la ruedita girando.

La solución profesional: **ejecutar esas tareas en background**, en un proceso
separado. La vista termina rápido, le dice al usuario "estamos procesando tu
pedido", y en paralelo un worker hace el trabajo. Cuando termina, notifica al
usuario.

**Celery** es la biblioteca estándar para esto en Python. Su modelo:

- Un **mensaje broker** (usualmente Redis o RabbitMQ) hace de cola.
- **Workers** (procesos aparte) consumen la cola y ejecutan las tareas.
- **Django** encola tareas escribiendo mi_tarea.delay(...).

Ejemplo típico:

```python
from celery import shared_task


@shared_task
def enviar_resumen_mensual(usuario_id):
    """Genera y envía el resumen del mes por email. Puede tardar minutos."""
    ...


# En una vista:
def solicitar_resumen(request):
    enviar_resumen_mensual.delay(request.user.id)
    messages.info(request, "Te llegará por email en unos minutos")
    return redirect('banco:home')
```

.delay() no espera: encola la tarea y devuelve el control inmediatamente.

### Cuando interesa:

- Envíos masivos de emails.
- Procesamiento de imágenes o videos.
- Reportes complejos.
- Integraciones con servicios externos lentos.
- Tareas programadas (correr todos los días a las 3 AM).

**Alternativas modernas más simples**: si el proyecto es chico, Celery es
sobredimensionado. django-q2, dramatiq, o incluso django-background-tasks son
opciones más livianas.

## Deploy: llevar el sistema al mundo

En el capítulo anterior mencionamos deploy. Profundizamos ahora.

Deploy es el proceso de poner tu sistema en un servidor accesible desde
internet. Los componentes:

### Servidor de aplicación

- **Gunicorn**: el más usado con Django. Configuración simple, robusto,
  gratis.
- **uWSGI**: alternativa clásica, más features pero más complejo.
- **Daphne**: para Django con Channels/WebSockets.

### Servidor web / proxy inverso

Adelante del servidor de aplicación:

- **Nginx**: el estándar. Sirve archivos estáticos, hace de proxy, maneja
  HTTPS.
- **Apache**: alternativa histórica, todavía muy usada.
- **Caddy**: nuevo, se configura mucho más simple que Nginx, HTTPS automático.

### Base de datos

- **PostgreSQL**: recomendación para casi cualquier caso.
- **MySQL/MariaDB**: alternativa, muy usado especialmente en hosting
  compartido.

### Contenedores: Docker

**Docker** es una tecnología para empaquetar aplicaciones junto con todas sus
dependencias en "contenedores". Ventajas:

- Tu aplicación corre igual en cualquier lado (tu máquina, staging,
  producción).
- Simplifica el deploy dramáticamente.
- Facilita orquestar múltiples servicios (Django + PostgreSQL + Redis +
  Nginx).

Es la práctica estándar en la industria. Aprender Docker es una de las
inversiones más rentables para cualquier desarrollador Python.

**Docker Compose** permite definir múltiples contenedores en un solo archivo
YAML - por ejemplo, un docker-compose.yml que levanta Django, PostgreSQL y
Nginx juntos.

### Servicios de deploy

Como mencionamos en el capítulo anterior, hay plataformas que abstraen mucho
del deploy:

- **Railway**, **Render**, **Fly.io**: modernos, fáciles, con tiers gratuitos.
- **DigitalOcean App Platform**: sencillo, con opciones de crecimiento.
- **Heroku**: histórico, ya pago, pero muy documentado.
- **AWS Elastic Beanstalk**, **Google App Engine**: los gigantes, más
  complejos.

Para el primer deploy real, **Railway o Render** son ideales. En 30 minutos,
con Git y unos pocos comandos, el banco puede quedar accesible por internet.

**Recurso recomendado:** para Docker en general, la serie de tutoriales de
TestDriven.io es excelente. Para deploy con Django específicamente, Adam
Johnson (django-htmx, django-linear-migrations) tiene libros y artículos muy
prácticos.

## Signals: el gancho invisible

Django tiene un sistema de **signals**: eventos que se disparan cuando pasan
cosas, y a los que otras partes del sistema pueden "engancharse".

Ejemplo típico:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from banco.models import PersonaFisica


@receiver(post_save, sender=PersonaFisica)
def enviar_bienvenida(sender, instance, created, **kwargs):
    if created:
        # se ejecuta automáticamente cuando se crea una PersonaFisica
        enviar_email(instance.usuario.email, "Bienvenido al banco")
```

### Ventajas:

- Desacopla componentes. La creación de personas no sabe nada de emails, el
  signal los conecta.
- Permite agregar comportamiento sin modificar el modelo.

### Desventajas:

- **Poco explícito.** Es fácil olvidarse de que existe un signal,
  especialmente en proyectos grandes. "¿Por qué se está mandando este email?" -
  buscando en los models no hay nada, hay que buscar en signals.py.
- Puede generar bugs difíciles de rastrear.

**Regla mental:** usar signals cuando el desacople es real (código que
verdaderamente no debería vivir en el modelo). Para lógica que pertenece al
modelo, poner el código directamente ahí (con save() sobrescrito, por
ejemplo). Signals no es siempre la mejor solución solo por ser "más limpio".

## Class-Based Views avanzadas

En el manual usamos **Function-Based Views (FBV)** para todo. En proyectos
reales, muchos equipos prefieren **Class-Based Views (CBV)** para casos
estándar.

Django trae vistas genéricas listas para usar:

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView


class CuentaListView(ListView):
    model = Cuenta
    template_name = 'banco/cuentas.html'
    context_object_name = 'cuentas'


class CuentaCreateView(CreateView):
    model = Cuenta
    fields = ['numero', 'titular', 'cbu']
    success_url = '/cuentas/'
```

Con dos clases, Django genera vistas completas de listado y creación. **Muy
poderoso** cuando el caso es estándar.

### Cuando usar CBV:

- CRUD simple (listar, crear, editar, borrar objetos).
- Vistas repetitivas que solo cambian el modelo o el template.

### Cuando usar FBV:

- Lógica compleja o específica.
- Cuando la vista hace algo que no encaja en las genéricas.
- Cuando priorizás legibilidad para principiantes.

En proyectos reales se mezclan: CBV para casos genéricos, FBV para casos
específicos. Aprender CBV a fondo (mixins, herencia de vistas, hooks) es un
salto de productividad importante.

## Frontend moderno: cuando HTML+Bootstrap no alcanza

Todo el manual usamos HTML server-rendered con Bootstrap. Es un stack válido y
muchos proyectos exitosos lo usan.

Pero hay casos donde no alcanza:

- **Interfaces muy interactivas**: componentes que se actualizan sin recargar,
  drag-and-drop, editores en vivo.
- **Aplicaciones con estado complejo** en el cliente.
- **Requisitos de UX modernos**: transiciones suaves, feedback inmediato,
  feeling de "app" en vez de "sitio".

Ahí entran los **frameworks JavaScript**:

- **React**: el más popular. Ecosistema enorme, muchísimos trabajos
  disponibles.
- **Vue**: más simple, curva de aprendizaje más suave.
- **Svelte**: moderno, compila a JavaScript muy eficiente.
- **Angular**: potente, más complejo, se usa mucho en empresas grandes.

El patrón típico con framework JS + Django:

- Django expone una **API REST** con DRF.
- El frontend (React/Vue/Svelte) es una aplicación separada que consume esa
  API.
- Django deja de servir HTML - solo devuelve JSON.

Este stack se llama **"headless Django"** o **"backend-frontend separado"**. Es
la arquitectura más común hoy en aplicaciones nuevas.

**Alternativa moderna: HTMX.** Si querés interactividad sin la complejidad de
un framework JS completo, **HTMX** es una biblioteca minimalista que agrega
interactividad directamente al HTML server-rendered. Funciona perfecto con
Django. Cada vez más popular por su simplicidad. Vale la pena mirar.

### Cuando aprender JS moderno:

- Si el trabajo lo pide (mercado laboral fullstack).
- Si el proyecto necesita interactividad avanzada.
- Si te interesa el desarrollo web completo.

**Cuando no obsesionarse:** para proyectos internos, herramientas de
administración, sistemas B2B - Django + HTMX + Bootstrap alcanza y sobra en el
80% de los casos.

## Testing avanzado

En el manual vimos testing básico con TestCase. Hay más:

- **pytest-django**: sintaxis más limpia, fixtures potentes, mejor salida en
  fallos. Estándar de facto en proyectos modernos.
- **factory-boy**: crear objetos de prueba complejos con una línea. Reemplaza
  el setUp manual.
- **model-bakery**: alternativa a factory-boy, más simple.
- **Selenium / Playwright**: tests end-to-end que abren un navegador real y
  hacen click. Más lentos, más completos.
- **hypothesis**: property-based testing. En vez de probar casos específicos,
  Python genera cientos de entradas aleatorias y verifica que tu código las
  maneje.
- **tox / nox**: correr tests en múltiples versiones de Python/Django
  simultáneamente.

### Cuando aprender:

- pytest y factory-boy: apenas se sumen a un equipo profesional.
- Selenium/Playwright: cuando el proyecto necesita tests de UI real.
- hypothesis: para código con lógica compleja, algoritmos, procesamiento de
  datos.

## Bases de datos: más allá de SQL

Todo el manual usamos SQL (SQLite, PostgreSQL). Es lo dominante. Pero hay
familias enteras de bases de datos que resuelven otros problemas:

### NoSQL - Documentos

- **MongoDB**: guarda documentos JSON. Bueno cuando la estructura de datos
  varía o es muy flexible.
- Django permite usar MongoDB con Django, aunque no es transparente como
  PostgreSQL.

### NoSQL - Clave-valor

- **Redis**: almacenamiento en memoria, ultra rápido. Usado como caché, cola de
  mensajes, sesiones. Django tiene backends para usarlo.

### Búsqueda de texto completo

- **ElasticSearch**: motor especializado en búsqueda. Django-elasticsearch-dsl
  lo integra.
- **PostgreSQL full-text search**: PostgreSQL tiene búsqueda de texto muy
  potente, muchas veces alcanza sin sumar otro sistema.

### Bases de tiempo

- **InfluxDB**, **TimescaleDB**: para métricas y series temporales. Sensores,
  logs, monitoreo.

### Cuando estudiar:

- **Redis**: incluso si no usás Redis como base principal, es muy útil como
  caché y como broker de Celery. Aprender Redis básico rinde mucho.
- Las otras: cuando el problema específico lo pida.

## Ciencia de datos y ML

Python es también el lenguaje dominante en ciencia de datos y machine
learning. Es un mundo enorme pero comparte lenguaje con lo que ya saben.

### Bibliotecas fundamentales:

- **NumPy**: arrays multidimensionales, álgebra lineal, computación numérica
  eficiente.
- **Pandas**: manipulación de datos tabulares. Como Excel pero en código, y
  para millones de filas.
- **Matplotlib / Seaborn / Plotly**: gráficos y visualizaciones.
- **scikit-learn**: machine learning clásico (regresiones, árboles,
  clustering, SVM).
- **PyTorch / TensorFlow**: deep learning y redes neuronales.

### Cuando interesa:

- Si el trabajo va hacia análisis de datos, business intelligence, reportes.
- Si les interesa investigación, ciencia, ingeniería con datos.
- Si su rol combina web + datos (por ejemplo, un dashboard con predicciones).

**Recurso recomendado:** el libro *Python for Data Analysis* de Wes McKinney
(creador de Pandas). Traducido al español.

## DevOps para desarrolladores

Cuando un proyecto crece, hay habilidades operacionales que ya no son
opcionales:

- **Git avanzado**: rebasing, cherry-picking, resolución de conflictos.
  Herramientas como git-lfs para archivos grandes.
- **Linux/Unix**: manejo de terminal, procesos, permisos, redes. No hay forma
  de trabajar en servidores serios sin esto.
- **Nginx / Apache**: configuración de servidores web.
- **Docker + Docker Compose**: mencionado arriba, pero vale repetir.
  Fundamental.
- **CI/CD**: GitHub Actions, GitLab CI. Automatizar tests y deploys.
- **Monitoring**: herramientas como Sentry (para errores en producción),
  Grafana (métricas), Loggly (logs).
- **Cloud básico**: al menos entender AWS, Google Cloud o Azure a nivel
  conceptual.

Estas habilidades **multiplican tu valor** como desarrollador. Un dev que solo
puede escribir código y necesita que otro le arme el entorno vale menos que uno
que puede llevar el sistema desde el código hasta producción.

## Especialización: caminos posibles

Con el conocimiento que tienen ahora, hay varios rumbos claros:

### Backend Python puro

- Profundizar Django, DRF, Celery, PostgreSQL.
- Aprender arquitecturas de microservicios.
- Fastapi para APIs modernas.
- Bases de datos avanzadas, caching, colas.

### Fullstack Python + JS

- React o Vue como frontend.
- APIs REST o GraphQL como backend.
- Deploy full-stack.

### DevOps / SRE

- Docker, Kubernetes.
- Infraestructura como código (Terraform, Ansible).
- Observabilidad, monitoring, alerting.
- Cloud engineering.

### Data / ML

- Pandas, NumPy, scikit-learn.
- PyTorch/TensorFlow.
- Ingeniería de datos con Spark, Airflow.
- MLOps.

### Automatización / Scripting

- Python como herramienta para automatizar procesos.
- Web scraping, procesamiento de documentos, integración de sistemas.
- Se cruza mucho con roles de análisis y consultoría.

### Ciberseguridad

- Python es el lenguaje dominante en pentesting y análisis de seguridad.
- Frameworks como Metasploit, herramientas como Scapy.

Todos estos caminos son válidos. La elección depende de qué les interesa y qué
mercado laboral tienen cerca.

## Mantenerse actualizado

El ecosistema Python cambia constantemente. Bibliotecas nuevas, features en el
lenguaje, mejores prácticas. Algunas fuentes recomendadas para no quedarse
atrás:

### Newsletters:

- **Django News** (https://django-news.com/): novedades semanales del
  ecosistema Django.
- **PyCoder's Weekly** (https://pycoders.com/): general de Python, muy curado.
- **Python Weekly** (https://www.pythonweekly.com/): alternativa a PyCoder's.

### Podcasts:

- **Talk Python to Me** (Michael Kennedy): entrevistas con desarrolladores del
  ecosistema.
- **Real Python Podcast**: variado, muchos tutoriales cortos.
- **Django Chat**: enfocado en Django, temas específicos.

### Blogs:

- **Real Python** (https://realpython.com/): tutoriales de calidad, algunos
  gratuitos.
- **Django Girls Tutorial**: entry level, sigue vigente.
- **Adam Johnson's Blog** (https://adamj.eu/): profundidad técnica en Django y
  Python.
- **Simon Willison** (https://simonwillison.net/): creador de Django, escribe
  cosas interesantes.

### Conferencias:

- **PyCon**: la conferencia anual global de Python. Los videos están en
  YouTube.
- **DjangoCon**: enfocado en Django, US y Europe.
- **PyCon Argentina**: la comunidad local, ediciones anuales.
- **PyDay La Plata**: La comunidad de la Facultad Regional La Plata de la
  Universidad Tecnológica Nacional enfocado a la difusión del lenguaje,
  ediciones anuales.

### Comunidades:

- Django Discord oficial.
- r/django y r/Python en Reddit.
- Stack Overflow: sigue siendo la referencia para preguntas técnicas.

## Contribuir al open source

Un paso importante para crecer como desarrollador: **contribuir a proyectos
open source**. Es gratis, mejora tus habilidades, arma portfolio, te conecta
con la comunidad.

Cómo empezar:

1. Encontrá un proyecto que uses y te guste (Django, DRF, requests, cualquier
   otro).
2. Buscá issues etiquetados como good first issue o beginner friendly.
3. Leé la guía de contribución (CONTRIBUTING.md).
4. Empezá con algo chico: mejorar documentación, agregar tests, arreglar un bug
   simple.
5. Abrí un pull request. Aprendé del feedback.

No hace falta contribuir código de entrada - traducciones, documentación,
ejemplos, reporte de bugs, todo cuenta.

### Beneficios:

- Aprendés a leer código profesional.
- Aprendés flujos de trabajo reales (Git, code review, CI/CD).
- Aparece en tu perfil de GitHub - reclutadores lo ven.
- Conocés a otros desarrolladores del ecosistema.

## El proyecto banco como base

El sistema bancario que construyeron a lo largo del manual **no tiene que
quedar acá**. Es una base sólida sobre la que pueden seguir experimentando y
aprendiendo.

Ideas de expansión:

- **API REST**: exponerlo con DRF, hacer una app móvil que lo consuma.
- **Notificaciones**: cuando se hace una transferencia, notificar al receptor.
  Empieza con emails, después WebSockets.
- **Dashboards**: gráficos de saldo en el tiempo, distribución de gastos por
  categoría. Con Chart.js o Plotly.
- **Reportes**: generar PDFs de resúmenes mensuales con reportlab o
  weasyprint. Enviar por email con Celery.
- **Integración externa**: consultar el dólar oficial y blue en tiempo real
  desde alguna API pública.
- **Deploy real**: subirlo a Railway o Render, compartir el link.
- **Machine learning simple**: detectar movimientos "sospechosos" (montos
  inusuales, muchas operaciones en poco tiempo) con scikit-learn.

Cada una de estas expansiones es una excusa para aprender algo nuevo, y **el
código base ya está listo** para recibirlo. Ese es el poder de haber
construido con buenas prácticas desde el principio.
