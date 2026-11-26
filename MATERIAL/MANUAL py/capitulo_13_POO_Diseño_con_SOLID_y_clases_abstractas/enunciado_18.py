# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Mini sistema aplicando los cinco principios. Notificador es una ABC
# con enviar(mensaje, destinatario) y tres implementaciones. Alerta es
# una dataclass frozen con titulo, mensaje y nivel. SistemaAlertas
# recibe el notificador por constructor y lo usa para avisarle a una
# lista de destinatarios. Identificá qué principio aplica cada pieza.
# -------------------------------------------------------------------------

from abc import ABC, abstractmethod
from dataclasses import dataclass


class Notificador(ABC):
    """Abstracción para entregar un mensaje a un destinatario."""

    @abstractmethod
    def enviar(self, mensaje: str, destinatario: str) -> None:
        """Entrega el mensaje por el canal correspondiente."""


class NotificadorEmail(Notificador):
    """Canal de correo electrónico."""

    def enviar(self, mensaje: str, destinatario: str) -> None:
        print(f"[EMAIL a {destinatario}] {mensaje}")


class NotificadorSMS(Notificador):
    """Canal de mensajes de texto."""

    def enviar(self, mensaje: str, destinatario: str) -> None:
        print(f"[SMS a {destinatario}] {mensaje}")


class NotificadorPush(Notificador):
    """Canal de avisos push."""

    def enviar(self, mensaje: str, destinatario: str) -> None:
        print(f"[PUSH a {destinatario}] {mensaje}")


@dataclass(frozen=True)
class Alerta:
    """Alerta inmutable: una vez emitida no se edita."""

    titulo: str
    mensaje: str
    nivel: str

    def texto(self) -> str:
        """Devuelve la alerta formateada en una línea."""
        return f"[{self.nivel}] {self.titulo}: {self.mensaje}"


class SistemaAlertas:
    """Coordina el envío mediante el Notificador inyectado."""

    def __init__(self, notificador: Notificador) -> None:
        self._notificador = notificador

    def emitir(
        self,
        alerta: Alerta,
        destinatarios: list[str],
    ) -> None:
        """Envía la alerta a todos los destinatarios."""
        for destinatario in destinatarios:
            self._notificador.enviar(alerta.texto(), destinatario)


if __name__ == "__main__":
    # SRP: cada clase hace una sola cosa.
    # OCP: agregar un canal nuevo no toca SistemaAlertas.
    # LSP: los tres notificadores son intercambiables.
    # ISP: Notificador declara un único método, el que todos cumplen.
    # DIP: SistemaAlertas depende de la ABC, no de los canales.
    alerta = Alerta(
        titulo="Servidor caído",
        mensaje="No responde el ping",
        nivel="CRÍTICO",
    )

    canales = [
        NotificadorEmail(),
        NotificadorSMS(),
        NotificadorPush(),
    ]

    for canal in canales:
        SistemaAlertas(canal).emitir(alerta, ["guardia", "soporte"])
