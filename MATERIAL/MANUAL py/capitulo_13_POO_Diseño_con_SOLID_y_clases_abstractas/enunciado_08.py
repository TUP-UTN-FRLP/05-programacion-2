# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# DIP: separá SistemaAlerta en una abstracción y sus implementaciones.
# Definí Notificador como ABC, con NotificadorEmail y NotificadorSMS
# como concretos. SistemaAlerta debe recibir el notificador por
# constructor (inyección de dependencias) y no importar ni conocer
# ninguna de las dos clases concretas.
# -------------------------------------------------------------------------

from abc import ABC, abstractmethod


class Notificador(ABC):
    """Abstracción: cualquier cosa que sepa enviar un mensaje."""

    @abstractmethod
    def enviar(self, mensaje: str) -> None:
        """Entrega el mensaje por el canal que corresponda."""


class NotificadorEmail(Notificador):
    """Notificador concreto por correo electrónico."""

    def __init__(self, destinatario: str) -> None:
        self._destinatario = destinatario

    def enviar(self, mensaje: str) -> None:
        print(f"[EMAIL a {self._destinatario}] {mensaje}")


class NotificadorSMS(Notificador):
    """Notificador concreto por mensaje de texto."""

    def __init__(self, telefono: str) -> None:
        self._telefono = telefono

    def enviar(self, mensaje: str) -> None:
        print(f"[SMS a {self._telefono}] {mensaje}")


class SistemaAlerta:
    """Sistema que depende de la abstracción, no del canal."""

    def __init__(self, notificador: Notificador) -> None:
        self._notificador = notificador

    def alertar(self, mensaje: str) -> None:
        """Emite una alerta por el canal inyectado."""
        self._notificador.enviar(f"ALERTA: {mensaje}")


if __name__ == "__main__":
    # Quien construye el sistema elige el canal. SistemaAlerta no se
    # entera de cuál le tocó.
    for sistema in [
        SistemaAlerta(NotificadorEmail("admin@sistema.com")),
        SistemaAlerta(NotificadorSMS("+54 221 555-0000")),
    ]:
        sistema.alertar("Servidor sin respuesta")
