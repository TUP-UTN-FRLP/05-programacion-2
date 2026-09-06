# Ejercicios integradores

> **Convención del capítulo.** Todos los atributos se declaran
> protegidos (`_nombre`, `_saldo`) siguiendo lo visto en el capítulo 10.
> El código de prueba nunca los lee directamente: interactúa con los
> objetos a través de sus métodos o de `__str__`.

## `enunciado_01.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Definí una clase Vehiculo con atributos marca y modelo, y un método
# descripcion() que los imprima. Después definí Moto(Vehiculo) con un
# atributo extra cilindrada. Usá super() en el __init__. Sobrescribí
# descripcion() para que llame a la del padre y agregue la cilindrada.
# -------------------------------------------------------------------------

class Vehiculo:
    """Vehículo con marca y modelo."""

    def __init__(self, marca, modelo):
        self._marca = marca
        self._modelo = modelo

    def descripcion(self):
        """Imprime los datos comunes a todo vehículo."""
        print(f"{self._marca} {self._modelo}")


class Moto(Vehiculo):
    """Moto que agrega la cilindrada al vehículo base."""

    def __init__(self, marca, modelo, cilindrada):
        super().__init__(marca, modelo)
        self._cilindrada = cilindrada

    def descripcion(self):
        """Extiende la descripción del padre con la cilindrada."""
        super().descripcion()
        print(f"Cilindrada: {self._cilindrada}cc")


vehiculo = Vehiculo("Ford", "Focus")
moto = Moto("Honda", "CBR", 600)

vehiculo.descripcion()
print()
moto.descripcion()
```

## `enunciado_02.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Definí una clase Persona con nombre y edad. Hacé Estudiante(Persona)
# que agrega carrera. Sobrescribí __str__ para que la persona imprima
# "Nombre (Edad años)" y el estudiante "Nombre (Edad años, Carrera)".
# Acá la hija reemplaza el formato completo del padre.
# -------------------------------------------------------------------------

class Persona:
    """Persona con nombre y edad."""

    def __init__(self, nombre, edad):
        self._nombre = nombre
        self._edad = edad

    def __str__(self):
        return f"{self._nombre} ({self._edad} años)"


class Estudiante(Persona):
    """Persona que agrega una carrera."""

    def __init__(self, nombre, edad, carrera):
        super().__init__(nombre, edad)
        self._carrera = carrera

    def __str__(self):
        return (
            f"{self._nombre} ({self._edad} años, {self._carrera})"
        )


persona = Persona("Juan", 40)
estudiante = Estudiante("Ana", 22, "Ingeniería")

print(persona)
print(estudiante)
```

## `enunciado_03.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Continuando el ejercicio 2, hacé Profesor(Persona) que agrega materia
# y antiguedad. Sobrescribí __str__. Después creá una lista con dos
# estudiantes y dos profesores. Recorré e imprimí cada uno: el bucle es
# el mismo para todos y cada objeto imprime su propio formato.
# -------------------------------------------------------------------------

class Persona:
    """Persona con nombre y edad."""

    def __init__(self, nombre, edad):
        self._nombre = nombre
        self._edad = edad

    def __str__(self):
        return f"{self._nombre} ({self._edad} años)"


class Estudiante(Persona):
    """Persona que agrega una carrera."""

    def __init__(self, nombre, edad, carrera):
        super().__init__(nombre, edad)
        self._carrera = carrera

    def __str__(self):
        return (
            f"{self._nombre} ({self._edad} años, {self._carrera})"
        )


class Profesor(Persona):
    """Persona que agrega materia y antigüedad docente."""

    def __init__(self, nombre, edad, materia, antiguedad):
        super().__init__(nombre, edad)
        self._materia = materia
        self._antiguedad = antiguedad

    def __str__(self):
        return (
            f"{self._nombre} ({self._edad} años, "
            f"enseña {self._materia}, "
            f"{self._antiguedad} años de antigüedad)"
        )


gente = [
    Estudiante("Ana", 22, "Ingeniería"),
    Estudiante("Pedro", 20, "Matemática"),
    Profesor("Juan", 45, "Programación 2", 10),
    Profesor("Lucía", 50, "Investigación Operativa", 15),
]

for persona in gente:
    print(persona)
```

## `enunciado_04.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Figura con un método abstracto conceptual area(), que
# lanza NotImplementedError informando el nombre de la clase concreta.
# Definí tres hijas: Cuadrado(lado), Rectangulo(base, altura) y
# Triangulo(base, altura). Cada una implementa area(). Comprobá también
# qué pasa si alguien instancia Figura y le pide el área.
# -------------------------------------------------------------------------

class Figura:
    """Figura base cuyo cálculo de área debe implementar cada hija."""

    def area(self):
        """Contrato que toda figura concreta debe cumplir."""
        raise NotImplementedError(
            f"La clase {type(self).__name__} debe implementar area()"
        )


