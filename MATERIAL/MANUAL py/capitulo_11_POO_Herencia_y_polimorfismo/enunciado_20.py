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
