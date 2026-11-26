# Datos, Tipos Primitivos y Expresiones

_Parecido a C, pero tiene sus particularidades…_

## ¿Por qué leemos este capítulo?

Este título es clásico. Antes de poder tomar decisiones en un programa (como evaluar si un usuario es mayor de edad o si una nota está aprobada), necesitamos comprender cómo el programa almacena, transforma y muestra los datos. En este capítulo, abandonaremos la rigidez de la memoria de C para adoptar el modelo dinámico de Python.

## Asignación de Datos: Cajas vs. Etiquetas

El concepto más crítico que debe desaprender un programador de C es cómo funciona la asignación de variables.

En C, una variable es una "caja" física en la memoria RAM. Cuando escribimos `int x = 5;`, le decimos al compilador: "Resérvame una caja del tamaño de un entero (4 bytes), ponle una etiqueta que diga x y meté el número 5 adentro". Si intentás poner un texto ahí, el programa explota porque la caja es muy chiquita o del tipo equivocado.

En Python, las variables son **etiquetas** (o referencias). Cuando escribís `x = 5`, le estás diciendo al intérprete: "Creá un objeto en memoria que contenga el valor 5, y pegale la etiqueta x". Esto permite la **re-asignación de tipos** (tipado dinámico), algo imposible en C:

```python
x = 10		# La etiqueta 'x' apunta a un objeto entero

x = "Hola"	# Ahora la etiqueta 'x' la despegamos del 10,
    		# y la pegamos a un objeto texto

x = 3.14   	# Ahora apunta a un objeto
 			# flotante
```

Es decir, ante el cambio de tipo, solo apunta a otro lugar de memoria. Además, en Python no existen los puntos y coma al final de la instrucción. El final de la línea marca el final de la asignación.

## Tipos de Datos Primitivos

Python maneja los datos fundamentales de manera muy distinta a C. A continuación, los cuatro tipos primitivos esenciales:

### Enteros (int)

En C, un entero tiene un límite (por ejemplo, 32 bits, llegando hasta unos 2 mil millones). En Python, el tipo int tiene **precisión arbitraria**. Ocupa la memoria que sea necesaria. Podés calcular un número con 1000 dígitos y Python no sufrirá un **overflow** (desbordamiento).

```python
edad = 25
numero_gigante = 10 ** 100
# El doble ** es potencia, o sea generamos 1 con 100 ceros, funciona perfectamente
```

### Flotantes (float)

Representan números con decimales. Equivalen al double de C (64 bits, estándar IEEE 754).

```python
precio = 150.50
pi = 3.14159
```

### Booleanos (bool)

Solo pueden tener dos valores: True o False (Con mayúscula inicial, a diferencia del true o false de C o Java). Internamente, Python trata a True como el número 1 y a False como el número 0.

```python
es_mayor = True
aprobado = False
```

### Cadenas de texto (str)

En C, un texto es un arreglo de caracteres terminado en \0. En Python, es un objeto inmutable de primera clase.

**Diferencia clave:** En Python no existe el tipo char (carácter individual). Un carácter simple es simplemente un string de longitud 1. Se pueden definir con comillas simples o dobles (indistintamente).

```python
letra = "A"       # Esto es un string, no un char
nombre = 'Juan'   # Esto también es un string
frase = "Hola Mundo"
```

### La función type()

Como el tipo es dinámico, si en algún momento no sabés de qué tipo es tu variable, podés preguntarle a Python usando la función incorporada type().

```python
type(10)        # Devuelve <class 'int'>
type(3.14)      # Devuelve <class 'float'>
type("Hola")    # Devuelve <class 'str'>
```

## Por qué Python no necesita imports como `#include <stdio.h>`

En C, los #include son directivas del preprocesador que traen declaraciones de funciones y tipos necesarios para compilar el código. Por ejemplo, #include <stdio.h> aporta las funciones printf() y scanf().

Python, siendo un lenguaje interpretado con una filosofía de "baterías incluidas" (**batteries included**), integra directamente en su intérprete una biblioteca estándar muy amplia que proporciona funciones esenciales como print(), input(), len(), range() y muchas otras sin necesidad de importarlas explícitamente.

Solo necesitas usar import en Python cuando quieres acceder a módulos especializados (como math, random, datetime) que no son parte del núcleo del lenguaje, esto hace que el código sea más limpio y accesible para principiantes, ya que pueden comenzar a programar inmediatamente sin preocuparse por incluir librerías básicas de entrada/salida como en C.

## Entrada y Salida de Datos (I/O)

Comunicarse con el usuario es fundamental. En C usábamos printf y scanf. En Python usamos funciones.

### Salida con print():

Por defecto, agrega un salto de línea al final.

```python
print("Hola Mundo")
print("Línea 1")
print("Línea 2")
```

### La magia de los f-strings:

Para mezclar texto con variables, en C usábamos %d o %s. En Python moderno (3.6+) se usan los **f-strings**. Se antepone una f a las comillas y se incrustan las variables entre llaves {}.

```python
edad = 20
nombre = "Ana"
print(f"Mi nombre es {nombre} y tengo {edad} años")
```

