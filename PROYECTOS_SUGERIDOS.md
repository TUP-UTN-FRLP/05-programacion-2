# Proyectos sugeridos — Programación 2

> ## IMPORTANTE: cómo elegir el proyecto del grupo
>
> 1. Elijan **un proyecto entre los 19 restantes (del 2 al 20)**. El **proyecto 1, Biblioteca barrial, es el proyecto guía de la cátedra y no se elige**. **Cada proyecto lo puede tener un solo grupo**: gana el primero que lo anote.
> 2. **Modifiquen este archivo:** en la fila del proyecto elegido, escriban en la columna *Comisión y grupo* el número de comisión y de grupo. Ejemplo: `TUP11 - Grupo 02`.
> 3. Después **copien el nombre del proyecto** y péguenlo en [`GRUPOS.md`](GRUPOS.md), en la entrada de su grupo, **justo debajo del título del grupo y arriba de `Integrantes:`**, con este formato:
>
> ```text
> ### TUP11 - Grupo 2
>
> Proyecto: Biblioteca barrial
>
> Integrantes:
> ```
>
> Antes de anotarse, **verifiquen que la fila esté vacía**. Modifiquen únicamente la fila de su proyecto.

## Reserva de proyectos

El proyecto 1 lo desarrolla la cátedra en paralelo, a lo largo de la cursada, como modelo para que los grupos sigan su estructura y su forma de trabajo. Los grupos eligen entre el 2 y el 20.

| # | Proyecto | Comisión y grupo |
| --- | --- | --- |
| 1 | Biblioteca barrial | **PROYECTO GUÍA DE LA CÁTEDRA (no se elige)** |
| 2 | Turnos de consultorio |  |
| 3 | Gimnasio | TUP11 - Grupo 1 |
| 4 | Veterinaria |  |
| 5 | Alquiler de canchas |  |
| 6 | Alquiler de herramientas |  |
| 7 | Escuela de idiomas |  |
| 8 | Taller mecánico |  |
| 9 | Peluquería |  |
| 10 | Club deportivo (cuotas) |  |
| 11 | Hostel |  |
| 12 | Tienda de ropa |  |
| 13 | Cine |  |
| 14 | Eventos y entradas |  |
| 15 | Stock de farmacia |  |
| 16 | Consorcio |  |
| 17 | Pedidos de un restaurante |  |
| 18 | Préstamo de equipos del laboratorio |  |
| 19 | Torneo de fútbol |  |
| 20 | Mesa de ayuda |  |

---

## 1. El molde común

Los 20 proyectos son la misma estructura con otro tema. Eso permite dar las mismas clases a todos y comparar entregas con el mismo criterio.

| App | Rol | Equivale en el BANCO a | Ejemplo (biblioteca) |
| --- | --- | --- | --- |
| **App 1: personas** | Quién participa | `Persona` | `Socio` |
| **App 2: recursos** | Lo que se ofrece, prestan o venden | `Cuenta` | `Libro` |
| **App 3: operaciones** | Lo que une a los dos, con fecha y estado | `Movimiento` | `Prestamo` |

Las apps dependen en una sola dirección: **operaciones → personas y recursos**. Personas y recursos no se conocen entre sí (excepciones: en el 4 la mascota depende del dueño y en el 19 el jugador depende del equipo; ahí la dependencia es hacia la otra app de datos base y no hacia operaciones).

### Requisitos mínimos (iguales para todos)

1. **CRUD completo** (alta, listado, detalle, modificación y baja) de las entidades de las apps 1 y 2, y alta, listado y detalle de las operaciones.
2. **Plantillas:** un `base.html` con `extends`, menú y mensajes (`messages`).
3. **Validaciones en el modelo** (`clean()` y validadores de campo), nunca solo en el formulario: DNI o documento, rangos de números, fechas coherentes, textos obligatorios.
4. **2 o 3 reglas de negocio** en una capa de servicios (`servicios.py`), no dentro de las vistas.
5. **Tests:** al menos 15, con `TestCase`: 1 grupo por app, más pruebas de cada regla de negocio y de cada validación (caso válido y caso inválido).
6. **Datos de ejemplo** con un comando `cargar_demo`.
7. **Admin** configurado para las tres entidades.

### Lo que NO se pide

Login ni permisos, API, JavaScript, pagos reales, envío de mails ni subida de imágenes. Si algún grupo termina antes, eso queda como extra.


## 2. Los 20 proyectos

Todos tienen el mismo nivel de dificultad. Las reglas de negocio son el **máximo** que se pide.

### 1. Biblioteca barrial — PROYECTO GUÍA DE LA CÁTEDRA

> **Este proyecto no se elige.** Lo desarrolla la cátedra en paralelo con los grupos y sirve como plantilla: estructura de apps, validaciones, servicios y tests que cada grupo debe replicar en su propio proyecto.

**Apps sugeridas:** `socios`, `libros` y `prestamos`

