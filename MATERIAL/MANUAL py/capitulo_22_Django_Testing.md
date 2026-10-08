# Capítulo 22. Testing en Django

*Verificando lo que promete el sistema.*

## ¿Por qué leemos este capítulo?

Hasta ahora, después de cada cambio en el banco, la única forma de saber si
algo se rompió era **probarlo a mano**: abrir el navegador, loguearse,
depositar, extraer, transferir, verificar que los saldos son correctos,
chequear que los mensajes aparecen. Cada verificación toma minutos. Y no se
hace la mayoría de las veces - cambiás algo, corre en el caso que probaste, y
confiás.

Esta forma de trabajar tiene un límite: **el sistema crece más rápido de lo
que podés probar a mano**. Con 20 vistas, 10 modelos, 5 formularios, es
imposible verificar todo tras cada cambio. Se acumulan bugs silenciosos. Se
rompen cosas viejas al agregar cosas nuevas. Es la muerte lenta de cualquier
proyecto que no tenga tests.

**Testing automático** resuelve esto. Escribís código que verifica que otro
código hace lo que promete. Corrés una sola línea de comando, y en segundos
sabés si todo sigue funcionando. Un cambio rompió algo ➡ los tests fallan ➡
lo corregís antes de que llegue al usuario.

En el capítulo 14 sembramos la idea con `assert`. En este capítulo la
formalizamos con las herramientas de Django. Al final, con
`python manage.py test` vas a poder verificar todo el sistema bancario en
segundos.

## Qué es testing

Un **test** es una función que ejercita una parte del sistema y verifica que
el resultado es el esperado. Estructura básica:

| Arrange | Act | Assert |
| --- | --- | --- |
| (preparar) | (actuar) | (verificar) |
| Armar los datos y objetos necesarios. | Ejecutar la operación a probar. | Chequear que el resultado es correcto. |

Ejemplo simple, sin Django todavía:

```python
def test_suma():

    # Arrange: no necesitamos preparar nada

    # Act

    resultado = 2 + 3

    # Assert

    assert resultado == 5, f"2 + 3 debería ser 5, obtuve {resultado}"




test_suma()      # si pasa no dice nada, si falla AssertionError
```

Ese patrón AAA (Arrange, Act, Assert) se repite en todos los tests. Con
frameworks de testing como el de Django, el `assert` se enriquece con métodos
más expresivos y con manejo automático de fallos.

### Los tres niveles

| Unit tests | Integration tests | End-to-end tests |
| --- | --- | --- |
| (unitarios) | (integración) | (E2E) |
| Prueban una unidad aislada: una función, un método, una clase - sin depender de otras partes del sistema. Rápidos y precisos. | Prueban que varias unidades trabajan juntas. Por ejemplo, que una vista consulta el modelo y devuelve el HTML correcto. | Simulan un usuario real usando el sistema completo. Abren un navegador, hacen click, verifican pantallas. Los más lentos, pero los más realistas. |

En Django cubrimos naturalmente los dos primeros niveles. E2E requiere
herramientas extra (Selenium, Playwright) y queda para cursos más avanzados.

## El framework de test de Django

Django trae su propio framework de testing basado en unittest de Python, con
extensiones específicas. Los tests viven en el archivo `tests.py` de cada app.

Cuando corriste `python manage.py startapp banco`, Django creó `banco/tests.py`
prácticamente vacío. Vamos a llenarlo.

### Un primer test

**`banco/tests.py`**

```python
from django.test import TestCase
from banco.models import PersonaFisica




class PersonaFisicaTest(TestCase):
    """Tests para el modelo PersonaFisica."""

    def test_crear_persona(self):
        persona = PersonaFisica.objects.create(
            nombre="Ana",
            apellido="Pérez",
            dni="12345678",
            edad=32,
        )
        self.assertEqual(persona.nombre, "Ana")
        self.assertEqual(persona.dni, "12345678")

    def test_str_muestra_nombre_y_dni(self):
        persona = PersonaFisica.objects.create(
            nombre="Ana",
            apellido="Pérez",
            dni="12345678",
            edad=32,
        )
        self.assertEqual(str(persona), "Ana (DNI 12345678)")
```

