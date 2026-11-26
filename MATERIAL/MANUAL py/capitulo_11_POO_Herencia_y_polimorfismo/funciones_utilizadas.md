# Funciones Utilizadas en capitulo_11_POO_Herencia_y_polimorfismo

Documento que agrupa las funciones built-in, los métodos, los módulos,
los tipos de excepción y las construcciones del lenguaje utilizados en
los ejercicios y enunciados, organizados por tipo y en orden
alfabético.

Este capítulo trata la **herencia** y el **polimorfismo**. Igual que
en el capítulo 9, el foco no está en funciones nuevas sino en la
sintaxis del lenguaje: declarar una subclase con `class Hija(Padre)`,
reutilizar el código del padre con `super()`, sobrescribir métodos y
apoyarse en que Python elige la versión correcta según el objeto
(despacho dinámico). Las pocas funciones built-in que aparecen
(`isinstance`, `type`, `sum`) ya se vieron antes; acá se usan al
servicio del polimorfismo.

---

## Funciones Generales

### `isinstance(objeto, clase)`

**¿Qué realiza?**

Verifica si un objeto es una instancia de una clase o de alguna de sus
subclases. En este capítulo se usa para comprobar que una instancia de
una subclase también "es" del tipo del padre, y para mostrar que todo
objeto hereda, en última instancia, de `object`.

En el enunciado sobre descuentos aparece el patrón contrario: un bucle
lleno de `isinstance` que *hay que eliminar* reemplazándolo por
polimorfismo. `isinstance` sirve para preguntar el tipo, pero cuando se
lo usa para decidir qué comportamiento aplicar, casi siempre es señal
de que ese comportamiento debería vivir dentro de cada clase.

**¿Qué retorna?**

Un valor de tipo `bool`.

**Ejemplos típicos:**

```python
class Animal:
    pass

class Perro(Animal):
    pass

pichicho = Perro()

isinstance(pichicho, Perro)    # True
isinstance(pichicho, Animal)   # True: un Perro también es un Animal
isinstance(pichicho, object)   # True: todo hereda de object
```

### `len(colección)`

**¿Qué realiza?**

Retorna la cantidad de elementos de una colección. En el capítulo se
usa sobre la lista de personas a cargo de un `Gerente` para armar el
texto de la presentación.

**¿Qué retorna?**

Un valor de tipo `int`.

**Ejemplos típicos:**

```python
class Gerente(Empleado):

    def __init__(self, nombre, equipo):
        super().__init__(nombre)
        self._equipo = equipo

    def presentarse(self):
        super().presentarse()
        print(f"y dirijo un equipo de {len(self._equipo)} personas")
```

### `print(*objetos, sep=' ', end='\n')`

**¿Qué realiza?**

Escribe uno o varios valores en la salida estándar. Cuando recibe un
objeto de una clase propia usa su `__str__`; si el objeto es de una
subclase, usa el `__str__` que corresponda a esa subclase, aunque el
bucle que llama a `print()` sea el mismo para todos.

**¿Qué retorna?**

`None`.

**Ejemplos típicos:**

```python
for instrumento in banda:
    print(instrumento)          # cada uno imprime su propio __str__

print(f"Error esperado: {error}")
print(f"Gasto total: ${total:.2f}")
```

### `sum(iterable)`

**¿Qué realiza?**

Retorna la suma de los elementos de un iterable numérico. En este
capítulo se combina con una expresión generadora que recorre una lista
**mixta** de objetos y le pide a cada uno un valor (`area()`,
`sueldo()`, `precio_final()`). El código que suma no pregunta de qué
tipo es cada elemento: eso es polimorfismo.

**¿Qué retorna?**

La suma total.

**Ejemplos típicos:**

```python
total = sum(figura.area() for figura in figuras)

total = sum(empleado.sueldo() for empleado in plantilla)

def precio_total(self):
    return sum(
        producto.precio_final()
        for producto in self._productos
    )
```

### `type(objeto)`

**¿Qué realiza?**

Retorna la clase exacta de un objeto. En el capítulo casi no se usa
para comparar tipos, sino para obtener el **nombre** de la clase
concreta con `type(self).__name__`, tanto en el mensaje de un
`NotImplementedError` como en un `__str__` genérico heredado.

**¿Qué retorna?**

