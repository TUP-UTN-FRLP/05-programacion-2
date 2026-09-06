# POO: Composición y gestión de colecciones (ABM/CRUD)

_Cuando los objetos colaboran._

## ¿Por qué leemos este capítulo?

Los capítulos anteriores nos enseñaron a construir objetos que se defienden
solos (encapsulamiento) y a organizarlos en jerarquías (herencia). Pero un
objeto solo es poca cosa. Los sistemas reales están hechos de muchos objetos
que se comunican entre sí: un banco que gestiona cuentas, una cuenta que
registra movimientos, un movimiento que referencia a un cajero. Ninguno vive
aislado.

Este capítulo te da las herramientas para conectar objetos entre sí. Vas a
ver:

- **Composición**: cuando un objeto tiene otros objetos adentro. Es la
  contracara de la herencia: donde ésta modela "es un", la composición modela
  "tiene un".
- **Colecciones de objetos**: una clase que mantiene por dentro una lista o
  un diccionario de otros objetos, y expone operaciones sobre esa colección.
- **El patrón ABM/CRUD**: la forma estándar de gestionar colecciones, con
  operaciones para dar de alta, consultar, modificar y dar de baja.
- **Organización en módulos**: cuando el proyecto crece, cortar en varios
  archivos deja de ser un lujo y pasa a ser necesidad.
- **Un primer vistazo a SRP**: la idea de que cada clase debe tener una sola
  razón para cambiar.

Al final del capítulo armamos la iteración 4 del banco, la más ambiciosa del
proyecto: aparece la clase `Banco` con ABM completo, la clase `Movimiento`
que registra el historial, y el sistema queda dividido en módulos, como en un
proyecto real. Cuando lleguen a Django van a reconocer esta estructura casi
al pie de la letra.

> **Una nota antes de empezar.** De acá en adelante vas a ver que el código
> de prueba de cada ejemplo va dentro de `if __name__ == "__main__":`. Ya lo
> venías viendo desde el capítulo 9; en la sección de módulos de este mismo
> capítulo explicamos por fin qué significa exactamente. Por ahora leelo como
> "esto solo corre si ejecuto este archivo directamente".

## Composición: "tiene un" en lugar de "es un"

En el capítulo anterior vimos que la **herencia** responde a la pregunta
"¿A es un B?". Una `CuentaAhorro` es una `Cuenta`. Un `Auto` es un
`Vehiculo`.

La **composición** responde a otra pregunta: "¿A tiene un B?". Una `Cuenta`
tiene un titular. Una `Empresa` tiene empleados. Un `Auto` tiene un `Motor` y
cuatro `Ruedas`. Estas relaciones no se modelan con herencia: se modelan
haciendo que un objeto sea atributo de otro.

Ya vimos composición en el capítulo 10 sin nombrarla, cuando la `Cuenta`
guardó una `Persona` como titular:

```python
ana = Persona("Ana", "Pérez", "12345678")
cuenta = Cuenta("001-234", ana, 1000)     # Ana vive adentro de la cuenta
```

El titular de la cuenta no es un string ni un número: es un objeto `Persona`
completo, con sus propios atributos y métodos. La cuenta lo tiene, y puede
consultarlo a través de los métodos de `Persona`:

```python
print(cuenta.resumen())     # [001-234] Pérez, Ana - $1000
```

Fijate que no escribimos `cuenta._titular.dni`. El titular es interno a la
cuenta, y el mundo de afuera le pregunta a la cuenta, no le revuelve los
atributos. Eso vale igual que en el capítulo 10: la composición no suspende
el encapsulamiento.

### Delegación: el mecanismo cotidiano de la composición

Mirá cómo se arma `Cuenta.resumen()`:

```python
class Cuenta:
    def __init__(self, numero, titular, saldo):
        self._numero = numero
        self._titular = titular
        self._saldo = saldo

    def resumen(self):
        return f"[{self._numero}] {self._titular} - ${self._saldo}"
```

`{self._titular}` invoca el `__str__` de `Persona`. La cuenta **no sabe** cómo
se formatea el nombre de una persona, ni le importa: le pasa la pelota al
objeto que sí sabe. Eso se llama **delegación**, y es el mecanismo que hace
funcionar a la composición. Si mañana `Persona` cambia el formato de su
`__str__`, `Cuenta` se entera sola.

Regla que vale para todo el capítulo: **cada objeto calcula lo suyo y le pide
el resto al que corresponde.** Si te encontrás escribiendo la lógica del
objeto contenido dentro del contenedor, algo está mal repartido.

### Composición vs. herencia: la elección de diseño

Los alumnos que recién ven POO tienden a usar herencia para todo. Cada vez
que dos clases se parecen quieren declarar que una hereda de la otra. Es un
error clásico: muchas relaciones que parecen jerárquicas son en realidad de
composición.

Ejemplo típico: alguien dice "un `Empleado` tiene una `Empresa` donde
trabaja, entonces `Empleado` hereda de `Empresa`". Está mal, y la prueba del
"es un" lo revela: ¿un empleado es una empresa? No. Un empleado trabaja en
una empresa. Composición.

Otra prueba práctica: si podés cambiar la relación después de crear el
objeto, es composición. Un empleado puede cambiar de empresa en su vida; una
caja de ahorro no puede pasar a ser cuenta corriente. Lo primero es
composición, lo segundo herencia.

| Relación | Herramienta | Ejemplo |
|---|---|---|
| Es un | Herencia | `CuentaAhorro` es una `Cuenta` |
| Tiene un | Composición | `Cuenta` tiene un titular |
| Usa un | Composición | `Motor` usa un combustible |
| Está compuesto por | Composición (lista) | `Empresa` tiene empleados |

> **Cuando dudes, gana la composición.** Es más flexible, permite cambiar la
> relación en tiempo de ejecución y no impone la rigidez de una jerarquía.

### Composición y agregación: quién le pertenece a quién

Dentro del "tiene un" conviene distinguir dos casos, porque en UML tienen
nombres distintos y en el diseño tienen consecuencias distintas.

