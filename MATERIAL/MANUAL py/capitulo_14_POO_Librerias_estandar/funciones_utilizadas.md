# Funciones Utilizadas en capitulo_14_POO_Librerias_estandar

Documento que agrupa las funciones built-in, los métodos, los módulos,
los tipos de excepción y las construcciones del lenguaje utilizados en
los ejercicios y enunciados, organizados por tipo y en orden
alfabético.

Este capítulo es un recorrido por la **biblioteca estándar**: `math`,
`decimal`, `random`, `secrets`, `string`, `datetime`, `zoneinfo`,
`pathlib`, `csv`, `json`, `re`, `collections`, `enum`, `itertools` y
`functools`. Todos esos módulos, con sus funciones y métodos, están
explicados en la teoría, así que **no** se repiten acá. Este archivo
junta lo de siempre que los ejercicios usan como andamiaje y que la
teoría del capítulo no vuelve a desarrollar: las built-in de propósito
general (`sorted`, `sum`, `enumerate`, `range`, `set`...), los métodos
de string más comunes (`split`, `lower`, `join`, `replace`), las
comprensiones (incluidas las anidadas y las de diccionario), el
desempaquetado de tuplas, y las excepciones `ValueError` y
`AssertionError` que se lanzan o se capturan en las pruebas.

---

## Funciones Generales

### `dict(argumento)`

**¿Qué realiza?**

Construye un diccionario. En el capítulo se usa para **congelar** un
`defaultdict` o un `Counter` en un `dict` común antes de devolverlo o
mostrarlo, así el llamador no arrastra el comportamiento especial (que
`d[clave]` cree entradas nuevas, por ejemplo).

**¿Qué retorna?**

Un diccionario nuevo.

**Ejemplos típicos:**

```python
def contar_extensiones(carpeta):
    contador = Counter(
        item.suffix for item in carpeta.iterdir() if item.is_file()
    )
    return dict(contador)

return dict(por_alumno)          # deja de ser defaultdict
```

### `enumerate(iterable, start=0)`

**¿Qué realiza?**

Recorre un iterable entregando, en cada vuelta, una tupla
`(indice, elemento)`. Sirve para numerar filas de un reporte sin llevar
un contador a mano.

**¿Qué retorna?**

Un iterador de tuplas `(indice, elemento)`.

**Ejemplos típicos:**

```python
for numero, linea in enumerate(lineas, start=1):
    print(f"{numero:>3}: {linea}")
```

### `float(valor)`

**¿Qué realiza?**

Convierte a número de punto flotante. Es imprescindible al leer de un
CSV o un JSON de texto: `csv.DictReader` y `re.findall` devuelven
**strings**, y para operar hay que convertir.

**¿Qué retorna?**

Un `float`.

**Errores posibles:**

Lanza `ValueError` si el texto no representa un número
(`float("abc")`).

**Ejemplos típicos:**

```python
for fila in csv.DictReader(entrada):
    precio = float(fila["precio"])
    fila["precio"] = f"{precio * factor:.2f}"

notas_por_alumno[fila["nombre"]].append(float(fila["nota"]))
```

### `int(valor)`

**¿Qué realiza?**

Convierte a entero. En el capítulo aparece al leer el `stock` de un CSV
y al truncar el resultado de `math.sqrt()` para acotar la búsqueda de
divisores.

**¿Qué retorna?**

Un `int`.

**Ejemplos típicos:**

```python
stock = int(fila["stock"])

for divisor in range(3, int(math.sqrt(n)) + 1, 2):
    ...
```

### `isinstance(objeto, clase)`

**¿Qué realiza?**

Verifica si un objeto es de una clase. En el capítulo se usa para
validar el tipo de un argumento antes de trabajarlo con `re`: si no es
`str`, la función devuelve `False` en vez de reventar.

**¿Qué retorna?**

Un valor de tipo `bool`.

**Ejemplos típicos:**

