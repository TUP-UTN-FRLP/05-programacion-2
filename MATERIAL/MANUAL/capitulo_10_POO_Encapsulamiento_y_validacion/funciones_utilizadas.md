# Funciones Utilizadas en capitulo_10_POO_Encapsulamiento_y_validacion

Documento que agrupa las funciones built-in, los métodos, los módulos,
los tipos de excepción y las construcciones del lenguaje utilizados en
los ejercicios y enunciados, organizados por tipo y en orden
alfabético.

Este capítulo continúa la Programación Orientada a Objetos y se centra
en el **encapsulamiento** y la **validación**: atributos privados por
convención (`_nombre`), `@property` y sus setters para controlar el
acceso, validación de tipo y de valor con `raise`, y la creación de
excepciones propias del dominio.

---

## Funciones Generales

### `any(iterable)`

**¿Qué realiza?**

Retorna `True` si al menos uno de los elementos del iterable es
verdadero. Se detiene apenas encuentra el primero. Se usa junto a una
expresión generadora para comprobar si algún carácter de un string
cumple una condición (por ejemplo, si hay al menos un dígito).

**¿Qué retorna?**

Un valor de tipo `bool`.

**Ejemplos típicos:**

```python
# ¿Hay al menos un dígito en la contraseña?
if not any(c.isdigit() for c in valor):
    raise ContraseñaDebilError("Debe contener al menos un dígito")

# ¿Hay al menos una mayúscula?
if not any(caracter.isupper() for caracter in valor):
    raise ClaveSinMayusculaError("Debe tener al menos una mayúscula")
```

### `isinstance(objeto, clase)`

**¿Qué realiza?**

Verifica si un objeto es una instancia de una clase (o de una tupla de
clases). Es la forma habitual de validar el tipo de un valor recibido
antes de guardarlo.

Acepta una tupla como segundo argumento para admitir varios tipos:
`isinstance(valor, (int, float))`.

**¿Qué retorna?**

Un valor de tipo `bool`.

**Ejemplos típicos:**

```python
if not isinstance(nombre, str) or not nombre.strip():
    raise ValueError("El nombre debe ser un string no vacío")

if not isinstance(valor, (int, float)):
    raise TypeError("El precio debe ser un número")

if not isinstance(x, (int, float)):
    raise TypeError("x debe ser numérico")
```

### `len(colección)`

**¿Qué realiza?**

Retorna la cantidad de elementos de una colección o la longitud de un
string. En este capítulo se usa para validar longitudes mínimas
(contraseñas, números de tarjeta, DNI) y para calcular promedios.

**¿Qué retorna?**

Un valor de tipo `int`.

**Ejemplos típicos:**

```python
if len(valor) < 8:
    raise ContraseñaDebilError("Debe tener al menos 8 caracteres")

if not (isinstance(numero, str) and len(numero) == 16 and numero.isdigit()):
    raise ValueError("Número inválido: debe ser 16 dígitos")

if len(dni) not in (7, 8):
    raise ValueError("DNI debe ser 7 u 8 dígitos numéricos")
```

### `max(iterable)`

**¿Qué realiza?**

Retorna el elemento más grande de un iterable. Se usa en la property
`mejor_nota` sobre la lista interna de notas.

**¿Qué retorna?**

El mayor de los elementos.

**Errores posibles:**

Lanza `ValueError` si el iterable está vacío. Por eso la property
comprueba antes `if not self._notas` y devuelve `None`.

**Ejemplos típicos:**

```python
@property
def mejor_nota(self):
    if not self._notas:
        return None
    return max(self._notas)
```

### `print(*objetos, sep=' ', end='\n')`

**¿Qué realiza?**

Escribe uno o varios valores en la salida estándar. En este capítulo
se usa sobre todo para mostrar el mensaje de las excepciones
capturadas (`print(f"Error: {error}")`) y para verificar el estado de
los objetos.

**¿Qué retorna?**

`None`.

**Ejemplos típicos:**

```python
print(f"Error: {error}")
print(f"${empleado.sueldo_basico:.2f}")
print(f"Área: {circulo.area:.2f}")
```

### `sum(iterable)`

**¿Qué realiza?**

Retorna la suma de los elementos de un iterable numérico. Se usa para
calcular el promedio de notas dentro de una property.

**¿Qué retorna?**

La suma total.

**Ejemplos típicos:**

