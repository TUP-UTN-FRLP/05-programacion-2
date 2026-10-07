# 20 proyectos finales con Django (variaciones del mismo molde)

Material del docente. Pensado para estudiantes que recién empiezan: pocas reglas de negocio, mucha validación y tests.

## 1. El molde común

Los 20 proyectos son la misma estructura con otro tema. Eso permite dar las mismas clases a todos y comparar entregas con el mismo criterio.

| App | Rol | Equivale en el BANCO a | Ejemplo (biblioteca) |
| --- | --- | --- | --- |
| **App 1: personas** | Quién participa | `Persona` | `Socio` |
| **App 2: recursos** | Lo que se ofrece, prestan o venden | `Cuenta` | `Libro` |
| **App 3: operaciones** | Lo que une a los dos, con fecha y estado | `Movimiento` | `Prestamo` |

Las apps dependen en una sola dirección: **operaciones → personas y recursos**. Personas y recursos no se conocen entre sí (excepciones: en el 4 la mascota depende del dueño y en el 19 el jugador depende del equipo; ahí la dependencia es hacia la otra app de datos base y no hacia operaciones).

Si un grupo es de dos integrantes, puede fusionar personas y recursos en una sola app y quedarse con dos apps.

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

---

## 2. Los 20 proyectos

La columna de reglas es el **máximo** que se le pide a cada proyecto. Todas son del mismo nivel de dificultad.

| # | Proyecto | App 1: personas | App 2: recursos | App 3: operaciones | Reglas de negocio sugeridas |
| --- | --- | --- | --- | --- | --- |
| 1 | **Biblioteca barrial** | `Socio` (nombre, DNI, email, activo) | `Libro` (título, autor, ISBN, ejemplares) | `Prestamo` (socio, libro, fecha, devolución) | Máximo 3 préstamos activos por socio. No se presta si no quedan ejemplares. |
| 2 | **Turnos de consultorio** | `Paciente` (nombre, DNI, obra social) | `Profesional` (nombre, matrícula, especialidad) | `Turno` (paciente, profesional, fecha y hora, estado) | No hay dos turnos del mismo profesional a la misma hora. No se pide turno en el pasado. |
| 3 | **Gimnasio** | `Socio` (nombre, DNI, fecha de alta) | `Clase` (disciplina, día, horario, cupo) | `Inscripcion` (socio, clase, fecha) | No se supera el cupo. Un socio no se anota dos veces a la misma clase. |
| 4 | **Veterinaria** | `Duenio` (nombre, DNI, teléfono) y `Mascota` | `Veterinario` (nombre, matrícula) | `Consulta` (mascota, veterinario, fecha, motivo, importe) | Una mascota tiene un solo dueño. No hay consultas con fecha futura. Importe mayor que 0. |
| 5 | **Alquiler de canchas** | `Cliente` (nombre, teléfono, DNI) | `Cancha` (nombre, deporte, precio por hora) | `Reserva` (cliente, cancha, fecha, hora inicio, horas) | No se solapan reservas de la misma cancha. Entre 1 y 3 horas por reserva. |
| 6 | **Alquiler de herramientas** | `Cliente` (nombre, DNI, domicilio) | `Herramienta` (nombre, categoría, precio diario, stock) | `Alquiler` (cliente, herramienta, desde, hasta, total) | Hasta no antes de desde. El total es días por precio. No se alquila sin stock. |
| 7 | **Escuela de idiomas** | `Alumno` (nombre, DNI, nacimiento) | `Curso` (idioma, nivel, cupo, cuota mensual) | `Inscripcion` (alumno, curso, fecha, nota final) | No se supera el cupo. La nota va de 1 a 10. Un alumno no repite curso activo. |
| 8 | **Taller mecánico** | `Cliente` (nombre, DNI) y `Vehiculo` (patente, marca, año) | `Servicio` (descripción, precio) | `Orden` (vehículo, servicio, fecha, estado) | La patente tiene formato válido. Estados: pendiente, en curso, terminada, sin saltearse pasos. |
| 9 | **Peluquería** | `Cliente` (nombre, teléfono) | `Servicio` (nombre, duración, precio) y `Estilista` | `Turno` (cliente, estilista, servicio, fecha y hora) | El estilista no atiende dos turnos a la vez. Horario entre 9 y 20. |
| 10 | **Club deportivo (cuotas)** | `Socio` (nombre, DNI, categoría) | `Actividad` (nombre, cuota mensual) | `Cuota` (socio, actividad, mes, año, pagada) | No hay dos cuotas del mismo socio, actividad y mes. Mes entre 1 y 12. |
| 11 | **Hostel** | `Huesped` (nombre, documento, país) | `Habitacion` (número, camas, precio por noche) | `Reserva` (huésped, habitación, ingreso, egreso) | Egreso posterior al ingreso. No se solapan reservas de la misma habitación. |
| 12 | **Tienda de ropa** | `Cliente` (nombre, DNI, email) | `Producto` (nombre, talle, precio, stock) | `Venta` (cliente, producto, cantidad, fecha) | La venta descuenta stock y no puede dejarlo negativo. Cantidad mayor que 0. |
| 13 | **Cine** | `Espectador` (nombre, DNI, email) | `Funcion` (película, sala, fecha, precio, butacas) | `Entrada` (espectador, función, cantidad) | No se vende más de las butacas libres. No se vende para una función pasada. |
| 14 | **Eventos y entradas** | `Asistente` (nombre, DNI, email) | `Evento` (nombre, lugar, fecha, capacidad, precio) | `Ticket` (asistente, evento, código, usado) | No se supera la capacidad. Un ticket se usa una sola vez. |
| 15 | **Stock de farmacia** | `Proveedor` (razón social, CUIT) | `Medicamento` (nombre, laboratorio, stock, stock mínimo) | `MovimientoStock` (medicamento, proveedor, tipo, cantidad, fecha) | Una salida no deja el stock negativo. Avisar cuando el stock cae por debajo del mínimo. |
| 16 | **Consorcio** | `Propietario` (nombre, DNI, email) | `Unidad` (piso, depto, porcentaje de expensas) | `Expensa` (unidad, período, importe, pagada) | Un porcentaje entre 0 y 100. No hay dos expensas de la misma unidad y período. |
| 17 | **Pedidos de un restaurante** | `Mesa` (número, capacidad) | `Plato` (nombre, categoría, precio) | `Pedido` (mesa, plato, cantidad, estado) | Cantidad mayor que 0. No se pide en una mesa cerrada. Estados con orden fijo. |
| 18 | **Préstamo de equipos del laboratorio** | `Docente` (nombre, legajo, email) | `Equipo` (código, tipo, disponible) | `Reserva` (docente, equipo, fecha, turno) | No se reserva un equipo ya reservado en el mismo turno. No se reserva uno no disponible. |
| 19 | **Torneo de fútbol** | `Jugador` (nombre, DNI, camiseta) | `Equipo` (nombre, año de fundación) | `Partido` (local, visitante, fecha, goles de cada uno) | Local distinto de visitante. Camiseta única dentro del equipo. Goles mayor o igual que 0. |
| 20 | **Mesa de ayuda** | `Usuario` (nombre, legajo, email) | `Categoria` (nombre, prioridad) | `Ticket` (usuario, categoría, descripción, estado, fecha) | No se cierra un ticket sin respuesta. Estados con orden fijo (abierto, en curso, cerrado). |

