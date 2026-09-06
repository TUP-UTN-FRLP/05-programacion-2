# Ejercicios integradores

> **Convenciones de este archivo.**
> 1. Los atributos van protegidos (`_nombre`). Las clases contenidas
>    exponen métodos de lectura (`precio()`, `numero()`) y de cambio de
>    estado (`ocupar()`, `cambiar_precio()`); nadie las manotea desde
>    afuera.
> 2. El código de prueba va dentro de `if __name__ == "__main__":`, tal
>    como pide el capítulo: así el archivo se puede importar sin que la
>    prueba se ejecute.
> 3. Un método llamado `buscar_algo()` **lanza excepción** si no
>    encuentra. Si querés un método que pueda devolver `None`, se llama
>    distinto y se documenta.

## `enunciado_01.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Direccion con calle, numero y ciudad. Después hacé
# Persona que tenga una Direccion como atributo, usando composición.
# Imprimí una persona con su dirección completa. Fijate que Persona no
# reimplementa el formato de la dirección: se lo delega a Direccion.
# -------------------------------------------------------------------------

class Direccion:
    """Dirección postal, pensada para vivir dentro de otras clases."""

    def __init__(self, calle, numero, ciudad):
        self._calle = calle
        self._numero = numero
        self._ciudad = ciudad

    def __str__(self):
        return f"{self._calle} {self._numero}, {self._ciudad}"


class Persona:
    """Persona que tiene una Direccion como atributo."""

    def __init__(self, nombre, direccion):
        self._nombre = nombre
        self._direccion = direccion

    def __str__(self):
        return f"{self._nombre} vive en {self._direccion}"


if __name__ == "__main__":
    direccion = Direccion("Av. 7", 1234, "La Plata")
    persona = Persona("Ana Perez", direccion)

    print(persona)
```

## `enunciado_02.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Motor con cilindrada y potencia, y una clase Auto con
# marca, modelo y un Motor. Imprimí un auto con toda su información.
# Después creá un solo Motor y dos Autos que lo compartan, cambiale la
# potencia y observá que los dos autos ven el cambio: guardan una
# referencia al mismo objeto, no una copia. Pensá por qué compartir un
# motor entre dos autos es un error de modelado.
# -------------------------------------------------------------------------

class Motor:
    """Motor de un auto. En la realidad pertenece a un solo auto."""

    def __init__(self, cilindrada, potencia):
        self._cilindrada = cilindrada
        self._potencia = potencia

    def ajustar_potencia(self, potencia):
        """Cambia la potencia declarada del motor."""
        self._potencia = potencia

    def __str__(self):
        return f"Motor {self._cilindrada}cc / {self._potencia}HP"


class Auto:
    """Auto compuesto por un objeto Motor."""

    def __init__(self, marca, modelo, motor):
        self._marca = marca
        self._modelo = modelo
        self._motor = motor

    def __str__(self):
        return f"{self._marca} {self._modelo} - {self._motor}"


if __name__ == "__main__":
    auto = Auto("Ford", "Focus", Motor(2000, 150))
    print(auto)

    # Un mismo motor referenciado por dos autos.
    compartido = Motor(1600, 110)
    uno = Auto("Fiat", "Cronos", compartido)
    otro = Auto("Peugeot", "208", compartido)

    compartido.ajustar_potencia(120)

    print(uno)
    print(otro)

    # Los dos cambiaron: es un solo Motor con dos referencias.
    # Con una Direccion compartida entre dos Personas esto sería
    # correcto (agregación). Con un Motor no lo es: un motor
    # pertenece a un único auto y debería crearse para él.
```

## `enunciado_03.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Curso con nombre y una lista de Alumno, donde cada
# alumno tiene nombre y legajo. Agregá los métodos inscribir(alumno),
# cantidad_inscriptos() y listar_alumnos(). El nombre del curso no se
# lee desde afuera: exponelo con __str__.
# -------------------------------------------------------------------------

class Alumno:
    """Alumno identificado por nombre y legajo."""

    def __init__(self, nombre, legajo):
        self._nombre = nombre
        self._legajo = legajo

    def legajo(self):
        """Devuelve el legajo del alumno."""
        return self._legajo

    def __str__(self):
        return f"[{self._legajo}] {self._nombre}"


class Curso:
    """Curso que administra una colección de alumnos."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._alumnos = []

    def inscribir(self, alumno):
        """Agrega un alumno a la lista de inscriptos."""
        self._alumnos.append(alumno)

    def cantidad_inscriptos(self):
        """Devuelve cuántos alumnos hay inscriptos."""
        return len(self._alumnos)

    def listar_alumnos(self):
        """Imprime todos los alumnos inscriptos."""
        for alumno in self._alumnos:
            print(f"  {alumno}")

    def __str__(self):
        return (
            f"{self._nombre}: "
            f"{self.cantidad_inscriptos()} inscriptos"
        )


if __name__ == "__main__":
    curso = Curso("Programación 2")
    curso.inscribir(Alumno("Ana", "L-001"))
    curso.inscribir(Alumno("Juan", "L-002"))
    curso.inscribir(Alumno("Pedro", "L-003"))

    print(curso)
    curso.listar_alumnos()
```

## `enunciado_04.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Continuando el ejercicio 3, sumale buscar_por_legajo(legajo), que
# devuelva el alumno correspondiente o lance una excepción propia si no
# lo encuentra. Probá los dos caminos: el que encuentra y el que falla.
# -------------------------------------------------------------------------

class AlumnoNoEncontrado(Exception):
    """Indica que no existe un alumno con el legajo solicitado."""

    pass


class Alumno:
    """Alumno identificado por nombre y legajo."""

    def __init__(self, nombre, legajo):
        self._nombre = nombre
        self._legajo = legajo

    def legajo(self):
        """Devuelve el legajo del alumno."""
        return self._legajo

    def __str__(self):
        return f"[{self._legajo}] {self._nombre}"


class Curso:
    """Curso que administra y busca alumnos por legajo."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._alumnos = []

    def inscribir(self, alumno):
        """Agrega un alumno a la lista de inscriptos."""
        self._alumnos.append(alumno)

    def cantidad_inscriptos(self):
        """Devuelve cuántos alumnos hay inscriptos."""
        return len(self._alumnos)

    def listar_alumnos(self):
        """Imprime todos los alumnos inscriptos."""
        for alumno in self._alumnos:
            print(f"  {alumno}")

    def buscar_por_legajo(self, legajo):
        """Devuelve el alumno con ese legajo o lanza excepción."""
        for alumno in self._alumnos:
            if alumno.legajo() == legajo:
                return alumno

        raise AlumnoNoEncontrado(
            f"No hay alumno con legajo {legajo}"
        )


if __name__ == "__main__":
    curso = Curso("Programación 2")
    curso.inscribir(Alumno("Ana", "L-001"))
    curso.inscribir(Alumno("Juan", "L-002"))

    print(curso.buscar_por_legajo("L-001"))

    try:
        curso.buscar_por_legajo("L-999")
    except AlumnoNoEncontrado as error:
        print(f"Error: {error}")
```

## `enunciado_05.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Playlist con nombre y una lista de Cancion. Cada
# Cancion tiene titulo, artista y duracion_seg. Agregá los métodos
# agregar_cancion(), duracion_total(), cantidad() y listar(). Mostrá
# la duración total en formato minutos:segundos.
# -------------------------------------------------------------------------

class Cancion:
    """Canción con título, artista y duración en segundos."""

    def __init__(self, titulo, artista, duracion_seg):
        self._titulo = titulo
        self._artista = artista
        self._duracion_seg = duracion_seg

    def duracion_seg(self):
        """Devuelve la duración de la canción en segundos."""
        return self._duracion_seg

    def __str__(self):
        minutos, segundos = divmod(self._duracion_seg, 60)
        return (
            f"{self._titulo} - {self._artista} "
            f"({minutos}:{segundos:02d})"
        )


