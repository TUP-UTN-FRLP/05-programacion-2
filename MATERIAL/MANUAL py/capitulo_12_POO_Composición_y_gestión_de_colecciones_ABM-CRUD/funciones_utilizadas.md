# Funciones Utilizadas en capitulo_12_POO_Composición_y_gestión_de_colecciones_ABM-CRUD

Documento que agrupa las funciones built-in, los métodos, los módulos,
los tipos de excepción y las construcciones del lenguaje utilizados en
los ejercicios y enunciados, organizados por tipo y en orden
alfabético.

Este capítulo trabaja la **composición** (un objeto que contiene a
otros) y la **gestión de colecciones** con operaciones de alta, baja,
modificación y consulta (ABM/CRUD). Aparecen dos herramientas nuevas
respecto de los capítulos anteriores: el **diccionario como colección
interna** indexada por una clave (`self._autos = {}`), con su acceso
por `[]`, `.get()`, `in` y `del`; y el módulo **`copy`** para
distinguir una referencia compartida de una copia independiente.
También se consolidan las **excepciones propias**, que acá se lanzan
en casi todos los archivos para señalar "no encontrado" y "duplicado".

---

## Funciones Generales

### `divmod(a, b)`

**¿Qué realiza?**

Devuelve en un solo paso el cociente y el resto de dividir `a` por `b`,
como una tupla `(cociente, resto)`. En el capítulo se usa para pasar
una duración en segundos a minutos y segundos.

**¿Qué retorna?**

Una tupla de dos enteros: `(a // b, a % b)`.

**Ejemplos típicos:**

```python
minutos, segundos = divmod(self._duracion_seg, 60)
return f"{self._titulo} - {self._artista} ({minutos}:{segundos:02d})"
```

### `isinstance(objeto, clase)`

**¿Qué realiza?**

Verifica si un objeto es una instancia de una clase (o de una tupla de
clases). En este capítulo se usa dentro de un módulo de validaciones
para comprobar que un dato recibido sea del tipo esperado antes de
seguir.

**¿Qué retorna?**

Un valor de tipo `bool`.

**Ejemplos típicos:**

```python
def es_dni_valido(dni):
    return (
        isinstance(dni, str)
        and dni.isdigit()
        and len(dni) in (7, 8)
    )
```

### `len(colección)`

**¿Qué realiza?**

Retorna la cantidad de elementos de una colección (lista o
diccionario). Se usa para contar inscriptos, calcular un promedio,
saber cuánto cupo queda en un torneo y validar longitudes de texto.

**¿Qué retorna?**

Un valor de tipo `int`.

**Ejemplos típicos:**

```python
def cantidad_inscriptos(self):
    return len(self._alumnos)

def cupo_disponible(self):
    return MAX_EQUIPOS - len(self._equipos)

return total / len(self._empleados)     # promedio de sueldos
```

### `list(iterable)`

**¿Qué realiza?**

Construye una lista nueva a partir de un iterable. En el capítulo se
usa sobre todo para **devolver hacia afuera una copia** de la
colección interna: `list(self._autos.values())` entrega los objetos
sin exponer el diccionario real, y `list(self._movimientos)` entrega
una copia de la lista para que nadie la modifique desde afuera.

**¿Qué retorna?**

Una lista nueva.

**Ejemplos típicos:**

```python
def listar(self):
    return list(self._productos.values())

def historial(self):
    return list(self._movimientos)      # copia defensiva
```

### `print(*objetos, sep=' ', end='\n')`

**¿Qué realiza?**

Escribe uno o varios valores en la salida estándar. Se usa para
mostrar listados, el mensaje de las excepciones capturadas y los
totales calculados.

**¿Qué retorna?**

`None`.

**Ejemplos típicos:**

```python
for producto in almacen.listar():
    print(producto)

print(f"Error: {error}")
print(f"Promedio: ${empresa.promedio_sueldos():.2f}")
```

### `range(fin)`

**¿Qué realiza?**