class Cuadrado(Figura):
    """Cuadrado definido por su lado."""

    def __init__(self, lado):
        self._lado = lado

    def area(self):
        """Devuelve lado al cuadrado."""
        return self._lado ** 2


class Rectangulo(Figura):
    """Rectángulo definido por base y altura."""

    def __init__(self, base, altura):
        self._base = base
        self._altura = altura

    def area(self):
        """Devuelve base por altura."""
        return self._base * self._altura


class Triangulo(Figura):
    """Triángulo definido por base y altura."""

    def __init__(self, base, altura):
        self._base = base
        self._altura = altura

    def area(self):
        """Devuelve base por altura sobre dos."""
        return self._base * self._altura / 2


print(Cuadrado(4).area())
print(Rectangulo(5, 3).area())
print(Triangulo(6, 4).area())

# Figura se puede instanciar: NotImplementedError avisa recién al
# llamar area(). Bloquear la instanciación es tema del capítulo 13.
try:
    Figura().area()
except NotImplementedError as error:
    print(f"Error esperado: {error}")
```

## `enunciado_05.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Continuando el ejercicio 4, creá una lista con figuras mixtas y
# calculá el área total sumando area() de cada una. El código que suma
# no debe preguntar de qué tipo es cada figura: eso es polimorfismo.
# -------------------------------------------------------------------------

class Figura:
    """Figura base cuyo cálculo de área debe implementar cada hija."""

    def area(self):
        """Contrato que toda figura concreta debe cumplir."""
        raise NotImplementedError(
            f"La clase {type(self).__name__} debe implementar area()"
        )


class Cuadrado(Figura):
    """Cuadrado definido por su lado."""

    def __init__(self, lado):
        self._lado = lado

    def area(self):
        """Devuelve lado al cuadrado."""
        return self._lado ** 2


class Rectangulo(Figura):
    """Rectángulo definido por base y altura."""

    def __init__(self, base, altura):
        self._base = base
        self._altura = altura

    def area(self):
        """Devuelve base por altura."""
        return self._base * self._altura


class Triangulo(Figura):
    """Triángulo definido por base y altura."""

    def __init__(self, base, altura):
        self._base = base
        self._altura = altura

    def area(self):
        """Devuelve base por altura sobre dos."""
        return self._base * self._altura / 2


figuras = [
    Cuadrado(4),
    Rectangulo(5, 3),
    Triangulo(6, 4),
]

total = sum(figura.area() for figura in figuras)
print(f"Área total: {total}")
```

## `enunciado_06.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Animal con nombre y un método sonido() que devuelve
# "...". Hacé Perro(Animal), Gato(Animal) y Vaca(Animal) que
# sobrescriban sonido() con "Guau", "Miau" y "Muu". Recorré una lista
# mixta que incluya también un Animal genérico y hacé que cada uno
# hable: el genérico responde con la versión heredada del padre.
# -------------------------------------------------------------------------

class Animal:
    """Animal base con nombre y sonido genérico."""

    def __init__(self, nombre):
        self._nombre = nombre

    def sonido(self):
        """Sonido por defecto de un animal sin especializar."""
        return "..."

    def hablar(self):
        """Imprime el nombre del animal junto a su sonido."""
        print(f"{self._nombre} dice: {self.sonido()}")


class Perro(Animal):
    """Animal cuyo sonido es Guau."""

    def sonido(self):
        return "Guau"


class Gato(Animal):
    """Animal cuyo sonido es Miau."""

    def sonido(self):
        return "Miau"


class Vaca(Animal):
    """Animal cuyo sonido es Muu."""

    def sonido(self):
        return "Muu"


animales = [
    Perro("Firulais"),
    Gato("Michi"),
    Vaca("Lola"),
    Animal("Bicho"),
]

for animal in animales:
    animal.hablar()
```

## `enunciado_07.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Empleado con nombre y método sueldo() que devuelve 0.
# Hacé EmpleadoAsalariado(nombre, sueldo_fijo) y
# EmpleadoComision(nombre, base, ventas, porcentaje). Las dos
# sobrescriben sueldo(). Listá la plantilla y calculá el gasto total
# recorriendo la lista una sola vez, sin preguntar tipos.
# -------------------------------------------------------------------------

class Empleado:
    """Empleado base con sueldo genérico."""

    def __init__(self, nombre):
        self._nombre = nombre

    def sueldo(self):
        """Sueldo por defecto de un empleado sin especializar."""
        return 0

    def __str__(self):
        return f"{self._nombre}: ${self.sueldo():.2f}"


class EmpleadoAsalariado(Empleado):
    """Empleado con sueldo fijo mensual."""

    def __init__(self, nombre, sueldo_fijo):
        super().__init__(nombre)
        self._sueldo_fijo = sueldo_fijo

    def sueldo(self):
        return self._sueldo_fijo


class EmpleadoComision(Empleado):
    """Empleado con sueldo base más comisión sobre ventas."""

    def __init__(self, nombre, base, ventas, porcentaje):
        super().__init__(nombre)
        self._base = base
        self._ventas = ventas
        self._porcentaje = porcentaje

    def sueldo(self):
        comision = self._ventas * self._porcentaje / 100
        return self._base + comision


