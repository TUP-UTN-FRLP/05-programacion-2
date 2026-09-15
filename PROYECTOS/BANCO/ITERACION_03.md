# Proyecto Integrador Banco — Iteración 3

## Introducción

Hasta acá el banco tiene una `Cuenta` y una `Persona` **genéricas**: sirven para
todo y no representan bien a nada. Un banco real no trata igual a una caja de
ahorro que a una cuenta corriente, ni a una persona física que a una empresa.

Con lo que sabíamos hasta la Iteración 2, la única forma de representar esas
diferencias sería llenar los métodos de `if tipo == "ahorro"`. En esta
iteración las partimos en **tipos especializados** usando herencia.

La regla de oro de la iteración: **cada subclase agrega o modifica solo lo
necesario, sin duplicar código**.

---

## Qué cambia respecto de la Iteración 2

| Tema | Iteración 2 | Iteración 3 |
| --- | --- | --- |
| Personas | una sola clase `Persona` | `Persona` base + `PersonaFisica` + `PersonaJuridica` |
| Identificación | `dni` en `Persona` | `dni` baja a `PersonaFisica`; `cuit` aparece en `PersonaJuridica` |
| Cuentas | una sola clase `Cuenta` | `Cuenta` base + `CuentaAhorro` + `CuentaCorriente` |
| Reglas de extracción | iguales para todos | las define cada subclase |
| Intereses | no existen | `CuentaAhorro` los liquida |
| Descubierto | no existe | `CuentaCorriente` lo permite hasta un límite |
| Presentación | `__str__` | `__str__` + `resumen()` polimórfico |
| Validaciones | 5 funciones | se agregan `validar_cuit`, `validar_edad`, `validar_tasa` |
| Verificación | leer `test.py` y reproducir a mano | **ejecutar** `test.py` con `pytest` + tests propios |

Todo lo de la Iteración 2 (encapsulamiento, properties de solo lectura,
validaciones que cortan con excepción) **se conserva**. Lo que cambia es que
ahora hay una jerarquía.

---

## Objetivo de la Iteración 3

```text
          Persona                              Cuenta
             │                                    │
     ┌───────┴────────┐                  ┌────────┴────────┐
     ▼                ▼                  ▼                 ▼
PersonaFisica   PersonaJuridica    CuentaAhorro     CuentaCorriente
  (dni, edad)   (cuit, razón           (interés)      (descubierto)
                    social)

     └────────────── es titular de ──────────────┘
```

Dos relaciones distintas conviviendo:

- **herencia** (`es un`): una `CuentaAhorro` **es una** `Cuenta`;
- **composición** (`tiene un`): una cuenta **tiene un** titular.

Poder explicar la diferencia es parte de la entrega.

---

## Conceptos que se trabajan

- herencia simple y reutilización de código;
- `super()` en el constructor y dentro de un método sobrescrito;
- sobrescritura de métodos (*override*);
- polimorfismo: el mismo mensaje, distinta respuesta según el objeto;
- atributos de clase vs. atributos de instancia;
- `isinstance()` e `issubclass()`;
- properties heredadas y properties nuevas;
- una lista mixta recorrida con un solo `for`.

---

## Importante: qué NO buscamos todavía

En esta iteración **no** se debe implementar:

- clases abstractas (`ABC`, `@abstractmethod`);
- `@dataclass` ni type hints sistemáticos;
- excepciones personalizadas (se siguen usando `ValueError` y `TypeError`);
- registro de movimientos ni historial;
- clase `Banco`, ABM, búsquedas ni CBU;
- transferencias entre cuentas;
- división del proyecto en varios archivos de dominio;
- menú, `input()`, persistencia, Django o frontend.

> **Novedad de la iteración: `pytest` se empieza a ejecutar.** El
> `test.py` de la cátedra deja de leerse y pasa a correrse; que pase es
> condición de entrega. Además cada estudiante escribe sus propios
> tests. La organización en varios archivos de test con `conftest.py`
> llega recién en la Iteración 4; acá alcanza con `test.py` + un archivo
> propio. Detalle en la sección 5 y en `GUIA_TESTS_ITERACION_03.md`.