Genera una secuencia de enteros de `0` a `fin - 1`. En el capítulo se
usa para repetir un alta tantas veces como indica una constante del
módulo.

**¿Qué retorna?**

Un objeto `range`, iterable.

**Ejemplos típicos:**

```python
for numero in range(MAX_EQUIPOS):
    torneo.agregar_equipo(Equipo(f"Equipo {numero + 1}"))
```

### `sorted(iterable, key=...)`

**¿Qué realiza?**

Devuelve una lista nueva con los elementos ordenados, sin tocar el
original. Con `key` se indica según qué criterio ordenar: `key=lambda
jugador: jugador.numero()` ordena por número de camiseta. Sobre un
diccionario, `sorted(self._pasajeros)` ordena sus **claves**.

**¿Qué retorna?**

Una lista nueva ordenada.

**Ejemplos típicos:**

```python
ordenados = sorted(
    self._jugadores,
    key=lambda jugador: jugador.numero(),
)

for asiento in sorted(self._pasajeros):     # ordena las claves del dict
    print(f"  {self._pasajeros[asiento]}")
```

### `sum(iterable)`

**¿Qué realiza?**

Retorna la suma de los elementos de un iterable numérico. Se combina
con una expresión generadora que le pide un número a cada objeto de la
colección: subtotales de un carrito, saldos de cuentas, sueldos de
empleados, precios finales de una compra.

**¿Qué retorna?**

La suma total.

**Ejemplos típicos:**

```python
def total(self):
    return sum(linea.subtotal() for linea in self._lineas)

def saldo_total(self):
    return sum(cuenta.saldo() for cuenta in self._cuentas)

total = sum(empleado.sueldo() for empleado in self._empleados)
```

---

## Métodos de Strings (Cadenas de Texto)

Los siguientes elementos son métodos de la clase `str`. Se invocan
sobre un objeto de tipo string, por ejemplo, `nombre.strip()`.

### `string.isdigit()`

**¿Qué realiza?**

Verifica si todos los caracteres del string son dígitos y el string no
está vacío. Se usa para validar un DNI.

**¿Qué retorna?**

Un valor de tipo `bool`.

**Ejemplos típicos:**

```python
def es_dni_valido(dni):
    return isinstance(dni, str) and dni.isdigit() and len(dni) in (7, 8)
```

### `string.strip()`

**¿Qué realiza?**

Devuelve el string sin los espacios en blanco de los extremos. Se usa
para normalizar un nombre antes de guardarlo o mostrarlo.

**¿Qué retorna?**

Un nuevo string.

**Ejemplos típicos:**

```python
def normalizar_nombre(nombre):
    return nombre.strip().title()     # "  ana maría  " -> "Ana María"
```

### `string.title()`

**¿Qué realiza?**

Devuelve el string con la primera letra de cada palabra en mayúscula y
el resto en minúscula. Se encadena con `strip()` para normalizar
nombres.

**¿Qué retorna?**

Un nuevo string.

**Ejemplos típicos:**

```python
nombre.strip().title()
```

### `separador.join(iterable_de_strings)`

**¿Qué realiza?**

Une los elementos de un iterable de strings en un solo string,
intercalando entre ellos el string sobre el que se invoca. Es la
operación inversa de `split()`. En el capítulo se usa en el
`ExportadorCsv`: se arma una lista con una línea de texto por libro y al
final se pegan todas con `"\n"` en el medio para formar el CSV
completo.

**¿Qué retorna?**

Un nuevo string.

**Errores posibles:**

Lanza `TypeError` si algún elemento del iterable no es un string (hay
que convertir los números con `str()` antes de unir).

**Ejemplos típicos:**

```python
def exportar(self, biblioteca):
    lineas = ["isbn,titulo,autor"]
    for libro in biblioteca.listar():
        lineas.append(
            f"{libro.isbn()},{libro.titulo()},{libro.autor()}"
        )
    return "\n".join(lineas)
```

---

## Métodos de Listas

