# Funciones Utilizadas en capitulo_09_POO_Objetos_y_clases

Documento que agrupa las funciones built-in, los métodos, los módulos
y las construcciones del lenguaje utilizados en los ejercicios y
enunciados, organizados por tipo y en orden alfabético.

Este capítulo introduce la Programación Orientada a Objetos. El foco
no está en funciones nuevas, sino en las construcciones del lenguaje
que permiten definir clases, crear objetos y darles comportamiento:
`class`, `__init__`, `self`, los atributos de instancia, los métodos
y los métodos especiales como `__str__`.

---

## Funciones Generales

### `isinstance(objeto, clase)`

**¿Qué realiza?**

Verifica si un objeto es una instancia de una clase determinada (o de
una de sus subclases). Es la forma recomendada de comprobar el tipo
de un objeto, en lugar de comparar `type(objeto) == clase`.

**¿Qué retorna?**

Un valor de tipo `bool`: `True` si el objeto pertenece a esa clase,
`False` en caso contrario.

**Ejemplos típicos:**

```python
class Persona:
    pass

persona1 = Persona()

isinstance(persona1, Persona)   # Retorna True
isinstance("hola", Persona)     # Retorna False
```

### `len(colección)`

**¿Qué realiza?**

Retorna la cantidad de elementos de una colección. En este capítulo
se usa sobre la lista interna de un objeto (por ejemplo, la lista de
notas de un `Estudiante`).

**¿Qué retorna?**

Un valor de tipo `int`.

**Errores posibles:**

Cuando se usa como divisor (`sum(notas) / len(notas)`), si la lista
está vacía `len()` retorna `0` y la división lanza
`ZeroDivisionError`. Por eso los métodos que calculan promedios
verifican antes `if len(self.notas) == 0`.

**Ejemplos típicos:**

```python
def promedio(self):
    if len(self.notas) == 0:
        return 0
    return sum(self.notas) / len(self.notas)
```

### `max(iterable)`

**¿Qué realiza?**

Retorna el elemento más grande de un iterable.

**¿Qué retorna?**

El mayor de los elementos. El tipo depende de los elementos del
iterable.

**Errores posibles:**

Lanza `ValueError` si el iterable está vacío. Por eso el método
`mejor_nota()` verifica antes si la lista tiene elementos y devuelve
`None` cuando está vacía.

**Ejemplos típicos:**

```python
def mejor_nota(self):
    if len(self.notas) == 0:
        return None
    return max(self.notas)
```

### `print(*objetos, sep=' ', end='\n')`

**¿Qué realiza?**

Escribe uno o varios valores en la salida estándar.

Cuando se le pasa un objeto de una clase propia, `print()` usa el
método `__str__` de esa clase si está definido. Si no lo está,
imprime la representación por defecto de Python, que incluye el nombre
de la clase y la dirección del objeto en memoria.

**¿Qué retorna?**

`None`.

**Ejemplos típicos:**

```python
# Sin __str__: representación por defecto
print(persona1)   # <__main__.Persona object at 0x000001F2...>

# Con __str__ definido: usa ese texto
print(libro)      # 'El Aleph' de Jorge Luis Borges (224 páginas)

print(f"Soy {self.nombre}, tengo {self.edad} años")
print(f"Área: {c.area():.2f} unidades cuadradas")
```

### `range(inicio, fin, paso)`

**¿Qué realiza?**

Genera una secuencia de enteros. Con un solo argumento genera desde
`0` hasta `fin - 1`.

**¿Qué retorna?**

Un objeto `range`, iterable pero no una lista.

**Ejemplos típicos:**

```python
# Se usa para repetir una acción sobre un objeto muchas veces.
# La variable de control no se utiliza, por eso se llama _.
for _ in range(3700):
    c.avanzar_segundo()
    print(c)
```

### `sum(iterable)`

**¿Qué realiza?**

Retorna la suma de los elementos de un iterable numérico. En este
capítulo se usa sobre la lista interna de notas de un objeto.

**¿Qué retorna?**

La suma total. El tipo del resultado depende de los elementos.

**Ejemplos típicos:**

```python
def promedio(self):
    if len(self.notas) == 0:
        return 0
    return sum(self.notas) / len(self.notas)
```