**Composición** (en sentido estricto): la parte **no existe sin el todo** y
le pertenece en exclusiva. Un `Motor` pertenece a un solo `Auto`; si el auto
se destruye, ese motor deja de tener sentido en el modelo. Un `Movimiento`
pertenece a una sola `Cuenta`. Típicamente el objeto contenido **se crea
adentro** del contenedor:

```python
class Cuenta:
    def depositar(self, monto):
        self._saldo += monto
        self._movimientos.append(Movimiento("depósito", monto, self._saldo))
        #                        ^ el movimiento nace acá adentro
```

**Agregación**: la parte **existe por su cuenta** y puede ser compartida. Una
`Direccion` puede vivir dentro de una `Persona`, de un `Comercio` o de las
dos a la vez. Un `Alumno` existe aunque el `Curso` se cierre. Típicamente el
objeto contenido **se crea afuera y se pasa por parámetro**:

```python
ana = Persona("Ana", "Pérez", "12345678")
cuenta = Cuenta("001-234", ana, 1000)     # Ana ya existía
```

La pista práctica está en el constructor: si el contenedor recibe el objeto
ya hecho, es agregación; si lo fabrica adentro, es composición. No es una
distinción burocrática: determina si podés compartir el objeto sin romper
nada, que es justo el tema de la sección siguiente.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 1** — Modelá una `Casa` que tiene un objeto `Direccion` como
> atributo (calle, número, ciudad). Después imprimí la casa incluyendo la
> dirección completa. No uses herencia: una `Casa` no es una dirección, tiene
> una.
>
> El código de este ejercicio está resuelto en `ejercicio_01.py`.

```python
class Direccion:
    """Dirección postal, pensada para vivir dentro de otras clases."""

    def __init__(self, calle, numero, ciudad):
        self._calle = calle
        self._numero = numero
        self._ciudad = ciudad

    def __str__(self):
        return f"{self._calle} {self._numero}, {self._ciudad}"


class Casa:
    """Casa compuesta por un objeto Direccion."""

    def __init__(self, dueno, direccion):
        self._dueno = dueno
        self._direccion = direccion

    def __str__(self):
        return f"Casa de {self._dueno} en {self._direccion}"


if __name__ == "__main__":
    direccion = Direccion("Av. 7", 1234, "La Plata")
    casa = Casa("Ana Perez", direccion)

    print(casa)      # Casa de Ana Perez en Av. 7 1234, La Plata
```

`Direccion` es una clase independiente y `Casa` la usa por agregación. La
misma `Direccion` podría vivir dentro de una `Persona`, un `Comercio` o
cualquier otra clase que necesite ubicación. Ese es el poder de la
composición: reutilización sin jerarquía.

---

## Referencias entre objetos y sus consecuencias

Un detalle importante cuando trabajás con composición: cuando un objeto
guarda a otro como atributo, **no lo copia, lo referencia**. Los dos apuntan
al mismo objeto en memoria.

```python
familiar = Direccion("Av. 7", 1234, "La Plata")

madre = Persona("Ana", familiar)
hijo = Persona("Pedro", familiar)     # la misma Direccion en los dos
```

`madre` y `hijo` no tienen cada uno "su" dirección: tienen **la misma**.
Cuando esa dirección cambia, cambia para los dos:

```python
familiar.mudar("Calle 50", 900)

print(madre)     # Ana: Calle 50 900, La Plata
print(hijo)      # Pedro: Calle 50 900, La Plata
```

En el mundo real esto **suele ser lo que querés**: si la familia se muda, las
dos personas deberían ver la dirección nueva. Pero hay que entenderlo,
porque el bug clásico es el opuesto: modificar un objeto creyendo que se
trabajaba con una copia y descubrir que se modificó en cinco lugares más.

Es el mismo modelo de "etiquetas apuntando a objetos" que vimos en el
capítulo 2. En composición se hace visible.

### Cuándo importa, y cómo se resuelve

Compartir referencias es cómodo mientras el objeto compartido sea estable
(una dirección, una categoría, un titular). Se vuelve un problema cuando
cambia seguido y no todos los que lo referencian quieren esos cambios. Ahí la
salida es copiar, y acá hay que ser preciso:

```python
import copy

lista_b = lista_a.copy()               # copia SUPERFICIAL
independiente = copy.deepcopy(objeto)  # copia PROFUNDA
```

`list.copy()`, que vimos en el capítulo de colecciones, crea una lista nueva
pero **con las mismas referencias adentro**. Si la lista tiene objetos,
seguís compartiendo los objetos: sirve para que agregar o quitar elementos en
una lista no afecte a la otra, y no sirve para nada si lo que querés es que
los objetos sean independientes.

Para eso está `copy.deepcopy()`, que copia el objeto y, recursivamente, todo
lo que tiene adentro. Es más caro, así que se usa solo cuando de verdad
necesitás dos objetos que evolucionen por separado.

> **En una frase.** `copy()` copia el contenedor; `deepcopy()` copia el
> contenido. El problema de las referencias compartidas solo lo resuelve el
> segundo.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 2** — Creá una sola `Direccion` y dos `Persona` que la
> compartan. Mudá la dirección y comprobá que las dos personas ven el cambio.
> Después hacé lo mismo con `copy.deepcopy` y verificá que ahí sí quedan
> independientes.
>
> El código de este ejercicio está resuelto en `ejercicio_02.py`.

```python
import copy


class Direccion:
    """Dirección postal que puede cambiar de valores."""

    def __init__(self, calle, numero, ciudad):
        self._calle = calle
        self._numero = numero
        self._ciudad = ciudad

    def mudar(self, calle, numero):
        """Cambia calle y número conservando la ciudad."""
        self._calle = calle
        self._numero = numero

    def __str__(self):
        return f"{self._calle} {self._numero}, {self._ciudad}"


class Persona:
    """Persona que tiene una Direccion."""

    def __init__(self, nombre, direccion):
        self._nombre = nombre
        self._direccion = direccion

    def __str__(self):
        return f"{self._nombre}: {self._direccion}"


if __name__ == "__main__":
    familiar = Direccion("Av. 7", 1234, "La Plata")

    madre = Persona("Ana", familiar)
    hijo = Persona("Pedro", familiar)

    familiar.mudar("Calle 50", 900)

    print(madre)      # Ana: Calle 50 900, La Plata
    print(hijo)       # Pedro: Calle 50 900, La Plata

    independiente = Persona("Lucía", copy.deepcopy(familiar))
    familiar.mudar("Diagonal 74", 55)

    print(madre)            # Ana: Diagonal 74 55, La Plata
    print(independiente)    # Lucía: Calle 50 900, La Plata
```