```python
@property
def promedio(self):
    if not self._notas:
        return 0
    return sum(self._notas) / len(self._notas)
```

### `type(objeto)`

**¿Qué realiza?**

Retorna la clase exacta de un objeto. En este capítulo se usa en
comparaciones para exigir un tipo **exacto**, sin admitir subclases:
`type(nota) is not int` o `type(valor) not in (int, float)`.

La diferencia con `isinstance()` es importante para el tipo `bool`:
`isinstance(True, int)` es `True` (porque `bool` es subclase de
`int`), pero `type(True) is int` es `False`.

**¿Qué retorna?**

Un objeto de tipo `type` (la clase del objeto).

**Ejemplos típicos:**

```python
if type(nota) is not int:
    raise TypeError("La nota debe ser un número entero")

if type(valor) not in (int, float):
    raise TypeError("El precio debe ser numérico")

if type(cantidad) is not int:
    raise TypeError("La cantidad debe ser un número entero")
```

---

## Métodos de Strings (Cadenas de Texto)

Los siguientes elementos son métodos de la clase `str`. Se invocan
sobre un objeto de tipo string, por ejemplo, `valor.strip()`.

### `string.count(subcadena)`

**¿Qué realiza?**

Cuenta cuántas veces aparece `subcadena` en el string. Se usa para
validar que un email tenga exactamente una `@`.

**¿Qué retorna?**

Un valor de tipo `int`.

**Ejemplos típicos:**

```python
if valor.count("@") != 1:
    raise EmailInvalidoError("Debe tener exactamente una @")
```

### `string.find(subcadena, inicio)`

**¿Qué realiza?**

Busca `subcadena` dentro del string y devuelve la posición de la
primera aparición. Con un segundo argumento, comienza a buscar desde
esa posición. Si no la encuentra, devuelve `-1`.

**¿Qué retorna?**

Un valor de tipo `int`: la posición encontrada, o `-1` si no aparece.

**Ejemplos típicos:**

```python
arroba = valor.find("@")              # posición de la @

# ¿Hay un punto después de la @?
if valor.find(".", arroba) == -1:
    raise EmailInvalidoError("Debe tener un punto después de la @")
```

### `string.isdigit()`

**¿Qué realiza?**

Verifica si todos los caracteres del string son dígitos y el string no
está vacío. Se usa para validar números de tarjeta, DNI y para
comprobar si un carácter suelto es un dígito.

**¿Qué retorna?**

`True` si todos los caracteres son dígitos, `False` en caso contrario.

**Ejemplos típicos:**

```python
if not dni.isdigit() or len(dni) not in (7, 8):
    raise ValueError("DNI debe ser 7 u 8 dígitos numéricos")

# Sobre cada carácter, dentro de any():
if not any(c.isdigit() for c in valor):
    raise ContraseñaDebilError("Debe contener al menos un dígito")
```

### `string.islower()` y `string.isupper()`

**¿Qué realiza?**

`islower()` verifica si el carácter (o string) está en minúscula;
`isupper()`, si está en mayúscula. Se aplican carácter por carácter
dentro de `any()` para validar la fortaleza de una contraseña.

**¿Qué retorna?**

Un valor de tipo `bool`.

**Ejemplos típicos:**

```python
if not any(caracter.isupper() for caracter in valor):
    raise ClaveSinMayusculaError("Debe tener al menos una mayúscula")

if not any(caracter.islower() for caracter in valor):
    raise ClaveSinMinusculaError("Debe tener al menos una minúscula")
```

### `string.strip()`

**¿Qué realiza?**

Devuelve el string sin los espacios en blanco de los extremos. Se usa
para validar que un nombre no esté vacío (`not nombre.strip()` es
`True` si el string solo tenía espacios) y para normalizar el valor
antes de guardarlo.

**¿Qué retorna?**

Un nuevo string.

**Ejemplos típicos:**

```python
if not isinstance(nombre, str) or not nombre.strip():
    raise ValueError("El nombre no puede estar vacío")

self._nombre = nombre.strip()
```

### `string.title()`

**¿Qué realiza?**

Devuelve el string con la primera letra de cada palabra en mayúscula y
el resto en minúscula. Se usa para normalizar nombres y apellidos.

**¿Qué retorna?**

Un nuevo string.

**Ejemplos típicos:**

```python
self._nombre = nombre.strip().title()      # "  ana  " -> "Ana"
self._apellido = apellido.strip().title()  # "pérez" -> "Pérez"
```

