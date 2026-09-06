# Capítulo 13. POO: Diseño con SOLID y clases abstractas

*Escribiendo código que sobrevive al tiempo.*

## ¿Por qué leemos este capítulo?

En los capítulos anteriores construimos un sistema bancario real, capa por
capa. Aprendimos a hacer objetos, a protegerlos con encapsulamiento, a
especializarlos con herencia, a componerlos en sistemas más grandes. En cada
iteración el proyecto creció y el diseño se mantuvo, no por casualidad sino
porque veníamos tomando decisiones correctas sin nombrarlas todavía.

Este capítulo es distinto. No trae mucha sintaxis nueva. Trae cinco
principios que sirven como brújula para saber si un diseño está bien pensado.
Se conocen colectivamente como **SOLID**: un acrónimo de cinco letras, una
por cada principio.

SOLID no son leyes, son heurísticas. No hay que aplicarlas al pie de la letra
en todos los ejercicios. Son herramientas para responder preguntas como "¿por
qué esta clase se está volviendo un monstruo?", "¿por qué agregar una
funcionalidad rompió tres cosas al mismo tiempo?", "¿por qué estoy copiando y
pegando código otra vez?".

Los cinco principios son:

- **SRP**: *Single Responsibility Principle* (responsabilidad única).
- **OCP**: *Open/Closed Principle* (abierto a extensión, cerrado a
  modificación).
- **LSP**: *Liskov Substitution Principle* (sustitución de Liskov).
- **ISP**: *Interface Segregation Principle* (segregación de interfaces).
- **DIP**: *Dependency Inversion Principle* (inversión de dependencias).

Además de SOLID vamos a ver cuatro herramientas que apoyan estos principios
en Python:

- **Clases abstractas** (`ABC` y `@abstractmethod`): la formalización del
  "método abstracto conceptual" que veníamos haciendo con
  `NotImplementedError`.
- **Type hints**: anotaciones que declaran los tipos esperados. Documentan la
  intención y ayudan al IDE.
- **Protocolos** (`typing.Protocol`): la forma pythónica de declarar una
  interfaz sin obligar a heredar de nada.
- **Dataclasses**: una forma moderna y compacta de crear clases-contenedor.

Y como cierre, la **iteración 5**: aplicamos todo lo aprendido para dejar el
sistema bancario en su forma final, listo para servir de base a Django el año
que viene.

## SRP: Responsabilidad Única

> **Principio:** cada clase debería tener una sola razón para cambiar.

Ya vimos SRP intuitivamente en el capítulo 12. Ahora lo formalizamos.

**La idea.** Una clase debería hacer una sola cosa bien. Si podés describir lo
que hace usando la palabra "y" varias veces, probablemente estés violando
SRP: *"esta clase gestiona cuentas **y** envía notificaciones **y** genera
reportes **y** calcula impuestos"*. Cada una de esas "y" es una razón para
cambiar la clase, y cada cambio corre el riesgo de romper todo lo demás.

**Contraejemplo:** una clase que hace demasiado.

```python
class GestorDeCuentas:
    def __init__(self):
        self._cuentas = {}

    def abrir_cuenta(self, numero, titular): ...
    def cerrar_cuenta(self, numero): ...

    # Estos métodos NO son responsabilidad del gestor de cuentas
    def enviar_email(self, destinatario, mensaje): ...
    def exportar_a_csv(self, ruta): ...
    def calcular_impuestos(self): ...
    def imprimir_reporte_mensual(self): ...
```

Esta clase tiene al menos cinco razones para cambiar: si cambia la lógica de
cuentas, si cambia el servidor de email, si cambia el formato del CSV, si
cambia la ley impositiva, si cambia el formato del reporte. Cada uno de esos
cambios puede introducir bugs en las otras responsabilidades. Y si mañana
necesito enviar emails desde otra parte del sistema, tengo que duplicar
código o arrastrar un `GestorDeCuentas` entero para algo que no tiene nada que
ver con cuentas.

**Solución:** partir en clases con responsabilidades específicas.

```python
class GestorDeCuentas:
    """Solo gestiona la colección de cuentas."""

    def abrir_cuenta(self, numero, titular): ...
    def cerrar_cuenta(self, numero): ...


class NotificadorEmail:
    """Solo sabe enviar emails."""

    def enviar(self, destinatario, mensaje): ...


class ExportadorCSV:
    """Solo sabe exportar a CSV."""

    def exportar(self, cuentas, ruta): ...


class CalculadorImpuestos:
    """Solo calcula impuestos."""

    def calcular(self, cuentas): ...
```

Cada una es más chica, más testeable, más reutilizable. Los cambios en una no
tocan las otras.

### SRP en nuestro banco

| Clase | Responsabilidad única |
|---|---|
| `Cuenta` | Manejar el saldo y el historial de una cuenta |
| `Persona` | Representar la identidad de un titular |
| `Movimiento` | Registrar un evento de operación |
| `Banco` | Gestionar la colección de cuentas (ABM) |
| `validaciones.py` | Validar y normalizar datos |
| `errores.py` | Definir las excepciones del dominio |

Ninguna clase hace más de lo que dice su nombre. Cada una tiene una sola
razón para cambiar y esa razón está bien acotada. Nuestro diseño ya respetaba
SRP sin haberlo nombrado: lo veníamos aplicando desde el capítulo 10.

### Señales de alarma de SRP violado

- La clase tiene más de 200 o 300 líneas.
- Al describir qué hace, usás mucho la palabra "y".
- El nombre de la clase es genérico: `Utils`, `Helper`, `Manager`, `Handler`,
  `Manejador`.
- Tiene métodos que no comparten atributos entre sí: viven en la misma clase
  por conveniencia, no por lógica.
- Al modificar un método por un cambio de requerimientos, rompés cosas que no
  tenían nada que ver.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 1** — Identificá por qué esta clase viola SRP y proponé cómo
> partirla.

```python
class Alumno:
    def __init__(self, nombre, notas):
        self.nombre = nombre
        self.notas = notas

    def promedio(self):
        return sum(self.notas) / len(self.notas)

    def guardar_en_archivo(self, ruta):
        with open(ruta, "w") as archivo:
            archivo.write(f"{self.nombre}: {self.notas}")

    def enviar_boletin_por_email(self, email):
        # ... conecta a un servidor SMTP, envía el mail, etc.
        pass
```

**Solución.** `Alumno` tiene tres responsabilidades: representar un alumno
(nombre, notas, promedio), persistir en archivo y notificar por email. Cada
una tiene su propia razón para cambiar: si cambia la definición de "alumno",
si cambia el formato de archivo, o si cambia el servidor SMTP.

```python
class Alumno:
    """Representa un alumno y calcula su promedio. Nada más."""

    def __init__(self, nombre, notas):
        self._nombre = nombre
        self._notas = list(notas)

    def nombre(self):
        """Devuelve el nombre del alumno."""
        return self._nombre

    def notas(self):
        """Devuelve una copia de las notas."""
        return list(self._notas)

    def promedio(self):
        """Promedio de las notas; 0 si todavía no tiene ninguna."""
        if not self._notas:
            return 0

        return sum(self._notas) / len(self._notas)


class RepositorioAlumnos:
    """Única responsabilidad: guardar y cargar alumnos de disco."""

    def guardar(self, alumno, ruta):
        """Escribe el alumno en un archivo de texto."""
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(f"{alumno.nombre()}: {alumno.notas()}")


class NotificadorEmail:
    """Única responsabilidad: enviar mensajes por email."""

    def enviar_boletin(self, alumno, email):
        """Simula el envío del boletín al alumno."""
        print(
            f"[EMAIL a {email}] {alumno.nombre()}, "
            f"promedio {alumno.promedio():.2f}"
        )
```