Estructura:

- **Clase que hereda de `TestCase`**: agrupa tests relacionados.
- **Cada método que empieza con `test_`**: es un test independiente.
- **`self.assertEqual(a, b)`**: verifica que `a == b`. Si no, el test falla con
  un mensaje claro.

Django tiene decenas de métodos `assert*`:

- `assertEqual(a, b) / assertNotEqual(a, b)`
- `assertTrue(x) / assertFalse(x)`
- `assertIsNone(x) / assertIsNotNone(x)`
- `assertIn(a, b) / assertNotIn(a, b)`
- `assertRaises(ExceptionClass)`
- `assertContains(response, text)` (para respuestas HTTP)
- Y muchos más.

Todos dan mensajes de error más útiles que un `assert` desnudo.

### Corriendo los tests

Con el servidor detenido (o en otra terminal), ejecutá:

```bash
python manage.py test
```

Django:

1. Crea una **base de datos temporal** vacía.
2. Aplica todas las migraciones.
3. Ejecuta cada test.
4. Al terminar, borra la base temporal.

**Los tests nunca tocan tu base de datos real.** Cada test empieza desde cero,
garantizando que no dependen del estado previo.

Salida típica:

```text
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 0.043s

OK
Destroying test database for alias 'default'...
```

Cada `.` es un test exitoso. Si un test falla, aparece `F` (fail) o `E` (error)
y al final se muestra el detalle.

### `setUp` y `tearDown`

Muchos tests necesitan los mismos datos iniciales. En vez de repetir el setup
en cada método, se usa `setUp`:

```python
class CuentaAhorroTest(TestCase):

    def setUp(self):
        """Se ejecuta antes de cada test."""
        self.ana = PersonaFisica.objects.create(
            nombre="Ana",
            apellido="Pérez",
            dni="12345678",
            edad=32,
        )

    def test_apertura_con_saldo_positivo(self):
        cuenta = CuentaAhorro.objects.create(
            numero="001-100",
            titular=self.ana,
            cbu="0170123456789012345678",
            saldo=5000,
        )
        self.assertEqual(cuenta.saldo, 5000)

    def test_apertura_con_saldo_cero(self):
        cuenta = CuentaAhorro.objects.create(
            numero="001-101",
            titular=self.ana,
            cbu="0170123456789012345679",
        )
        self.assertEqual(cuenta.saldo, 0)
```

`setUp` corre **antes de cada test**, con la base recién limpia. `self.ana` está
disponible en cada método.

Hay también `tearDown` (después de cada test) y `setUpTestData` (una sola vez,
más eficiente pero con restricciones). Para el manual, con `setUp` alcanza.

## Testeando modelos

Empecemos con los tests más simples: los del modelo. Verifican que las clases
hacen lo que prometen sin importar cómo se acceden desde afuera.

**`banco/tests.py`**

