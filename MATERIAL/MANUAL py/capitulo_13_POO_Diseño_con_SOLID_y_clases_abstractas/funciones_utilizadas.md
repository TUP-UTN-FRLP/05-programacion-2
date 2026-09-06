# Funciones Utilizadas en capitulo_13_POO_Diseño_con_SOLID_y_clases_abstractas

Documento que agrupa las funciones built-in, los métodos, los módulos,
los tipos de excepción y las construcciones del lenguaje utilizados en
los ejercicios y enunciados, organizados por tipo y en orden
alfabético.

Este capítulo trata el **diseño con los principios SOLID** y las
**clases abstractas**. Como en el capítulo 11, el foco no está en
funciones nuevas sino en cómo se organizan las clases: separar
responsabilidades, programar contra una abstracción (`ABC` o
`Protocol`) y no contra una implementación concreta, e inyectar las
dependencias por el constructor. Todo el andamiaje de `abc`,
`@dataclass`, `typing` y `assert` está explicado en la teoría; acá se
listan las piezas de apoyo que aparecen en los ejercicios y que la
teoría del capítulo no desarrolla: las built-in `min()` y `max()` con
`key`, la introspección con `hasattr()`, `getattr()` e
`inspect.getsource()`, unas pocas fórmulas de `math`, las anotaciones
`Any`, `Callable` y `TypeVar` de `typing`, y el `TypeError` que Python
lanza al intentar instanciar una clase abstracta.

---

## Funciones Generales

### `getattr(objeto, "nombre")`

**¿Qué realiza?**

Devuelve el atributo cuyo nombre se pasa como string. Es acceso
dinámico: el nombre se decide en tiempo de ejecución. En el capítulo se
usa sobre la **clase** (no sobre una instancia) para obtener el
descriptor `saldo` y comprobar que es una `property` de verdad, y no un
atributo común que cualquier acceso pasaría por alto.

**¿Qué retorna?**

El valor del atributo pedido. `getattr(Clase, "saldo")` sobre una
property devuelve el objeto `property`, no el saldo de ninguna
instancia.

**Ejemplos típicos:**

```python
assert isinstance(getattr(clase, "saldo"), property), (
    f"{nombre}: saldo no es una property"
)
```

### `hasattr(objeto, "nombre")`

**¿Qué realiza?**

Indica si el objeto tiene un atributo o método con ese nombre. En el
capítulo aparece después de partir una interfaz gorda en interfaces
chicas (ISP): sirve para mostrar que la clase que solo implementa una
de ellas **no** tiene los métodos de las otras, en vez de tenerlos y
que lancen `NotImplementedError`.

**¿Qué retorna?**

Un valor de tipo `bool`.

**Ejemplos típicos:**

```python
# ImpresoraSimple implementa Impresora, no Escaner
print(hasattr(ImpresoraSimple(), "escanear"))     # False

# Robot implementa SabeTrabajar, no RecibeRemuneracion
print(hasattr(Robot(), "cobrar_sueldo"))          # False
```

### `isinstance(objeto, clase)`

**¿Qué realiza?**

Verifica si un objeto es instancia de una clase. En el capítulo tiene
dos usos: con un `Protocol` decorado con `@runtime_checkable` comprueba
que un objeto cumple la forma del protocolo sin heredar de él (esto lo
explica la teoría); y con la clase `property` como segundo argumento
comprueba que un atributo de clase es realmente una property.

**¿Qué retorna?**

Un valor de tipo `bool`.

**Ejemplos típicos:**

```python
print(isinstance(Alumno("L-002", "Juan"), Exportable))   # True
print(isinstance(Aula(101), Exportable))                  # False

assert isinstance(getattr(clase, "saldo"), property)
```

### `len(colección)`

**¿Qué realiza?**

Retorna la cantidad de elementos de una colección. Se usa para
promediar notas, contar los libros de un catálogo y verificar cuántos
vértices tiene cada polígono.

**¿Qué retorna?**

Un valor de tipo `int`.

**Ejemplos típicos:**

```python
def promedio(self):
    if not self._notas:
        return 0
    return sum(self._notas) / len(self._notas)

assert len(cuadrado.vertices) == 0
```

### `list(iterable)`

**¿Qué realiza?**

Construye una lista nueva a partir de un iterable. Igual que en los
capítulos 10 a 12, se usa para **devolver una copia** de una colección
interna (`list(self._movimientos)`, `list(self._libros.values())`) y
para no compartir la lista que llega por parámetro
(`self._notas = list(notas)`).

