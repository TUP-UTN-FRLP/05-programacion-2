# Git — Parte 2: Fundamentos de uso diario

> **Fuente**
> El libro [Pro Git](https://git-scm.com/book), de Scott Chacon y Ben Straub, está disponible para leer en línea gratis en `git-scm.com`.
> Se distribuye bajo licencia Creative Commons BY-NC-SA 3.0. Las figuras citadas pertenecen al sitio oficial `git-scm.com`.

## Alcance

Esta es la **Parte 2** del apunte. Cubre estos apartados del libro **Pro Git**:

- Obteniendo un repositorio Git
- Guardando cambios en el Repositorio
- Ver el Historial de Confirmaciones
- Deshacer Cosas
- Trabajar con Remotos
- Etiquetado
- Alias de Git
- Resumen

## Objetivo de la parte

Construir el circuito operativo más frecuente en Git: obtener un repositorio, revisar el estado, preparar cambios, confirmar, revisar el historial, corregir errores comunes y sincronizar con remotos.

---

## 1. Obtener un repositorio

Hay dos caminos principales.

### a) Crear un repositorio en una carpeta existente

```bash
git init
```

Transforma la carpeta actual en un repositorio Git. Todavía **no está conectado a ningún servidor**.

### b) Clonar un repositorio existente

```bash
git clone URL_DEL_REPOSITORIO
```

Copia el proyecto y su historial completo, y deja el remoto `origin` ya configurado.

### En la práctica

`init` empieza desde una carpeta local.
`clone` parte de un repositorio que ya existe.

La diferencia importa más de lo que parece: si se empieza con `init`, hay que agregar el remoto a mano antes de poder publicar (sección 5).

---

## 2. Flujo diario mínimo

```bash
git init                       # o: git clone URL
git remote add origin URL      # solo si empezaste con init
git status
git add archivo.py
git commit -m "Mensaje claro"
git push -u origin main        # SOLO la primera vez, con -u
```

De ahí en adelante, publicar es solo `git push`: el `-u` (de *upstream*) asocia la rama local con la remota una única vez, y después Git ya sabe a dónde enviar.

### Secuencia mental

1. `git status` → miro qué pasa.
2. `git add` → preparo cambios.
3. `git commit` → confirmo una instantánea.
4. `git log --oneline` → reviso el historial.
5. `git push` → publico.

![Tres áreas de Git](https://git-scm.com/book/es/v2/images/areas.png)

### En la práctica

Conviene usar `git add archivo.py` (nombrando el archivo) hasta tener el `.gitignore` escrito. Después, `git add .` es cómodo y seguro. Ver la sección 4.

---

## 3. Ver el historial

```bash
git log --oneline
git log --oneline --graph --decorate
git log -3
git show HEAD
```

### Lectura rápida

- `--oneline` resume cada commit en una línea: identificador corto + mensaje.
- `--graph` dibuja las líneas de trabajo. En la Parte 1 no hace falta; en la Parte 3 se vuelve indispensable.
- `--decorate` muestra dónde apuntan las ramas y `HEAD`.

### En la práctica

Confirmar sin revisar nunca el historial deja el commit como un acto ciego. Mirar `git log --oneline` después de cada commit ayuda a entender qué acabás de hacer.

---

## 4. Qué NO se versiona: `.gitignore`

Un archivo de texto llamado `.gitignore`, en la raíz del repositorio, indica qué archivos Git debe ignorar.

Ejemplo típico para un proyecto Python:

```gitignore
__pycache__/
*.pyc
.venv/
env/
.idea/
.vscode/
```

### En la práctica

En un proyecto Python el `.gitignore` es imprescindible: sin él, el primer `git add .` se lleva `__pycache__/` y el entorno virtual completo, y el repositorio queda inservible para revisar cambios.

**Regla práctica:** escribir el `.gitignore` **antes** del primer `git add`.

---

## 5. Trabajar con remotos

Un remoto es una referencia a otro repositorio, por ejemplo uno alojado en GitHub.

### Comandos básicos

```bash
git remote add origin URL      # conectar el repo local con el remoto
git remote -v                  # ver los remotos configurados
git fetch origin               # traer, sin integrar
git pull origin main           # traer e integrar (fetch + merge)
git push -u origin main        # publicar y dejar la rama asociada
```

### Distinción clave

- `fetch` trae información del remoto pero no la integra automáticamente.
- `pull` trae e integra (equivale a `fetch` seguido de `merge`, así que también puede generar conflictos).
- `push` publica commits locales en el remoto.

### En la práctica

Uno de los errores más comunes es pensar que **guardar localmente** y **publicar en GitHub** son lo mismo. No lo son.

El otro error frecuente es más silencioso: hacer `git init`, trabajar, y descubrir recién al final que `git push` falla porque nunca se ejecutó `git remote add origin`.

---

## 6. Deshacer cosas

Git permite corregir, pero no todos los comandos corrigen del mismo modo. La primera pregunta que conviene hacerse es:

> ¿El cambio todavía no fue confirmado o ya forma parte de un commit?

### Comandos frecuentes

```bash
git restore archivo.py            # descartar cambios del directorio de trabajo
git restore --staged archivo.py   # sacar el cambio del área de preparación
git commit --amend                # reemplazar el último commit
```

### Lectura rápida

- `git restore archivo.py` → descarta los cambios no confirmados de ese archivo. **Lo descartado no se recupera.**
- `git restore --staged archivo.py` → lo saca del área de preparación; el contenido del archivo no se toca. Es la operación segura de las tres.
- `git commit --amend` → **no edita** el último commit: lo **reemplaza** por uno nuevo, con otro identificador. Si ese commit ya estaba publicado, el historial local deja de coincidir con el remoto.

**¿Y si borré un archivo que sí estaba confirmado?** No se perdió: está en el último commit. `git restore archivo.py` lo trae de vuelta. Recuperar una versión más vieja (de otro commit) se ve en la Parte 3.

### Nota sobre el libro

La edición en español documenta estas operaciones con la sintaxis anterior:

```bash
git reset HEAD archivo.py         # equivale a git restore --staged
git checkout -- archivo.py        # equivale a git restore
```

Hacen lo mismo. Conviene usar `restore` (separa dos operaciones que `checkout` mezclaba) y conocer la equivalencia, porque es lo que vas a encontrar en el libro, en tutoriales viejos y en la salida de `git status` de versiones anteriores.

### En la práctica

Leer `git status` **antes** de deshacer: la propia salida indica qué comando corresponde en cada caso.

Y una frase que conviene repetir: todo lo confirmado se puede recuperar; lo que nunca se confirmó, no.

---

## 7. Etiquetado

Las etiquetas marcan puntos relevantes del historial, normalmente versiones.

### Comandos básicos

```bash
git tag                                # listar
git tag -a v1.0 -m "Primera versión"   # etiqueta anotada
git push origin v1.0                   # publicarla
git push origin --tags                 # publicar todas
```

### Dos tipos de etiqueta

- **Anotada** (`-a`): se guarda como un objeto completo, con autor, fecha y mensaje. Es la recomendada.
- **Ligera**: es solo un puntero al commit, sin información extra. Se crea sin `-a`, `-s` ni `-m`.

### En la práctica

Sirven para señalar hitos como entregas, parciales, releases o versiones estables.

Un detalle que sorprende siempre: **`git push` no envía etiquetas por defecto**. Hay que empujarlas explícitamente.

---

## 8. Alias de Git

Los alias permiten crear atajos para comandos frecuentes.

### Ejemplos

```bash
git config --global alias.st status
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.sw switch
git config --global alias.lg "log --oneline --graph --decorate"
```

### En la práctica

No son obligatorios para empezar, pero muestran que Git también puede adaptarse al usuario.

Nota: en el libro el ejemplo clásico es `alias.co checkout`. Como este apunte usa `switch` y `restore` en lugar de `checkout`, el alias equivalente es `alias.sw switch`.

---

## 9. Cierre de la parte 2

### Ideas fuerza

- `init` y `clone` no resuelven el mismo problema; con `init` hay que agregar el remoto a mano.
- El flujo diario mínimo es: mirar, preparar, confirmar, revisar y publicar.
- Deshacer depende de **dónde está** el cambio; `--amend` reemplaza, no edita.
- Git local y remoto no se sincronizan solos.
- `.gitignore` decide qué queda afuera del historial.
- Las etiquetas marcan hitos y los alias simplifican el uso repetitivo.

### Práctica corta

Hacela sobre un repositorio **propio** (tuyo o de tu grupo) o sobre un *fork*. Si clonás un repositorio ajeno sin permiso de escritura, el `push` del final falla.

1. Crear un repositorio vacío en GitHub.
2. Clonarlo (o: `git init` + `git remote add origin URL`).
3. Escribir un `.gitignore`.
4. Crear o editar un archivo.
5. Ejecutar `git status`.
6. Preparar el cambio con `git add`.
7. Confirmar con `git commit -m`.
8. Revisar con `git log --oneline`.
9. Publicar con `git push -u origin main`.

---

## 10. Síntesis de comandos — referencia práctica

> Todo esta parte gira alrededor de un mismo circuito: **mirar → preparar → confirmar → revisar → publicar**. Las tablas siguientes están ordenadas por "¿cómo hago para…?".

### Obtener un repositorio

| Quiero… | Comando |
|---|---|
| Crear un repo en una carpeta que ya tengo | `git init` |
| Copiar un repo que ya existe (con su historial) | `git clone URL` |
| Conectar mi repo local con GitHub (solo si usé `init`) | `git remote add origin URL` |
| Ver a qué remotos está conectado | `git remote -v` |

### Circuito diario

| Quiero… | Comando |
|---|---|
| Ver qué cambió | `git status` |
| Preparar un archivo para el próximo commit | `git add archivo.py` |
| Preparar todo lo modificado (con `.gitignore` ya escrito) | `git add .` |
| Confirmar una instantánea | `git commit -m "Mensaje claro"` |
| Publicar por primera vez esta rama | `git push -u origin main` |
| Publicar las veces siguientes | `git push` |

### Revisar el historial

| Quiero… | Comando |
|---|---|
| Historial resumido, una línea por commit | `git log --oneline` |
| Historial con las ramas dibujadas | `git log --oneline --graph --decorate` |
| Solo los últimos 3 commits | `git log -3` |
| El detalle completo del último commit | `git show HEAD` |

### Deshacer (leer `git status` antes)

| Situación | Comando | Ojo |
|---|---|---|
| Cambié un archivo y quiero descartar lo no confirmado | `git restore archivo.py` | lo descartado **no se recupera** |
| Preparé un archivo por error y quiero sacarlo del stage | `git restore --staged archivo.py` | el contenido del archivo no se toca (es la opción segura) |
| Me equivoqué en el mensaje o me olvidé un archivo del último commit | `git commit --amend` | **reemplaza** el commit; no lo uses si ya lo publicaste |

Sintaxis antigua equivalente (aparece en el libro y en tutoriales viejos):
`git reset HEAD archivo.py` = `git restore --staged` · `git checkout -- archivo.py` = `git restore`.

### Sincronizar con el remoto

| Quiero… | Comando |
|---|---|
| Traer info del remoto sin integrarla | `git fetch origin` |
| Traer e integrar (`fetch` + `merge`) | `git pull origin main` |
| Subir mis commits | `git push` |

### Etiquetar una entrega

| Quiero… | Comando |
|---|---|
| Listar etiquetas | `git tag` |
| Marcar una entrega o versión | `git tag -a v1.0 -m "Entrega TP1"` |
| Publicar una etiqueta | `git push origin v1.0` |
| Publicar todas las etiquetas | `git push origin --tags` |

### Alias (atajos opcionales)

```bash
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --decorate"
# después: git st   /   git lg
```

### Mini-receta: entregar un TP de POO

```bash
# --- una sola vez, al crear el repo ---
git init
git remote add origin https://github.com/mi-usuario/tp-poo.git
printf "__pycache__/\n*.pyc\n.venv/\n.idea/\n.vscode/\n" > .gitignore
git add .gitignore
git commit -m "Agrega .gitignore"
git push -u origin main

# --- cada vez que termino un ejercicio o una clase ---
git status
git add cuenta.py persona.py
git commit -m "Ejercicio 3: clase Cuenta con depositar() y extraer()"
git push

# --- al cerrar la entrega ---
git tag -a tp1 -m "Entrega TP1 - POO"
git push origin --tags
```

**Regla de oro:** escribir el `.gitignore` **antes** del primer `git add`.

---

## Enlaces fuente

- https://git-scm.com/book/es/v2/Fundamentos-de-Git-Obteniendo-un-repositorio-Git
- https://git-scm.com/book/es/v2/Fundamentos-de-Git-Guardando-cambios-en-el-Repositorio
- https://git-scm.com/book/es/v2/Fundamentos-de-Git-Ver-el-Historial-de-Confirmaciones
- https://git-scm.com/book/es/v2/Fundamentos-de-Git-Deshacer-Cosas
- https://git-scm.com/book/es/v2/Fundamentos-de-Git-Trabajar-con-Remotos
- https://git-scm.com/book/es/v2/Fundamentos-de-Git-Etiquetado
- https://git-scm.com/book/es/v2/Fundamentos-de-Git-Alias-de-Git
- https://git-scm.com/book/es/v2/Fundamentos-de-Git-Resumen