- `socios`: `Socio` (nombre, DNI, email, activo)
- `libros`: `Libro` (título, autor, ISBN, ejemplares)
- `prestamos`: `Prestamo` (socio, libro, fecha, devolución)

**Reglas de negocio:** Máximo 3 préstamos activos por socio. No se presta si no quedan ejemplares.

### 2. Turnos de consultorio

**Apps sugeridas:** `pacientes`, `profesionales` y `turnos`

- `pacientes`: `Paciente` (nombre, DNI, obra social)
- `profesionales`: `Profesional` (nombre, matrícula, especialidad)
- `turnos`: `Turno` (paciente, profesional, fecha y hora, estado)

**Reglas de negocio:** No hay dos turnos del mismo profesional a la misma hora. No se pide turno en el pasado.

### 3. Gimnasio

**Apps sugeridas:** `socios`, `clases` y `inscripciones`

- `socios`: `Socio` (nombre, DNI, fecha de alta)
- `clases`: `Clase` (disciplina, día, horario, cupo)
- `inscripciones`: `Inscripcion` (socio, clase, fecha)

**Reglas de negocio:** No se supera el cupo. Un socio no se anota dos veces a la misma clase.

### 4. Veterinaria

**Apps sugeridas:** `duenios`, `veterinarios` y `consultas`

- `duenios`: `Duenio` (nombre, DNI, teléfono) y `Mascota`
- `veterinarios`: `Veterinario` (nombre, matrícula)
- `consultas`: `Consulta` (mascota, veterinario, fecha, motivo, importe)

**Reglas de negocio:** Una mascota tiene un solo dueño. No hay consultas con fecha futura. Importe mayor que 0.

### 5. Alquiler de canchas

**Apps sugeridas:** `clientes`, `canchas` y `reservas`

- `clientes`: `Cliente` (nombre, teléfono, DNI)
- `canchas`: `Cancha` (nombre, deporte, precio por hora)
- `reservas`: `Reserva` (cliente, cancha, fecha, hora inicio, horas)

**Reglas de negocio:** No se solapan reservas de la misma cancha. Entre 1 y 3 horas por reserva.

### 6. Alquiler de herramientas

**Apps sugeridas:** `clientes`, `herramientas` y `alquileres`

- `clientes`: `Cliente` (nombre, DNI, domicilio)
- `herramientas`: `Herramienta` (nombre, categoría, precio diario, stock)
- `alquileres`: `Alquiler` (cliente, herramienta, desde, hasta, total)

**Reglas de negocio:** Hasta no antes de desde. El total es días por precio. No se alquila sin stock.

### 7. Escuela de idiomas

**Apps sugeridas:** `alumnos`, `cursos` y `inscripciones`

- `alumnos`: `Alumno` (nombre, DNI, nacimiento)
- `cursos`: `Curso` (idioma, nivel, cupo, cuota mensual)
- `inscripciones`: `Inscripcion` (alumno, curso, fecha, nota final)

**Reglas de negocio:** No se supera el cupo. La nota va de 1 a 10. Un alumno no repite curso activo.

### 8. Taller mecánico

**Apps sugeridas:** `clientes`, `servicios` y `ordenes`

- `clientes`: `Cliente` (nombre, DNI) y `Vehiculo` (patente, marca, año)
- `servicios`: `Servicio` (descripción, precio)
- `ordenes`: `Orden` (vehículo, servicio, fecha, estado)

**Reglas de negocio:** La patente tiene formato válido. Estados: pendiente, en curso, terminada, sin saltearse pasos.

### 9. Peluquería

**Apps sugeridas:** `clientes`, `servicios` y `turnos`

- `clientes`: `Cliente` (nombre, teléfono)
- `servicios`: `Servicio` (nombre, duración, precio) y `Estilista`
- `turnos`: `Turno` (cliente, estilista, servicio, fecha y hora)

**Reglas de negocio:** El estilista no atiende dos turnos a la vez. Horario entre 9 y 20.

### 10. Club deportivo (cuotas)

**Apps sugeridas:** `socios`, `actividades` y `cuotas`

- `socios`: `Socio` (nombre, DNI, categoría)
- `actividades`: `Actividad` (nombre, cuota mensual)
- `cuotas`: `Cuota` (socio, actividad, mes, año, pagada)

**Reglas de negocio:** No hay dos cuotas del mismo socio, actividad y mes. Mes entre 1 y 12.

### 11. Hostel

**Apps sugeridas:** `huespedes`, `habitaciones` y `reservas`

- `huespedes`: `Huesped` (nombre, documento, país)
- `habitaciones`: `Habitacion` (número, camas, precio por noche)
- `reservas`: `Reserva` (huésped, habitación, ingreso, egreso)

**Reglas de negocio:** Egreso posterior al ingreso. No se solapan reservas de la misma habitación.

### 12. Tienda de ropa

**Apps sugeridas:** `clientes`, `productos` y `ventas`