Ahora, si cambia el formato de archivo tocás `RepositorioAlumnos` y nada más.
Si cambia el SMTP, tocás `NotificadorEmail`. `Alumno` queda intacta.

---

## OCP: Abierto a extensión, cerrado a modificación

> **Principio:** el software debe estar abierto a la extensión, pero cerrado a
> la modificación.

**Traducción:** cuando aparece un requerimiento nuevo, deberías poder
cumplirlo agregando código nuevo, sin tocar el código que ya funciona.

Suena raro al principio. ¿Cómo agrego funcionalidad sin modificar nada? La
respuesta es polimorfismo y herencia: si diseñaste bien la abstracción base,
cada tipo nuevo se agrega como una subclase y el código que usa la
abstracción no se entera.

**Contraejemplo.** Un sistema de cálculo de sueldos:

```python
def calcular_sueldo(empleado):
    if empleado.tipo == "mensual":
        return empleado.sueldo_fijo
    elif empleado.tipo == "por_hora":
        return empleado.tarifa * empleado.horas
    elif empleado.tipo == "comision":
        return empleado.base + empleado.ventas * empleado.porcentaje / 100
    else:
        return 0
```

Ahora aparece un tipo nuevo: pasante. Para agregarlo hay que abrir este
archivo, agregar un `elif` y esperar no romper los otros casos. Y si tenés
cinco funciones parecidas (`calcular_aguinaldo`, `imprimir_recibo`,
`enviar_notificacion`), hay que modificar las cinco. Ese es el olor: **cada
tipo nuevo obliga a tocar código existente**.

Con polimorfismo queda así:

```python
class Empleado:
    def calcular_sueldo(self):
        raise NotImplementedError


class EmpleadoMensual(Empleado):
    def __init__(self, sueldo_fijo):
        self.sueldo_fijo = sueldo_fijo

    def calcular_sueldo(self):
        return self.sueldo_fijo


class EmpleadoPorHora(Empleado):
    def __init__(self, tarifa, horas):
        self.tarifa = tarifa
        self.horas = horas

    def calcular_sueldo(self):
        return self.tarifa * self.horas
```

La función original desaparece: se reemplaza por `empleado.calcular_sueldo()`,
polimórficamente. Y agregar `Pasante` es:

```python
class Pasante(Empleado):
    def __init__(self, viatico_mensual):
        self.viatico_mensual = viatico_mensual

    def calcular_sueldo(self):
        return self.viatico_mensual
```

Cero modificaciones al código existente. Los cinco lugares que usaban
`empleado.calcular_sueldo()` funcionan automáticamente con el tipo nuevo. Eso
es OCP.

*(Más adelante en este capítulo vamos a ver que ese `raise
NotImplementedError` de la clase base se escribe mejor con `ABC` y
`@abstractmethod`. La idea es la misma; la herramienta, más firme.)*

### OCP en nuestro banco

En la iteración 3 introdujimos `CuentaAhorro` y `CuentaCorriente` como hijas
de `Cuenta`. Todo el resto del sistema —`Banco`, `main.py`, cualquier código
que use `cuenta.depositar()`— funciona idénticamente para las dos, sin saber
cuál es cuál.

En la iteración 5, al final de este capítulo, vamos a agregar `CuentaSueldo`,
un tipo nuevo con reglas propias. Vas a ver que no hay que tocar `Banco`, ni
`Movimiento`, ni las demás cuentas: basta con crear la clase nueva.

> **La regla mental.** Si te encontrás escribiendo `if isinstance(x, ...)` o
> `if x.tipo == "..."` seguido de ramas por tipo, preguntate si eso no debería
> ser un método polimórfico. Nueve de cada diez veces, sí.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 2** — El siguiente código viola OCP. Reescribilo usando herencia
> y polimorfismo, y después agregá `Triangulo` sin tocar nada de lo anterior.

```python
def area_figura(figura):
    if figura.tipo == "circulo":
        return 3.14 * figura.radio ** 2
    elif figura.tipo == "cuadrado":
        return figura.lado ** 2
    elif figura.tipo == "rectangulo":
        return figura.base * figura.altura
    else:
        return 0
```

**Solución.**

```python
import math
from abc import ABC, abstractmethod


class Figura(ABC):
    """Figura cuyo cálculo de área implementa cada hija."""

    @abstractmethod
    def area(self):
        """Superficie encerrada por la figura."""


class Circulo(Figura):
    def __init__(self, radio):
        self._radio = radio

    def area(self):
        return math.pi * self._radio ** 2


class Cuadrado(Figura):
    def __init__(self, lado):
        self._lado = lado

    def area(self):
        return self._lado ** 2


class Rectangulo(Figura):
    def __init__(self, base, altura):
        self._base = base
        self._altura = altura

    def area(self):
        return self._base * self._altura


class Triangulo(Figura):
    """Figura agregada después: ninguna clase anterior cambió."""

    def __init__(self, base, altura):
        self._base = base
        self._altura = altura

    def area(self):
        return self._base * self._altura / 2
```

---

## LSP: Sustitución de Liskov

> **Principio:** si `S` es subclase de `T`, entonces los objetos de tipo `T`
> deberían poder reemplazarse por objetos de tipo `S` sin romper el programa.

**Traducción:** una subclase tiene que cumplir el "contrato" que promete su
clase padre. Si el padre dice "este método devuelve un número positivo", la
hija no puede devolver negativos. Si el padre dice "este método no lanza
excepciones", la hija no puede empezar a tirarlas. Si le pasás una hija donde
se esperaba una instancia del padre, todo tiene que seguir funcionando.

El principio lleva el nombre de **Barbara Liskov**, científica de la
computación estadounidense que ganó el Premio Turing en 2008. Lo formuló en
1988, en un trabajo donde definía cuándo una subclase es realmente un
*subtipo* válido.

### La conexión con teoría de conjuntos

Recordá el paralelo que trazamos en capítulos anteriores: una subclase es un
subconjunto.

```
Si S ⊆ T, entonces:   x ∈ S  ⟹  x ∈ T
```

Todo elemento de `S` también es elemento de `T`. Y toda propiedad `P` que se
cumple para los elementos de `T` tiene que seguir cumpliéndose para los de
`S`:

```
∀x ∈ T : P(x)     ⟹     ∀x ∈ S : P(x)
```

Si existe algún `x ∈ S` que no cumple `P`, entonces `S` no es subconjunto de
`T` en el sentido que nos importa: el elemento no pertenece de verdad a la
categoría.

LSP lleva esa idea al código. Una `CuentaAhorro` es una `Cuenta`, por lo tanto
todo lo que un cliente espera de una `Cuenta` —que pueda depositar, extraer,
consultar saldo, respetar las reglas de saldo— tiene que valer también para
una `CuentaAhorro`. Si la subclase rompe alguna de esas promesas, ya no es un
subtipo válido.

### Contraejemplo: cuadrado y rectángulo

Este es el ejemplo más famoso de violación de LSP, y es el que dejamos
pendiente en el capítulo 11. Parece intuitivo y sin embargo es incorrecto:

```python
class Rectangulo:
    def __init__(self, base, altura):
        self._base = base
        self._altura = altura

    def cambiar_base(self, base):
        self._base = base

    def cambiar_altura(self, altura):
        self._altura = altura

    def area(self):
        return self._base * self._altura


class Cuadrado(Rectangulo):
    """Un cuadrado es un rectángulo con base = altura."""

    def __init__(self, lado):
        super().__init__(lado, lado)

    def cambiar_base(self, base):
        self._base = base
        self._altura = base        # "sincronizamos" los dos lados

    def cambiar_altura(self, altura):
        self._base = altura
        self._altura = altura
```

Parece razonable. Pero mirá qué pasa cuando alguien usa un `Cuadrado`
esperando un `Rectangulo`:

```python
def probar(rectangulo):
    rectangulo.cambiar_base(5)
    rectangulo.cambiar_altura(3)
    assert rectangulo.area() == 15


probar(Rectangulo(1, 1))     # OK
probar(Cuadrado(1))          # AssertionError: el área es 9
```

Con un `Rectangulo`, la promesa "el área es base por altura después de setear
las dos" se cumple. Con un `Cuadrado` no, porque `cambiar_altura` también toca
la base. La sustitución rompe el programa.

> **La lección.** En matemática un cuadrado es un rectángulo. En programación
> no siempre: depende del contrato que el padre haya prometido. Si
> `Rectangulo` promete que base y altura son independientes, `Cuadrado` no
> puede ser una subclase válida. Hay que modelarlos como **hermanas**: una
> `Figura` abstracta con `Rectangulo` y `Cuadrado` como hijas por separado.

Fijate el detalle importante: en el capítulo 11 la jerarquía `Cuadrado`
`(Rectangulo)` **no** violaba LSP, porque ahí `Rectangulo` no tenía setters.
El contrato era solo "sé calcular mi área", y `Cuadrado` lo cumplía perfecto.
Lo que rompió la herencia fue **agregarle setters al padre**. La moraleja es
que LSP no se evalúa mirando la jerarquía sola, sino la jerarquía junto con
las promesas que hace.

### Otro ejemplo: el pájaro y el pingüino

Si tenés una clase `Ave` con método `volar()` y hacés `Pinguino(Ave)`, ¿qué
pasa con `volar()`? El pingüino no vuela. Podés:

- Sobrescribir con `raise NotImplementedError("Los pingüinos no vuelan")`.
  Pero eso rompe LSP: cualquier código que reciba un `Ave` y llame
  `ave.volar()` va a explotar con pingüinos.
- Modelar mejor la jerarquía: `Ave` no debería tener `volar()` en primer
  lugar. Poné `volar()` en una clase `AveVoladora(Ave)` y que `Pinguino`
  herede solo de `Ave`.

> **La lección.** Cuando estés diseñando la clase base, pensá qué promesas
> hace. Si alguna de esas promesas no va a poder cumplirse en todas las
> subclases, la clase base está mal factorizada.

### Cómo detectar violaciones de LSP

- Una subclase sobrescribe un método y lanza excepciones que el padre no
  lanzaba.
- Una subclase sobrescribe un método y devuelve un tipo distinto que el padre.
- Una subclase agrega **precondiciones más estrictas**: el padre acepta
  cualquier número y la hija solo positivos.
- Una subclase ofrece **postcondiciones más débiles**: el padre garantiza algo
  y la hija no.
- El código que usa la clase base tiene que preguntar `isinstance` para
  trabajar bien.

Notá la asimetría, que es la parte fina del principio: **debilitar
precondiciones está permitido** (aceptar más casos que el padre) y
**fortalecer postcondiciones también** (garantizar más). Lo prohibido es al
revés: pedir más y garantizar menos.

### LSP en nuestro banco

Nuestras clases pasan la prueba. `CuentaAhorro` y `CuentaCorriente` respetan
el contrato de `Cuenta`: todas exponen `depositar()`, `extraer()` y `saldo`;
ninguna sorprende con excepciones inesperadas, usan las mismas que ya usaba el
padre; y `Banco` puede trabajar sobre cualquier tipo de cuenta
indistintamente.

`CuentaCorriente.extraer` es el caso interesante: hace algo distinto que
`Cuenta.extraer`, porque permite ir en rojo. ¿Viola LSP? **No**, y es
exactamente el caso de la precondición más débil. El contrato del padre es
"extrae si el monto está permitido, si no lanza `SaldoInsuficienteError`". La
corriente extiende qué significa "permitido" con el límite de descubierto:
acepta **más** casos, pero rechaza los inválidos con la misma excepción. Todo
código que usaba `cuenta.extraer(monto)` sigue funcionando.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 3** — ¿Esta jerarquía viola LSP? Justificá y reorganizala si
> hace falta.

```python
class ArchivoLectura:
    def leer(self):
        return "contenido"


class ArchivoEscritura(ArchivoLectura):
    def leer(self):
        raise PermissionError("Este archivo es solo de escritura")

    def escribir(self, contenido):
        pass
```

**Solución.** Sí, viola LSP. `ArchivoLectura` promete que `leer()` devuelve un
string; `ArchivoEscritura`, como subclase, debería cumplir esa promesa, pero
lanza `PermissionError`. Cualquier código que reciba un `ArchivoLectura` y
llame `.leer()` falla si le pasan un `ArchivoEscritura`.

La solución es reorganizar la jerarquía con una base neutra:

```python
class Archivo:
    """Base neutra: no promete ni lectura ni escritura."""

    def __init__(self, ruta):
        self._ruta = ruta

    def ruta(self):
        """Devuelve la ruta del archivo."""
        return self._ruta


class ArchivoLectura(Archivo):
    def leer(self):
        """Devuelve el contenido del archivo."""
        return f"contenido de {self._ruta}"


class ArchivoEscritura(Archivo):
    def escribir(self, contenido):
        """Guarda el contenido en el archivo."""
        print(f"Escribiendo en {self._ruta}: {contenido}")
```

Ahora ninguna promete algo que la otra no pueda cumplir.

---

## ISP: Segregación de Interfaces

> **Principio:** un cliente no debería estar obligado a depender de métodos
> que no usa.

**Traducción:** es mejor tener varias interfaces chicas y específicas que una
gigante con todo adentro.

