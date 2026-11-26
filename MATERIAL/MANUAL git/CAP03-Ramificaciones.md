# Git — Parte 3: Ramificaciones

> **Fuente**
> El libro [Pro Git](https://git-scm.com/book), de Scott Chacon y Ben Straub, está disponible para leer en línea gratis en `git-scm.com`.
> Se distribuye bajo licencia Creative Commons BY-NC-SA 3.0. Las figuras citadas pertenecen al sitio oficial `git-scm.com`.

## Alcance

Esta es la **Parte 3** del apunte. Cubre estos apartados del libro **Pro Git**:

- ¿Qué es una rama?
- Procedimientos Básicos para Ramificar y Fusionar (incluye conflictos)
- Gestión de Ramas
- Flujos de Trabajo Ramificados
- Ramas Remotas
- Reorganizar el Trabajo Realizado
- Recapitulación

## Objetivo de la parte

Comprender qué es una rama, cómo permite trabajo paralelo, cómo se fusiona, qué hacer cuando la fusión no es automática, cómo se publica y por qué `rebase` conviene usarlo con criterio.

---

## 1. ¿Qué es una rama?

Una rama es un **apuntador móvil a un commit**. No crea una copia completa del proyecto cada vez que se genera. Marca una línea de trabajo dentro del historial.

![Una rama y su historial de confirmaciones](https://git-scm.com/book/es/v2/images/branch-and-history.png)

![Dos ramas apuntando al mismo grupo de confirmaciones](https://git-scm.com/book/es/v2/images/two-branches.png)

### En la práctica

Es habitual imaginar una rama como “otra carpeta”. Conviene desarmar esa idea desde el principio: no hay copias, hay apuntadores.

---

## 2. HEAD

`HEAD` indica dónde estamos posicionados. Normalmente apunta a la rama actual, y esa rama apunta a un commit.

### Comandos útiles

```bash
git branch
git switch nombre-rama
git log --oneline --decorate --graph --all
```

![HEAD apunta a la rama actual](https://git-scm.com/book/es/v2/images/head-to-master.png)

![La rama apuntada por HEAD avanza con cada confirmación](https://git-scm.com/book/es/v2/images/advance-testing.png)

### En la práctica

Más que profundizar en los internals, alcanza con entender que cuando hacés un commit **avanza la rama actual** (la que señala `HEAD`). Esas dos figuras son las que mejor desarman la idea de “rama = carpeta”.

---

## 3. Crear y cambiar de rama

```bash
git switch -c iteracion-01/mi-nombre
```

En materiales más antiguos aparece `git checkout -b`. Hoy, `git switch -c` suele ser más claro.

Atajo útil: `git switch -` vuelve a la rama en la que estabas antes (como "atrás" en el navegador). Sirve mucho cuando se salta seguido entre `main` y una rama de trabajo.

![Crear un apuntador a la rama nueva](https://git-scm.com/book/es/v2/images/basic-branching-2.png)

---

## 4. Fusionar ramas

```bash
git switch main
git merge nombre-rama
```

### Idea clave

- Si `main` **no avanzó** desde que se creó la rama, su commit es ancestro directo del otro y Git puede hacer un **fast-forward**: simplemente mueve el apuntador, sin crear un commit nuevo.
- Si hubo trabajo paralelo en las dos ramas, Git busca el **ancestro común** y crea un commit de fusión, que tiene dos padres.

![Git identifica el mejor ancestro común para la fusión](https://git-scm.com/book/es/v2/images/basic-merging-1.png)

![Git crea una nueva confirmación para la fusión](https://git-scm.com/book/es/v2/images/basic-merging-2.png)

### En la práctica

Conviene mostrar el merge como “volver a unir líneas de trabajo”, no solo como ejecutar un comando.

---

## 5. Cuando la fusión no es automática: conflictos

Si las dos ramas modificaron **las mismas líneas** del mismo archivo, Git no decide por vos: se detiene y deja el conflicto marcado en el archivo.

### Cómo se ve

```text
<<<<<<< HEAD
precio = 100
=======
precio = 120
>>>>>>> rama-precio
```

- Arriba, entre `<<<<<<<` y `=======`, está la versión de la rama actual (`HEAD`).
- Abajo, entre `=======` y `>>>>>>>`, la de la rama que se está fusionando.

### Cómo se resuelve

```bash
git status                  # 1. lista los archivos en conflicto
# 2. abrir el archivo, dejar la versión final y borrar los tres marcadores
git add archivo.py          # 3. marcar el conflicto como resuelto
git commit                  # 4. cerrar la fusión
```

Si el conflicto es grande y conviene rehacerlo con calma:

```bash
git merge --abort           # vuelve al estado anterior a la fusión
```

### En la práctica

Este es el punto donde más se traba una primera práctica grupal. Conviene generar un conflicto a propósito para practicarlo con calma, en vez de encontrarlo por primera vez en una entrega.

Vale la pena decirlo explícitamente: **un conflicto no es un error tuyo**. Es Git avisando que dos personas cambiaron lo mismo y que la decisión es humana.

---

## 6. Gestión de ramas

Comandos útiles:

```bash
git branch
git branch -v
git branch --merged
git branch --no-merged
git branch -d nombre-rama     # falla si la rama no fue fusionada
git branch -D nombre-rama     # fuerza el borrado
```

### Lectura rápida

`git branch -d` **ya protege**: si la rama tiene trabajo sin fusionar, devuelve un error y sugiere `-D`. Es decir, borrar por accidente requiere insistir.

### En la práctica

Antes de borrar una rama, revisar con `--merged` / `--no-merged` si ya fue integrada. Eso evita perder trabajo o generar confusión.

---

## 7. Flujos de trabajo ramificados

Para empezar conviene un flujo simple:

1. `main` queda estable.
2. Cada integrante trabaja en su rama.
3. Publica esa rama en remoto.
4. Abre un Pull Request.
5. Se revisa y se fusiona.

```bash
git switch main
git pull origin main
git switch -c iteracion-01/mi-nombre
# trabajar, agregar, confirmar
git push -u origin iteracion-01/mi-nombre
```

### Precisión importante

El **Pull Request es una función de GitHub**, no de Git. En el libro aparece en el capítulo 6; el capítulo 3 describe la idea subyacente en términos de:

- **ramas de larga duración**: `main` (y a veces `develop`), que se mantienen estables en el tiempo;
- **ramas puntuales** (*topic branches*): una por tarea o por issue, de vida corta, que se borran una vez integradas.

El flujo de arriba es exactamente eso, con el PR como mecanismo de revisión.

### En la práctica

La clave no es memorizar nombres de flujos complejos, sino entender **cómo no pisarse entre varias personas**.

---

## 8. Ramas remotas

Las ramas remotas (`origin/main`, `origin/mi-rama`) muestran el estado del repositorio remoto **tal como Git lo conoció la última vez que se conectó**. No se actualizan solas.

### Comandos básicos

```bash
git fetch origin                      # actualizar lo que sé del remoto
git branch -r                         # ver ramas remotas
git push -u origin iteracion-01/mi-nombre   # publicar mi rama
git switch iteracion-01/otro-nombre   # crear la local siguiendo a origin/...
git push origin --delete nombre-rama  # borrar la rama en el remoto
```

### Lectura rápida

- Después de un `git fetch`, si existe `origin/mi-rama` y no hay una rama local con ese nombre, `git switch mi-rama` crea la local y la deja **siguiendo** a la remota.
- Borrar una rama local con `git branch -d` **no** la borra del servidor: para eso está `git push origin --delete`.

![Servidor y repositorio local luego de ser clonado](https://git-scm.com/book/es/v2/images/remote-branches-1.png)

![git fetch actualiza las referencias del remoto](https://git-scm.com/book/es/v2/images/remote-branches-3.png)

### En la práctica

Una rama local no aparece mágicamente en GitHub: hay que publicarla con `push`.

Y `origin/main` no es `main`: es la foto del remoto que Git tiene guardada localmente.

---

## 9. Rebase

`rebase` reaplica commits sobre una nueva base para producir una historia más lineal. Los commits resultantes son **nuevos**: mismo cambio, otro identificador.

### Secuencia completa

```bash
git switch experimento     # pararse en la rama a reorganizar
git rebase main            # reaplicar sus commits sobre main
git switch main
git merge experimento      # ahora es un avance rápido
```

![Reorganizando sobre C3 los cambios introducidos en C4](https://git-scm.com/book/es/v2/images/basic-rebase-3.png)

![Avance rápido de la rama principal](https://git-scm.com/book/es/v2/images/basic-rebase-4.png)

### Regla práctica

Al empezar:

> No usar `rebase` sobre commits ya publicados o compartidos, salvo que el equipo entienda exactamente qué está haciendo.

### En la práctica

No hace falta usar `rebase` mucho al principio. Sí conviene entender que **reescribe historia**: `C4` no se mueve, se crea `C4'`. Si otra persona ya basó su trabajo en `C4`, ese trabajo queda huérfano.

---

## 10. Cierre de la parte 3

### Ideas fuerza

- Una rama es un apuntador móvil, no una copia suelta del proyecto.
- `HEAD` indica dónde estamos trabajando; al confirmar, avanza la rama actual.
- Crear ramas permite trabajo paralelo.
- `merge` vuelve a unir líneas de trabajo; a veces es un fast-forward y a veces crea un commit de fusión.
- Un conflicto es una decisión pendiente, no una falla.
- Las ramas remotas representan el estado publicado, actualizado por `fetch`.
- `rebase` puede ordenar historia, pero crea commits nuevos y exige cuidado.

### Práctica corta

1. Crear una rama personal con `git switch -c`.
2. Hacer un commit en esa rama.
3. Publicarla con `git push -u origin ...`.
4. Volver a `main`.
5. Fusionar la rama.
6. **Provocar un conflicto a propósito**: dos integrantes editan la misma línea en ramas distintas y fusionan. Resolverlo con `git status`, edición, `git add` y `git commit`.
7. Revisar el historial con `git log --graph --oneline --all`.
8. Borrar la rama ya integrada (`git branch -d` local y `git push origin --delete` en el remoto).

---

## 11. Síntesis de comandos — referencia práctica

> Trabajar con ramas agrega dos preguntas al circuito diario: **¿en qué rama estoy?** y **¿esta rama ya está integrada?**

### Moverse entre ramas

| Quiero… | Comando |
|---|---|
| Ver las ramas locales (y en cuál estoy) | `git branch` |
| Ver cada rama con su último commit | `git branch -v` |
| Crear una rama y pasarme a ella | `git switch -c iteracion-01/mi-nombre` |
| Cambiar a una rama que ya existe | `git switch nombre-rama` |
| Volver a la rama anterior (ida y vuelta) | `git switch -` |
| Ver el historial de todas las ramas juntas | `git log --oneline --graph --decorate --all` |

En materiales viejos: `git checkout -b` = `git switch -c` · `git checkout rama` = `git switch rama`.

### Fusionar

| Quiero… | Comando |
|---|---|
| Traer el trabajo de otra rama a la actual | `git switch main` y luego `git merge nombre-rama` |
| Cancelar una fusión que se complicó | `git merge --abort` |

### Resolver un conflicto

```bash
git status                 # 1. ver qué archivos quedaron en conflicto
# 2. abrir cada archivo, dejar la versión final y
#    borrar las líneas <<<<<<<, ======= y >>>>>>>
git add archivo.py         # 3. marcar ese archivo como resuelto
git commit                 # 4. cerrar la fusión
```

Un conflicto **no es un error tuyo**: Git avisa que dos personas cambiaron lo mismo y que la decisión es humana.

### Limpiar ramas

| Quiero… | Comando |
|---|---|
| Ver qué ramas ya se fusionaron a la actual | `git branch --merged` |
| Ver las que todavía no | `git branch --no-merged` |
| Borrar una rama ya integrada | `git branch -d nombre-rama` |
| Forzar el borrado (tiene trabajo sin fusionar) | `git branch -D nombre-rama` |

### Ramas remotas

| Quiero… | Comando |
|---|---|
| Actualizar lo que sé del remoto | `git fetch origin` |
| Ver las ramas remotas | `git branch -r` |
| Publicar mi rama por primera vez | `git push -u origin iteracion-01/mi-nombre` |
| Bajar una rama que creó otra persona (después de `fetch`) | `git switch nombre-rama` |
| Borrar una rama en el remoto | `git push origin --delete nombre-rama` |

### Rebase (con cuidado)

```bash
git switch experimento
git rebase main            # reaplica los commits de experimento sobre main
git switch main
git merge experimento      # ahora es un avance rápido
```

Regla al empezar: **no rebasar commits ya publicados o compartidos.**

### Mini-receta: entregar una iteración por rama + Pull Request

```bash
git switch main
git pull origin main                          # partir de lo último
git switch -c iteracion-01/ana-gomez          # una rama por tarea

# ...crear o editar las clases, y después:
git add figura.py circulo.py rectangulo.py
git commit -m "Iteracion 1: jerarquia Figura -> Circulo, Rectangulo"
git push -u origin iteracion-01/ana-gomez     # publicar la rama

# en GitHub: abrir el Pull Request hacia main y esperar la revisión

# cuando el PR ya fue fusionado:
git switch main
git pull origin main
git branch -d iteracion-01/ana-gomez                 # borrar la local
git push origin --delete iteracion-01/ana-gomez      # borrar la remota
```

---

## Nota sobre las imágenes

Los pies de figura corresponden a los del libro. Si las imágenes se guardan en el repositorio del curso, hay que mantener la atribución (CC BY-NC-SA 3.0).

## Enlaces fuente

- <https://git-scm.com/book/es/v2/Ramificaciones-en-Git-%C2%BFQu%C3%A9-es-una-rama%3F>
- <https://git-scm.com/book/es/v2/Ramificaciones-en-Git-Procedimientos-B%C3%A1sicos-para-Ramificar-y-Fusionar>
- <https://git-scm.com/book/es/v2/Ramificaciones-en-Git-Gesti%C3%B3n-de-Ramas>
- <https://git-scm.com/book/es/v2/Ramificaciones-en-Git-Flujos-de-Trabajo-Ramificados>
- <https://git-scm.com/book/es/v2/Ramificaciones-en-Git-Ramas-Remotas>
- <https://git-scm.com/book/es/v2/Ramificaciones-en-Git-Reorganizar-el-Trabajo-Realizado>
- <https://git-scm.com/book/es/v2/Ramificaciones-en-Git-Recapitulaci%C3%B3n>
