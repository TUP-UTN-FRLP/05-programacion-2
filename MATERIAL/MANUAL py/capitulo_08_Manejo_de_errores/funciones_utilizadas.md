# Funciones Utilizadas en capitulo_08_Manejo_de_errores

Documento que agrupa las funciones built-in, los métodos, los módulos,
los tipos de excepción y las construcciones del lenguaje utilizados en
los ejercicios y enunciados, organizados por tipo y en orden
alfabético.

---

## Funciones Generales

### `float(valor)`

**¿Qué realiza?**

Convierte un valor compatible en un número de punto flotante (`float`).
Acepta strings que representen números enteros o decimales. No acepta
texto arbitrario ni strings vacíos.

**¿Qué retorna?**

Un valor de tipo `float`.

**Errores posibles:**

Lanza `ValueError` si el string no representa un número válido.

**Ejemplos típicos:**

```python
float("3.14")                  # Retorna 3.14
float("42")                    # Retorna 42.0
float("-1.5")                  # Retorna -1.5
a = float(input("Número: "))   # Convierte la entrada a float
```

### `input(mensaje)`

**¿Qué realiza?**

Solicita una entrada al usuario desde la entrada estándar. Muestra un
mensaje y espera que el usuario escriba un valor.

**¿Qué retorna?**

Un valor de tipo `str` con los caracteres ingresados por el usuario.

`input()` siempre retorna un string, aunque el usuario ingrese un
número.

**Ejemplos típicos:**

```python
texto = input("Texto: ")           # Retorna un str
numero = float(input("Número: "))  # Convierte al tipo deseado
```

### `int(valor)`

**¿Qué realiza?**

Convierte un valor compatible en un número entero (`int`). Acepta
strings que representen números enteros, incluyendo negativos. No
acepta decimales en formato string.

**¿Qué retorna?**

Un valor de tipo `int`.

**Errores posibles:**

Lanza `ValueError` si el string contiene texto, decimales o está
vacío. Por ejemplo, `int("3.14")` falla aunque `"3.14"` parezca un
número.

**Ejemplos típicos:**

```python
int("42")                       # Retorna 42
int("-5")                       # Retorna -5
int("3.14")                     # Lanza ValueError
numero = int(input("Edad: "))   # Convierte la entrada a int
```

### `len(colección)`

**¿Qué realiza?**

Retorna la cantidad de elementos de una colección o la longitud de
un string. Funciona con listas, tuplas, sets, diccionarios y strings.

**¿Qué retorna?**

Un valor de tipo `int`.

**Errores posibles:**

Cuando se usa como divisor (`sum(lista) / len(lista)`), si la
colección está vacía `len()` retorna `0` y la división lanza
`ZeroDivisionError`.

**Ejemplos típicos:**

```python
len([7, 8, 9])       # Retorna 3
len([])              # Retorna 0

promedio = sum(lista) / len(lista)
# len([]) == 0 causaría ZeroDivisionError
```

### `open(nombre_archivo, modo='r')`

**¿Qué realiza?**

Abre un archivo del sistema de archivos. Por defecto lo abre en modo
lectura (`'r'`). Se utiliza con la sentencia `with` para garantizar
que el archivo se cierre automáticamente al salir del bloque.

**¿Qué retorna?**

Un objeto de tipo archivo (`file object`) con métodos como `read()`.

**Errores posibles:**

Lanza `FileNotFoundError` si el archivo no existe en la ruta indicada.

**Ejemplos típicos:**

```python
with open("config.txt") as f:
    contenido = f.read()

try:
    with open(nombre_archivo) as f:
        return f.read()
except FileNotFoundError:
    return {}
```

### `print(*objetos, sep=' ', end='\n')`

**¿Qué realiza?**

Escribe uno o varios valores en la salida estándar. Por defecto, la
salida se dirige a la consola.

**¿Qué retorna?**

`None`.

**Ejemplos típicos:**

```python
print("Entrada inválida")
print(f"Ingresaste {numero}")
print(f"Error: {e}")
print(f"Extracción exitosa. Nuevo saldo: ${saldo:.2f}")
```

### `range(inicio, fin, paso)`

**¿Qué realiza?**

Genera una secuencia de enteros. Con un solo argumento genera desde
`0` hasta `fin - 1`.

**¿Qué retorna?**

Un objeto `range`, iterable pero no una lista.