**¿Qué retorna?**

Una lista nueva.

**Ejemplos típicos:**

```python
def __init__(self, nombre, notas):
    self._nombre = nombre
    self._notas = list(notas)          # copia, no la lista de afuera

def historial(self) -> list[Movimiento]:
    return list(self._movimientos)     # copia defensiva
```

### `max(iterable, key=...)`

**¿Qué realiza?**

Devuelve el elemento mayor de un iterable. Con `key` se indica según
qué criterio comparar: `key=lambda forma: forma.area()` compara por
área. El bucle no pregunta de qué tipo es cada forma: es el
polimorfismo del capítulo 11 al servicio de una búsqueda.

**¿Qué retorna?**

El elemento (no el valor que devuelve `key`).

**Ejemplos típicos:**

```python
def forma_con_mayor_area(formas: list[Forma]) -> Forma:
    return max(formas, key=lambda forma: forma.area())
```

### `min(iterable, key=...)`

**¿Qué realiza?**

Devuelve el elemento menor de un iterable, con el mismo `key` que
`max()`. En el capítulo se llama dos veces sobre la misma lista de
medios de transporte para encontrar, por separado, el más rápido y el
más barato.

**¿Qué retorna?**

El elemento (no el valor que devuelve `key`).

**Ejemplos típicos:**

```python
mas_rapido = min(medios, key=lambda medio: medio.tiempo_estimado(km))
mas_barato = min(medios, key=lambda medio: medio.costo(km))

return mas_rapido, mas_barato
```

### `print(*objetos, sep=' ', end='\n')`

**¿Qué realiza?**

Escribe valores en la salida estándar. Se usa para mostrar los
resultados de las pruebas, el mensaje de las excepciones capturadas y
el estado de cada objeto (que resuelve su `__str__` según su clase
real).

**¿Qué retorna?**

`None`.

**Ejemplos típicos:**

```python
for vehiculo in [Auto("Ford"), Camion("Scania"), Moto("Honda")]:
    print(vehiculo)

print(f"Error: {error}")
```

### `sum(iterable)`

**¿Qué realiza?**

Suma los elementos de un iterable numérico. Se combina con una
expresión generadora que le pide un número a cada objeto: subtotales de
un pedido, notas de un alumno, precios finales de una lista de ítems,
saldos de las cuentas de un banco.

**¿Qué retorna?**

La suma total.

**Ejemplos típicos:**

```python
def total(self):
    return sum(
        precio * cantidad
        for _, precio, cantidad in self._lineas
    )

def total_depositado(self) -> float:
    return sum(cuenta.saldo for cuenta in self.listar())
```

### `type(objeto)`

**¿Qué realiza?**

Retorna la clase real de un objeto. Como en el capítulo 11, casi
siempre se usa `type(algo).__name__` para obtener el nombre de la clase
concreta: en un `__str__` heredado y en los mensajes que informan qué
tipo resultó más rápido o más barato. La teoría lo repasa con
`type(self).__name__`; en los ejercicios también aparece sobre
variables locales y parámetros.

**¿Qué retorna?**

La clase. `type(objeto).__name__` es un `str`.

**Ejemplos típicos:**

```python
print(f"Más rápido: {type(rapido).__name__}")

def __str__(self):
    return f"{type(self).__name__} {self._marca}: ..."
```

---

## Métodos de Strings (Cadenas de Texto)

### `separador.join(iterable_de_strings)`

**¿Qué realiza?**

Une los elementos de un iterable de strings intercalando el string
sobre el que se invoca. En el capítulo arma un texto o un CSV con una
línea por elemento y las pega con `"\n"` en el medio, sin dejar un
salto de línea al final.

**¿Qué retorna?**

Un nuevo string.

**Ejemplos típicos:**

```python
def exportar(self, pedido):
    lineas = [f"pedido,{pedido.numero()},{pedido.cliente()}"]
    for descripcion, precio, cantidad in pedido.lineas():
        lineas.append(f"{descripcion},{precio},{cantidad}")
    return "\n".join(lineas)

return "\n".join(elemento.a_csv() for elemento in elementos)
```

---

## Métodos de Listas

### `list.append(elemento)`

**¿Qué realiza?**

Agrega `elemento` al final de la lista, en el lugar. Aparece al sumar
una línea a un pedido, un vértice a un polígono, una parada a una ruta
o un movimiento al historial de una cuenta.

**¿Qué retorna?**

`None`.

