# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# SRP: la clase Pedido guarda sus líneas, calcula el total, imprime el
# remito por pantalla, lo exporta a texto y lo manda por email. Contá
# cuántas razones para cambiar tiene y separala en clases con una sola
# responsabilidad cada una.
# -------------------------------------------------------------------------

class Pedido:
    """Representa un pedido y calcula su total. Nada más."""

    def __init__(self, numero, cliente):
        self._numero = numero
        self._cliente = cliente
        self._lineas = []

    def numero(self):
        """Devuelve el número de pedido."""
        return self._numero

    def cliente(self):
        """Devuelve el nombre del cliente."""
        return self._cliente

    def agregar(self, descripcion, precio, cantidad):
        """Suma una línea al pedido."""
        self._lineas.append((descripcion, precio, cantidad))

    def lineas(self):
        """Devuelve una copia de las líneas del pedido."""
        return list(self._lineas)

    def total(self):
        """Suma precio por cantidad de todas las líneas."""
        return sum(
            precio * cantidad
            for _, precio, cantidad in self._lineas
        )


class RemitoEnPantalla:
    """Única responsabilidad: mostrar un pedido por pantalla."""

    def imprimir(self, pedido):
        """Imprime el remito del pedido recibido."""
        print(f"Remito {pedido.numero()} - {pedido.cliente()}")

        for descripcion, precio, cantidad in pedido.lineas():
            print(f"  {descripcion} x{cantidad}: ${precio * cantidad}")

        print(f"  TOTAL: ${pedido.total()}")


class ExportadorTexto:
    """Única responsabilidad: representar un pedido como texto."""

    def exportar(self, pedido):
        """Devuelve el pedido como texto plano separado por comas."""
        lineas = [f"pedido,{pedido.numero()},{pedido.cliente()}"]

        for descripcion, precio, cantidad in pedido.lineas():
            lineas.append(f"{descripcion},{precio},{cantidad}")

        return "\n".join(lineas)


class NotificadorEmail:
    """Única responsabilidad: enviar mensajes por email."""

    def enviar_remito(self, pedido, email):
        """Simula el envío del remito por correo."""
        print(f"[EMAIL a {email}] Remito {pedido.numero()} enviado")


if __name__ == "__main__":
    # Cuatro razones para cambiar en la clase original: el modelo de
    # pedido, el formato de pantalla, el formato de texto y el envío.
    pedido = Pedido("P-001", "Ana Perez")
    pedido.agregar("Yerba", 3500, 2)
    pedido.agregar("Leche", 800, 3)

    RemitoEnPantalla().imprimir(pedido)
    print()
    print(ExportadorTexto().exportar(pedido))
    NotificadorEmail().enviar_remito(pedido, "ana@correo.com")
