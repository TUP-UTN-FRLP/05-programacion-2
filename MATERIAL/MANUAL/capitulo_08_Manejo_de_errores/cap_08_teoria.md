# Manejo de errores

> Anticipando lo que puede fallar.

## ¿Por qué leemos este capítulo?

Hasta acá venimos escribiendo programas que funcionan cuando el usuario colabora. Si el ejercicio pide un número entero, esperamos que ingrese un número entero. Si abrimos un archivo, esperamos que exista. Si dividimos, esperamos que el divisor no sea cero. En el mundo real, ninguna de esas cosas está garantizada.

Ya venís esquivando este problema desde el capítulo de condicionales, cuando validábamos con isdigit() antes de hacer int(). Esa estrategia, chequear todo antes, se llama **look before you leap (LBYL)**: mirá antes de saltar. Funciona, pero se vuelve engorroso: si querés cubrir todos los casos posibles, terminás escribiendo más código de validación que de lógica real.

Python ofrece una alternativa: **easier to ask forgiveness than permission (EAFP)**: probá directo, y si algo falla, atrapalo. Ese es el trabajo del bloque try/except. En vez de anticipar cada error posible, lo dejás pasar, lo capturás cuando ocurre, y decidís qué hacer.

Este capítulo es corto pero clave. Sin manejo de errores, un programa que corre en el laboratorio se rompe la primera vez que lo prueba un usuario real.

### LBYL vs EAFP: El estilo pythónico

Python favorece la filosofía EAFP (Easier to Ask Forgiveness than Permission) sobre LBYL (Look Before You Leap).

En vez de chequear con if que algo va a andar antes de intentarlo, se ejecuta la acción y se atrapa con **try/except** si falla. Es más robusto, cubre errores que no anticipaste y evita **condiciones de carrera** cuando aprendamos programación concurrente en Django.

## Excepciones: qué son y por qué ocurren

Una **excepción** es la forma que tiene Python de decir "algo salió mal". Cuando el intérprete se encuentra con una situación que no puede resolver como dividir por cero, convertir "abc" a entero, abrir un archivo que no existe, lanza una excepción y **el programa se corta** en ese punto.

```python
edad = int("abc")   # ValueError: invalid literal for int() with base 10: 'abc'
```

El mensaje que vemos en rojo no es una alerta cualquiera: es Python contándonos qué tipo de excepción se produjo **(ValueError)** y por qué. Ese tipo tiene nombre propio, y sirve para atraparla selectivamente después.

Algunas excepciones que ya te cruzaste:

| Excepción | Cuando aparece |
| --- | --- |
| ValueError | Un valor tiene el tipo correcto, pero es inválido: int("hola"), float("$5") |
| TypeError | Se combinan tipos incompatibles: "3" + 5, len(42) |
| ZeroDivisionError | Se divide algo por cero |
| IndexError | Se accede a un índice fuera de rango en una lista: lst[100] con len(lst) == 3 |
| KeyError | Se accede a una clave que no existe en un diccionario: d["fantasma"] |
| FileNotFoundError | Se intenta abrir un archivo que no existe |
| AttributeError | Se llama a un método que no tiene ese objeto: "hola".append("x") |
| NameError | Se usa una variable que no fue definida |

Todas ellas descienden de una clase base común (Exception), tema que vas a ver formalmente en POO, por ahora alcanza a saber que son categorías con jerarquía.

## try / except: la estructura básica

La idea es simple: envolvés en try el código que puede fallar, y ponés en except qué hacer si falla.

```python
try:
    edad = int(input("Edad: "))
    print(f"El año que viene tendrás {edad + 1}")
except ValueError:
    print("Eso no es un número válido")
```

Si el usuario ingresa 25, todo corre normal y el mensaje del except no aparece. Si ingresa veinticinco, int() lanza ValueError y Python **salta** al except, ejecuta esa rama, y el programa continúa después del bloque sin romperse.

Comparalo con la versión LBYL que veníamos usando:

```python
# Versión "look before you leap" (chequear antes)
entrada = input("Edad: ")
if entrada.isdigit():
    edad = int(entrada)
    print(f"El año que viene tendrás {edad + 1}")
else:
    print("Eso no es un número válido")
```

Las dos hacen lo mismo, pero:

- La versión con isdigit() **no acepta negativos** ("-5".isdigit() es False).
- La versión con int() sí acepta negativos, y espacios en los extremos, y ceros a la izquierda: int(" -05 ") devuelve -5 sin drama.

**Ese es el mensaje central:**

try/except no es solo "más limpio", es más general. Delegamos la validación al mecanismo que ya sabe qué es un número válido para Python.

### EJERCICIO 1

Reescribí este código para que use try/except en vez de isdigit(). Debe aceptar negativos.

```python
entrada = input("Número: ")
if entrada.isdigit():
    numero = int(entrada)
    print(f"El doble es {numero * 2}")
else:
    print("No es un número")
```