**Ejemplos típicos:**

```python
def agregar(self, descripcion, precio, cantidad):
    self._lineas.append((descripcion, precio, cantidad))

def _registrar(self, tipo: str, monto: float) -> None:
    self._movimientos.append(Movimiento(tipo, monto, self._saldo))
```

---

## El Diccionario como Colección Interna

Varias clases del capítulo guardan sus objetos en un diccionario
indexado por identificador (`{isbn: Libro}`, `{numero: Cuenta}`), igual
que en el capítulo 12. Se resume acá el acceso que se usa.

### `diccionario[clave] = valor` / `diccionario.get(clave)`

**¿Qué realiza?**

`d[clave] = valor` da de alta o reemplaza; `d.get(clave)` devuelve el
valor o `None` si la clave no está, sin lanzar `KeyError`. El patrón de
búsqueda es pedir con `.get()` y, si vino `None`, lanzar una excepción
propia.

**Ejemplos típicos:**

```python
def agregar_libro(self, libro: Libro) -> None:
    self._libros[libro.isbn()] = libro

def buscar_por_isbn(self, isbn: str) -> Libro:
    libro = self._libros.get(isbn)
    if libro is None:
        raise LibroNoEncontrado(f"No hay libro con ISBN {isbn}")
    return libro
```

### `diccionario.values()`

**¿Qué realiza?**

Devuelve una vista de los valores (los objetos guardados), para
recorrerlos o convertirlos en lista con `list()`.

**Ejemplos típicos:**

```python
def listar(self) -> list[Libro]:
    return list(self._libros.values())

def todas(self) -> list[Cuenta]:
    return list(self._cuentas.values())
```

---

## Módulo `math`

Requiere `import math`. La teoría no desarrolla el módulo (es el tema
del capítulo 14); acá aparece solo en las fórmulas geométricas de
algunos ejercicios.

### `math.pi`

**¿Qué realiza?**

Constante con el valor de π. Se usa en el área y el perímetro del
círculo y en la fórmula del área del pentágono regular.

**Ejemplos típicos:**

```python
def area(self) -> float:
    return math.pi * self._radio ** 2

def perimetro(self) -> float:
    return 2 * math.pi * self._radio
```

### `math.sqrt(x)`

**¿Qué realiza?**

Devuelve la raíz cuadrada de `x`. Se usa en la fórmula de Herón para el
área de un triángulo a partir de sus tres lados.

**¿Qué retorna?**

Un `float`.

**Ejemplos típicos:**

```python
def area(self) -> float:
    semi = self.perimetro() / 2
    return math.sqrt(
        semi
        * (semi - self._lado_a)
        * (semi - self._lado_b)
        * (semi - self._lado_c)
    )
```

### `math.tan(x)`

**¿Qué realiza?**

Devuelve la tangente de `x`, con `x` en radianes. En el capítulo
`math.tan(math.pi / 5)` aparece en el denominador de la fórmula del
área del pentágono regular.

**¿Qué retorna?**

Un `float`.

**Ejemplos típicos:**

```python
def area(self) -> float:
    numerador = 5 * self._lado ** 2
    denominador = 4 * math.tan(math.pi / 5)
    return numerador / denominador
```

---

## Módulo `inspect`

### `inspect.getsource(objeto)`

**¿Qué realiza?**

Devuelve, como string, el código fuente de una función o clase.
Requiere `import inspect`. En el capítulo se usa para **demostrar
OCP**: se guarda el fuente de `area_total()` antes y después de agregar
una figura nueva y se comprueba con `assert` que no cambió ni una
línea.

**¿Qué retorna?**

Un `str` con el código fuente.

**Ejemplos típicos:**

```python
codigo_antes = inspect.getsource(area_total)
# ... se agrega Pentagono y se vuelve a calcular ...
codigo_despues = inspect.getsource(area_total)
assert codigo_antes == codigo_despues, (
    "area_total no debería haber cambiado"
)
```

---

## Módulo `typing`

Requiere `from typing import ...`. La teoría del capítulo explica los
type hints básicos, `Optional` y `Protocol` / `@runtime_checkable`;
acá se listan las tres piezas que los ejercicios usan y que la teoría
no desarrolla: `Any`, `Callable` y `TypeVar`. No cambian el
comportamiento en tiempo de ejecución, son ayudas para la anotación.

### `Any`

**¿Qué realiza?**

Es el tipo "cualquier cosa": apaga la verificación para ese valor.
En el capítulo aparece cuando una función guarda o transporta datos
sin importarle su tipo (un repositorio genérico que persiste un
diccionario).