plantilla = [
    EmpleadoAsalariado("Ana", 500000),
    EmpleadoComision("Juan", 200000, 3000000, 5),
    EmpleadoAsalariado("Pedro", 800000),
]

for empleado in plantilla:
    print(empleado)

total = sum(empleado.sueldo() for empleado in plantilla)
print(f"Gasto total: ${total:.2f}")
```

## `enunciado_08.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Te dan este bucle, que pregunta el tipo antes de actuar:
#
#     for cliente in clientes:
#         if isinstance(cliente, ClienteVIP):
#             descuento = 20
#         elif isinstance(cliente, ClientePremium):
#             descuento = 35
#         else:
#             descuento = 0
#         print(cliente._nombre, descuento)
#
# Reescribilo con polimorfismo: cada clase debe saber su propio
# descuento(). El bucle final no debe preguntar ningún tipo, y agregar
# una categoría nueva no debe obligar a tocarlo.
# -------------------------------------------------------------------------

class Cliente:
    """Cliente sin beneficios: no tiene descuento."""

    def __init__(self, nombre):
        self._nombre = nombre

    def descuento(self):
        """Porcentaje de descuento de la categoría."""
        return 0

    def __str__(self):
        return f"{self._nombre}: {self.descuento()}% de descuento"


class ClienteVIP(Cliente):
    """Cliente con 20 por ciento de descuento."""

    def descuento(self):
        return 20


class ClientePremium(Cliente):
    """Cliente con 35 por ciento de descuento."""

    def descuento(self):
        return 35


class ClienteMayorista(Cliente):
    """Categoría agregada después: el bucle no cambió."""

    def descuento(self):
        return 40


clientes = [
    Cliente("Ana"),
    ClienteVIP("Juan"),
    ClientePremium("Pedro"),
    ClienteMayorista("Lucía"),
]

for cliente in clientes:
    print(cliente)
```

## `enunciado_09.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Producto con nombre, precio y un método precio_final()
# que devuelve el precio. Hacé ProductoConIVA(Producto) que sobrescriba
# precio_final() agregando 21% de IVA, y ProductoImportado que agregue
# un 15% de arancel sobre el anterior. Fijate cómo cada super() encadena
# con el nivel inmediatamente superior.
#
# Ojo con el diseño: la prueba del "es un" acá no se sostiene del todo.
# Un producto importado no "es un" producto con IVA: el IVA es una regla
# fiscal, no un tipo de producto. Sirve para ver super() en cadena, pero
# en el capítulo 12 vamos a modelarlo mejor con composición.
# -------------------------------------------------------------------------

class Producto:
    """Producto con precio base."""

    def __init__(self, nombre, precio):
        self._nombre = nombre
        self._precio = precio

    def precio_final(self):
        """Precio sin recargos."""
        return self._precio

    def __str__(self):
        return f"{self._nombre}: ${self.precio_final():.2f}"


class ProductoConIVA(Producto):
    """Producto que agrega 21 por ciento de IVA."""

    def precio_final(self):
        return super().precio_final() * 1.21


class ProductoImportado(ProductoConIVA):
    """Producto que agrega un arancel sobre el precio con IVA."""

    def precio_final(self):
        return super().precio_final() * 1.15


producto = Producto("Yerba", 3000)
producto_iva = ProductoConIVA("Bebida", 3000)
importado = ProductoImportado("Whisky", 3000)

print(producto)
print(producto_iva)
print(importado)
```

## `enunciado_10.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Forma3D con un método abstracto conceptual volumen().
# Definí Cubo(lado), Esfera(radio) y Cilindro(radio, altura). Cada una
# implementa volumen() con su fórmula. Recorré una lista mixta y mostrá
# el volumen de cada una redondeado a dos decimales.
# -------------------------------------------------------------------------

import math


class Forma3D:
    """Forma tridimensional cuyo volumen implementan sus hijas."""

    def volumen(self):
        """Contrato que toda forma concreta debe cumplir."""
        raise NotImplementedError(
            f"La clase {type(self).__name__} debe implementar volumen()"
        )

    def __str__(self):
        return f"{type(self).__name__}: {self.volumen():.2f}"


class Cubo(Forma3D):
    """Cubo definido por la longitud de su lado."""

    def __init__(self, lado):
        self._lado = lado

    def volumen(self):
        return self._lado ** 3


class Esfera(Forma3D):
    """Esfera definida por su radio."""

    def __init__(self, radio):
        self._radio = radio

    def volumen(self):
        return 4 / 3 * math.pi * self._radio ** 3


class Cilindro(Forma3D):
    """Cilindro definido por radio y altura."""

    def __init__(self, radio, altura):
        self._radio = radio
        self._altura = altura

    def volumen(self):
        return math.pi * self._radio ** 2 * self._altura


formas = [
    Cubo(3),
    Esfera(2),
    Cilindro(2, 5),
]