Lucía se quedó con la dirección vieja porque su `Direccion` es otro objeto.
Ana siguió al objeto original.

---

## Colecciones de objetos

Un objeto puede tener **una lista o un diccionario de otros objetos** como
atributo. Esta es la forma más común de composición en sistemas reales.
Ejemplo clásico: una biblioteca tiene libros.

```python
class Libro:
    """Libro con título, autor e ISBN."""

    def __init__(self, isbn, titulo, autor):
        self._isbn = isbn
        self._titulo = titulo
        self._autor = autor

    def isbn(self):
        """Devuelve el ISBN del libro."""
        return self._isbn

    def __str__(self):
        return f"'{self._titulo}' de {self._autor}"


class Biblioteca:
    """Biblioteca que administra una colección de libros."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._libros = []            # colección interna

    def agregar_libro(self, libro):
        """Suma un libro al catálogo."""
        self._libros.append(libro)

    def cantidad_libros(self):
        """Devuelve cuántos libros hay en el catálogo."""
        return len(self._libros)

    def listar_libros(self):
        """Imprime el catálogo completo."""
        for libro in self._libros:
            print(f"  - {libro}")
```

Uso:

```python
biblio = Biblioteca("Biblioteca Central")
biblio.agregar_libro(Libro("978-987-1", "El Aleph", "Borges"))
biblio.agregar_libro(Libro("978-987-2", "Rayuela", "Cortázar"))
biblio.agregar_libro(Libro("978-987-3", "Ficciones", "Borges"))

print(f"Total: {biblio.cantidad_libros()}")
biblio.listar_libros()

# Total: 3
#   - 'El Aleph' de Borges
#   - 'Rayuela' de Cortázar
#   - 'Ficciones' de Borges
```

Fijate qué pasó:

- `Biblioteca` guarda internamente `_libros` como una lista de objetos
  `Libro`.
- `agregar_libro`, `cantidad_libros` y `listar_libros` son **operaciones
  sobre la colección**.
- El acceso a los libros pasa siempre por los métodos de la biblioteca. Nadie
  de afuera modifica `_libros` directamente.

Este patrón —un objeto "gestor" que mantiene una colección de otros objetos y
expone métodos para operar sobre ella— es la base del sistema que vamos a
construir al final del capítulo.

### Diccionario en vez de lista

Cuando cada objeto de la colección tiene un identificador único, usar un
**diccionario** en lugar de una lista es mucho más eficiente para buscar:

```python
class Biblioteca:
    def __init__(self, nombre):
        self._nombre = nombre
        self._libros = {}            # {isbn: libro}

    def agregar_libro(self, libro):
        self._libros[libro.isbn()] = libro
```

Con un diccionario, buscar por ISBN es prácticamente instantáneo aunque haya
miles de libros; con una lista habría que recorrerla entera. Esta elección
—lista o diccionario para la colección interna— es una decisión de diseño que
vale la pena tomar conscientemente.

Ojo con un efecto secundario: `self._libros[libro.isbn()] = libro` **pisa en
silencio** un libro que ya estuviera con ese ISBN. Con una lista tendrías dos
copias; con un diccionario, la segunda tapa a la primera y nadie se entera.
Ninguno de los dos comportamientos suele ser el deseado, y por eso el patrón
ABM que viene enseguida empieza siempre por rechazar los duplicados.

### Buscar: ¿devolver `None` o lanzar excepción?

Cuando escribís un método de búsqueda tenés dos opciones y hay que elegir una
a conciencia, porque el que use tu clase va a programar según lo que
prometas:

```python
def buscar_por_isbn(self, isbn):
    return self._libros.get(isbn)          # devuelve None si no está


def buscar_por_isbn(self, isbn):
    libro = self._libros.get(isbn)
    if libro is None:
        raise LibroNoEncontrado(f"No hay libro con ISBN {isbn}")
    return libro                            # nunca devuelve None
```

Criterio práctico:

- **Lanzá excepción** cuando no encontrar el objeto es un **error**: el
  usuario pidió modificar, cobrar o dar de baja algo que debería existir. Así
  el problema estalla en el lugar donde se produjo, con un mensaje claro.
- **Devolvé `None`** cuando la ausencia es un **resultado legítimo**: estás
  preguntando si algo existe. En ese caso el nombre del método debería
  avisarlo (`buscar_si_existe`, `obtener_o_none`) y quien lo llama está
  obligado a chequear.

El peor de los mundos es mezclar los dos criterios sin avisar, que es como se
producen los `AttributeError: 'NoneType' object has no attribute...`. En este
capítulo adoptamos una convención y la sostenemos: **todo método que se llame
`buscar_algo()` lanza excepción si no encuentra.**

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 3** — Modelá una clase `Curso` que tiene un nombre y una lista
> de `Alumno` (nombre, legajo). Métodos: `inscribir(alumno)`,
> `cantidad_inscriptos()` y `listar_alumnos()`.
>
> El código de este ejercicio está resuelto en `ejercicio_03.py`.

```python
class Alumno:
    """Alumno identificado por nombre y legajo."""

    def __init__(self, nombre, legajo):
        self._nombre = nombre
        self._legajo = legajo

    def __str__(self):
        return f"[{self._legajo}] {self._nombre}"


class Curso:
    """Curso que contiene una colección de alumnos."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._alumnos = []

    def inscribir(self, alumno):
        """Agrega un alumno a la lista de inscriptos."""
        self._alumnos.append(alumno)

    def cantidad_inscriptos(self):
        """Devuelve cuántos alumnos hay inscriptos."""
        return len(self._alumnos)

    def listar_alumnos(self):
        """Imprime todos los alumnos inscriptos."""
        for alumno in self._alumnos:
            print(f"  {alumno}")

    def __str__(self):
        return (
            f"Inscriptos en {self._nombre}: "
            f"{self.cantidad_inscriptos()}"
        )


if __name__ == "__main__":
    curso = Curso("Programación 2")
    curso.inscribir(Alumno("Ana", "L-001"))
    curso.inscribir(Alumno("Juan", "L-002"))
    curso.inscribir(Alumno("Pedro", "L-003"))

    print(curso)
    curso.listar_alumnos()
```