**¿Qué retorna?**

No retorna: se usa solo como anotación, por ejemplo `dict[str, Any]`
o `Optional[Any]`.

**Ejemplos típicos:**

```python
from typing import Any, Optional

def guardar(self, clave: str, valor: Any) -> None:
    self._datos[clave] = valor

def obtener(self, clave: str) -> Optional[Any]:
    return self._datos.get(clave)
```

### `Callable[[params], retorno]`

**¿Qué realiza?**

Anota que un parámetro es "algo que se puede llamar" (una función, un
método, un `lambda`), indicando entre corchetes los tipos de los
argumentos y, después, el tipo que devuelve. `Callable[[T], bool]` es
"una función que recibe un `T` y devuelve `bool`".

**¿Qué retorna?**

No retorna: se usa solo como anotación.

**Ejemplos típicos:**

```python
from typing import Callable, TypeVar

T = TypeVar("T")

def filtrar(elementos: list[T], condicion: Callable[[T], bool]) -> list[T]:
    return [elemento for elemento in elementos if condicion(elemento)]


aprobados = filtrar(alumnos, lambda a: a.promedio() >= 6)
```

### `TypeVar("T")`

**¿Qué realiza?**

Declara un **tipo variable** (un genérico). Sirve para decir "el tipo
que entra es el mismo que sale": `filtrar(list[T], ...) -> list[T]`
conserva el tipo de los elementos, sea cual sea.

**¿Qué retorna?**

Devuelve un objeto `TypeVar` que se usa dentro de otras anotaciones.

**Ejemplos típicos:**

```python
from typing import Callable, TypeVar

T = TypeVar("T")

def primero_que_cumpla(
    elementos: list[T],
    condicion: Callable[[T], bool],
) -> T:
    for elemento in elementos:
        if condicion(elemento):
            return elemento
    raise ValueError("Ninguno cumple la condición")
```

---

## Tipos de Excepción

### `Exception`

**¿Cuándo se produce?**

Es la clase base de todas las excepciones. No se lanza directo: se
hereda de ella para **definir excepciones propias** del dominio, como
se hizo en el capítulo 12.

**Ejemplos típicos:**

```python
class LibroNoEncontrado(Exception):
    """Indica que no existe un libro con ese ISBN."""
    pass
```

### `TypeError`

**¿Cuándo se produce?**

Al intentar instanciar una clase abstracta: una `ABC` que todavía
tiene métodos `@abstractmethod` sin implementar. Pasa tanto con la
clase base como con una hija que se olvidó de implementar alguno. Los
ejercicios lo capturan para mostrar que `abc` **impide crear el
objeto**, a diferencia de `NotImplementedError`, que recién avisa al
llamar al método.

**Ejemplos típicos:**

```python
try:
    Instrumento("cualquiera")
except TypeError as error:
    print(f"Instrumento es abstracta: {error}")

try:
    Bateria("Ludwig")            # no implementa afinar()
except TypeError as error:
    print(f"Bateria quedó incompleta: {error}")
```

### `ValueError`

**¿Cuándo se produce?**

Cuando un valor es del tipo correcto pero no es válido. En el capítulo
lo lanza el `__post_init__` de una dataclass al validar los datos
apenas se construye el objeto.

**Ejemplos típicos:**

```python
@dataclass(unsafe_hash=True)
class Producto:
    codigo: str
    nombre: str = field(compare=False)
    precio: float = field(compare=False)
    stock: int = field(compare=False)

    def __post_init__(self):
        if self.precio <= 0:
            raise ValueError("El precio debe ser positivo")
```

### Excepciones personalizadas

**¿Cuándo se producen?**

Cuando el error pertenece al dominio del problema. Se definen heredando
de `Exception`, con cuerpo `pass` o un docstring, tal como en el
capítulo 12. En este capítulo aparecen sobre todo en la iteración 5
del banco.

Familias que aparecen:

| Excepción | Se lanza cuando... |
| --------- | ------------------ |
| `LibroNoEncontrado`, `CuentaNoEncontrada` | se busca por identificador y no existe |
| `NumeroDuplicadoError` | el alta usa un número de cuenta ya tomado |
| `SaldoInsuficienteError`, `MontoInvalidoError` | la operación bancaria no es válida |
| `CuentaBloqueadaError` | se opera sobre una cuenta bloqueada |

**Ejemplos típicos:**