---

## Métodos de Listas

Los siguientes elementos son métodos de la clase `list`. Se invocan
sobre una lista que es atributo privado de un objeto, por ejemplo,
`self._notas.append(x)`.

### `list.append(elemento)`

**¿Qué realiza?**

Agrega `elemento` al final de la lista, modificándola en el lugar.
Es la operación que usa `agregar_nota()` una vez que la nota superó
las validaciones.

**¿Qué retorna?**

`None`.

**Ejemplos típicos:**

```python
def agregar_nota(self, nota):
    if type(nota) is not int:
        raise TypeError("La nota debe ser un número entero")
    if not 0 <= nota <= 10:
        raise ValueError("La nota debe estar entre 0 y 10")
    self._notas.append(nota)
```

### `list.pop()`

**¿Qué realiza?**

Sin argumento, elimina el último elemento de la lista y lo devuelve.
Se usa en `borrar_ultima_nota()` para quitar y retornar la nota
eliminada.

**¿Qué retorna?**

El elemento eliminado.

**Errores posibles:**

Lanza `IndexError` si la lista está vacía. Por eso el método verifica
antes `if not self._notas` y lanza un `IndexError` con un mensaje
propio.

**Ejemplos típicos:**

```python
def borrar_ultima_nota(self):
    if not self._notas:
        raise IndexError("No hay notas para borrar")
    return self._notas.pop()
```

---

## Acceso a Diccionarios por Clave

En algunos enunciados se usa un diccionario interno como tabla de
consulta: la cantidad de días de cada mes, o el estado siguiente de un
semáforo. El acceso se hace con `diccionario[clave]`.

**¿Qué realiza?**

Devuelve el valor asociado a `clave`. Lanza `KeyError` si la clave no
existe, por eso el mes se valida **antes** de consultar el
diccionario.

**Ejemplos típicos:**

```python
dias_por_mes = {1: 31, 2: 28, 3: 31, 4: 30, ...}

if not 1 <= mes <= 12:                 # se valida primero
    raise ValueError("Mes fuera de rango (1-12)")

maximo_dias = dias_por_mes[mes]        # ahora la clave existe seguro

# Tabla de transiciones de estado:
transiciones = {"verde": "amarillo", "amarillo": "rojo", "rojo": "verde"}
siguiente_estado = transiciones[self._estado]
```

---

## Módulo `datetime`

### `datetime.now()`

**¿Qué realiza?**

Retorna un objeto `datetime` con la fecha y hora actuales del sistema.
Requiere `from datetime import datetime`. En el capítulo se usan sus
atributos `.year` y `.month` para comprobar si una tarjeta está
vencida.

**¿Qué retorna?**

Un objeto `datetime`. `.year` y `.month` son enteros.

**Ejemplos típicos:**

```python
from datetime import datetime

hoy = datetime.now()

if anio_vencimiento < hoy.year or (
    anio_vencimiento == hoy.year and mes_vencimiento < hoy.month
):
    raise TarjetaVencidaError(
        f"Tarjeta vencida en {mes_vencimiento}/{anio_vencimiento}"
    )
```

---

## Módulo `math`

### `math.pi`

**¿Qué realiza?**

Constante con el valor de π. Requiere `import math`. Se usa en las
properties calculadas `area` y `perimetro` de la clase `Circulo`.

**Ejemplos típicos:**

```python
import math

@property
def area(self):
    return math.pi * self._radio ** 2

@property
def perimetro(self):
    return 2 * math.pi * self._radio
```

---

## Tipos de Excepción

### `AttributeError`

**¿Cuándo se produce?**

Cuando se intenta asignar un valor a una property que solo tiene
getter (no tiene `@<attr>.setter`). Python no encuentra un setter y
lanza `AttributeError`. Es la forma en que una property de solo
lectura protege su valor.

**Ejemplos típicos:**

```python
@property
def area(self):
    return math.pi * self._radio ** 2
# No hay @area.setter

try:
    circulo.area = 100
except AttributeError as error:
    print(f"Error: {error}")
```

### `Exception`

**¿Cuándo se produce?**

Es la clase base de todas las excepciones. No se lanza directamente:
se usa como superclase al **definir excepciones propias**.

**Ejemplos típicos:**

```python
class StockInsuficienteError(Exception):
    pass

class ContraseñaDebilError(Exception):
    """Se lanza cuando una contraseña no cumple los requisitos mínimos."""
    pass
```