Solución:

*Ver código en el archivo `.py` correspondiente.*

Ahora "-3" funciona: el doble de -3 es -6. Con isdigit() no habría pasado la validación.

## Atrapando varias excepciones

Un solo try puede lanzar varios tipos distintos de excepción. Podés atraparlas por separado:

```python
try:
    numerador = int(input("Numerador: "))
    denominador = int(input("Denominador: "))
    print(f"Resultado: {numerador / denominador}")
except ValueError:
    print("Ingresá números enteros, por favor")
except ZeroDivisionError:
    print("No se puede dividir por cero")
```

Python evalúa los except en orden, y ejecuta solo el que corresponde al tipo de excepción. Si ninguno matchea, la excepción sigue viajando "hacia afuera" y el programa termina como si no hubieras puesto el try.

También podés atrapar varios tipos en una sola rama, con una tupla:

```python
try:
    ...
except (ValueError, ZeroDivisionError):
    print("Entrada inválida o división por cero")
```

Se usa cuando la reacción es la misma para varios tipos.

### EJERCICIO 2

Una calculadora simple que pida dos números y una operación (+, -, *, /), y muestre el resultado. Debe manejar entradas no numéricas y división por cero, con mensajes distintos.

*Ver código en el archivo `.py` correspondiente.*

Todo el bloque de conversiones y cálculos vive dentro del try. Si algún paso falla, se corta ahí y salta al except correspondiente.

## Capturando el mensaje del error

A veces querés saber **qué dijo exactamente** la excepción. Se hace con as:

```python
try:
    edad = int(input("Edad: "))
except ValueError as e:
    print(f"Error: {e}")
```

Si el usuario ingresa hola, la salida es:

```python
Error: invalid literal for int() with base 10: 'hola'
```

Los mensajes vienen en inglés porque son de la biblioteca estándar. Sirven para logs, debug o para mostrar información técnica en un modo verboso. En un programa para usuarios finales, mejor traducir el mensaje a algo comprensible.

## Un peligro: except sin tipo

Se puede escribir un except sin especificar tipo, que atrapa **todo**:

```python
try:
    edad = int(input("Edad: "))
except:                     # Peligroso
    print("Algo salió mal")
```

**No lo hagas.** Este **idiom** atrapa incluso **KeyboardInterrupt (Ctrl+C para cortar el programa)** o **SystemExit**, lo cual complica muchísimo la depuración. Además, esconde bugs: si el problema era un **Typo** (anglicismo, error de tipeo abreviado) en el código y no una entrada inválida, el except se lo traga y nunca te enterás.

**Regla firme:**

Siempre especificá el tipo.

Si de verdad querés atrapar cualquier error "esperable", usá except Exception, que captura los errores comunes, pero deja pasar los de sistema:

```python
try:
    ...
except Exception as e:
    print(f"Error inesperado: {e}")
```

## else y finally

El bloque try tiene dos cláusulas opcionales que a veces salvan el día:

### else: cuando no hubo excepción

Se ejecuta **solo si el try no lanzó ninguna excepción**. Es útil para separar el código que puede fallar del que corre "si todo salió bien":

```python
try:
    edad = int(input("Edad: "))
except ValueError:
    print("Edad inválida")
else:
    print(f"Tenés {edad} años")
    print(f"El año que viene tendrás {edad + 1}")
```

¿Por qué separar los print en el **else** en vez de meterlos dentro del **try**? Porque el try debería contener solo el código que puede fallar. Poner lógica extra ahí adentro es pedir que se atrapen errores inesperados en el lugar equivocado, si uno de los print fallara por otro motivo (imaginate un f-string mal formateado), el except ValueError lo taparía y mostraría "Edad inválida" cuando el problema era otro.

### finally: pase lo que pase

Se ejecuta **siempre**, haya habido excepción o no. Sirve para tareas de limpieza que no pueden saltarse:

```python
try:
    archivo = open("datos.txt")
    contenido = archivo.read()
    archivo.close()
except FileNotFoundError:
    print("El archivo no existe")
finally:
    print("Fin del intento de lectura")
```

**¿Qué es ese** close() **que aparece?** Cuando abrís un archivo con open(), Python le pide al sistema operativo un **recurso**: un canal de comunicación entre tu programa y el archivo en disco. Ese canal ocupa memoria, se cuenta contra el límite de "archivos abiertos simultáneamente" del sistema, y bloquea al archivo para otros programas.

close() libera ese recurso, le avisa al sistema operativo *"terminé con este archivo"*. Si no lo llamás, pasan cosas malas: se acumulan fugas de memoria, y si estabas escribiendo, tus datos pueden no llegar al disco (Python guarda lo que escribís en un buffer interno que se vacía al cerrar). **Siempre que abras un archivo, tenés que cerrarlo.**