```python
def validar_dni(dni):
    if not isinstance(dni, str):
        return False
    return PATRON_DNI.fullmatch(dni) is not None
```

### `len(colección)`

**¿Qué realiza?**

Retorna la cantidad de elementos. Se usa para promediar, para validar
una longitud exacta (10 dígitos de un teléfono) y para armar una barra
de asteriscos proporcional a un conteo.

**¿Qué retorna?**

Un valor de tipo `int`.

**Ejemplos típicos:**

```python
if len(solo_digitos) != 10:
    raise ValueError(
        f"Se esperaban 10 dígitos, hay {len(solo_digitos)}"
    )

promedio = sum(notas) / len(notas)
```

### `list(iterable)`

**¿Qué realiza?**

Construye una lista a partir de un iterable. En el capítulo copia la
lista de movimientos que llega por parámetro
(`list(movimientos or [])`) y materializa un iterador cuando hace falta
recorrerlo más de una vez.

**¿Qué retorna?**

Una lista nueva.

**Ejemplos típicos:**

```python
def __init__(self, titular, movimientos=None):
    self._titular = titular
    self._movimientos = list(movimientos or [])
```

### `max(iterable)`

**¿Qué realiza?**

Devuelve el elemento mayor. En el capítulo aparece sin `key`, sobre
números, para encontrar el promedio más alto o la nota máxima.

**¿Qué retorna?**

El elemento mayor.

**Ejemplos típicos:**

```python
mejor = max(promedios.values())
```

### `min(iterable)`

**¿Qué realiza?**

Devuelve el elemento menor, de forma simétrica a `max()`.

**¿Qué retorna?**

El elemento menor.

**Ejemplos típicos:**

```python
peor = min(promedios.values())
```

### `open(ruta, modo, encoding=...)`

**¿Qué realiza?**

Abre un archivo y devuelve un objeto archivo. En este capítulo se usa
para los archivos de `csv` y `json`, siempre con `with` y siempre con
`encoding="utf-8"`; para escribir CSV se agrega `newline=""`. La
alternativa `Path.write_text` / `Path.read_text` la explica la teoría.

**¿Qué retorna?**

Un objeto archivo, que se usa como gestor de contexto.

**Ejemplos típicos:**

```python
with open(ruta, "w", newline="", encoding="utf-8") as salida:
    escritor = csv.DictWriter(salida, fieldnames=CAMPOS)
    escritor.writeheader()
    escritor.writerows(productos)

with open(ruta, encoding="utf-8") as archivo:
    datos = json.load(archivo)
```

### `print(*objetos, sep=' ', end='\n')`

**¿Qué realiza?**

Escribe en la salida estándar. Se usa para mostrar los resultados de
las pruebas y los mensajes de las excepciones capturadas.

**¿Qué retorna?**

`None`.

**Ejemplos típicos:**

```python
for numero in range(2, 20):
    print(f"{numero:>4}: {es_primo(numero)}")
```

### `range(inicio, fin, paso)`

**¿Qué realiza?**

Genera una secuencia de enteros. En el capítulo aparece con **paso**
(`range(3, limite, 2)` para saltear los pares) y como cantidad de
repeticiones de una comprensión (`for _ in range(tiradas)`).

**¿Qué retorna?**

Un objeto `range` (iterable perezoso).

**Ejemplos típicos:**

```python
tiradas = [random.randint(1, 6) for _ in range(cantidad)]

for divisor in range(3, int(math.sqrt(n)) + 1, 2):
    if n % divisor == 0:
        return False
```

### `set(iterable)`

**¿Qué realiza?**

Construye un conjunto (sin repetidos, sin orden). En el capítulo
guarda los feriados y los días no laborables para preguntar con `in`
de forma directa, y para definir el conjunto de "palabras vacías" que
se descartan al contar frecuencias.

**¿Qué retorna?**

Un `set`.

**Ejemplos típicos:**

