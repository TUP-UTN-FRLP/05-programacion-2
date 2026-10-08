# Capítulo 21. Django: Autenticación y usuarios

*Cada uno ve lo suyo.*

## ¿Por qué leemos este capítulo?

Hasta ahora, cualquiera que abra el navegador puede ver todas las cuentas,
todos los movimientos, todos los clientes. Está bien para desarrollo, pero **no
es un banco**: es un catálogo público de datos financieros.

Este capítulo cambia eso. Vamos a agregar:

- **Login y logout**: usuarios que se autentican con credenciales.
- **Registro de usuarios**: alta de nuevos clientes.
- **Protección de vistas**: solo usuarios logueados pueden ver ciertas
  páginas.
- **Filtrado por usuario**: Ana ve solo sus cuentas, Juan solo las suyas.
- **Distinción entre clientes y empleados**: el admin sigue reservado para
  staff.

Al final del capítulo, el sistema deja de ser una demo abierta y se convierte
en un **home banking real**, con la seguridad básica que espera cualquier
aplicación web moderna.

## El sistema de autenticación de Django

Cuando corriste `python manage.py migrate` al principio del proyecto, Django
creó varias tablas propias - entre ellas, la de **usuarios**. El sistema de
autenticación viene incluido: no hay que instalar nada extra, no hay que
configurar nada.

### El modelo User

Django trae un modelo `User` en `django.contrib.auth.models`. Sus campos
principales:

- **`username`**: nombre de usuario único.
- **`password`**: guardado hasheado, nunca en texto plano.
- **`email`**: correo (opcional por defecto).
- **`first_name`, `last_name`**: nombre y apellido.
- **`is_active`**: si la cuenta está activa (bloqueo/desbloqueo).
- **`is_staff`**: si puede entrar al admin.
- **`is_superuser`**: permisos totales.

Cuando creaste el superusuario con `createsuperuser`, se generó una fila en
esta tabla. Lo mismo va a pasar cuando registremos clientes: cada uno va a
tener su `User`.

### Vincular User con PersonaFisica

En el banco tenemos dos entidades relacionadas pero distintas:

- **`User`** de Django: usuario para login (username, password).
- **`PersonaFisica`** nuestra: datos del cliente (nombre, apellido, DNI,
  edad).

**Un cliente del banco es una persona física con un usuario asociado**. Los
empleados (staff) también tienen usuario, pero no son personas físicas del
banco.

Para vincularlos, agregamos un `OneToOneField` en `PersonaFisica`:

**`banco/models.py`**

```python
from django.contrib.auth.models import User


class PersonaFisica(Persona):
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    edad = models.IntegerField()
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='persona_fisica',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Persona Física"
        verbose_name_plural = "Personas Físicas"

    # ... resto igual ...
```

**`OneToOneField`**: cada `User` tiene a lo sumo una `PersonaFisica`, y cada
`PersonaFisica` tiene a lo sumo un `User`. Los `null=True, blank=True`
permiten que existan personas físicas sin usuario (por ejemplo, empleados del
banco creados desde el admin, o personas físicas dadas de alta antes de tener
acceso web).

**`related_name='persona_fisica'`**: desde un `User` accedemos con
`user.persona_fisica`. Esto es lo que nos va a permitir preguntar *"¿qué
persona es este usuario?"*.

Después del cambio, generamos migración:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Login y logout: vistas built-in

Django trae vistas prehechas para login y logout. Solo hay que activarlas.

En `banco_utn/urls.py` agregamos:

**`banco_utn/urls.py`**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('banco.urls')),
]
```

**`django.contrib.auth.urls`** registra automáticamente:

- `/accounts/login/` - página de login.
- `/accounts/logout/` - logout.
- `/accounts/password_change/` - cambiar contraseña.
- `/accounts/password_reset/` - recuperar contraseña por email.
- Y varias más relacionadas con reset de password.

**No hay que escribir ninguna vista.** Django las trae. Lo único que **sí**
hay que escribir son los templates.

### Template de login

Por convención, la vista de login busca el template en
`registration/login.html`. Creá:

![Diagrama de la estructura de carpetas del proyecto, en forma de árbol que se
lee de izquierda a derecha, con cajas conectadas por líneas. La raíz es la
carpeta "banco", de la que cuelgan ".venv", "banco_utn", otra carpeta "banco"
(la app, resaltada) y "manage.py". La carpeta de la app "banco" contiene
"\_\_init\_\_.py", "admin,py" (así figura en el diagrama), "apps.py",
"models.py", "tests.py", "views.py", "migrations", "templates" y "static". Dentro
de "templates" hay dos carpetas: "banco", con "base.html", "home.html",
"listar_cuentas.html", "detalle_cuentas.html", "listar_personas.html",
"detalle_persona.html" y "formulario_operacion.html"; y "registration", con el
archivo nuevo "login.html" resaltado en violeta oscuro.](images/cap21-estructura-templates-login.png)

**`banco/templates/registration/login.html`**

```html
{% extends 'banco/base.html' %}

