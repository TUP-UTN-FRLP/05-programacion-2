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