```python
sin_laborar = set(feriados or [])
if actual.weekday() < 5 and actual not in sin_laborar:
    habiles += 1

VACIAS = {"la", "el", "de", "que", "y", "en", "un", "una"}
```

### `sorted(iterable, key=..., reverse=...)`

**¿Qué realiza?**

Devuelve una **lista nueva** ordenada. En el capítulo se usa de tres
formas: sin argumentos sobre las claves de un diccionario
(`for mes in sorted(resumen)`), sobre `d.items()` para ordenar por
clave, y con `key=lambda par: par[1], reverse=True` para armar un
ranking por el segundo elemento de cada par.

**¿Qué retorna?**

Una lista nueva ordenada.

**Ejemplos típicos:**

```python
ranking = sorted(
    promedios.items(),
    key=lambda par: par[1],
    reverse=True,
)

for extension, cantidad in sorted(resultado.items()):
    print(f"{extension or '(sin extensión)':>18}: {cantidad}")
```

### `sum(iterable)`

**¿Qué realiza?**

Suma los elementos de un iterable numérico, a menudo alimentado por una
expresión generadora: tamaño total de una carpeta, suma de notas,
total de una lista de importes.

**¿Qué retorna?**

La suma total.

**Ejemplos típicos:**

```python
total = sum(
    item.stat().st_size
    for item in carpeta.iterdir()
    if item.is_file()
)

promedio = sum(alumno["notas"]) / len(alumno["notas"])
```

### `type(objeto)`

**¿Qué realiza?**

Retorna la clase de un objeto. En el capítulo se usa para **mostrar**
qué tipo devuelve `re.compile()` (`re.Pattern`), como parte de la
explicación de esa parte del módulo.

**¿Qué retorna?**

La clase del objeto.

**Ejemplos típicos:**

```python
PATRON_EMAIL = re.compile(r"[\w.-]+@[\w.-]+\.\w+")
print(type(PATRON_EMAIL))          # <class 're.Pattern'>
print(PATRON_EMAIL.pattern)
```

---

## Métodos de Strings (Cadenas de Texto)

Los siguientes elementos son métodos de la clase `str`. Se invocan
sobre un objeto de tipo string, por ejemplo, `texto.split()`.

### `string.join(iterable_de_strings)`

**¿Qué realiza?**

Une los elementos de un iterable de strings intercalando el string
sobre el que se invoca. En el capítulo pega una contraseña carácter por
carácter (`""`), arma una cola con `" -> "` en el medio y junta líneas
con `"\n"`.

**¿Qué retorna?**

Un nuevo string.

**Ejemplos típicos:**

```python
alfabeto = string.ascii_letters + string.digits
clave = "".join(secrets.choice(alfabeto) for _ in range(longitud))

def __str__(self):
    return " -> ".join(self._cola)
```

### `string.lower()`

**¿Qué realiza?**

Devuelve una copia del string en minúsculas. En el capítulo normaliza
un texto antes de contar palabras, para que "Casa" y "casa" sumen
juntas.

**¿Qué retorna?**

Un nuevo string.

**Ejemplos típicos:**

```python
limpio = re.sub(r"[^\w\s]", "", texto.lower())
palabras = limpio.split()
```

### `string.replace(viejo, nuevo)`

**¿Qué realiza?**

Devuelve una copia con todas las apariciones de `viejo` cambiadas por
`nuevo`. En el capítulo saca los puntos de miles de un número escrito
como texto antes de convertirlo con `float()`.

**¿Qué retorna?**

Un nuevo string.

**Ejemplos típicos:**

```python
numeros = PATRON_NUMERO.findall(texto)
valores = [float(numero.replace(".", "")) for numero in numeros]
```

### `string.split(separador=None)`

**¿Qué realiza?**

Parte el string en una lista de subcadenas. Sin argumento, corta por
cualquier bloque de espacios y descarta los vacíos, ideal para separar
un texto en palabras.