Los siguientes elementos son métodos de la clase `list`. Se invocan
sobre una lista que es atributo privado de un objeto, por ejemplo,
`self._alumnos.append(x)`.

### `list.append(elemento)`

**¿Qué realiza?**

Agrega `elemento` al final de la lista, modificándola en el lugar. Es
la operación de "alta" cuando la colección interna es una lista
(inscribir un alumno, contratar un empleado, agregar una línea al
carrito).

**¿Qué retorna?**

`None`.

**Ejemplos típicos:**

```python
def inscribir(self, alumno):
    self._alumnos.append(alumno)

def agregar(self, producto, cantidad):
    self._lineas.append(LineaDeCarrito(producto, cantidad))
```

### `list.remove(elemento)`

**¿Qué realiza?**

Busca la **primera** aparición de `elemento` en la lista (por
igualdad) y la elimina. Es la "baja" cuando la colección es una lista:
primero se busca el objeto con `buscar_por_legajo()` y después se lo
quita.

**¿Qué retorna?**

`None`.

**Errores posibles:**

Lanza `ValueError` si el elemento no está en la lista. Por eso el
código busca antes al empleado (y esa búsqueda ya lanza su propia
excepción si no existe).

**Ejemplos típicos:**

```python
def despedir(self, legajo):
    empleado = self.buscar_por_legajo(legajo)   # lanza si no existe
    self._empleados.remove(empleado)
```

---

## El Diccionario como Colección Interna (ABM)

Varios enunciados guardan los objetos en un diccionario indexado por
su identificador (`{patente: Auto}`, `{numero: Mesa}`,
`{asiento: Pasajero}`) en lugar de una lista. Así la búsqueda es
directa, sin recorrer todo, y el alta puede rechazar identificadores
repetidos.

### `clave in diccionario`

**¿Qué realiza?**

Indica si la clave ya existe en el diccionario. Es la comprobación
previa al alta para rechazar un identificador duplicado.

**Ejemplos típicos:**

```python
def agregar_auto(self, patente, marca, modelo, precio):
    if patente in self._autos:
        raise PatenteDuplicadaError(f"La patente {patente} ya existe")
    self._autos[patente] = Auto(patente, marca, modelo, precio)
```

### `diccionario[clave] = valor`

**¿Qué realiza?**

Guarda (o reemplaza) el objeto asociado a `clave`. Es el "alta" cuando
la colección es un diccionario.

**Ejemplos típicos:**

```python
self._productos[codigo] = producto
self._mesas[numero] = Mesa(numero, capacidad)
```

### `diccionario.get(clave)`

**¿Qué realiza?**

Devuelve el valor asociado a `clave`, o `None` si la clave no existe,
**sin lanzar** `KeyError`. Es el patrón de búsqueda del capítulo:
pedir con `.get()`, y si vino `None`, lanzar una excepción propia con
un mensaje claro.

**¿Qué retorna?**

El objeto guardado, o `None`.

**Ejemplos típicos:**

```python
def buscar(self, codigo):
    producto = self._productos.get(codigo)
    if producto is None:
        raise ProductoNoEncontrado(f"No existe el código {codigo}")
    return producto
```

### `diccionario.values()`

**¿Qué realiza?**

Devuelve una vista de los valores del diccionario (los objetos
guardados), para recorrerlos o convertirlos en lista. Las claves no
interesan en el listado.

**Ejemplos típicos:**

```python
def listar(self):
    return list(self._productos.values())

return [
    mesa
    for mesa in self._mesas.values()
    if not mesa.esta_ocupada()
]
```

### `del diccionario[clave]`

**¿Qué realiza?**

Elimina la entrada de esa clave. Es la "baja física": el objeto
desaparece de la colección. Se valida antes que la clave exista para
no cortar con un `KeyError`.

**Ejemplos típicos:**

```python
def dar_de_baja(self, codigo):
    self.buscar(codigo)          # lanza ProductoNoEncontrado si no está
    del self._productos[codigo]
```

### Iterar y ordenar un diccionario

**¿Qué realiza?**