- `clientes`: `Cliente` (nombre, DNI, email)
- `productos`: `Producto` (nombre, talle, precio, stock)
- `ventas`: `Venta` (cliente, producto, cantidad, fecha)

**Reglas de negocio:** La venta descuenta stock y no puede dejarlo negativo. Cantidad mayor que 0.

### 13. Cine

**Apps sugeridas:** `espectadores`, `funciones` y `entradas`

- `espectadores`: `Espectador` (nombre, DNI, email)
- `funciones`: `Funcion` (película, sala, fecha, precio, butacas)
- `entradas`: `Entrada` (espectador, función, cantidad)

**Reglas de negocio:** No se vende más de las butacas libres. No se vende para una función pasada.

### 14. Eventos y entradas

**Apps sugeridas:** `asistentes`, `eventos` y `tickets`

- `asistentes`: `Asistente` (nombre, DNI, email)
- `eventos`: `Evento` (nombre, lugar, fecha, capacidad, precio)
- `tickets`: `Ticket` (asistente, evento, código, usado)

**Reglas de negocio:** No se supera la capacidad. Un ticket se usa una sola vez.

### 15. Stock de farmacia

**Apps sugeridas:** `proveedores`, `medicamentos` y `movimientos`

- `proveedores`: `Proveedor` (razón social, CUIT)
- `medicamentos`: `Medicamento` (nombre, laboratorio, stock, stock mínimo)
- `movimientos`: `MovimientoStock` (medicamento, proveedor, tipo, cantidad, fecha)

**Reglas de negocio:** Una salida no deja el stock negativo. Avisar cuando el stock cae por debajo del mínimo.

### 16. Consorcio

**Apps sugeridas:** `propietarios`, `unidades` y `expensas`

- `propietarios`: `Propietario` (nombre, DNI, email)
- `unidades`: `Unidad` (piso, depto, porcentaje de expensas)
- `expensas`: `Expensa` (unidad, período, importe, pagada)

**Reglas de negocio:** Un porcentaje entre 0 y 100. No hay dos expensas de la misma unidad y período.

### 17. Pedidos de un restaurante

**Apps sugeridas:** `mesas`, `platos` y `pedidos`

- `mesas`: `Mesa` (número, capacidad)
- `platos`: `Plato` (nombre, categoría, precio)
- `pedidos`: `Pedido` (mesa, plato, cantidad, estado)

**Reglas de negocio:** Cantidad mayor que 0. No se pide en una mesa cerrada. Estados con orden fijo.

### 18. Préstamo de equipos del laboratorio

**Apps sugeridas:** `docentes`, `equipos` y `reservas`

- `docentes`: `Docente` (nombre, legajo, email)
- `equipos`: `Equipo` (código, tipo, disponible)
- `reservas`: `Reserva` (docente, equipo, fecha, turno)

**Reglas de negocio:** No se reserva un equipo ya reservado en el mismo turno. No se reserva uno no disponible.

### 19. Torneo de fútbol

**Apps sugeridas:** `jugadores`, `equipos` y `partidos`

- `jugadores`: `Jugador` (nombre, DNI, camiseta)
- `equipos`: `Equipo` (nombre, año de fundación)
- `partidos`: `Partido` (local, visitante, fecha, goles de cada uno)

**Reglas de negocio:** Local distinto de visitante. Camiseta única dentro del equipo. Goles mayor o igual que 0.

### 20. Mesa de ayuda

**Apps sugeridas:** `usuarios`, `categorias` y `tickets`

- `usuarios`: `Usuario` (nombre, legajo, email)
- `categorias`: `Categoria` (nombre, prioridad)
- `tickets`: `Ticket` (usuario, categoría, descripción, estado, fecha)

**Reglas de negocio:** No se cierra un ticket sin respuesta. Estados con orden fijo (abierto, en curso, cerrado).

## 3. Hoja de ruta de 6 semanas

Calendario sugerido, parecido al orden con que se armó el BANCO.

| Semana | Entregable | Equivale a |
| --- | --- | --- |
| 1 | Proyecto, `settings`, `base.html`, app 1 con modelo, admin y migraciones | Primera página + modelo |
| 2 | App 1 completa: CRUD, formularios, validaciones y sus tests | Iteraciones 2 y 3 |
| 3 | App 2 completa: CRUD, validaciones y tests. Relaciones entre apps | Iteración 3 |
| 4 | App 3: la operación, con `ForeignKey` a las otras dos y sus vistas | Iteración 4 |
| 5 | `servicios.py` con las reglas de negocio, mensajes de error y tests de las reglas | Iteración 4 y 5 |
| 6 | Pulido: `cargar_demo`, README, revisión de tests y defensa | Entrega |

## Para presentar el trabajo

- Un repositorio por grupo, que cree la cátedra a partir de `GRUPOS.md`.
- Cada grupo entrega un `README.md` con: tema, apps, entidades, reglas de negocio y cómo correr los tests.
- Se espera **un commit por semana** como mínimo (ver `GUIA_COMMITS.md`).