for forma in formas:
    print(forma)
```

## `enunciado_11.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Notificacion con mensaje y un método
# enviar(destinatario) que imprime "Enviando a X: mensaje". Hacé
# NotificacionEmail, NotificacionSMS y NotificacionPush que sobrescriban
# enviar() con el mismo dato pero formatos distintos. Probá las cuatro.
# -------------------------------------------------------------------------

class Notificacion:
    """Notificación base con un mensaje."""

    def __init__(self, mensaje):
        self._mensaje = mensaje

    def enviar(self, destinatario):
        """Envía el mensaje con el formato genérico."""
        print(f"Enviando a {destinatario}: {self._mensaje}")


class NotificacionEmail(Notificacion):
    """Notificación enviada por correo electrónico."""

    def enviar(self, destinatario):
        print(f"[EMAIL] a {destinatario}: {self._mensaje}")


class NotificacionSMS(Notificacion):
    """Notificación enviada por SMS."""

    def enviar(self, destinatario):
        print(f"[SMS] a {destinatario}: {self._mensaje}")


class NotificacionPush(Notificacion):
    """Notificación enviada como aviso push."""

    def enviar(self, destinatario):
        print(f"[PUSH] a {destinatario}: {self._mensaje}")


avisos = [
    Notificacion("Aviso genérico"),
    NotificacionEmail("Bienvenido"),
    NotificacionSMS("Su código es 1234"),
    NotificacionPush("Tenés un mensaje nuevo"),
]

for aviso in avisos:
    aviso.enviar("ana@correo.com")
```

## `enunciado_12.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Con las clases del ejercicio 11, hacé una función
# enviar_a_todos(notificacion, destinatarios) que recorra la lista de
# destinatarios, cadenas de texto, y para cada uno llame al enviar() de
# la notificación recibida. La misma función debe servir para cualquiera
# de los cuatro tipos: es polimorfismo por parámetro.
# -------------------------------------------------------------------------

class Notificacion:
    """Notificación base con un mensaje."""

    def __init__(self, mensaje):
        self._mensaje = mensaje

    def enviar(self, destinatario):
        """Envía el mensaje con el formato genérico."""
        print(f"Enviando a {destinatario}: {self._mensaje}")


class NotificacionEmail(Notificacion):
    """Notificación enviada por correo electrónico."""

    def enviar(self, destinatario):
        print(f"[EMAIL] a {destinatario}: {self._mensaje}")


class NotificacionSMS(Notificacion):
    """Notificación enviada por SMS."""

    def enviar(self, destinatario):
        print(f"[SMS] a {destinatario}: {self._mensaje}")


class NotificacionPush(Notificacion):
    """Notificación enviada como aviso push."""

    def enviar(self, destinatario):
        print(f"[PUSH] a {destinatario}: {self._mensaje}")


def enviar_a_todos(notificacion, destinatarios):
    """Envía una misma notificación a cada destinatario."""
    for destinatario in destinatarios:
        notificacion.enviar(destinatario)


destinatarios = [
    "ana@correo.com",
    "juan@correo.com",
    "pedro@correo.com",
]

enviar_a_todos(NotificacionEmail("Bienvenidos al banco"), destinatarios)
print()
enviar_a_todos(NotificacionSMS("Su código es 1234"), destinatarios)
```

## `enunciado_13.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Cuenta con titular y saldo, un método comision() que
# devuelve 50 y un método extraer(monto) que valida que haya saldo
# suficiente, descuenta monto más comision() e informa el resultado.
# Hacé CuentaVIP(Cuenta) que sobrescriba únicamente comision() para
# devolver 0. Fijate que no hace falta reescribir extraer(): el padre
# llama a self.comision() y Python resuelve cuál usar según el objeto.
# -------------------------------------------------------------------------

class Cuenta:
    """Cuenta que cobra una comisión fija en cada extracción."""

    def __init__(self, titular, saldo):
        self._titular = titular
        self._saldo = saldo

    def comision(self):
        """Costo fijo que cobra el banco por extraer."""
        return 50

    def extraer(self, monto):
        """Extrae monto más comisión si el saldo alcanza."""
        if monto <= 0:
            print("El monto debe ser positivo")
            return False
        total = monto + self.comision()
        if total > self._saldo:
            print(f"{self._titular}: saldo insuficiente")
            return False
        self._saldo -= total
        print(
            f"{self._titular}: extrajo ${monto}, "
            f"comisión ${self.comision()}, saldo ${self._saldo}"
        )
        return True


class CuentaVIP(Cuenta):
    """Cuenta que no paga comisión por extraer."""

    def comision(self):
        return 0


cuenta = Cuenta("Ana", 1000)
vip = CuentaVIP("Pedro", 1000)

cuenta.extraer(100)
vip.extraer(100)
cuenta.extraer(5000)
```

## `enunciado_14.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Pago con monto y un método abstracto conceptual
# procesar(). Hacé las hijas PagoEfectivo, PagoTarjeta y
# PagoTransferencia, cada una con su lógica propia de procesar().
# Recorré una lista mixta de pagos y procesalos todos con un solo bucle.
# -------------------------------------------------------------------------