{% block titulo %}Iniciar sesión - Banco UTN{% endblock %}

{% block contenido %}
    <div class="row justify-content-center">
        <div class="col-md-5">
            <h1 class="mb-4">Iniciar sesión</h1>

            {% if form.errors %}
                <div class="alert alert-danger">
                    Usuario o contraseña incorrectos.
                </div>
            {% endif %}

            <form method="post">
                {% csrf_token %}
                <div class="mb-3">
                    <label for="{{ form.username.id_for_label }}" class="form-label">
                        Usuario
                    </label>
                    <input type="text" name="username" id="{{ form.username.id_for_label }}"
                           class="form-control" required>
                </div>
                <div class="mb-3">
                    <label for="{{ form.password.id_for_label }}" class="form-label">
                        Contraseña
                    </label>
                    <input type="password" name="password" id="{{ form.password.id_for_label }}"
                           class="form-control" required>
                </div>
                <button type="submit" class="btn btn-primary">Ingresar</button>
                <a href="{% url 'banco:home' %}" class="btn btn-secondary">Cancelar</a>
            </form>

            <p class="mt-3">
                ¿No tenés cuenta?
                <a href="{% url 'banco:registrarse' %}">Registrate</a>
            </p>
        </div>
    </div>
{% endblock %}
```

Es un formulario común: username + password + submit. Django procesa la
autenticación automáticamente cuando llega el POST.

### Redirección después del login

Después del login exitoso, Django redirige a `LOGIN_REDIRECT_URL` (por defecto
`/accounts/profile/`, que en nuestro caso no existe). Configuralo en
`settings.py`:

**`banco_utn/settings.py`**

```python
LOGIN_REDIRECT_URL = 'banco:home'
LOGOUT_REDIRECT_URL = 'banco:home'
LOGIN_URL = 'login'   # a dónde ir cuando @login_required rebota al usuario
```

Con eso:

- Después de login exitoso ➡ home del banco.
- Después de logout ➡ home del banco.
- Cuando alguien intenta entrar a una página protegida sin estar logueado ➡
  login.

### El template de logout

Django 5 exige que el logout se haga por **POST** (no por GET), como
protección extra contra CSRF. Vamos a agregar un botón que dispare el POST
desde el menú.

En `banco/templates/banco/base.html`, en la navbar, agregamos:

**`banco/templates/banco/base.html`**

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
        <a class="navbar-brand" href="{% url 'banco:home' %}">🏛 Banco UTN</a>

        <div class="navbar-nav ms-auto">
            {% if user.is_authenticated %}
                <span class="nav-link text-white">Hola, {{ user.username }}</span>
                <a class="nav-link text-white" href="{% url 'banco:mis_cuentas' %}">Mis cuentas</a>
                <form method="post" action="{% url 'logout' %}" class="d-inline">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-link nav-link text-white">
                        Salir
                    </button>
                </form>
            {% else %}
                <a class="nav-link text-white" href="{% url 'login' %}">Ingresar</a>
                <a class="nav-link text-white" href="{% url 'banco:registrarse' %}">Registrarse</a>
            {% endif %}
        </div>
    </div>
</nav>
```

Puntos importantes:

- **`user.is_authenticated`**: variable disponible en todos los templates. Es
  `True` si el usuario está logueado.
- **`{{ user.username }}`**: mostramos su nombre de usuario.
- **Menú condicional**: si está logueado, ve "Salir" y "Mis cuentas". Si no,
  ve "Ingresar" y "Registrarse".
