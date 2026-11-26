# Control de flujo condicional

_If, lógica, match/case_

## ¿Por qué leemos este capítulo?

Este capítulo marca el verdadero punto de inflexión entre programar en C y programar en Python. Hasta aquí manejamos datos y los guardamos en memoria. Ahora comenzamos a tomar decisiones. El cambio no radica en la lógica (una condición verdadera o falsa sigue siendo lo mismo), sino en cómo se escribe esa lógica y cómo interactúa con las funciones nativas de Python.

## La estructura IF en Python: Adiós a los paréntesis

En C, la sintaxis de un condicional exige el uso de paréntesis para la condición y llaves para el bloque de código. Python simplifica esto drásticamente, pero impone una regla estricta de formato.

**Diferencias clave al escribir un IF en Python:**

- No se usan paréntesis alrededor de la condición (aunque si los ponés, Python no se queja, pero se considera mala práctica).
- La condición debe terminar obligatoriamente con dos puntos (`:`).
- La línea siguiente debe estar indentada (corrida hacia la derecha, por convención 4 espacios). Esto reemplaza a las llaves `{}` de C.
- Para el "sino", se usa la palabra reservada `else`, seguida de dos puntos.

Estructura en C:

```c
if (edad >= 18) {
    printf("Es mayor");
} else {
    printf("Es menor");
}
```

Estructura en Python:

```python
if edad >= 18:
    print("Es mayor")
else:
    print("Es menor")
```

> **TIP:** El error más común al venir de C es olvidar los dos puntos (`:`) al final de la línea del `if` o del `else`. Si no los ponés, Python dará un error de sintaxis antes de que siquiera ejecutes el programa.

![](img/cap03_img01.jpeg)

**EJERCICIO** (en VSC abre crea una carpeta de ejercicio y crea un archivo con el nombre que quieras, escribis el codigo y guardalo como .py):

Escribí un programa que pida al usuario un número. Antes de verificar si es positivo o cero, usá un `if` para comprobar que el usuario no haya ingresado letras (podés usar la función de strings `isdigit()`). Si ingresó letras, mostrá un error. Si no, evaluá el número e imprimí "Positivo" o "Cero".

> Ver código en el archivo `.py`.

Los comentarios se indican con `#` en cada línea.

La forma `variable.funcion()` es mas de programación orientada a objetos. Un objeto tiene un comportamiento ante un mensaje y se llama así: `objeto.mensaje()`. En este caso, `entrada.isdigit()` pregunta "¿entrada, no sos digito?" y si ingresas digito responde `True` y lo negás con el `not`, queda `False`.

Pero ojo, no es que pregunta si es número, pregunta es dígito. Es una diferencia sutil, lo que pregunta es si el carácter es de un número, pero sigue siendo carácter. Por eso, al asegurarnos que es de un 0 a un 9, lo convertimos a digito usando el input para forzar que se guarde un número, no un carácter.

```python
numero = int(entrada)
```

El resto seguro que ya lo entendiste.

## Operadores Lógicos: El fin de &&, || y !

En C, para unir condiciones usábamos los símbolos `&&` (Y), `||` (O) y `!` (NO). Python abandona estos símbolos por legibilidad, simple es mejor, reemplazándolos por palabras en inglés. Tampoco se usa paréntesis.

### AND (Y lógico):

Ambas condiciones deben ser verdaderas.

- En C: `if (a > 0 && b > 0)`
- En Python: `if a > 0 and b > 0`

### OR (O lógico):

Al menos una condición debe ser verdadera.

- En C: `if (nota == 10 || nota == 9)`
- En Python: `if nota == 10 or nota == 9`

### NOT (NO lógico):

Invierte el valor de verdad.

- En C: `if (!bandera)`
- En Python: `if not bandera`

> **TIP: Comparaciones encadenadas.**
> En C, para saber si un número está entre 1 y 10, debías escribir: `if (x >= 1 && x <= 10)`. En Python, podés escribirlo exactamente como lo leés en matemáticas: `if 1 <= x <= 10`. Esto es exclusivo de Python y está permitido gracias a su diseño.

