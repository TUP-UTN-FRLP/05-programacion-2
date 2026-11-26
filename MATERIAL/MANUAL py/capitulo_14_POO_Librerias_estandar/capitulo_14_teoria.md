# Capítulo 14. Librerías estándar

*Herramientas que ya vienen con Python.*

## ¿Por qué leemos este capítulo?

Todo lo que aprendimos hasta acá (sintaxis, colecciones, funciones, POO,
SOLID) es el lenguaje en sí. Pero Python trae además una enorme cantidad de
herramientas listas para usar: módulos que resuelven tareas comunes sin que
tengas que reinventar la rueda. Se llama la **biblioteca estándar**
(*standard library*) y viene incluida en toda instalación de Python: no hay
que instalar nada extra.

En este capítulo vamos a ver los módulos más importantes para la vida diaria
de un desarrollador Python:

- **math** y **decimal**: matemática más allá de las operaciones básicas.
- **random** y **secrets**: aleatoriedad para simulaciones y para secretos.
- **datetime**: manejo de fechas y horas.
- **pathlib**: rutas de archivos y directorios con sintaxis moderna.
- **csv**: lectura y escritura de archivos separados por comas.
- **json**: serialización de datos estructurados.
- **re**: expresiones regulares.
- **collections**: estructuras de datos especializadas.
- **enum**: conjuntos cerrados de valores con nombre.
- **itertools** y **functools**: iteración y trabajo con funciones.

Es un capítulo largo, pero de referencia: no hace falta memorizarlo todo. La
idea es que sepas qué existe y cuándo usarlo, para poder volver a consultar
cuando lo necesites.

![Mapa de la biblioteca estándar del capítulo agrupada por propósito, en ocho
tarjetas. Cálculo: math y decimal (raíces, logaritmos, trigonometría; y plata
exacta). Azar: random y secrets (simular y muestrear; o generar secretos
seguros). Tiempo: datetime y zoneinfo (fechas, duraciones, formato; zonas
horarias con nombre). Archivos y rutas: pathlib (rutas multiplataforma,
leer/escribir, recorrer carpetas). Formatos de datos: csv y json (tablas para
planillas; intercambio entre sistemas y APIs). Texto: re (expresiones
regulares: validar, extraer, reemplazar). Colecciones y tipos: collections y
enum (Counter, defaultdict, deque; y valores cerrados con nombre). Funciones e
iteración: itertools y functools (iteradores combinables; lru_cache, reduce).
Todo esto ya viene con Python y el año que viene, en Django, cada pieza vuelve
con otro nombre hecha por el framework.](images/mapa-biblioteca-estandar.png)

**Y no es un apéndice suelto.** Estos módulos son la pieza que le faltaba al
proyecto: hasta acá, cada vez que cerrábamos el programa el banco desaparecía
de la memoria. Al final del capítulo le vamos a dar persistencia, guardando
las cuentas en JSON y los movimientos en CSV, con las clases que ya
escribimos en los capítulos 12 y 13.

**Nota sobre POO.** Todos estos módulos exponen su funcionalidad como clases
y métodos, así que ahora que sabés POO la interfaz te va a resultar natural:
un `datetime` con properties, un `Path` que sabe navegar el sistema de
archivos, un `re.Pattern` que sabe hacer *matches*, un `Counter` que hereda de
`dict`. Todo lo que aprendiste en los capítulos anteriores se aplica acá.

## math: matemática más allá de lo básico

Los operadores `+`, `-`, `*`, `/`, `**` y `%` son parte del lenguaje. Para
todo lo demás (raíces, logaritmos, trigonometría, constantes) está el módulo
`math`.

```python
import math

# O importando nombres específicos:
from math import pi, sqrt, log
```

### Constantes

```python
math.pi        # 3.141592653589793
math.e         # 2.718281828459045
math.tau       # 6.283185307179586 (2π)
math.inf       # infinito positivo
math.nan       # "not a number"
```

### Funciones básicas

```python
math.sqrt(16)     # 4.0   raíz cuadrada
math.pow(2, 10)   # 1024.0  potencia
math.floor(4.7)   # 4     piso (redondeo hacia abajo)
math.ceil(4.1)    # 5     techo (redondeo hacia arriba)
math.trunc(4.9)   # 4     trunca la parte decimal

abs(-5)           # 5     valor absoluto (built-in, no math)
round(4.567, 2)   # 4.57  redondeo con decimales (built-in)
```

Ojo con `math.pow`: **no es idéntica a `**`**. `math.pow(2, 10)` devuelve
`1024.0`, un float, mientras que `2 ** 10` devuelve `1024`, un entero. Si
trabajás con enteros grandes, `**` conserva la precisión exacta y `math.pow`
no. Para potencias de enteros, usá `**`.

### Logaritmos y exponenciales

```python
math.log(math.e)     # 1.0   logaritmo natural (base e)
math.log10(1000)     # 3.0   logaritmo base 10
math.log2(8)         # 3.0   logaritmo base 2
math.log(100, 10)    # 2.0   logaritmo con base explícita
math.exp(1)          # 2.718...  e elevado a x
```

### Trigonometría

Todas las funciones trigonométricas trabajan en **radianes**, no en grados.
Para convertir, `math.radians()` y `math.degrees()`:

```python
math.sin(math.pi / 2)        # 1.0
math.cos(0)                  # 1.0
math.tan(math.pi / 4)        # 0.9999999999999999 (≈ 1)

math.radians(180)            # 3.14159... (π)
math.degrees(math.pi)        # 180.0
math.sin(math.radians(30))   # 0.49999999999999994 (≈ 0.5)
```

### Otras útiles

```python
math.gcd(12, 18)            # 6    máximo común divisor
math.lcm(4, 6)              # 12   mínimo común múltiplo (Python 3.9+)
math.factorial(5)           # 120  factorial (5!)
math.hypot(3, 4)            # 5.0  hipotenusa / norma del vector
math.dist([0, 0], [3, 4])   # 5.0  distancia euclidiana (Python 3.8+)
math.isclose(0.1 + 0.2, 0.3)  # True
```

### Por qué `0.1 + 0.2 != 0.3`

Ese último caso merece explicación, porque es la fuente de bugs más común con
números en cualquier lenguaje:

```python
print(0.1 + 0.2)          # 0.30000000000000004
print(0.1 + 0.2 == 0.3)   # False
```

No es un error de Python. Los `float` se guardan en **binario**, y 0.1 en
binario es periódico, igual que 1/3 en decimal es 0.333... infinito. Como la
computadora tiene lugar finito, guarda una aproximación, y las
aproximaciones acumulan error al sumarse.

La consecuencia práctica: **nunca compares floats con `==`**. Usá
`math.isclose`, que compara con una tolerancia razonable:

```python
math.isclose(0.1 + 0.2, 0.3)   # True
```

### `decimal`: cuando la plata tiene que dar exacto

`math.isclose` sirve para comparar, pero no arregla el error: si sumás mil
importes con `float`, el redondeo final puede quedar a un centavo del valor
real. Para plata y contabilidad, Python trae el módulo `decimal`, que
representa los números en base 10 —igual que los escribís— y no arrastra ese
error:

```python
from decimal import Decimal

Decimal("0.1") + Decimal("0.2")        # Decimal('0.3')  exacto
Decimal("0.1") + Decimal("0.2") == Decimal("0.3")   # True

# OJO: se construye desde string, no desde float
Decimal(0.1)      # Decimal('0.1000000000000000055511151231257827...')
Decimal("0.1")    # Decimal('0.1')
```

La regla es construir siempre desde `str` (o desde `int`): si le pasás un
`float`, `Decimal` hereda el error binario que justamente querías evitar. El
banco de este manual usa `float` para no complicar los ejemplos, pero un
sistema real de cuentas usaría `Decimal` o enteros de centavos.

> Los nombres con nota de versión (`math.lcm` en 3.9, `math.dist` en 3.8)
> importan en el aula: si a un compañero no le corre tu código, chequeá la
> versión de Python antes que nada.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 1** — Escribí una función que reciba las coordenadas de dos
> puntos, `(x1, y1)` y `(x2, y2)`, y devuelva la distancia entre ellos usando
> `math.sqrt` primero y `math.dist` después. Verificá con `math.isclose` que
> dan el mismo resultado.

```python
import math


def distancia_manual(x1, y1, x2, y2):
    """Calcula la distancia con la fórmula euclidiana."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def distancia_con_dist(x1, y1, x2, y2):
    """Calcula la misma distancia usando math.dist."""
    return math.dist([x1, y1], [x2, y2])


if __name__ == "__main__":
    d1 = distancia_manual(0, 0, 3, 4)
    d2 = distancia_con_dist(0, 0, 3, 4)

    print(d1)                     # 5.0
    print(d2)                     # 5.0
    print(math.isclose(d1, d2))   # True

    # math.dist funciona con cualquier dimensión, no solo 2D.
    print(math.dist([1, 2, 3], [4, 5, 6]))
```

`math.dist` te ahorra escribir la fórmula, recibe dos secuencias de
coordenadas y funciona en cualquier dimensión.

---

## random: aleatoriedad controlada

Cuando necesitás valores impredecibles (dados de juego, muestreo de datos,
simulaciones) usás `random`.

### Números aleatorios básicos

```python
import random

random.random()             # float uniforme entre 0.0 y 1.0
random.uniform(1, 10)       # float uniforme entre 1 y 10
random.randint(1, 6)        # entero entre 1 y 6 (incluye ambos extremos)
random.randrange(0, 100, 5) # 0, 5, 10, ..., 95
```

**Diferencia importante:** `randint(1, 6)` **incluye** el 6;
`randrange(1, 6)` **no** lo incluye, porque funciona como `range`.

### Elegir de una secuencia

```python
random.choice(["rojo", "verde", "azul"])   # elige uno al azar
random.choices([1, 2, 3, 4], k=2)          # 2 CON reemplazo (repetibles)
random.sample([1, 2, 3, 4], k=2)           # 2 SIN reemplazo (únicos)
```

`choices` puede repetir el mismo elemento; `sample` no.

### Mezclar una lista

```python
mazo = ["A", "K", "Q", "J", "10", "9", "8", "7"]
random.shuffle(mazo)
print(mazo)     # los mismos elementos, en orden aleatorio
```

`shuffle` **modifica la lista en el lugar** y devuelve `None`. Si querés
preservar la original, usá `random.sample(mazo, k=len(mazo))`, que devuelve
una lista nueva mezclada.

### Semilla reproducible

Cuando estás debugueando, comparando resultados con un compañero o querés que
una simulación dé siempre lo mismo, fijá la **semilla** del generador:

```python
random.seed(42)
print(random.random())    # siempre el mismo número con seed=42
```

Con la misma semilla, la secuencia completa de números es idéntica. Es
imprescindible para poder reproducir un resultado; en producción no se fija.

### `secrets`: cuando la aleatoriedad tiene que ser secreta

Y acá viene la advertencia más importante de esta sección. `random` es un
**generador pseudoaleatorio**: produce una secuencia determinista a partir de
un estado interno. Es perfecto para simulaciones y juegos, y **completamente
inadecuado para secretos**. Si alguien puede inferir el estado del generador,
puede predecir todos los valores siguientes.

Para contraseñas, tokens de sesión, códigos de recuperación o cualquier cosa
que un atacante no deba poder adivinar, Python trae el módulo `secrets`, que
usa la fuente de aleatoriedad criptográfica del sistema operativo:

```python
import secrets
import string

alfabeto = string.ascii_letters + string.digits

# MAL: predecible si se conoce la semilla
clave = "".join(random.choices(alfabeto, k=12))

# BIEN
clave = "".join(secrets.choice(alfabeto) for _ in range(12))

# Y para tokens, directamente:
secrets.token_hex(16)      # '9f8c...' 32 caracteres hexadecimales
secrets.token_urlsafe(16)  # apto para poner en una URL
```

> **Regla:** `random` para simular, `secrets` para proteger. Si el valor
> tiene que ser difícil de adivinar, no uses `random`.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 2** — Simulá 1000 tiradas de dos dados. Contá cuántas veces
> sale doble (dos números iguales) y calculá el porcentaje. Fijá la semilla
> para que el resultado sea reproducible.

```python
import random

TIRADAS = 1000


def contar_dobles(tiradas):
    """Cuenta cuántas veces salen dos dados iguales."""
    dobles = 0

    for _ in range(tiradas):
        if random.randint(1, 6) == random.randint(1, 6):
            dobles += 1

    return dobles


if __name__ == "__main__":
    random.seed(42)

    dobles = contar_dobles(TIRADAS)
    porcentaje = dobles / TIRADAS * 100

    print(f"Dobles: {dobles} ({porcentaje:.2f}%)")
    print("Probabilidad teórica: 16.67% (1/6)")
```

La probabilidad teórica de un doble es 1/6 ≈ 16.67%. Con 1000 tiradas el
resultado va a estar cerca, aunque no exacto: es una simulación. Con la
semilla fija, sin embargo, **siempre da el mismo número**, y eso permite
comparar tu resultado con el de la solución.

---

## datetime: fechas y horas

Todo lo que tenga que ver con fechas (cuándo ocurrió algo, cuánto tiempo
pasó, cómo mostrarla) vive en `datetime`.

### Los cuatro tipos principales

```python
from datetime import datetime, date, time, timedelta
```

- **`datetime`**: fecha + hora combinadas. Es lo que más se usa.
- **`date`**: solo fecha (año, mes, día).
- **`time`**: solo hora (hora, minuto, segundo).
- **`timedelta`**: una **duración**, no un momento.

Los cuatro se escriben en minúscula: son los nombres reales de las clases.

### Crear una fecha

```python
ahora = datetime.now()
print(ahora)          # 2026-07-26 14:23:45.123456

hoy = date.today()
print(hoy)            # 2026-07-26

# Fechas explícitas
navidad = date(2026, 12, 25)
cumple = datetime(2026, 8, 15, 20, 30)   # 20:30 del 15/08/2026
```

### Acceso a componentes

Cada `datetime` expone sus partes como properties, exactamente el concepto
del capítulo 10:

```python
ahora = datetime.now()

print(ahora.year)        # 2026
print(ahora.month)       # 7
print(ahora.day)         # 26
print(ahora.hour)        # 14
print(ahora.minute)      # 23
print(ahora.second)      # 45
print(ahora.weekday())   # 0=lunes, ..., 6=domingo
```

### Diferencias entre fechas: `timedelta`

Restar dos fechas devuelve un `timedelta`:

```python
inicio = date(2026, 1, 1)
fin = date(2026, 12, 31)

diferencia = fin - inicio
print(diferencia)        # 364 days, 0:00:00
print(diferencia.days)   # 364
```

Y sumar un `timedelta` a una fecha da otra fecha:

```python
hoy = date.today()
en_una_semana = hoy + timedelta(days=7)
hace_un_mes = hoy - timedelta(days=30)
```

`timedelta` acepta `days`, `hours`, `minutes`, `seconds`, `weeks`,
`milliseconds` y `microseconds`.

### Formatear y parsear: `strftime` / `strptime`

Para convertir un `datetime` a texto con formato específico, `strftime`:

```python
ahora = datetime.now()

print(ahora.strftime("%d/%m/%Y"))   # 26/07/2026
print(ahora.strftime("%H:%M:%S"))   # 14:23:45
```

Los códigos más comunes:

| Código | Significado | Ejemplo |
|---|---|---|
| `%Y` | Año, 4 dígitos | 2026 |
| `%m` | Mes numérico | 07 |
| `%d` | Día del mes | 26 |
| `%H` | Hora, 24h | 14 |
| `%M` | Minuto | 23 |
| `%S` | Segundo | 45 |
| `%A` | Nombre del día | Sunday |
| `%B` | Nombre del mes | July |

Para el camino inverso (texto ➜ `datetime`), `strptime`:

```python
texto = "26/07/2026"
fecha = datetime.strptime(texto, "%d/%m/%Y")
print(fecha)        # 2026-07-26 00:00:00
```

**Truco mnemotécnico:** `strftime` = *format time* (hacia string),
`strptime` = *parse time* (desde string).

Un atajo cómodo: las f-strings aceptan directamente los códigos de
`strftime`, sin llamar al método.

```python
print(f"{ahora:%d/%m/%Y}")    # 26/07/2026
```

> **`%A` y `%B` dependen del idioma del sistema.** Por eso el ejemplo de
> arriba da `Sunday` y `July` y no `domingo` y `julio`: esos códigos usan el
> *locale* configurado, que en la mayoría de las instalaciones es inglés. Se
> puede cambiar con el módulo `locale`, pero es frágil y depende de qué
> idiomas tenga instalados el sistema. Para mostrar fechas en español, lo más
> robusto en un programa chico es una lista propia:
>
> ```python
> MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
>          "julio", "agosto", "septiembre", "octubre", "noviembre",
>          "diciembre"]
>
> print(f"{ahora.day} de {MESES[ahora.month - 1]} de {ahora.year}")
> # 26 de julio de 2026
> ```

### Fechas con y sin zona horaria

Un detalle que conviene conocer desde el principio. `datetime.now()` devuelve
un datetime **naive** (ingenuo): sabe qué hora es, pero no de dónde. Si dos
usuarios en husos distintos guardan "las 14:00", no hay forma de saber si se
refieren al mismo instante.

Un datetime **aware** (consciente) lleva la zona adjunta:

```python
from datetime import datetime, timezone

naive = datetime.now()
print(naive.tzinfo)                  # None

aware = datetime.now(timezone.utc)
print(aware.tzinfo)                  # UTC
print(aware.isoformat())             # 2026-07-26T17:23:45+00:00
```

La práctica profesional es **guardar todo en UTC y convertir solo al
mostrar**. Para nuestros programas de una sola máquina, `datetime.now()`
alcanza. Pero cuando lleguen a Django van a ver la opción `USE_TZ = True`
activada por defecto y un aviso cada vez que se guarda un datetime naive: es
exactamente esta distinción.

`timezone.utc` alcanza para trabajar en UTC. Si necesitás una zona con
nombre —con su desfasaje real y, donde corresponda, su horario de verano—
Python 3.9+ trae `zoneinfo`:

```python
from datetime import datetime
from zoneinfo import ZoneInfo

ahora = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
print(ahora.isoformat())        # 2026-07-26T14:23:45-03:00
```

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 3** — Escribí `dias_hasta_navidad()` que devuelva cuántos días
> faltan para la próxima Navidad (25 de diciembre). Si la de este año ya
> pasó, la próxima es la del año siguiente.

```python
from datetime import date


def dias_hasta_navidad(hoy=None):
    """Días que faltan para la próxima Navidad."""
    if hoy is None:
        hoy = date.today()

    navidad = date(hoy.year, 12, 25)

    if hoy > navidad:
        navidad = date(hoy.year + 1, 12, 25)

    return (navidad - hoy).days


if __name__ == "__main__":
    print(f"Faltan {dias_hasta_navidad()} días para Navidad")
    print(dias_hasta_navidad(date(2026, 12, 26)))    # 364
```

Restando dos objetos `date` obtenés un `timedelta`, y su atributo `.days` te
da la diferencia en días enteros. Notá el parámetro opcional `hoy`: permite
probar la función con fechas fijas en vez de depender del día en que se
ejecute.

---

## pathlib: rutas de archivos con sintaxis moderna

Manipular rutas como strings (`"C:/carpeta/subcarpeta/archivo.txt"`) es
propenso a errores: barras al revés en Windows, concatenación manual,
verificar si existe, obtener la extensión. Todo eso se resuelve con
`pathlib`.

### Crear un `Path`

```python
from pathlib import Path

archivo = Path("datos.txt")                    # ruta relativa
absoluto = Path("/home/usuario/datos.txt")     # ruta absoluta
mixto = Path("carpeta") / "subcarpeta" / "archivo.txt"
```

El operador `/` está sobrecargado para combinar componentes de ruta. Es el
mismo mecanismo de `__add__` que vimos en POO, con `__truediv__`. Funciona
igual en Windows, Mac y Linux: no hay que preocuparse por las barras.

### Componentes de una ruta

```python
ruta = Path("/home/ana/documentos/informe.pdf")

print(ruta.name)     # informe.pdf   nombre + extensión
print(ruta.stem)     # informe       nombre sin extensión
print(ruta.suffix)   # .pdf          extensión con punto
print(ruta.parent)   # /home/ana/documentos
print(ruta.parts)    # ('/', 'home', 'ana', 'documentos', 'informe.pdf')
```

### Existencia y tipo

```python
ruta = Path("datos.txt")

print(ruta.exists())    # True o False
print(ruta.is_file())   # True si es archivo
print(ruta.is_dir())    # True si es directorio
```

### Leer y escribir archivos

Con `pathlib` no hace falta `open` para archivos simples:

```python
ruta = Path("mensaje.txt")

ruta.write_text("Hola mundo", encoding="utf-8")
contenido = ruta.read_text(encoding="utf-8")
print(contenido)     # Hola mundo
```