- **Logout como POST**: el botón está dentro de un `<form>` con
  `method="post"`. Es la forma segura.

## Registro de nuevos usuarios

Django trae `UserCreationForm` para el registro básico, pero como queremos
crear también la `PersonaFisica` asociada, hacemos un form propio.

**`banco/forms.py`**

```python
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from banco.models import PersonaFisica


class RegistroClienteForm(UserCreationForm):
    """Registro combinado: crea el User + PersonaFisica."""

    # Campos extra que no vienen en UserCreationForm
    apellido = forms.CharField(max_length=100)
    dni = forms.CharField(
        max_length=8,
        min_length=7,
        help_text="Solo dígitos, sin puntos"
    )
    edad = forms.IntegerField(min_value=18, max_value=120)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email',
                  'apellido', 'dni', 'edad',
                  'password1', 'password2']
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombre',
            'email': 'Email',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregamos clases Bootstrap a todos los campos
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_dni(self):
        dni = self.cleaned_data['dni'].strip()
        if not dni.isdigit():
            raise forms.ValidationError("El DNI debe contener solo dígitos")
        if PersonaFisica.objects.filter(dni=dni).exists():
            raise forms.ValidationError("Ya existe una persona con ese DNI")
        return dni

    def save(self, commit=True):
        """Crea el User y la PersonaFisica asociada."""
        # Guardamos el User primero (esto ya hashea el password)
        user = super().save(commit=commit)

        # Después creamos la PersonaFisica vinculada
        if commit:
            PersonaFisica.objects.create(
                nombre=self.cleaned_data['first_name'],
                apellido=self.cleaned_data['apellido'],
                dni=self.cleaned_data['dni'],
                edad=self.cleaned_data['edad'],
                usuario=user,
            )

        return user
```

Puntos importantes:

- **Hereda de `UserCreationForm`**: aprovecha su validación de contraseña (dos
  veces, con reglas de fortaleza) y el hasheo automático.
- **Agrega campos extra**: `apellido`, `dni`, `edad` para la `PersonaFisica`.
- **`clean_dni`**: valida formato + unicidad. Que el DNI sea único a nivel de
  persona física (no a nivel de `User`).
- **`save()` sobrescrito**: primero guarda el `User`, después crea la
  `PersonaFisica` vinculada. Ambas cosas en una sola transacción de la vista.

Y la vista:

**`banco/views.py`**

```python
from django.contrib.auth import login
from banco.forms import RegistroClienteForm

def registrarse(request):
    if request.user.is_authenticated:
        return redirect('banco:home')

    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)         # login automático después de registrar
            messages.success(request, f"Bienvenido, {user.username}!")
            return redirect('banco:home')
    else:
        form = RegistroClienteForm()

    return render(request, 'banco/registrarse.html', {'form': form})
```

**`login(request, user)`**: función de Django que autentica al usuario en la
sesión actual. Después del registro, el cliente ya queda logueado sin tener
que ingresar credenciales.

Y agregamos la URL:

**`banco/urls.py`**

```python
urlpatterns = [
    path('', views.home, name='home'),
    path('registrarse/', views.registrarse, name='registrarse'),
    # ... resto ...
]
```

Template básico:

**`banco/templates/banco/registrarse.html`**

```html
{% extends 'banco/base.html' %}

{% block titulo %}Registrarse - Banco UTN{% endblock %}

{% block contenido %}
    <div class="row justify-content-center">
        <div class="col-md-6">
            <h1 class="mb-4">Registro de cliente</h1>

            <form method="post">
                {% csrf_token %}
                {% for field in form %}
                    <div class="mb-3">
                        <label for="{{ field.id_for_label }}" class="form-label">
                            {{ field.label }}
                        </label>
                        {{ field }}
                        {% if field.errors %}
                            <div class="text-danger small">{{ field.errors|join:", " }}</div>
                        {% endif %}
                        {% if field.help_text %}
                            <div class="form-text small">{{ field.help_text }}</div>
                        {% endif %}
                    </div>
                {% endfor %}

                <button type="submit" class="btn btn-primary">Crear cuenta</button>
                <a href="{% url 'banco:home' %}" class="btn btn-secondary">Cancelar</a>
            </form>
        </div>
    </div>
{% endblock %}
```