class Playlist:
    """Playlist que contiene una colección de canciones."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._canciones = []

    def agregar_cancion(self, cancion):
        """Suma una canción al final de la playlist."""
        self._canciones.append(cancion)

    def cantidad(self):
        """Devuelve cuántas canciones tiene la playlist."""
        return len(self._canciones)

    def duracion_total(self):
        """Suma las duraciones de todas las canciones."""
        return sum(
            cancion.duracion_seg()
            for cancion in self._canciones
        )

    def listar(self):
        """Imprime el detalle de la playlist."""
        minutos, segundos = divmod(self.duracion_total(), 60)
        print(f"{self._nombre} ({self.cantidad()} temas)")

        for cancion in self._canciones:
            print(f"  {cancion}")

        print(f"  Duración total: {minutos}:{segundos:02d}")


if __name__ == "__main__":
    playlist = Playlist("Rock nacional")
    playlist.agregar_cancion(
        Cancion("Seminare", "Serú Girán", 315)
    )
    playlist.agregar_cancion(
        Cancion("Rasguña las piedras", "Sui Generis", 240)
    )

    playlist.listar()
```

## `enunciado_06.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé un Carrito de compras con tres clases: Producto, con nombre y
# precio; LineaDeCarrito, que junta un Producto con una cantidad y sabe
# calcular su subtotal; y Carrito, que contiene una lista de líneas.
# Agregá agregar(producto, cantidad), total() y mostrar(). Fijate que
# cada clase calcula lo suyo y le pide el resto a la de abajo.
# -------------------------------------------------------------------------

class Producto:
    """Producto con nombre y precio unitario."""

    def __init__(self, nombre, precio):
        self._nombre = nombre
        self._precio = precio

    def nombre(self):
        """Devuelve el nombre del producto."""
        return self._nombre

    def precio(self):
        """Devuelve el precio unitario."""
        return self._precio

    def __str__(self):
        return f"{self._nombre} (${self._precio})"


class LineaDeCarrito:
    """Una línea del carrito: un producto y su cantidad."""

    def __init__(self, producto, cantidad):
        self._producto = producto
        self._cantidad = cantidad

    def subtotal(self):
        """Precio unitario por la cantidad pedida."""
        return self._producto.precio() * self._cantidad

    def __str__(self):
        return (
            f"{self._producto.nombre()} x{self._cantidad}: "
            f"${self.subtotal()}"
        )


class Carrito:
    """Carrito compuesto por líneas de compra."""

    def __init__(self):
        self._lineas = []

    def agregar(self, producto, cantidad):
        """Suma una línea nueva al carrito."""
        self._lineas.append(
            LineaDeCarrito(producto, cantidad)
        )

    def total(self):
        """Suma los subtotales de todas las líneas."""
        return sum(
            linea.subtotal() for linea in self._lineas
        )

    def mostrar(self):
        """Imprime el detalle del carrito y su total."""
        for linea in self._lineas:
            print(f"  {linea}")

        print(f"  TOTAL: ${self.total()}")


if __name__ == "__main__":
    carrito = Carrito()
    carrito.agregar(Producto("Yerba", 3500), 2)
    carrito.agregar(Producto("Leche", 800), 3)

    carrito.mostrar()
```

## `enunciado_07.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Equipo con nombre y una lista de Jugador. Cada Jugador
# tiene nombre, posicion y numero. Agregá agregar_jugador(),
# jugador_por_numero(numero), que lance una excepción propia si no está,
# y alineacion(), que imprima todos los jugadores ordenados por número.
# -------------------------------------------------------------------------

class JugadorNoEncontrado(Exception):
    """Indica que no existe un jugador con el número pedido."""

    pass


class Jugador:
    """Jugador con nombre, posición y número de camiseta."""

    def __init__(self, nombre, posicion, numero):
        self._nombre = nombre
        self._posicion = posicion
        self._numero = numero

    def numero(self):
        """Devuelve el número de camiseta."""
        return self._numero

    def __str__(self):
        return (
            f"#{self._numero} {self._nombre} "
            f"({self._posicion})"
        )


class Equipo:
    """Equipo que administra una colección de jugadores."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._jugadores = []

    def agregar_jugador(self, jugador):
        """Suma un jugador al plantel."""
        self._jugadores.append(jugador)

    def jugador_por_numero(self, numero):
        """Devuelve el jugador con ese número o lanza excepción."""
        for jugador in self._jugadores:
            if jugador.numero() == numero:
                return jugador

        raise JugadorNoEncontrado(
            f"No hay jugador con número {numero}"
        )

    def alineacion(self):
        """Imprime el plantel ordenado por número de camiseta."""
        ordenados = sorted(
            self._jugadores,
            key=lambda jugador: jugador.numero(),
        )

        print(f"{self._nombre}:")

        for jugador in ordenados:
            print(f"  {jugador}")


if __name__ == "__main__":
    equipo = Equipo("Estudiantes")
    equipo.agregar_jugador(Jugador("Verón", "Volante", 11))
    equipo.agregar_jugador(Jugador("Palermo", "Delantero", 9))
    equipo.agregar_jugador(Jugador("Andújar", "Arquero", 1))

    equipo.alineacion()
    print(equipo.jugador_por_numero(9))

    try:
        equipo.jugador_por_numero(99)
    except JugadorNoEncontrado as error:
        print(f"Error: {error}")
```

## `enunciado_08.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Concesionaria con ABM completo de autos. Auto tiene
# patente, marca, modelo y precio. Agregá agregar_auto(),
# buscar_por_patente(), listar_autos(), actualizar_precio() y
# eliminar_auto(). Usá excepciones propias para patente duplicada y auto
# no encontrado, y reutilizá buscar_por_patente() dentro de los otros
# métodos en lugar de repetir la comprobación.
# -------------------------------------------------------------------------

class PatenteDuplicadaError(Exception):
    """Indica que una patente ya está registrada."""

    pass


class AutoNoEncontrado(Exception):
    """Indica que no existe el auto solicitado."""

    pass


class Auto:
    """Auto identificado por su patente."""

    def __init__(self, patente, marca, modelo, precio):
        self._patente = patente
        self._marca = marca
        self._modelo = modelo
        self._precio = precio

    def cambiar_precio(self, nuevo_precio):
        """Actualiza el precio de venta del auto."""
        if nuevo_precio <= 0:
            raise ValueError("El precio debe ser positivo")

        self._precio = nuevo_precio

    def __str__(self):
        return (
            f"[{self._patente}] {self._marca} "
            f"{self._modelo} - ${self._precio}"
        )


class Concesionaria:
    """Gestiona un ABM de autos indexados por patente."""

    def __init__(self):
        self._autos = {}

    def agregar_auto(self, patente, marca, modelo, precio):
        """Da de alta un auto nuevo y lo devuelve."""
        if patente in self._autos:
            raise PatenteDuplicadaError(
                f"La patente {patente} ya existe"
            )

        auto = Auto(patente, marca, modelo, precio)
        self._autos[patente] = auto

        return auto

    def buscar_por_patente(self, patente):
        """Devuelve el auto con esa patente o lanza excepción."""
        auto = self._autos.get(patente)

        if auto is None:
            raise AutoNoEncontrado(
                f"No hay auto con patente {patente}"
            )

        return auto

    def listar_autos(self):
        """Devuelve la lista de autos en venta."""
        return list(self._autos.values())

    def actualizar_precio(self, patente, nuevo_precio):
        """Cambia el precio del auto indicado."""
        auto = self.buscar_por_patente(patente)
        auto.cambiar_precio(nuevo_precio)

    def eliminar_auto(self, patente):
        """Da de baja física el auto indicado."""
        self.buscar_por_patente(patente)
        del self._autos[patente]


if __name__ == "__main__":
    concesionaria = Concesionaria()
    concesionaria.agregar_auto(
        "AA123BB", "Ford", "Focus", 15000000
    )
    concesionaria.agregar_auto(
        "AC456CD", "Toyota", "Corolla", 20000000
    )

    concesionaria.actualizar_precio("AA123BB", 16000000)
    concesionaria.eliminar_auto("AC456CD")

    for auto in concesionaria.listar_autos():
        print(auto)

    try:
        concesionaria.buscar_por_patente("AC456CD")
    except AutoNoEncontrado as error:
        print(f"Error: {error}")