Un objeto de tipo `type` (la clase). `type(self).__name__` es un `str`.

**Ejemplos típicos:**

```python
def area(self):
    raise NotImplementedError(
        f"La clase {type(self).__name__} debe implementar area()"
    )

def __str__(self):
    return f"{type(self).__name__}: {self.volumen():.2f}"
```

---

## Métodos de Listas

Los siguientes elementos son métodos de la clase `list`. Se invocan
sobre una lista que es atributo privado de un objeto, por ejemplo,
`self._productos.append(x)`.

### `list.append(elemento)`

**¿Qué realiza?**

Agrega `elemento` al final de la lista, modificándola en el lugar. En
este capítulo la usa una clase contenedora (`Tienda`) para sumar
objetos a su colección interna.

**¿Qué retorna?**

`None`.

**Ejemplos típicos:**

```python
class Tienda:

    def __init__(self, nombre):
        self._nombre = nombre
        self._productos = []

    def agregar(self, producto):
        self._productos.append(producto)
```

---

## Módulo `math`

### `math.pi`

**¿Qué realiza?**

Constante con el valor de π. Requiere `import math`. Se usa en las
fórmulas de volumen de la esfera y el cilindro, dentro del método
`volumen()` que cada subclase implementa a su manera.

**Ejemplos típicos:**

```python
import math


class Esfera(Forma3D):

    def __init__(self, radio):
        self._radio = radio

    def volumen(self):
        return 4 / 3 * math.pi * self._radio ** 3


class Cilindro(Forma3D):

    def volumen(self):
        return math.pi * self._radio ** 2 * self._altura
```

---

## Tipos de Excepción

### `AttributeError`

**¿Cuándo se produce?**

Cuando se llama a un método (o se accede a un atributo) que el objeto
no tiene. En el capítulo aparece al pedirle a una instancia de la
clase **padre** un método que solo definió la **hija**: el método
existe en `Perro`, no en `Animal`, así que `animal_generico.ladrar()`
lanza `AttributeError`.

**Ejemplos típicos:**

```python
class Animal:
    def respirar(self):
        print("Respirando...")

class Perro(Animal):
    def ladrar(self):
        print("¡Guau!")

generico = Animal()

try:
    generico.ladrar()          # Animal no tiene ladrar()
except AttributeError as error:
    print(f"Error esperado: {error}")
```

### `NotImplementedError`

**¿Cuándo se produce?**

Cuando se ejecuta un método pensado como **abstracto conceptual**: el
padre lo define solo para dejar el contrato escrito y hace `raise
NotImplementedError` en el cuerpo. Si una subclase olvida
implementarlo, o si alguien instancia directamente la clase base y
llama al método, salta esta excepción con un mensaje que nombra la
clase culpable.

No bloquea la creación del objeto (eso se ve en el capítulo 13 con
`abc`): el aviso llega recién al llamar al método.

**Ejemplos típicos:**

```python
class Figura:

    def area(self):
        raise NotImplementedError(
            f"La clase {type(self).__name__} debe implementar area()"
        )


class Cuadrado(Figura):

    def __init__(self, lado):
        self._lado = lado

    def area(self):
        return self._lado ** 2


try:
    Figura().area()
except NotImplementedError as error:
    print(f"Error esperado: {error}")
```

---

## Construcciones del Lenguaje

Las siguientes construcciones son el tema central del capítulo: la
sintaxis de Python para heredar de otra clase y para que un mismo
llamado se comporte distinto según el objeto.

### `class Hija(Padre)` — Declarar una subclase

**¿Qué realiza?**

Define una clase que **hereda** de otra: recibe todos sus atributos y
métodos sin reescribirlos. La clase entre paréntesis es la
superclase (padre, clase base); la que se define es la subclase
(hija, clase derivada).

**Sintaxis:**

```python
class Perro(Animal):
    # todo lo de Animal ya está disponible acá
    ...
```

**Ejemplos típicos:**

```python
class Animal:
    def respirar(self):
        print("Respirando...")


class Perro(Animal):
    pass


pichicho = Perro()
pichicho.respirar()      # heredado de Animal, sin escribir nada
```

### La relación "es un"

**¿Qué realiza?**