Recorrer directamente el diccionario (o `sorted(diccionario)`) itera
sobre sus **claves**. Con la clave se accede al valor por `[]`.

**Ejemplos típicos:**

```python
for asiento in sorted(self._pasajeros):
    print(f"  {self._pasajeros[asiento]}")
```

---

## Módulo `copy`

### `copy.deepcopy(objeto)`

**¿Qué realiza?**

Crea una copia **profunda** e independiente de un objeto: duplica
también los objetos que tiene adentro. Requiere `import copy`. En el
capítulo se usa para mostrar la diferencia con una referencia
compartida: dos personas que guardan *la misma* `Direccion` ven
cualquier cambio; si una guarda `copy.deepcopy(direccion)`, queda
aislada.

**¿Qué retorna?**

Un objeto nuevo, sin vínculos con el original.

**Ejemplos típicos:**

```python
import copy

madre = Persona("Ana", familiar)
hijo = Persona("Pedro", familiar)          # misma Direccion: comparten

familiar.mudar("Calle 50", 900)            # cambian los dos

independiente = Persona("Lucía", copy.deepcopy(familiar))
familiar.mudar("Diagonal 74", 55)          # Lucía NO se entera
```

---

## Tipos de Excepción

### `Exception`

**¿Cuándo se produce?**

Es la clase base de todas las excepciones. No se lanza directamente:
se usa como superclase al **definir excepciones propias**, que en este
capítulo son la herramienta central para señalar errores de la
gestión ("no encontrado", "duplicado", "ocupado", "lleno").

**Ejemplos típicos:**

```python
class ProductoNoEncontrado(Exception):
    """Indica que no existe el producto solicitado."""
    pass


class CodigoDuplicadoError(Exception):
    """Indica que el código del producto ya existe."""
    pass
```

### `ValueError`

**¿Cuándo se produce?**

Cuando un valor es del tipo correcto pero está fuera de rango. En el
capítulo se lanza desde los métodos que modifican un objeto (cambiar
precio, depositar, extraer) al recibir un monto no positivo. También
lo lanza `list.remove()` si el elemento no está.

**Ejemplos típicos:**

```python
def cambiar_precio(self, nuevo_precio):
    if nuevo_precio <= 0:
        raise ValueError("El precio debe ser positivo")
    self._precio = nuevo_precio

def depositar(self, monto):
    if monto <= 0:
        raise ValueError("El monto debe ser positivo")
    self._saldo += monto
```

### Excepciones personalizadas

**¿Cuándo se producen?**

Cuando el error pertenece al dominio del problema. Se definen como una
clase que hereda de `Exception`, con cuerpo `pass` o solo un
docstring, y permiten que quien usa la clase distinga con `except` qué
salió mal: no es lo mismo "la habitación no existe" que "existe pero
está ocupada".

Familias de excepciones propias que aparecen en el capítulo:

| Excepción (o familia) | Se lanza cuando... |
| --------------------- | ------------------ |
| `ProductoNoEncontrado`, `ContactoNoEncontrado`, `AlumnoNoEncontrado`, `AutoNoEncontrado`, `MesaNoEncontrada`, `EmpleadoNoEncontrado`, `SocioNoEncontrado`, `HabitacionNoEncontrada`, `JugadorNoEncontrado`, `CuentaNoEncontrada`, `SuscriptorNoEncontrado`, `AsientoLibre` | se busca por identificador y no existe (o el asiento está vacío) |
| `CodigoDuplicadoError`, `NombreDuplicadoError`, `PatenteDuplicadaError`, `NumeroDuplicadoError`, `AsientoOcupadoError`, `EmailDuplicadoError` | el alta usa un identificador que ya está tomado |
| `MesaOcupadaError`, `HabitacionNoDisponible` | se intenta ocupar/reservar algo que ya está en uso |
| `TorneoLlenoError` | el alta supera un cupo máximo |
| `SaldoInsuficienteError`, `MontoInvalidoError` | la operación bancaria no es válida |

**Ejemplos típicos:**