```

## `enunciado_09.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Restaurant con un diccionario de Mesa. Cada Mesa tiene
# numero, capacidad y un estado de ocupación. Agregá abrir_mesa(),
# ocupar(numero), liberar(numero) y mesas_libres(). Importante: el
# Restaurant no debe cambiar el estado de la mesa desde afuera, tiene
# que pedírselo a la Mesa con ocupar() y liberar(). Validá que la mesa
# exista y que no se ocupe una mesa ya ocupada.
# -------------------------------------------------------------------------

class MesaNoEncontrada(Exception):
    """Indica que no existe la mesa solicitada."""

    pass


class MesaOcupadaError(Exception):
    """Indica que la mesa ya está ocupada."""

    pass


class Mesa:
    """Mesa que administra su propio estado de ocupación."""

    def __init__(self, numero, capacidad):
        self._numero = numero
        self._capacidad = capacidad
        self._ocupada = False

    def esta_ocupada(self):
        """Informa si la mesa está ocupada."""
        return self._ocupada

    def ocupar(self):
        """Marca la mesa como ocupada."""
        if self._ocupada:
            raise MesaOcupadaError(
                f"La mesa {self._numero} ya está ocupada"
            )

        self._ocupada = True

    def liberar(self):
        """Marca la mesa como libre."""
        self._ocupada = False

    def __str__(self):
        estado = "ocupada" if self._ocupada else "libre"
        return (
            f"Mesa {self._numero} "
            f"(cap. {self._capacidad}) - {estado}"
        )


class Restaurant:
    """Restaurant que gestiona sus mesas por número."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._mesas = {}

    def abrir_mesa(self, numero, capacidad):
        """Suma una mesa nueva al salón."""
        self._mesas[numero] = Mesa(numero, capacidad)

    def buscar_mesa(self, numero):
        """Devuelve la mesa pedida o lanza excepción."""
        mesa = self._mesas.get(numero)

        if mesa is None:
            raise MesaNoEncontrada(
                f"No existe la mesa {numero}"
            )

        return mesa

    def ocupar(self, numero):
        """Le pide a la mesa que se marque como ocupada."""
        self.buscar_mesa(numero).ocupar()

    def liberar(self, numero):
        """Le pide a la mesa que se marque como libre."""
        self.buscar_mesa(numero).liberar()

    def mesas_libres(self):
        """Devuelve las mesas que no están ocupadas."""
        return [
            mesa
            for mesa in self._mesas.values()
            if not mesa.esta_ocupada()
        ]


if __name__ == "__main__":
    restaurant = Restaurant("La Trattoria")

    for numero, capacidad in [(1, 4), (2, 2), (3, 6)]:
        restaurant.abrir_mesa(numero, capacidad)

    restaurant.ocupar(2)

    for mesa in restaurant.mesas_libres():
        print(mesa)

    try:
        restaurant.ocupar(2)
    except MesaOcupadaError as error:
        print(f"Error: {error}")

    try:
        restaurant.ocupar(99)
    except MesaNoEncontrada as error:
        print(f"Error: {error}")
```

## `enunciado_10.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Empresa con una lista de Empleado. Cada Empleado tiene
# legajo, nombre, sueldo y departamento. Agregá contratar(),
# despedir(legajo), que lance excepción si el legajo no existe,
# promedio_sueldos() y empleados_por_departamento(depto). Usá el legajo
# como identificador, no el nombre: dos empleados pueden llamarse igual.
# -------------------------------------------------------------------------

class EmpleadoNoEncontrado(Exception):
    """Indica que no existe el empleado solicitado."""

    pass


class Empleado:
    """Empleado con legajo, sueldo y departamento."""

    def __init__(self, legajo, nombre, sueldo, departamento):
        self._legajo = legajo
        self._nombre = nombre
        self._sueldo = sueldo
        self._departamento = departamento

    def legajo(self):
        """Devuelve el legajo del empleado."""
        return self._legajo

    def sueldo(self):
        """Devuelve el sueldo del empleado."""
        return self._sueldo

    def departamento(self):
        """Devuelve el departamento del empleado."""
        return self._departamento

    def __str__(self):
        return (
            f"[{self._legajo}] {self._nombre} - "
            f"{self._departamento} (${self._sueldo})"
        )


class Empresa:
    """Empresa que administra una colección de empleados."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._empleados = []

    def contratar(self, empleado):
        """Suma un empleado a la nómina."""
        self._empleados.append(empleado)

    def buscar_por_legajo(self, legajo):
        """Devuelve el empleado con ese legajo o lanza excepción."""
        for empleado in self._empleados:
            if empleado.legajo() == legajo:
                return empleado

        raise EmpleadoNoEncontrado(
            f"No hay empleado con legajo {legajo}"
        )

    def despedir(self, legajo):
        """Saca de la nómina al empleado indicado."""
        empleado = self.buscar_por_legajo(legajo)
        self._empleados.remove(empleado)

    def promedio_sueldos(self):
        """Promedio de sueldos; 0 si no hay empleados."""
        if not self._empleados:
            return 0

        total = sum(
            empleado.sueldo()
            for empleado in self._empleados
        )

        return total / len(self._empleados)

    def empleados_por_departamento(self, depto):
        """Devuelve los empleados de un departamento."""
        return [
            empleado
            for empleado in self._empleados
            if empleado.departamento() == depto
        ]


if __name__ == "__main__":
    empresa = Empresa("Sistemas SA")
    empresa.contratar(Empleado("E-1", "Ana", 500000, "IT"))
    empresa.contratar(Empleado("E-2", "Juan", 600000, "IT"))
    empresa.contratar(
        Empleado("E-3", "Pedro", 450000, "Ventas")
    )

    print(f"Promedio: ${empresa.promedio_sueldos():.2f}")

    for empleado in empresa.empleados_por_departamento("IT"):
        print(f"  {empleado}")

    empresa.despedir("E-2")

    try:
        empresa.despedir("E-99")
    except EmpleadoNoEncontrado as error:
        print(f"Error: {error}")
```

## `enunciado_11.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Baja lógica: hacé una clase Club con ABM de Socio, con numero y
# nombre. Dar de baja no debe borrar al socio, sino marcarlo como
# inactivo, para no perder el historial. Sumale listar_activos(),
# listar_todos() y reactivar(numero). El alta debe rechazar números
# repetidos y la baja debe fallar si el socio no existe.
# -------------------------------------------------------------------------

class SocioNoEncontrado(Exception):
    """Indica que no existe el socio solicitado."""

    pass


class NumeroDuplicadoError(Exception):
    """Indica que el número de socio ya está usado."""

    pass


class Socio:
    """Socio del club con estado de alta lógico."""

    def __init__(self, numero, nombre):
        self._numero = numero
        self._nombre = nombre
        self._activo = True

    def esta_activo(self):
        """Informa si el socio está activo."""
        return self._activo

    def dar_de_baja(self):
        """Marca al socio como inactivo sin borrarlo."""
        self._activo = False

    def reactivar(self):
        """Vuelve a marcar al socio como activo."""
        self._activo = True

    def __str__(self):
        estado = "activo" if self._activo else "de baja"
        return f"[{self._numero}] {self._nombre} ({estado})"