```python
from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError

from banco.models import (
    PersonaFisica,
    CuentaAhorro,
    CuentaCorriente,
    Movimiento,
)




class CuentaAhorroTest(TestCase):
    """Tests para el modelo CuentaAhorro."""

    def setUp(self):
        self.ana = PersonaFisica.objects.create(
            nombre="Ana",
            apellido="Pérez",
            dni="12345678",
            edad=32,
        )
        self.cuenta = CuentaAhorro.objects.create(
            numero="001-100",
            titular=self.ana,
            cbu="0170123456789012345678",
            saldo=Decimal('10000'),
            tasa_interes_anual=Decimal('5'),
        )

    def test_deposito_aumenta_saldo(self):
        self.cuenta.depositar(Decimal('500'))
        self.assertEqual(self.cuenta.saldo, Decimal('10500'))

    def test_deposito_registra_movimiento(self):
        cantidad_inicial = self.cuenta.movimientos.count()
        self.cuenta.depositar(Decimal('500'), descripcion="Test")

        self.assertEqual(self.cuenta.movimientos.count(), cantidad_inicial + 1)

        ultimo = self.cuenta.movimientos.order_by('-fecha').first()
        self.assertEqual(ultimo.tipo, "deposito")
        self.assertEqual(ultimo.monto, Decimal('500'))
        self.assertEqual(ultimo.descripcion, "Test")

    def test_deposito_negativo_lanza_error(self):
        with self.assertRaises(ValidationError):
            self.cuenta.depositar(Decimal('-100'))

    def test_deposito_cero_lanza_error(self):
        with self.assertRaises(ValidationError):
            self.cuenta.depositar(Decimal('0'))

    def test_extraccion_disminuye_saldo(self):
        self.cuenta.extraer(Decimal('3000'))
        self.assertEqual(self.cuenta.saldo, Decimal('7000'))

    def test_extraccion_mayor_al_saldo_lanza_error(self):
        with self.assertRaises(ValidationError):
            self.cuenta.extraer(Decimal('100000'))

    def test_cuenta_cerrada_no_permite_operar(self):
        self.cuenta.cerrar()

        with self.assertRaises(ValidationError):
            self.cuenta.depositar(Decimal('100'))

        with self.assertRaises(ValidationError):
            self.cuenta.extraer(Decimal('100'))

    def test_acreditar_intereses(self):
        # Saldo inicial: 10000, tasa 5% anual ➡ 5%/12 mensual ≈ 41.67
        saldo_previo = self.cuenta.saldo

        self.cuenta.acreditar_intereses()

        # El saldo debe haber aumentado
        self.assertGreater(self.cuenta.saldo, saldo_previo)

        # Debe haber un movimiento de tipo "interes"
        ultimo = self.cuenta.movimientos.order_by('-fecha').first()
        self.assertEqual(ultimo.tipo, "interes")
```

Este bloque testea el comportamiento completo del modelo `CuentaAhorro`:

- Deposito aumenta el saldo y registra movimiento.
- Deposito negativo o cero, lanza error.
- Extracción funciona normal.
- Extracción excesiva lanza error.
- Cuenta cerrada no permite operaciones.
- Intereses se acreditan.

Cada test es **una hipótesis verificable**. Si en el futuro cambiás la lógica
de `depositar()` y por accidente rompes la validación del monto negativo,
`test_deposito_negativo_lanza_error` falla y te avisa.

### Tests para `CuentaCorriente`

```python
class CuentaCorrienteTest(TestCase):

    def setUp(self):
        self.juan = PersonaFisica.objects.create(
            nombre="Juan",
            apellido="López",
            dni="87654321",
            edad=45,
        )
        self.cuenta = CuentaCorriente.objects.create(
            numero="001-200",
            titular=self.juan,
            cbu="0170123456789012345679",
            saldo=Decimal('5000'),
            limite_descubierto=Decimal('10000'),
        )

    def test_extraccion_hasta_saldo_normal(self):
        self.cuenta.extraer(Decimal('3000'))
        self.assertEqual(self.cuenta.saldo, Decimal('2000'))

    def test_extraccion_con_descubierto(self):
        # Saldo 5000, descubierto 10000, extraer 8000 ➡ saldo -3000
        self.cuenta.extraer(Decimal('8000'))
        self.assertEqual(self.cuenta.saldo, Decimal('-3000'))

    def test_extraccion_excede_descubierto(self):
        # Saldo 5000 + descubierto 10000 = 15000 disponible
        # Intentar extraer 20000 debe fallar
        with self.assertRaises(ValidationError):
            self.cuenta.extraer(Decimal('20000'))
```

Cada tipo de cuenta tiene sus propias reglas, y las pruebas las verifican. Si
alguien mañana confunde `CuentaAhorro` con `CuentaCorriente` en algún lado, el
test lo detecta.

## Testeando vistas

Para probar vistas, Django trae un **cliente de testing** que simula requests
HTTP sin necesidad de un navegador ni servidor corriendo. Se accede como
`self.client`.

**`banco/tests.py`**

```python
from django.urls import reverse




class HomeViewTest(TestCase):

    def test_home_devuelve_200(self):
        response = self.client.get(reverse('banco:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_muestra_titulo(self):
        response = self.client.get(reverse('banco:home'))
        self.assertContains(response, "Bienvenido al Banco UTN")
```