**¿Qué retorna?**

Una lista de strings.

**Ejemplos típicos:**

```python
limpio = re.sub(r"[^\w\s]", "", texto.lower())
palabras = limpio.split()
frecuentes = Counter(palabras).most_common(cantidad)
```

### `string.strip()`

**¿Qué realiza?**

Devuelve una copia sin los espacios (ni saltos de línea) del principio
y del final. En el capítulo se aplica después de colapsar los espacios
internos con `re.sub`.

**¿Qué retorna?**

Un nuevo string.

**Ejemplos típicos:**

```python
PATRON_BLANCOS = re.compile(r"\s+")
limpio = PATRON_BLANCOS.sub(" ", texto).strip()
```

### `string.title()`

**¿Qué realiza?**

Devuelve una copia con la primera letra de cada palabra en mayúscula y
el resto en minúscula. Se usa para presentar nombres.

**¿Qué retorna?**

Un nuevo string.

**Ejemplos típicos:**

```python
print(nombre.title())
```

---

## Métodos de Listas

### `list.append(elemento)`

**¿Qué realiza?**

Agrega `elemento` al final de la lista, en el lugar. En el capítulo
aparece sobre todo con el `defaultdict(list)`: `d[clave].append(...)`
donde `d[clave]` es la lista vacía que el `defaultdict` acaba de crear.

**¿Qué retorna?**

`None`.

**Ejemplos típicos:**

```python
por_alumno = defaultdict(list)
for alumno, _materia, nota in registros:
    por_alumno[alumno].append(nota)
```

---

## Tipos de Excepción

### `AssertionError`

**¿Cuándo se produce?**

Cuando falla un `assert`. En este capítulo los ejercicios de
persistencia lo usan para verificar que los datos sobreviven la ida y
vuelta a JSON o CSV, y a veces lo **capturan** para imprimir un
mensaje prolijo en lugar del traceback.

**Ejemplos típicos:**

```python
try:
    assert recuperado == objeto, (
        "El objeto no sobrevivió la ida y vuelta a JSON"
    )
    print("OK: los datos coinciden")
except AssertionError as error:
    print(f"FALLÓ: {error}")
```

### `ValueError`

**¿Cuándo se produce?**

Cuando un valor es del tipo correcto pero no sirve. En el capítulo lo
lanzan a mano varias funciones al validar sus argumentos: una
contraseña de menos de 8 caracteres, un ángulo fuera de `(0, 90)`, un
teléfono que no tiene 10 dígitos, una fecha mal escrita. También lo
puede lanzar `float()` / `int()` sobre un texto inválido.

**Ejemplos típicos:**

```python
if longitud < 8:
    raise ValueError("La contraseña debe tener 8 o más caracteres")

if len(solo_digitos) != 10:
    raise ValueError(
        f"Se esperaban 10 dígitos, hay {len(solo_digitos)}"
    )

try:
    generar_clave(4)
except ValueError as error:
    print(f"Rechazada: {error}")
```

---

## Construcciones del Lenguaje

### Comprensión de listas

**¿Qué realiza?**

Arma una lista recorriendo un iterable en una sola expresión, con un
`if` opcional para filtrar. En el capítulo genera tiradas de dados,
junta todas las notas de todos los alumnos y filtra palabras vacías.

**Ejemplos típicos:**

```python
tiradas = [random.randint(1, 6) for _ in range(cantidad)]

valores = [float(numero.replace(".", "")) for numero in numeros]

utiles = [palabra for palabra in palabras if palabra not in vacias]
```

### Comprensión de listas anidada

**¿Qué realiza?**

Dos `for` en la misma comprensión, para aplanar una estructura de dos
niveles. Se lee en el mismo orden que si fueran dos `for` anidados:
primero el de afuera, después el de adentro.

**Ejemplos típicos:**

```python
todas_las_notas = [
    nota
    for alumno in datos["alumnos"]
    for nota in alumno["notas"]
]
```