class Club:
    """Club que aplica baja lógica sobre sus socios."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._socios = {}

    def asociar(self, numero, nombre):
        """Da de alta un socio nuevo y lo devuelve."""
        if numero in self._socios:
            raise NumeroDuplicadoError(
                f"El socio {numero} ya existe"
            )

        socio = Socio(numero, nombre)
        self._socios[numero] = socio

        return socio

    def buscar(self, numero):
        """Devuelve el socio pedido o lanza excepción."""
        socio = self._socios.get(numero)

        if socio is None:
            raise SocioNoEncontrado(
                f"No existe el socio {numero}"
            )

        return socio

    def dar_de_baja(self, numero):
        """Marca al socio como inactivo (baja lógica)."""
        self.buscar(numero).dar_de_baja()

    def reactivar(self, numero):
        """Vuelve a poner activo a un socio dado de baja."""
        self.buscar(numero).reactivar()

    def listar_activos(self):
        """Devuelve solo los socios activos."""
        return [
            socio
            for socio in self._socios.values()
            if socio.esta_activo()
        ]

    def listar_todos(self):
        """Devuelve todos los socios, activos o no."""
        return list(self._socios.values())


if __name__ == "__main__":
    club = Club("Club Estudiantes")
    club.asociar(1, "Ana")
    club.asociar(2, "Juan")
    club.asociar(3, "Pedro")

    club.dar_de_baja(2)

    print("Activos:")
    for socio in club.listar_activos():
        print(f"  {socio}")

    print("Todos (el historial se conserva):")
    for socio in club.listar_todos():
        print(f"  {socio}")

    club.reactivar(2)
    print(club.buscar(2))
```

## `enunciado_12.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Hotel con nombre y un diccionario de Habitacion. Cada
# Habitacion tiene numero, tipo, precio por noche y disponibilidad.
# Agregá agregar_habitacion(), buscar_habitacion(numero), que lance
# excepción si no existe, y habitaciones_disponibles().
# -------------------------------------------------------------------------

class HabitacionNoEncontrada(Exception):
    """Indica que no existe la habitación solicitada."""

    pass


class Habitacion:
    """Habitación con tipo, precio y disponibilidad."""

    def __init__(self, numero, tipo, precio):
        self._numero = numero
        self._tipo = tipo
        self._precio = precio
        self._disponible = True

    def numero(self):
        """Devuelve el número de habitación."""
        return self._numero

    def esta_disponible(self):
        """Informa si la habitación se puede reservar."""
        return self._disponible

    def ocupar(self):
        """Marca la habitación como no disponible."""
        self._disponible = False

    def liberar(self):
        """Marca la habitación como disponible."""
        self._disponible = True

    def __str__(self):
        return (
            f"Hab {self._numero} ({self._tipo}) - "
            f"${self._precio}/noche"
        )


class Hotel:
    """Hotel que administra habitaciones por número."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._habitaciones = {}

    def agregar_habitacion(self, numero, tipo, precio):
        """Suma una habitación al hotel."""
        self._habitaciones[numero] = Habitacion(
            numero, tipo, precio
        )

    def buscar_habitacion(self, numero):
        """Devuelve la habitación pedida o lanza excepción."""
        habitacion = self._habitaciones.get(numero)

        if habitacion is None:
            raise HabitacionNoEncontrada(
                f"No existe la habitación {numero}"
            )

        return habitacion

    def habitaciones_disponibles(self):
        """Devuelve las habitaciones libres."""
        return [
            habitacion
            for habitacion in self._habitaciones.values()
            if habitacion.esta_disponible()
        ]


if __name__ == "__main__":
    hotel = Hotel("Hotel Central")
    hotel.agregar_habitacion(101, "single", 15000)
    hotel.agregar_habitacion(102, "doble", 22000)

    for habitacion in hotel.habitaciones_disponibles():
        print(habitacion)

    try:
        hotel.buscar_habitacion(999)
    except HabitacionNoEncontrada as error:
        print(f"Error: {error}")
```

## `enunciado_13.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Extendé el ejercicio 12: sumale una clase Reserva, con habitacion,
# huesped y dias, y una lista de reservas dentro del hotel. Incorporá
# reservar(numero, huesped, dias). Distinguí los dos errores posibles
# con excepciones distintas: que la habitación no exista y que exista
# pero ya esté ocupada. No son lo mismo y el usuario necesita saber
# cuál de los dos ocurrió.
# -------------------------------------------------------------------------

class HabitacionNoEncontrada(Exception):
    """Indica que no existe la habitación solicitada."""

    pass


class HabitacionNoDisponible(Exception):
    """Indica que la habitación existe pero está ocupada."""

    pass


class Habitacion:
    """Habitación con tipo, precio y disponibilidad."""

    def __init__(self, numero, tipo, precio):
        self._numero = numero
        self._tipo = tipo
        self._precio = precio
        self._disponible = True

    def numero(self):
        """Devuelve el número de habitación."""
        return self._numero

    def precio(self):
        """Devuelve el precio por noche."""
        return self._precio

    def esta_disponible(self):
        """Informa si la habitación se puede reservar."""
        return self._disponible

    def ocupar(self):
        """Marca la habitación como no disponible."""
        self._disponible = False

    def __str__(self):
        return (
            f"Hab {self._numero} ({self._tipo}) - "
            f"${self._precio}/noche"
        )


class Reserva:
    """Reserva que referencia una habitación del hotel."""

    def __init__(self, habitacion, huesped, dias):
        self._habitacion = habitacion
        self._huesped = huesped
        self._dias = dias

    def importe(self):
        """Precio por noche multiplicado por los días."""
        return self._habitacion.precio() * self._dias

    def __str__(self):
        return (
            f"{self._huesped} en hab "
            f"{self._habitacion.numero()} por {self._dias} "
            f"días: ${self.importe()}"
        )


class Hotel:
    """Hotel que gestiona habitaciones y reservas."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._habitaciones = {}
        self._reservas = []

    def agregar_habitacion(self, numero, tipo, precio):
        """Suma una habitación al hotel."""
        self._habitaciones[numero] = Habitacion(
            numero, tipo, precio
        )

    def buscar_habitacion(self, numero):
        """Devuelve la habitación pedida o lanza excepción."""
        habitacion = self._habitaciones.get(numero)

        if habitacion is None:
            raise HabitacionNoEncontrada(
                f"No existe la habitación {numero}"
            )

        return habitacion

    def reservar(self, numero, huesped, dias):
        """Reserva una habitación libre y devuelve la reserva."""
        habitacion = self.buscar_habitacion(numero)

        if not habitacion.esta_disponible():
            raise HabitacionNoDisponible(
                f"La habitación {numero} ya está ocupada"
            )

        reserva = Reserva(habitacion, huesped, dias)
        self._reservas.append(reserva)
        habitacion.ocupar()

        return reserva

    def listar_reservas(self):
        """Devuelve las reservas registradas."""
        return list(self._reservas)


if __name__ == "__main__":
    hotel = Hotel("Hotel Central")
    hotel.agregar_habitacion(101, "single", 15000)
    hotel.agregar_habitacion(102, "doble", 22000)

    print(hotel.reservar(101, "Ana Perez", 3))

    try:
        hotel.reservar(101, "Otro huésped", 2)
    except HabitacionNoDisponible as error:
        print(f"Ocupada: {error}")

    try:
        hotel.reservar(999, "Otro huésped", 2)
    except HabitacionNoEncontrada as error:
        print(f"Inexistente: {error}")
```

## `enunciado_14.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Torneo que contenga equipos por composición y un
# método agregar_equipo() que rechace la operación si ya se llegó al
# máximo. Definí el máximo como una constante del módulo, en MAYÚSCULAS,
# en vez de escribir el número suelto en el código. Usá una excepción
# propia TorneoLlenoError y sumá listar_equipos().
# -------------------------------------------------------------------------

MAX_EQUIPOS = 8


class TorneoLlenoError(Exception):
    """Indica que el torneo alcanzó el máximo de equipos."""

    pass


class Equipo:
    """Equipo participante de un torneo."""

    def __init__(self, nombre):
        self._nombre = nombre

    def __str__(self):
        return self._nombre


class Torneo:
    """Torneo con un cupo máximo de equipos."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._equipos = []

    def cupo_disponible(self):
        """Cuántos equipos más entran en el torneo."""
        return MAX_EQUIPOS - len(self._equipos)

    def agregar_equipo(self, equipo):
        """Inscribe un equipo si queda cupo."""
        if self.cupo_disponible() <= 0:
            raise TorneoLlenoError(
                f"El torneo ya tiene {MAX_EQUIPOS} equipos"
            )

        self._equipos.append(equipo)

    def listar_equipos(self):
        """Imprime los equipos inscriptos."""
        print(f"{self._nombre}:")

        for equipo in self._equipos:
            print(f"  {equipo}")