En lenguajes con `interface` explícita (Java, C#) el principio se aplica
creando interfaces separadas. En Python, donde las interfaces son implícitas,
ISP se traduce en: **no obligues a una clase a implementar métodos que no le
corresponden**.

**Contraejemplo.**

```python
class MaquinaMultifuncion:
    def imprimir(self, doc): ...
    def escanear(self, doc): ...
    def enviar_fax(self, doc): ...


class ImpresoraSimple(MaquinaMultifuncion):
    def imprimir(self, doc): ...

    def escanear(self, doc):
        raise NotImplementedError      # no puede

    def enviar_fax(self, doc):
        raise NotImplementedError      # tampoco
```

`ImpresoraSimple` está obligada a "implementar" métodos que no puede realizar.
Es una violación de ISP y, de paso, también de LSP: rompe el contrato con un
`raise` que el padre no lanzaba.

**La solución:** partir la interfaz gigante en interfaces chicas.

```python
from abc import ABC, abstractmethod


class Impresora(ABC):
    @abstractmethod
    def imprimir(self, doc):
        """Imprime el documento en papel."""


class Escaner(ABC):
    @abstractmethod
    def escanear(self, doc):
        """Digitaliza el documento."""


class Fax(ABC):
    @abstractmethod
    def enviar_fax(self, doc):
        """Envía el documento por fax."""


class ImpresoraSimple(Impresora):
    def imprimir(self, doc): ...


class MultifuncionVieja(Impresora, Escaner, Fax):
    def imprimir(self, doc): ...
    def escanear(self, doc): ...
    def enviar_fax(self, doc): ...
```

Cada clase implementa solo lo que puede hacer. Nada de métodos vacíos ni
`NotImplementedError` en cosas que no le corresponden.

> **Un momento: ¿no habíamos dicho que no usábamos herencia múltiple?**
> Sí, y sigue en pie. En los capítulos 11 y 12 la desaconsejamos porque
> heredar **estado y comportamiento** de dos padres a la vez trae el problema
> del diamante: si los dos definen el mismo método con implementaciones
> distintas, hay que resolver cuál gana.
>
> Este caso es la excepción, y es la única que usa el manual:
> `Impresora`, `Escaner` y `Fax` son **ABCs puras**. No tienen `__init__`, no
> tienen atributos, no tienen implementación: son solo contratos. Heredar de
> tres contratos no es heredar comportamiento, es **declarar que cumplís
> tres interfaces**. Es exactamente lo que en Java se escribe
> `implements Impresora, Escaner, Fax`, y no hay diamante que resolver porque
> no hay nada que resolver.
>
> La regla queda así: **herencia múltiple solo entre ABCs sin estado.** Si
> alguna de las bases tiene atributos o métodos concretos, volvé a composición.

### ISP en nuestro banco

`Cuenta` es una interfaz coherente: todos los tipos de cuenta necesitan
`depositar`, `extraer` y `saldo`. Ningún método está "de más" para las hijas.

Si apareciera un requerimiento como "algunas cuentas también acreditan
intereses", la solución **no** sería agregar `acreditar_intereses` a `Cuenta`
con el cuerpo vacío. Sería que `CuentaAhorro` implemente ese método por su
cuenta, sin obligar a `CuentaCorriente` a fingir que puede. Que es
exactamente lo que hicimos en la iteración 3.

### Cuándo aplicar ISP en Python

- Si tu clase base define métodos que la mitad de las hijas no usa, la clase
  base está mal.
- Si una clase hija tiene métodos con solo `pass` o `raise
  NotImplementedError`, algo está mal.
- Es mejor tener tres bases chicas (`Legible`, `Escribible`, `Serializable`)
  que una `EntidadCompleta` que promete todo.

Este principio es más importante en lenguajes que exigen implementar toda la
interfaz. En Python, con duck typing, cada vez que necesitás "solo el método
X" alcanza con que el objeto tenga X. Más adelante en este capítulo vamos a
ver `typing.Protocol`, que es la forma de decirle eso al verificador de tipos
sin obligar a nadie a heredar de nada.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 4** — Una interfaz `MaquinaMultifuncion` obliga a implementar
> `imprimir()`, `escanear()` y `enviar_fax()`. `ImpresoraSimple` solo puede
> imprimir, así que lanza `NotImplementedError` en los otros dos. Partí la
> interfaz para que cada clase implemente solo lo que cumple, y escribí una
> función `imprimir_todo(equipos, documento)` que funcione con las dos.

*(La solución es el código de la sección anterior, más:)*

```python
def imprimir_todo(equipos, documento):
    """Solo pide imprimir(): no le importa qué más sabe el equipo."""
    for equipo in equipos:
        equipo.imprimir(documento)


imprimir_todo([ImpresoraSimple(), MultifuncionVieja()], "informe.pdf")
```

`imprimir_todo` depende de la interfaz más chica que le alcanza. Ese es el
punto de ISP.

---

## DIP: Inversión de Dependencias

> **Principio:** dependé de abstracciones, no de implementaciones concretas.

Este es el principio más abstracto y también el que más impacto tiene en
sistemas grandes.

Imaginate que nuestro `Banco` necesita guardar las cuentas en algún lado
permanente: un archivo, una base de datos, un servicio remoto. La primera
reacción sería:

```python
import sqlite3


class Banco:
    def __init__(self):
        self._db = sqlite3.connect("banco.db")

    def guardar_cuenta(self, cuenta):
        ...     # SQL directo
```

Ahora `Banco` depende directamente de SQLite. ¿Qué pasa cuando el proyecto
crece y quieren migrar a PostgreSQL? Hay que reescribir `Banco`. ¿Qué pasa si
en las pruebas queremos usar una base en memoria sin tocar disco? Otra vez,
reescribir `Banco`.

La dependencia va en la dirección equivocada: la clase importante (`Banco`,
con la lógica de negocio) depende de un detalle técnico (la biblioteca de
persistencia).

### La inversión

DIP dice: dá vuelta la dependencia. En vez de que `Banco` conozca a `sqlite3`,
definí una abstracción de "algo que sabe guardar cuentas" y hacé que `Banco`
dependa de esa abstracción.

```python
from abc import ABC, abstractmethod


class RepositorioCuentas(ABC):
    """Abstracción: cualquier cosa que sepa guardar y recuperar cuentas."""

    @abstractmethod
    def guardar(self, cuenta):
        """Persiste la cuenta."""

    @abstractmethod
    def obtener(self, numero):
        """Devuelve la cuenta o None si no está."""


class RepositorioEnMemoria(RepositorioCuentas):
    def __init__(self):
        self._datos = {}

    def guardar(self, cuenta):
        self._datos[cuenta.numero] = cuenta

    def obtener(self, numero):
        return self._datos.get(numero)


class RepositorioSQLite(RepositorioCuentas):
    def __init__(self, archivo):
        import sqlite3
        self._db = sqlite3.connect(archivo)

    def guardar(self, cuenta): ...
    def obtener(self, numero): ...


class Banco:
    def __init__(self, repositorio):
        self._repositorio = repositorio
```

Fijate lo que cambió:

- `Banco` no importa `sqlite3`. No sabe nada de bases de datos.
- `Banco` recibe el repositorio como parámetro en el constructor. Esa técnica
  se llama **inyección de dependencias**.
- Para probar `Banco`, usás `RepositorioEnMemoria`. Para producción,
  `RepositorioSQLite`. Para migrar a PostgreSQL, escribís
  `RepositorioPostgreSQL` sin tocar `Banco`.

**La intuición: depender del qué, no del cómo.** `Banco` no depende de
"SQLite" (el cómo), depende de "algo que sepa guardar cuentas" (el qué). Esa
abstracción es un contrato, no una implementación. Y quién decide la
implementación concreta es quien construye el `Banco`, no la clase misma.

Este patrón es la razón por la que las aplicaciones grandes se pueden probar,
migrar y extender. Django lo usa masivamente: los modelos no saben si están
guardados en SQLite, PostgreSQL o MySQL. Vos configurás el backend y Django
hace el resto. Eso es DIP a escala.

![Comparación en dos paneles. ANTES: la clase Banco tiene una flecha "importa
y usa directo" que apunta a sqlite3, una biblioteca concreta; cambiar de motor
obliga a reescribir Banco. DESPUÉS: Banco tiene una flecha "depende de" que
apunta a RepositorioCuentas, un contrato abstracto (ABC); y RepositorioMemoria
y RepositorioSQLite apuntan hacia arriba a ese mismo contrato con flechas
"implementa". Banco no conoce ninguna implementación: ambos lados dependen de
la abstracción, y quien arma el Banco elige qué repositorio
inyectarle.](images/dip-inversion-dependencias.png)

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 5** — Hacé que `Banco` deje de depender de una implementación
> concreta de almacenamiento. Definí `RepositorioCuentas` como abstracción,
> una implementación en memoria y un doble de prueba que solo cuente llamadas.
> `Banco` debe recibir el repositorio por constructor.

```python
class RepositorioFalso(RepositorioCuentas):
    """Doble de prueba: no guarda nada, cuenta las llamadas."""

    def __init__(self):
        self.llamadas_guardar = 0

    def guardar(self, numero, cuenta):
        self.llamadas_guardar += 1

    def obtener(self, numero):
        return None


falso = RepositorioFalso()
Banco(falso).abrir_cuenta("001-101", 5000)

assert falso.llamadas_guardar == 1
```

Poder escribir ese `assert` sin base de datos, sin disco y sin red es
exactamente lo que DIP compra. En el archivo de ejercicios está la versión
completa.

---

## Formalizando las abstractas: `ABC` y `@abstractmethod`

Veníamos usando métodos abstractos con un truco: `raise NotImplementedError`.
Funciona, pero tiene un problema que ya señalamos en el capítulo 11: Python te
deja instanciar la clase base igual, y el error solo aparece cuando alguien
llama al método, quizás mucho después y en otro archivo.

Python tiene una forma oficial de declarar clases abstractas: el módulo `abc`
(*Abstract Base Classes*). Con él, la clase base no se puede instanciar y las
hijas están obligadas a implementar los métodos abstractos.

### Sintaxis

```python
from abc import ABC, abstractmethod


class Figura(ABC):
    """Clase abstracta: no se puede instanciar."""

    @abstractmethod
    def area(self):
        """Cada hija debe calcular su propia área."""
```

Dos cosas nuevas:

- **`ABC`** (por *Abstract Base Class*): al heredar de esta clase, Python sabe
  que la clase es abstracta.
- **`@abstractmethod`**: marca un método como abstracto. Las hijas están
  obligadas a implementarlo o tampoco podrán instanciarse.

Notá que el cuerpo del método abstracto es solo el docstring. No hace falta
`pass`: el docstring ya es una sentencia válida, y además documenta el
contrato, que es justo lo que un método abstracto tiene para ofrecer.

Uso:

```python
class Circulo(Figura):
    def __init__(self, radio):
        self._radio = radio

    def area(self):
        return 3.1416 * self._radio ** 2


print(Circulo(5).area())     # OK

Figura()   # TypeError: Can't instantiate abstract class Figura
           # with abstract method area
```

Ahí está la diferencia con `NotImplementedError`: antes `Figura()` te dejaba
crear la instancia y el error llegaba tarde. Ahora Python bloquea la
instanciación misma. Es una protección real, y en el momento correcto.

Si una hija se olvida de implementar el método abstracto, también se bloquea:

```python
class TrianguloIncompleto(Figura):
    pass       # ¡no implementó area()!


TrianguloIncompleto()    # TypeError: Can't instantiate abstract class
```

> **Error típico: `@abstractmethod` sin `ABC`.**
> El decorador solo no hace nada. Si escribís:
>
> ```python
> class Figura:                      # ← falta heredar de ABC
>     @abstractmethod
>     def area(self):
>         """..."""
> ```
>
> Python **no protesta** y `Figura()` se instancia sin problemas. El decorador
> marca el método, pero es la metaclase que trae `ABC` la que revisa esas
> marcas al construir el objeto. Sin `ABC`, nadie revisa nada. Es el error
> número uno con este módulo y no da ningún mensaje: simplemente la protección
> que creías tener no existe.

### Varios métodos abstractos

Una clase abstracta puede tener varios métodos abstractos y también métodos
concretos con implementación normal:

```python
class Empleado(ABC):
    def __init__(self, nombre):
        self._nombre = nombre           # implementación normal

    @abstractmethod
    def calcular_sueldo(self):
        """Sueldo del período, en pesos."""

    @abstractmethod
    def descripcion_del_puesto(self):
        """Descripción legible del puesto."""

    def presentarse(self):
        """Método concreto que usa los abstractos."""
        print(f"Soy {self._nombre}, {self.descripcion_del_puesto()}")
```

Las hijas deben implementar `calcular_sueldo` y `descripcion_del_puesto`;
`presentarse` se hereda tal cual. Ese patrón —el padre define el esqueleto y
las hijas completan las piezas— es el mismo *template method* que usamos en
el capítulo 12 con `puede_extraer`, ahora con la garantía de que ninguna hija
puede olvidarse de completar su parte.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 6** — Convertí `Instrumento`, con los métodos `tocar()` y
> `afinar()`, en una clase abstracta usando `ABC` y `@abstractmethod`. Después
> hacé `Guitarra` y `Piano` como hijas concretas. Verificá que no podés
> instanciar `Instrumento` directamente ni una hija que se olvide de
> implementar algún método.

```python
from abc import ABC, abstractmethod


class Instrumento(ABC):
    """Instrumento abstracto: todo instrumento toca y se afina."""

    def __init__(self, nombre):
        self._nombre = nombre

    @abstractmethod
    def tocar(self):
        """Produce el sonido característico del instrumento."""

    @abstractmethod
    def afinar(self):
        """Ajusta la afinación del instrumento."""


class Guitarra(Instrumento):
    def tocar(self):
        print(f"Rasguido con {self._nombre}")

    def afinar(self):
        print(f"Afinando las cuerdas de {self._nombre}")


class Bateria(Instrumento):
    """Hija incompleta: se olvidó de implementar afinar()."""

    def tocar(self):
        print(f"Redoble en {self._nombre}")


Guitarra("Fender").tocar()

Instrumento("cualquiera")    # TypeError: clase abstracta
Bateria("Ludwig")            # TypeError: falta afinar()
```

---

## Type hints: declarando los tipos esperados

Python es dinámicamente tipado: no declarás qué tipos aceptan los parámetros
ni qué devuelven las funciones. Es cómodo, pero también inseguro: nada avisa
si pasás un string donde esperabas un número, hasta que el programa explota.

Desde Python 3.5 existen los **type hints**: una sintaxis para declarar los
tipos esperados. No cambian el comportamiento del programa —Python los ignora
al ejecutar— pero documentan la intención, ayudan al IDE a autocompletar y
habilitan herramientas de análisis estático.

### Sintaxis básica

Se agregan con `:` después del parámetro y `->` antes del retorno:

```python
def sumar(a: int, b: int) -> int:
    return a + b


def saludar(nombre: str) -> None:
    print(f"Hola, {nombre}")
```

Se leen: "sumar recibe `a` (int) y `b` (int) y devuelve un int"; "saludar
recibe `nombre` (str) y no devuelve nada".

### En clases

Los atributos también pueden llevar anotación:

```python
class Cuenta:
    def __init__(self, titular: str, saldo: float = 0) -> None:
        self._titular: str = titular
        self._saldo: float = saldo

    @property
    def saldo(self) -> float:
        return self._saldo

    def depositar(self, monto: float) -> None:
        self._saldo += monto

    def es_vip(self) -> bool:
        return self._saldo > 1_000_000
```

### Tipos compuestos

Para listas, diccionarios y otros contenedores se usa la sintaxis genérica:

```python
def promedio(numeros: list[float]) -> float:
    return sum(numeros) / len(numeros)


def contar_palabras(texto: str) -> dict[str, int]:
    ...
```

`list[float]` significa "lista de floats"; `dict[str, int]`, "diccionario con
claves string y valores int".

> **Ojo con la versión de Python.** Los type hints existen desde 3.5, pero
> escribir `list[float]` y `dict[str, int]` con los tipos incorporados
> requiere **Python 3.9 o superior**. En versiones anteriores hay que importar
> `List` y `Dict` de `typing`. Y `str | None` requiere **3.10 o superior**;
> antes se escribe `Optional[str]`. Si el código de un compañero no te corre,
> chequeá la versión antes que nada.

### `Optional` y valores que pueden ser `None`

```python
from typing import Optional


def buscar_si_existe(nombre: str) -> Optional[Persona]:
    ...
```

`Optional[Persona]` significa "una `Persona` o `None`". Y acá vale reconectar
con la convención del capítulo 12: si el método puede devolver `None`, el
nombre debe avisarlo y el hint lo confirma. Si el método se llama `buscar` y
promete lanzar excepción, el hint es `-> Persona` a secas, sin `Optional`. El
tipo y el nombre cuentan la misma historia.

### Los hints no se verifican en tiempo de ejecución

Un punto importante: Python **no revisa los hints al ejecutar**. Si declarás
`def sumar(a: int, b: int) -> int:` y le pasás strings, funciona igual
(mientras la operación `+` sea válida). Los hints son documentación asistida,
no un sistema de tipos estricto.

Si querés verificación real, herramientas como **mypy** o **pyright** analizan
el código sin ejecutarlo y avisan de inconsistencias antes de correrlo.

## `Protocol`: interfaces sin herencia

Cuando vimos ISP dijimos que en Python las interfaces son implícitas: alcanza
con que el objeto tenga el método. Eso es duck typing y funciona perfecto en
tiempo de ejecución. El problema aparece al anotar: ¿qué tipo escribo en una
función que acepta "cualquier cosa que sepa describirse"?

Una opción es hacer una ABC y obligar a todos a heredar de ella. Pero eso
contradice el espíritu del duck typing y no siempre es posible (no podés hacer
que una clase de otra biblioteca herede de la tuya).

La respuesta moderna es `typing.Protocol`, disponible desde **Python 3.8**:

```python
from typing import Protocol


class Describible(Protocol):
    """Cualquier objeto que sepa describirse en una línea."""

    def describir(self) -> str:
        """Devuelve una descripción legible del objeto."""
        ...


def informar(cosas: list[Describible]) -> None:
    for cosa in cosas:
        print(f"  {cosa.describir()}")
```

Ahora `Alumno` y `Materia` pueden cumplir el protocolo **sin heredar de
nada**:

```python
class Alumno:
    def describir(self) -> str:
        return f"Alumno {self._nombre}"


class Materia:
    def describir(self) -> str:
        return f"Materia {self._nombre}"


informar([Alumno(), Materia()])    # mypy lo acepta sin quejarse
```

Esto se llama **tipado estructural**: lo que importa es la forma del objeto
(qué métodos tiene), no su ascendencia. Es duck typing con verificación
estática, que es exactamente lo que ISP pide en Python.

Si además querés usar `isinstance`, agregá el decorador
`@runtime_checkable`:

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Describible(Protocol):
    def describir(self) -> str: ...


isinstance(Alumno(), Describible)     # True
isinstance(Aula(101), Describible)    # False, no tiene describir()
```

> **ABC o Protocol, ¿cuál uso?**
> **ABC** cuando vos controlás la jerarquía y querés obligar: las hijas son
> tuyas y te conviene que Python las bloquee si se olvidan de implementar
> algo. Es el caso de `Cuenta` en el banco.
> **Protocol** cuando querés aceptar objetos que no controlás, o cuando la
> relación no es de familia sino de capacidad: "cualquier cosa que sepa
> exportarse". Es el caso de `Describible` o `Exportable`.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 7** — Declará un protocolo `Exportable` con un método `a_csv()`
> que devuelva una línea de texto. Hacé dos clases sin relación de herencia
> entre sí, `Alumno` y `Materia`, que lo cumplan, y una función
> `exportar(elementos)` tipada con `list[Exportable]`. Verificá con
> `isinstance` usando `@runtime_checkable`.

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Exportable(Protocol):
    """Cualquier objeto que sepa representarse como línea CSV."""

    def a_csv(self) -> str:
        """Devuelve los datos del objeto separados por comas."""
        ...


def exportar(elementos: list[Exportable]) -> str:
    """Arma un CSV con cualquier objeto que sepa exportarse."""
    return "\n".join(elemento.a_csv() for elemento in elementos)
```

La versión completa, con las tres clases y las comprobaciones, está en el
archivo de ejercicios.

---

## Dataclasses: clases-contenedor sin *boilerplate*

Muchas veces necesitás una clase que solo guarda datos. Como nuestro
`Movimiento`: tipo, monto, saldo resultante. Sin lógica compleja, solo un
contenedor. La versión manual tenía un `__init__`, accesores y `__str__`: un
montón de líneas para algo que es esencialmente "una tupla con nombre".

Desde Python 3.7 existen los **dataclasses**: un decorador que genera
automáticamente el `__init__`, el `__repr__` y otros métodos a partir de la
lista de atributos anotados.

### Sintaxis básica

```python
from dataclasses import dataclass


@dataclass
class Punto:
    x: float
    y: float
```

Con solo eso, Python genera:

- `__init__(self, x, y)`, que asigna los dos atributos.
- `__repr__`, que muestra `Punto(x=3, y=5)`.
- `__eq__`, que compara dos puntos como iguales si tienen los mismos valores.

```python
p1 = Punto(3, 5)
print(p1)          # Punto(x=3, y=5)
print(p1.x)        # 3

p2 = Punto(3, 5)
p1 == p2           # True. Esto no vendría gratis con una clase normal
```

Sin `dataclass` habría que escribir el `__init__`, el `__repr__` y el `__eq__`
a mano: unas quince líneas para el mismo resultado.

Notá que las anotaciones de tipo **no son opcionales acá**: `dataclass` mira
las anotaciones del cuerpo de la clase para saber qué campos generar. Un
atributo sin anotación no se convierte en campo.

### Valores por defecto y orden de los campos

```python
@dataclass
class Configuracion:
    host: str = "localhost"
    puerto: int = 8080
    debug: bool = False


c1 = Configuracion()                            # todos los defaults
c2 = Configuracion(host="servidor.com")         # cambia solo host
c3 = Configuracion("192.168.1.1", 9000, True)   # todos explícitos
```

> **Trampa 1: el orden importa.** Los campos con valor por defecto tienen que
> ir **después** de los que no lo tienen, igual que en cualquier función. Si
> escribís esto:
>
> ```python
> @dataclass
> class Alumno:
>     activo: bool = True
>     nombre: str          # ← sin default, después de uno con default
> ```
>
> Python falla al definir la clase con
> `TypeError: non-default argument 'nombre' follows default argument`.

> **Trampa 2: nunca uses una lista o un dict como valor por defecto.**
>
> ```python
> @dataclass
> class Ruta:
>     nombre: str
>     paradas: list = []      # ValueError al definir la clase
> ```
>
> Ese default sería **un solo objeto lista compartido por todas las
> instancias**: es el mismo problema de referencias compartidas del capítulo
> 12. `dataclass` es lo bastante amable como para rechazarlo con un
> `ValueError` explícito en vez de dejarte el bug. La forma correcta es
> `field(default_factory=...)`, que llama a la fábrica una vez por instancia:
>
> ```python
> from dataclasses import dataclass, field
>
> @dataclass
> class Ruta:
>     nombre: str
>     paradas: list[str] = field(default_factory=list)
> ```

### Solo lectura: `frozen=True`

Si querés que la dataclass sea inmutable, como una tupla:

```python
@dataclass(frozen=True)
class Coordenada:
    latitud: float
    longitud: float


c = Coordenada(-34.9, -58.4)
c.latitud = 0     # FrozenInstanceError
```

Muy útil para valores que no cambian: coordenadas, colores, un movimiento
bancario ya registrado.

### Igualdad y hash

Hay un detalle que sorprende. Por defecto `@dataclass` genera `__eq__`, y
**cuando una clase define `__eq__`, Python le pone `__hash__ = None`**. O sea:
tu dataclass compara bien por valor pero **no se puede usar como clave de un
diccionario ni meter en un `set`**.

```python
@dataclass
class Producto:
    codigo: str
    nombre: str


{Producto("P-1", "Yerba"): 20}    # TypeError: unhashable type
```

Tenés dos salidas:

- `@dataclass(frozen=True)`: si es inmutable, Python genera el `__hash__`
  automáticamente. Es la opción preferida.
- `@dataclass(unsafe_hash=True)`: genera el `__hash__` aunque la clase sea
  mutable. Se llama *unsafe* porque si mutás un campo que participa del hash
  mientras el objeto está en un diccionario, lo perdés. Es seguro cuando los
  campos que definen la identidad no cambian nunca.

Y si querés que la igualdad dependa de un solo campo (por ejemplo, dos
productos son el mismo si comparten código), no escribas `__eq__` a mano:
usá `field(compare=False)` en los demás.

```python
from dataclasses import dataclass, field


@dataclass(unsafe_hash=True)
class Producto:
    codigo: str
    nombre: str = field(compare=False)
    precio: float = field(compare=False)
```

### Cuándo usar dataclass y cuándo no

**Usala** cuando la clase es esencialmente un contenedor de datos, no tiene
lógica compleja y querés comparación por valor y buena representación textual.

**No la uses** cuando tenés mucha lógica de negocio o validaciones complejas,
cuando la clase tiene métodos que operan sobre su estado (ahí una clase normal
se lee mejor), o cuando necesitás properties con setters elaborados.

`Movimiento` es un candidato perfecto, y así lo vamos a rehacer en la
iteración 5. `Cuenta` no: tiene demasiada lógica.

---

<img src="images/ejercicio-icono.jpeg" alt="Ícono de ejercicio" width="55" align="right">

> **EJERCICIO 8** — Escribí `Punto` como `@dataclass` con `x` e `y`, y
> `Poligono` como dataclass con nombre y una lista de vértices usando
> `field(default_factory=list)`. Verificá con `assert` que dos puntos con los
> mismos valores son iguales y que dos polígonos recién creados no comparten
> la misma lista.

```python
from dataclasses import dataclass, field


@dataclass
class Punto:
    x: float
    y: float


@dataclass
class Poligono:
    nombre: str
    vertices: list[Punto] = field(default_factory=list)


uno, otro = Punto(3, 5), Punto(3, 5)
assert uno == otro, "dataclass debería comparar por valor"
assert uno is not otro, "son dos objetos distintos"

triangulo, cuadrado = Poligono("triángulo"), Poligono("cuadrado")
assert triangulo.vertices is not cuadrado.vertices
```

---

## Sembrando testing con `assert`

Cerramos la teoría con una anticipación. El año que viene, con Django, van a
aprender *testing* formalmente: la práctica de escribir código que verifica
que otro código hace lo que promete. Es una parte central del desarrollo
profesional moderno.

Todavía no estamos ahí, pero Python tiene una instrucción que sirve para
verificar cosas simples: `assert`.

```python
assert condicion, "mensaje si falla"
```

`assert` chequea que la condición sea verdadera. Si lo es, no pasa nada. Si es
falsa, lanza `AssertionError` con el mensaje.

```python
def calcular_promedio(numeros):
    return sum(numeros) / len(numeros)


resultado = calcular_promedio([10, 20, 30])
assert resultado == 20, f"Promedio incorrecto: {resultado}"
```

### Uso didáctico: verificar los principios

En este capítulo `assert` nos sirve para comprobar que el diseño funciona como
esperamos. Con LSP, por ejemplo:

```python
def verificar_contrato(cuenta):
    """LSP: toda subclase de Cuenta debe cumplir lo que el padre promete."""
    previo = cuenta.saldo
    cuenta.depositar(100)

    assert cuenta.saldo == previo + 100, (
        f"{type(cuenta).__name__} no acreditó el depósito"
    )


for cuenta in [CuentaAhorro(...), CuentaCorriente(...), CuentaSueldo(...)]:
    verificar_contrato(cuenta)

print("Todas las cuentas respetan el contrato de depósito")
```

Si alguna subclase rompiera el contrato —si `CuentaSueldo` se quedara con una
comisión del depósito, por ejemplo— el `assert` lo detectaría inmediatamente,
en vez de que el error apareciera meses después en un resumen mal calculado.

### La advertencia que no se puede omitir

> **`assert` desaparece cuando Python corre optimizado.**
> Si ejecutás `python -O programa.py` (o si la variable de entorno
> `PYTHONOPTIMIZE` está activa), el intérprete **elimina todas las sentencias
> `assert`**. No las ignora: no las compila. Es como si no estuvieran.
>
> La consecuencia es directa y hay que tenerla clarísima:
>
> ```python
> def depositar(self, monto):
>     assert monto > 0, "El monto debe ser positivo"    # ← MAL
>     self._saldo += monto
> ```
>
> Esa validación **no existe** en modo optimizado, y un depósito negativo pasa
> sin control. Para reglas de negocio y datos que vienen del usuario va lo que
> venimos haciendo desde el capítulo 10:
>
> ```python
> def depositar(self, monto):
>     if monto <= 0:
>         raise MontoInvalidoError("El monto debe ser positivo")
>     self._saldo += monto
> ```
>
> **Regla:** `assert` para verificar supuestos internos del programador y para
> pruebas. `raise` con una excepción propia para todo lo que sea validación
> real.

Cuando aprendan testing con Django van a ver que los frameworks (`unittest`,
`pytest`) hacen exactamente esta idea: correr código y verificar que las
promesas se cumplen. `assert` es la versión artesanal; los frameworks, la
profesional. La mentalidad es la misma.

## Iteración 5: el cierre del banco

Llegamos al final del proyecto. En esta iteración aplicamos todo lo del
capítulo sobre el sistema que venimos armando desde el capítulo 9. Cuatro
cambios:

1. `Movimiento` pasa a ser una **dataclass frozen**: es un dato inmutable, un
   hecho ya ocurrido.
2. `Cuenta` se vuelve **abstracta con `ABC`** y define el esqueleto de
   `extraer()`, delegando la regla en `puede_extraer()`.
3. Aparece **`CuentaSueldo`**, el tipo nuevo que prometimos al hablar de OCP.
4. `Banco` deja de guardar el diccionario y recibe un **`RepositorioCuentas`
   inyectado**, aplicando DIP.

Todo anotado con type hints.

**`movimientos.py`**

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Movimiento:
    """Registro inmutable de una operación sobre una cuenta."""

    tipo: str
    monto: float
    saldo_resultante: float

    def __str__(self) -> str:
        return (
            f"{self.tipo:<12} ${self.monto:>10,.2f} "
            f"-> ${self.saldo_resultante:,.2f}"
        )
```

**`cuentas.py`**

```python
from abc import ABC, abstractmethod

from errores import MontoInvalidoError, SaldoInsuficienteError
from movimientos import Movimiento


class Cuenta(ABC):
    """Cuenta abstracta: define el esqueleto de las operaciones."""

    def __init__(self, numero: str, titular: str, saldo: float = 0) -> None:
        self._numero = numero
        self._titular = titular
        self._saldo = saldo
        self._movimientos: list[Movimiento] = []

    @property
    def numero(self) -> str:
        """Número identificador de la cuenta."""
        return self._numero

    @property
    def saldo(self) -> float:
        """Saldo actual, de solo lectura."""
        return self._saldo

    @abstractmethod
    def puede_extraer(self, monto: float) -> bool:
        """Regla propia de cada tipo de cuenta."""

    @abstractmethod
    def costo_mantenimiento(self) -> float:
        """Costo mensual que cobra el banco por la cuenta."""

    def depositar(self, monto: float) -> None:
        """Acredita un monto positivo y lo registra."""
        if monto <= 0:
            raise MontoInvalidoError("El monto debe ser positivo")

        self._saldo += monto
        self._registrar("depósito", monto)

    def extraer(self, monto: float) -> None:
        """Debita el monto si la regla de la cuenta lo permite."""
        if monto <= 0:
            raise MontoInvalidoError("El monto debe ser positivo")

        if not self.puede_extraer(monto):
            raise SaldoInsuficienteError(
                f"Extracción rechazada en {self._numero}"
            )

        self._saldo -= monto
        self._registrar("extracción", monto)

    def _registrar(self, tipo: str, monto: float) -> None:
        """Agrega un movimiento al historial."""
        self._movimientos.append(Movimiento(tipo, monto, self._saldo))

    def historial(self) -> list[Movimiento]:
        """Devuelve una copia del historial de movimientos."""
        return list(self._movimientos)


class CuentaAhorro(Cuenta):
    """No admite descubierto y paga mantenimiento."""

    def puede_extraer(self, monto: float) -> bool:
        return monto <= self._saldo

    def costo_mantenimiento(self) -> float:
        return 500


class CuentaCorriente(Cuenta):
    """Admite girar en descubierto hasta un límite."""

    def __init__(
        self,
        numero: str,
        titular: str,
        saldo: float = 0,
        descubierto: float = 50000,
    ) -> None:
        super().__init__(numero, titular, saldo)
        self._descubierto = descubierto

    def puede_extraer(self, monto: float) -> bool:
        return monto <= self._saldo + self._descubierto

    def costo_mantenimiento(self) -> float:
        return 1500


class CuentaSueldo(Cuenta):
    """Tipo nuevo de esta iteración: sin descubierto ni costo."""

    def puede_extraer(self, monto: float) -> bool:
        return monto <= self._saldo

    def costo_mantenimiento(self) -> float:
        return 0
```

**`repositorios.py`**

```python
from abc import ABC, abstractmethod
from typing import Optional

from cuentas import Cuenta


class RepositorioCuentas(ABC):
    """Abstracción: algo que sabe guardar y recuperar cuentas."""

    @abstractmethod
    def guardar(self, cuenta: Cuenta) -> None:
        """Persiste la cuenta."""

    @abstractmethod
    def obtener(self, numero: str) -> Optional[Cuenta]:
        """Devuelve la cuenta o None si no está."""

    @abstractmethod
    def todas(self) -> list[Cuenta]:
        """Devuelve todas las cuentas guardadas."""


class RepositorioMemoria(RepositorioCuentas):
    """Implementación en memoria: la que usamos por ahora."""

    def __init__(self) -> None:
        self._cuentas: dict[str, Cuenta] = {}

    def guardar(self, cuenta: Cuenta) -> None:
        self._cuentas[cuenta.numero] = cuenta

    def obtener(self, numero: str) -> Optional[Cuenta]:
        return self._cuentas.get(numero)

    def todas(self) -> list[Cuenta]:
        return list(self._cuentas.values())
```

**`banco.py`**

```python
from cuentas import Cuenta
from errores import CuentaNoEncontrada, NumeroDuplicadoError
from repositorios import RepositorioCuentas


class Banco:
    """ABM de cuentas. No sabe dónde ni cómo se guardan."""

    def __init__(self, nombre: str, repositorio: RepositorioCuentas) -> None:
        self._nombre = nombre
        self._repositorio = repositorio

    def abrir_cuenta(self, cuenta: Cuenta) -> Cuenta:
        """Registra una cuenta ya construida."""
        if self._repositorio.obtener(cuenta.numero) is not None:
            raise NumeroDuplicadoError(f"La cuenta {cuenta.numero} ya existe")

        self._repositorio.guardar(cuenta)

        return cuenta

    def buscar(self, numero: str) -> Cuenta:
        """Devuelve la cuenta pedida o lanza excepción."""
        cuenta = self._repositorio.obtener(numero)

        if cuenta is None:
            raise CuentaNoEncontrada(f"No existe la cuenta {numero}")

        return cuenta

    def listar(self) -> list[Cuenta]:
        """Devuelve todas las cuentas del banco."""
        return self._repositorio.todas()

    def total_depositado(self) -> float:
        """Suma los saldos de todas las cuentas."""
        return sum(cuenta.saldo for cuenta in self.listar())
```

### Los cinco principios, en un sistema que funciona

Mirá el sistema terminado y buscá cada principio:

- **SRP**: `Movimiento` registra, `Cuenta` opera sobre su saldo,
  `RepositorioMemoria` guarda, `Banco` gestiona la colección. Cuatro clases,
  cuatro razones para cambiar.
- **OCP**: agregar `CuentaSueldo` no obligó a tocar ni una línea de `Banco`,
  `Movimiento`, `RepositorioCuentas` o las otras cuentas. Solo escribimos una
  clase nueva con sus dos métodos.
- **LSP**: las tres cuentas cumplen el mismo contrato. `depositar(100)` suma
  100 en las tres; `extraer` rechaza con la misma excepción en las tres.
  `CuentaCorriente` acepta más casos (precondición más débil), que es
  legítimo.
- **ISP**: `Cuenta` declara solo lo que toda cuenta puede cumplir. El costo de
  mantenimiento es abstracto porque **todas** lo tienen, aunque en
  `CuentaSueldo` valga cero. Si algún día aparece `acreditar_intereses`, no va
  en la base.
- **DIP**: `Banco` depende de `RepositorioCuentas`, no de un diccionario ni de
  SQLite. El día que quieran persistencia real, escriben
  `RepositorioSQLite(RepositorioCuentas)` y se lo inyectan. Cero cambios en el
  resto del sistema.

![Tabla resumen "SOLID en la iteración 5 del banco" con una fila por principio.
S, Responsabilidad única: Movimiento registra, Cuenta opera su saldo,
RepositorioMemoria guarda, Banco gestiona la colección. O, Abierto/Cerrado:
agregar CuentaSueldo no tocó ninguna otra clase. L, Sustitución de Liskov: las
tres cuentas cumplen el mismo contrato de depositar y extraer. I, Segregación
de interfaces: Cuenta declara solo lo que toda cuenta puede cumplir, sin
métodos vacíos. D, Inversión de dependencias: Banco depende de
RepositorioCuentas, no de un diccionario ni de SQLite. Al pie: un modelo de
Django reúne todo lo de los capítulos 10 a 12 y su ORM es DIP
puro.](images/solid-en-el-banco.png)

Y el cierre, que es lo que van a reconocer el año que viene: cuando abran
Django y escriban su primer modelo, van a estar mirando esta misma
arquitectura. Un modelo es una clase con validaciones (capítulo 10). Hereda de
`models.Model` (capítulo 11). Se relaciona con otros por `ForeignKey`
(capítulo 12). El `Manager` hace el ABM (capítulo 12). Y el ORM es DIP puro:
tu modelo no sabe en qué motor está guardado. No van a estar aprendiendo
conceptos nuevos, van a estar viendo cómo un framework industrial concreta lo
que ustedes ya escribieron a mano.