Es la prueba para decidir si corresponde usar herencia. `Perro` hereda
de `Animal` porque un perro **es un** animal. `Moto` hereda de
`Vehiculo` porque una moto **es un** vehículo. Cuando la frase natural
es "tiene un" (un auto *tiene un* motor), no va herencia sino
composición, que es el tema del capítulo 12.

**Ejemplos típicos:**

```python
class Vehiculo:
    def __init__(self, marca, modelo):
        self._marca = marca
        self._modelo = modelo


class Moto(Vehiculo):        # una Moto ES UN Vehiculo
    def __init__(self, marca, modelo, cilindrada):
        super().__init__(marca, modelo)
        self._cilindrada = cilindrada
```

### `pass` en una subclase que no agrega nada

**¿Qué realiza?**

Cuando una subclase hereda todo y no aporta atributos ni métodos
propios, el cuerpo de la clase igual necesita una instrucción: se
escribe `pass`. La subclase queda funcional gracias a lo que hereda.

**Ejemplos típicos:**

```python
class Perro(Animal):
    pass


class CuentaVIP(Cuenta):
    def comision(self):      # acá sí agrega algo: cambia una regla
        return 0
```

### `super().__init__(...)` — Reutilizar el constructor del padre

**¿Qué realiza?**

Desde el `__init__` de la hija, llama al `__init__` del padre para que
inicialice los atributos comunes. Así la hija no repite las
asignaciones que ya sabe hacer el padre y solo agrega las suyas.

**Sintaxis:**

```python
def __init__(self, <parámetros del padre>, <parámetros nuevos>):
    super().__init__(<parámetros del padre>)
    self._<atributo nuevo> = <parámetro nuevo>
```

**Ejemplos típicos:**

```python
class Gerente(Empleado):

    def __init__(self, nombre, equipo):
        super().__init__(nombre)       # Empleado guarda el nombre
        self._equipo = equipo          # Gerente agrega el equipo
```

```python
class Cuadrado(Rectangulo):

    def __init__(self, lado):
        super().__init__(lado, lado)   # un lado sirve de base y altura
```

### `super().<metodo>()` — Reutilizar un método del padre

**¿Qué realiza?**

`super()` no sirve solo en `__init__`. Dentro de una sobrescritura,
`super().metodo()` ejecuta la versión del padre y la hija le agrega lo
suyo antes, después o en el medio. Evita copiar y pegar el cuerpo del
método del padre.

**Ejemplos típicos:**

```python
class Moto(Vehiculo):

    def descripcion(self):
        super().descripcion()                  # imprime marca y modelo
        print(f"Cilindrada: {self._cilindrada}cc")   # agrega lo propio


class LibroDigital(Libro):

    def __str__(self):
        return f"{super().__str__()} [{self._formato}]"


class ProductoImportado(ProductoConIVA):

    def precio_final(self):
        return super().precio_final() * 1.15   # encadena con el nivel de arriba
```

### Sobrescritura de métodos (override)

**¿Qué realiza?**

La hija define un método con el **mismo nombre** que el del padre. Al
llamarlo sobre una instancia de la hija, Python usa la versión de la
hija. Puede reemplazar por completo el comportamiento o extenderlo con
`super()`.

**Ejemplos típicos:**

```python
class Instrumento:
    def tocar(self):
        return "..."


class Guitarra(Instrumento):
    def tocar(self):                 # reemplaza la versión del padre
        return "Rasguido de guitarra"


class Piano(Instrumento):
    def tocar(self):
        return "Acorde de piano"
```

### Polimorfismo: un mismo bucle, muchos tipos

**¿Qué realiza?**

Un solo bucle recorre una lista con objetos de **distintas clases** y
llama al mismo método en todos. Cada objeto responde con su propia
versión. El código del bucle no tiene `if` por tipo y no hay que
tocarlo cuando aparece una clase nueva.

**Ejemplos típicos:**

```python
animales = [Perro("Firulais"), Gato("Michi"), Vaca("Lola"), Animal("Bicho")]

for animal in animales:
    animal.hablar()          # cada uno usa su sonido()


clientes = [Cliente("Ana"), ClienteVIP("Juan"), ClienteMayorista("Lucía")]

for cliente in clientes:
    print(cliente)           # cada categoría sabe su descuento()
```

### Despacho dinámico: `self.metodo()` resuelto según el objeto