> **`write_text` y `read_text` NO usan UTF-8 por defecto.** Es un error muy
> extendido. Sin el argumento `encoding`, estos métodos usan la codificación
> preferida del sistema, igual que `open()`: en Linux y Mac suele ser UTF-8,
> pero en Windows es habitualmente `cp1252`. El resultado es un archivo que
> se escribe bien en una máquina y se lee con caracteres rotos en otra, o un
> `UnicodeDecodeError` directamente.
>
> **Pasá siempre `encoding="utf-8"` explícito**, en `open()` y en los métodos
> de `Path`. Es la única forma de que el mismo archivo funcione en las tres
> plataformas.

Para archivos grandes o cuando querés control fino, seguimos usando `open`
con `with`:

```python
with open(ruta, "r", encoding="utf-8") as archivo:
    for linea in archivo:
        print(linea.strip())
```

### Recorrer directorios

```python
carpeta = Path("mi_proyecto")

# Todo lo que hay en la carpeta (no recursivo)
for item in carpeta.iterdir():
    print(item)

# Solo archivos .py de esta carpeta
for archivo_py in carpeta.glob("*.py"):
    print(archivo_py)

# Búsqueda recursiva, incluye subcarpetas
for archivo_py in carpeta.rglob("*.py"):
    print(archivo_py)
```

`glob` usa patrones: `*.py` es "cualquier cosa terminada en .py". `rglob(p)`
es equivalente a `glob("**/" + p)`.

### Crear directorios

```python
nueva = Path("resultados/reportes/mensuales")
nueva.mkdir(parents=True, exist_ok=True)
```

- `parents=True`: crea también las carpetas intermedias si no existen.
- `exist_ok=True`: no falla si la carpeta ya existía.

Es el idiom que vas a usar siempre antes de escribir un archivo en una
carpeta que quizás no está.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 4** — Escribí `contar_archivos_por_extension(carpeta)` que
> reciba un `Path` a una carpeta y devuelva un diccionario
> `{extensión: cantidad}` con los archivos de cada tipo.

```python
from collections import Counter
from pathlib import Path


def contar_archivos_por_extension(carpeta):
    """Cuenta los archivos directos agrupados por extensión."""
    contador = Counter(
        item.suffix
        for item in carpeta.iterdir()
        if item.is_file()
    )

    return dict(contador)


if __name__ == "__main__":
    resultado = contar_archivos_por_extension(Path("."))

    for extension, cantidad in sorted(resultado.items()):
        nombre = extension or "(sin extensión)"
        print(f"  {nombre}: {cantidad}")
```

`Counter` (de `collections`, que vemos más abajo) es un diccionario
especializado para contar: se puede construir directamente desde un
generador, sin inicializar ninguna clave.

---

## csv: leer y escribir archivos separados por comas

El formato **CSV** (*Comma-Separated Values*) es el más simple para datos
tabulares: una fila por línea, campos separados por comas. Excel y cualquier
hoja de cálculo lo abren, y es lo primero que se usa para exportar e importar
datos entre sistemas.

### Leer un CSV

Supongamos un archivo `alumnos.csv`:

```
nombre,edad,carrera
Ana,22,Ingeniería
Juan,25,Matemática
Pedro,20,Programación
```

Para leerlo:

```python
import csv

with open("alumnos.csv", newline="", encoding="utf-8") as archivo:
    lector = csv.reader(archivo)

    for fila in lector:
        print(fila)

# ['nombre', 'edad', 'carrera']
# ['Ana', '22', 'Ingeniería']
# ['Juan', '25', 'Matemática']
# ['Pedro', '20', 'Programación']
```

Cada fila es una **lista de strings**: todos los valores llegan como texto,
incluso los números. Convertirlos es responsabilidad de quien lee.

### `DictReader`: leer como diccionarios

Muchas veces es más cómodo trabajar con los nombres de columna:

```python
with open("alumnos.csv", newline="", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        print(f"{fila['nombre']} estudia {fila['carrera']}")
```

`DictReader` toma la primera línea como encabezados y devuelve cada fila como
un `dict`.

### Escribir un CSV

```python
alumnos = [
    ["nombre", "edad", "carrera"],
    ["Ana", 22, "Ingeniería"],
    ["Juan", 25, "Matemática"],
]

with open("salida.csv", "w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerows(alumnos)
```

O con diccionarios:

```python
alumnos = [
    {"nombre": "Ana", "edad": 22, "carrera": "Ingeniería"},
    {"nombre": "Juan", "edad": 25, "carrera": "Matemática"},
]

campos = ["nombre", "edad", "carrera"]

with open("salida.csv", "w", newline="", encoding="utf-8") as archivo:
    escritor = csv.DictWriter(archivo, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(alumnos)
```

> **Sobre `newline=""`:** incluilo siempre al abrir un archivo CSV. Sin él,
> en Windows aparecen líneas en blanco extra entre filas. Es el idiom
> estándar de Python y lo pide la propia documentación del módulo.

### CSV y dataclasses

Ahora que sabés POO, hay un paso natural: en vez de trabajar con diccionarios
sueltos, leer el CSV directamente a objetos. Con las `dataclass` del capítulo
13 sale en pocas líneas:

```python
import csv
from dataclasses import asdict, dataclass, fields


@dataclass
class Producto:
    """Producto leído desde una fila de CSV."""

    codigo: str
    nombre: str
    precio: float
    stock: int


def leer_csv(ruta):
    """Lee el CSV y devuelve una lista de objetos Producto."""
    with open(ruta, newline="", encoding="utf-8") as archivo:
        return [
            Producto(
                codigo=fila["codigo"],
                nombre=fila["nombre"],
                precio=float(fila["precio"]),
                stock=int(fila["stock"]),
            )
            for fila in csv.DictReader(archivo)
        ]


def guardar_csv(productos, ruta):
    """Guarda una lista de Producto en un archivo CSV."""
    campos = [campo.name for campo in fields(Producto)]

    with open(ruta, "w", newline="", encoding="utf-8") as salida:
        escritor = csv.DictWriter(salida, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(asdict(p) for p in productos)
```

`asdict()` convierte una dataclass en diccionario y `fields()` da la lista de
sus campos, así que los encabezados del CSV salen solos de la definición de
la clase. Con esto, el resto del programa trabaja con objetos `Producto`
—con sus métodos, sus validaciones y su `__eq__`— y el CSV queda como un
detalle de entrada y salida. Es la misma separación de responsabilidades del
capítulo 13.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 5** — Dado un CSV con notas de alumnos (columnas `nombre`,
> `materia`, `nota`), calculá el promedio de cada alumno y guardá el
> resultado en un CSV nuevo.

```python
import csv
from collections import defaultdict


def calcular_promedios(ruta_entrada, ruta_salida):
    """Agrupa las notas por alumno y guarda los promedios."""
    notas_por_alumno = defaultdict(list)

    with open(ruta_entrada, newline="", encoding="utf-8") as archivo:
        for fila in csv.DictReader(archivo):
            notas_por_alumno[fila["nombre"]].append(
                float(fila["nota"])
            )

    with open(ruta_salida, "w", newline="", encoding="utf-8") as salida:
        escritor = csv.writer(salida)
        escritor.writerow(["nombre", "promedio"])

        for nombre, notas in notas_por_alumno.items():
            promedio = sum(notas) / len(notas)
            escritor.writerow([nombre, f"{promedio:.2f}"])

    return notas_por_alumno
```