```python
class AutoNoEncontrado(Exception):
    pass


def buscar_por_patente(self, patente):
    auto = self._autos.get(patente)
    if auto is None:
        raise AutoNoEncontrado(f"No hay auto con patente {patente}")
    return auto
```

```python
try:
    hotel.reservar(101, "Otro huésped", 2)
except HabitacionNoDisponible as error:
    print(f"Ocupada: {error}")
except HabitacionNoEncontrada as error:
    print(f"Inexistente: {error}")
```

---

## Construcciones del Lenguaje

Las siguientes construcciones sostienen la composición y la gestión de
colecciones.

### Composición: un objeto como atributo de otro

**¿Qué realiza?**

Una clase guarda una instancia de otra clase como atributo, y le
delega la parte del trabajo que le corresponde. Una `Casa` *tiene una*
`Direccion`; un `Auto` *tiene un* `Motor`. La clase contenedora no
reimplementa el `__str__` de lo que contiene: se lo pide.

**Ejemplos típicos:**

```python
class Persona:

    def __init__(self, nombre, direccion):
        self._nombre = nombre
        self._direccion = direccion       # una Direccion adentro

    def __str__(self):
        return f"{self._nombre} vive en {self._direccion}"
```

### Colección interna (`[]` o `{}`) como atributo

**¿Qué realiza?**

La clase contenedora arranca con una lista o un diccionario vacío en
`__init__` y ahí guarda los objetos que administra. La lista sirve
cuando el orden importa y no hay clave natural; el diccionario, cuando
cada objeto tiene un identificador único por el que se lo va a buscar.

**Ejemplos típicos:**

```python
class Equipo:
    def __init__(self, nombre):
        self._nombre = nombre
        self._jugadores = []              # lista: sin clave natural


class Concesionaria:
    def __init__(self):
        self._autos = {}                  # dict: indexado por patente
```

### Delegación: `self.buscar(x).hacer_algo()`

**¿Qué realiza?**

La clase contenedora no cambia el estado de los objetos que guarda
desde afuera: encuentra el objeto y le pide a él que haga el trabajo.
El `Restaurant` no hace `mesa._ocupada = True`; llama a
`self.buscar_mesa(numero).ocupar()` y la `Mesa` decide.

**Ejemplos típicos:**

```python
def ocupar(self, numero):
    self.buscar_mesa(numero).ocupar()

def actualizar_precio(self, codigo, nuevo_precio):
    self.buscar(codigo).cambiar_precio(nuevo_precio)
```

### Reutilizar `buscar_*()` dentro de otros métodos

**¿Qué realiza?**

En vez de repetir en cada método la comprobación de "¿existe?", se
escribe una sola vez en `buscar()` (que devuelve el objeto o lanza la
excepción) y los demás métodos la llaman. Una sola regla, un solo
lugar.

**Ejemplos típicos:**

```python
def actualizar_precio(self, codigo, nuevo_precio):
    self.buscar(codigo).cambiar_precio(nuevo_precio)

def reponer_stock(self, codigo, cantidad):
    self.buscar(codigo).reponer(cantidad)

def dar_de_baja(self, codigo):
    self.buscar(codigo)
    del self._productos[codigo]
```

### `raise` y definir una excepción personalizada

**¿Qué realiza?**

`raise TipoDeError("mensaje")` interrumpe el método y lanza la
excepción. Las excepciones propias se definen antes, heredando de
`Exception`, normalmente con cuerpo `pass` o un docstring.

**Ejemplos típicos:**

```python
class TorneoLlenoError(Exception):
    """Indica que el torneo alcanzó el máximo de equipos."""
    pass


def agregar_equipo(self, equipo):
    if self.cupo_disponible() <= 0:
        raise TorneoLlenoError(f"El torneo ya tiene {MAX_EQUIPOS} equipos")
    self._equipos.append(equipo)
```

### `try/except ... as error`

**¿Qué realiza?**