### `IndexError`

**¿Cuándo se produce?**

Cuando se accede a una posición inexistente de una lista, o al hacer
`pop()` sobre una lista vacía. En el capítulo se lanza además
manualmente para señalar que no hay una "última nota" para borrar.

**Ejemplos típicos:**

```python
def borrar_ultima_nota(self):
    if not self._notas:
        raise IndexError("No hay notas para borrar")
    return self._notas.pop()
```

### `TypeError`

**¿Cuándo se produce?**

Cuando un valor es del tipo equivocado. En este capítulo se lanza
manualmente desde los setters y los métodos al detectar que un
argumento no es del tipo esperado (un precio que no es número, una
nota que no es `int`).

**Ejemplos típicos:**

```python
if not isinstance(valor, (int, float)):
    raise TypeError("El precio debe ser un número")

if type(nota) is not int:
    raise TypeError("La nota debe ser un número entero")
```

### `ValueError`

**¿Cuándo se produce?**

Cuando un valor es del tipo correcto pero está fuera del rango o del
formato permitido. Es la excepción más frecuente del capítulo: se
lanza manualmente desde casi todos los setters y constructores
(precio negativo, mes fuera de 1–12, radio no positivo, nombre vacío).

**Ejemplos típicos:**

```python
if valor <= 0:
    raise ValueError("El radio debe ser mayor que cero")

if not 1 <= mes <= 12:
    raise ValueError("Mes fuera de rango (1-12)")

if valor < 0:
    raise ValueError("El precio no puede ser negativo")
```

### Excepciones personalizadas

**¿Cuándo se producen?**

Cuando el error pertenece al dominio del problema y ninguna excepción
estándar lo describe bien. Se definen como una clase que hereda de
`Exception`, normalmente con cuerpo `pass` o solo un docstring.

Excepciones propias definidas en el capítulo:

| Excepción | Se lanza cuando... |
| --------- | ------------------ |
| `StockInsuficienteError` | se intenta vender más unidades que las disponibles |
| `ContraseñaDebilError` | una contraseña no llega a 8 caracteres o no tiene dígito |
| `EmailInvalidoError` | un email no tiene una sola `@` o no tiene `.` después de la `@` |
| `ClaveCortaError`, `ClaveSinMayusculaError`, `ClaveSinMinusculaError`, `ClaveSinDigitoError` | cada regla de contraseña incumplida, con una excepción distinta por regla |
| `TarjetaVencidaError` | la fecha de vencimiento de una tarjeta ya pasó |
| `LimiteExtraccionSuperadoError` | un monto a extraer supera el límite diario |

**Ejemplos típicos:**

```python
class StockInsuficienteError(Exception):
    pass


class Producto:

    def vender(self, cantidad):
        if cantidad > self.stock:
            raise StockInsuficienteError(
                f"Hay {self.stock} unidades y se pidieron {cantidad}"
            )
        self.stock -= cantidad
```

```python
try:
    p.vender(20)
except StockInsuficienteError as e:
    print("Error:", e)
```

---

## Construcciones del Lenguaje

Las siguientes construcciones son el tema central del capítulo: la
sintaxis de Python para encapsular atributos y validar su valor.

### Atributo privado por convención (`_nombre`)

**¿Qué realiza?**

Un guion bajo al inicio del nombre de un atributo (`self._edad`) indica
que ese atributo es de uso interno de la clase. **Python no impide el
acceso**: es una convención. Acceder a `persona._edad` desde afuera
funciona técnicamente, pero rompe el contrato de la clase.

**Ejemplos típicos:**

```python
class Persona:

    def __init__(self, nombre, edad):
        self.nombre = nombre
        self._edad = edad          # interno por convención

persona = Persona("Ana", 30)
print(persona._edad)               # funciona, pero no se debería
persona._edad = -5                 # nada lo impide: por eso hacen falta properties
```

### Name mangling (`__nombre`) — por qué NO se usa

**¿Qué realiza?**

Dos guiones bajos al inicio (`self.__edad`) activan el *name mangling*:
Python renombra internamente el atributo a `_Clase__edad` para evitar
colisiones de nombres en la herencia. En este capítulo **no se usa**:
para marcar un atributo como interno alcanza con un solo guion bajo.

**Ejemplos típicos:**