`defaultdict(list)` auto-crea una lista vacía la primera vez que se accede a
una clave nueva; sin él habría que escribir `if nombre not in ...` en cada
vuelta. En el archivo de ejercicios está la versión completa, que además
genera su propio CSV de entrada para poder ejecutarse tal cual.

---

## json: intercambio de datos estructurados

**JSON** (*JavaScript Object Notation*) es el formato estándar para
intercambiar datos entre sistemas: APIs web, archivos de configuración,
respuestas de servicios. Se parece mucho a los diccionarios de Python.

### El formato

```json
{
  "nombre": "Ana",
  "edad": 22,
  "carreras": ["Ingeniería", "Matemática"],
  "activa": true,
  "direccion": {
    "calle": "Av. 7",
    "numero": 1234
  }
}
```

Casi igual que un `dict` de Python. Diferencias: `true`/`false` en minúscula,
`null` en vez de `None`, y comillas siempre dobles.

### Convertir Python ⇄ JSON

```python
import json

datos = {
    "nombre": "Ana",
    "edad": 22,
    "aprobados": True,
    "materias": ["Prog2", "IO"],
}

# Python a texto JSON
texto = json.dumps(datos)
print(texto)
# {"nombre": "Ana", "edad": 22, "aprobados": true, ...}

# Con indentación, para que lo lea un humano
texto_bonito = json.dumps(datos, indent=2, ensure_ascii=False)

# Texto JSON a Python
recuperado = json.loads(texto)
print(recuperado["nombre"])    # Ana
```

`ensure_ascii=False` es importante si tenés acentos: sin él, "Pérez" se
guarda como `"P\u00e9rez"`, que es válido pero ilegible al abrir el archivo.

### Leer y escribir archivos JSON

```python
# Escribir
with open("datos.json", "w", encoding="utf-8") as archivo:
    json.dump(datos, archivo, indent=2, ensure_ascii=False)

# Leer
with open("datos.json", encoding="utf-8") as archivo:
    datos = json.load(archivo)
```

Notá la diferencia: `dumps`/`loads` trabajan con **strings** (la `s` es de
*string*), `dump`/`load` con **archivos**.

### Qué entiende JSON y qué no

JSON solo conoce tipos básicos: string, número, booleano, `null`, lista y
objeto. Eso tiene dos consecuencias que sorprenden:

```python
from datetime import datetime

json.loads(json.dumps({"punto": (3, 5)}))
# {'punto': [3, 5]}   ← la tupla volvió como lista

json.dumps({"cuando": datetime.now()})
# TypeError: Object of type datetime is not JSON serializable
```

Las tuplas se serializan como listas y vuelven como listas. Los `datetime`
directamente no se pueden serializar: hay que convertirlos a texto con
`.isoformat()` y reconstruirlos con `datetime.fromisoformat()` al leer.

### Serializar objetos propios

Si querés guardar un objeto de una clase tuya, primero hay que convertirlo a
algo que JSON entienda. El idiom es un par de métodos:

```python
class Persona:
    """Persona que sabe convertirse a diccionario y volver."""

    def __init__(self, nombre, edad):
        self._nombre = nombre
        self._edad = edad

    def to_dict(self):
        """Devuelve la persona como diccionario serializable."""
        return {"nombre": self._nombre, "edad": self._edad}

    @classmethod
    def from_dict(cls, datos):
        """Reconstruye una Persona desde un diccionario."""
        return cls(datos["nombre"], datos["edad"])


# Serializar
ana = Persona("Ana", 22)
texto = json.dumps(ana.to_dict())

# Deserializar
recuperada = Persona.from_dict(json.loads(texto))
```

> **`@classmethod`, un decorador nuevo.** En el capítulo 13 vimos
> `@property`, `@abstractmethod` y `@dataclass`. Este es el cuarto.
> Un método decorado con `@classmethod` recibe como primer parámetro **la
> clase**, no la instancia; por convención se lo llama `cls` en vez de
> `self`. Sirve para escribir **constructores alternativos**: `Persona(...)`
> construye desde nombre y edad, `Persona.from_dict(...)` construye desde un
> diccionario, y los dos devuelven una `Persona`.
>
> Usar `cls(...)` en vez de `Persona(...)` no es un capricho: si mañana
> alguien hereda de `Persona`, `from_dict` va a construir la subclase
> correcta sin cambios. Es el mismo principio de sustitución del capítulo 13.

Si la clase es una `dataclass`, `asdict()` te da el `to_dict` gratis y
`cls(**datos)` te da el `from_dict`.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 6** — Guardá una lista de contactos (nombre y teléfono) en
> `contactos.json`, después leelo de vuelta y mostralos por pantalla, para
> comprobar que la ida y la vuelta conservan los datos.

```python
import json


def guardar_contactos(contactos, ruta):
    """Guarda la lista de contactos en un archivo JSON."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(contactos, archivo, indent=2, ensure_ascii=False)


def cargar_contactos(ruta):
    """Lee la lista de contactos desde un archivo JSON."""
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)


if __name__ == "__main__":
    contactos = [
        {"nombre": "Ana Pérez", "telefono": "221-1234"},
        {"nombre": "Juan Gómez", "telefono": "221-5678"},
    ]

    guardar_contactos(contactos, "contactos.json")
    recuperados = cargar_contactos("contactos.json")

    for contacto in recuperados:
        print(f"  {contacto['nombre']}: {contacto['telefono']}")

    assert recuperados == contactos, "Se perdieron datos"
```

JSON es el formato de referencia para persistencia liviana. Cuando lleguen a
Django van a ver que las APIs REST devuelven JSON casi siempre.

---

## re: expresiones regulares

Las **expresiones regulares** (o *regex*) son patrones de texto. Sirven para
validar un formato (email, teléfono), extraer partes de una cadena (buscar
todos los números de un texto) o reemplazar con criterio (colapsar espacios
múltiples). El módulo se llama `re`.

### Los patrones básicos

Un patrón es un string con caracteres normales y **metacaracteres**
especiales:

| Metacarácter | Significa |
|---|---|
| `.` | Cualquier carácter, excepto salto de línea |
| `\d` | Un dígito (0-9) |
| `\w` | Letra, dígito o guion bajo |
| `\s` | Espacio, tabulación o salto de línea |
| `\D` `\W` `\S` | Lo opuesto de los anteriores |
| `\b` | Límite de palabra |
| `^` | Inicio del string |
| `$` | Fin del string |
| `[abc]` | Cualquier carácter de los del corchete |
| `[a-z]` | Rango de caracteres |
| `[^abc]` | Cualquiera **excepto** los del corchete |
| `*` | 0 o más veces del anterior |
| `+` | 1 o más veces del anterior |
| `?` | 0 o 1 vez (opcional) |
| `{n}` | Exactamente n veces |
| `{n,m}` | Entre n y m veces |
| `\` | Escape, para usar un metacarácter literal |
| `(...)` | Grupo que captura |
| `(?:...)` | Grupo que agrupa pero no captura |
| `\|` | Alternativa (o) |

### `search`: la primera coincidencia

```python
import re

texto = "Mi teléfono es 221-1234567"
resultado = re.search(r"\d{3}-\d{7}", texto)

if resultado:
    print(resultado.group())    # 221-1234567