Explicación:

- **`self.client.get(url)`**: simula un pedido GET.
- **`response.status_code`**: el código HTTP de la respuesta (200 = OK, 404 = no
  encontrada, 302 = redirección).
- **`assertContains(response, texto)`**: verifica que el HTML devuelto contenga
  texto.

Otros métodos útiles:

- `self.client.post(url, data)` - pedido POST con datos.
- `self.client.login(username, password)` - logueá un usuario.
- `response.url` - a dónde redirigió (si hubo redirección).
- `response.context` - el diccionario de contexto que se pasó al template.

### Tests con autenticación

Muchas vistas requieren login. Django lo simula así:

```python
from django.contrib.auth.models import User




class MisCuentasViewTest(TestCase):

    def setUp(self):
        # Creamos usuario y persona vinculada
        self.usuario = User.objects.create_user(
            username='ana',
            password='clave123',
        )
        self.ana = PersonaFisica.objects.create(
            nombre="Ana",
            apellido="Pérez",
            dni="12345678",
            edad=32,
            usuario=self.usuario,
        )
        # Le creamos una cuenta
        self.cuenta = CuentaAhorro.objects.create(
            numero="001-100",
            titular=self.ana,
            cbu="0170123456789012345678",
            saldo=Decimal('5000'),
        )

    def test_usuario_no_logueado_es_redirigido(self):
        response = self.client.get(reverse('banco:mis_cuentas'))
        self.assertEqual(response.status_code, 302)
        # Debería redirigir a login
        self.assertIn('login', response.url)

    def test_usuario_logueado_ve_sus_cuentas(self):
        self.client.login(username='ana', password='clave123')

        response = self.client.get(reverse('banco:mis_cuentas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "001-100")

    def test_usuario_no_ve_cuentas_ajenas(self):
        # Creamos otro usuario y cuenta
        juan_user = User.objects.create_user(username='juan', password='clave456')
        juan = PersonaFisica.objects.create(
            nombre="Juan",
            apellido="López",
            dni="87654321",
            edad=45,
            usuario=juan_user,
        )
        cuenta_juan = CuentaAhorro.objects.create(
            numero="001-200",
            titular=juan,
            cbu="0170123456789012345679",
            saldo=Decimal('99999'),
        )

        # Ana intenta ver la cuenta de Juan
        self.client.login(username='ana', password='clave123')
        response = self.client.get(
            reverse('banco:detalle_cuenta', args=[cuenta_juan.numero])
        )

        # Debería ser rechazada
        self.assertEqual(response.status_code, 302)   # redirect
        # O si el sistema devuelve 403:
        # self.assertEqual(response.status_code, 403)
```

**Este test es crítico para la seguridad**: verifica que Ana no puede ver la
cuenta de Juan aunque sepa el número. Sin este test, un bug en la vista podría
abrir un agujero de datos privados sin que nadie lo note.

### Tests de vistas POST (operaciones)

Testeamos que las operaciones bancarias funcionan a través del formulario:

```python
class DepositoViewTest(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='ana',
            password='clave123',
        )
        self.ana = PersonaFisica.objects.create(
            nombre="Ana",
            apellido="Pérez",
            dni="12345678",
            edad=32,
            usuario=self.usuario,
        )
        self.cuenta = CuentaAhorro.objects.create(
            numero="001-100",
            titular=self.ana,
            cbu="0170123456789012345678",
            saldo=Decimal('5000'),
        )
        self.client.login(username='ana', password='clave123')

    def test_deposito_exitoso(self):
        response = self.client.post(
            reverse('banco:depositar', args=[self.cuenta.numero]),
            {'monto': '1000', 'descripcion': 'Test'}
        )

        # Debería redirigir al detalle de la cuenta
        self.assertEqual(response.status_code, 302)

        # El saldo debe estar actualizado
        self.cuenta.refresh_from_db()   # recargar desde la base
        self.assertEqual(self.cuenta.saldo, Decimal('6000'))

    def test_deposito_monto_invalido(self):
        response = self.client.post(
            reverse('banco:depositar', args=[self.cuenta.numero]),
            {'monto': '-100'}
        )

        # No redirige - vuelve a mostrar el formulario con error
        self.assertEqual(response.status_code, 200)

        # El saldo no cambió
        self.cuenta.refresh_from_db()
        self.assertEqual(self.cuenta.saldo, Decimal('5000'))
```