---

## Métodos de Listas

Los siguientes elementos son métodos de la clase `list`. En este
capítulo se invocan sobre una lista que es atributo de un objeto,
por ejemplo, `self.notas.append(x)`.

### `list.append(elemento)`

**¿Qué realiza?**

Agrega `elemento` al final de la lista, modificándola en el lugar.
Es la operación que usa un método como `agregar_nota()` para
incorporar un dato a la colección interna del objeto.

**¿Qué retorna?**

`None`. La lista se modifica directamente.

**Ejemplos típicos:**

```python
class Estudiante:

    def __init__(self, nombre):
        self.nombre = nombre
        self.notas = []

    def agregar_nota(self, nota):
        self.notas.append(nota)
```

---

## Módulo `math`

### `math.pi`

**¿Qué realiza?**

Es una constante (no una función) con el valor de π
(`3.141592653589793`). Requiere `import math`.

**Ejemplos típicos:**

```python
import math

class Circulo:

    def __init__(self, radio):
        self.radio = radio

    def area(self):
        return math.pi * self.radio ** 2

    def perimetro(self):
        return 2 * math.pi * self.radio
```

### `math.sqrt(x)`

**¿Qué realiza?**

Retorna la raíz cuadrada de `x` como número de punto flotante.
Requiere `import math`.

**¿Qué retorna?**

Un valor de tipo `float`.

**Errores posibles:**

Lanza `ValueError` si `x` es negativo.

**Ejemplos típicos:**

```python
import math

class Punto:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distancia_al_origen(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
```

---

## Construcciones del Lenguaje

Las siguientes construcciones son el tema central del capítulo: la
sintaxis de Python para definir clases y trabajar con objetos.

### `class` — Definición de una clase

**¿Qué realiza?**

Define un nuevo tipo de dato. Una clase es el molde a partir del cual
se crean objetos (instancias). El nombre de la clase se escribe, por
convención, en `PascalCase` (`Persona`, `ProductoStock`).

**Sintaxis:**

```python
class NombreDeLaClase:
    # atributos y métodos
```

**Ejemplos típicos:**

```python
class Persona:
    pass

class Producto:

    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
```

### `pass` — Cuerpo vacío

**¿Qué realiza?**

Es una instrucción que no hace nada. Se usa como relleno cuando la
sintaxis exige un bloque de código pero todavía no hay nada que
escribir, como en una clase sin atributos ni métodos.

**Ejemplos típicos:**

```python
class Persona:
    pass


persona1 = Persona()
persona2 = Persona()
```

### Instanciación — Crear un objeto

**¿Qué realiza?**

Escribir el nombre de la clase seguido de paréntesis crea un objeto
nuevo de esa clase. Python reserva memoria para el objeto y ejecuta
automáticamente su método `__init__`, pasándole los argumentos que
haya entre los paréntesis.

**Sintaxis:**

```python
objeto = NombreDeLaClase(argumentos)
```

**Ejemplos típicos:**

```python
persona1 = Persona()
pan = Producto("Pan", 500)
ana = Alumno("Ana", 22, 8.5)
```

### `__init__(self, ...)` — El constructor

**¿Qué realiza?**

Es un método especial que Python ejecuta automáticamente cada vez que
se crea un objeto. Su tarea habitual es recibir los datos iniciales y
guardarlos como atributos de la instancia.

El primer parámetro siempre es `self`. Los demás son los valores que
se pasan al crear el objeto.

**Sintaxis:**

```python
def __init__(self, parametro1, parametro2):
    self.atributo1 = parametro1
    self.atributo2 = parametro2
```

**Ejemplos típicos:**

```python
class Alumno:

    def __init__(self, nombre, edad, promedio):
        self.nombre = nombre
        self.edad = edad
        self.promedio = promedio
```

### `self` — La referencia al propio objeto

**¿Qué realiza?**

`self` es el primer parámetro de todos los métodos de instancia y
representa al objeto sobre el que se llamó el método. A través de
`self` se accede a los atributos y a otros métodos del mismo objeto.

No se escribe al llamar al método: Python lo pasa solo.
`ana.presentarse()` ejecuta `presentarse(self=ana)`.

**Ejemplos típicos:**