```python
try:
    sueldo.extraer(999999)
except SaldoInsuficienteError as error:
    print(f"Error: {error}")
```

---

## Construcciones del Lenguaje

### Herencia múltiple de interfaces (ABCs puras)

**¿Qué realiza?**

Una clase hereda de **varias** `ABC` a la vez, cuando cada una declara
una sola capacidad (ISP). Es la única herencia múltiple que usa el
manual: las bases son ABCs sin estado ni `__init__` propio, o sea
interfaces, así que no hay implementación que resolver ni "problema del
diamante".

**Ejemplos típicos:**

```python
class Humano(SabeTrabajar, NecesitaDescanso, RecibeRemuneracion):
    def trabajar(self) -> None: ...
    def comer(self) -> None: ...
    def dormir(self) -> None: ...
    def cobrar_sueldo(self) -> None: ...


class MultifuncionVieja(Impresora, Escaner, Fax):
    ...
```

### `lambda` como criterio de `min()` / `max()` y como filtro

**¿Qué realiza?**

Una función anónima de una línea. Se pasa como `key` a `min()` y
`max()` para decir por qué atributo comparar, y como criterio a una
función de filtrado.

**Ejemplos típicos:**

```python
mas_rapido = min(medios, key=lambda medio: medio.tiempo_estimado(km))

mejor = max(formas, key=lambda forma: forma.area())

aprobados = filtrar(alumnos, lambda a: a.promedio() >= 6)
```

### Expresión generadora en `sum()`

**¿Qué realiza?**

Recorre una colección y produce un número por cada objeto, sin armar
una lista intermedia, para que `sum()` lo totalice.

**Ejemplos típicos:**

```python
return sum(precio * cantidad for _, precio, cantidad in self._lineas)

return sum(item.precio_final() for item in items)
```

### Concatenación de listas con `+`

**¿Qué realiza?**

`lista + [elemento]` devuelve una lista nueva con el elemento agregado,
sin tocar la original. En el capítulo sirve para probar OCP: se arma la
lista extendida sin modificar la lista de formas originales.

**Ejemplos típicos:**

```python
originales = [Circulo(5), Rectangulo(4, 6)]
extendidas = originales + [Pentagono(3)]
```

### Devolver y desempaquetar una tupla

**¿Qué realiza?**

Una función devuelve varios valores separados por coma (una tupla) y
quien la llama los recibe en varias variables. El tipo se anota como
`tuple[...]`.

**Ejemplos típicos:**

```python
def mejor_opcion(
    km: float,
    medios: list[MedioTransporte],
) -> tuple[MedioTransporte, MedioTransporte]:
    ...
    return mas_rapido, mas_barato


rapido, barato = mejor_opcion(500, [Bicicleta(), Auto(), Avion()])
```

### `_` como variable de descarte

**¿Qué realiza?**

Un guion bajo como nombre indica "este valor no me interesa". Aparece
al desempaquetar una tupla de la que solo se usan algunos campos.

**Ejemplos típicos:**

```python
return sum(
    precio * cantidad
    for _, precio, cantidad in self._lineas   # se ignora la descripción
)
```

### Valores por defecto en parámetros

**¿Qué realiza?**

Un parámetro puede tener un valor que se usa si no se pasa. Las cuentas
nacen con saldo `0`; la cuenta corriente, con un descubierto de `50000`
salvo que se indique otro.

**Ejemplos típicos:**

```python
class Cuenta(ABC):
    def __init__(self, numero: str, titular: str, saldo: float = 0) -> None:
        ...

class CuentaCorriente(Cuenta):
    def __init__(self, numero, titular, saldo=0, descubierto=50000):
        super().__init__(numero, titular, saldo)
        self._descubierto = descubierto
```

### `super().__init__(...)` con los argumentos reacomodados

**¿Qué realiza?**

La hija llama al constructor del padre (repaso del capítulo 11). Acá
aparece pasando un mismo valor dos veces
(`super().__init__(lado, lado)`) o reenviando varios parámetros tal
cual.

**Ejemplos típicos:**

```python
class CuadradoMalModelado(RectanguloMutable):
    def __init__(self, lado: float) -> None:
        super().__init__(lado, lado)
```

### `if __name__ == "__main__":`

**¿Qué realiza?**

`__name__` vale `"__main__"` cuando el archivo se ejecuta directo. La
prueba va adentro de este `if` para que corra al ejecutar el archivo
pero no al importarlo. Todos los archivos del capítulo lo usan.

**Ejemplos típicos:**