**`self.cuenta.refresh_from_db()`** es importante: después de que la vista
modificó el objeto en la base, el objeto en memoria queda desactualizado.
`refresh_from_db()` lo vuelve a cargar. Sin eso, `self.cuenta.saldo` sigue
mostrando el valor viejo.

## Fixtures: precargar datos

Muchas veces querés tener datos preexistentes para varios tests. En vez de
crearlos en cada `setUp`, podés usar **fixtures**: archivos JSON o YAML con
datos que Django carga automáticamente.

Generar un fixture a partir de la base actual:

```bash
python manage.py dumpdata banco.PersonaFisica banco.CuentaAhorro --indent=2 > banco/fixtures/datos_test.json
```

Después, en tu clase de test:

```python
class MiTest(TestCase):
    fixtures = ['datos_test']       # sin la extensión .json

    def test_algo(self):
        persona = PersonaFisica.objects.get(dni="12345678")
        ...
```

Django carga el fixture antes de cada test, así que los datos siempre están
disponibles.

**Para el manual usamos `setUp`** porque es más explícito y didáctico. Fixtures
son útiles cuando manejás muchos datos o cuando compartís el mismo conjunto
entre muchas suites.

## Testeando forms

Los formularios se testean directamente, sin pasar por vistas:

```python
from banco.forms import DepositoForm




class DepositoFormTest(TestCase):

    def test_form_valido(self):
        form = DepositoForm(data={'monto': '500', 'descripcion': 'Test'})
        self.assertTrue(form.is_valid())

    def test_monto_negativo_invalida(self):
        form = DepositoForm(data={'monto': '-100'})
        self.assertFalse(form.is_valid())
        self.assertIn('monto', form.errors)

    def test_monto_no_numerico_invalida(self):
        form = DepositoForm(data={'monto': 'abc'})
        self.assertFalse(form.is_valid())
```

Testear forms es rápido porque no requiere base de datos ni cliente HTTP. Solo
se valida la lógica del formulario en sí.

## Cobertura: qué se está probando

Un tema natural que aparece: *"¿estoy testeando todo, o me faltan casos?"*. La
**cobertura de código** es una métrica que mide qué porcentaje de tu código se
ejecuta durante los tests.

Se instala una herramienta llamada coverage:

```bash
pip install coverage
```

Y se corre:

```bash
coverage run --source='.' manage.py test
coverage report
```

Salida:

```text
Name                        Stmts   Miss Cover
-----------------------------------------------
banco/models.py               127      8   94%
banco/views.py                 98     22   78%
banco/forms.py                 45      3   93%
-----------------------------------------------
TOTAL                         270     33   88%
```

Te dice qué porcentaje del código está cubierto por tests. `coverage report -m`
muestra además **qué líneas exactas** no están cubiertas.

**¿Es cierto que hay que apuntar al 100%?** No siempre. Cobertura del 80-90%
es un buen objetivo. El 100% suele requerir esfuerzo desproporcionado en
código trivial. Lo importante es que **la lógica crítica** (operaciones
bancarias, seguridad, cálculos) esté completamente cubierta.

## Organizando los tests

Cuando el proyecto crece, `tests.py` se vuelve enorme. Django permite
convertirlo en un **paquete**: reemplazás el archivo por una carpeta con
`__init__.py`.

Estructura general hasta ahora, y lo nuevo (coloreado) recomendado:

![Diagrama en árbol de la estructura del proyecto. A la izquierda, la carpeta raíz "banco" (en rojo) de la que cuelgan: ".venv" (entorno virtual); "banco_utn" (configuración global del proyecto: __init__.py, settings.py, urls.py, asgi.py y wsgi.py, agrupados con una llave verde y la nota "Configuraciones (base de datos, apps, idioma…), ruteos, servidor"); la app principal "banco" (en rosa, "App principal, la lógica del banco"); "db.sqlite3" (nuestra base de datos) y "manage.py". La app "banco" contiene: __init__.py (indicador de paquete); un recuadro verde punteado "Núcleo de la app" con admin.py, urls.py, apps.py, models.py, forms.py, decorators.py y views.py; la carpeta "tests" (en rosa, lo nuevo recomendado) con __init__.py, test_models.py, test_views.py, test_forms.py y test_auth.py (en violeta); la carpeta "migrations" con __init__.py, 0001_initial.py y 0002_persona_usuario.py ("Lo generado al hacer las migraciones: el 0001 cuando armaste los modelos, el 0002 al vincular user"); la carpeta "templates" ("Lo que ve el usuario") con la subcarpeta "banco" (base.html, home.html, listar_cuentas.html, detalle_cuenta.html, listar_personas.html, detalle_persona.html, formulario_operacion.html, registrarse.html) y la subcarpeta "registration" (login.html); y la carpeta "static" con "banco" y dentro css/estilo.css, img/logo.png y js/custom.js. Abajo a la izquierda, un recuadro rojo dice: "En este punto, RECONOCE y MEMORIZATE esta estructura. Decilo en voz alta para fijarlo".](images/cap22-estructura-proyecto-con-tests.png)

Cada archivo agrupa tests por tipo. Django encuentra todos los archivos que
empiezan con `test_*` automáticamente.

Para el manual, mantengamos `tests.py` como archivo único, pero el patrón de
organización es bueno de conocer.

## Un vistazo a pytest-django

Django trae su framework de test, pero en la comunidad Python moderna hay una
alternativa muy popular: **pytest**. Con pytest-django, se puede escribir el
mismo tipo de tests con una sintaxis más limpia:

tests con pytest-django (solo para comparar)

```python
import pytest
from banco.models import PersonaFisica




@pytest.mark.django_db
def test_crear_persona():
    persona = PersonaFisica.objects.create(
        nombre="Ana",
        apellido="Pérez",
        dni="12345678",
        edad=32,
    )
    assert persona.nombre == "Ana"
    assert str(persona) == "Ana (DNI 12345678)"
```

Ventajas de pytest:

- Sintaxis más clara (funciones en vez de clases, `assert` normal).
- Fixtures más potentes (equivalentes al `setUp`, pero reutilizables).
- Mejor salida en fallos.
- Muchas librerías compatibles (pytest-cov, pytest-mock).

En proyectos reales modernos, **pytest se usa más que el framework nativo**.
Para el manual mostramos el framework de Django (por ser el default), pero
saber que pytest existe es importante - es lo que van a ver en muchas
empresas.

## Buenas prácticas de testing

1. **Cada test es independiente.** Nunca dependas del estado que dejó otro
   test. Django ya se encarga de esto (base de datos limpia entre tests), pero
   mantené la disciplina.
2. **Un test, una hipótesis.** No metas tres verificaciones distintas en un
   mismo test. Si algo falla, tenés que poder identificar exactamente qué es.
3. **Nombres descriptivos.** `test_deposito_negativo_lanza_error` es mucho mejor
   que `test_deposito_2`. El nombre del test debería resumir la hipótesis.
4. **AAA es tu amigo.** Arrange, Act, Assert. En ese orden. Si un test tiene
   100 líneas antes del "Act", probablemente esté probando demasiado.
5. **Testeá el comportamiento, no la implementación.** Verificá **qué hace** el
   código, no **cómo lo hace**. Si el test se rompe con cualquier refactor
   interno, está mal escrito.
6. **Datos mínimos y explícitos.** No cargues fixtures gigantes solo para
   probar una funcionalidad chica. Usá lo mínimo indispensable, así los tests
   son legibles.
7. **Los tests son documentación.** Un test bien escrito le muestra a un
   programador nuevo cómo se supone que debe usarse una función.
   `test_deposito_negativo_lanza_error` documenta que "no se puede depositar
   valores negativos".
8. **Los tests son parte del código, no un extra.** Se commitean junto con el
   código. Si un feature no tiene tests, no está completo. Es la mentalidad
   estándar en la industria.