**Ejemplos típicos:**

```python
range(5)    # 0, 1, 2, 3, 4

for i in range(5):
    entrada = input(f"Número {i + 1}: ")
```

### `sum(iterable)`

**¿Qué realiza?**

Retorna la suma de los elementos de un iterable numérico.

**¿Qué retorna?**

La suma total. El tipo del resultado depende de los elementos.

**Ejemplos típicos:**

```python
sum([7, 8, 9])                    # Retorna 24
promedio = sum(edades) / len(edades)
```

---

## Métodos de Strings (Cadenas de Texto)

Los siguientes elementos son métodos de la clase `str`. Se invocan
sobre un objeto de tipo string, por ejemplo, `texto.split("/")`.

### `string.split(sep=None)`

**¿Qué realiza?**

Divide el string en una lista de subcadenas utilizando `sep` como
separador. Si `sep` es `None` (o se omite), divide por espacios en
blanco.

**¿Qué retorna?**

Una lista de strings.

**Ejemplos típicos:**

```python
"25/07/2026".split("/")    # Retorna ["25", "07", "2026"]
"hola mundo".split()       # Retorna ["hola", "mundo"]
```

---

## Métodos de Listas

Los siguientes elementos son métodos de la clase `list`. Se invocan
sobre un objeto de tipo lista, por ejemplo, `mi_lista.append(x)`.

### `list.append(elemento)`

**¿Qué realiza?**

Agrega `elemento` al final de la lista, modificándola en el lugar.

**¿Qué retorna?**

`None`. La lista se modifica directamente.

**Ejemplos típicos:**

```python
numeros = []
numeros.append(int(s))          # Agrega el entero convertido

validos = []
validos.append(float(entrada))

edades = []
edades.append(persona["edad"])
```

---

## Métodos de Diccionarios

Los siguientes elementos son métodos de la clase `dict`. Se invocan
sobre un objeto de tipo diccionario.

### `dict.get(clave, default=None)`

**¿Qué realiza?**

Retorna el valor asociado a `clave` si esta existe en el diccionario.
Si `clave` no existe, retorna `default` en lugar de lanzar `KeyError`.

**¿Qué retorna?**

El valor asociado a `clave`, o `default` si la clave no existe.
Por defecto, `default` es `None`.

**Ejemplos típicos:**

```python
usuario = {"nombre": "Ana", "edad": 25}

usuario.get("nombre", "[dato faltante]")   # Retorna "Ana"
usuario.get("email", "[dato faltante]")    # Retorna "[dato faltante]"
```

Este método es la alternativa idiomática a `try/except KeyError`.
Evita definir un bloque `try` cuando el único propósito es proveer
un valor por defecto.

---

## Métodos de Archivos

Los siguientes métodos pertenecen al objeto archivo (`file object`)
que retorna `open()`. Se invocan sobre ese objeto dentro del bloque
`with`.

### `file.read()`

**¿Qué realiza?**

Lee el contenido completo del archivo abierto como un único string.

**¿Qué retorna?**

Un `str` con el contenido del archivo.

**Ejemplos típicos:**

```python
with open("config.txt") as f:
    contenido = f.read()

def abrir_configuracion(nombre_archivo):
    try:
        with open(nombre_archivo) as f:
            return f.read()
    except FileNotFoundError:
        return {}
```

---

## Módulo `datetime`

### `datetime.now()`

**¿Qué realiza?**

Retorna un objeto `datetime` que representa la fecha y hora actuales
del sistema.

Requiere `from datetime import datetime`.

**¿Qué retorna?**

Un objeto de tipo `datetime`. El atributo `.year` extrae el año como
un entero.

**Ejemplos típicos:**

```python
from datetime import datetime

año_actual = datetime.now().year   # Por ejemplo, 2026

if año > datetime.now().year:
    raise ValueError("No podés haber nacido en el futuro")
```

---

## Módulo `math`

### `sqrt(x)` (importado como `from math import sqrt`)

**¿Qué realiza?**

Retorna la raíz cuadrada de `x` como número de punto flotante.

No acepta números negativos; lanza `ValueError` si `x < 0`.

Requiere `from math import sqrt`.

**¿Qué retorna?**

Un valor de tipo `float`.

**Ejemplos típicos:**

