# Proyecto Integrador — Banco

## Programación 2

El **Proyecto Banco** es el primer proyecto integrador de Programación 2.

A lo largo de **5 iteraciones semanales** construiremos progresivamente un
sistema bancario utilizando los conceptos de Programación Orientada a Objetos
trabajados durante la materia.

El proyecto comienza deliberadamente con una solución muy sencilla. En cada
iteración aparecerán nuevos problemas y utilizaremos los conceptos aprendidos
para hacer evolucionar el sistema.

---

## Objetivo

El objetivo no es solamente llegar a un programa terminado.

Durante el proyecto cada estudiante deberá:

- desarrollar personalmente cada iteración completa;
- utilizar Git para registrar la evolución de su trabajo;
- trabajar con ramas;
- realizar commits frecuentes y descriptivos;
- publicar su trabajo en GitHub;
- comparar su solución con las de sus compañeros;
- participar en revisiones mediante Pull Requests;
- discutir decisiones de diseño;
- participar en la construcción de la solución integrada del grupo.

---

## Organización de los grupos

Los grupos estarán formados por **3 o 4 integrantes**.

Todos los grupos desarrollarán **el mismo Proyecto Banco**, pero cada grupo
trabajará en un repositorio privado independiente.

De esta manera:

- todos parten del mismo problema;
- todos tienen los mismos objetivos;
- todos disponen del mismo tiempo;
- cada grupo construye su propia solución;
- un grupo no puede consultar el código de los demás grupos.

---

## Regla fundamental

Durante las cinco iteraciones iniciales **no se divide el programa entre los
integrantes**.

No trabajaremos de esta manera:

```text
Integrante A → una clase
Integrante B → otra clase
Integrante C → validaciones
Integrante D → pruebas
```

Cada integrante deberá realizar **la iteración completa** en su propia rama:

```text
Integrante A → iteración completa
Integrante B → iteración completa
Integrante C → iteración completa
Integrante D → iteración completa
```

El objetivo es que todos atraviesen personalmente los mismos problemas y
apliquen los mismos conceptos de Programación Orientada a Objetos.

---

## Forma de trabajo de cada iteración

Cada semana se utilizará el siguiente ciclo:

```text
                 main
                  │
        ┌─────────┼─────────┐
        ↓         ↓         ↓
    alumno A   alumno B   alumno C
        │         │         │
        └─────────┼─────────┘
                  ↓
        comparación y revisión
                  ↓
       integración de la semana
                  ↓
           Pull Request
                  ↓
             revisión
                  ↓
                 main
```

En grupos de cuatro habrá cuatro ramas individuales.

---

## Ramas individuales

Cada estudiante creará una rama para la iteración.

Por ejemplo:

```text
iteracion-01/juan-perez
iteracion-01/ana-gomez
iteracion-01/pedro-lopez
```

Cada una deberá contener la solución completa desarrollada por ese
estudiante.

---

## Integración

Después de finalizar el trabajo individual, el grupo comparará las distintas
soluciones.

La versión grupal se construirá en una rama como:

```text
integracion/iteracion-01
```

La integración **no consiste simplemente en elegir el código de uno de los
integrantes**.

El grupo deberá analizar las soluciones, discutir las diferencias y construir
una versión que todos puedan comprender y explicar.

---

## Líder de integración

En cada iteración habrá un **líder de integración**.

El rol será rotativo.

El líder será responsable de:

- coordinar la revisión de las soluciones individuales;
- revisar los Pull Requests;
- solicitar correcciones cuando corresponda;
- coordinar la construcción de la solución integrada;
- verificar el funcionamiento de la versión grupal;
- abrir el Pull Request final de la iteración.

Ser líder no significa realizar el trabajo de los demás ni decidir
unilateralmente qué solución utilizar.

---

## Iteraciones

El proyecto se desarrolla durante cinco semanas. Cada iteración incorpora
solamente los conceptos trabajados hasta ese momento en la materia y parte de la
versión integrada de la semana anterior.

### Iteración 1 — Clases y objetos

[Ver consigna de la Iteración 1](ITERACION_01.md)

Modela una **cuenta bancaria básica** (`Cuenta`) que se pueda crear, depositar,
extraer y mostrar. La versión es deliberadamente incompleta: no hay validaciones
y se prueban también las situaciones incorrectas (depósito negativo, extracción
sin fondos, datos vacíos, modificación directa del saldo).

Conceptos principales:

- clases, objetos, atributos y métodos;
- `self`, `__init__`, `__str__`;
- parámetros y parámetros con valor por defecto;
- el bloque `if __name__ == "__main__":` como escenario de prueba.

### Iteración 2 — Encapsulamiento y validación

[Ver consigna de la Iteración 2](ITERACION_02.md)

Aparece la clase `Persona` y la `Cuenta` **tiene un** titular `Persona`
(composición). Las entidades ya **no pueden nacer con un estado inválido**: los
atributos se encapsulan, se exponen con `@property` de solo lectura y los datos
incorrectos cortan con una excepción.

Conceptos principales:

- encapsulamiento con doble guion bajo y *name mangling*;
- `@property` sin setters (lectura controlada);
- composición entre objetos;
- excepciones estándar (`ValueError`, `TypeError`);
- módulo aparte `validaciones.py` con funciones reutilizables;
- `lambda` para diferir la ejecución de cada caso inválido;
- `.gitignore`.

### Iteración 3 — Herencia y polimorfismo

[Ver consigna de la Iteración 3](ITERACION_03.md) ·
[Contrato TDD](TDD_ITERACION_03.md) ·
[Guía de tests](GUIA_TESTS_ITERACION_03.md)

Las clases genéricas se parten en **tipos especializados**: `Persona` base con
`PersonaFisica` y `PersonaJuridica`; `Cuenta` base con `CuentaAhorro` y
`CuentaCorriente`. Cada subclase agrega solo lo que tiene de distinto, sin
duplicar código.

Conceptos principales:

- herencia simple y `super()` (en el constructor y en métodos sobrescritos);
- sobrescritura de métodos y polimorfismo (`resumen()`, `identificacion`);
- atributos de clase vs. de instancia;
- `isinstance()` / `issubclass()`;
- validaciones nuevas: CUIT con dígito verificador, edad, tasa, límite;
- **`pytest` se empieza a ejecutar**: el `test.py` de la cátedra se corre y debe
  pasar, y cada estudiante escribe sus propios tests.

### Iteración 4 — Sistema, movimientos y excepciones propias

[Ver consigna de la Iteración 4](ITERACION_04.md) ·
[Contrato TDD](TDD_ITERACION_04.md) ·
[Guía de tests](GUIA_TESTS_ITERACION_04.md)

Es la iteración más grande. Aparecen la clase `Movimiento` (historial con fecha,
tipo, monto y saldo posterior), la clase `Banco` (ABM de cuentas y generación de
**CBU**), la transferencia **atómica** entre cuentas, la **baja lógica** y una
jerarquía de errores propia. El proyecto se reorganiza en varios módulos.

Conceptos principales:

- excepciones personalizadas y jerarquías de excepciones;
- herencia múltiple aplicada a los errores (`ValueError` por compatibilidad);
- `raise ... from ...`, `try` / `except` / `else` / `finally`;
- colecciones de objetos (`list` para el historial, `dict` como índice);
- diccionario como despachador de operaciones;
- `@classmethod` / `@staticmethod`, `__len__` / `__contains__` / `__iter__`;
- `datetime` con zona horaria, dígitos verificadores del CBU;
- separación entre lógica de negocio e interfaz (`main.py` con el menú);
- `pytest` con carpeta `tests/`, `conftest.py` y cobertura.

### Iteración 5 — Abstracción y principios de diseño (final)

[Ver consigna de la Iteración 5](ITERACION_05.md) ·
[Contrato TDD](TDD_ITERACION_05.md) ·
[Guía de tests](GUIA_TESTS_ITERACION_05.md)

No agrega funcionalidad importante: **mejora el diseño**. `Cuenta` y `Persona`
pasan a ser abstractas, `extraer()` se escribe una sola vez como método
plantilla, aparece `CuentaSueldo` **sin tocar el código existente** (OCP),
`Movimiento` pasa a `@dataclass(frozen=True)` y `Banco` delega el almacenamiento
en un `RepositorioCuentas` inyectado (DIP). Deja el sistema listo para el
próximo proyecto integrador con Django.

Conceptos principales:

- clases abstractas con `abc.ABC` y `@abstractmethod`, property abstracta;
- método plantilla;
- `@dataclass`, `frozen=True`, `field(default_factory=...)`, `__post_init__`;
- type hints en toda la jerarquía (`Optional`, `TYPE_CHECKING`);
- inyección de dependencias por constructor;
- principios **OCP**, **LSP** y **DIP**;
- `assert` como verificación ejecutable de invariantes de diseño;
- `README.md` del grupo para un lector externo.

---

## Evolución del proyecto

Cada iteración parte de la versión integrada de la semana anterior:

```text
Iteración 1
     ↓
    main
     ↓
Iteración 2
     ↓
    main
     ↓
Iteración 3
     ↓
    main
     ↓
Iteración 4
     ↓
    main
     ↓
Iteración 5
     ↓
Proyecto Banco
```

Por esta razón es importante respetar los límites de cada consigna.

No se busca resolver anticipadamente problemas correspondientes a contenidos
que todavía no fueron trabajados.

---

## Repositorios

Este repositorio público contiene las **consignas y documentación común** del
Proyecto Banco.

El código de los estudiantes se desarrolla en repositorios privados
independientes para cada grupo.

El repositorio privado será utilizado para registrar todo el proceso de
trabajo:

```text
código
↓
commits
↓
ramas
↓
Pull Requests
↓
revisión
↓
integración
```

---

## Resultado esperado

Al finalizar las cinco iteraciones no buscamos solamente tener un sistema
bancario funcionando.

Cada estudiante deberá poder decir:

> Implementé cada etapa del proyecto, comparé mi solución con otras,
> participé en revisiones, discutí decisiones de diseño y colaboré en la
> construcción de la versión integrada de mi grupo.
