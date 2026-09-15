# Guía de Commits y Pull Requests --- Proyecto Integrador Banco

Esta guía complementa a [`GUIA_GIT.md`](GUIA_GIT.md).

Mientras que `GUIA_GIT.md` explica el flujo de trabajo (ramas,
integración, Pull Requests entre ramas), esta guía se enfoca en algo
más puntual: **cómo armar buenos commits** y **cómo escribir buenos
mensajes**, tanto de commit como de Pull Request.

Está pensada para estudiantes que recién comienzan a trabajar con Git.

------------------------------------------------------------------------

## 1. Sugerencias para hacer buenos commits

### 1.1 Commits atómicos

Un commit **atómico** registra un solo cambio lógico y coherente.

No es lo mismo:

``` text
Agrega validacion de CBU
```

que:

``` text
Agrega validacion de CBU, corrige un typo en README y empieza el metodo transferir
```

El segundo mezcla tres cosas distintas en un solo commit. Si algo falla
o hay que revertirlo, se termina revirtiendo también lo que funcionaba
bien.

> **Por qué:** un commit atómico se puede leer, revisar, revertir o
> citar (`git blame`) de forma aislada. Si el commit mezcla varios
> cambios, esa trazabilidad se pierde.

Preguntate antes de comitear: *"¿Puedo describir este commit en una
sola frase, sin usar la palabra 'y'?"* Si no podés, probablemente
convenga dividirlo en más de un commit.

Esto no significa que cada commit deba ser mínimo (por ejemplo, una
sola línea). Significa que debe ser **coherente**: todo lo que está
adentro pertenece a la misma idea.

### 1.2 Correr el suite de pruebas antes de stagear y comitear

Antes de hacer `git add` y `git commit`, corré las pruebas:

``` bash
python -m pytest -q
```

Si algo falla, no comitees ese estado (salvo que el commit sea,
justamente, para dejar registrado un test que todavía falla como parte
del ciclo TDD, algo que se explica en las guías de cada iteración).

> **Por qué:** un commit representa un punto del historial al que
> alguien puede volver (`git checkout`, `git revert`, `git bisect`).
> Si el historial está lleno de commits rotos, esas herramientas dejan
> de ser confiables. Correr las pruebas antes de comitear es más
> barato que descubrir el problema varios commits después.

Un buen hábito, encadenando con lo que ya recomienda `GUIA_GIT.md`:

``` bash
python -m pytest -q
git status
git add archivo.py
git commit -m "Mensaje del commit"
```

### 1.3 Revisar el diff antes de stagear

Antes de `git add`, mirá qué cambiaste:

``` bash
git diff
```

Y después de agregar al área de preparación, antes de comitear:

``` bash
git diff --staged
```

> **Por qué:** es habitual dejar código de prueba (`print()` de
> depuración, comentarios temporales, cambios accidentales en otro
> archivo) sin darse cuenta. Revisar el diff es la última oportunidad
> de detectarlo antes de que quede en el historial.

### 1.4 No comitear archivos generados

Evitá agregar al repositorio carpetas y archivos que se generan
automáticamente, como:

``` text
__pycache__/
*.pyc
.pytest_cache/
.vscode/
```

Si el repositorio no tiene un archivo `.gitignore` que ya los
excluya, prestá atención a `git status` antes de `git add .` para no
incluirlos por error.

### 1.5 Preferir varios commits chicos a uno gigante

No es necesario (ni deseable) trabajar toda una sesión y recién al
final hacer un único commit con todo. Como ya indica `GUIA_GIT.md`,
la cátedra quiere poder observar la **evolución** del desarrollo.

Commitear seguido, en puntos donde el código compila y las pruebas
relacionadas pasan, tiene ventajas concretas:

- si algo se rompe más adelante, `git bisect` permite encontrar en qué
  commit exacto empezó el problema;
- revertir un cambio puntual (`git revert`) es simple y seguro;
- el historial cuenta una historia entendible de cómo se construyó la
  solución.

### 1.6 Un commit, un mensaje que explique el "qué" y, si hace falta, el "por qué"

El título del commit dice **qué** cambió. Si la razón no es obvia,
agregá una descripción debajo explicando **por qué**:

``` bash
git commit -m "Corrige redondeo del interes en cierre de periodo" -m "El calculo usaba float y arrastraba error de precision en montos grandes; se cambia a Decimal."
```

No hace falta descripción larga en cada commit. Alcanza cuando el
motivo no se explica solo con el título.

### 1.7 No reescribir historial ya publicado

Evitá `git commit --amend`, `git rebase` o `git push --force` sobre
commits que ya hiciste `push` y que otros compañeros pueden haber
descargado. Si necesitás corregir algo, hacé un commit nuevo que
corrija lo anterior (como ya indica la sección 27 y 28 de
`GUIA_GIT.md`).

------------------------------------------------------------------------

## 2. Estándar de mensajes de commit por tipo

