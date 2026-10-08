# Capítulo 17. El Admin de Django

*ABM gratis.*

## ¿Por qué leemos este capítulo?

Desde el capítulo 12, cuando armamos el patrón ABM en el proyecto bancario,
veníamos prometiendo esto: *"todo lo que hicimos a mano, Django lo genera
automáticamente"*. Este es el capítulo donde la promesa se cumple.

En el capítulo 15, la iteración 4 del banco tenía una clase Banco con métodos
abrir_cuenta, buscar_cuenta, listar_cuentas_activas, cerrar_cuenta. Cada uno
con su lógica, sus validaciones, sus excepciones. Al final del capítulo 15,
esa clase tenía casi 100 líneas de código.

En Django, ese mismo ABM, con **interfaz web incluida**, con formularios, con
búsqueda, con paginación, con filtros, se logra con **3 líneas por modelo**.

No es magia: es el **Admin de Django**, una app built-in que analiza tus
modelos y genera automáticamente una interfaz de administración web completa.
Es una de las razones por las que Django gana proyectos donde el equipo
necesita productividad rápida: podés tener un sistema web operable en un par
de días, sin escribir una sola vista, sin un template, sin un formulario.

Este capítulo es corto, pero visualmente muy gratificante. Al final vas a
tener el sistema bancario administrable desde el navegador, **con la misma
potencia que aplicaciones que en el mercado cuestan miles de dólares**.

## Qué es el Admin

El Admin es una **aplicación Django** (django.contrib.admin) que viene
**preinstalada**. Su función:

- Detecta los modelos que registres.
- Genera automáticamente páginas para: listar, crear, editar y borrar objetos
  de cada modelo.
- Ofrece búsqueda, filtros, ordenamiento, paginación.
- Maneja autenticación: solo usuarios "staff" pueden entrar.
- Se puede personalizar hasta el detalle sin escribir HTML.

Es una **interfaz para administradores del sistema**, no para usuarios
finales. Los clientes del banco no van a usar el admin, los empleados del
banco sí. Esa distinción es importante: no toda la interfaz web va acá. Para
vistas al usuario final (el home banking del cliente), vamos a construir
vistas y templates propios en los próximos capítulos.

## Lo que ya viene funcionando

Cuando corriste python manage.py migrate en el capítulo anterior, Django ya
creó las tablas del admin, junto con las de autenticación de usuarios. El
admin está listo, solo hay que activarlo.

## Primer paso: crear un superusuario

Para entrar al admin necesitás un **usuario administrador**. Django trae el
comando para crearlo:

```bash
python manage.py createsuperuser
```

Te va a pedir tres datos:

```text
Nombre de usuario: admin
Dirección de correo electrónico: admin@banco.utn.edu.ar
Password:
Password (again):
Superusuario creado exitosamente.
```

El password no se muestra mientras lo escribís (es normal, no está roto).

En un proyecto real de curso, usá un password fácil de recordar, es tu
ambiente de desarrollo, nadie más lo va a usar. En producción, usá algo largo
y seguro.

Ya podemos entrar.

## Acceder al Admin

Arrancá el servidor si no lo tenés corriendo:

```bash
python manage.py runserver
```

Y en el navegador andá a:

**http://127.0.0.1:8000/admin/**

Vas a ver la pantalla de login. Ingresá el usuario y contraseña que acabás de
crear. Adentro:

![Dos capturas de pantalla del admin de Django en inglés. A la izquierda y
arriba, la pantalla de login "Django administration" en la dirección
127.0.0.1:8000/admin/login/?next=/admin/, con el campo Username completado con
"sinny", el campo Password con puntos y el botón "Log in". Superpuesta a la
derecha y abajo, la pantalla "Site administration" luego de entrar
("WELCOME, SINNY."), con dos secciones: "Authentication and Authorization"
(Groups y Users) y "Faculty" (Faculty_details), cada fila con los enlaces
"Add" y "Change", y a la derecha el panel "Recent Actions" con "None
available".](images/cap17-admin-login-y-pantalla-inicial.jpg)

Django todavía **no muestra nuestros modelos**. Solo aparecen los que vienen
con la app auth. Eso es porque **no los registramos**. Es el próximo paso.

## Registrando modelos

**banco/admin.py**

```python
from django.contrib import admin
from banco.models import (
    PersonaFisica,
    PersonaJuridica,
    CuentaAhorro,
    CuentaCorriente,
    CuentaSueldo,
    Movimiento,
)

admin.site.register(PersonaFisica)
admin.site.register(PersonaJuridica)
admin.site.register(CuentaAhorro)
admin.site.register(CuentaCorriente)
admin.site.register(CuentaSueldo)
admin.site.register(Movimiento)
```

Guardá el archivo. Django recarga el servidor automáticamente (deberías ver en
la terminal algo como *"Watching for file changes"*). Actualizá el navegador.

Ahora ves:

![Captura de la pantalla de inicio del admin de Django en español, con la
barra "Django administration", el saludo "Bienvenido, admin. Salir" y la
ruta "Inicio". Hay dos secciones: "Autenticación y autorización" (Grupos y
Usuarios) y "Banco", que ahora lista Personas Físicas, Personas Jurídicas,
Cuentas de Ahorro, Cuentas Corrientes, Cuentas Sueldo y Movimientos. Cada
fila tiene el botón verde "+ Añadir" y el enlace "Cambiar". A la derecha, el
panel "Acciones recientes" con "Mis acciones: Ninguno
disponible".](images/cap17-admin-con-modelos-banco.jpg)

Con seis líneas de código, tenemos una app de administración web funcional
para todos nuestros modelos.

Hacé click en "Personas Físicas". Vas a ver una lista vacía y un botón
"Agregar Persona Física +". Hacé click y se abre un formulario con los campos
del modelo: nombre, apellido, dni, edad. Completá los datos y guardá. Django
lo persiste automáticamente en la base.

Después vas a "Cuentas de Ahorro", agregás una nueva, seleccionás a la
persona que acabás de crear como titular (el desplegable ya la muestra), y
guardás.

**Todo el ABM del capítulo 12 funciona sin haber escrito una vista, ni un
template, ni un formulario.**

## Cómo Django decide qué nombres mostrar

Django usa los verbose_name y verbose_name_plural de la Meta de cada modelo.
Por eso ves "Personas Físicas" y "Cuentas de Ahorro" con las tildes y el
plural correcto: fue lo que definimos en el capítulo anterior.

El texto que aparece para cada objeto en el listado es lo que devuelve
\_\_str\_\_. Por eso las cuentas se muestran como *"Cuenta 001-100 - Ana Pérez
- $65000.00"*, es exactamente lo que devuelve nuestro método.

Esto ilustra un principio importante: **el trabajo que hicimos en el modelo se
refleja automáticamente en el admin**. Ahora entienden por qué insistimos en
\_\_str\_\_ prolijos y en Meta bien configurados: el admin los aprovecha
gratis.

## Personalizando: ModelAdmin

El registro simple con admin.site.register(Modelo) funciona bien, pero es lo
mínimo. Para casos reales, uno quiere personalizar cómo se muestran los
modelos en el admin.

Para eso está la clase **ModelAdmin**: una configuración que le pasás al admin
para adaptar la interfaz. La sintaxis:

```python
from django.contrib import admin

from banco.models import PersonaFisica


class PersonaFisicaAdmin(admin.ModelAdmin):
    # opciones de configuración
    ...


admin.site.register(PersonaFisica, PersonaFisicaAdmin)
```

Las opciones más útiles se ven mejor con ejemplos.

### list_display: qué columnas mostrar en el listado

Por defecto, el listado de cada modelo muestra una sola columna con el
\_\_str\_\_. Con list_display decidís qué columnas ver:

```python
class PersonaFisicaAdmin(admin.ModelAdmin):
    list_display = ['apellido', 'nombre', 'dni', 'edad', 'creado_en']
```

Ahora en la lista de personas físicas ves cinco columnas ordenadas. Cada una
es clickeable para ordenar ascendente/descendente por esa columna.

Podés incluir **métodos del modelo** (o del admin), no solo campos:

```python
class PersonaFisicaAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'dni', 'edad']
```

Django llama persona.nombre_completo() para cada fila y muestra el resultado.

### list_filter: filtros laterales

Un panel lateral con filtros por valor:

```python
class CuentaAhorroAdmin(admin.ModelAdmin):
    list_display = ['numero', 'titular', 'saldo', 'activa', 'creada_en']
    list_filter = ['activa', 'creada_en']
```

Con eso, en la lista de cuentas de ahorro aparece un panel derecho con
filtros: "Activa (sí / no)" y "Creada en (hoy / última semana / último mes /
este año)". Django genera los filtros automáticamente según el tipo de campo.

### search_fields: barra de búsqueda

Buscar por texto libre en campos específicos:

```python
class PersonaFisicaAdmin(admin.ModelAdmin):
    list_display = ['apellido', 'nombre', 'dni']
    search_fields = ['apellido', 'nombre', 'dni']
```

Aparece una barra de búsqueda arriba del listado. Cuando escribís algo,
Django busca coincidencias en los campos listados (con icontains implícito,
case-insensitive, contiene el texto).

Para buscar en un campo relacionado, se usa doble subrayado:

```python
class CuentaAhorroAdmin(admin.ModelAdmin):
    search_fields = ['numero', 'titular__nombre', 'titular__apellido']
    # buscar cuentas por número, o por nombre/apellido del titular
```

Esto es potente: **una única barra de búsqueda puede recorrer relaciones**.
Buscá "Pérez" y aparecen todas las cuentas cuyo titular se apellida Pérez.

### readonly_fields: campos no editables

Algunos campos no deberían modificarse desde el admin - como fechas
automáticas, saldo (que solo cambia por operaciones), CBU:

```python
class CuentaAhorroAdmin(admin.ModelAdmin):
    list_display = ['numero', 'titular', 'saldo', 'activa']
    readonly_fields = ['saldo', 'cbu', 'creada_en']
```

Ahora al editar una cuenta, esos tres campos se muestran pero no se pueden
cambiar. Sigue siendo posible ver su valor.

### ordering: orden por defecto del listado

```python
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'cuenta', 'tipo', 'monto', 'saldo_posterior']
    ordering = ['-fecha']       # más recientes primero
```

Esto sobrescribe el ordering del Meta del modelo, solo para el admin.

### Todo junto: personalizar PersonaFisica

```python
class PersonaFisicaAdmin(admin.ModelAdmin):
    list_display = ['apellido', 'nombre', 'dni', 'edad', 'cantidad_cuentas']
    list_filter = ['edad']
    search_fields = ['apellido', 'nombre', 'dni']
    ordering = ['apellido', 'nombre']

    def cantidad_cuentas(self, obj):
        return obj.cuentas.count()

    cantidad_cuentas.short_description = "Cuentas"
```

Fijate lo último: **cantidad_cuentas es un método del ModelAdmin, no del
modelo**. Recibe el objeto (obj) y devuelve lo que se muestra en la columna.
El atributo .short_description cambia el título de la columna en la tabla.

Es una forma de agregar "columnas calculadas" al admin sin ensuciar el modelo
con lógica de presentación.

### El decorador `@admin.register`

Hay una sintaxis alternativa más compacta usando el decorador
@admin.register:

```python
from django.contrib import admin
from banco.models import PersonaFisica


@admin.register(PersonaFisica)
class PersonaFisicaAdmin(admin.ModelAdmin):
    list_display = ['apellido', 'nombre', 'dni', 'edad']
    search_fields = ['apellido', 'nombre', 'dni']
```

Se lee más natural: *"registrá esta clase como admin de PersonaFisica"*. Es
equivalente al admin.site.register(...) que veníamos usando. En proyectos
modernos, se prefiere el decorador. Vamos a usarlo de acá en adelante.

## Inlines: mostrar relaciones dentro de un objeto

Uno de los superpoderes del admin son los **inlines**: cuando estás editando
un objeto, podés ver y editar los objetos relacionados en la misma pantalla.

Ejemplo: cuando abrimos el admin de una persona, sería útil ver **todas sus
cuentas** directamente ahí, en vez de tener que ir a la sección de cuentas por
separado.

```python
from django.contrib import admin

from banco.models import PersonaFisica, Cuenta


class CuentaInline(admin.TabularInline):
    model = Cuenta
    fields = ['numero', 'saldo', 'activa']
    readonly_fields = ['numero', 'saldo']
    extra = 0       # cuántas filas vacías mostrar para agregar nuevos objetos


@admin.register(PersonaFisica)
class PersonaFisicaAdmin(admin.ModelAdmin):
    list_display = ['apellido', 'nombre', 'dni', 'edad']
    search_fields = ['apellido', 'nombre', 'dni']
    inlines = [CuentaInline]
```

Ahora, cuando abrís una persona física, debajo de sus datos aparece una
**tabla con todas sus cuentas**. Es la vista que un empleado del banco
necesita: ver un cliente y todas sus cuentas de una sola vez.

Dos tipos de inline:

| admin.TabularInline | admin.StackedInline |
| --- | --- |
| Muestra los objetos como filas de una tabla (compacto). | Los muestra como formularios apilados (más espacio, más detalle). |

Usualmente TabularInline es más útil para relaciones simples, StackedInline
para relaciones con muchos campos.

## Acciones personalizadas del admin

Otra funcionalidad muy útil: **acciones sobre múltiples objetos
seleccionados**. Django trae la acción "Borrar seleccionados" por defecto,
pero podés agregar las tuyas.

Ejemplo: una acción "Acreditar intereses" que aplique intereses a todas las
cuentas de ahorro seleccionadas.

```python
from django.contrib import admin, messages

from banco.models import CuentaAhorro


@admin.register(CuentaAhorro)
class CuentaAhorroAdmin(admin.ModelAdmin):
    list_display = ['numero', 'titular', 'saldo', 'tasa_interes_anual', 'activa']
    list_filter = ['activa']
    search_fields = ['numero', 'titular__nombre', 'titular__apellido']
    readonly_fields = ['saldo', 'cbu']
    actions = ['acreditar_intereses_masivo']

    @admin.action(description="Acreditar intereses del mes")
    def acreditar_intereses_masivo(self, request, queryset):
        exitosas = 0
        for cuenta in queryset:
            try:
                cuenta.acreditar_intereses()
                exitosas += 1
            except Exception as e:
                self.message_user(
                    request,
                    f"Error en cuenta {cuenta.numero}: {e}",
                    level=messages.ERROR
                )

        self.message_user(
            request,
            f"Se acreditaron intereses en {exitosas} cuentas.",
            level=messages.SUCCESS
        )
```

Ahora en el listado de cuentas de ahorro, aparece un menú desplegable "Acción"
con la opción "Acreditar intereses del mes". Seleccionás varias cuentas con
los checkboxes, elegís la acción, aplicás y Django ejecuta
acreditar_intereses() en cada una, mostrando un mensaje al final.

Detalles:

| @admin.action(description="...") | queryset | self.message_user(...) |
| --- | --- | --- |
| decorador que registra el método como acción, con el texto que aparece en el menú. | es el conjunto de objetos seleccionados. Podés iterar sobre él como una lista. | muestra un mensaje al administrador al terminar la acción. El level puede ser SUCCESS, WARNING, ERROR. |

Las acciones son extremadamente útiles para operaciones masivas: aplicar
intereses, marcar cuentas inactivas, cambiar precios, enviar notificaciones.
Sin acciones, tendrías que editar objeto por objeto.

## `admin.py` completo del banco

Con todo lo visto, así queda el archivo completo:

**banco/admin.py**

```python
"""Configuración del admin del banco."""

from django.contrib import admin, messages
from banco.models import (
    PersonaFisica,
    PersonaJuridica,
    Cuenta,
    CuentaAhorro,
    CuentaCorriente,
    CuentaSueldo,
    Movimiento,
)


# ------------------------------------------------------------------
# Inlines
# ------------------------------------------------------------------

class CuentaInline(admin.TabularInline):
    model = Cuenta
    fields = ['numero', 'saldo', 'activa']
    readonly_fields = ['numero', 'saldo']
    extra = 0
    can_delete = False


class MovimientoInline(admin.TabularInline):
    model = Movimiento
    fields = ['fecha', 'tipo', 'monto', 'saldo_posterior', 'descripcion']
    readonly_fields = ['fecha', 'tipo', 'monto', 'saldo_posterior', 'descripcion']
    extra = 0
    can_delete = False
    ordering = ['-fecha']


# ------------------------------------------------------------------
# Personas
# ------------------------------------------------------------------

@admin.register(PersonaFisica)
class PersonaFisicaAdmin(admin.ModelAdmin):
    list_display = ['apellido', 'nombre', 'dni', 'edad', 'cantidad_cuentas']
    list_filter = ['edad']
    search_fields = ['apellido', 'nombre', 'dni']
    ordering = ['apellido', 'nombre']
    inlines = [CuentaInline]

    @admin.display(description="Cuentas")
    def cantidad_cuentas(self, obj):
        return obj.cuentas.count()


@admin.register(PersonaJuridica)
class PersonaJuridicaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cuit', 'cantidad_cuentas']
    search_fields = ['nombre', 'cuit']
    inlines = [CuentaInline]

    @admin.display(description="Cuentas")
    def cantidad_cuentas(self, obj):
        return obj.cuentas.count()


# ------------------------------------------------------------------
# Cuentas
# ------------------------------------------------------------------

@admin.register(CuentaAhorro)
class CuentaAhorroAdmin(admin.ModelAdmin):
    list_display = ['numero', 'titular', 'saldo', 'tasa_interes_anual', 'activa']
    list_filter = ['activa', 'creada_en']
    search_fields = ['numero', 'titular__nombre']
    readonly_fields = ['numero', 'saldo', 'cbu', 'creada_en']
    inlines = [MovimientoInline]
    actions = ['acreditar_intereses_masivo']

    @admin.action(description="Acreditar intereses del mes")
    def acreditar_intereses_masivo(self, request, queryset):
        exitosas = 0
        for cuenta in queryset:
            try:
                cuenta.acreditar_intereses()
                exitosas += 1
            except Exception as e:
                self.message_user(
                    request,
                    f"Error en cuenta {cuenta.numero}: {e}",
                    level=messages.ERROR
                )
        self.message_user(
            request,
            f"Se acreditaron intereses en {exitosas} cuentas.",
            level=messages.SUCCESS
        )


@admin.register(CuentaCorriente)
class CuentaCorrienteAdmin(admin.ModelAdmin):
    list_display = ['numero', 'titular', 'saldo', 'limite_descubierto', 'activa']
    list_filter = ['activa']
    search_fields = ['numero', 'titular__nombre']
    readonly_fields = ['numero', 'saldo', 'cbu', 'creada_en']
    inlines = [MovimientoInline]


@admin.register(CuentaSueldo)
class CuentaSueldoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'titular', 'saldo', 'tope_sin_retencion', 'activa']
    list_filter = ['activa']
    search_fields = ['numero', 'titular__nombre']
    readonly_fields = ['numero', 'saldo', 'cbu', 'creada_en']
    inlines = [MovimientoInline]


# ------------------------------------------------------------------
# Movimientos
# ------------------------------------------------------------------

@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'cuenta', 'tipo', 'monto', 'saldo_posterior']
    list_filter = ['tipo', 'fecha']
    search_fields = ['cuenta__numero', 'descripcion']
    readonly_fields = ['cuenta', 'tipo', 'monto', 'saldo_posterior',
                       'descripcion', 'fecha']
    ordering = ['-fecha']

    def has_add_permission(self, request):
        return False    # los movimientos se crean automáticamente, no a mano
```

Notas de diseño:

- **Movimientos como readonly**: no permitimos crear o editar movimientos
  desde el admin. Los movimientos son "hechos ocurridos" que se generan
  automáticamente cuando se hace una operación en la cuenta. Modificarlos a
  mano sería falsear el historial. El método has_add_permission bloquea la
  creación manual.
- **Saldo y CBU son readonly**: mismo motivo. El saldo se modifica por
  operaciones (depositar, extraer), el CBU se asigna una vez y no cambia.
- **Los movimientos aparecen como inline dentro de las cuentas**: al abrir una
  cuenta, ves todos sus movimientos.
- **Las cuentas aparecen como inline dentro de las personas**: al abrir una
  persona, ves todas sus cuentas.

## Anatomía visual del admin

Con esta configuración, un empleado del banco entra al admin y ve:

**Página principal:**

![Captura de la página principal del admin del banco. Bajo la barra "Django
administration" y la ruta "Inicio", la sección "Autenticación y autorización"
(Grupos, Usuarios) y la sección "Banco" con Personas Físicas (5), Personas
Jurídicas (2), Cuentas de Ahorro (8), Cuentas Corrientes (3), Cuentas Sueldo
(2) y Movimientos (147), cada una con el botón "+ Añadir" y el enlace
"Cambiar". Un recuadro de esquinas redondeadas resalta las seis filas de la
sección Banco.](images/cap17-admin-pagina-principal.png)

**Lista de Personas Físicas:**

![Captura del listado "Seleccione persona física para modificar". Arriba, la
barra de búsqueda con el botón "Buscar" y el botón verde "AÑADIR PERSONA
FÍSICA +". Debajo, el selector "Acción" con el botón "Ejecutar" y "0 de 3
seleccionados". La tabla tiene las columnas APELLIDO (ordenada
ascendentemente), NOMBRE, DNI, EDAD y CUENTAS, con tres filas: Pérez, Ana,
12345678, 32, 3; López, Juan, 87654321, 45, 2; Rodríguez, Pedro, 11223344, 28,
1. Al pie, "3 personas físicas".](images/cap17-admin-lista-personas-fisicas.jpg)