```python
from math import sqrt

sqrt(9)     # Retorna 3.0
sqrt(2)     # Retorna 1.4142135623730951

print(f"√{numero} = {sqrt(numero):.4f}")
```

---

## Módulo `random`

### `random.randint(a, b)`

**¿Qué realiza?**

Retorna un número entero aleatorio `n` tal que `a <= n <= b`.
A diferencia de `range()`, el extremo superior `b` es inclusivo.

Requiere `import random`.

**¿Qué retorna?**

Un valor de tipo `int`.

**Ejemplos típicos:**

```python
import random

random.randint(1, 100)   # Entero aleatorio entre 1 y 100 inclusive
random.randint(1, 6)     # Simula un dado de 6 caras

secreto = random.randint(1, 100)
```

---

## Tipos de Excepción

Los siguientes son los tipos de excepción (clases de error) que
aparecen en los ejercicios y enunciados del capítulo. Cada uno
representa una categoría específica de error de Python.

### `FileNotFoundError`

**¿Cuándo se produce?**

Cuando se intenta abrir un archivo que no existe en la ruta indicada.
Es una subclase de `OSError`.

**Ejemplos típicos:**

```python
open("no_existe.txt")    # Lanza FileNotFoundError

try:
    with open(nombre_archivo) as f:
        return f.read()
except FileNotFoundError:
    return {}
```

### `IndexError`

**¿Cuándo se produce?**

Cuando se accede a una posición de una lista, tupla o string que está
fuera del rango válido de índices.

**Ejemplos típicos:**

```python
lista = [10, 20, 30]
lista[100]     # Lanza IndexError (el índice no existe)
lista[-10]     # Lanza IndexError (negativo fuera de rango)

try:
    return lista[indice]
except IndexError:
    return None
```

### `KeyError`

**¿Cuándo se produce?**

Cuando se accede a una clave de un diccionario que no existe, usando
la sintaxis `diccionario[clave]`.

No se produce cuando se usa `dict.get(clave, default)`.

**Ejemplos típicos:**

```python
usuario = {"nombre": "Ana"}
usuario["email"]    # Lanza KeyError: 'email'

try:
    return diccionario[clave]
except KeyError:
    return "[dato faltante]"
```

### `TypeError`

**¿Cuándo se produce?**

Cuando una operación se aplica a un objeto de tipo incompatible. Por
ejemplo, sumar un entero y un string, o usar un string como índice.

**Ejemplos típicos:**

```python
10 + "cinco"             # Lanza TypeError
[1, 2, 3]["abc"]         # Lanza TypeError

try:
    return lista[:indice], lista[indice:]
except TypeError:
    return lista, []
```

### `ValueError`

**¿Cuándo se produce?**

Cuando una función recibe un argumento del tipo correcto pero con un
valor inapropiado. Es el tipo de excepción más frecuente en este
capítulo.

Casos típicos:

- `int()` o `float()` con un string que no representa un número.
- `raise ValueError(...)` lanzado manualmente para señalar que un
  valor está fuera del rango esperado.

**Ejemplos típicos:**

```python
int("hola")      # Lanza ValueError
float("abc")     # Lanza ValueError
int("3.14")      # Lanza ValueError (no es entero)

# Lanzado manualmente:
raise ValueError("Edad fuera de rango")
raise ValueError("Saldo insuficiente")

try:
    numero = int(input("Número: "))
except ValueError:
    print("Entrada inválida")
```

### `ZeroDivisionError`

**¿Cuándo se produce?**

Cuando se intenta dividir un número por cero, usando `/`, `//` o `%`.

**Ejemplos típicos:**

```python
10 / 0     # Lanza ZeroDivisionError

# También ocurre cuando la lista está vacía:
sum(lista) / len(lista)   # len([]) == 0 causa ZeroDivisionError

try:
    return a / b
except ZeroDivisionError:
    return None
```

---

## Construcciones del Lenguaje

Las siguientes construcciones son características propias de la
sintaxis de Python para el manejo de errores, que son el tema central
de este capítulo.

### Bloque `try/except`

**¿Qué realiza?**

Intenta ejecutar el código dentro de `try`. Si ocurre un error del
tipo indicado en `except`, se ejecuta el bloque `except` en lugar
de cortar el programa con un traceback.

**Sintaxis:**

```python
try:
    # código que puede fallar
except TipoDeError:
    # qué hacer si ocurre ese error
```