Notá que el nombre del curso se muestra con `__str__` y no leyendo
`curso._nombre` desde afuera. Es un atributo interno como cualquier otro.

---

## Organizando el proyecto: módulos e imports

Antes de meternos con el ABM y con el proyecto grande hay que resolver un
problema práctico: **el archivo se está volviendo demasiado largo**. Ya en la
iteración 3 del banco tenemos siete clases (`Persona`, `PersonaFisica`,
`PersonaJuridica`, `Cuenta`, `CuentaAhorro`, `CuentaCorriente` y las
excepciones). En la iteración 4 vamos a sumar más. Todo en un solo
`banco.py` empieza a ser inmanejable.

La solución es cortar el proyecto en varios archivos, cada uno con su propia
responsabilidad. Cada archivo `.py` es un **módulo** de Python.

### Qué es un módulo

Un módulo es cualquier archivo Python. No hay que declarar nada especial:
cuando creás `mi_archivo.py` con código adentro, ya es un módulo. La
diferencia es cómo lo usás: podés **ejecutarlo directamente**
(`python mi_archivo.py`) o **importarlo desde otro archivo** para usar las
clases y funciones que define.

### `import`: usar código de otro archivo

Supongamos que tenés dos archivos. **`validaciones.py`**:

```python
def es_dni_valido(dni):
    """Indica si el DNI es una cadena de 7 u 8 dígitos."""
    return (
        isinstance(dni, str)
        and dni.isdigit()
        and len(dni) in (7, 8)
    )
```

**`main.py`**, en la misma carpeta:

```python
import validaciones

dni = input("DNI: ")

if validaciones.es_dni_valido(dni):
    print("DNI OK")
else:
    print("DNI inválido")
```

`import validaciones` le dice a Python: *"cargá el archivo `validaciones.py`
como módulo con ese nombre"*. Después accedés a lo que define prefijando el
nombre del módulo: `validaciones.es_dni_valido(...)`.

### `from ... import ...`: traer nombres específicos

Si querés usar la función sin el prefijo, importás el nombre directamente:

```python
from validaciones import es_dni_valido

if es_dni_valido(dni):
    print("DNI OK")
```

La sintaxis general es `from modulo import nombre1, nombre2, ...`, y también
sirve para traer varios de una vez:

```python
from validaciones import es_dni_valido, es_cuit_valido, normalizar_nombre
```

¿Cuándo usar cada forma?

- **`import modulo`**: cuando vas a usar varios nombres del módulo, o cuando
  el prefijo hace más claro de dónde viene lo que estás usando. Ejemplo:
  `math.pi`, `math.sqrt(x)`. Ves inmediatamente que vienen de `math`.
- **`from modulo import nombre`**: cuando vas a usar uno o dos nombres
  específicos y el prefijo sería ruido. Ejemplo:
  `from datetime import datetime`.

Tanto `import` como `from ... import` van al principio del archivo, todos
juntos, como pide PEP 8. Nunca adentro de una función o de un método.

### `if __name__ == "__main__":`

Ahora sí, cumplimos la promesa del capítulo 9. `__name__` es una variable
especial que Python define automáticamente en cada módulo, y su valor depende
de cómo se ejecuta el archivo:

- **Si el archivo se ejecutó directamente** (`python banco.py`), `__name__`
  vale `"__main__"`.
- **Si el archivo fue importado por otro** (`import banco`), `__name__` vale
  `"banco"`, el nombre del módulo.

Entonces `if __name__ == "__main__":` significa exactamente: *"esto que va
adentro solo se ejecuta si soy el archivo principal, no si me importan desde
otro lado"*.

¿Para qué sirve? Para separar el **código de prueba** del **código que otros
van a importar**. **`cuentas.py`**, que define la clase:

```python
class Cuenta:
    """Cuenta con titular y saldo."""

    def __init__(self, titular, saldo):
        self._titular = titular
        self._saldo = saldo

    def __str__(self):
        return f"{self._titular}: ${self._saldo}"


if __name__ == "__main__":
    # Estas líneas SOLO se ejecutan si corro "python cuentas.py".
    # Si otro archivo hace "from cuentas import Cuenta", no corren.
    print(Cuenta("Prueba", 100))
```

**`main.py`**, que usa la clase:

```python
from cuentas import Cuenta

mi_cuenta = Cuenta("Ana", 5000)
print(mi_cuenta)
```

Al importar `cuentas.py`, la sección de prueba de arriba no se ejecuta. Sin
el `if __name__ == "__main__":`, esas líneas correrían **cada vez que alguien
importa el módulo**, contaminando la salida del programa principal con
pruebas que nadie pidió.

### Estructura típica de un proyecto Python chico

Cuando un proyecto crece se corta en archivos con responsabilidades
separadas. La organización que vamos a usar en el banco:

```
banco/
├── errores.py       # las excepciones propias del dominio
├── personas.py      # Persona, PersonaFisica, PersonaJuridica
├── movimientos.py   # Movimiento
├── cuentas.py       # Cuenta, CuentaAhorro, CuentaCorriente
├── banco.py         # Banco: el ABM de cuentas
├── validaciones.py  # es_dni_valido, es_cuit_valido, ...
└── main.py          # el programa que usa todo lo anterior
```

Cada archivo importa lo que necesita de los otros:

```python
# cuentas.py
from errores import MontoInvalidoError, SaldoInsuficienteError
from movimientos import Movimiento
from personas import Persona


class Cuenta:
    ...
```

Notá la dirección de las flechas: `cuentas.py` importa de `errores.py` y de
`movimientos.py`, pero ninguno de esos dos importa de `cuentas.py`. Las
dependencias van en un solo sentido, de lo general a lo particular. Si dos
módulos se importan mutuamente, Python protesta con un error de importación
circular, y casi siempre es señal de que las responsabilidades quedaron mal
repartidas.