![](img/cap03_img01.jpeg)

**EJERCICIO**

Escribí un programa que pida una edad y un género (ingresado como "M" o "F"). Utilizá la función `lower()` del string ingresado para asegurarte de que funcione, aunque el usuario ingrese "m" o "f" minúscula. La persona debe ser mayor o igual a 18 años Y del género "F" para imprimir "Cumple para integrar equipos deportivos femeninos". En cualquier otro caso, imprimir "No cumple con el perfil".

> Ver código en el archivo `.py`.

Los comentarios se indican con `#` en cada línea. Por legibilidad separa cada parte del programa con comentarios. Ya lo vimos, pero es importante que entiendas la forma `variable.funcion()`. En este caso, `genero.lower()` pide una acción "pasalo a minúsculas" tomando cada carácter en mayúsculas y lo pasa a minúsculas. Lo mismo que `isdigit()`, analiza caracteres ASCII.

## Decisiones múltiples: ELIF y MATCH/CASE

Cuando tenemos múltiples caminos posibles en C, usábamos una estructura de `else if` encadenados, o un `switch/case`.

### ELIF (Else If):

En Python, el "else if" se escribe junto y sin espacios: `elif`. Siempre va después de un `if` y antes de un `else` (si lo hay).

### MATCH / CASE (El nuevo Switch):

Durante mucho tiempo Python no tuvo `switch`. A partir de la versión 3.10 (la que usamos en la materia), se introdujo `match/case`.

**Diferencias con el switch de C:**

- No se usa la palabra `switch`, se usa `match`.
- En C se usa `case valor:`, en Python también `case valor:`.
- No es necesario poner un `break` al final de cada caso. Python no tiene la falla de caída (fall-through) de C. Al terminar un `case`, sale automáticamente.
- El equivalente a `default` es `case _` (un guión bajo).

En C:

```c
switch (dia) {
    case "Lunes":
        printf("Inicio de semana\n");
        break;
    case "Viernes":
        printf("Casi fin de semana\n");
        break;
    default:
        printf("Día normal\n");
}
```

Match en Python:

```python
match dia:
    case "Lunes":
        print("Inicio de semana")
    case "Viernes":
        print("Casi fin de semana")
    case _:
        print("Día normal")
```

> **TIP:** Cuando usás `match/case` con strings, es muy útil aplicar funciones como `capitalize()` o `strip()` al valor ingresado para normalizar los datos antes de compararlos en los casos.

![](img/cap03_img01.jpeg)

**EJERCICIO**

Escribí un programa que pida un día de la semana (por ejemplo "lunes"). Usá la función `capitalize()` para convertir la primera letra a mayúscula y luego la estructura `match/case` para imprimir "Inicio de semana" (Lunes), "Mitad de semana" (Miércoles) o "Día normal" para el resto. Si ingresan cualquier otra cosa, imprimí "Dato no válido" usando el `case _`.

> Ver código en el archivo `.py`.

Los comentarios se indican con `#` en cada línea. Por legibilidad separa cada parte del programa con comentarios.

Ya lo vimos la forma `variable.funcion()`. En este caso, `dia.capitalize()` pide una acción "pasa la primera letra a mayúsculas". Eso permite que se compare unívocamente los casos, todos tienen la primera letra mayúscula.

Una forma más compacta (recomendable) es combinar "mensajes":

```python
dia = input("Ingresa un día de la semana: ").capitalize()
```

Otra interesante forma que ofrece Python es el uso de "pipes". Acá lo que hacemos es indicar si es Lunes o si es Martes…. O sea, mira el primer caso y pregunta ¿Es o no? Ante false, buscamos el siguiente. Solo si todos es falso paso al siguiente caso. Asi actúa el `match`, verificando si un caso es `True` y de no serlo, pasa al siguiente. De esta manera evitamos escribir 5 casos para que responda lo mismo:

```python
case "Martes" | "Jueves" | "Viernes" | "Sábado" | "Domingo":
```