Rodea la operación que puede fallar (un alta duplicada, una búsqueda
sin resultado) y captura la excepción para mostrar su mensaje sin
cortar el programa. Con varios `except` se distinguen los distintos
errores del dominio.

**Ejemplos típicos:**

```python
try:
    almacen.dar_de_alta("P-001", "Otra yerba", 3000, 5)
except CodigoDuplicadoError as error:
    print(f"Error: {error}")
```

### Comprobación temprana con `return` / `is None`

**¿Qué realiza?**

Los métodos chequean primero la condición de corte y salen (o lanzan)
enseguida, dejando el camino feliz sin anidar. `if x is None:` después
de un `.get()` es el chequeo típico.

**Ejemplos típicos:**

```python
def buscar(self, numero):
    socio = self._socios.get(numero)
    if socio is None:
        raise SocioNoEncontrado(f"No existe el socio {numero}")
    return socio

def promedio_sueldos(self):
    if not self._empleados:          # colección vacía es "falsa"
        return 0
    ...
```

### `if __name__ == "__main__":` y la variable `__name__`

**¿Qué realiza?**

`__name__` vale `"__main__"` cuando el archivo se ejecuta directo, y
el nombre del módulo cuando lo importa otro archivo. Poner la prueba
dentro de `if __name__ == "__main__":` hace que corra al ejecutar el
archivo pero no al importarlo. En este capítulo **todos** los archivos
la usan para separar las definiciones de la demostración.

**Ejemplos típicos:**

```python
def es_dni_valido(dni):
    ...

if __name__ == "__main__":
    print(f'__name__ vale "{__name__}"')     # "__main__" si se ejecuta
    print(es_dni_valido("12345678"))
```

### Constante de módulo en MAYÚSCULAS

**¿Qué realiza?**

Un valor fijo que se usa en varios lugares se define una sola vez a
nivel del módulo, con nombre en mayúsculas, en lugar de escribir el
número suelto ("número mágico") repartido por el código.

**Ejemplos típicos:**

```python
MAX_EQUIPOS = 8


class Torneo:

    def cupo_disponible(self):
        return MAX_EQUIPOS - len(self._equipos)
```

### List comprehension con filtro

**¿Qué realiza?**

Arma una lista nueva recorriendo una colección y quedándose solo con
los elementos que cumplen una condición. Es el patrón de las consultas
"dame los que...": mesas libres, empleados de un departamento, socios
activos.

**Ejemplos típicos:**

```python
def mesas_libres(self):
    return [
        mesa
        for mesa in self._mesas.values()
        if not mesa.esta_ocupada()
    ]

def empleados_por_departamento(self, depto):
    return [
        empleado
        for empleado in self._empleados
        if empleado.departamento() == depto
    ]
```

### Expresión generadora en `sum()`

**¿Qué realiza?**

Recorre la colección y produce un número por cada objeto, sin construir
una lista intermedia, para que `sum()` lo totalice.

**Ejemplos típicos:**

```python
return sum(linea.subtotal() for linea in self._lineas)

return sum(cuenta.saldo() for cuenta in self.listar())
```

### `lambda` como criterio de orden

**¿Qué realiza?**

Una función anónima de una sola línea. Se usa como `key` de `sorted()`
para indicar por qué atributo ordenar cuando los elementos son
objetos.

**Ejemplos típicos:**

```python
ordenados = sorted(
    self._jugadores,
    key=lambda jugador: jugador.numero(),
)
```

### Expresión condicional inline (`a if cond else b`)

**¿Qué realiza?**

Elige entre dos valores en una sola expresión. Se usa dentro de
`__str__` para mostrar el estado de un objeto según un booleano.

**Ejemplos típicos:**

```python
def __str__(self):
    estado = "ocupada" if self._ocupada else "libre"
    return f"Mesa {self._numero} (cap. {self._capacidad}) - {estado}"
```

### Desempaquetado de tuplas

**¿Qué realiza?**

Asignar varias variables de una vez a partir de una tupla. Aparece al
recorrer una lista de pares `(numero, capacidad)` en un `for` y al
recibir el resultado de `divmod()`.