```python
if __name__ == "__main__":
    verificar_liskov([CuentaAhorro, CuentaCorriente])
```

### f-strings y formato de valores

**¿Qué realiza?**

Incrustan expresiones en un string. Además de `{valor:.2f}` (dos
decimales), en el capítulo aparecen la **alineación** en ancho fijo
(`{x:<12}` a la izquierda, `{x:>10}` a la derecha) y el separador de
miles `{x:,}`, para alinear las columnas de un historial de
movimientos.

**Ejemplos típicos:**

```python
def __str__(self) -> str:
    return (
        f"{self.tipo:<12} ${self.monto:>10,.2f} "
        f"-> ${self.saldo_resultante:,.2f}"
    )

return (
    f"[{self._numero}] {type(self).__name__} de "
    f"{self._titular}: ${self._saldo:,.2f}"
)
```

---

## Resumen por Categoría

| Categoría | Elementos |
| --------- | --------- |
| **Funciones built-in** | `getattr`, `hasattr`, `isinstance`, `len`, `list`, `max`, `min`, `print`, `sum`, `type` |
| **Métodos de `str`** | `join` |
| **Métodos de `list`** | `append` |
| **Diccionario como colección** | `d[clave] = v`, `d.get(clave)`, `d.values()` |
| **Módulo `math`** | `math.pi`, `math.sqrt`, `math.tan` |
| **Módulo `inspect`** | `inspect.getsource` |
| **Módulo `typing`** | `Any`, `Callable`, `TypeVar` (los básicos, `Optional` y `Protocol` los explica la teoría) |
| **Tipos de excepción** | `Exception`, `TypeError` (instanciar una ABC), `ValueError` (`__post_init__`), y las excepciones personalizadas del capítulo 12 |
| **Construcciones del lenguaje** | herencia múltiple de interfaces, `lambda` en `min`/`max`/filtro, expresión generadora en `sum()`, concatenación de listas `+`, devolver/desempaquetar tuplas, `_` de descarte, valores por defecto, `super().__init__()` reacomodado, `if __name__ == "__main__":`, f-strings (`:.2f`, `:<12`, `:>10`, `:,`) |

---

## Notas Importantes

- **`abc` impide crear el objeto; `NotImplementedError` solo avisa.**
  Instanciar una `ABC` con métodos abstractos sin implementar lanza
  `TypeError` en el momento de la construcción. La versión del
  capítulo 11 (`raise NotImplementedError` en el cuerpo) deja crear el
  objeto y falla recién al llamar al método.

- **`min()` y `max()` con `key` son polimorfismo.** El bucle interno
  que recorre la lista no tiene `if` por tipo: le pide `area()` o
  `tiempo_estimado()` a cada objeto y compara los resultados. Agregar
  una clase nueva no toca la función de búsqueda.

- **`getattr(Clase, "saldo")` mira la clase, no la instancia.** Para
  comprobar que algo es una `property` de verdad hay que buscar el
  descriptor en la clase; `instancia.saldo` ya devolvería el número y
  cualquier atributo común pasaría la prueba.

- **`hasattr()` confirma que ISP se aplicó bien.** Si partir la
  interfaz gorda salió como corresponde, la clase que no cumple una
  capacidad directamente **no tiene** ese método, en vez de tenerlo y
  que lance una excepción.

- **`assert` está explicado en la teoría** y se usa en varios
  ejercicios como verificación de contrato (`verificar_liskov`,
  `probar_ocp`, `verificar_contrato`). Recordá que `python -O` los
  saltea: no sirven para validar datos en producción.

- **`inspect.getsource()` es una curiosidad para demostrar OCP**, no
  algo de uso diario: sirve para "probar" que una función no fue
  modificada al extender el sistema.

- **`Any`, `Callable` y `TypeVar` son solo anotaciones.** No hacen
  nada en tiempo de ejecución: Python no verifica los tipos. `TypeVar`
  sirve para escribir funciones genéricas que conservan el tipo de
  entrada (`list[T] -> list[T]`), y `Callable` para anotar un
  parámetro que es una función o un `lambda`.

- **Las excepciones propias son las del capítulo 12.** SOLID no cambia
  el patrón: heredar de `Exception`, lanzar con un mensaje claro,
  capturar con `except ... as error`.

- **`"\n".join(lista)` arma el texto de una sola vez**, en lugar de ir
  concatenando con `+` dentro de un bucle. Se llena una lista con una
  línea por elemento y al final se pegan todas.