```python
class Alumno:

    def __init__(self, nombre, edad, promedio):
        self.nombre = nombre          # self.nombre: atributo del objeto
        # nombre (sin self): parámetro local que desaparece

    def presentarse(self):
        print(f"Soy {self.nombre}, tengo {self.edad} años")
```

### Atributos de instancia

**¿Qué realiza?**

Son variables que pertenecen a cada objeto. Se crean asignándoles un
valor con `self.nombre = valor`, normalmente dentro de `__init__`.
Cada objeto tiene su propia copia: cambiar el atributo de un objeto
no afecta a los demás.

Un atributo puede inicializarse desde un parámetro o con un valor
fijo (por ejemplo, un `stock` o un `contador` que siempre arranca
en `0`).

**Ejemplos típicos:**

```python
class Producto:

    def __init__(self, nombre, precio):
        self.nombre = nombre     # desde un parámetro
        self.precio = precio     # desde un parámetro
        self.stock = 0           # valor fijo inicial


class Estudiante:

    def __init__(self, nombre):
        self.nombre = nombre
        self.notas = []          # lista vacía inicial
```

### Métodos de instancia

**¿Qué realiza?**

Son funciones definidas dentro de una clase que operan sobre un
objeto. Su primer parámetro es `self`. Se llaman con la notación de
punto: `objeto.metodo(argumentos)`.

Se distinguen dos usos frecuentes:

- **Métodos que modifican el estado:** cambian el valor de uno o más
  atributos (`reponer`, `acelerar`, `cumplir_años`). Suelen devolver
  `None`.
- **Métodos que consultan:** calculan y devuelven un valor a partir de
  los atributos, sin modificarlos (`valor_stock`, `area`,
  `es_mayor`).

**Ejemplos típicos:**

```python
class Producto:

    def reponer(self, cantidad):     # modifica
        self.stock += cantidad

    def valor_stock(self):           # consulta
        return self.precio * self.stock
```

### Retorno de una expresión booleana

**¿Qué realiza?**

Un método puede devolver directamente el resultado de una comparación.
No hace falta escribir `if ... return True else return False`: la
comparación ya produce un `bool`.

**Ejemplos típicos:**

```python
def es_mayor(self):
    return self.edad >= 18

def es_extenso(self):
    return self.paginas > 300
```

### `__str__(self)` — Representación en texto

**¿Qué realiza?**

Es un método especial que define qué texto se muestra cuando el objeto
se pasa a `print()` o a `str()`. Debe devolver un `str`.

Si una clase no define `__str__`, `print()` muestra la representación
por defecto (`<__main__.Clase object at 0x...>`).

**Sintaxis:**

```python
def __str__(self):
    return f"..."
```

**Ejemplos típicos:**

```python
class Libro:

    def __init__(self, titulo, autor, paginas):
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas

    def __str__(self):
        return f"'{self.titulo}' de {self.autor} ({self.paginas} páginas)"


libro = Libro("El Aleph", "Jorge Luis Borges", 224)
print(libro)   # 'El Aleph' de Jorge Luis Borges (224 páginas)
```

### Asignación aumentada (`+=`, `-=`)

**¿Qué realiza?**

Modifica un atributo a partir de su valor actual. `self.edad += 1`
equivale a `self.edad = self.edad + 1`. Es la operación típica de los
métodos que actualizan un contador o un acumulador.

**Ejemplos típicos:**

```python
def cumplir_años(self):
    self.edad += 1

def acelerar(self):
    self.velocidad_actual += 10

def frenar(self):
    self.velocidad_actual -= 10
    if self.velocidad_actual < 0:
        self.velocidad_actual = 0
```

### Operador de exponente `**`

**¿Qué realiza?**

Eleva un número a una potencia. `x ** 2` es `x` al cuadrado.

**Ejemplos típicos:**

```python
def area(self):
    return math.pi * self.radio ** 2

def distancia_al_origen(self):
    return math.sqrt(self.x ** 2 + self.y ** 2)
```

### Variable descartable `_` en `for`

**¿Qué realiza?**

Cuando se necesita repetir una acción una cantidad de veces pero no
interesa el valor del contador, se usa `_` como nombre de la variable
de control. Es una convención que indica "este valor no se usa".