> **Sobre `Persona` y `Cuenta` genéricas:** al terminar esta iteración va a ser
> posible escribir `Cuenta("12345678901234", titular)` y crear una cuenta que no
> es de ningún tipo. Eso es incorrecto desde el modelo, pero **no hay que
> impedirlo todavía**: se resuelve en la Iteración 5 con clases abstractas. Es
> el mismo criterio de la Iteración 1: observar la limitación antes de tener la
> herramienta.

---

## Organización de archivos

```text
banco.py          # todas las clases + escenario en if __name__ == "__main__"
validaciones.py   # se amplía
test.py           # contrato de la cátedra; SE EJECUTA con pytest, NO se modifica
test_propios.py   # tus pruebas (nombre libre, con prefijo test_)
pytest.ini        # config de pytest (necesaria: el archivo se llama test.py)
.gitignore        # + .pytest_cache/ y __pycache__/
```

Se mantiene un solo `banco.py`. La división en módulos —y la carpeta
`tests/` con `conftest.py`— llegan en la Iteración 4, cuando la cantidad
de clases y de pruebas lo justifique.

---

## 1. Jerarquía de personas

### `Persona` (clase base)

Conserva de la Iteración 2 lo que es común a cualquier titular:

```python
Persona(nombre)
```

```text
__nombre     str validado y normalizado
```

Properties: `nombre` y `identificacion`.

`identificacion` en la clase base devuelve el texto que identifica al titular.
Como `Persona` genérica no tiene ninguno, devuelve `"SIN IDENTIFICACION"`.
Cada subclase la sobrescribe.

`__str__` de la base: nombre + identificación.

> **Refactor:** el `dni` deja de estar en `Persona`. Los datos de prueba de la
> Iteración 2 hay que adaptarlos: donde decía `Persona("Ana", "Perez",
> "12345678")` ahora va `PersonaFisica("Ana", "Perez", "12345678", 30)`.

### `PersonaFisica(Persona)`

```python
PersonaFisica(nombre, apellido, dni, edad)
```

Agrega:

```text
__apellido   str validado y normalizado
__dni        str de 7 u 8 dígitos (regla de la Iteración 2)
__edad       int entre 18 y 120
```

- el constructor **debe** delegar el nombre en `super().__init__(nombre)`;
- properties nuevas: `apellido`, `dni`, `edad`, `nombre_completo`
  (`"Apellido, Nombre"`);
- `identificacion` sobrescrita: `"DNI 12345678"`;
- `__str__` sobrescrita, reutilizando la de la base con `super().__str__()`.

Sobre la edad: el titular de una cuenta debe ser mayor de edad. Una edad menor
a 18 → `ValueError`. Una edad `float`, `bool` o `str` → `TypeError`.

### `PersonaJuridica(Persona)`

```python
PersonaJuridica(razon_social, cuit)
```

Agrega:

```text
__cuit   str de 11 dígitos, con dígito verificador válido
```

- la razón social viaja como `nombre` a la clase base, pero se admite un
  conjunto de caracteres más amplio que un nombre de persona: además de letras,
  espacios, `-` y `'`, se permiten dígitos, `.`, `&` y `,`
  (`"Distribuidora S.A."`, `"3M Argentina S.R.L."`). Requiere una validación
  propia: `validar_razon_social`;
- property nueva: `cuit`;
- property `razon_social`: alias de lectura de `nombre`;
- `identificacion` sobrescrita: `"CUIT 30-71234567-1"` (formateado con
  guiones a partir de los 11 dígitos guardados).

#### Cómo se arma el CUIT (y el CUIL) en la Argentina

El CUIT (empresas) y el CUIL (personas físicas en relación de dependencia) se
construyen igual: 11 dígitos, agrupados `XX-XXXXXXXX-X`.

```text
┌────┬──────────────┬───┐
│ 30 │  71234567    │ 1 │
└────┴──────────────┴───┘
  │        │          └─ dígito verificador (se calcula)
  │        └──────────── cuerpo: DNI de la persona, o número asignado
  └───────────────────── prefijo de tipo
```

Prefijos usados:

```text
20 / 23 / 24 / 27   persona física (CUIL / CUIT)
30 / 33 / 34        persona jurídica (CUIT)
```

Para `PersonaJuridica` solo importa que el número tenga 11 dígitos y que el
verificador cierre; el prefijo no se valida (queda como decisión de diseño para
discutir).

#### Dígito verificador del CUIT