![Diagrama de dependencias entre los módulos del banco: main.py arriba importa
a banco.py y a personas.py; banco.py importa a cuentas.py y a errores.py;
cuentas.py importa a personas.py, movimientos.py y errores.py. Las cajas
personas.py, movimientos.py y errores.py no importan a nadie del proyecto: son
la base. validaciones.py queda como módulo suelto, listo para reusar. Todas las
flechas apuntan hacia abajo, en un solo sentido; si se cerraran en círculo
Python cortaría con un error de importación circular](images/estructura-modulos-banco.png)

Esta separación tiene beneficios enormes:

- Editás archivos chicos y manejables.
- Encontrás las cosas rápido: si buscás la lógica de una cuenta, vas a
  `cuentas.py`; si buscás las validaciones, a `validaciones.py`.
- Podés reusar módulos entre proyectos: `validaciones.py` sirve tal cual en
  otro sistema que también valide DNIs y CUITs.
- Cuando lleguen a Django esta estructura les va a resultar familiar. Django
  obliga a separar en `models.py`, `views.py`, `forms.py`, etc.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 4** — Escribí un módulo de validaciones con `es_dni_valido(dni)`
> y `normalizar_nombre(nombre)`, y poné toda la prueba dentro de
> `if __name__ == "__main__":`. Imprimí el valor de `__name__` para ver la
> diferencia entre ejecutar el archivo e importarlo.
>
> El código de este ejercicio está resuelto en `ejercicio_04.py`.

```python
def es_dni_valido(dni):
    """Indica si el DNI es una cadena de 7 u 8 dígitos."""
    return (
        isinstance(dni, str)
        and dni.isdigit()
        and len(dni) in (7, 8)
    )


def normalizar_nombre(nombre):
    """Devuelve el nombre sin espacios sobrantes y capitalizado."""
    return nombre.strip().title()


if __name__ == "__main__":
    print(f'__name__ vale "{__name__}"')

    for dni in ["12345678", "1234", "12a45678", 12345678]:
        print(f"  {dni!r}: {es_dni_valido(dni)}")

    print(normalizar_nombre("  ana maría pérez  "))
```

Probalo de las dos formas. Ejecutado directamente imprime
`__name__ vale "__main__"` y corre todas las pruebas. Si desde otro archivo
hacés `import ejercicio_04`, no imprime nada: las funciones quedan
disponibles y la prueba no molesta.

---

## El patrón ABM/CRUD

Ahora sí, el tema central del capítulo. Cuando tenés una colección de
objetos, generalmente necesitás las mismas cuatro operaciones básicas para
gestionarla:

| Operación | En inglés | Qué hace |
|---|---|---|
| **A**lta | **C**reate | Agregar un objeto nuevo |
| Consulta | **R**ead | Buscar y listar objetos |
| **M**odificación | **U**pdate | Cambiar los datos de un objeto |
| **B**aja | **D**elete | Eliminar un objeto existente |

En español lo llamamos **ABM** (Alta, Baja, Modificación); en inglés se
conoce como **CRUD** (Create, Read, Update, Delete). Son lo mismo: el ABM
tradicionalmente da por supuesta la lectura, y CRUD la hace explícita como
cuarta operación. Las vas a ver mencionadas indistintamente en
documentación, en trabajos y en Django.

Cualquier sistema que administre entidades (usuarios, productos, alumnos,
cuentas, pedidos) implementa este patrón.

### Estructura de una clase gestora

Una clase que implementa ABM sigue casi siempre este esqueleto:

```python
class Gestor:
    def __init__(self):
        self._elementos = {}      # o lista, según el caso

    # --- Alta / Create ---
    def crear(self, datos):
        ...

    # --- Consulta / Read ---
    def buscar(self, identificador):
        ...

    def listar(self):
        ...

    # --- Modificación / Update ---
    def actualizar(self, identificador, datos):
        ...

    # --- Baja / Delete ---
    def eliminar(self, identificador):
        ...
```

Los nombres exactos varían por dominio: `crear_cuenta`, `abrir_cuenta`,
`dar_de_alta`, todos válidos. Lo importante es que las cuatro operaciones
estén y sean identificables.

Y hay una pieza que se repite en los cuatro: **encontrar el elemento o
fallar**. Escribila una sola vez en `buscar()` y que las demás la usen. Si
`actualizar()` y `eliminar()` repiten el `if identificador not in ...`, ya
tenés la misma regla en tres lugares y el día que cambie vas a arreglar dos
de tres.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 5** — Implementá un gestor de productos con ABM completo. Cada
> `Producto` tiene código, nombre, precio y stock. Usá un diccionario interno
> en `Almacen`, con alta, consulta, listado, actualización de precio,
> reposición de stock y baja. Creá excepciones propias para código duplicado y
> producto no encontrado, y reutilizá `buscar()` en los métodos que lo
> necesiten.
>
> El código de este ejercicio está resuelto en `ejercicio_05.py`.