```python
# Se usa esto:
self._x = x

# NO esto (name mangling, reservado para casos de herencia):
# self.__x = x
```

### `@property` — El getter

**¿Qué realiza?**

Convierte un método en un atributo de solo lectura de cara al exterior.
Se consulta sin paréntesis (`circulo.radio`, no `circulo.radio()`).
Normalmente devuelve el atributo interno correspondiente (`self._radio`).

**Sintaxis:**

```python
@property
def radio(self):
    return self._radio
```

**Ejemplos típicos:**

```python
class Circulo:

    def __init__(self, radio):
        self.radio = radio

    @property
    def radio(self):
        return self._radio


c = Circulo(5)
print(c.radio)     # 5  (sin paréntesis)
```

### `@<atributo>.setter` — El setter con validación

**¿Qué realiza?**

Define qué ocurre cuando se **asigna** un valor a la property
(`circulo.radio = 10`). Es el lugar donde se valida el valor antes de
guardarlo en el atributo interno. Si el valor es inválido, lanza una
excepción y no se guarda nada.

**Sintaxis:**

```python
@<atributo>.setter
def <atributo>(self, valor):
    if <valor inválido>:
        raise ValueError("...")
    self._<atributo> = valor
```

**Ejemplos típicos:**

```python
@radio.setter
def radio(self, valor):
    if valor <= 0:
        raise ValueError("El radio debe ser mayor que cero")
    self._radio = valor


@precio.setter
def precio(self, valor):
    if not isinstance(valor, (int, float)):
        raise TypeError("El precio debe ser un número")
    if valor < 0:
        raise ValueError("El precio no puede ser negativo")
    self._precio = valor
```

### Property de solo lectura

**¿Qué realiza?**

Una property que tiene `@property` (getter) pero **no** tiene setter.
Se puede consultar pero no asignar: intentar `objeto.x = ...` lanza
`AttributeError`. Sirve para exponer un dato que solo la clase puede
cambiar (`ventas_totales`, `nombre`, `leido`, `limite_diario`).

**Ejemplos típicos:**

```python
@property
def ventas_totales(self):
    return self._ventas_totales
# No hay @ventas_totales.setter

try:
    producto.ventas_totales = 100
except AttributeError as error:
    print(f"Error: {error}")
```

### Property calculada

**¿Qué realiza?**

Una property de solo lectura que no devuelve un atributo guardado, sino
que **calcula** su valor en cada consulta a partir de otros atributos.
No existe un `self._area`: se recalcula cada vez. Así, si cambia el
radio, el área queda automáticamente actualizada.

**Ejemplos típicos:**

```python
@property
def area(self):
    return math.pi * self._radio ** 2

@property
def diametro(self):
    return 2 * self._radio

@property
def nombre_completo(self):
    return f"{self._apellido}, {self._nombre}"
```

### Validación en el `__init__` vs. validación en el setter

**¿Qué realiza?**

Hay dos lugares para validar:

- **En el setter:** cuando el atributo es una property con setter, el
  `__init__` asigna con `self.precio = precio` (sin guion bajo). Esto
  ejecuta el setter, así que la validación corre también al crear el
  objeto. Una sola regla, un solo lugar.
- **En el `__init__` directamente:** cuando el atributo es de solo
  lectura (no tiene setter), la validación se escribe en el
  constructor antes de guardar en `self._x`.

**Ejemplos típicos:**

```python
class Producto:

    def __init__(self, nombre, precio, stock):
        # nombre es de solo lectura: se valida acá
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser un string no vacío")
        self.nombre = nombre
        # precio y stock son properties: el setter valida
        self.precio = precio
        self.stock = stock
```

```python
class Punto:

    def __init__(self, x, y):
        # x e y son de solo lectura: se validan acá, no hay setter
        if not isinstance(x, (int, float)):
            raise TypeError("x debe ser numérico")
        if not isinstance(y, (int, float)):
            raise TypeError("y debe ser numérico")
        self._x = x
        self._y = y
```

### `raise` — Lanzar una excepción manualmente

**¿Qué realiza?**

Interrumpe la ejecución del método y lanza una excepción. En este
capítulo se usa dentro de setters, constructores y métodos para
rechazar valores inválidos. La ejecución se detiene en el `raise`: el
código posterior (incluida la asignación `self._x = valor`) no se
ejecuta.

**Sintaxis:**

```python
raise TipoDeError("Mensaje descriptivo")
```