**Detalle de Ana Pérez:**

![Captura de la pantalla "Cambiar persona física" para Ana Pérez, con la ruta
Inicio > Banco > Personas Físicas > Ana Pérez. La sección "Datos personales"
muestra los campos Nombre (Ana), Apellido (Pérez), DNI (12345678) y Edad (32).
Debajo, la sección "Cuentas de Ana" con una tabla de columnas NÚMERO, SALDO y
ACTIVA: 001-100 con $65.000,00 y activa tildada; 001-101 con $12.500,00 y
activa tildada; 001-102 con $0,00, sin tildar y con la etiqueta gris "Dada de
baja". Al pie, el botón rojo "Eliminar" y los botones "Guardar y añadir otro",
"Guardar y continuar editando" y "Guardar".](images/cap17-admin-detalle-ana-perez.jpg)

**Detalle de una cuenta de ahorro:**

![Captura de la pantalla "Cambiar cuenta de ahorro" para la cuenta 001-100. La
sección "Datos de la cuenta" muestra: Número 001-100 (solo lectura); Titular,
un desplegable con "Ana Pérez (DNI 12345678)" y el enlace "ver detalle"; CBU
0170123456789012345678 (solo lectura); Saldo $65.000,00 (solo lectura); Tasa
de interés anual (%) 8,00 en un campo editable; Activa tildada; y Creada en
26/07/2026 15:41:23 (solo lectura). Debajo, la sección "Movimientos de esta
cuenta" con las columnas FECHA, TIPO, MONTO, SALDO POSTERIOR y DESCRIPCIÓN:
26/07/2026 15:45, Depósito, +$15.000,00, $65.000,00, "Depósito de prueba"; y
26/07/2026 15:42, Apertura, +$50.000,00, $50.000,00, "Apertura de cuenta". Al
pie, los botones "Eliminar", "Guardar y añadir otro", "Guardar y continuar
editando" y "Guardar".](images/cap17-admin-detalle-cuenta-ahorro.jpg)

Esto en una aplicación web tradicional sería 20 páginas HTML, 30 vistas,
decenas de formularios. Django lo genera todo a partir de nuestros modelos.

## Lo que ganamos y lo que no

**Lo que ganamos:**

- Un ABM completo, con interfaz web profesional, en 6 líneas.
- Búsqueda, filtros, paginación, autenticación, todo built-in.
- Cada modelo se administra según sus reglas: los movimientos son solo
  lectura, el saldo no se puede tocar a mano, las cuentas se ven anidadas en
  su titular.
- Acciones masivas sobre múltiples objetos (como acreditar intereses).
- Cambios inmediatos: modificás un list_display en el admin, guardás,
  recargás el navegador.

**Lo que el Admin NO es:**

- **NO es la interfaz para los usuarios finales del sistema.** Los clientes
  del banco no van a entrar al admin. El admin es para
  empleados/administradores.
- **NO reemplaza a las vistas propias.** Cuando querés páginas específicas. el
  "resumen de mi cuenta" para un cliente, un formulario web personalizado para
  transferir plata. hay que escribirlas como vistas + templates. Eso es lo que
  viene en los próximos capítulos.
- **NO es infinitamente customizable.** Para casos muy específicos, se vuelve
  más práctico hacer una app propia que forzar el admin.

> **Regla mental:** El admin es para el equipo interno, las vistas son para el
> usuario final.

## Buenas prácticas

Cerramos el capítulo con algunas buenas prácticas que emergieron
implícitamente:

1. **Registrá siempre todos tus modelos en el admin.** Aunque no los uses
   todos los días, tener el admin listo desde el principio te da un
   "backdoor" para inspeccionar y corregir datos manualmente si aparece un
   bug.
2. **Configurá list_display con las columnas más importantes.** El listado por
   defecto muestra solo \_\_str\_\_, y en un modelo con 20 campos eso es poco
   útil.
3. **Usá search_fields en todos los modelos que tienen algún identificador
   texto.** El admin es mucho más ágil cuando podés buscar por nombre, DNI,
   número de cuenta, en vez de scrollear listas gigantes.
4. **Poné readonly_fields en todo lo que no debería editarse manualmente.**
   Saldos, IDs, fechas automáticas, códigos generados por el sistema. Es una
   capa extra de seguridad contra errores humanos.
5. **Usá inlines para relaciones importantes.** Ver una persona y sus cuentas
   de una sola vez es mucho más productivo que navegar entre secciones.
6. **Escribí \_\_str\_\_ bien detallados en los modelos.** El admin los usa en
   desplegables, listas, títulos de páginas. Un \_\_str\_\_ claro hace el admin
   mucho más usable.
7. **Aprovechá las acciones masivas para operaciones repetitivas.** Cualquier
   tarea que se hace sobre muchos objetos a la vez es candidata a ser una
   acción.

En el próximo capítulo **URLs y Vistas**, vamos a empezar a construir la
interfaz del **cliente**: las páginas que van a usar los titulares de cuenta
cuando entren al sitio del banco. Vamos a escribir nuestras primeras vistas
propias, definir URLs personalizadas, y sentar las bases para el home banking
del proyecto. Es el capítulo donde Django deja de "generar cosas
automáticamente" y empezás a construir la aplicación que tenías en mente desde
el principio.