Usaremos una convención simple, basada en
[Conventional Commits](https://www.conventionalcommits.org/), adaptada
para este proyecto. El formato del título es:

``` text
tipo: descripción breve en presente
```

Ejemplos:

``` text
feat: agrega transferencia entre cuentas
fix: corrige saldo negativo permitido en cuenta ahorro
refactor: extrae validacion de CBU a un modulo aparte
docs: actualiza README con instrucciones de instalacion
test: agrega pruebas de cierre de periodo para cuenta sueldo
```

> **Nota:** en este proyecto es válido comitear en español, como ya
> muestra `GUIA_GIT.md` con mensajes como `"Agrega clase Cuenta"`. Lo
> importante no es el idioma, sino usar el prefijo correcto y una
> descripción clara. Lo que sí debe mantenerse siempre en el mismo
> idioma es el prefijo del tipo (`feat`, `fix`, etc.), que se deja en
> inglés porque es el estándar que vas a encontrar en cualquier
> proyecto profesional.

### Tabla de tipos

| Tipo       | Cuándo usarlo                                                            | Ejemplo                                                            |
|------------|--------------------------------------------------------------------------|--------------------------------------------------------------------|
| `feat`     | Agrega una funcionalidad nueva que antes no existía.                     | `feat: agrega CuentaSueldo con retencion sobre el excedente`       |
| `fix`      | Corrige un comportamiento incorrecto (un bug).                           | `fix: evita que se cierre una cuenta con saldo distinto de cero`   |
| `refactor` | Reorganiza o mejora código existente sin cambiar su comportamiento.      | `refactor: mueve las excepciones a banco/errores.py`               |
| `test`     | Agrega o modifica pruebas, sin tocar el código de producción.            | `test: agrega casos de descubierto en cuenta corriente`            |
| `docs`     | Cambios en documentación (README, guías, comentarios de consigna).       | `docs: agrega ejemplos de uso al README`                           |
| `style`    | Cambios de formato que no afectan el comportamiento (espacios, nombres). | `style: aplica formato consistente en banco.py`                    |
| `chore`    | Tareas de mantenimiento: configuración, dependencias, `.gitignore`.      | `chore: agrega __pycache__ al gitignore`                           |
| `perf`     | Mejora el rendimiento sin cambiar el comportamiento observable.          | `perf: evita recorrer el historial dos veces en cierre_de_periodo` |

> **Nota:** no confundas `style` con `refactor`. `style` son cambios
> puramente formales (espacios, nombres, orden de imports) que no
> tocan la estructura del código. `refactor` sí puede cambiar la
> estructura interna (mover código a otro módulo, extraer una
> función), siempre que el comportamiento observable sea el mismo.

### Cómo elegir el tipo correcto

Preguntas que ayudan a decidir:

- **¿Agregué algo que no existía?** → `feat`
- **¿Estaba roto y ahora funciona bien?** → `fix`
- **¿El comportamiento es exactamente el mismo, pero el código está
  mejor organizado?** → `refactor`
- **¿Solo toqué pruebas?** → `test`
- **¿Solo toqué texto explicativo, no código?** → `docs`

> **Nota:** si un commit mezcla, por ejemplo, un `fix` y un `refactor`,
> es una buena señal de que conviene dividirlo en dos commits (ver
> sección 1.1, commits atómicos).

------------------------------------------------------------------------

## 3. Estándar de títulos y mensajes de Pull Request

`GUIA_GIT.md` (secciones 18 a 20) ya explica **cuándo** y **hacia
dónde** abrir cada Pull Request. Esta sección detalla **cómo
titularlos y describirlos**.

### 3.1 Título del PR

**Para un PR individual** (alumno → integración), usar el formato que
ya sugiere `GUIA_GIT.md`:

``` text
Iteracion 03 - Juan Perez
```

**Para un PR de integración** (integración → `main`), usar un formato
similar al de los commits, describiendo el resultado grupal:

``` text
feat: integra Iteracion 03 - Cuentas y movimientos
```

**Para un PR de corrección** (cuando el docente o un compañero pide
cambios sobre un PR ya abierto), no se abre un PR nuevo — como ya
indica `GUIA_GIT.md`, los commits se agregan al mismo PR existente.

### 3.2 Cuerpo del PR

Una descripción de PR útil, breve y concreta, responde estas
preguntas:

``` text
## Qué implementa
Breve resumen de la funcionalidad o el cambio.

## Cómo lo probé
Qué pruebas corriste (por ejemplo: `python -m pytest -q`, y si agregaste
pruebas propias en `tests/`).

## Decisiones y limitaciones
Cualquier decisión de diseño que quieras que el grupo revise, o algo
que sabés que falta.
```

Ejemplo concreto para un PR individual de la Iteración 3:

``` text
## Qué implementa
Agrega CuentaAhorro y CuentaCorriente con validacion de saldo inicial
en 0 (toda carga se hace por `depositar`).

## Cómo lo probé
python -m pytest -q -> 14 passed
Agregué casos propios en tests/test_cuentas.py para el descubierto.

## Decisiones y limitaciones
Todavía no implementé cierre_de_periodo, queda para revisar con el grupo.
```

No hace falta un informe extenso (esto ya lo aclara `GUIA_GIT.md`):
alcanza con que cualquier compañero pueda entender, en un minuto, qué
cambió y cómo se validó.

> **Nota:** si el PR resuelve exactamente lo que pide una consigna
> (por ejemplo, `ITERACION_03.md`), no hace falta repetir la consigna
> completa en la descripción. Referenciarla alcanza.

------------------------------------------------------------------------

## 4. Resumen rápido

Antes de comitear:

``` bash
python -m pytest -q
git diff
git status
```

Al comitear:

``` bash
git add archivo.py
git commit -m "tipo: descripcion breve en presente"
```

Tipos disponibles: `feat`, `fix`, `refactor`, `test`, `docs`, `style`,
`chore`, `perf`.

Al abrir un Pull Request: título descriptivo + cuerpo con **qué
implementa**, **cómo lo probé** y **decisiones/limitaciones**.

Para todo lo referido a ramas, integración y el flujo completo del
proyecto, ver [`GUIA_GIT.md`](GUIA_GIT.md).