**Ejemplos típicos:**

```python
for _ in range(3700):
    c.avanzar_segundo()
    print(c)
```

### f-strings y formato de valores

**¿Qué realiza?**

Permiten incrustar expresiones dentro de un string usando el prefijo
`f` y llaves `{}`. Dentro de las llaves se puede indicar un formato
después de dos puntos.

**Formatos usados en el capítulo:**

- `{valor:.2f}` — muestra el número con dos decimales.
- `{valor:02d}` — muestra el entero con al menos dos dígitos,
  rellenando con un cero a la izquierda (`7` → `07`).

**Ejemplos típicos:**

```python
print(f"Área: {c.area():.2f} unidades cuadradas")
print(f"${juan.sueldo_total():.2f}")

def __str__(self):
    return f"{self.dia:02d}/{self.mes:02d}/{self.anio}"

def __str__(self):
    return f"{self.horas}:{self.minutos:02d}:{self.segundos:02d}"
```

---

## Resumen por Categoría

| Categoría | Elementos |
| --------- | --------- |
| **Funciones built-in** | `isinstance`, `len`, `max`, `print`, `range`, `sum` |
| **Métodos de `list`** | `append` |
| **Módulo `math`** | `math.pi`, `math.sqrt` |
| **Construcciones del lenguaje** | `class`, `pass`, instanciación, `__init__`, `self`, atributos de instancia, métodos de instancia, retorno de expresión booleana, `__str__`, asignación aumentada, operador `**`, variable `_` en `for`, f-strings con formato |

---

## Notas Importantes

- **Clase vs. objeto:** La clase es el molde; el objeto (instancia) es
  cada elemento concreto creado a partir de ese molde. `Persona` es la
  clase; `persona1`, `persona2` y `persona3` son tres objetos
  distintos, cada uno con sus propios atributos.

- **`__init__` no se llama a mano:** Python lo ejecuta solo al crear
  el objeto. Se escribe `Producto("Pan", 500)`, no
  `Producto.__init__(...)`.

```python
pan = Producto("Pan", 500)   # Python llama a __init__ con nombre="Pan", precio=500
```

- **`self` se recibe pero no se pasa:** Al definir el método se
  escribe `def presentarse(self)`, pero al llamarlo se escribe
  `ana.presentarse()`. Python completa `self` con el objeto que está
  a la izquierda del punto.

- **Atributo (`self.x`) vs. parámetro (`x`):** Dentro de `__init__`,
  `x` es una variable local que desaparece al terminar el método.
  `self.x` es el atributo que queda guardado en el objeto. Por eso
  se escribe `self.x = x`.

- **Cada objeto tiene sus propios atributos:** Modificar
  `focus.velocidad_actual` no cambia la velocidad de otro `Auto`.
  Las listas y otros objetos mutables como atributos deben crearse
  dentro de `__init__` (`self.notas = []`), no como atributo de
  clase, para que cada instancia tenga la suya.

- **Métodos que modifican vs. métodos que consultan:** `reponer()`
  cambia `self.stock` y no devuelve nada; `valor_stock()` no cambia
  nada y devuelve un número. Conviene que un método haga una cosa o
  la otra, no las dos.

```python
def reponer(self, cantidad):     # comando: modifica, devuelve None
    self.stock += cantidad

def valor_stock(self):           # consulta: no modifica, devuelve un valor
    return self.precio * self.stock
```

- **`__str__` debe devolver, no imprimir:** El método `__str__`
  retorna un string; es `print()` quien lo muestra. Si dentro de
  `__str__` se usara `print()`, el texto se mostraría al construir la
  representación y el método devolvería `None`.

- **Sin `__str__`, `print()` muestra la dirección de memoria:** La
  salida `<__main__.Persona object at 0x...>` no es un error: es la
  representación por defecto de un objeto que no definió `__str__`.

- **Un método puede usar otro método del mismo objeto:** A través de
  `self`, un método puede llamar a otro (`self.sueldo_total()` dentro
  de `__str__`, o `self.promedio()` dentro de `esta_aprobado()`).
  Así se evita repetir lógica.

```python
def esta_aprobado(self):
    return self.promedio() >= 6
```