**Ejemplos típicos:**

```python
for numero, capacidad in [(1, 4), (2, 2), (3, 6)]:
    restaurant.abrir_mesa(numero, capacidad)

minutos, segundos = divmod(self.duracion_total(), 60)
```

### `in` con una tupla de valores

**¿Qué realiza?**

`x in (7, 8)` comprueba si `x` es uno de esos valores. Es más corto
que `x == 7 or x == 8`.

**Ejemplos típicos:**

```python
return isinstance(dni, str) and dni.isdigit() and len(dni) in (7, 8)
```

### Truthiness de una colección vacía

**¿Qué realiza?**

Una lista o diccionario vacío se evalúa como `False`. `if not
self._empleados:` es la forma idiomática de preguntar "¿está vacía?"
antes de dividir por su longitud.

**Ejemplos típicos:**

```python
def promedio_sueldos(self):
    if not self._empleados:
        return 0
    total = sum(e.sueldo() for e in self._empleados)
    return total / len(self._empleados)
```

### Valores por defecto en parámetros

**¿Qué realiza?**

Un parámetro del `__init__` o de un método puede tener un valor por
defecto que se usa si no se pasa. Las cuentas nacen con saldo `0` si
no se indica otro.

**Ejemplos típicos:**

```python
class Cuenta:
    def __init__(self, numero, saldo_inicial=0):
        self._numero = numero
        self._saldo = saldo_inicial

def abrir_cuenta(self, numero, saldo_inicial=0):
    cuenta = Cuenta(numero, saldo_inicial)
    ...
```

### Método interno con guion bajo (`_registrar`)

**¿Qué realiza?**

Un método pensado para uso interno de la clase lleva un guion bajo al
inicio. `Cuenta._registrar()` arma un `Movimiento` y lo guarda; lo
llaman `depositar()` y `extraer()`, no el código de afuera.

**Ejemplos típicos:**

```python
def depositar(self, monto):
    ...
    self._saldo += monto
    self._registrar("depósito", monto)

def _registrar(self, tipo, monto):
    self._movimientos.append(Movimiento(tipo, monto, self._saldo))
```

### Composición combinada con herencia

**¿Qué realiza?**

Los dos mecanismos conviven: `ProductoConDescuento(Producto)` usa
herencia y `super().__init__()`, y una `Compra` los **contiene** a
todos en una lista, pidiéndoles `precio_final()` sin mirar el tipo (el
polimorfismo del capítulo 11 sigue funcionando).

**Ejemplos típicos:**

```python
class ProductoConDescuento(Producto):
    def __init__(self, nombre, precio, descuento):
        super().__init__(nombre, precio)
        self._descuento = descuento

    def precio_final(self):
        return self._precio * (1 - self._descuento / 100)


class Compra:
    def total(self):
        return sum(p.precio_final() for p in self._productos)
```

### f-strings y formato de valores

**¿Qué realiza?**

Incrustan expresiones en un string. Además del `{valor:.2f}` (dos
decimales) y `{valor:02d}` (cero a la izquierda) ya vistos, en el
capítulo aparecen la **alineación** en un ancho fijo (`{x:<10}` a la
izquierda, `{x:>10}` a la derecha) para armar columnas, y la
conversión `{x!r}`, que muestra el valor como lo haría `repr()` (con
las comillas en los strings).

**Ejemplos típicos:**

```python
def __str__(self):
    return f"{self._tipo:<10} ${self._monto:>10} -> saldo ${self._saldo_resultante}"

print(f"  {dni!r}: {es_dni_valido(dni)}")    # 'texto' con comillas

print(f"Promedio: ${empresa.promedio_sueldos():.2f}")
```

---

## Resumen por Categoría

