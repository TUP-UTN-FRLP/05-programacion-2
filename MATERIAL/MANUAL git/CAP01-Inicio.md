# Git — Parte 1: Inicio y control de versiones

> **Fuente**
> El libro [Pro Git](https://git-scm.com/book), de Scott Chacon y Ben Straub, está disponible para leer en línea gratis en `git-scm.com`.
> Se distribuye bajo licencia Creative Commons BY-NC-SA 3.0. Las figuras citadas pertenecen al sitio oficial `git-scm.com`.

## Alcance

Esta es la **Parte 1** del apunte. Cubre estos capítulos del libro **Pro Git**:

- Acerca del Control de Versiones
- Una breve historia de Git
- Fundamentos de Git
- La Línea de Comandos
- Configurando Git por primera vez
- ¿Cómo obtener ayuda?
- Resumen

## Objetivo de la parte

Entender qué problema resuelve Git, cómo piensa el historial de un proyecto y cuáles son las ideas mínimas necesarias para empezar a usarlo con criterio.

---

## 1. ¿Qué es el control de versiones?

Un sistema de control de versiones registra cambios sobre archivos a lo largo del tiempo. Permite:

- volver a una versión anterior;
- comparar cambios;
- saber quién modificó qué;
- recuperar trabajo perdido;
- trabajar con más seguridad cuando participan varias personas.

### En la práctica

Sin control de versiones, el “historial” termina siendo una carpeta con nombres como:

- `final.py`
- `final_bien.py`
- `final_ahora_si.py`
- `final_definitivo_2.py`

Git reemplaza ese caos por un historial explícito y consultable.

![Control de versiones local](https://git-scm.com/book/es/v2/images/local.png)

---

## 2. Modelos de control de versiones

### Local
El historial queda en una sola computadora.

### Centralizado
Hay un servidor central que concentra el historial del equipo.

### Distribuido
Cada clon del repositorio contiene una copia completa del historial.

### Comparación rápida

| Modelo | Ventaja | Riesgo |
|---|---|---|
| Local | Simple | Si se pierde la máquina, se pierde el historial |
| Centralizado | Orden común | El servidor es un punto único de falla |
| Distribuido | Cada copia tiene historial completo | Requiere entender sincronización |

![Control centralizado](https://git-scm.com/book/es/v2/images/centralized.png)

![Control distribuido](https://git-scm.com/book/es/v2/images/distributed.png)

---

## 3. Breve historia de Git

Git nace en 2005, en el contexto del desarrollo del kernel Linux. Surge como respuesta a la necesidad de contar con una herramienta:

- rápida;
- distribuida;
- confiable;
- preparada para trabajo colaborativo grande.

### En la práctica

No hace falta retener toda la historia: alcanza con entender que Git no nació “para guardar archivos”, sino para sostener trabajo colaborativo real y complejo.

---

## 4. Fundamentos de Git

El apartado “Fundamentos de Git” del libro plantea cinco ideas. Conviene no quedarse solo con la primera.

### 4.1 Instantáneas, no diferencias

Git no piensa el historial como una secuencia de diferencias aisladas. Piensa el proyecto como una sucesión de **instantáneas**.

Cada commit es como una foto del proyecto en un momento dado. Si un archivo no cambió, Git no vuelve a guardarlo completo: reutiliza la referencia al contenido anterior.

![Deltas](https://git-scm.com/book/es/v2/images/deltas.png)

![Snapshots](https://git-scm.com/book/es/v2/images/snapshots.png)

### 4.2 Casi todas las operaciones son locales

`git log`, `git diff`, `git branch` o `git status` no consultan ningún servidor: el historial completo está en el disco de cada clon.

**Por qué importa:** explica por qué Git es instantáneo y por qué se puede trabajar sin conexión. También anticipa la Parte 2: si todo es local, entonces publicar es un paso aparte.

### 4.3 Git tiene integridad

Todo lo que Git guarda se identifica por una **suma de verificación** calculada sobre el propio contenido. Nada se pierde ni se altera sin que Git lo detecte.

**Por qué importa:** explica de dónde salen esos identificadores largos que aparecen en `git log`. Los commits no se numeran 1, 2, 3: se identifican por su contenido.

### 4.4 Git generalmente solo añade información

Casi todas las operaciones agregan datos al historial. Lo que ya fue confirmado es muy difícil de perder.

**Por qué importa:** baja la ansiedad. Podés experimentar sin miedo, siempre que hayas confirmado antes.

### 4.5 Los tres estados

Se desarrolla en la sección siguiente.

---

## 5. Los tres estados y las tres secciones

El libro distingue dos cosas que conviene no mezclar: los **estados** en los que puede estar un archivo y las **secciones** del proyecto donde vive cada uno.

| Estado | Significado | Dónde está |
|---|---|---|
| Modified (modificado) | El archivo fue cambiado pero todavía no se preparó | Directorio de trabajo |
| Staged (preparado) | El cambio fue marcado para el próximo commit | Área de preparación |
| Committed (confirmado) | El cambio quedó guardado en la base de datos local | Directorio `.git` |

### Flujo básico

1. Modificás archivos en el directorio de trabajo.
2. Preparás los archivos, agregándolos al área de preparación.
3. Confirmás: Git toma lo que hay en el área de preparación y guarda esa instantánea en `.git`.

![Tres áreas de Git](https://git-scm.com/book/es/v2/images/areas.png)

### En la práctica

Esta es una de las ideas más importantes del apunte. Si entendés **directorio de trabajo → área de preparación → repositorio**, después los comandos tienen más sentido.

El camino de vuelta (`git switch` / `git checkout`, recuperar una versión guardada) se ve recién en la **Parte 3**. Por ahora alcanza con saber que existe.

---

## 6. La línea de comandos

Para empezar, conviene usar Git desde la terminal. Las interfaces gráficas pueden ayudar después, pero la consola hace visible el flujo real.

> Primero entender la lógica con comandos. Después, con ese criterio, se puede pasar a una interfaz gráfica.

---

## 7. Configuración inicial

Comandos mínimos para una primera instalación:

```bash
git config --global user.name "Nombre Apellido"
git config --global user.email "correo@example.com"
git config --global init.defaultBranch main
git config --list
```

Opcional, si el editor por defecto te resulta incómodo:

```bash
git config --global core.editor "code --wait"
```

### En la práctica

- `--global` deja la configuración aplicada al usuario del sistema, no solo al repositorio actual.
- `init.defaultBranch main` es importante para el resto del apunte: sin esa línea, según la versión instalada, `git init` puede crear una rama llamada `master` y las Partes 2 y 3 (que siempre hablan de `main`) dejan de coincidir con lo que ves en pantalla.

---

## 8. ¿Cómo obtener ayuda?

Comandos útiles:

```bash
git help config
git config --help
git config -h
man git-config
```

### Lectura rápida

- `git <verbo> -h` muestra la **ayuda corta**: la lista de opciones en la misma terminal. Es la que más se usa en el día a día.
- `git <verbo> --help` y `git help <verbo>` abren el **manual completo**.

### En la práctica

No hace falta memorizar todas las opciones: saber **pedir ayuda** ya es parte de aprender Git.

---

## 9. Cierre de la parte 1

### Ideas fuerza

- Git sirve para registrar historia, no solo para “subir archivos”.
- Git es distribuido: cada clon contiene el historial completo, y por eso casi todo es local.
- Git trabaja con instantáneas y verifica la integridad de todo lo que guarda.
- El flujo básico se entiende mejor desde los tres estados y las tres secciones.
- Antes de memorizar comandos, hay que entender el modelo.

### Práctica corta

1. Abrir una carpeta cualquiera.
2. Configurar nombre, correo y `init.defaultBranch` si hiciera falta.
3. Inicializar un repositorio con `git init`.
4. Ejecutar `git status` y observar qué informa.
5. Ejecutar `git branch` y verificar que la rama se llame `main`.

---

## 10. Síntesis de comandos — referencia práctica

> Tabla de consulta rápida. La idea no es memorizarla, sino tenerla al lado las primeras semanas. Cada fila responde a un "¿cómo hago para…?".

### Verificar que Git está instalado

```bash
git --version        # si esto falla, Git no está instalado todavía
```

### Puesta a punto (una sola vez por computadora)

| Quiero… | Comando |
|---|---|
| Decir quién soy (aparece firmando cada commit) | `git config --global user.name "Nombre Apellido"` |
| Registrar mi correo | `git config --global user.email "correo@example.com"` |
| Que los repos nuevos arranquen en la rama `main` | `git config --global init.defaultBranch main` |
| Usar VS Code como editor de Git (opcional) | `git config --global core.editor "code --wait"` |
| Revisar toda mi configuración | `git config --list` |

### Empezar a versionar una carpeta

| Quiero… | Comando | Qué obtengo |
|---|---|---|
| Convertir la carpeta actual en repositorio | `git init` | una subcarpeta oculta `.git` y la rama `main` vacía |
| Ver en qué estado está el repo | `git status` | qué archivos hay sin seguir, modificados o preparados |
| Ver en qué rama estoy | `git branch` | la lista de ramas; el `*` marca la actual |

### Pedir ayuda

| Quiero… | Comando |
|---|---|
| Ayuda corta, en la misma terminal | `git <verbo> -h` (ej.: `git commit -h`) |
| Manual completo | `git help <verbo>` o `git <verbo> --help` |

### Mini-receta: dejar lista una computadora nueva del laboratorio

```bash
git --version                                  # confirmar que está instalado
git config --global user.name "Ana Gómez"      # solo si nunca lo configuré acá
git config --global user.email "ana@mail.com"
git config --global init.defaultBranch main

cd carpeta-de-mi-practica
git init
git status          # todavía no hay nada confirmado
git branch          # tiene que decir: main
```

> No hace falta abrir ni tocar la carpeta `.git`: Git la administra solo. Borrarla elimina todo el historial.

Los comandos para **preparar y confirmar** cambios (`git add`, `git commit`) se ven en la Parte 2.

---

## Nota sobre las imágenes

Las figuras enlazadas arriba se cargan directamente desde `git-scm.com`, así que necesitás conexión para verlas. Si se guardan en el repositorio del curso, hay que mantener la atribución al libro (CC BY-NC-SA 3.0).

## Enlaces fuente

- https://git-scm.com/book/es/v2/Inicio---Sobre-el-Control-de-Versiones-Acerca-del-Control-de-Versiones
- https://git-scm.com/book/es/v2/Inicio---Sobre-el-Control-de-Versiones-Una-breve-historia-de-Git
- https://git-scm.com/book/es/v2/Inicio---Sobre-el-Control-de-Versiones-Fundamentos-de-Git
- https://git-scm.com/book/es/v2/Inicio---Sobre-el-Control-de-Versiones-La-L%C3%ADnea-de-Comandos
- https://git-scm.com/book/es/v2/Inicio---Sobre-el-Control-de-Versiones-Configurando-Git-por-primera-vez
- https://git-scm.com/book/es/v2/Inicio---Sobre-el-Control-de-Versiones-%C2%BFC%C3%B3mo-obtener-ayuda%3F
- https://git-scm.com/book/es/v2/Inicio---Sobre-el-Control-de-Versiones-Resumen