**Ejemplos típicos:**

```python
if valor <= 0:
    raise ValueError("La base debe ser positiva")

if cantidad > self.stock:
    raise StockInsuficienteError(
        f"Hay {self.stock} unidades y se pidieron {cantidad}"
    )

if porcentaje <= 0:
    raise ValueError("El porcentaje debe ser positivo")
```

### Definir una excepción personalizada

**¿Qué realiza?**

Crea un nuevo tipo de excepción heredando de `Exception`. El cuerpo
suele ser solo `pass` o un docstring. Permite capturar exactamente ese
error (`except StockInsuficienteError`) sin atrapar otros.

**Sintaxis:**

```python
class NombreError(Exception):
    pass
```

**Ejemplos típicos:**

```python
class EmailInvalidoError(Exception):
    """Se lanza cuando un email no tiene formato válido."""
    pass


class LimiteExtraccionSuperadoError(Exception):
    """Se lanza cuando una extracción supera el límite diario."""
    pass
```

### `try/except` para capturar la validación

**¿Qué realiza?**

Rodea el código que puede lanzar una excepción de validación (crear un
objeto, asignar a una property, llamar a un método) y captura el error
para mostrar su mensaje sin cortar el programa con el traceback.

**Ejemplos típicos:**

```python
try:
    c.radio = -3
except ValueError as e:
    print("Error:", e)

try:
    Circulo(0)
except ValueError as e:
    print("Error:", e)

# Varias excepciones a la vez:
try:
    Producto(*datos)
except (TypeError, ValueError) as e:
    print("Error:", e)
```

### Comparación encadenada (`1 <= x <= 12`)

**¿Qué realiza?**

Permite escribir un rango en una sola expresión, tal como en
matemática. Equivale a `1 <= x and x <= 12`. Combinada con `not` se usa
para detectar valores fuera de rango.

**Ejemplos típicos:**

```python
if not 1 <= mes <= 12:
    raise ValueError("Mes fuera de rango (1-12)")

if not 0 <= nota <= 10:
    raise ValueError("La nota debe estar entre 0 y 10")

if not 1 <= dia <= maximo_dias:
    raise ValueError(f"Día fuera de rango para el mes {mes}")
```

### `any()` con expresión generadora

**¿Qué realiza?**

Recorre los caracteres de un string y comprueba si alguno cumple una
condición, sin construir una lista intermedia. Es el patrón para
validar la composición de una contraseña.

**Ejemplos típicos:**

```python
if not any(c.isdigit() for c in valor):
    raise ContraseñaDebilError("Debe contener al menos un dígito")

if not any(caracter.isupper() for caracter in valor):
    raise ClaveSinMayusculaError("Debe tener al menos una mayúscula")
```

### Valores por defecto en parámetros

**¿Qué realiza?**

Un parámetro del `__init__` (o de un método) puede tener un valor por
defecto que se usa si no se pasa al crear el objeto.

**Ejemplos típicos:**

```python
class Cajero:
    def __init__(self, limite_diario=100000):
        ...

class Producto:
    def __init__(self, nombre, precio, stock=0):
        ...

cajero = Cajero()             # usa 100000
especial = Cajero(250000)     # usa 250000
```

### Expresión condicional inline (`a if cond else b`)

**¿Qué realiza?**

Elige entre dos valores en una sola expresión. Se usa dentro de
`__str__` para mostrar un texto u otro según un booleano.

**Ejemplos típicos:**

```python
def __str__(self):
    estado = "leído" if self._leido else "sin leer"
    return f"'{self._titulo}' de {self._autor} ({self._paginas} páginas, {estado})"
```

### f-strings y formato de valores

**¿Qué realiza?**

Incrustan expresiones dentro de un string. En el capítulo se usan para
armar los mensajes de las excepciones y para mostrar números con dos
decimales (`{valor:.2f}`) o con ceros a la izquierda (`{valor:02d}`).

**Ejemplos típicos:**

```python
raise ValueError(f"Día fuera de rango para el mes {mes}")
raise LimiteExtraccionSuperadoError(f"El límite diario es ${self._limite_diario:.2f}")

print(f"${empleado.sueldo_basico:.2f}")
return f"{self._dia:02d}/{self._mes:02d}/{self._anio}"
```

---

## Resumen por Categoría