Los 10 primeros dígitos son datos; el último se calcula por módulo 11.

```text
1. tomar los 10 primeros dígitos;
2. multiplicarlos, en orden, por los pesos 5 4 3 2 7 6 5 4 3 2;
3. sumar los productos;
4. resto = suma % 11;
5. verificador = 11 - resto;
   si verificador == 11  ->  0
   si verificador == 10  ->  el CUIT es inválido
6. el resultado debe coincidir con el dígito 11.
```

Ejemplo con `30712345671`:

```text
dígitos    3   0   7   1   2   3   4   5   6   7
pesos      5   4   3   2   7   6   5   4   3   2
producto  15   0  21   2  14  18  20  20  18  14   ->  suma = 142

142 % 11 = 10        verificador = 11 - 10 = 1     -> coincide con el dígito 11
```

Un CUIT de 11 dígitos con verificador incorrecto → `ValueError`.

CUIT válidos para probar: `30712345671`, `20123456786`, `27234567891`.
Un CUIT inválido para probar: `30712345670` (el mismo, con el verificador
cambiado).

> Este algoritmo es la primera regla del proyecto que no es un simple chequeo de
> formato: es un cálculo. Va en `validaciones.py`, no dentro de la clase.

---

## 2. Jerarquía de cuentas

### `Cuenta` (clase base)

Es la `Cuenta` de la Iteración 2, con tres cambios:

```python
Cuenta(numero, titular)
```

- `titular` debe ser una `Persona` (cualquier subclase sirve);
- se agrega el método `resumen()`;
- **el constructor ya no recibe saldo.** Toda cuenta nace con `saldo == 0`;
  no existe forma de crearla con fondos.

> **Por qué:** el banco no permite abrir una cuenta que ya tenga plata
> cargada. Ninguna cuenta se crea que no sea con saldo 0. Si el banco
> necesita darle un saldo inicial a una cuenta recién abierta, lo hace
> llamando a `depositar()` justo después de crearla — igual que cualquier
> otro movimiento posterior. Por eso `validar_saldo_inicial` desaparece de
> `validaciones.py`: al no existir el parámetro, no hay nada que validar.

Se conservan sin cambios: número de 14 dígitos, properties de solo lectura,
`depositar()` y `extraer()` con validación.

#### `resumen()`

Devuelve un `str` de varias líneas con el estado de la cuenta. En la clase base:

```text
--- Cuenta 12345678901234 ---
Titular: Perez, Ana (DNI 12345678)
Saldo:   $1300.00
```

Cada subclase lo sobrescribe agregando **su** información, reutilizando la parte
común con `super().resumen()`. No se copia y pega el texto de la base.

#### Atributo de clase

```python
class Cuenta:
    TIPO = "Cuenta"
```

Cada subclase redefine `TIPO`. Usarlo en `resumen()` y en `__str__` en lugar de
escribir el nombre del tipo a mano.

### `CuentaAhorro(Cuenta)`

```python
CuentaAhorro(numero, titular, tasa_interes=0.01)
```

```text
TIPO = "Caja de Ahorro"
__tasa_interes   float entre 0 y 1
```

Reglas:

- **no admite saldo negativo**: `extraer(monto)` sobrescrita, valida el monto
  (delegando en `super()`), y si `monto > saldo` corta con `ValueError` sin
  tocar el saldo;
- `liquidar_interes()`: acredita `saldo * tasa_interes` y devuelve el interés
  acreditado. Con saldo `0` no hace nada y devuelve `0`;
- property `tasa_interes` de solo lectura;
- `resumen()` agrega la tasa y el interés que se acreditaría hoy.

Atributo de clase con el valor por defecto de la tasa:

```python
TASA_POR_DEFECTO = 0.01
```

### `CuentaCorriente(Cuenta)`

```python
CuentaCorriente(numero, titular, limite_descubierto=0)
```

```text
TIPO = "Cuenta Corriente"
__limite_descubierto   numérico >= 0
```

Reglas:

- `extraer(monto)` sobrescrita: permite dejar el saldo negativo mientras
  `saldo - monto >= -limite_descubierto`. Si se pasa → `ValueError` sin tocar el
  saldo;
- property `limite_descubierto` de solo lectura;
- property calculada `saldo_disponible` = `saldo + limite_descubierto`;
- `cobrar_mantenimiento()`: descuenta el costo fijo, incluso si eso deja la
  cuenta en descubierto;