```python
class ProductoNoEncontrado(Exception):
    """Indica que no existe el producto solicitado."""

    pass


class CodigoDuplicadoError(Exception):
    """Indica que el código del producto ya existe."""

    pass


class Producto:
    """Producto identificado por un código."""

    def __init__(self, codigo, nombre, precio, stock):
        self._codigo = codigo
        self._nombre = nombre
        self._precio = precio
        self._stock = stock

    def cambiar_precio(self, nuevo_precio):
        """Actualiza el precio de venta."""
        if nuevo_precio <= 0:
            raise ValueError("El precio debe ser positivo")

        self._precio = nuevo_precio

    def reponer(self, cantidad):
        """Suma unidades al stock disponible."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")

        self._stock += cantidad

    def __str__(self):
        return (
            f"[{self._codigo}] {self._nombre} - "
            f"${self._precio} (stock: {self._stock})"
        )


class Almacen:
    """Gestiona un ABM de productos indexados por código."""

    def __init__(self):
        self._productos = {}

    # --- Alta ---
    def dar_de_alta(self, codigo, nombre, precio, stock):
        """Da de alta un producto nuevo y lo devuelve."""
        if codigo in self._productos:
            raise CodigoDuplicadoError(
                f"Ya existe un producto con código {codigo}"
            )

        producto = Producto(codigo, nombre, precio, stock)
        self._productos[codigo] = producto

        return producto

    # --- Consulta ---
    def buscar(self, codigo):
        """Devuelve el producto pedido o lanza excepción."""
        producto = self._productos.get(codigo)

        if producto is None:
            raise ProductoNoEncontrado(f"No existe el código {codigo}")

        return producto

    def listar(self):
        """Devuelve todos los productos del almacén."""
        return list(self._productos.values())

    # --- Modificación ---
    def actualizar_precio(self, codigo, nuevo_precio):
        """Le pide al producto que cambie su precio."""
        self.buscar(codigo).cambiar_precio(nuevo_precio)

    def reponer_stock(self, codigo, cantidad):
        """Le pide al producto que sume stock."""
        self.buscar(codigo).reponer(cantidad)

    # --- Baja ---
    def dar_de_baja(self, codigo):
        """Elimina físicamente el producto indicado."""
        self.buscar(codigo)
        del self._productos[codigo]
```

Dos cosas para mirar con atención. La primera: `buscar()` se reutiliza dentro
de `actualizar_precio()`, `reponer_stock()` y `dar_de_baja()`. La lógica
"encontrar el producto o dar error" está escrita una sola vez.

La segunda: el `Almacen` no escribe `producto._precio = nuevo_precio`. Le
pide al producto que cambie su precio, y el producto valida que sea positivo.
Cada clase defiende sus propias reglas. Si el gestor manoteara los atributos,
esa validación se podría saltear desde cualquier lado.

---

### Baja lógica vs. baja física

Cuando eliminamos un producto con `del self._productos[codigo]` lo estamos
**borrando de verdad**. Se dice que es una **baja física**: el objeto deja de
existir en la colección. Si mañana alguien pregunta "¿cuántos productos le
vendí a Ana el año pasado?" y esos productos ya se dieron de baja, la
información se perdió.

Por eso, en sistemas reales muchas veces se prefiere la **baja lógica**: el
objeto queda en la colección pero se marca como inactivo. Se agrega un
atributo booleano y los métodos que listan filtran los inactivos:

```python
class Producto:
    def __init__(self, codigo, nombre, precio, stock):
        ...
        self._activo = True          # nace activo

    def esta_activo(self):
        """Informa si el producto sigue vigente."""
        return self._activo

    def dar_de_baja(self):
        """Marca el producto como inactivo sin borrarlo."""
        self._activo = False


class Almacen:
    # ... resto igual ...

    def dar_de_baja(self, codigo):
        """Baja lógica: el producto queda pero deja de estar activo."""
        self.buscar(codigo).dar_de_baja()

    def listar_activos(self):
        """Devuelve solo los productos vigentes."""
        return [
            producto
            for producto in self._productos.values()
            if producto.esta_activo()
        ]

    def listar_todos(self):
        """Devuelve todos, incluidos los dados de baja."""
        return list(self._productos.values())
```

| Baja | Ventaja | Desventaja |
|---|---|---|
| **Física** | Simple, ahorra memoria | Se pierde la historia; los códigos se pueden reusar |
| **Lógica** | Preserva la historia; los códigos quedan bloqueados | Ocupa más espacio; hay que acordarse de filtrar |

Esa última desventaja no es menor: con baja lógica, **cualquier método que
liste y se olvide de filtrar muestra datos dados de baja**. Por eso conviene
que el método "normal" (`listar()`) sea el que filtra y que ver todo requiera
pedirlo explícitamente (`listar_todos()`).

En sistemas de dominio serio (facturación, historial médico, banco) **casi
siempre se usa baja lógica**.

### Anticipo: el ABM en Django

Cuando lleguen a Django van a ver que este patrón es **exactamente el corazón
del framework**. Un modelo Django (una clase que hereda de `models.Model`)
trae automáticamente:

- `MiModelo.objects.create(...)` — alta.
- `MiModelo.objects.get(pk=...)` — consulta por identificador.
- `MiModelo.objects.filter(...)` — listar.
- `objeto.save()` — modificación.
- `objeto.delete()` — baja.

Y el **Admin de Django** genera automáticamente una interfaz web con
formularios para crear, editar y borrar, sin que tengas que programar nada.
Todo eso funciona porque el patrón ABM está estandarizado.

Fijate incluso el detalle de `objects.get(pk=...)`: si no encuentra el
objeto, **lanza `DoesNotExist`**, no devuelve `None`. Es la misma decisión de
diseño que tomamos unas páginas atrás.

Cuando escribas modelos Django el año que viene ya no vas a estar aprendiendo
un concepto nuevo: vas a estar viendo cómo Django concreta el ABM que hoy
hacés a mano.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 6** — Hacé una clase `Agenda` con ABM completo de contactos.
> Cada contacto tiene nombre y teléfono. Métodos: `agregar_contacto`,
> `buscar`, `listar`, `actualizar_telefono` y `eliminar`. Usá excepciones
> propias (`ContactoNoEncontrado`, `NombreDuplicadoError`).
>
> El código de este ejercicio está resuelto en `ejercicio_06.py`.