class Pago:
    """Pago base cuyo procesamiento implementan sus hijas."""

    def __init__(self, monto):
        self._monto = monto

    def procesar(self):
        """Contrato que todo medio de pago debe cumplir."""
        raise NotImplementedError(
            f"La clase {type(self).__name__} debe implementar procesar()"
        )


class PagoEfectivo(Pago):
    """Pago realizado en efectivo."""

    def procesar(self):
        print(f"[EFECTIVO] ${self._monto} recibidos")


class PagoTarjeta(Pago):
    """Pago con tarjeta que agrega una comisión del 3%."""

    def procesar(self):
        comision = self._monto * 0.03
        print(
            f"[TARJETA] ${self._monto} "
            f"+ ${comision:.2f} de comisión"
        )


class PagoTransferencia(Pago):
    """Pago realizado mediante transferencia bancaria."""

    def procesar(self):
        print(
            f"[TRANSFERENCIA] ${self._monto} "
            f"acreditados a las 24hs"
        )


pagos = [
    PagoEfectivo(5000),
    PagoTarjeta(10000),
    PagoTransferencia(20000),
]

for pago in pagos:
    pago.procesar()
```

## `enunciado_15.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Vehiculo con marca y velocidad_maxima. Hacé
# Auto(Vehiculo) que agrega cantidad_puertas y después
# AutoDeportivo(Auto) que agrega caballos_de_fuerza. Cada nivel usa
# super() en el __init__ y sobrescribe __str__ reutilizando el del
# padre con super().__str__() para agregar solo su información extra.
# -------------------------------------------------------------------------

class Vehiculo:
    """Vehículo con marca y velocidad máxima."""

    def __init__(self, marca, velocidad_maxima):
        self._marca = marca
        self._velocidad_maxima = velocidad_maxima

    def __str__(self):
        return f"{self._marca} (Vmax: {self._velocidad_maxima}km/h)"


class Auto(Vehiculo):
    """Vehículo que agrega cantidad de puertas."""

    def __init__(self, marca, velocidad_maxima, cantidad_puertas):
        super().__init__(marca, velocidad_maxima)
        self._cantidad_puertas = cantidad_puertas

    def __str__(self):
        return f"{super().__str__()}, {self._cantidad_puertas} puertas"


class AutoDeportivo(Auto):
    """Auto que agrega caballos de fuerza."""

    def __init__(
        self,
        marca,
        velocidad_maxima,
        cantidad_puertas,
        caballos_de_fuerza,
    ):
        super().__init__(marca, velocidad_maxima, cantidad_puertas)
        self._caballos_de_fuerza = caballos_de_fuerza

    def __str__(self):
        return f"{super().__str__()}, {self._caballos_de_fuerza} HP"


vehiculos = [
    Vehiculo("Ford", 180),
    Auto("Toyota", 200, 4),
    AutoDeportivo("Ferrari", 320, 2, 720),
]

for vehiculo in vehiculos:
    print(vehiculo)
```

## `enunciado_16.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Producto con nombre y precio_final(), que devuelve el
# precio. Definí ProductoConDescuento(Producto) que sobrescribe
# precio_final() restando un porcentaje. Después hacé una clase Tienda
# con nombre, un método agregar(producto) y un método precio_total()
# que sume los precios finales. Tienda debe llamar a precio_final()
# polimórficamente, sin preguntar de qué tipo es cada producto.
# -------------------------------------------------------------------------

class Producto:
    """Producto cuyo precio final es igual a su precio de lista."""

    def __init__(self, nombre, precio):
        self._nombre = nombre
        self._precio = precio

    def precio_final(self):
        """Precio a cobrar por una unidad."""
        return self._precio

    def __str__(self):
        return f"  {self._nombre}: ${self.precio_final():.2f}"


class ProductoConDescuento(Producto):
    """Producto cuyo precio final aplica un descuento porcentual."""

    def __init__(self, nombre, precio, descuento):
        super().__init__(nombre, precio)
        self._descuento = descuento

    def precio_final(self):
        return self._precio * (1 - self._descuento / 100)