- `resumen()` agrega el límite y el disponible.

Atributo de clase:

```python
COSTO_MANTENIMIENTO = 500.0
```

### Cómo sobrescribir `extraer()` sin duplicar

La validación del monto (`> 0`, numérico) es igual en las dos subclases. No se
repite: se hereda. Un esquema posible:

```python
class CuentaAhorro(Cuenta):
    def extraer(self, monto):
        monto = validar_monto(monto)
        if monto > self.saldo:
            raise ValueError(...)
        return super().extraer(monto)
```

Discutir en grupo si conviene ese esquema o si conviene que la clase base tenga
un método `_puede_extraer(monto)` que cada subclase redefina. Las dos son
válidas en esta iteración; hay que poder defender la elegida.

---

## 3. Ampliación de `validaciones.py`

Se agregan:

```python
validar_razon_social(valor)   # -> str normalizado; admite dígitos . & ,
validar_cuit(valor)           # -> str de 11 dígitos con verificador válido
validar_edad(valor)           # -> int entre 18 y 120
validar_tasa(valor)           # -> float entre 0 y 1
validar_limite(valor)         # -> int/float >= 0
```

Se conservan `validar_nombre`, `validar_dni`, `validar_numero_cuenta` y
`validar_monto` de la Iteración 2. **`validar_saldo_inicial` desaparece**:
como ninguna cuenta admite saldo al crearse, no queda nada que validar ahí
(ver la explicación en la sección de `Cuenta`, más arriba). Mismo criterio
para las que quedan: `TypeError` para el tipo, `ValueError` para el valor,
sin `print()` ni `input()`, sin depender de ninguna clase.

---

## 4. `banco.py`: escenario obligatorio

Dentro de `if __name__ == "__main__":`:

1. crear una `PersonaFisica` y una `PersonaJuridica`;
2. imprimir la `identificacion` de cada una y observar que el mismo nombre de
   property devuelve cosas distintas;
3. crear una `CuentaAhorro` para la persona física y una `CuentaCorriente` para
   la jurídica;
4. operar sobre ambas con depósitos y extracciones válidas;
5. **extraer de la cuenta corriente hasta quedar en negativo** dentro del
   límite, y mostrar que la caja de ahorro no lo permite;
6. liquidar el interés de la caja de ahorro y cobrar el mantenimiento de la
   corriente;
7. recorrer una **lista mixta** y llamar `resumen()` sobre cada elemento;
8. mostrar, capturando la excepción, que fallan:

```python
PersonaFisica("Ana", "Perez", "12345678", 15)          # ValueError (menor)
PersonaJuridica("Distribuidora S.A.", "30712345670")   # ValueError (verificador)
PersonaJuridica("Distribuidora S.A.", 30712345671)     # TypeError
CuentaAhorro("12345678901234", titular, 1.5)           # ValueError (tasa)
CuentaCorriente("12345678901234", titular, -100)       # ValueError (límite)
ahorro.extraer(999999)                                 # ValueError
ahorro.saldo = 99999                                   # AttributeError
```

Se conserva el patrón con `lambda` de la Iteración 2 para diferir cada caso.

### El bucle polimórfico

El punto 7 es el corazón de la iteración:

```python
cuentas = [ahorro, corriente]

for cuenta in cuentas:
    print(cuenta.resumen())
    print()
```

El `for` no pregunta de qué tipo es cada cuenta. Cada objeto responde con su
propia versión de `resumen()`.

**No debe haber ningún `if` que consulte el tipo de cuenta ni de persona en
todo el archivo.** Si aparece un `if isinstance(...)` para decidir qué hacer, la
jerarquía está mal diseñada.

---

## 5. Pruebas con `pytest`

Esta iteración es el primer contacto con la ejecución de tests. La
herramienta y el paso a paso están en `GUIA_TESTS_ITERACION_03.md`; el
contrato de nombres y comportamiento, en `TDD_ITERACION_03.md`. Lo
mínimo:

```bash
python -m pip install pytest
python -m pytest -q
```

- El `test.py` de la cátedra **se ejecuta y debe pasar completo**. No
  se modifica: si algo no pasa, se corrige `banco.py` o
  `validaciones.py`.