```python
class ContactoNoEncontrado(Exception):
    """Indica que no existe el contacto solicitado."""

    pass


class NombreDuplicadoError(Exception):
    """Indica que el nombre ya existe en la agenda."""

    pass


class Contacto:
    """Contacto con nombre y teléfono."""

    def __init__(self, nombre, telefono):
        self._nombre = nombre
        self._telefono = telefono

    def cambiar_telefono(self, nuevo_telefono):
        """Actualiza el teléfono del contacto."""
        self._telefono = nuevo_telefono

    def __str__(self):
        return f"{self._nombre}: {self._telefono}"


class Agenda:
    """Gestiona un ABM de contactos indexados por nombre."""

    def __init__(self):
        self._contactos = {}

    def agregar_contacto(self, nombre, telefono):
        """Da de alta un contacto nuevo y lo devuelve."""
        if nombre in self._contactos:
            raise NombreDuplicadoError(f"{nombre} ya existe en la agenda")

        contacto = Contacto(nombre, telefono)
        self._contactos[nombre] = contacto

        return contacto

    def buscar(self, nombre):
        """Devuelve el contacto pedido o lanza excepción."""
        contacto = self._contactos.get(nombre)

        if contacto is None:
            raise ContactoNoEncontrado(f"No hay contacto llamado {nombre}")

        return contacto

    def listar(self):
        """Devuelve todos los contactos de la agenda."""
        return list(self._contactos.values())

    def actualizar_telefono(self, nombre, nuevo_telefono):
        """Le pide al contacto que cambie su teléfono."""
        self.buscar(nombre).cambiar_telefono(nuevo_telefono)

    def eliminar(self, nombre):
        """Elimina el contacto indicado de la agenda."""
        self.buscar(nombre)
        del self._contactos[nombre]


if __name__ == "__main__":
    agenda = Agenda()
    agenda.agregar_contacto("Ana", "221-1234")
    agenda.agregar_contacto("Juan", "221-5678")

    agenda.actualizar_telefono("Ana", "221-9999")
    agenda.eliminar("Juan")

    for contacto in agenda.listar():
        print(contacto)
```

---

## Un primer vistazo a SRP

En el próximo capítulo (SOLID) vamos a formalizar los principios de diseño de
POO. Uno de ellos ya deberíamos empezar a intuirlo: el **Principio de
Responsabilidad Única** (*Single Responsibility Principle*, SRP).

> **Definición corta:** cada clase debería tener una sola razón para cambiar.

Traducido: si una clase hace demasiadas cosas, cualquier cambio en cualquiera
de esas cosas la afecta. Se vuelve frágil, difícil de probar y difícil de
reutilizar.

Miremos un contraejemplo:

```python
class BibliotecaMalHecha:
    def __init__(self):
        self._libros = {}

    def agregar_libro(self, libro):
        ...

    def imprimir_libros_por_pantalla(self):    # también imprime
        ...

    def exportar_a_csv(self, ruta):            # y persiste en archivos
        ...

    def enviar_email_al_bibliotecario(self, mensaje):   # y manda mails
        ...
```

Esta clase viola SRP fuerte. Tiene al menos cuatro razones para cambiar: si
cambia cómo se muestra por pantalla, la modifico; si cambia el formato de
archivo, la modifico; si cambia el servidor de mail, la modifico; si cambia
la lógica del catálogo, la modifico. Cada uno de esos cambios puede
introducir bugs en los otros tres. Y si mañana necesito exportar a CSV desde
otra clase, tengo que duplicar código.

**La solución** es partirla en varias clases, cada una con una
responsabilidad clara. Así queda la separación, en código:

```python
class Biblioteca:
    """Única responsabilidad: administrar la colección."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._libros = {}

    def nombre(self):
        """Devuelve el nombre de la biblioteca."""
        return self._nombre

    def agregar(self, libro):
        """Suma un libro al catálogo."""
        self._libros[libro.isbn()] = libro

    def listar(self):
        """Devuelve todos los libros del catálogo."""
        return list(self._libros.values())


class MostradorDeLibros:
    """Única responsabilidad: presentar libros por pantalla."""

    def mostrar(self, biblioteca):
        """Imprime el catálogo de una biblioteca."""
        print(biblioteca.nombre())

        for libro in biblioteca.listar():
            print(f"  - {libro}")


class ExportadorCsv:
    """Única responsabilidad: representar libros como CSV."""

    def exportar(self, biblioteca):
        """Devuelve el catálogo como texto CSV."""
        lineas = ["isbn,titulo,autor"]

        for libro in biblioteca.listar():
            lineas.append(
                f"{libro.isbn()},{libro.titulo()},{libro.autor()}"
            )

        return "\n".join(lineas)
```

Fijate lo que se ganó: `Biblioteca` no sabe nada de pantallas ni de archivos;
`MostradorDeLibros` y `ExportadorCsv` no saben cómo se guardan los libros,
solo le piden `listar()`. Puedo agregar un `ExportadorJson` sin tocar una
línea de `Biblioteca`. Y puedo probar la biblioteca sin imprimir nada.

Además, `ExportadorCsv.exportar()` **devuelve** el texto en vez de escribirlo
al disco. Así la clase se puede probar sin tocar el sistema de archivos, y
quien la use decide qué hacer con ese texto: guardarlo, mandarlo por mail o
mostrarlo.

> **Regla práctica de este capítulo.** Si al describir lo que hace una clase
> usás la palabra "y" muchas veces, probablemente esté haciendo demasiado.
> Una clase debería poder resumirse en una sola oración.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 7** — Te dan una clase `Biblioteca` que gestiona libros, los
> imprime por pantalla y además los exporta a CSV. Partila en tres clases:
> `Biblioteca` (solo la colección), `MostradorDeLibros` (imprime) y
> `ExportadorCsv` (arma el texto CSV). Comprobá que ninguna de las tres
> necesita conocer el trabajo de las otras dos.
>
> El código de este ejercicio está resuelto en `ejercicio_07.py`.

```python
class Libro:
    """Libro con título, autor e ISBN."""

    def __init__(self, isbn, titulo, autor):
        self._isbn = isbn
        self._titulo = titulo
        self._autor = autor

    def isbn(self):
        """Devuelve el ISBN del libro."""
        return self._isbn

    def titulo(self):
        """Devuelve el título del libro."""
        return self._titulo

    def autor(self):
        """Devuelve el autor del libro."""
        return self._autor

    def __str__(self):
        return f"'{self._titulo}' de {self._autor}"


# Biblioteca, MostradorDeLibros y ExportadorCsv son las tres clases
# que aparecen más arriba, en la sección de SRP.

if __name__ == "__main__":
    biblioteca = Biblioteca("Biblioteca Central")
    biblioteca.agregar(Libro("978-987-1", "El Aleph", "Borges"))
    biblioteca.agregar(Libro("978-987-2", "Rayuela", "Cortázar"))

    MostradorDeLibros().mostrar(biblioteca)

    print()
    print(ExportadorCsv().exportar(biblioteca))
```

---

## Cierre: la iteración 4 del banco