if __name__ == "__main__":
    torneo = Torneo("Copa Argentina")

    for numero in range(MAX_EQUIPOS):
        torneo.agregar_equipo(Equipo(f"Equipo {numero + 1}"))

    torneo.listar_equipos()
    print(f"Cupo disponible: {torneo.cupo_disponible()}")

    try:
        torneo.agregar_equipo(Equipo("Equipo 9"))
    except TorneoLlenoError as error:
        print(f"Error: {error}")
```

## `enunciado_15.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Sistema con dos gestores adentro: RegistroUsuarios y
# RegistroProductos, cada uno con su propio ABM chico. Sistema no
# guarda usuarios ni productos: los delega. Exponé crear_usuario(),
# crear_producto() y resumen(), que imprime los totales de cada uno.
# Cada registro guarda objetos, no diccionarios sueltos: si el dato
# tiene identidad y comportamiento, merece una clase.
# -------------------------------------------------------------------------

class Usuario:
    """Usuario identificado por su email."""

    def __init__(self, email, nombre):
        self._email = email
        self._nombre = nombre

    def __str__(self):
        return f"{self._nombre} <{self._email}>"


class Producto:
    """Producto identificado por su código."""

    def __init__(self, codigo, nombre, precio):
        self._codigo = codigo
        self._nombre = nombre
        self._precio = precio

    def __str__(self):
        return f"[{self._codigo}] {self._nombre} ${self._precio}"


class RegistroUsuarios:
    """Registro de usuarios indexados por email."""

    def __init__(self):
        self._usuarios = {}

    def crear(self, email, nombre):
        """Da de alta un usuario y lo devuelve."""
        usuario = Usuario(email, nombre)
        self._usuarios[email] = usuario

        return usuario

    def cantidad(self):
        """Cuántos usuarios hay registrados."""
        return len(self._usuarios)

    def listar(self):
        """Devuelve todos los usuarios."""
        return list(self._usuarios.values())


class RegistroProductos:
    """Registro de productos indexados por código."""

    def __init__(self):
        self._productos = {}

    def crear(self, codigo, nombre, precio):
        """Da de alta un producto y lo devuelve."""
        producto = Producto(codigo, nombre, precio)
        self._productos[codigo] = producto

        return producto

    def cantidad(self):
        """Cuántos productos hay registrados."""
        return len(self._productos)

    def listar(self):
        """Devuelve todos los productos."""
        return list(self._productos.values())


class Sistema:
    """Sistema compuesto por dos registros independientes."""

    def __init__(self):
        self._usuarios = RegistroUsuarios()
        self._productos = RegistroProductos()

    def crear_usuario(self, email, nombre):
        """Delega el alta en el registro de usuarios."""
        return self._usuarios.crear(email, nombre)

    def crear_producto(self, codigo, nombre, precio):
        """Delega el alta en el registro de productos."""
        return self._productos.crear(codigo, nombre, precio)

    def resumen(self):
        """Imprime los totales de cada registro."""
        print(f"Usuarios:  {self._usuarios.cantidad()}")

        for usuario in self._usuarios.listar():
            print(f"  {usuario}")

        print(f"Productos: {self._productos.cantidad()}")

        for producto in self._productos.listar():
            print(f"  {producto}")


if __name__ == "__main__":
    sistema = Sistema()
    sistema.crear_usuario("ana@correo.com", "Ana")
    sistema.crear_usuario("juan@correo.com", "Juan")
    sistema.crear_producto("P-001", "Yerba", 3500)

    sistema.resumen()
```

## `enunciado_16.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Vuelo con origen, destino y sus pasajeros. Cada
# Pasajero tiene nombre, dni y asiento. Como el asiento identifica de
# forma única al pasajero dentro del vuelo, guardá los pasajeros en un
# diccionario {asiento: Pasajero} en lugar de una lista: la búsqueda
# deja de recorrer todo. Agregá asignar_pasajero(), que rechace un
# asiento ya tomado, buscar_por_asiento() y listar_pasajeros().
# -------------------------------------------------------------------------

class AsientoOcupadoError(Exception):
    """Indica que un asiento ya fue asignado."""

    pass


class AsientoLibre(Exception):
    """Indica que no hay pasajero en ese asiento."""

    pass


class Pasajero:
    """Pasajero con nombre, DNI y asiento asignado."""

    def __init__(self, nombre, dni, asiento):
        self._nombre = nombre
        self._dni = dni
        self._asiento = asiento

    def asiento(self):
        """Devuelve el asiento asignado."""
        return self._asiento

    def __str__(self):
        return f"{self._asiento}: {self._nombre} ({self._dni})"


class Vuelo:
    """Vuelo que administra sus pasajeros por asiento."""

    def __init__(self, origen, destino):
        self._origen = origen
        self._destino = destino
        self._pasajeros = {}

    def asignar_pasajero(self, pasajero):
        """Sienta al pasajero si su asiento está libre."""
        asiento = pasajero.asiento()

        if asiento in self._pasajeros:
            raise AsientoOcupadoError(
                f"El asiento {asiento} ya está ocupado"
            )

        self._pasajeros[asiento] = pasajero

    def buscar_por_asiento(self, asiento):
        """Devuelve el pasajero de ese asiento o lanza excepción."""
        pasajero = self._pasajeros.get(asiento)

        if pasajero is None:
            raise AsientoLibre(
                f"El asiento {asiento} está libre"
            )

        return pasajero

    def listar_pasajeros(self):
        """Imprime el vuelo y sus pasajeros."""
        print(f"Vuelo {self._origen} - {self._destino}")

        for asiento in sorted(self._pasajeros):
            print(f"  {self._pasajeros[asiento]}")


if __name__ == "__main__":
    vuelo = Vuelo("EZE", "MAD")
    vuelo.asignar_pasajero(Pasajero("Ana", "12345678", "12A"))
    vuelo.asignar_pasajero(Pasajero("Juan", "87654321", "12B"))

    vuelo.listar_pasajeros()
    print(vuelo.buscar_por_asiento("12A"))

    try:
        vuelo.asignar_pasajero(
            Pasajero("Pedro", "11223344", "12A")
        )
    except AsientoOcupadoError as error:
        print(f"Error: {error}")
```

## `enunciado_17.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé un Notificador que administre objetos Suscriptor, con email y
# nombre, no cadenas sueltas. Agregá suscribir(), que rechace un email
# repetido; desuscribir(), que aplique baja lógica marcando al
# suscriptor como inactivo; y enviar_a_todos(mensaje), que solo le
# escriba a los activos. Así, si alguien se vuelve a suscribir, el
# sistema sabe que ya había estado.
# -------------------------------------------------------------------------

class EmailDuplicadoError(Exception):
    """Indica que el email ya está suscripto."""

    pass


class SuscriptorNoEncontrado(Exception):
    """Indica que no existe ese suscriptor."""

    pass


class Suscriptor:
    """Suscriptor con email, nombre y estado de suscripción."""

    def __init__(self, email, nombre):
        self._email = email
        self._nombre = nombre
        self._activo = True

    def email(self):
        """Devuelve el email del suscriptor."""
        return self._email

    def esta_activo(self):
        """Informa si el suscriptor recibe mensajes."""
        return self._activo

    def desuscribir(self):
        """Marca al suscriptor como inactivo."""
        self._activo = False

    def resuscribir(self):
        """Vuelve a activar al suscriptor."""
        self._activo = True

    def __str__(self):
        estado = "activo" if self._activo else "de baja"
        return f"{self._nombre} <{self._email}> ({estado})"


class Notificador:
    """Notificador que administra una lista de suscriptores."""

    def __init__(self):
        self._suscriptores = {}

    def suscribir(self, email, nombre):
        """Da de alta un suscriptor o reactiva uno de baja."""
        existente = self._suscriptores.get(email)

        if existente is not None:
            if existente.esta_activo():
                raise EmailDuplicadoError(
                    f"{email} ya está suscripto"
                )

            existente.resuscribir()
            return existente

        suscriptor = Suscriptor(email, nombre)
        self._suscriptores[email] = suscriptor

        return suscriptor

    def desuscribir(self, email):
        """Aplica baja lógica al suscriptor indicado."""
        suscriptor = self._suscriptores.get(email)

        if suscriptor is None:
            raise SuscriptorNoEncontrado(
                f"No hay suscriptor con email {email}"
            )

        suscriptor.desuscribir()

    def activos(self):
        """Devuelve solo los suscriptores activos."""
        return [
            suscriptor
            for suscriptor in self._suscriptores.values()
            if suscriptor.esta_activo()
        ]

    def enviar_a_todos(self, mensaje):
        """Envía un mensaje a cada suscriptor activo."""
        for suscriptor in self.activos():
            print(f"[EMAIL a {suscriptor.email()}] {mensaje}")