**¿Qué realiza?**

Cuando un método del padre llama a `self.otro_metodo()`, Python usa la
versión de `otro_metodo` que corresponde al objeto **real**, no
necesariamente la del padre. Por eso `Cuenta.extraer()` puede llamar a
`self.comision()` y funcionar distinto para una `CuentaVIP` sin
reescribir `extraer()`.

**Ejemplos típicos:**

```python
class Cuenta:
    def comision(self):
        return 50

    def extraer(self, monto):
        total = monto + self.comision()   # ¿cuál comision()? la del objeto
        ...


class CuentaVIP(Cuenta):
    def comision(self):
        return 0

# vip.extraer(100) usa comision() == 0 sin tocar extraer()
```

### Duck typing: polimorfismo sin herencia

**¿Qué realiza?**

Una función llama a un método sobre el objeto que recibe sin
comprobar su tipo ni exigir una clase base común. Alcanza con que el
método exista. "Si camina como pato y hace cuac como un pato, es un
pato."

**Ejemplos típicos:**

```python
def hacer_hablar(cosa):
    print(cosa.hablar())          # no importa la clase, solo que tenga hablar()

hacer_hablar(Pato())
hacer_hablar(Robot())
hacer_hablar(Alarma())


def informar(dispositivos):
    for dispositivo in dispositivos:
        print(dispositivo.leer())   # Sensor, Reloj y Termostato: sin padre común
```

### Polimorfismo por parámetro

**¿Qué realiza?**

Una función recibe un objeto como parámetro y llama a su método. La
misma función sirve para cualquier subclase, porque el método llamado
se resuelve sobre el objeto concreto que se pasó.

**Ejemplos típicos:**

```python
def enviar_a_todos(notificacion, destinatarios):
    for destinatario in destinatarios:
        notificacion.enviar(destinatario)   # enviar() del tipo recibido

enviar_a_todos(NotificacionEmail("Bienvenidos"), destinatarios)
enviar_a_todos(NotificacionSMS("Su código es 1234"), destinatarios)
```

### `type(self).__name__` — Nombre de la clase concreta

**¿Qué realiza?**

Devuelve, como string, el nombre de la clase real del objeto. Se usa
para armar mensajes que se adapten a la subclase sin escribir el
nombre a mano en cada una.

**Ejemplos típicos:**

```python
raise NotImplementedError(
    f"La clase {type(self).__name__} debe implementar volumen()"
)

def __str__(self):
    return f"{type(self).__name__}: {self.volumen():.2f}"
```

### `__str__` heredado y `super().__str__()`

**¿Qué realiza?**

Si la hija no define `__str__`, usa el del padre. Si lo define, puede
reemplazarlo o reutilizar el del padre con `super().__str__()` y
agregar solo su parte, para no repetir el formato completo en cada
nivel de la jerarquía.

**Ejemplos típicos:**

```python
class Vehiculo:
    def __str__(self):
        return f"{self._marca} (Vmax: {self._velocidad_maxima}km/h)"


class Auto(Vehiculo):
    def __str__(self):
        return f"{super().__str__()}, {self._cantidad_puertas} puertas"


class AutoDeportivo(Auto):
    def __str__(self):
        return f"{super().__str__()}, {self._caballos_de_fuerza} HP"
```

### Acumulador manual (`+=`) frente a `sum()` con generador

**¿Qué realiza?**

Dos formas de totalizar sobre una lista polimórfica. El acumulador
manual sirve cuando además hay que hacer algo por cada elemento
(imprimir su estado); `sum()` con una expresión generadora es más
corto cuando solo interesa el total.

**Ejemplos típicos:**

```python
# Acumulador manual: se necesita imprimir en cada vuelta
danio_total = 0
for enemigo in enemigos:
    danio = enemigo.atacar()
    danio_total += danio
    print(f"{enemigo} ataca por {danio}")

# sum() + generador: solo interesa el total
total = sum(figura.area() for figura in figuras)
```

### Operador de exponente `**` y división

**¿Qué realiza?**

`x ** 2` eleva al cuadrado; `x ** 3`, al cubo. Se usan en las fórmulas
de área y volumen de cada subclase, junto con `/` para los factores
fraccionarios (`4 / 3`, `/ 2`).

**Ejemplos típicos:**