### Entrada con input():

Siempre lee lo que el usuario escribe en el teclado y lo devuelve como un string (texto). Si querés hacer operaciones matemáticas, tenés que transformarlo (hacer un **cast o conversión**).

Pedir un texto

```python
nombre = input("Ingrese su nombre: ") # No hace falta convertirlo
```

Pedir un número

```python
entrada = input("Ingrese su edad: ")  # Esto es un string, ej: "20"
edad = int(entrada)                   # Lo convertimos a entero
```

Forma abreviada (lo más común)

```python
edad = int(input("Ingrese su edad: "))
```

### La función eval():

![](img/cap02_img01.png)

Es probable que, al buscar soluciones en foros de internet o a la IA, te encuentres con la función eval(). Esta función evalúa una cadena de texto como si fuera código Python ejecutable, lo que a simple vista parece una "solución mágica" para evitar usar int() o float() al leer datos numéricos. Sin embargo, su uso está **ESTRICTAMENTE PROHIBIDO** en esta materia y en el desarrollo profesional seguro.

eval() representa un **agujero de seguridad crítico** (conocido como **inyección de código**): si un usuario ingresa una instrucción maliciosa o destructiva en lugar de un número simple, el programa la ejecutará sin dudarlo. La conversión explícita de tipos garantiza que el programa solo procese datos, nunca comandos ocultos.

## Expresiones Aritméticas y Operadores

Los operadores en Python son muy similares a los de C, pero con tres adiciones muy importantes que reemplazan librerías externas o bucles.

### Operadores básicos (Idénticos a C):

Suma			+

Resta			-

Multiplicación		*

### La División (¡CUIDADO AQUÍ!):

/ (División real): **Siempre devuelve un número flotante**, sin importar si los números son enteros.

```python
resultado = 10 / 2
# En C esto daría 5. En Python da 5.0 (float)
```

// (División entera o "Floor division"): Descarta la parte decimal.

A diferencia de C, redondea hacia abajo (hacia −∞), no hacia cero. Con números positivos el resultado es el mismo, con negativos no.

```python
resultado = 10 // 3  # Devuelve 3
```

## Operadores nuevos en Python sin import:

**\*\* (Potenciación):** Eleva un número a otro. En C requería la librería **math.h** o un bucle for.

```python
cuadrado = 5 ** 2   # Devuelve 25
cubo = 3 ** 3       # Devuelve 27
```

**% (Módulo):** Igual que en C, devuelve el resto de la división entera. Muy útil para saber si un número es par o impar.

## Precedencia de operadores:

Python respeta las mismas reglas matemáticas y de C: PEMDAS.

Paréntesis  ➡

Potenciación  ➡

Multiplicación, División, División Entera, Módulo ➡

Suma y Resta

También existe para los conectores lógicos:

not ➡ and ➡ or

## El Shell de Python (REPL): Tu Laboratorio de Pruebas

Antes de escribir programas completos en un archivo .py, es fundamental entender el entorno interactivo de Python, conocido como **REPL (Read-Eval-Print Loop).**

Si abrís la terminal y escribís python (o python3.13 en Linux, si instalaste con deadsnakes, dentro de un entorno virtual activado, alcanza con python), verás que aparece un prompt con tres símbolos mayores >>>. Esto no es un editor de texto, es una calculadora y un laboratorio vivo.

```
PS C:\Users > python
>>>
```

### ¿Para qué sirve el Shell?

Para hacer cálculos rápidos. Coloca la operación y presiona ENTER.

```
>>> 150 * 0.21
31.5
```

Para probar cómo funcionan las conversiones antes de escribirlas en el código:

```
>>> int("10") + 5
15
```

### Para consultar métodos: ipython

Podés usar la Python Interactive Window de VSCode. Lo podes instalar con:

```
PS C:\Users > pip install ipython
```

Debería activarse con **ipython**:

```
PS C:\Users > ipython
In [1]:
```

### ¿Cómo usarlo?

Si tenés un texto y no sabés qué se le puede hacer, podés definir una variable y guardar "hola". Luego llamas a la variable, no te olvides de agregarle un punto, y apretás la tecla Tab. Aparecerá una lista con todas las funciones de texto disponibles.

```
In [1]: texto = "hola"
In [2]: texto.
capitalize()		encode()       	format()   		isalpha()
isidentifier()	isspace()      	ljust()		partition()
rfind()         	casefold()		endswith()		format_map()
isascii()		islower()		istitle()      	lower()
removeprefix()	rindex()        	center()		expandtabs()
index()        	isdecimal()		isnumeric()		isupper()
lstrip()		removesuffix()	rjust()        	count()
find()			isalnum()      	isdigit()		isprintable()
join()         	maketrans()		replace()		rpartition()
```

Con el correr de los ejercicios vamos usando algunas de estas funciones.

### Regla de oro del Shell:

Todo lo que escriban ahí se ejecuta al instante, pero **se pierde al cerrar la ventana**. El shell se usa para experimentar, los archivos .py en VSCode se usan para guardar programas.