9. **Corré los tests antes de commitear.** Si los tests fallan, corregí el bug
   antes de subir el código. Con un pre-commit hook (algo que aprenderán
   después), esto se puede automatizar.
10. **Cuando aparece un bug, primero escribí un test que lo reproduzca.**
    Después arreglás el bug y verificás que el test pase. Así te garantizás que
    el bug **no va a volver**.

## Ejecución continua: CI

Un tema que solo tocamos al pasar: en proyectos profesionales, los tests se
ejecutan automáticamente en cada push al repositorio. Esto se hace con
servicios de **Continuous Integration** (CI): GitHub Actions, GitLab CI,
CircleCI, entre otros. El flujo es:

1. Programador hace `git push` a una rama.
2. El servicio de CI detecta el push.
3. Levanta un entorno limpio.
4. Instala dependencias.
5. Corre `python manage.py test`.
6. Si todo pasa, aprueba el push. Si falla, notifica al equipo.

Todo esto pasa **sin intervención humana**. Es la razón por la que grandes
proyectos con 500 programadores no explotan: los tests son la red de seguridad
que detecta problemas antes de que lleguen a producción.

Configurar CI está fuera del alcance del manual, pero es una habilidad que van
a aprender rápido cuando se sumen a un equipo profesional.

![Infografía "Integración continua (CI): Los tests se ejecutan automáticamente en cada push". Arriba, de izquierda a derecha: el "Desarrollador" frente a una laptop con una terminal que muestra git push; flecha punteada al "Servicio de CI" (GitHub Actions, GitLab CI y CircleCI); flecha punteada al "Resultado" (TODO OK: el push es aprobado; FALLO: se notifica al equipo); y el "Equipo", tres personas con una alerta. En el medio, seis pasos numerados: 1 Push al repositorio (git add ., git commit -m "Nueva funcionalidad", git push origin main); 2 CI detecta el push (el servicio de CI se activa ante el push); 3 Entorno limpio (levanta un entorno nuevo y aislado); 4 Instala dependencias (pip install -r requirements.txt); 5 Corre los tests (python manage.py test, con salida OK (123 tests)); 6 Resultado (tilde verde y cruz roja: si todo pasa, aprueba el push; si falla, notifica al equipo). Abajo, un recuadro "¿Por qué es importante?" con tres puntos (detecta errores rápido, evita romper el código compartido, da confianza para hacer cambios) y la secuencia Código, Push, CI, Tests, Resultado.](images/cap22-integracion-continua-ci.jpg)

## Un cierre y una vuelta atrás

En el capítulo 14, cuando cerramos SOLID, usamos `assert` como un anticipo de
testing. Esos asserts verificaban principios de diseño: que las subclases
respetaran LSP, que agregar clases nuevas no rompiera OCP. Eran **tests, sin
usar frameworks**.

En este capítulo, esos mismos principios se transforman en tests reales:

- **LSP**: `test_cuenta_ahorro_se_comporta_como_cuenta`,
  `test_cuenta_corriente_se_comporta_como_cuenta`.
- **OCP**: `test_agregar_cuenta_sueldo_no_rompe_transferencias`.
- **Validaciones del capítulo 10**: `test_deposito_negativo_falla`,
  `test_dni_debe_ser_numerico`.

**Todo lo que hiciste desde el capítulo 9 con clases, encapsulamiento,
herencia, SOLID - ahora tiene una red de seguridad automática.** Si en dos
meses cambian algo y accidentalmente rompen una regla vieja, los tests van a
avisarte al instante.

Ese es el ciclo profesional: diseñás con OO, implementás con framework,
verificás con tests. Los tres pilares se sostienen mutuamente.

En el próximo capítulo **De SQLite a PostgreSQL**, vamos a hacer un cambio
importante: migrar la base de datos del banco desde SQLite (el default,
pensado para desarrollo) a PostgreSQL (el motor profesional). Vas a ver una de
las mejores promesas del ORM cumplida: **cambiar de motor de base de datos sin
cambiar una línea del código de la aplicación**. Todo lo que escribiste hasta
acá va a seguir funcionando igual, contra un motor más robusto y adecuado para
producción.