```python
def area(self):
    return self._lado ** 2

def volumen(self):
    return 4 / 3 * math.pi * self._radio ** 3

def area(self):
    return self._base * self._altura / 2
```

### f-strings y formato de valores

**¿Qué realiza?**

Incrustan expresiones en un string. En el capítulo se usan para armar
mensajes y para dar formato numérico: `{valor:.2f}` muestra dos
decimales (sueldos, áreas, comisiones) y `{valor:02d}` rellena con un
cero a la izquierda (la hora del reloj).

**Ejemplos típicos:**

```python
print(f"Gasto total: ${total:.2f}")

def __str__(self):
    return f"{self._nombre}: ${self.sueldo():.2f}"

def leer(self):
    return f"Reloj: {self._hora:02d}:{self._minuto:02d}"
```

---

## Resumen por Categoría

| Categoría | Elementos |
| --------- | --------- |
| **Funciones built-in** | `isinstance`, `len`, `print`, `sum`, `type` |
| **Métodos de `list`** | `append` |
| **Módulo `math`** | `math.pi` |
| **Tipos de excepción** | `AttributeError`, `NotImplementedError` |
| **Construcciones del lenguaje** | `class Hija(Padre)`, relación "es un", `pass` en subclase vacía, `super().__init__()`, `super().<metodo>()`, sobrescritura de métodos, polimorfismo sobre lista mixta, despacho dinámico (`self.metodo()`), duck typing, polimorfismo por parámetro, `type(self).__name__`, `__str__` heredado y `super().__str__()`, acumulador `+=` vs. `sum()` con generador, operador `**` y división, f-strings con formato |

---

## Notas Importantes

- **Herencia = "es un"; composición = "tiene un".** `Moto(Vehiculo)`
  porque una moto es un vehículo. Un auto no hereda de motor: *tiene*
  un motor. Esa distinción decide qué herramienta usar (composición se
  trabaja en el capítulo 12).

- **`super().__init__()` va primero.** En el `__init__` de la hija se
  llama al del padre antes de asignar los atributos nuevos, para que
  el objeto quede completo y en orden.

```python
def __init__(self, nombre, equipo):
    super().__init__(nombre)     # primero lo del padre
    self._equipo = equipo        # después lo propio
```

- **Sobrescribir no es borrar: se puede reutilizar al padre.** Con
  `super().metodo()` la hija ejecuta la versión del padre y le suma lo
  suyo. Copiar y pegar el cuerpo del método del padre en la hija es el
  error que `super()` viene a evitar.

- **El polimorfismo se nota en el código que NO cambia.** Un bucle que
  llama a `figura.area()` sobre una lista mixta no lleva `if
  isinstance(...)`. Cuando aparece una figura nueva, se agrega la
  clase y el bucle sigue igual. Un bucle lleno de `isinstance` que
  decide comportamiento es justo lo que hay que reemplazar.

- **Python elige el método según el objeto, no según dónde está
  escrito el llamado.** `Cuenta.extraer()` llama a `self.comision()`;
  si el objeto es una `CuentaVIP`, se usa `CuentaVIP.comision()`
  aunque `extraer()` esté definido en `Cuenta`. Eso es el despacho
  dinámico.

- **Duck typing no necesita una clase base.** `Pato`, `Robot` y
  `Alarma` no heredan de nada en común: la función `hacer_hablar()`
  funciona porque las tres tienen `hablar()`. Hacer lo mismo con
  `__str__` no sería duck typing puro, porque `__str__` ya viene de
  `object` y toda clase lo hereda.

- **`NotImplementedError` avisa, no impide.** Definir `area()` en la
  clase base con `raise NotImplementedError` documenta el contrato y
  falla si alguien no lo cumple, pero no bloquea instanciar la clase
  base. Bloquear la instanciación es tema del capítulo 13 (`abc`).

- **Todo hereda de `object`.** `isinstance(pichicho, object)` es
  siempre `True`. Por eso todas las clases ya tienen un `__str__` y un
  `__init__` por defecto aunque no se escriban.

- **La cadena de herencia puede tener más de dos niveles.**
  `AutoDeportivo` → `Auto` → `Vehiculo`. Cada nivel usa `super()` para
  encadenar con el inmediatamente superior; no hace falta nombrar al
  "abuelo".