| Categoría | Elementos |
| --------- | --------- |
| **Funciones built-in** | `divmod`, `isinstance`, `len`, `list`, `print`, `range`, `sorted`, `sum` |
| **Métodos de `str`** | `isdigit`, `strip`, `title`, `join` |
| **Métodos de `list`** | `append`, `remove` |
| **Diccionario como colección** | `clave in d`, `d[clave] = v`, `d.get(clave)`, `d.values()`, `del d[clave]`, iterar/`sorted(d)` sobre claves |
| **Módulo `copy`** | `copy.deepcopy` |
| **Tipos de excepción** | `Exception`, `ValueError`, y excepciones personalizadas ("no encontrado", "duplicado", "ocupado", `TorneoLlenoError`, `SaldoInsuficienteError`, `MontoInvalidoError`) |
| **Construcciones del lenguaje** | composición (objeto como atributo), colección interna `[]`/`{}`, delegación (`self.buscar(x).hacer()`), reutilizar `buscar_*()`, `raise` y excepción propia, `try/except ... as error`, comprobación temprana / `is None`, `if __name__ == "__main__":` y `__name__`, constante de módulo en MAYÚSCULAS, list comprehension con filtro, expresión generadora en `sum()`, `lambda` en `key=`, expresión condicional inline, desempaquetado de tuplas, `in` con tupla, truthiness de colección vacía, valores por defecto, método interno `_nombre`, composición + herencia, f-strings con formato (`:.2f`, `:02d`, `:<10`/`:>10`, `!r`) |

---

## Notas Importantes

- **Composición = "tiene un"; herencia = "es un".** Una `Casa` no es
  una `Direccion`: tiene una. Se guarda como atributo y se le delega
  su parte del trabajo. Cuando la frase natural es "es un", va
  herencia (capítulo 11).

- **Compartir un objeto es distinto de copiarlo.** Dos `Persona` que
  guardan la misma `Direccion` ven cualquier cambio: hay una sola
  `Direccion` con dos referencias. `copy.deepcopy()` hace una copia
  independiente. Compartir una `Direccion` entre familiares está bien
  (agregación); compartir un `Motor` entre dos autos es un error de
  modelado.

- **Lista o diccionario: depende de si hay clave natural.** Si cada
  objeto tiene un identificador único por el que se lo va a buscar
  (patente, legajo, asiento), el diccionario `{clave: objeto}` evita
  recorrer todo. Si no la hay, o el orden de llegada importa, va la
  lista.

- **`.get()` no lanza; `[]` sí.** El patrón de búsqueda del capítulo
  es `d.get(clave)` y después `if x is None: raise ...Error(...)`. Así
  el mensaje de error lo elige la clase, en vez de dejar salir un
  `KeyError` genérico.

- **Validar antes de `del`.** `del d[clave]` con una clave que no
  existe lanza `KeyError`. Los métodos de baja llaman primero a
  `buscar()` (que lanza la excepción propia si no está) y recién
  después borran.

- **Una excepción por tipo de error deja elegir cómo reaccionar.** El
  hotel distingue `HabitacionNoEncontrada` de `HabitacionNoDisponible`
  porque el usuario necesita saber cuál de los dos pasó. Con un solo
  error genérico esa información se pierde.

- **La clase contenedora no toca el estado de lo que contiene.** El
  `Restaurant` no hace `mesa._ocupada = True`: le pide a la `Mesa` que
  se ocupe con `ocupar()`, y la mesa valida (si ya estaba ocupada,
  lanza). Cada objeto es dueño de su estado.

- **`buscar()` una vez, reusar en todos lados.** La comprobación de
  existencia se escribe una sola vez. `actualizar_precio()`,
  `reponer_stock()` y `dar_de_baja()` llaman a `buscar()` en lugar de
  repetir el `if ... is None`.

- **Baja lógica vs. baja física.** Marcar `self._activo = False`
  conserva el historial (socios, suscriptores); `del d[clave]` lo
  borra. El enunciado elige según si después hace falta saber que ese
  registro existió.

- **`if __name__ == "__main__":` separa la biblioteca del programa.**
  Lo de arriba (clases y funciones) se puede importar sin efectos; lo
  de adentro del `if` solo corre al ejecutar el archivo directamente.