if __name__ == "__main__":
    notificador = Notificador()
    notificador.suscribir("ana@correo.com", "Ana")
    notificador.suscribir("juan@correo.com", "Juan")

    notificador.enviar_a_todos("Nuevo curso disponible")

    notificador.desuscribir("juan@correo.com")
    print("Tras la baja de Juan:")
    notificador.enviar_a_todos("Otro mensaje")

    try:
        notificador.suscribir("ana@correo.com", "Ana")
    except EmailDuplicadoError as error:
        print(f"Error: {error}")
```

## `enunciado_18.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Composición uno a muchos: hacé una clase Cuenta con numero y saldo, y
# una clase Cliente con nombre, dni y una lista de Cuenta. Agregá
# abrir_cuenta(numero, saldo_inicial), saldo_total() y
# listar_cuentas(). Las cuentas nacen dentro del cliente: es el cliente
# quien las crea, no se las pasan hechas desde afuera.
# -------------------------------------------------------------------------

class Cuenta:
    """Cuenta simple con número y saldo."""

    def __init__(self, numero, saldo_inicial=0):
        self._numero = numero
        self._saldo = saldo_inicial

    def saldo(self):
        """Devuelve el saldo actual de la cuenta."""
        return self._saldo

    def depositar(self, monto):
        """Suma un monto positivo al saldo."""
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")

        self._saldo += monto

    def __str__(self):
        return f"Cta {self._numero}: ${self._saldo}"


class Cliente:
    """Cliente compuesto por una lista de cuentas propias."""

    def __init__(self, nombre, dni):
        self._nombre = nombre
        self._dni = dni
        self._cuentas = []

    def abrir_cuenta(self, numero, saldo_inicial=0):
        """Crea una cuenta nueva del cliente y la devuelve."""
        cuenta = Cuenta(numero, saldo_inicial)
        self._cuentas.append(cuenta)

        return cuenta

    def saldo_total(self):
        """Suma los saldos de todas las cuentas del cliente."""
        return sum(
            cuenta.saldo() for cuenta in self._cuentas
        )

    def listar_cuentas(self):
        """Imprime el detalle de las cuentas del cliente."""
        print(f"{self._nombre} (DNI {self._dni})")

        for cuenta in self._cuentas:
            print(f"  {cuenta}")

        print(f"  Saldo total: ${self.saldo_total()}")


if __name__ == "__main__":
    cliente = Cliente("Ana Perez", "12345678")
    cliente.abrir_cuenta("001-100", 5000)
    caja = cliente.abrir_cuenta("001-101", 12000)

    caja.depositar(3000)
    cliente.listar_cuentas()
```

## `enunciado_19.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Composición más herencia: hacé Producto con nombre y precio_final(),
# y ProductoConDescuento(Producto) que sobrescriba precio_final().
# Después hacé Compra, que contiene una lista de productos y un método
# factura() que imprima cada línea y el total. Compra no debe preguntar
# de qué tipo es cada producto: le pide precio_final() a todos por
# igual y el polimorfismo hace el resto.
# -------------------------------------------------------------------------

class Producto:
    """Producto cuyo precio final es su precio de lista."""

    def __init__(self, nombre, precio):
        self._nombre = nombre
        self._precio = precio

    def nombre(self):
        """Devuelve el nombre del producto."""
        return self._nombre

    def precio_final(self):
        """Precio a cobrar por una unidad."""
        return self._precio


class ProductoConDescuento(Producto):
    """Producto cuyo precio final aplica un descuento."""

    def __init__(self, nombre, precio, descuento):
        super().__init__(nombre, precio)
        self._descuento = descuento

    def precio_final(self):
        return self._precio * (1 - self._descuento / 100)


class Compra:
    """Compra que factura sus productos polimórficamente."""

    def __init__(self):
        self._productos = []

    def agregar(self, producto):
        """Suma un producto a la compra."""
        self._productos.append(producto)

    def total(self):
        """Suma los precios finales de todos los productos."""
        return sum(
            producto.precio_final()
            for producto in self._productos
        )

    def factura(self):
        """Imprime el detalle de la compra y su total."""
        print("=== FACTURA ===")

        for producto in self._productos:
            print(
                f"  {producto.nombre()}: "
                f"${producto.precio_final():.2f}"
            )

        print(f"TOTAL: ${self.total():.2f}")


if __name__ == "__main__":
    compra = Compra()
    compra.agregar(Producto("Yerba", 3500))
    compra.agregar(ProductoConDescuento("Leche", 800, 20))
    compra.agregar(Producto("Pan", 1200))

    compra.factura()
```

## `enunciado_20.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Integrador: armá la iteración 4 del banco. Persona guarda identidad,
# Movimiento registra una operación, Cuenta administra saldo y su
# historial de movimientos, y Banco hace el ABM de cuentas. Cada clase
# tiene una sola responsabilidad y ninguna se mete con las otras.
#
# En un proyecto real esto va en archivos separados: errores.py,
# personas.py, movimientos.py, cuentas.py, banco.py y main.py. Acá está
# todo junto para poder copiarlo de una, pero los comentarios marcan
# dónde estaría el corte de cada módulo.
# -------------------------------------------------------------------------

# --- errores.py ------------------------------------------------

class SaldoInsuficienteError(Exception):
    """Indica que la cuenta no tiene fondos para la operación."""

    pass


class MontoInvalidoError(Exception):
    """Indica que el monto de la operación no es válido."""

    pass


class CuentaNoEncontrada(Exception):
    """Indica que no existe la cuenta solicitada."""

    pass


class NumeroDuplicadoError(Exception):
    """Indica que el número de cuenta ya está usado."""

    pass


# --- personas.py -----------------------------------------------

class Persona:
    """Titular de una cuenta. Solo maneja identidad."""

    def __init__(self, nombre, apellido, dni):
        self._nombre = nombre
        self._apellido = apellido
        self._dni = dni

    def dni(self):
        """Devuelve el documento del titular."""
        return self._dni

    def __str__(self):
        return f"{self._apellido}, {self._nombre}"


# --- movimientos.py --------------------------------------------

class Movimiento:
    """Registro de una operación sobre una cuenta."""

    def __init__(self, tipo, monto, saldo_resultante):
        self._tipo = tipo
        self._monto = monto
        self._saldo_resultante = saldo_resultante

    def __str__(self):
        return (
            f"{self._tipo:<10} ${self._monto:>10} "
            f"-> saldo ${self._saldo_resultante}"
        )


# --- cuentas.py ------------------------------------------------

class Cuenta:
    """Cuenta que administra su saldo y su historial."""

    def __init__(self, numero, titular, saldo=0):
        self._numero = numero
        self._titular = titular
        self._saldo = saldo
        self._movimientos = []

    def numero(self):
        """Devuelve el número de cuenta."""
        return self._numero

    def saldo(self):
        """Devuelve el saldo actual."""
        return self._saldo

    def depositar(self, monto):
        """Acredita un monto positivo y lo registra."""
        if monto <= 0:
            raise MontoInvalidoError(
                "El monto debe ser positivo"
            )

        self._saldo += monto
        self._registrar("depósito", monto)

    def extraer(self, monto):
        """Debita un monto si el saldo alcanza y lo registra."""
        if monto <= 0:
            raise MontoInvalidoError(
                "El monto debe ser positivo"
            )

        if monto > self._saldo:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente en {self._numero}"
            )

        self._saldo -= monto
        self._registrar("extracción", monto)

    def _registrar(self, tipo, monto):
        """Agrega un movimiento al historial de la cuenta."""
        self._movimientos.append(
            Movimiento(tipo, monto, self._saldo)
        )

    def historial(self):
        """Devuelve los movimientos de la cuenta."""
        return list(self._movimientos)

    def __str__(self):
        return (
            f"[{self._numero}] {self._titular} "
            f"- ${self._saldo}"
        )