### Comprensión de diccionario

**¿Qué realiza?**

Como la de listas pero produce pares `clave: valor`. En el capítulo
construye un diccionario "nombre → promedio" a partir de una lista de
alumnos.

**Ejemplos típicos:**

```python
promedios = {
    alumno["nombre"]: sum(alumno["notas"]) / len(alumno["notas"])
    for alumno in datos["alumnos"]
}
```

### Expresión generadora en `sum()`, `Counter()`, `"".join()`

**¿Qué realiza?**

Igual que una comprensión pero sin los corchetes: produce los valores
de a uno, sin lista intermedia. Se pasa directo como único argumento de
una función.

**Ejemplos típicos:**

```python
total = sum(item.stat().st_size for item in carpeta.iterdir()
            if item.is_file())

contador = Counter(item.suffix for item in carpeta.iterdir()
                   if item.is_file())

clave = "".join(secrets.choice(alfabeto) for _ in range(longitud))
```

### Desempaquetado de tuplas

**¿Qué realiza?**

Asignar varias variables de una vez a partir de una tupla. En el
capítulo aparece al recorrer una lista de tuplas
(`for alumno, _materia, nota in registros`), al tomar el primer par de
`most_common` (`mas_frecuente, veces = conteo.most_common(1)[0]`) y al
pasar de una `namedtuple` a coordenadas sueltas (`x, y = tupla`).

**Ejemplos típicos:**

```python
for alumno, _materia, nota in registros:
    por_alumno[alumno].append(nota)

mas_frecuente, veces = conteo.most_common(1)[0]

x, y = punto
```

### `_` (y `_materia`) como variable de descarte

**¿Qué realiza?**

Un nombre que empieza con guion bajo avisa "este valor no se usa".
`for _ in range(n)` repite `n` veces sin necesitar el índice;
`_materia` en un desempaquetado marca el campo que se ignora.

**Ejemplos típicos:**

```python
tiradas = [random.randint(1, 6) for _ in range(cantidad)]

for alumno, _materia, nota in registros:
    ...
```

### `lambda` como `key=` de `sorted()`

**¿Qué realiza?**

Una función anónima de una línea que le dice a `sorted()` (o a
`max`/`min`) por qué valor comparar. `key=lambda par: par[1]` ordena
una lista de pares por el segundo elemento.

**Ejemplos típicos:**

```python
ranking = sorted(
    promedios.items(),
    key=lambda par: par[1],
    reverse=True,
)
```

### `defaultdict(lambda: {...})`

**¿Qué realiza?**

Al `defaultdict` se le puede pasar cualquier función sin argumentos
como fábrica del valor por defecto. Con un `lambda` que devuelve un
diccionario, cada clave nueva arranca con un acumulador
`{"cantidad": 0, "total": 0.0}` listo para sumar.

**Ejemplos típicos:**

```python
resumen = defaultdict(lambda: {"cantidad": 0, "total": 0.0})
for fila in csv.DictReader(entrada):
    mes = f"{fecha:%Y-%m}"
    resumen[mes]["cantidad"] += 1
    resumen[mes]["total"] += float(fila["importe"])
```

### `x or valor_por_defecto` y `set(x or [])`

**¿Qué realiza?**

`or` devuelve el primer operando "verdadero". `feriados or []`
reemplaza `None` (o una lista vacía) por `[]`; `extension or "(sin
extensión)"` muestra un texto cuando el string está vacío.

**Ejemplos típicos:**

```python
def dias_habiles(desde, hasta, feriados=None):
    sin_laborar = set(feriados or [])
    ...

etiqueta = extension or "(sin extensión)"
```

### Parámetros con valor por defecto `None`

**¿Qué realiza?**

Patrón para dar un valor por defecto que se calcula recién adentro de
la función (no se puede poner `hoy=date.today()` en la firma porque se
evaluaría una sola vez). Se pone `hoy=None` y en el cuerpo
`if hoy is None: hoy = date.today()`.

