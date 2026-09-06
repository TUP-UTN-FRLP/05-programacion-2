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