- Hace falta un `pytest.ini` en la raíz porque el archivo se llama
  `test.py` a secas y `pytest` por defecto solo descubre `test_*.py`:

  ```ini
  [pytest]
  python_files = test.py test_*.py
  testpaths = .
  addopts = -q
  ```

- Cada estudiante escribe **sus propios tests** en un archivo aparte
  (`test_propios.py` o similar), tomando como molde el `test.py` de la
  **Iteración 2** (`ITERACION-02/test.py`): misma estructura de
  imports, separadores, `@pytest.fixture` en lugar de la función
  `crear_titular()`, `pytest.raises` para los casos que deben fallar y
  `parametrize` para las tablas de datos. La guía tiene una tabla que
  mapea cada caso de la Iteración 2 con su equivalente en la 3.
- Agregar `.pytest_cache/` y `__pycache__/` al `.gitignore`.

---

## 6. Qué debe observarse al finalizar

- ninguna subclase repite una validación que ya hace su clase base;
- todos los constructores de las subclases llaman a `super().__init__(...)`;
- toda cuenta se crea con `saldo == 0`, sin excepción; un saldo inicial se
  carga con `depositar()`, nunca con un parámetro del constructor;
- una `CuentaAhorro` nunca queda con saldo negativo;
- una `CuentaCorriente` puede quedar negativa, pero solo hasta su límite;
- `identificacion` y `resumen()` devuelven cosas distintas según el objeto, con
  el mismo nombre de método;
- una lista mixta se recorre con un solo `for`, sin preguntar tipos;
- `depositar()` está escrito **una sola vez**, en la clase base;
- `Cuenta` y `Persona` genéricas todavía se pueden instanciar: queda anotado
  como limitación para la Iteración 5.

---

## 7. Decisiones de diseño para pensar

### 1. ¿Y si mañana hay `PersonaFisica` con CUIT?

Un monotributista es persona física y tiene CUIT. ¿Dónde iría ese atributo? ¿Se
sube el `cuit` a `Persona` y se baja el `dni`? ¿Qué se rompe en cada caso?

### 2. ¿`resumen()` o `__str__`?

Ya existe `__str__`. ¿Por qué agregar `resumen()` en vez de hacer que `__str__`
devuelva el texto largo? Pista: pensar en `print(lista_de_cuentas)`.

### 3. Sustitución

Cualquier código que reciba una `Cuenta` debe funcionar si le pasan una
`CuentaAhorro`. ¿Se cumple? ¿Qué pasaría si `CuentaAhorro.extraer()` pidiera un
parámetro extra que la base no pide?

### 4. La validación de la tasa

`tasa_interes` se valida entre 0 y 1. ¿Qué pasa si alguien pasa `5` pensando en
"5 %"? ¿Conviene aceptar porcentajes, rechazarlos, o documentar la unidad?

---

## 8. Forma de trabajo individual

Rama:

```text
iteracion-03/nombre-apellido
```

Cada integrante resuelve la iteración completa: las dos jerarquías, las
validaciones nuevas y el escenario.

---

## 9. Commits sugeridos

```text
Refactoriza Persona como clase base
Agrega PersonaFisica con dni y edad
Agrega validacion de CUIT con digito verificador
Agrega PersonaJuridica con cuit y razon social
Agrega resumen y atributo TIPO en Cuenta
Implementa CuentaAhorro con liquidacion de interes
Implementa CuentaCorriente con limite de descubierto
Agrega validaciones de edad tasa y limite
Agrega escenario polimorfico de la iteracion 3
```

---

## 10. Integración grupal

Rama:

```text
integracion/iteracion-03
```

En la comparación el grupo debe discutir, como mínimo:

- si `extraer()` se sobrescribió entera o se apoyó en un método auxiliar;
- dónde quedó ubicado el `dni` y por qué;
- cuánto código quedó duplicado entre las dos subclases de cuenta;
- cómo resolvió cada uno `identificacion`.

El líder de la semana abre el Pull Request final hacia `main`.

---

## Criterio central

La pregunta de esta iteración es:

> ¿Cuánto código hay que escribir para agregar un tipo de cuenta o de persona
> nuevo?

Si la respuesta es "solo lo que ese tipo tiene de distinto", la herencia está
bien usada. Si hay que volver a escribir el constructor entero, no.