Con todo lo del capítulo ya podemos armar el banco completo. Cuatro clases,
cuatro responsabilidades, cada una en su módulo.

**`errores.py`** — solo las excepciones del dominio:

```python
class SaldoInsuficienteError(Exception):
    """Indica que la cuenta no tiene fondos para la operación."""


class MontoInvalidoError(Exception):
    """Indica que el monto de la operación no es válido."""


class CuentaNoEncontrada(Exception):
    """Indica que no existe la cuenta solicitada."""


class NumeroDuplicadoError(Exception):
    """Indica que el número de cuenta ya está usado."""
```

**`personas.py`** — solo identidad:

```python
class Persona:
    """Titular de una cuenta. Solo maneja identidad."""

    def __init__(self, nombre, apellido, dni):
        self._nombre = nombre
        self._apellido = apellido
        self._dni = dni

    def dni(self):
        """Devuelve el documento del titular."""
        return self._dni

    def __str__(self):
        return f"{self._apellido}, {self._nombre}"
```

**`movimientos.py`** — solo el registro de una operación:

```python
class Movimiento:
    """Registro de una operación sobre una cuenta."""

    def __init__(self, tipo, monto, saldo_resultante):
        self._tipo = tipo
        self._monto = monto
        self._saldo_resultante = saldo_resultante

    def __str__(self):
        return (
            f"{self._tipo:<10} ${self._monto:>10} "
            f"-> saldo ${self._saldo_resultante}"
        )
```

**`cuentas.py`** — saldo e historial. Acá se ven las dos formas de tener
objetos adentro: el titular llega hecho de afuera (agregación) y los
movimientos nacen adentro (composición):

```python
from errores import MontoInvalidoError, SaldoInsuficienteError
from movimientos import Movimiento


class Cuenta:
    """Cuenta que administra su saldo y su historial."""

    def __init__(self, numero, titular, saldo=0):
        self._numero = numero
        self._titular = titular          # agregación: ya existía
        self._saldo = saldo
        self._movimientos = []           # composición: nacen acá

    def numero(self):
        """Devuelve el número de cuenta."""
        return self._numero

    def saldo(self):
        """Devuelve el saldo actual."""
        return self._saldo

    def depositar(self, monto):
        """Acredita un monto positivo y lo registra."""
        if monto <= 0:
            raise MontoInvalidoError("El monto debe ser positivo")

        self._saldo += monto
        self._registrar("depósito", monto)

    def extraer(self, monto):
        """Debita un monto si el saldo alcanza y lo registra."""
        if monto <= 0:
            raise MontoInvalidoError("El monto debe ser positivo")

        if monto > self._saldo:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente en {self._numero}"
            )

        self._saldo -= monto
        self._registrar("extracción", monto)

    def _registrar(self, tipo, monto):
        """Agrega un movimiento al historial de la cuenta."""
        self._movimientos.append(Movimiento(tipo, monto, self._saldo))

    def historial(self):
        """Devuelve los movimientos de la cuenta."""
        return list(self._movimientos)

    def __str__(self):
        return f"[{self._numero}] {self._titular} - ${self._saldo}"
```

**`banco.py`** — el ABM, y nada más:

```python
from cuentas import Cuenta
from errores import CuentaNoEncontrada, NumeroDuplicadoError


class Banco:
    """Banco que hace el ABM de cuentas. No calcula saldos."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._cuentas = {}

    def abrir_cuenta(self, numero, titular, saldo=0):
        """Da de alta una cuenta nueva y la devuelve."""
        if numero in self._cuentas:
            raise NumeroDuplicadoError(f"La cuenta {numero} ya existe")

        cuenta = Cuenta(numero, titular, saldo)
        self._cuentas[numero] = cuenta

        return cuenta

    def buscar(self, numero):
        """Devuelve la cuenta pedida o lanza excepción."""
        cuenta = self._cuentas.get(numero)

        if cuenta is None:
            raise CuentaNoEncontrada(f"No existe la cuenta {numero}")

        return cuenta

    def cerrar_cuenta(self, numero):
        """Da de baja la cuenta indicada."""
        self.buscar(numero)
        del self._cuentas[numero]

    def listar(self):
        """Devuelve todas las cuentas del banco."""
        return list(self._cuentas.values())

    def total_depositado(self):
        """Suma los saldos de todas las cuentas."""
        return sum(cuenta.saldo() for cuenta in self.listar())
```

**`main.py`** — el programa que usa todo:

```python
from banco import Banco
from errores import CuentaNoEncontrada, SaldoInsuficienteError
from personas import Persona

if __name__ == "__main__":
    banco = Banco("Banco de La Plata")

    ana = Persona("Ana", "Pérez", "12345678")
    cuenta_ana = banco.abrir_cuenta("001-100", ana, 10000)

    cuenta_ana.depositar(2500)
    cuenta_ana.extraer(4000)

    for cuenta in banco.listar():
        print(cuenta)

    print(f"Total depositado: ${banco.total_depositado()}")

    for movimiento in cuenta_ana.historial():
        print(f"  {movimiento}")

    try:
        cuenta_ana.extraer(999999)
    except SaldoInsuficienteError as error:
        print(f"Error: {error}")
```

Mirá el reparto de responsabilidades, que es la síntesis del capítulo:

- `Persona` maneja identidad. No sabe qué es una cuenta.
- `Movimiento` registra un hecho. No sabe quién lo produjo.
- `Cuenta` maneja saldo e historial. No sabe que existe un banco.
- `Banco` hace el ABM. **No calcula saldos ni valida montos**: cuando alguien
  deposita, le pide a la cuenta que deposite. Si `Banco` tuviera un método
  `depositar(numero, monto)` que hiciera `cuenta._saldo += monto`, estaríamos
  otra vez con la validación en dos lugares.

Si mañana agregamos `CuentaAhorro` con intereses, `Banco` no cambia: sigue
guardando cuentas y pidiéndoles cosas. Si agregamos un `ExportadorCsv` de
cuentas, ninguna de las cuatro clases cambia. Eso es lo que ganamos, y en el
capítulo 13 vamos a ponerle nombre formal a cada una de esas propiedades.