**Ejemplos típicos:**

```python
try:
    numero = int(input("Número entero: "))
    print(f"Ingresaste {numero}")
except ValueError:
    print("Entrada inválida")
```

### Bloque `try/except` con múltiples cláusulas `except`

**¿Qué realiza?**

Permite manejar distintos tipos de error con mensajes o acciones
diferentes. Python ejecuta la primera cláusula `except` cuyo tipo
coincida con el error ocurrido.

**Sintaxis:**

```python
try:
    # código que puede fallar de más de una forma
except TipoDeErrorA:
    # qué hacer si ocurre el error A
except TipoDeErrorB:
    # qué hacer si ocurre el error B
```

**Ejemplos típicos:**

```python
try:
    a = float(input("Numerador: "))
    b = float(input("Denominador: "))
    print(f"Resultado: {a / b}")
except ValueError:
    print("Los números deben ser válidos")
except ZeroDivisionError:
    print("No se puede dividir por cero")
```

### Bloque `try/except/else`

**¿Qué realiza?**

El bloque `else` se ejecuta solo si el bloque `try` completó sin
ningún error. Es útil para separar el código del "camino exitoso" del
código de manejo de errores.

**Sintaxis:**

```python
try:
    # código que puede fallar
except TipoDeError:
    # qué hacer si ocurre el error
else:
    # qué hacer si NO ocurrió ningún error
```

**Ejemplos típicos:**

```python
while True:
    try:
        numero = int(input("Número: "))
    except ValueError:
        print("Eso no es un número, probá de nuevo")
    else:
        break   # Solo se ejecuta si int() tuvo éxito
```

### Bloque `try/except/finally`

**¿Qué realiza?**

El bloque `finally` se ejecuta siempre, haya ocurrido un error o no.
Se usa para garantizar que ciertas acciones se realicen sin importar
el resultado (mostrar mensajes de cierre, liberar recursos).

**Sintaxis:**

```python
try:
    # código que puede fallar
except TipoDeError:
    # qué hacer si ocurre el error
finally:
    # esto se ejecuta siempre, con o sin error
```

**Ejemplos típicos:**

```python
try:
    edad = int(input("Edad: "))
except ValueError:
    print("No ingresaste un número válido")
else:
    print(f"Perfecto, tenés {edad} años")
finally:
    print("Gracias por participar")   # Siempre se imprime
```

### `except TipoDeError as e`

**¿Qué realiza?**

Captura la excepción en una variable para acceder a su mensaje
descriptivo. La variable `e` contiene el objeto excepción, y al
convertirlo a string con `f"{e}"` muestra el texto del error.

**Sintaxis:**

```python
except TipoDeError as e:
    print(f"Error: {e}")
```

**Ejemplos típicos:**

```python
try:
    imc = calcular_imc(70, -1.75)
except ValueError as e:
    print(f"Error: {e}")
    # Imprime: Error: Peso y altura deben ser positivos

try:
    if monto > saldo:
        raise ValueError("Saldo insuficiente")
except ValueError as e:
    print(f"Error: {e}")
    # Captura tanto ValueError de int() como el de raise
```

### `raise` — Lanzar excepciones manualmente

**¿Qué realiza?**

Lanza una excepción de forma explícita desde el código. Permite
señalar condiciones de error que Python no detecta automáticamente,
como un valor fuera de un rango de negocio.

Una excepción lanzada con `raise` dentro de un bloque `try` es
capturada por el `except` correspondiente, igual que un error
automático de Python.

**Sintaxis:**

```python
raise TipoDeError("Mensaje descriptivo del error")
```

**Ejemplos típicos:**

```python
def calcular_imc(peso, altura):
    if peso <= 0 or altura <= 0:
        raise ValueError("Peso y altura deben ser positivos")
    return peso / (altura ** 2)

if edad < 0 or edad > 130:
    raise ValueError(f"Edad fuera de rango: {edad}")

if monto > saldo:
    raise ValueError("Saldo insuficiente")

if año > año_actual:
    raise ValueError("No podés haber nacido en el futuro")
```

### f-strings (cadenas formateadas)

**¿Qué realiza?**

Permiten incrustar expresiones de Python directamente dentro de un
string. Se escriben con el prefijo `f` y las expresiones entre `{}`.

**Sintaxis:**