Con esto, un cliente nuevo puede registrarse desde la web, crear su usuario y
su persona física de una sola vez, y quedar logueado automáticamente.

## Protegiendo vistas: `@login_required`

Ya podemos loguear usuarios. El siguiente paso: **impedir que usuarios
anónimos vean cosas que solo los logueados deberían ver**.

Django tiene un decorador `@login_required` que se aplica a cualquier vista:

```python
from django.contrib.auth.decorators import login_required


@login_required
def mis_cuentas(request):
    # solo se ejecuta si el usuario está logueado
    ...
```

Si alguien sin login intenta entrar a esta vista, Django lo redirige
automáticamente a la página de login (definida en `LOGIN_URL`). Después del
login, lo devuelve a la página que intentaba visitar.

Aplicamos el decorador a todas las vistas del sistema que requieran usuario
logueado:

**`banco/views.py`**

```python
from django.contrib.auth.decorators import login_required


@login_required
def mis_cuentas(request):
    ...


@login_required
def detalle_cuenta(request, numero):
    ...


@login_required
def depositar_en_cuenta(request, numero):
    ...
```

El home y la página de registro **no** llevan el decorador - deben ser
accesibles sin login.

## Filtrando por usuario: "solo tus cuentas"

Ahora la parte más importante: cuando Ana entra al banco, tiene que ver **solo
sus cuentas**, no las de Juan.

Hasta ahora `detalle_cuenta` devolvía cualquier cuenta por su número. Eso es un
agujero de seguridad enorme: Ana podría entrar a `/cuentas/001-200/` y ver la
cuenta de Juan si adivina el número.

La corrección se hace en la vista, filtrando por el usuario logueado:

**`banco/views.py`**

```python
@login_required
def mis_cuentas(request):
    """Cuentas del usuario logueado."""
    try:
        persona = request.user.persona_fisica
    except PersonaFisica.DoesNotExist:
        # Usuario sin persona física asociada (empleado del banco, por ejemplo)
        messages.warning(request, "Tu usuario no tiene cliente asociado")
        return redirect('banco:home')

    cuentas = persona.cuentas.filter(activa=True)
    return render(request, 'banco/mis_cuentas.html', {
        'persona': persona,
        'cuentas': cuentas,
    })


@login_required
def detalle_cuenta(request, numero):
    """Detalle de una cuenta. Solo el titular puede verla."""
    cuenta = get_object_or_404(Cuenta, numero=numero)

    # Verificamos que sea del usuario logueado (o es staff/admin)
    if not es_titular(request.user, cuenta) and not request.user.is_staff:
        messages.error(request, "No tenés permiso para ver esta cuenta")
        return redirect('banco:mis_cuentas')

    movimientos = cuenta.movimientos.order_by('-fecha')[:10]
    return render(request, 'banco/detalle_cuenta.html', {
        'cuenta': cuenta,
        'movimientos': movimientos,
    })


def es_titular(user, cuenta):
    """Devuelve True si el user es el titular de la cuenta."""
    try:
        return cuenta.titular_id == user.persona_fisica.id
    except (PersonaFisica.DoesNotExist, AttributeError):
        return False
```

Puntos clave:

- **`mis_cuentas`** obtiene la persona a través de `request.user.persona_fisica`
  (el `related_name` que definimos). Después filtra sus cuentas activas.
- **`detalle_cuenta`** ahora chequea que el usuario sea el titular **o** sea
  staff. Si no, redirige con un error.
- **Función auxiliar `es_titular`**: encapsula la lógica de "¿este usuario es
  el titular de esta cuenta?". Reutilizable en cualquier vista.

**Este patrón es fundamental en Django y en cualquier framework web**: no
basta con exigir login, hay que **filtrar los datos según quién es el
usuario**. Si Ana intenta acceder a la cuenta de Juan, el sistema debe
rechazarla - no confiar en que "seguro que no se le ocurre".

## Aplicar el mismo criterio a las operaciones

Todas las vistas que operan sobre cuentas deben validar la titularidad:

```python
@login_required
def depositar_en_cuenta(request, numero):
    cuenta = get_object_or_404(Cuenta, numero=numero)

    if not es_titular(request.user, cuenta):
        messages.error(request, "No tenés permiso para operar esta cuenta")
        return redirect('banco:mis_cuentas')

    # ... resto de la lógica ...
```