# --- banco.py --------------------------------------------------

class Banco:
    """Banco que hace el ABM de cuentas. No calcula saldos."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._cuentas = {}

    def abrir_cuenta(self, numero, titular, saldo=0):
        """Da de alta una cuenta nueva y la devuelve."""
        if numero in self._cuentas:
            raise NumeroDuplicadoError(
                f"La cuenta {numero} ya existe"
            )

        cuenta = Cuenta(numero, titular, saldo)
        self._cuentas[numero] = cuenta

        return cuenta

    def buscar(self, numero):
        """Devuelve la cuenta pedida o lanza excepción."""
        cuenta = self._cuentas.get(numero)

        if cuenta is None:
            raise CuentaNoEncontrada(
                f"No existe la cuenta {numero}"
            )

        return cuenta

    def cerrar_cuenta(self, numero):
        """Da de baja física la cuenta indicada."""
        self.buscar(numero)
        del self._cuentas[numero]

    def listar(self):
        """Devuelve todas las cuentas del banco."""
        return list(self._cuentas.values())

    def total_depositado(self):
        """Suma los saldos de todas las cuentas."""
        return sum(
            cuenta.saldo() for cuenta in self.listar()
        )


# --- main.py ---------------------------------------------------

if __name__ == "__main__":
    banco = Banco("Banco de La Plata")

    ana = Persona("Ana", "Pérez", "12345678")
    juan = Persona("Juan", "Gómez", "87654321")

    cuenta_ana = banco.abrir_cuenta("001-100", ana, 10000)
    banco.abrir_cuenta("001-101", juan, 5000)

    cuenta_ana.depositar(2500)
    cuenta_ana.extraer(4000)

    for cuenta in banco.listar():
        print(cuenta)

    print(f"Total depositado: ${banco.total_depositado()}")

    print(f"Historial de {cuenta_ana.numero()}:")
    for movimiento in cuenta_ana.historial():
        print(f"  {movimiento}")

    try:
        cuenta_ana.extraer(999999)
    except SaldoInsuficienteError as error:
        print(f"Error: {error}")

    try:
        banco.buscar("001-999")
    except CuentaNoEncontrada as error:
        print(f"Error: {error}")
```

# Ejercicios intercalados en el texto

## `ejercicio_01.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Modelá una Casa que tiene un objeto Direccion como atributo, con
# calle, número y ciudad. Después imprimí la casa incluyendo la
# dirección completa. No uses herencia: una Casa no es una dirección,
# tiene una.
# -------------------------------------------------------------------------

class Direccion:
    """Dirección postal, pensada para vivir dentro de otras clases."""

    def __init__(self, calle, numero, ciudad):
        self._calle = calle
        self._numero = numero
        self._ciudad = ciudad

    def __str__(self):
        return f"{self._calle} {self._numero}, {self._ciudad}"


class Casa:
    """Casa compuesta por un objeto Direccion."""

    def __init__(self, dueno, direccion):
        self._dueno = dueno
        self._direccion = direccion

    def __str__(self):
        return f"Casa de {self._dueno} en {self._direccion}"


if __name__ == "__main__":
    direccion = Direccion("Av. 7", 1234, "La Plata")
    casa = Casa("Ana Perez", direccion)

    print(casa)
```

## `ejercicio_02.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Creá una sola Direccion y dos Personas que la compartan. Mudá la
# dirección con mudar() y comprobá que las dos personas ven el cambio:
# guardan una referencia al mismo objeto, no una copia. Después hacé lo
# mismo con copy.deepcopy y verificá que ahí sí quedan independientes.
# -------------------------------------------------------------------------

import copy


class Direccion:
    """Dirección postal que puede cambiar de valores."""

    def __init__(self, calle, numero, ciudad):
        self._calle = calle
        self._numero = numero
        self._ciudad = ciudad

    def mudar(self, calle, numero):
        """Cambia calle y número conservando la ciudad."""
        self._calle = calle
        self._numero = numero

    def __str__(self):
        return f"{self._calle} {self._numero}, {self._ciudad}"


class Persona:
    """Persona que tiene una Direccion."""

    def __init__(self, nombre, direccion):
        self._nombre = nombre
        self._direccion = direccion

    def __str__(self):
        return f"{self._nombre}: {self._direccion}"


if __name__ == "__main__":
    familiar = Direccion("Av. 7", 1234, "La Plata")

    madre = Persona("Ana", familiar)
    hijo = Persona("Pedro", familiar)

    print("Antes de la mudanza:")
    print(f"  {madre}")
    print(f"  {hijo}")

    familiar.mudar("Calle 50", 900)

    print("Después de la mudanza (cambiaron los dos):")
    print(f"  {madre}")
    print(f"  {hijo}")

    # Con una copia profunda, la dirección del hijo es otro objeto.
    independiente = Persona("Lucía", copy.deepcopy(familiar))
    familiar.mudar("Diagonal 74", 55)

    print("Con deepcopy, Lucía no se entera del cambio:")
    print(f"  {madre}")
    print(f"  {independiente}")
```

## `ejercicio_03.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Modelá una clase Curso que tiene un nombre y una lista de Alumno.
# Cada Alumno tiene nombre y legajo. Agregá los métodos
# inscribir(alumno), cantidad_inscriptos() y listar_alumnos(). El
# nombre del curso se muestra con __str__, no leyendo el atributo
# desde afuera.
# -------------------------------------------------------------------------

class Alumno:
    """Alumno identificado por nombre y legajo."""

    def __init__(self, nombre, legajo):
        self._nombre = nombre
        self._legajo = legajo

    def __str__(self):
        return f"[{self._legajo}] {self._nombre}"


class Curso:
    """Curso que contiene una colección de alumnos."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._alumnos = []

    def inscribir(self, alumno):
        """Agrega un alumno a la lista de inscriptos."""
        self._alumnos.append(alumno)

    def cantidad_inscriptos(self):
        """Devuelve cuántos alumnos hay inscriptos."""
        return len(self._alumnos)

    def listar_alumnos(self):
        """Imprime todos los alumnos inscriptos."""
        for alumno in self._alumnos:
            print(f"  {alumno}")

    def __str__(self):
        return (
            f"Inscriptos en {self._nombre}: "
            f"{self.cantidad_inscriptos()}"
        )


if __name__ == "__main__":
    curso = Curso("Programación 2")
    curso.inscribir(Alumno("Ana", "L-001"))
    curso.inscribir(Alumno("Juan", "L-002"))
    curso.inscribir(Alumno("Pedro", "L-003"))

    print(curso)
    curso.listar_alumnos()
```

## `ejercicio_04.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Escribí un módulo de validaciones con es_dni_valido(dni) y
# normalizar_nombre(nombre), y poné toda la prueba dentro de
# if __name__ == "__main__":. Imprimí el valor de __name__ para ver la
# diferencia: si ejecutás el archivo vale "__main__" y la prueba corre;
# si otro archivo hace "import ejercicio_04", vale "ejercicio_04" y la
# prueba no corre.
# -------------------------------------------------------------------------

def es_dni_valido(dni):
    """Indica si el DNI es una cadena de 7 u 8 dígitos."""
    return (
        isinstance(dni, str)
        and dni.isdigit()
        and len(dni) in (7, 8)
    )


def normalizar_nombre(nombre):
    """Devuelve el nombre sin espacios sobrantes y capitalizado."""
    return nombre.strip().title()


if __name__ == "__main__":
    print(f'__name__ vale "{__name__}"')

    for dni in ["12345678", "1234", "12a45678", 12345678]:
        print(f"  {dni!r}: {es_dni_valido(dni)}")

    print(normalizar_nombre("  ana maría pérez  "))
```

## `ejercicio_05.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Implementá un gestor de productos con ABM completo. Cada Producto
# tiene codigo, nombre, precio y stock. Usá un diccionario interno en
# Almacen, con alta, consulta, listado, actualización de precio,
# reposición de stock y baja. Creá excepciones propias para código
# duplicado y producto no encontrado, y reutilizá buscar() dentro de
# los métodos que necesitan encontrar un producto.
# -------------------------------------------------------------------------