En el ejemplo de arriba, el close() está **dentro del try**: se cierra solo si open() funcionó. Si open() falla, el close() no se ejecuta, y está bien, porque no hay nada que cerrar. La idea de meter close() en el **finally** "por si acaso" parece prolija, pero rompe: si open() falló, la variable archivo nunca se creó, y archivo.close() daría NameError.

### La solución moderna: with

Todo este baile de "abrir, procesar, acordarse de cerrar, manejar el caso donde no se pudo abrir" tiene una respuesta más limpia: el bloque with. Cierra el archivo automáticamente al salir del bloque, incluso si hubo excepción:

```python
try:
    with open("datos.txt") as archivo:
        contenido = archivo.read()
        # trabajás con el archivo acá adentro

    # al salir del bloque with, el archivo ya se cerró solo
except FileNotFoundError:
    print("El archivo no existe")
```

with es el **idiom pythónico** para trabajar con archivos y con cualquier recurso que necesite cerrarse: conexiones a bases de datos, sockets de red, locks. Delega la limpieza a Python. En este capítulo solo lo mencionamos, lo vamos a ver formalmente en el capítulo de librerías.

**Consecuencia práctica:**

En código moderno, finally se usa poco. Antes de with era la única forma de garantizar el cierre, hoy queda para casos especiales (limpiar variables, reiniciar estado, cerrar cosas más raras que archivos). Conceptualmente vale conocerlo porque vas a ver finally en código heredado, y porque la idea de "esto se ejecuta pase lo que pase" es útil en sí misma.

### Estructura completa

Cuando aparecen las cuatro cláusulas, el orden es fijo:

```python
try:
    # código que puede fallar
except TipoError:
    # si falló con TipoError
else:
    # si no falló
finally:
    # siempre, haya fallado o no
```

#### EJERCICIO 3

**(ejercicio didáctico):** aunque ya vimos que finally se usa poco en código real, vale la pena armar al menos un bloque con las cuatro cláusulas para que veas cuándo se dispara cada una.

Convertí un pedido de edad en un bloque completo: el **try intenta convertir, el except ValueError maneja el error, el else felicita al usuario, y el finally imprime "Gracias por participar"** siempre.

**Solución:**

*Ver código en el archivo `.py` correspondiente.*

Probá con 25, con abc, y observá cuándo se imprime cada mensaje. Vas a ver que:

**Con 25:** se ejecutan else y finally.

**Con abc:** se ejecutan except y finally.

**En los dos casos** aparece "Gracias por participar", esa es la marca registrada de finally.

## Lanzar excepciones con raise

Hasta ahora **atrapamos** excepciones. Pero también podés **lanzarlas** vos mismo, cuando tu código detecta una situación inválida:

*Ver código en el archivo `.py` correspondiente.*

Usar **raise** en tus propias funciones deja claro que un caso no está soportado, y le da al que llama la oportunidad de manejarlo con **try/except**. Es más limpio que devolver None y esperar que el llamador se acuerde de chequear.

### Reglas prácticas para elegir qué excepción lanzar

- **ValueError**: el valor es del tipo correcto pero inválido (número negativo donde hay que positivo, string vacío donde no debería, fecha imposible).
- **TypeError**: el tipo es incorrecto (te pasaron un string donde esperabas un número).
- **KeyError / IndexError**: para colecciones, cuando no encontrás algo.
- **Exception**: genérico, solo si no encaja en ninguna categoría.

Al principio te vas a apoyar en las excepciones existentes. En POO vas a aprender a **crear las tuyas propias**, con nombres específicos para tu dominio (SaldoInsuficienteError, AlumnoNoEncontrado, etc.).

## Comparando estilos: LBYL vs EAFP

Volvamos al principio del capítulo con más claridad. Los dos estilos son válidos y a veces conviven en el mismo programa. Cuando usar cada uno:

### LBYL (chequear antes)

```python
if divisor != 0:
    resultado = numerador / divisor
```

✅ Rápido cuando el chequeo es simple.

✅ Deja explícita la condición en el código (lees "solo si es distinto de cero").

❌ Se vuelve pesado si hay que chequear muchas cosas.

❌ **Race conditions**: entre el chequeo y la acción, algo pudo haber cambiado (más importante en archivos y bases de datos).

### EAFP (probar y atrapar)

```python
try:
    resultado = numerador / divisor
except ZeroDivisionError:
    resultado = 0
```

✅ Cubre todos los casos posibles automáticamente.

✅ Más idiomático en Python (la comunidad lo prefiere).

✅ Sin race conditions.

❌ Levemente más lento cuando hay excepciones (irrelevante en la práctica salvo miles por segundo).

❌ Puede esconder bugs si atrapás demasiado (por eso el except Exception es el límite).

**En Python la comunidad favorece EAFP.**

No es una regla estricta, pero el idiom preferido para validar entradas del usuario, acceder a archivos, o convertir tipos es try/except. Reservá LBYL para condiciones de negocio (validar un rango, chequear un estado interno) donde el chequeo es parte de la lógica, no del manejo de fallas.