```python
f"texto {expresión} texto"
f"número con decimales {valor:.2f}"
```

**Ejemplos típicos:**

```python
print(f"Ingresaste {numero}")
print(f"Error: {e}")
print(f"Resultado: {a / b}")
print(f"Extracción exitosa. Nuevo saldo: ${saldo:.2f}")
print(f"√{numero} = {sqrt(numero):.4f}")
print(f"Número {i + 1}: ")
```

---

## Resumen por Categoría

| Categoría | Elementos |
| --------- | --------- |
| **Funciones built-in** | `float`, `input`, `int`, `len`, `open`, `print`, `range`, `sum` |
| **Métodos de `str`** | `split` |
| **Métodos de `list`** | `append` |
| **Métodos de `dict`** | `get` |
| **Métodos de archivos** | `read` |
| **Módulo `datetime`** | `datetime.now` |
| **Módulo `math`** | `sqrt` |
| **Módulo `random`** | `randint` |
| **Tipos de excepción** | `FileNotFoundError`, `IndexError`, `KeyError`, `TypeError`, `ValueError`, `ZeroDivisionError` |
| **Construcciones del lenguaje** | `try/except`, múltiples `except`, `try/except/else`, `try/except/finally`, `except ... as e`, `raise`, f-strings |

---

## Notas Importantes

- **`try/except` vs. `if`:** Se usa `try/except` cuando el error es
  inesperado o externo (entrada del usuario, archivo que no existe,
  tipo equivocado). Se usa `if` cuando la condición es conocida y
  controlable (verificar si un número es negativo antes de operar).

```python
# Con if (condición predecible):
if b == 0:
    print("No se puede dividir por cero")
else:
    print(a / b)

# Con try/except (error externo):
try:
    print(a / b)
except ZeroDivisionError:
    print("No se puede dividir por cero")
```

- **El orden de los `except` importa:** Python evalúa las cláusulas
  `except` de arriba hacia abajo y ejecuta la primera que coincida.
  Si se pone `except Exception` primero, captura todo y los `except`
  siguientes nunca se ejecutan.

```python
# Orden correcto: de más específico a más general
except ValueError:
    ...
except ZeroDivisionError:
    ...
```

- **`raise` dentro de `try` es capturado por `except`:** Una
  excepción lanzada manualmente con `raise` dentro del mismo bloque
  `try` es capturada por su `except`, igual que una excepción
  automática.

```python
try:
    if edad < 0:
        raise ValueError("Edad negativa")   # Capturado por except
    edad = int(input("Edad: "))             # También capturado
except ValueError as e:
    print(f"Error: {e}")
```

- **`else` vs. código dentro del `try`:** Poner código en `else` en
  lugar de al final del `try` deja claro qué parte puede fallar y qué
  parte se ejecuta solo cuando todo salió bien.

```python
# Menos claro:
try:
    numero = int(input("Número: "))
    print(f"Ingresaste {numero}")   # ¿Puede esto fallar?

# Más claro:
try:
    numero = int(input("Número: "))
except ValueError:
    print("No es un número")
else:
    print(f"Ingresaste {numero}")   # Solo si int() tuvo éxito
```

- **`finally` siempre se ejecuta:** Incluso si hay un `return`
  dentro del `try` o del `except`, el bloque `finally` se ejecuta
  antes de salir de la función.

- **`dict.get()` como alternativa a `try/except KeyError`:** Cuando
  el único propósito del `try` es devolver un valor por defecto si la
  clave no existe, `dict.get()` es más conciso.

```python
# Con try/except:
try:
    return diccionario[clave]
except KeyError:
    return "[dato faltante]"

# Equivalente con .get():
return diccionario.get(clave, "[dato faltante]")
```

- **`int()` no acepta decimales en string:** `int("3.14")` lanza
  `ValueError`. Si el usuario puede ingresar decimales, hay que usar
  `float()` primero y luego convertir si es necesario.

```python
int("3.14")       # ValueError
int(float("3.14"))  # Retorna 3 (trunca)
```

- **`ValueError` tiene dos orígenes posibles:** En un mismo bloque
  `try` puede provenir de `int()` o `float()` (entrada inválida)
  o de un `raise ValueError(...)` manual (valor fuera de rango).
  El `except ValueError as e` captura ambos casos; el mensaje `{e}`
  permite distinguirlos al mostrarlo.
