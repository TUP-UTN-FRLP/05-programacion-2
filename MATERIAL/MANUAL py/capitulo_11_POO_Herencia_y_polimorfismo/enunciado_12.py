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