class Tienda:
    """Tienda que suma precios finales polimórficamente."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._productos = []

    def agregar(self, producto):
        """Suma un producto al catálogo de la tienda."""
        self._productos.append(producto)

    def precio_total(self):
        """Devuelve la suma de los precios finales del catálogo."""
        return sum(
            producto.precio_final()
            for producto in self._productos
        )

    def listar(self):
        """Imprime el catálogo y el total a cobrar."""
        print(f"{self._nombre}")
        for producto in self._productos:
            print(producto)
        print(f"  Total: ${self.precio_total():.2f}")


tienda = Tienda("Almacén")
tienda.agregar(Producto("Pan", 500))
tienda.agregar(ProductoConDescuento("Yerba", 3500, 20))
tienda.agregar(Producto("Leche", 800))

tienda.listar()
```

## `enunciado_17.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Enemigo con nombre, vida y un método atacar() que
# devuelve 10 de daño. Hacé Dragon(Enemigo), que ataca por 50, y
# Goblin(Enemigo), que ataca por 5. Simulá un turno recorriendo una
# lista mixta: cada enemigo ataca, se informa su estado y se acumula el
# daño total del grupo.
# -------------------------------------------------------------------------

class Enemigo:
    """Enemigo base con nombre, vida y ataque genérico."""

    def __init__(self, nombre, vida):
        self._nombre = nombre
        self._vida = vida

    def atacar(self):
        """Daño que provoca el enemigo en un turno."""
        return 10

    def __str__(self):
        return f"{self._nombre} (vida: {self._vida})"


class Dragon(Enemigo):
    """Enemigo que causa 50 puntos de daño."""

    def atacar(self):
        return 50


class Goblin(Enemigo):
    """Enemigo que causa 5 puntos de daño."""

    def atacar(self):
        return 5


enemigos = [
    Dragon("Smaug", 300),
    Goblin("Verdo", 30),
    Goblin("Rojo", 30),
    Enemigo("Sombra", 50),
]

danio_total = 0
for enemigo in enemigos:
    danio = enemigo.atacar()
    danio_total += danio
    print(f"{enemigo} ataca por {danio}")

print(f"Daño total del turno: {danio_total}")
```

## `enunciado_18.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Documento con titulo, contenido y método imprimir().
# Hacé Reporte(Documento) que sobrescriba imprimir() agregando
# encabezado y pie. Hacé ReporteAnual(Reporte) que sobrescriba de nuevo
# agregando un resumen ejecutivo antes del reporte. Cada nivel usa
# super() para incluir lo del padre en el medio de lo suyo.
# -------------------------------------------------------------------------

class Documento:
    """Documento base con título y contenido."""

    def __init__(self, titulo, contenido):
        self._titulo = titulo
        self._contenido = contenido

    def imprimir(self):
        """Muestra el título y el cuerpo del documento."""
        print(f"=== {self._titulo} ===")
        print(self._contenido)


class Reporte(Documento):
    """Documento con encabezado y pie propios de un reporte."""

    def imprimir(self):
        print("---- REPORTE ----")
        super().imprimir()
        print("--- Fin del reporte ---")


class ReporteAnual(Reporte):
    """Reporte que antepone un resumen ejecutivo."""

    def imprimir(self):
        print("### REPORTE ANUAL ###")
        print("### Resumen ejecutivo ###")
        super().imprimir()


documentos = [
    Documento("Nota", "Contenido cualquiera"),
    Reporte("Ventas Q3", "Facturación: $10M"),
    ReporteAnual("Ventas 2026", "Facturación: $50M"),
]

for documento in documentos:
    documento.imprimir()
    print()
```

## `enunciado_19.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Creá tres clases sin relación de herencia entre sí: Sensor, Reloj y
# Termostato. Cada una implementa leer(), que devuelve una cadena con su
# lectura actual. Escribí una función informar(dispositivos) que recorra
# cualquier lista y llame leer() sobre cada elemento. Esto es duck
# typing: no hay un padre común, alcanza con que el método exista.
#
# Ojo: hacer lo mismo con __str__ no sería duck typing puro, porque
# __str__ ya viene definido en object y toda clase lo hereda.
# -------------------------------------------------------------------------

class Sensor:
    """Dispositivo que informa una temperatura medida."""

    def __init__(self, ubicacion, temperatura):
        self._ubicacion = ubicacion
        self._temperatura = temperatura

    def leer(self):
        """Devuelve la lectura del sensor como texto."""
        return f"Sensor {self._ubicacion}: {self._temperatura} C"


class Reloj:
    """Dispositivo que informa una hora."""

    def __init__(self, hora, minuto):
        self._hora = hora
        self._minuto = minuto

    def leer(self):
        """Devuelve la hora como texto."""
        return f"Reloj: {self._hora:02d}:{self._minuto:02d}"


class Termostato:
    """Dispositivo que informa la temperatura configurada."""

    def __init__(self, objetivo):
        self._objetivo = objetivo

    def leer(self):
        """Devuelve la consigna del termostato como texto."""
        return f"Termostato: consigna {self._objetivo} C"


def informar(dispositivos):
    """Muestra la lectura de cualquier objeto que sepa leer()."""
    for dispositivo in dispositivos:
        print(dispositivo.leer())


tablero = [
    Sensor("cocina", 22),
    Reloj(9, 5),
    Termostato(24),
    Sensor("patio", 17),
]

informar(tablero)
```

## `enunciado_20.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Diseñá una jerarquía chica para un simulador de RPG. Personaje, el
# padre, con nombre, vida, atacar(), 10 de daño, y defender(), bloquea
# 5. Hacé Guerrero(Personaje), que ataca 25 y defiende igual;
# Mago(Personaje), que ataca 40 y defiende 2; y Sanador(Personaje), que
# ataca 5 y agrega curar(aliado), que le suma 20 de vida. Recorré una
# lista mixta y hacé que cada uno actúe en su turno. Prestá atención:
# atacar() y defender() están en todos, así que el bucle es uniforme;
# curar() existe solo en Sanador y queda fuera de la parte polimórfica.
# -------------------------------------------------------------------------

class Personaje:
    """Personaje base de un simulador de RPG."""

    def __init__(self, nombre, vida):
        self._nombre = nombre
        self._vida = vida

    def nombre(self):
        """Devuelve el nombre del personaje."""
        return self._nombre

    def atacar(self):
        """Daño que provoca el personaje en su turno."""
        return 10

    def defender(self):
        """Daño que el personaje logra bloquear."""
        return 5

    def recibir_curacion(self, puntos):
        """Suma puntos de vida al personaje."""
        self._vida += puntos

    def __str__(self):
        return f"{self._nombre} (vida: {self._vida})"


class Guerrero(Personaje):
    """Personaje con ataque alto y defensa heredada."""

    def atacar(self):
        return 25


class Mago(Personaje):
    """Personaje con ataque muy alto y defensa reducida."""

    def atacar(self):
        return 40

    def defender(self):
        return 2


class Sanador(Personaje):
    """Personaje con ataque bajo y capacidad de curar aliados."""

    def atacar(self):
        return 5

    def curar(self, aliado):
        """Cura a un aliado sumándole 20 puntos de vida."""
        aliado.recibir_curacion(20)
        print(f"{self._nombre} cura a {aliado.nombre()} (+20)")


grupo = [
    Guerrero("Aragorn", 100),
    Mago("Gandalf", 80),
    Sanador("Elrond", 90),
]

# Parte polimórfica: todos saben atacar y defender.
for personaje in grupo:
    print(
        f"{personaje} ataca por {personaje.atacar()} "
        f"y bloquea {personaje.defender()}"
    )

print()

# curar() no está en la interfaz común: no entra en el bucle de arriba.
guerrero = grupo[0]
sanador = grupo[2]
print(f"Antes:   {guerrero}")
sanador.curar(guerrero)
print(f"Después: {guerrero}")
```

# Ejercicios intercalados en el texto

## `ejercicio_01.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Definí una clase Animal con un método respirar() que imprima
# "Respirando...". Después definí Perro(Animal) sin agregar nada. Creá
# un perro y hacelo respirar. Comprobá con isinstance que es al mismo
# tiempo Perro y Animal.
# -------------------------------------------------------------------------

class Animal:
    """Animal base con la capacidad de respirar."""

    def respirar(self):
        """Imprime que el animal está respirando."""
        print("Respirando...")


class Perro(Animal):
    """Perro que hereda todo sin agregar comportamiento propio."""

    pass


pichicho = Perro()
pichicho.respirar()

print(isinstance(pichicho, Perro))
print(isinstance(pichicho, Animal))
print(isinstance(pichicho, object))
```

## `ejercicio_02.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Partí de la clase Animal con respirar(). Hacé que Perro agregue un
# método ladrar() que imprima "¡Guau!". Creá un perro, hacelo respirar
# y ladrar. Después creá un Animal genérico y comprobá que no puede
# ladrar: el método existe solo en la hija.
# -------------------------------------------------------------------------

class Animal:
    """Animal base con la capacidad de respirar."""

    def respirar(self):
        """Imprime que el animal está respirando."""
        print("Respirando...")


class Perro(Animal):
    """Animal que agrega el comportamiento de ladrar."""

    def ladrar(self):
        """Imprime el ladrido del perro."""
        print("¡Guau!")


firulais = Perro()
firulais.respirar()
firulais.ladrar()

generico = Animal()
generico.respirar()

try:
    generico.ladrar()
except AttributeError as error:
    print(f"Error esperado: {error}")
```

## `ejercicio_03.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Partí de una clase Empleado con __init__(nombre), que guarda el
# nombre, y un método presentarse() que imprime "Soy Ana". Hacé una
# hija Gerente que agrega el atributo equipo, la lista de personas a
# cargo. Su __init__ debe usar super() para no repetir código. Además,
# Gerente.presentarse() debe llamar a la del padre y agregar "y dirijo
# un equipo de N personas".
# -------------------------------------------------------------------------

class Empleado:
    """Empleado con nombre y presentación básica."""

    def __init__(self, nombre):
        self._nombre = nombre

    def presentarse(self):
        """Imprime la presentación común a todo empleado."""
        print(f"Soy {self._nombre}")


class Gerente(Empleado):
    """Empleado que además dirige un equipo."""

    def __init__(self, nombre, equipo):
        super().__init__(nombre)
        self._equipo = equipo

    def presentarse(self):
        """Extiende la presentación del padre con el equipo."""
        super().presentarse()
        print(f"y dirijo un equipo de {len(self._equipo)} personas")


empleado = Empleado("Juan")
gerente = Gerente("Ana", ["Juan", "Pedro", "Lucía"])

empleado.presentarse()
print()
gerente.presentarse()
```

## `ejercicio_04.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Rectangulo con __init__(base, altura) y un método
# area() que devuelve base * altura. Después hacé Cuadrado(Rectangulo)
# con un solo parámetro lado en el constructor: usá super() para pasar
# el mismo valor como base y altura. Sobrescribí descripcion():
# Rectangulo imprime "Rectángulo de base X y altura Y" y Cuadrado,
# "Cuadrado de lado X". Fijate que area() no hace falta reescribirla.
# -------------------------------------------------------------------------

class Rectangulo:
    """Rectángulo definido por base y altura."""

    def __init__(self, base, altura):
        self._base = base
        self._altura = altura

    def area(self):
        """Devuelve base por altura."""
        return self._base * self._altura

    def descripcion(self):
        """Imprime las dos dimensiones del rectángulo."""
        print(
            f"Rectángulo de base {self._base} "
            f"y altura {self._altura}"
        )


class Cuadrado(Rectangulo):
    """Rectángulo especializado cuyos dos lados son iguales."""

    def __init__(self, lado):
        super().__init__(lado, lado)

    def descripcion(self):
        """Imprime el único lado que define al cuadrado."""
        print(f"Cuadrado de lado {self._base}")


rectangulo = Rectangulo(5, 3)
rectangulo.descripcion()
print(rectangulo.area())

cuadrado = Cuadrado(4)
cuadrado.descripcion()
print(cuadrado.area())
```

## `ejercicio_05.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Libro con titulo y autor, y un __str__ que devuelva
# "Titulo, de Autor". Después hacé LibroDigital(Libro) que agregue el
# formato y sobrescriba __str__ reutilizando el del padre con
# super().__str__(), en vez de repetir el formato completo.
# -------------------------------------------------------------------------

class Libro:
    """Libro impreso con título y autor."""

    def __init__(self, titulo, autor):
        self._titulo = titulo
        self._autor = autor

    def __str__(self):
        return f"{self._titulo}, de {self._autor}"


class LibroDigital(Libro):
    """Libro que además tiene un formato de archivo."""

    def __init__(self, titulo, autor, formato):
        super().__init__(titulo, autor)
        self._formato = formato

    def __str__(self):
        return f"{super().__str__()} [{self._formato}]"


papel = Libro("Rayuela", "Cortázar")
digital = LibroDigital("El Aleph", "Borges", "PDF")

print(papel)
print(digital)
```

## `ejercicio_06.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Instrumento con atributo nombre y método tocar() que
# devuelve "...". Hacé Guitarra(Instrumento), Piano(Instrumento) y
# Bateria(Instrumento) que sobrescriban tocar() con mensajes distintos.
# Después creá una lista mixta y hacé que cada uno toque.
# -------------------------------------------------------------------------

class Instrumento:
    """Instrumento con nombre y sonido genérico."""

    def __init__(self, nombre):
        self._nombre = nombre

    def tocar(self):
        """Sonido por defecto de un instrumento sin especializar."""
        return "..."

    def __str__(self):
        return f"{self._nombre}: {self.tocar()}"


class Guitarra(Instrumento):
    """Guitarra con su propia forma de sonar."""

    def tocar(self):
        return "Rasguido de guitarra"


class Piano(Instrumento):
    """Piano con su propia forma de sonar."""

    def tocar(self):
        return "Acorde de piano"


class Bateria(Instrumento):
    """Batería con su propia forma de sonar."""

    def tocar(self):
        return "Redoble de batería"


banda = [
    Guitarra("Fender"),
    Piano("Yamaha"),
    Bateria("Ludwig"),
]

for instrumento in banda:
    print(instrumento)
```

## `ejercicio_07.py`
```python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Creá las clases Pato, Robot y Alarma, sin relación de herencia entre
# sí. Cada una debe tener un método hablar() que devuelva un mensaje
# propio. Hacé una función hacer_hablar(cosa) que imprima cosa.hablar()
# y probala con objetos de las tres clases: eso es duck typing.
# -------------------------------------------------------------------------

class Pato:
    """Objeto que sabe hablar sin heredar de una clase común."""

    def hablar(self):
        """Devuelve el sonido del pato."""
        return "Cuac"


class Robot:
    """Objeto que sabe hablar sin heredar de una clase común."""

    def hablar(self):
        """Devuelve el mensaje binario del robot."""
        return "01001000..."


class Alarma:
    """Objeto que sabe hablar sin heredar de una clase común."""

    def hablar(self):
        """Devuelve el aviso de la alarma."""
        return "BEEP BEEP BEEP"


def hacer_hablar(cosa):
    """Invoca hablar() sin comprobar el tipo del objeto."""
    print(cosa.hablar())


hacer_hablar(Pato())
hacer_hablar(Robot())
hacer_hablar(Alarma())
```
