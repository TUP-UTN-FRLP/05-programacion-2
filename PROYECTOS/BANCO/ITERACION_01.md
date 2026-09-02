# Proyecto Integrador Banco — Iteración 1

## Introducción

A partir de esta etapa comenzaremos a construir un sistema bancario que irá
evolucionando durante cinco iteraciones.

Cada iteración incorporará solamente los conceptos trabajados hasta ese
momento en la materia.

El objetivo no es construir desde el primer día un sistema completo, sino
hacer evolucionar el mismo problema a medida que incorporamos nuevos
conceptos de Programación Orientada a Objetos.

---

## Objetivo de la Iteración 1

Modelar una **cuenta bancaria básica** que permita:

- crear una cuenta;
- almacenar un número de cuenta;
- almacenar un titular;
- almacenar un saldo;
- depositar dinero;
- extraer dinero;
- mostrar el estado de la cuenta.

En esta primera iteración se utilizarán exclusivamente los conceptos vistos
hasta este momento:

- clases;
- atributos;
- métodos;
- `self`;
- `__init__`;
- `__str__`;
- parámetros;
- parámetros con valor por defecto.

---

## Importante: esta versión es deliberadamente incompleta

En esta iteración **no deben agregarse validaciones ni mecanismos que todavía
no fueron trabajados en clase**.

No deben utilizarse:

- propiedades;
- getters o setters;
- excepciones;
- herencia;
- archivos;
- bases de datos;
- Django;
- interfaces gráficas;
- frontend;
- mecanismos de persistencia.

Que el programa permita determinadas situaciones incorrectas forma parte
del objetivo de esta iteración.

La siguiente etapa del proyecto utilizará nuevos conceptos para resolver
algunas de estas limitaciones.

---

## La clase `Cuenta`

Cada estudiante deberá implementar una clase llamada:

```python
Cuenta
```

La clase deberá tener tres atributos:

```text
numero
titular
saldo
```

El constructor deberá recibir:

```text
numero
titular
saldo_inicial
```

El parámetro `saldo_inicial` deberá tener como valor por defecto:

```python
0
```

Por lo tanto, deberá ser posible crear una cuenta indicando un saldo inicial
o crearla sin indicar saldo.

Ejemplo conceptual:

```python
cuenta_1 = Cuenta("001-234", "Ana Pérez", 1000)
cuenta_2 = Cuenta("001-235", "Juan López")
```

La segunda cuenta deberá comenzar con saldo cero.

---

## Métodos obligatorios

La clase deberá implementar los siguientes métodos.

### `depositar(monto)`

Debe aumentar el saldo de la cuenta en el monto recibido.

En esta iteración no debe realizar validaciones.

### `extraer(monto)`

Debe disminuir el saldo de la cuenta en el monto recibido.

En esta iteración no debe realizar validaciones.

### `__str__()`

Debe devolver una representación legible de la cuenta que incluya:

- número de cuenta;
- titular;
- saldo.

El formato exacto puede variar levemente, pero debe ser claro y permitir
identificar el estado de la cuenta.

Ejemplo esperado:

```text
Cuenta N° 001-234 - Ana Pérez - Saldo: $1300.00
```

---

## Archivo de trabajo

La solución deberá guardarse en:

```text
banco.py
```

Cada estudiante trabajará sobre su propia rama correspondiente a la
iteración.

Ejemplo:

```text
iteracion-01/juan-perez
iteracion-01/ana-gomez
iteracion-01/pedro-lopez
```

Cada integrante debe resolver **la iteración completa**.

No se divide el trabajo de la clase entre integrantes.

---

## Sobre el archivo `test.py`

En el repositorio del grupo puede aparecer un archivo `test.py` provisto por la
cátedra.

**En esta iteración no se usa ni se agrega:** no se ejecuta, no se modifica y
no se instala `pytest`. No forma parte de la entrega de la Iteración 1.

Está únicamente como **referencia para el estudiante**: se puede abrir y leer
para ver, escrito en código, qué comportamiento se va a verificar más adelante.
El trabajo con `pytest` se incorpora recién en la Iteración 4, para no sumar
una herramienta más mientras se aprenden los primeros conceptos de POO.

La verificación de esta iteración es la que se describe en las secciones
siguientes: ejecutar el escenario de `banco.py` y observar la salida.

---

## Pruebas obligatorias

Cada estudiante deberá demostrar en su propia solución que puede:

1. crear una cuenta con saldo inicial;
2. crear una cuenta sin saldo inicial;
3. realizar un depósito;
4. realizar una extracción;
5. mostrar la cuenta antes y después de operar.