---

## 3. Notas por tipo de relación

Para repartir proyectos según lo que se quiere practicar:

| Tipo | Proyectos | Qué practican |
| --- | --- | --- |
| **Operación con solapamiento de fechas** | 2, 5, 9, 11, 18 | Consultas con rangos de fechas, `Q`, validación cruzada |
| **Cupo o stock que se descuenta** | 1, 3, 6, 7, 12, 13, 14, 15 | Servicios con `transaction.atomic`, `F()`, errores del negocio |
| **Estados con orden** | 8, 17, 20 | Máquina de estados sencilla, `choices`, método que valida la transición |
| **Período único (restricción de unicidad)** | 10, 16 | `UniqueConstraint` con varios campos, validación de rangos |
| **Dos entidades personales** | 4, 8, 19 | `ForeignKey` entre apps 1 y 1, y `related_name` |

Recomendación: darles a elegir entre 3 o 4 proyectos de **tipos distintos** y no dejar libre la elección, así se reparten los temas.

---

## 4. Hoja de ruta de 6 semanas

Este es el calendario sugerido, parecido al orden del BANCO.

| Semana | Entregable | Equivale a |
| --- | --- | --- |
| 1 | Proyecto, `settings`, `base.html`, app 1 con modelo, admin y migraciones | Primera página + modelo |
| 2 | App 1 completa: CRUD, formularios, validaciones y sus tests | Iteraciones 2 y 3 |
| 3 | App 2 completa: CRUD, validaciones y tests. Relaciones entre apps | Iteración 3 |
| 4 | App 3: la operación, con `ForeignKey` a las otras dos y sus vistas | Iteración 4 |
| 5 | `servicios.py` con las reglas de negocio, mensajes de error y tests de las reglas | Iteración 4 y 5 |
| 6 | Pulido: `cargar_demo`, README, revisión de tests y defensa | Entrega |

## 5. Criterios de evaluación sugeridos

| Criterio | Peso |
| --- | --- |
| Estructura (3 apps, dependencias en una sola dirección, modelos claros) | 20 % |
| Validaciones en el modelo, con mensajes claros | 20 % |
| Reglas de negocio en `servicios.py`, no en las vistas | 20 % |
| Tests (cantidad, calidad, casos válidos e inválidos) | 25 % |
| Plantillas y uso del admin | 5 % |
| Defensa oral: cada integrante explica una parte del código | 10 % |

## 6. Para presentar el trabajo

- Lo ideal es **grupos de dos o tres**, con un repositorio por grupo.
- Cada grupo entrega un `README.md` con: tema, apps, entidades, reglas de negocio y cómo correr los tests.
- Conviene pedir **un commit por semana** para ver el avance (retomando `GUIA_COMMITS.md`).