**Ejemplos típicos:**

```python
def edad(nacimiento, hoy=None):
    if hoy is None:
        hoy = date.today()
    ...
```

### `is None` / `is not None`

**¿Qué realiza?**

Compara identidad contra el objeto `None`. Se usa para el patrón del
parámetro por defecto y para convertir el resultado de
`fullmatch()` (que es un objeto `Match` o `None`) en un `bool` limpio.

**Ejemplos típicos:**

```python
return PATRON_DNI.fullmatch(dni) is not None

if hoy is None:
    hoy = date.today()
```

### Comparación de tuplas

**¿Qué realiza?**

Python compara tuplas elemento por elemento, de izquierda a derecha.
`(hoy.month, hoy.day) < (nacimiento.month, nacimiento.day)` responde
"¿todavía no llegó el cumpleaños este año?" sin encadenar `and`.

**Ejemplos típicos:**

```python
anios = hoy.year - nacimiento.year
if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
    anios -= 1
```

### Rebanado (slicing) de strings

**¿Qué realiza?**

`texto[inicio:fin]` devuelve un tramo. En el capítulo parte un teléfono
ya normalizado en área, prefijo y número.

**Ejemplos típicos:**

```python
area = solo_digitos[:3]
prefijo = solo_digitos[3:6]
resto = solo_digitos[6:]
return f"({area}) {prefijo}-{resto}"
```

### `"texto" * n` (repetición de string)

**¿Qué realiza?**

Multiplicar un string por un entero lo repite. Se usa para dibujar una
barra de frecuencias con `#` y para generar un archivo de prueba con
contenido de relleno.

**Ejemplos típicos:**

```python
for nota in sorted(conteo):
    print(f"{nota}: {'#' * conteo[nota]}")

(carpeta / "grande.txt").write_text("hola " * 100, encoding="utf-8")
```

### `cls(**datos)` — desempaquetar un diccionario en argumentos

**¿Qué realiza?**

`**diccionario` en una llamada convierte cada par `clave: valor` en un
argumento con nombre. Es la contracara de `asdict()`: permite
reconstruir una dataclass desde el diccionario que salió del JSON.

**Ejemplos típicos:**

```python
@classmethod
def from_dict(cls, datos):
    return cls(**datos)
```

### `if __name__ == "__main__":`

**¿Qué realiza?**

`__name__` vale `"__main__"` cuando el archivo se ejecuta directo. La
prueba va adentro de este `if` para que corra al ejecutar el archivo
pero no al importarlo. Todos los archivos del capítulo lo usan.

**Ejemplos típicos:**

```python
if __name__ == "__main__":
    print(generar_clave(12))
```

### Constantes en MAYÚSCULAS a nivel de módulo

**¿Qué realiza?**

Convención de PEP 8: los valores fijos van en MAYÚSCULAS, arriba del
todo. En el capítulo son patrones `re` ya compilados, formatos de
fecha, listas de datos de ejemplo y cantidades de iteraciones.

**Ejemplos típicos:**

```python
PATRON_EMAIL = re.compile(r"[\w.-]+@[\w.-]+\.\w+")
FORMATO_FECHA = "%d/%m/%Y"
TIRADAS = 10_000
VACIAS = {"la", "el", "de", "que", "y", "en"}
```

### Separador de miles en literales numéricos

**¿Qué realiza?**

Python ignora los guiones bajos dentro de un número: `10_000` es
`10000`, solo que se lee mejor.

**Ejemplos típicos:**

```python
TIRADAS = 10_000
```

### f-strings: alineación, separador de miles y `!r`

**¿Qué realiza?**