```

El `r` antes del string (`r"..."`) es un **raw string**: le dice a Python que
no interprete `\d` como una secuencia de escape. Se usa siempre con regex.

### `findall`: todas las coincidencias

```python
texto = "Ana tiene 25 años, Juan tiene 30, Pedro tiene 22"
edades = re.findall(r"\d+", texto)
print(edades)     # ['25', '30', '22']
```

### `sub`: reemplazar

```python
texto = "hola     mundo \n\n\t python"
limpio = re.sub(r"\s+", " ", texto)
print(repr(limpio))     # 'hola mundo python'
```

`\s+` matchea uno o más blancos consecutivos (espacios, tabulaciones o saltos
de línea) y los reemplaza por un solo espacio. Es la forma estándar de
normalizar texto que viene de un formulario o de copiar y pegar.

`sub` también acepta una **función** en lugar de una cadena de reemplazo: la
llama con cada coincidencia y usa lo que devuelva. Sirve cuando el reemplazo
depende de lo encontrado:

```python
def enmascarar(coincidencia):
    """Devuelve tantas X como dígitos tenía el número."""
    return "X" * len(coincidencia.group())


print(re.sub(r"\b\d{7,8}\b", enmascarar, "DNI 12345678 y 8765432"))
# DNI XXXXXXXX y XXXXXXX
```

### `match` y `fullmatch`: coincidencia desde el principio

```python
re.match(r"\d{8}", "12345678abc")      # coincide: solo mira el inicio
re.fullmatch(r"\d{8}", "12345678abc")  # None: exige cubrir todo
```

`match` chequea el patrón **desde el inicio** pero no le importa qué haya
después; por eso se lo suele acompañar de `$`. `fullmatch` exige que el
patrón cubra **toda** la cadena y es más claro y más difícil de equivocar.
Para validar formatos completos, preferí `fullmatch`.

### Grupos: capturar partes

Los paréntesis capturan lo que matchea adentro para usarlo después:

```python
texto = "Fecha: 26/07/2026"
resultado = re.search(r"(\d{2})/(\d{2})/(\d{4})", texto)

if resultado:
    dia, mes, anio = resultado.groups()
    print(f"Día: {dia}, Mes: {mes}, Año: {anio}")
```

`groups()` devuelve una tupla con lo capturado en cada grupo, en orden. Si el
grupo está solo para agrupar y no querés capturarlo, usá `(?:...)`.

### `re.compile`: el objeto `Pattern`

Cuando el mismo patrón se usa muchas veces, conviene **compilarlo una sola
vez**. `re.compile` devuelve un objeto `re.Pattern` con los mismos métodos
que el módulo:

```python
PATRON_EMAIL = re.compile(r"[\w.-]+@[\w.-]+\.\w+")

PATRON_EMAIL.findall(texto)
PATRON_EMAIL.fullmatch("ana@correo.com")
PATRON_EMAIL.sub("[oculto]", texto)

print(type(PATRON_EMAIL))     # <class 're.Pattern'>
print(PATRON_EMAIL.pattern)   # el string original
```

Acá se ve claro lo que decíamos al principio del capítulo: la biblioteca
estándar es POO. `re.compile` es una fábrica que devuelve un objeto, y ese
objeto tiene métodos y atributos propios. Además, ponerlo en una constante en
mayúsculas al tope del módulo le da nombre a la intención: se lee
`PATRON_EMAIL.findall(...)` en vez de un jeroglífico en medio del código.

### Cuándo usar regex y cuándo no

Las expresiones regulares son poderosas pero **difíciles de leer**. Regla
práctica:

**Sí:** patrones simples y bien definidos (formato de DNI, teléfono,
extracción de números, limpieza de espacios).

**No:** parsear HTML o JSON (hay librerías específicas), validaciones muy
complejas (mejor código con `if` y funciones), o cuando un `str.split()` o
`str.replace()` alcanza.

Si tu regex pasa los 40 caracteres y tiene varios grupos anidados,
probablemente convenga otra solución.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 7** — Validá si un texto tiene formato de email con una
> expresión regular.

```python
import re

PATRON_EMAIL = re.compile(r"[\w.-]+@[\w.-]+\.\w+")


def es_email(texto):
    """Devuelve True si el texto tiene forma de email."""
    return PATRON_EMAIL.fullmatch(texto) is not None


print(es_email("ana@correo.com"))   # True
print(es_email("no es email"))      # False
```

Este patrón es una **aproximación didáctica**. La especificación real de
direcciones de correo es sorprendentemente compleja, y en un sistema de
verdad la validación definitiva es enviar un mail y ver si llega.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 8** — Extraé los números del texto `"El precio es $3.500 y el
> descuento del 15% deja $2.975"`.

```python
texto = "El precio es $3.500 y el descuento del 15% deja $2.975"
numeros = re.findall(r"\d+(?:\.\d+)?", texto)
print(numeros)    # ['3.500', '15', '2.975']
```

Cuidado con el punto: acá es **separador de miles**, no decimal. `3.500` son
tres mil quinientos, así que para convertirlos a número hay que sacar el
punto primero: `float(numero.replace(".", ""))`.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 9** — Limpiá un texto con espacios, saltos de línea y
> tabulaciones repetidos para obtener `"Ana María Pérez"`.

```python
sucio = "   Ana    María \n\n\t  Pérez   "
limpio = re.sub(r"\s+", " ", sucio).strip()
print(repr(limpio))     # 'Ana María Pérez'
```

`re.sub` colapsa los blancos internos y `strip()` recorta los de los
extremos. Los dos pasos son necesarios.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 10** — Escribí `formatear_telefono(numero)` que reciba un
> teléfono en cualquier formato (`2211234567`, `221-123-4567`,
> `221 1234567`) y devuelva siempre `221-123-4567`.

```python
import re

PATRON_NO_DIGITO = re.compile(r"\D")


def formatear_telefono(numero):
    """Normaliza un teléfono de diez dígitos al formato estándar."""
    solo_digitos = PATRON_NO_DIGITO.sub("", numero)

    if len(solo_digitos) != 10:
        raise ValueError(
            f"Se esperaban 10 dígitos, hay {len(solo_digitos)}"
        )

    return (
        f"{solo_digitos[:3]}-"
        f"{solo_digitos[3:6]}-"
        f"{solo_digitos[6:]}"
    )
```

Estrategia común: primero **normalizar** (quitar todo lo que no sirve),
después **reformatear** (agregar la estructura deseada). Mucho más simple que
armar un regex que matchee todos los formatos posibles de entrada.

---

## collections: estructuras de datos especializadas

El módulo `collections` trae estructuras que **extienden** las básicas
(`list`, `dict`, `set`) para casos específicos.

### `Counter`: contar elementos

```python
from collections import Counter

texto = "hola mundo, mundo hola python"
conteo = Counter(texto.split())

print(conteo)
# Counter({'hola': 2, 'mundo,': 1, 'mundo': 1, 'python': 1})

print(conteo.most_common(2))
# [('hola', 2), ('mundo,', 1)]
```

`Counter` es un `dict` especializado que cuenta ocurrencias. Hereda de `dict`,
así que todo lo que sabés de diccionarios sirve acá. Lo propio:

- `most_common(n)`: los n elementos más frecuentes, como lista de tuplas.
- Devuelve `0` en lugar de `KeyError` para una clave que nunca vio.
- Se pueden sumar, restar y comparar dos `Counter` entre sí.

### `defaultdict`: diccionario con valor por defecto

Un `defaultdict` **auto-crea un valor** cuando accedés a una clave nueva:

```python
from collections import defaultdict

# Con dict normal esto falla:
# d = {}
# d["nueva"].append(1)      # KeyError

d = defaultdict(list)
d["nueva"].append(1)        # crea automáticamente d["nueva"] = []
d["nueva"].append(2)
print(d)     # defaultdict(<class 'list'>, {'nueva': [1, 2]})
```

Es muy útil para agrupar. Recorrés una lista y agrupás por criterio:

```python
alumnos = [
    ("Ana", "Ingeniería"),
    ("Juan", "Matemática"),
    ("Pedro", "Ingeniería"),
]

por_carrera = defaultdict(list)

for nombre, carrera in alumnos:
    por_carrera[carrera].append(nombre)

for carrera, nombres in por_carrera.items():
    print(f"{carrera}: {', '.join(nombres)}")

# Ingeniería: Ana, Pedro
# Matemática: Juan
```

El argumento de `defaultdict` es una **función sin parámetros** que fabrica el
valor: `list` da `[]`, `int` da `0`, `set` da `set()`. Es el mismo mecanismo
que `default_factory` en las dataclasses del capítulo 13, y por la misma
razón: si pusieras `[]` directo, todas las claves compartirían la misma lista.

### `namedtuple`: tuplas con nombres

Una `namedtuple` es una tupla donde cada posición tiene nombre:

```python
from collections import namedtuple

Punto = namedtuple("Punto", ["x", "y"])
p = Punto(3, 5)

print(p.x, p.y)       # 3 5
print(p[0], p[1])     # 3 5, también funciona por índice
x, y = p              # y se desempaqueta como cualquier tupla
```

Se parece a una `@dataclass(frozen=True)`: es más antigua, más liviana y, al
ser una tupla, se puede indexar y desempaquetar. A cambio, no admite métodos
propios ni valores por defecto cómodos.

**Hoy se prefiere `@dataclass`**, salvo cuando necesitás que el objeto *sea*
una tupla (para desempaquetar, o para pasarlo a código que espera tuplas).
`namedtuple` sigue muy vivo en código heredado y en la propia biblioteca
estándar: por ejemplo, `os.stat()` devuelve una.

### `deque`: cola de doble punta

Una `deque` (*double-ended queue*) es como una lista, pero **muy eficiente**
para agregar y quitar en los dos extremos:

```python
from collections import deque

cola = deque([1, 2, 3])

cola.append(4)        # al final:      [1, 2, 3, 4]
cola.appendleft(0)    # al principio:  [0, 1, 2, 3, 4]
cola.pop()            # quita del final:     4
cola.popleft()        # quita del principio: 0
```

En una lista normal, `list.insert(0, x)` y `list.pop(0)` obligan a correr
todos los elementos: son O(n). En una `deque` son O(1). Si vas a operar mucho
en los extremos, `deque` gana; para acceso por índice en el medio, la lista
sigue siendo mejor.

### Nota: los `dict` ya vienen ordenados

Es posible que veas `OrderedDict` en código o en tutoriales viejos. **Desde
Python 3.7, los diccionarios normales conservan el orden de inserción como
parte del lenguaje**, así que `OrderedDict` casi no se usa: solo cuando
necesitás sus métodos propios, como `move_to_end()`, o comparación sensible
al orden. Para todo lo demás, alcanza con un `dict`.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 11** — Usá `Counter` sobre una lista de notas para contar la
> frecuencia de cada una y mostrar cuál fue la más frecuente.

```python
from collections import Counter

notas = [7, 8, 5, 9, 7, 8, 6, 7, 10, 5]
conteo = Counter(notas)

print(conteo)
# Counter({7: 3, 8: 2, 5: 2, 9: 1, 6: 1, 10: 1})

for nota in sorted(conteo):
    print(f"  {nota:>2}: {'#' * conteo[nota]}")

mas_frecuente, veces = conteo.most_common(1)[0]
print(f"La nota más frecuente fue {mas_frecuente} ({veces})")
```

`most_common(1)` devuelve una lista con una sola tupla, por eso el `[0]`
antes de desempaquetar.

---

## enum: un conjunto cerrado de valores con nombre

Cuando una variable solo puede tomar unos pocos valores fijos (el estado de
un pedido, el palo de una carta, el tipo de un movimiento bancario), la
tentación es usar strings sueltos: `"deposito"`, `"extraccion"`. Funciona,
pero nada impide escribir `"depsito"` con un error de tipeo, y el editor no
ayuda porque para él es texto cualquiera.

El módulo `enum` resuelve esto: define una clase donde cada valor posible es
un miembro con nombre.

```python
from enum import Enum


class TipoMovimiento(Enum):
    """Los únicos tipos de movimiento que existen."""

    DEPOSITO = "deposito"
    EXTRACCION = "extraccion"


print(TipoMovimiento.DEPOSITO)         # TipoMovimiento.DEPOSITO
print(TipoMovimiento.DEPOSITO.name)    # 'DEPOSITO'
print(TipoMovimiento.DEPOSITO.value)   # 'deposito'
```

Es una clase como las del capítulo 11: podés darle métodos, y sus miembros
son objetos únicos (existe **un solo** `TipoMovimiento.DEPOSITO` en todo el
programa, así que se comparan con `is`).

```python
tipo = TipoMovimiento.DEPOSITO

if tipo is TipoMovimiento.DEPOSITO:
    print("suma al saldo")

# Recuperar el miembro desde su valor guardado:
TipoMovimiento("deposito")     # TipoMovimiento.DEPOSITO
TipoMovimiento("depsito")      # ValueError: 'depsito' is not a valid ...
```

Esa última línea es la ganancia: un valor inválido **explota al instante**,
en vez de propagarse como un string silencioso que rompe algo tres funciones
más adelante.

### Variantes útiles

```python
from enum import Enum, IntEnum, auto


class Prioridad(IntEnum):        # se comporta además como int
    BAJA = 1
    MEDIA = 2
    ALTA = 3


Prioridad.ALTA > Prioridad.BAJA   # True


class Color(Enum):
    ROJO = auto()                # 1, 2, 3... si el valor no te importa
    VERDE = auto()
    AZUL = auto()
```

- `IntEnum`: los miembros son enteros de verdad, se pueden comparar y ordenar.
- `auto()`: asigna valores automáticos cuando solo te interesa el nombre.

Para persistir un enum en JSON o CSV se guarda `.value` y se reconstruye con
`TipoMovimiento(valor)`, exactamente el mismo idiom `to_dict` / `from_dict`
que venimos usando.

---

## itertools y functools: iteración y funciones

Dos módulos chicos que aparecen todo el tiempo en código Python idiomático.
No hace falta dominarlos ahora, pero conviene saber que existen.

`itertools` arma iteradores combinables sin cargar todo en memoria:

```python
import itertools

itertools.chain([1, 2], [3, 4])          # 1, 2, 3, 4  (encadena)
itertools.count(10)                       # 10, 11, 12, ... infinito
itertools.islice(itertools.count(), 5)    # 0, 1, 2, 3, 4  (los primeros 5)
list(itertools.combinations("ABC", 2))    # [('A','B'), ('A','C'), ('B','C')]

# Agrupar elementos consecutivos por una clave (la lista tiene que venir
# ordenada por esa misma clave):
datos = [("fruta", "pera"), ("fruta", "uva"), ("verdura", "papa")]
for clave, grupo in itertools.groupby(datos, key=lambda par: par[0]):
    print(clave, [x[1] for x in grupo])
```

`functools` opera sobre funciones:

```python
from functools import lru_cache, reduce


@lru_cache(maxsize=None)
def fib(n):
    """Cachea cada resultado: la segunda llamada con el mismo n es gratis."""
    return n if n < 2 else fib(n - 1) + fib(n - 2)


reduce(lambda acum, x: acum + x, [1, 2, 3, 4], 0)   # 10  (suma acumulada)
```

`@lru_cache` es el más usado: memoiza una función pura (misma entrada, misma
salida) sin que escribas el diccionario de cache a mano.

---

## Cierre: el banco que sobrevive al apagado

Llegamos al final del capítulo con una pieza que le faltaba al proyecto desde
el capítulo 9. Nuestro banco funciona perfecto mientras el programa está
corriendo, y desaparece por completo apenas se cierra: las cuentas viven solo
en memoria.

Con `json` y `pathlib` podemos arreglarlo sin tocar la lógica de negocio. La
estrategia es la del idiom `to_dict` / `from_dict`: cada clase sabe
convertirse a tipos básicos y reconstruirse desde ellos, y dos funciones
sueltas se ocupan del archivo.

```python
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class Movimiento:
    """Registro inmutable de una operación sobre una cuenta."""

    tipo: str
    monto: float
    fecha: str

    def to_dict(self):
        """Devuelve el movimiento como diccionario serializable."""
        return asdict(self)

    @classmethod
    def from_dict(cls, datos):
        """Reconstruye un Movimiento desde un diccionario."""
        return cls(**datos)
```

Notá que la fecha se guarda como **texto ISO**, no como `datetime`: JSON no
sabe serializar fechas, así que las convertimos al construir el movimiento
con `datetime.now().isoformat()` y podemos recuperarlas, si hace falta, con
`datetime.fromisoformat()`.

El campo `tipo` es un `str` para no alargar el ejemplo, pero es justo el caso
de la sección de `enum`: un `TipoMovimiento(Enum)` evitaría que se cuele un
`"depsito"` mal escrito. Se guardaría `tipo.value` en el diccionario y se
reconstruiría con `TipoMovimiento(datos["tipo"])` en `from_dict`.

La cuenta hace lo mismo, delegando en sus movimientos:

```python
class Cuenta:
    """Cuenta que sabe convertirse a diccionario y volver."""

    def __init__(self, numero, titular, saldo=0, movimientos=None):
        self._numero = numero
        self._titular = titular
        self._saldo = saldo
        self._movimientos = list(movimientos or [])

    def to_dict(self):
        """Devuelve la cuenta como diccionario serializable."""
        return {
            "numero": self._numero,
            "titular": self._titular,
            "saldo": self._saldo,
            "movimientos": [
                movimiento.to_dict()
                for movimiento in self._movimientos
            ],
        }

    @classmethod
    def from_dict(cls, datos):
        """Reconstruye una Cuenta desde un diccionario."""
        return cls(
            numero=datos["numero"],
            titular=datos["titular"],
            saldo=datos["saldo"],
            movimientos=[
                Movimiento.from_dict(movimiento)
                for movimiento in datos["movimientos"]
            ],
        )
```

Y la persistencia queda en dos funciones que no saben nada de bancos:

```python
def guardar_banco(cuentas, ruta):
    """Guarda todas las cuentas del banco en un archivo JSON."""
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(
            [cuenta.to_dict() for cuenta in cuentas],
            archivo,
            indent=2,
            ensure_ascii=False,
        )


def cargar_banco(ruta):
    """Reconstruye las cuentas del banco desde un archivo JSON."""
    with open(ruta, encoding="utf-8") as archivo:
        return [
            Cuenta.from_dict(datos) for datos in json.load(archivo)
        ]
```

Uso:

```python
ruta = Path("datos") / "banco.json"

ahorro = Cuenta("A-1", "Ana Pérez", 10000)
ahorro.depositar(2500)

guardar_banco([ahorro], ruta)

# ... el programa termina, la máquina se apaga, pasa una semana ...

recuperadas = cargar_banco(ruta)

assert recuperadas[0].saldo == ahorro.saldo
assert recuperadas[0].historial() == ahorro.historial()
```

Mirá el reparto de responsabilidades, que es el del capítulo 13 aplicado a un
problema nuevo:

- `Movimiento` y `Cuenta` **no saben qué es JSON**. Solo saben convertirse a
  diccionario y volver, que son tipos de Python.
- `guardar_banco` y `cargar_banco` **no saben qué es una cuenta**. Solo
  serializan lo que les den.
- Si mañana hay que guardar en CSV, en una base de datos o mandar los datos
  por una API, se escriben funciones nuevas y las clases del dominio **no
  cambian**. Es exactamente el `RepositorioCuentas` del capítulo 13: la
  lógica de negocio depende de una abstracción, no de un formato.

![Diagrama en dos filas. Fila de arriba, IDA (guardar_banco): tres cajas
conectadas por flechas de izquierda a derecha —"Cuenta / Movimiento", objetos
del dominio; luego "dict / list", tipos básicos de Python; luego "banco.json",
archivo en disco. La primera flecha está rotulada .to_dict() y la segunda
json.dump(). Fila de abajo, VUELTA (cargar_banco): las mismas tres cajas pero
las flechas van de derecha a izquierda —de "banco.json" a "dict / list" con
json.load(), y de "dict / list" a "Cuenta / Movimiento" con .from_dict(),
reconstruyendo los objetos. Un recuadro punteado encierra la columna de las
clases con la nota "no saben qué es JSON" y otro encierra la columna del
archivo con "json + pathlib". Al pie: guardar_banco() y cargar_banco() no
saben qué es una cuenta; es el mismo reparto de responsabilidades que
RepositorioCuentas en el capítulo 13.](images/persistencia-ida-y-vuelta.png)

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 12** — Completá el cierre: dale a `Movimiento` y a `Cuenta` sus
> métodos `to_dict()` y `from_dict()`, guardá todas las cuentas en
> `banco.json` y volvé a cargarlas. Verificá con `assert` que los saldos y
> los historiales se conservan intactos.

La versión completa y ejecutable está en el archivo de ejercicios.

Y con esto cerramos el recorrido. Empezamos en el capítulo 1 con variables y
`print`, y terminamos con un sistema bancario que valida sus datos, organiza
sus tipos en una jerarquía, reparte responsabilidades entre clases, respeta
los cinco principios SOLID y ahora también sobrevive al apagado de la
computadora. El año que viene, cuando abran Django, van a encontrar cada una
de esas piezas con otro nombre y hechas por el framework. Pero ya van a saber
qué hacen y por qué.