Ídem para extraer y transferir. Sin esa verificación, cualquier usuario
logueado podría depositar/extraer en cuentas ajenas.

## Refactor: un decorador propio

Repetir la verificación de titularidad en cada vista se vuelve pesado. Django
permite crear decoradores propios:

**`banco/decorators.py`**

```python
from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from banco.models import Cuenta


def titular_requerido(vista_func):
    """Decorador que verifica que el usuario logueado sea titular de la cuenta.

    Se aplica a vistas que reciben `numero` como parámetro.
    """
    @wraps(vista_func)
    def wrapper(request, numero, *args, **kwargs):
        cuenta = get_object_or_404(Cuenta, numero=numero)
        try:
            persona = request.user.persona_fisica
            if cuenta.titular_id != persona.id:
                messages.error(request, "No tenés permiso para operar esta cuenta")
                return redirect('banco:mis_cuentas')
        except AttributeError:
            messages.error(request, "Tu usuario no tiene cliente asociado")
            return redirect('banco:home')

        return vista_func(request, numero, *args, **kwargs)

    return wrapper
```

Y ahora las vistas quedan:

```python
from banco.decorators import titular_requerido

@login_required
@titular_requerido
def depositar_en_cuenta(request, numero):
    cuenta = get_object_or_404(Cuenta, numero=numero)
    # ... lógica ...


@login_required
@titular_requerido
def extraer_de_cuenta(request, numero):
    ...
```

**Los decoradores se apilan**: primero se aplica `login_required` (más
externo), después `titular_requerido`. Django ejecuta el orden natural.