Además de `{x:.2f}`, el capítulo usa la **alineación** en ancho fijo
(`{x:>4}`, `{x:>28}`) para armar columnas, el **separador de miles**
(`{total:,.2f}`), el formato `{x:.0f}` (sin decimales) y `{x!r}` para
mostrar el `repr()` de un valor (útil para ver espacios y comillas).
Los códigos de fecha (`{fecha:%Y-%m}`, `{momento:%Y%m%d}`) también van
directo dentro de la f-string.

**Ejemplos típicos:**

```python
print(f"{caso!r:>14}: {validar_dni(caso)}")

print(f"{cara}: {conteo[cara]:>5}  ({porcentaje:.2f}%)")

print(f"${datos['total']:,.2f}")

ruta = carpeta / f"reporte_{momento:%Y%m%d}.json"
```

---

## Resumen por Categoría

| Categoría | Elementos |
| --------- | --------- |
| **Funciones built-in** | `dict`, `enumerate`, `float`, `int`, `isinstance`, `len`, `list`, `max`, `min`, `open`, `print`, `range`, `set`, `sorted`, `sum`, `type` |
| **Métodos de `str`** | `join`, `lower`, `replace`, `split`, `strip`, `title` |
| **Métodos de `list`** | `append` |
| **Tipos de excepción** | `AssertionError` (falla un `assert`), `ValueError` (validación de argumentos, `float`/`int`) |
| **Construcciones del lenguaje** | comprensiones de lista / anidadas / de diccionario, expresión generadora como argumento, desempaquetado de tuplas, `_` de descarte, `lambda` en `key=`, `defaultdict(lambda: {...})`, `x or defecto`, parámetro `None` + `is None`, comparación de tuplas, slicing de strings, `"txt" * n`, `cls(**datos)`, `if __name__ == "__main__":`, constantes en MAYÚSCULAS, `10_000`, f-strings (`:>4`, `:,.2f`, `:.0f`, `!r`, `%Y-%m`) |

---

## Notas Importantes

- **La teoría cubre los módulos; este archivo cubre el andamiaje.**
  Todo lo de `math`, `random`, `datetime`, `pathlib`, `csv`, `json`,
  `re`, `collections`, etc. está explicado capítulo adentro. Acá está
  lo que se usa "de paso": built-in de siempre, métodos de string,
  comprensiones y desempaquetados.

- **Leer de un archivo devuelve texto.** `csv.DictReader`,
  `re.findall` y `json` sobre strings entregan `str`. Antes de sumar,
  comparar o promediar hay que convertir con `float()` o `int()`, y eso
  puede lanzar `ValueError`.

- **`dict(...)` "congela" un `defaultdict` o un `Counter`.** Conviene
  devolver un `dict` común para que quien recibe el resultado no
  arrastre el comportamiento mágico (que consultar una clave nueva la
  cree, en el caso del `defaultdict`).

- **El parámetro por defecto se evalúa una sola vez.** Por eso nunca
  se pone `hoy=date.today()` ni `feriados=[]` en la firma: se pone
  `None` y se resuelve adentro. Una lista por defecto compartida entre
  llamadas es un error clásico.

- **`fullmatch(...) is not None` convierte un `Match` en un `bool`.**
  Los métodos de `re` devuelven un objeto `Match` (verdadero) o `None`.
  Comparar contra `None` deja la función devolviendo un `bool` limpio.

- **Comparar tuplas evita encadenar `and`.**
  `(hoy.month, hoy.day) < (nac.month, nac.day)` es más corto y más
  claro que `hoy.month < nac.month or (hoy.month == nac.month and ...)`.

- **`x or valor` sirve para el caso vacío**, no solo para `None`: una
  lista vacía, un string vacío o un `0` también disparan el
  reemplazo. Tenelo presente si el valor legítimo puede ser "falsy".

- **`asdict()` y `cls(**datos)` son las dos mitades de la
  persistencia.** `asdict(objeto)` baja la dataclass a un diccionario
  para el JSON; `cls(**datos)` la reconstruye al leer. Ver la teoría
  para `to_dict` / `from_dict` y `@classmethod`.