Además deberá comprobar que, en esta versión, también son posibles situaciones
incorrectas.

---

## Situaciones incorrectas que deben probarse

### Depositar un monto negativo

La versión actual deberá permitir algo equivalente a:

```python
cuenta.depositar(-500)
```

Esto es incorrecto desde el punto de vista del negocio bancario, pero todavía
no existe ninguna validación que lo impida.

### Extraer más dinero del disponible

La versión actual deberá permitir algo equivalente a:

```python
cuenta.extraer(100000)
```

La cuenta puede quedar con saldo negativo.

Por ahora no debe evitarse.

### Crear una cuenta con datos inválidos

La versión actual puede permitir una cuenta con:

```text
número vacío
titular vacío
saldo inicial negativo
```

Por ejemplo, conceptualmente:

```python
Cuenta("", "", -1000)
```

No debe corregirse todavía.

### Modificar directamente el saldo

En esta iteración también será posible modificar el atributo directamente:

```python
cuenta.saldo = 99999999
```

Por ahora tampoco debe impedirse.

---

## ¿Por qué probamos cosas que están mal?

Porque queremos observar las limitaciones reales de esta versión.

Todo esto es legítimo desde el punto de vista del programa actual: todavía
no existen reglas que protejan los datos ni validen las operaciones.

Estas limitaciones servirán como punto de partida para la siguiente
iteración, donde trabajaremos encapsulamiento y validación.

---

## Bloque de prueba

Las pruebas pueden colocarse dentro de:

```python
if __name__ == "__main__":
```

Por ahora alcanza con entender que ese bloque contiene código que se ejecuta
cuando `banco.py` se ejecuta directamente.

Su funcionamiento se explicará con más detalle más adelante.

---

## Decisiones de diseño para pensar

### 1. ¿Por qué conviene que el número de cuenta sea un `str`?

Pensar en casos como:

```text
001-234
000123
CA-001-2026
```

¿El número de cuenta se utiliza para realizar operaciones matemáticas o para
identificar una cuenta?

### 2. Fecha de creación

Si en una iteración futura quisiéramos almacenar la fecha de creación de una
cuenta:

¿debería recibirla el constructor como parámetro o debería determinarla
automáticamente la propia clase?

No es necesario implementarlo todavía.

---

## Trabajo individual

Cada integrante del grupo deberá:

- crear su propia rama;
- desarrollar la iteración completa;
- escribir el código;
- ejecutar sus propias pruebas;
- realizar commits durante el proceso;
- publicar la rama en GitHub;
- abrir un Pull Request hacia la rama de integración del grupo cuando
  corresponda.

Ejemplo de rama:

```text
iteracion-01/nombre-apellido
```

---

## Commits

No se espera un único commit al finalizar.

Se recomienda registrar avances identificables.

Ejemplos:

```text
Agrega clase Cuenta
Implementa constructor de Cuenta
Implementa deposito y extraccion
Agrega representacion de Cuenta
Agrega pruebas de la iteracion 1
```

Evitar mensajes como:

```text
cambios
prueba
final
cosas
```

---

## Integración grupal

Una vez que todos los integrantes hayan publicado su solución individual,
el grupo comparará las distintas implementaciones.

Después se construirá una versión consensuada en:

```text
integracion/iteracion-01
```

El objetivo no es elegir automáticamente la solución de un integrante.

El grupo deberá comparar las alternativas y construir una versión que todos
puedan explicar.

---

## Líder de la semana

Cada iteración tendrá un integrante designado como líder de integración.

Durante esta semana el líder será responsable de:

- revisar los Pull Requests individuales;
- coordinar la comparación de soluciones;
- conducir la construcción de la rama de integración;
- verificar que la versión integrada funcione;
- abrir el Pull Request final de la iteración.

El liderazgo rotará en las siguientes iteraciones.

---

## Entrega de la Iteración 1

La entrega final de la semana será la rama:

```text
integracion/iteracion-01
```

El líder abrirá un Pull Request hacia:

```text
main
```

Ese Pull Request será revisado por la cátedra.

La versión integrada deberá contener:

- la clase `Cuenta`;
- las operaciones solicitadas;
- ejemplos o pruebas de funcionamiento;
- pruebas de las limitaciones actuales;
- código que todos los integrantes puedan explicar.

---

## Criterio central

El objetivo de esta iteración no es solamente obtener un programa que
funcione.

Cada integrante debe poder decir:

> Implementé personalmente toda la iteración, probé sus limitaciones,
> comparé mi solución con las de mis compañeros y participé en la
> construcción de la versión integrada del grupo.