| Categoría | Elementos |
| --------- | --------- |
| **Funciones built-in** | `any`, `isinstance`, `len`, `max`, `print`, `sum`, `type` |
| **Métodos de `str`** | `count`, `find`, `isdigit`, `islower`, `isupper`, `strip`, `title` |
| **Métodos de `list`** | `append`, `pop` |
| **Acceso a `dict`** | indexación por clave (`d[clave]`) |
| **Módulo `datetime`** | `datetime.now` (`.year`, `.month`) |
| **Módulo `math`** | `math.pi` |
| **Tipos de excepción** | `AttributeError`, `Exception`, `IndexError`, `TypeError`, `ValueError`, y excepciones personalizadas (`StockInsuficienteError`, `ContraseñaDebilError`, `EmailInvalidoError`, `ClaveCortaError` y familia, `TarjetaVencidaError`, `LimiteExtraccionSuperadoError`) |
| **Construcciones del lenguaje** | atributo privado `_nombre`, name mangling `__nombre` (no usado), `@property`, `@<attr>.setter`, property de solo lectura, property calculada, validación en `__init__` vs. setter, `raise`, definir excepción personalizada, `try/except`, comparación encadenada, `any()` con generador, valores por defecto en parámetros, expresión condicional inline, f-strings con formato |

---

## Notas Importantes

- **El guion bajo no protege nada: la property sí.** `_edad` es solo
  una señal para el programador. Lo que realmente impide guardar un
  valor inválido es el setter, que valida antes de asignar.

```python
# Sin property: nada frena esto
persona._edad = -5

# Con property y setter: el setter lanza ValueError y no guarda nada
persona.edad = -5   # -> ValueError
```

- **En `__init__`, asignar a la property (sin guion bajo) hace que el
  setter valide al crear el objeto.** Escribir `self.radio = radio`
  ejecuta el setter; escribir `self._radio = radio` lo saltea y deja
  pasar valores inválidos.

```python
def __init__(self, radio):
    self.radio = radio     # pasa por el setter (valida)
    # self._radio = radio  # NO: saltea la validación
```

- **Property de solo lectura = getter sin setter.** Si no se define
  `@x.setter`, cualquier asignación `objeto.x = ...` lanza
  `AttributeError`. Es lo que se quiere para `area`, `nombre`,
  `ventas_totales`, etc.

- **Una property calculada no se guarda.** `area`, `perimetro`,
  `diametro` y `nombre_completo` se recalculan en cada consulta a
  partir de otros atributos. No hace falta actualizarlas cuando cambia
  el radio o el nombre: siempre reflejan el estado actual.

- **`raise` corta la ejecución.** Cuando una validación falla y lanza
  una excepción, el `self._x = valor` que viene después no se ejecuta.
  Por eso, tras un intento rechazado, el objeto conserva su valor
  anterior.

- **`isinstance` vs. `type(x) is int`.** `isinstance` admite
  subclases; `type(x) is int` exige el tipo exacto. La diferencia
  importa con `bool`: `isinstance(True, int)` es `True`, pero
  `type(True) is int` es `False`. Los enunciados que no quieren
  aceptar `True` como número usan `type(...) is int`.

- **Validar el orden correcto.** Cuando una validación depende de
  otra, el orden importa: hay que validar que `mes` esté entre 1 y 12
  **antes** de hacer `dias_por_mes[mes]`, o la clave podría no existir
  y saltar un `KeyError` en lugar del `ValueError` esperado.

- **Una excepción por regla permite mensajes y manejo distintos.**
  La clase `Password` define `ClaveCortaError`, `ClaveSinMayusculaError`,
  `ClaveSinMinusculaError` y `ClaveSinDigitoError` por separado, así
  quien la usa puede reaccionar de forma diferente a cada
  incumplimiento, o capturarlas todas juntas con una tupla.

```python
except (ClaveCortaError, ClaveSinMayusculaError,
        ClaveSinMinusculaError, ClaveSinDigitoError) as error:
    print(f"Error: {error}")
```

- **Excepción propia = hereda de `Exception`.** Con
  `class StockInsuficienteError(Exception): pass` alcanza. El
  docstring es opcional pero ayuda a documentar cuándo se lanza.

- **Los métodos que modifican estado deberían pasar por la property.**
  En `vender()`, en lugar de `self._stock -= cantidad`, los enunciados
  hacen `self.stock = nuevo_stock` para que el cambio también pase por
  el setter y su validación. Una sola puerta de entrada al atributo.