class ProductoNoEncontrado(Exception):
    """Indica que no existe el producto solicitado."""

    pass


class CodigoDuplicadoError(Exception):
    """Indica que el código del producto ya existe."""

    pass


class Producto:
    """Producto identificado por un código."""

    def __init__(self, codigo, nombre, precio, stock):
        self._codigo = codigo
        self._nombre = nombre
        self._precio = precio
        self._stock = stock

    def cambiar_precio(self, nuevo_precio):
        """Actualiza el precio de venta."""
        if nuevo_precio <= 0:
            raise ValueError("El precio debe ser positivo")

        self._precio = nuevo_precio

    def reponer(self, cantidad):
        """Suma unidades al stock disponible."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")

        self._stock += cantidad

    def __str__(self):
        return (
            f"[{self._codigo}] {self._nombre} - "
            f"${self._precio} (stock: {self._stock})"
        )


class Almacen:
    """Gestiona un ABM de productos indexados por código."""

    def __init__(self):
        self._productos = {}

    def dar_de_alta(self, codigo, nombre, precio, stock):
        """Da de alta un producto nuevo y lo devuelve."""
        if codigo in self._productos:
            raise CodigoDuplicadoError(
                f"Ya existe un producto con código {codigo}"
            )

        producto = Producto(codigo, nombre, precio, stock)
        self._productos[codigo] = producto

        return producto

    def buscar(self, codigo):
        """Devuelve el producto pedido o lanza excepción."""
        producto = self._productos.get(codigo)

        if producto is None:
            raise ProductoNoEncontrado(
                f"No existe el código {codigo}"
            )

        return producto

    def listar(self):
        """Devuelve todos los productos del almacén."""
        return list(self._productos.values())

    def actualizar_precio(self, codigo, nuevo_precio):
        """Le pide al producto que cambie su precio."""
        self.buscar(codigo).cambiar_precio(nuevo_precio)

    def reponer_stock(self, codigo, cantidad):
        """Le pide al producto que sume stock."""
        self.buscar(codigo).reponer(cantidad)

    def dar_de_baja(self, codigo):
        """Elimina físicamente el producto indicado."""
        self.buscar(codigo)
        del self._productos[codigo]


if __name__ == "__main__":
    almacen = Almacen()
    almacen.dar_de_alta("P-001", "Yerba", 3500, 20)
    almacen.dar_de_alta("P-002", "Leche", 800, 15)

    almacen.actualizar_precio("P-001", 4000)
    almacen.reponer_stock("P-001", 10)
    almacen.dar_de_baja("P-002")

    for producto in almacen.listar():
        print(producto)

    try:
        almacen.dar_de_alta("P-001", "Otra yerba", 3000, 5)
    except CodigoDuplicadoError as error:
        print(f"Error: {error}")

    try:
        almacen.buscar("P-002")
    except ProductoNoEncontrado as error:
        print(f"Error: {error}")
```

## `ejercicio_06.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Agenda con ABM completo de contactos. Cada Contacto
# tiene nombre y telefono. Agregá agregar_contacto(), buscar(),
# listar(), actualizar_telefono() y eliminar(). Usá las excepciones
# propias ContactoNoEncontrado y NombreDuplicadoError.
# -------------------------------------------------------------------------

class ContactoNoEncontrado(Exception):
    """Indica que no existe el contacto solicitado."""

    pass


class NombreDuplicadoError(Exception):
    """Indica que el nombre ya existe en la agenda."""

    pass


class Contacto:
    """Contacto con nombre y teléfono."""

    def __init__(self, nombre, telefono):
        self._nombre = nombre
        self._telefono = telefono

    def cambiar_telefono(self, nuevo_telefono):
        """Actualiza el teléfono del contacto."""
        self._telefono = nuevo_telefono

    def __str__(self):
        return f"{self._nombre}: {self._telefono}"


class Agenda:
    """Gestiona un ABM de contactos indexados por nombre."""

    def __init__(self):
        self._contactos = {}

    def agregar_contacto(self, nombre, telefono):
        """Da de alta un contacto nuevo y lo devuelve."""
        if nombre in self._contactos:
            raise NombreDuplicadoError(
                f"{nombre} ya existe en la agenda"
            )

        contacto = Contacto(nombre, telefono)
        self._contactos[nombre] = contacto

        return contacto

    def buscar(self, nombre):
        """Devuelve el contacto pedido o lanza excepción."""
        contacto = self._contactos.get(nombre)

        if contacto is None:
            raise ContactoNoEncontrado(
                f"No hay contacto llamado {nombre}"
            )

        return contacto

    def listar(self):
        """Devuelve todos los contactos de la agenda."""
        return list(self._contactos.values())

    def actualizar_telefono(self, nombre, nuevo_telefono):
        """Le pide al contacto que cambie su teléfono."""
        self.buscar(nombre).cambiar_telefono(nuevo_telefono)

    def eliminar(self, nombre):
        """Elimina el contacto indicado de la agenda."""
        self.buscar(nombre)
        del self._contactos[nombre]


if __name__ == "__main__":
    agenda = Agenda()
    agenda.agregar_contacto("Ana", "221-1234")
    agenda.agregar_contacto("Juan", "221-5678")

    agenda.actualizar_telefono("Ana", "221-9999")
    agenda.eliminar("Juan")

    for contacto in agenda.listar():
        print(contacto)

    try:
        agenda.buscar("Juan")
    except ContactoNoEncontrado as error:
        print(f"Error: {error}")
```

## `ejercicio_07.py`

```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# SRP: te dan una clase Biblioteca que gestiona libros, los imprime por
# pantalla y además los exporta a CSV. Son tres razones distintas para
# cambiarla. Partila en tres clases: Biblioteca, que solo administra la
# colección; MostradorDeLibros, que sabe imprimir; y ExportadorCsv, que
# sabe armar el texto CSV. Fijate que ninguna de las tres necesita
# conocer el trabajo de las otras dos.
# -------------------------------------------------------------------------

class Libro:
    """Libro con título, autor e ISBN."""

    def __init__(self, isbn, titulo, autor):
        self._isbn = isbn
        self._titulo = titulo
        self._autor = autor

    def isbn(self):
        """Devuelve el ISBN del libro."""
        return self._isbn

    def titulo(self):
        """Devuelve el título del libro."""
        return self._titulo

    def autor(self):
        """Devuelve el autor del libro."""
        return self._autor

    def __str__(self):
        return f"'{self._titulo}' de {self._autor}"


class Biblioteca:
    """Única responsabilidad: administrar la colección."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._libros = {}

    def nombre(self):
        """Devuelve el nombre de la biblioteca."""
        return self._nombre

    def agregar(self, libro):
        """Suma un libro al catálogo."""
        self._libros[libro.isbn()] = libro

    def listar(self):
        """Devuelve todos los libros del catálogo."""
        return list(self._libros.values())


class MostradorDeLibros:
    """Única responsabilidad: presentar libros por pantalla."""

    def mostrar(self, biblioteca):
        """Imprime el catálogo de una biblioteca."""
        print(f"{biblioteca.nombre()}")

        for libro in biblioteca.listar():
            print(f"  - {libro}")


class ExportadorCsv:
    """Única responsabilidad: representar libros como CSV."""

    def exportar(self, biblioteca):
        """Devuelve el catálogo como texto CSV."""
        lineas = ["isbn,titulo,autor"]

        for libro in biblioteca.listar():
            lineas.append(
                f"{libro.isbn()},{libro.titulo()},"
                f"{libro.autor()}"
            )

        return "\n".join(lineas)


if __name__ == "__main__":
    biblioteca = Biblioteca("Biblioteca Central")
    biblioteca.agregar(
        Libro("978-987-1", "El Aleph", "Borges")
    )
    biblioteca.agregar(
        Libro("978-987-2", "Rayuela", "Cortázar")
    )

    MostradorDeLibros().mostrar(biblioteca)

    print()
    print(ExportadorCsv().exportar(biblioteca))
```