Este es un ejemplo de **DRY** (*Don't Repeat Yourself*): la validación de
titularidad vive en un solo lugar y se reutiliza. Si mañana cambia la regla
(por ejemplo, se permite acceso a un cotitular), se toca en un solo archivo.

## Grupos y permisos: staff vs clientes

Django trae un sistema de **grupos y permisos**. Sirve para agrupar usuarios en
roles y asignarles permisos específicos.

Para el banco:

- **Clientes**: personas físicas con usuario. Solo ven sus cuentas.
- **Empleados**: staff. Pueden acceder al admin y operar sobre cualquier
  cuenta.
- **Superusuarios**: full access.

Esta distinción ya la tenemos implícitamente con los atributos del `User`:

- **`is_staff = True`**: puede entrar al admin.
- **`is_superuser = True`**: bypass de todas las restricciones.

Para restringir vistas por rol, existen decoradores adicionales:

```python
from django.contrib.auth.decorators import user_passes_test


@login_required
@user_passes_test(lambda u: u.is_staff)
def panel_administrativo(request):
    """Solo accesible por staff."""
    ...
```

`user_passes_test` recibe una función que evalúa al usuario. Si devuelve
`False`, se redirige a login.

Para casos más complejos (permisos granulares), Django ofrece `has_perm()` y
decoradores específicos. En el manual no profundizamos porque el banco no lo
necesita - con `is_staff` alcanza para el 90% de los casos.

## Vistas para el cliente: home banking

Ahora sí armamos las vistas propias del **home banking** del cliente. Un
usuario común entra, ve sus cuentas, opera. Las vistas administrativas siguen
en el admin.

### banco/urls.py actualizado

**`banco/urls.py`**

```python
from django.urls import path
from banco import views

app_name = 'banco'

urlpatterns = [
    path('', views.home, name='home'),
    path('registrarse/', views.registrarse, name='registrarse'),

    # Home banking del cliente
    path('mis-cuentas/', views.mis_cuentas, name='mis_cuentas'),
    path('cuentas/<str:numero>/', views.detalle_cuenta, name='detalle_cuenta'),
    path('cuentas/<str:numero>/depositar/', views.depositar_en_cuenta, name='depositar'),
    path('cuentas/<str:numero>/extraer/', views.extraer_de_cuenta, name='extraer'),
    path('cuentas/<str:numero>/transferir/', views.transferir_desde_cuenta, name='transferir'),
]
```

Removimos las vistas de "listar todas las cuentas" y "listar todas las
personas" que dejamos en el capítulo 19. Esas eran para desarrollo - un
cliente real no puede acceder a ellas. Si querés mantenerlas, restringilas a
staff con `@user_passes_test`.

### mis_cuentas.html

**`banco/templates/banco/mis_cuentas.html`**

```html
{% extends 'banco/base.html' %}

{% block titulo %}Mis cuentas - Banco UTN{% endblock %}

{% block contenido %}
    <h1 class="mb-4">Mis cuentas</h1>
    <p class="text-muted">Cliente: {{ persona }}</p>

    {% if cuentas %}
        <div class="row">
            {% for cuenta in cuentas %}
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">{{ cuenta.numero }}</h5>
                            <p class="card-text">
                                <strong>Saldo:</strong>
                                <span class="fs-3">${{ cuenta.saldo|floatformat:2 }}</span>
                            </p>
                            <p class="text-muted small">CBU: {{ cuenta.cbu }}</p>
                            <a href="{% url 'banco:detalle_cuenta' cuenta.numero %}"
                               class="btn btn-primary btn-sm">Ver movimientos</a>
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="alert alert-info">
            No tenés cuentas activas. Contactá a un empleado del banco para abrir una.
        </div>
    {% endif %}
{% endblock %}
```

Y con eso, cada usuario logueado ve sus cuentas y solo las suyas. Si Ana
intenta entrar a la URL de una cuenta de Juan, el sistema la rechaza.

## Contraseñas: cambio y recuperación

Django trae vistas built-in para:

- **Cambiar contraseña**: `/accounts/password_change/`.
- **Recuperar por email**: `/accounts/password_reset/`.

Ya las incluimos con `path('accounts/', include('django.contrib.auth.urls'))`.
Solo faltan los templates:

- `registration/password_change_form.html`
- `registration/password_change_done.html`
- `registration/password_reset_form.html`
- `registration/password_reset_done.html`
- `registration/password_reset_confirm.html`
- `registration/password_reset_complete.html`
- `registration/password_reset_email.html`

Es una lista larga, pero cada template es muy simple (formulario + submit). En
un proyecto real se copian, se adaptan al estilo y listo.

Para el manual, no vamos a implementar todos. Pero mostramos el patrón:
**Django trae la lógica, nosotros aportamos los templates**.

Para configurar el envío real de emails de recuperación, hay que configurar
`EMAIL_BACKEND` en `settings.py`. En desarrollo se usa un backend de consola
que solo imprime el email:

**`banco_utn/settings.py`**

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Cuando un usuario pide reset de contraseña, el email aparece en la terminal
donde corre `runserver`. Suficiente para desarrollo. Para producción se
configura un servidor SMTP real (Gmail, SendGrid, Mailgun, etc.).

## Buenas prácticas de seguridad

Cerramos el capítulo con las prácticas fundamentales que emergieron:

1. **Nunca guardes contraseñas en texto plano.** Django lo hace automático:
   hashea con PBKDF2 por defecto. Nunca las veas, nunca las loguees.
2. **Siempre validá titularidad, no solo login.** `@login_required` protege
   contra usuarios anónimos, pero no contra usuarios logueados que quieran ver
   datos ajenos. Filtrá por `request.user`.
3. **CSRF en todos los formularios.** `{% csrf_token %}` siempre. Django lo
   requiere, si no lo ponés los POST fallan.
4. **HTTPS en producción.** El manual usa HTTP en desarrollo (localhost)
   porque es simple. En producción es HTTPS obligatorio para que las
   credenciales viajen cifradas.
5. **No expongas datos sensibles innecesariamente.** El listado de "todas las
   cuentas del banco" no debería existir para clientes. El listado de "todos
   los movimientos" tampoco. Cada usuario ve solo lo suyo.
6. **Sesiones cortas en operaciones críticas.** Django tiene
   `SESSION_COOKIE_AGE` y `SESSION_EXPIRE_AT_BROWSER_CLOSE`. En bancos reales,
   la sesión cierra por inactividad después de unos minutos. Es una
   configuración simple con impacto grande en seguridad.
7. **Passwords fuertes.** `UserCreationForm` valida longitud mínima,
   similitud con datos del usuario, contraseñas comunes. No lo desactives.
8. **Los admins son los admins, los clientes son los clientes.** No permitas
   que un cliente entre al admin (`is_staff = False` por defecto). No
   confundas las URLs.
