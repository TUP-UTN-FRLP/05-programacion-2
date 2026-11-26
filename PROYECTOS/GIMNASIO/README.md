<<<<<<< HEAD
Iniciar el proyecto
--Descargar entorno virtual--
python -m venv .venv
--Activar entorno virtual--
.venv\Scripts\Activate

Tecnologias utlizadas -> Como descargarla con entorno virtual Activo
-Django -> pip install django
-Django -> pip install django pillow
=======
# /TUP-UTN-FRLP

Organización general de la carrera **TECNICATURA UNIVERSITARIA DE
PROGRAMACIÓN**\
Director: Ing. Sergio ANTONINI\
<antonini@frlp.utn.edu.ar>

## /05-programacion-2

Materia **Programación 2**, segundo cuatrimestre\
Docente: Sergio Adrián MALDONADO\
<smaldonado@frlp.utn.edu.ar>\
Telegram: <https://t.me/pincha_lp>

Repositorio de códigos, manuales y proyectos de la materia
**PROGRAMACIÓN 2** de la **TECNICATURA UNIVERSITARIA DE PROGRAMACIÓN -
FACULTAD REGIONAL LA PLATA - UNIVERSIDAD TECNOLÓGICA NACIONAL -
REPÚBLICA ARGENTINA**.

## Metodología de trabajo

Git y GitHub forman parte de la metodología de la materia. No se
utilizarán solamente para entregar un trabajo terminado: permitirán
registrar el proceso de desarrollo, trabajar con ramas, realizar
commits, comparar soluciones, integrar código y utilizar Pull Requests.

Durante los proyectos, GitHub será también una herramienta para observar
la evolución del trabajo individual y grupal.

La explicación detallada se encuentra en
[METODOLOGIA_DE_TRABAJO.md](METODOLOGIA_DE_TRABAJO.md).

## Grupos de trabajo

Los proyectos se realizarán en grupos de **3 o 4 estudiantes, ni menos
ni más**. Las comisiones participantes son **TUP11** y **TUP13**.

La conformación de los grupos se registra en [GRUPOS.md](GRUPOS.md).

Cada grupo tendrá un repositorio privado independiente para desarrollar
sus proyectos. Los integrantes de un grupo podrán trabajar y revisar el
código de sus compañeros, pero no podrán consultar las soluciones de los
demás grupos.

## Proyecto Integrador --- Banco

El primer proyecto integrador de la materia será el **Proyecto Banco**.

Todos los grupos recibirán el mismo problema y lo desarrollarán durante
**5 iteraciones semanales**. El sistema evolucionará progresivamente a
medida que se incorporen nuevos conceptos de Programación Orientada a
Objetos.

Las consignas y documentación del Proyecto Banco se encuentran en:

- [Proyecto Banco](PROYECTOS/BANCO/README.md)
- [Iteración 1 — Clases y objetos](PROYECTOS/BANCO/ITERACION_01.md)

Las siguientes iteraciones se publicarán progresivamente a medida que
avancemos con los contenidos de la materia.

## Regla fundamental de las primeras cinco iteraciones

Durante estas cinco iteraciones el objetivo principal es que **todos los
integrantes recorran personalmente los mismos problemas de Programación
Orientada a Objetos**.

Por esta razón, el trabajo no se dividirá inicialmente en
funcionalidades diferentes.

No trabajaremos de esta manera:

``` text
Integrante A → una parte del programa
Integrante B → otra parte del programa
Integrante C → otra parte del programa
```

Cada integrante deberá desarrollar **la iteración completa** en su
propia rama:

``` text
Integrante A → iteración completa
Integrante B → iteración completa
Integrante C → iteración completa
Integrante D → iteración completa
```

De esta manera, todos deberán escribir, probar y comprender el código
correspondiente a cada etapa del proyecto.

## Flujo de trabajo de una iteración

Cada integrante partirá de la versión integrada de `main` y desarrollará
su solución en una rama individual.

Ejemplo para un grupo de cuatro integrantes:

``` text
main
│
├── iteracion-01/juan-perez
├── iteracion-01/ana-gomez
├── iteracion-01/pedro-lopez
└── iteracion-01/maria-diaz
```

Durante el desarrollo cada estudiante deberá publicar avances mediante
commits que permitan observar la evolución de su solución.

Finalizada la etapa individual:

1. cada integrante abrirá un Pull Request hacia la rama de integración;
2. el grupo comparará las distintas soluciones;
3. se discutirán las decisiones de diseño;
4. se realizarán las correcciones necesarias;
5. se construirá una versión integrada que todos puedan explicar.

La rama grupal tendrá el formato:

``` text
integracion/iteracion-01
```

El flujo general será:

``` text
ramas individuales
        │
        ├── Pull Requests
        │
        ↓
comparación y revisión
        │
        ↓
integracion/iteracion-01
        │
        ├── Pull Request
        ↓
       main
```

## Líder de integración

En cada iteración uno de los integrantes será el **líder de
integración**.

El rol será rotativo.

El líder tendrá como responsabilidades:

- coordinar la revisión de los Pull Requests individuales;
- solicitar correcciones cuando corresponda;
- coordinar la comparación de las soluciones;
- conducir la construcción de la versión integrada;
- verificar que la versión grupal funcione;
- abrir el Pull Request final hacia `main`.

Ser líder no significa realizar el trabajo de los demás ni decidir
unilateralmente qué solución utilizar.

Todos los integrantes deben participar de la integración y comprender la
versión final.

## Revisión docente

La versión integrada de cada semana llegará a `main` mediante un Pull
Request.

Ese Pull Request será revisado por la cátedra antes de incorporar la
iteración como nueva versión oficial del proyecto.

De esta manera podremos observar tanto:

- el trabajo individual;
- la evolución registrada en los commits;
- las distintas soluciones;
- la revisión entre compañeros;
- el proceso de integración;
- el resultado grupal.

## Iteraciones del Proyecto Banco

### Iteración 1 --- Clases y objetos

[Ver consigna de la Iteración 1](PROYECTOS/BANCO/ITERACION_01.md)

Conceptos principales:

- clases;
- objetos;
- atributos;
- métodos;
- `self`;
- `__init__`;
- `__str__`;
- parámetros;
- parámetros con valores por defecto.

### Iteración 2

La consigna será publicada al comenzar la segunda iteración.

### Iteración 3

La consigna será publicada al comenzar la tercera iteración.

### Iteración 4

La consigna será publicada al comenzar la cuarta iteración.

### Iteración 5

La consigna será publicada al comenzar la quinta iteración.

Cada iteración partirá de la versión integrada de la anterior:

``` text
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

Por esta razón, es importante respetar el alcance de cada consigna y no
resolver anticipadamente problemas correspondientes a contenidos que
todavía no fueron trabajados.

## Objetivo del proceso

Al finalizar las cinco iteraciones no buscamos solamente obtener un
programa funcionando.

Cada estudiante deberá haber:

- implementado personalmente cada etapa;
- registrado su evolución mediante commits;
- utilizado ramas;
- creado y revisado Pull Requests;
- comparado diferentes soluciones;
- discutido decisiones de diseño;
- participado en la integración grupal;
- ejercido el rol de líder de integración cuando corresponda;
- comprendido y podido explicar la versión final del grupo.

## Organización del repositorio

El repositorio público de la materia queda organizado conceptualmente de
la siguiente manera:

``` text
05-programacion-2/
│
├── MATERIAL/
│   └── MANUAL/
│
├── PROYECTOS/
│   └── BANCO/
│       ├── README.md
│       ├── ITERACION_01.md
│       ├── ITERACION_02.md
│       ├── ITERACION_03.md
│       ├── ITERACION_04.md
│       └── ITERACION_05.md
│
├── GRUPOS.md
├── METODOLOGIA_DE_TRABAJO.md
└── README.md
```

El repositorio general contiene el material, las consignas y la
documentación común.

El código desarrollado por cada grupo se mantendrá en repositorios
privados independientes administrados por la cátedra.

## /MATERIAL

Se guardan todos los materiales necesarios para el seguimiento de las
clases.

## /MANUAL

Dentro de `MATERIAL/MANUAL` encontrarás el **MANUAL DE PROGRAMACIÓN 2**,
donde:

1. repasamos Programación 1 pasando de la sintaxis de C a Python;
2. desarrollamos Programación Orientada a Objetos;
3. aprendemos a usar el framework Django;
4. explicamos Docker y deploy;
5. nos adentramos en el uso de agentes generadores de código.

## Estado del manual

### Último capítulo actualizado: 9

Se está trabajando en el capítulo 10:
**POO_Encapsulamiento_y_validacion**.
>>>>>>> upstream/main
