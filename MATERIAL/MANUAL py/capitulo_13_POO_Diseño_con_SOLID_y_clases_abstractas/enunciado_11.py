# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Dataclass, dos trampas: reescribí Coordenada como
# @dataclass(frozen=True) y explicá por qué frozen tiene sentido acá.
# Después hacé Ruta, una dataclass con nombre y una lista de paradas.
# Fijate qué pasa si ponés la lista como valor por defecto directo y
# resolvelo con field(default_factory=list).
# -------------------------------------------------------------------------

from dataclasses import FrozenInstanceError, dataclass, field


@dataclass(frozen=True)
class Coordenada:
    """Coordenada geográfica inmutable."""

    latitud: float
    longitud: float


@dataclass
class Ruta:
    """Ruta con nombre y una lista propia de paradas."""

    nombre: str
    paradas: list[Coordenada] = field(default_factory=list)

    def agregar(self, coordenada: Coordenada) -> None:
        """Suma una parada al final de la ruta."""
        self.paradas.append(coordenada)


if __name__ == "__main__":
    # frozen=True: una coordenada representa un valor, no una entidad
    # que evoluciona. Para otro punto se crea otra instancia.
    plaza = Coordenada(-34.921, -57.954)
    print(plaza)

    try:
        plaza.latitud = 0
    except FrozenInstanceError as error:
        print(f"No puede modificarse: {error}")

    # paradas: list = [] sería un error: ese mismo objeto lista se
    # compartiría entre TODAS las rutas. default_factory=list crea una
    # lista nueva por instancia. De hecho, dataclass directamente
    # rechaza el default mutable con ValueError.
    una = Ruta("Centro")
    otra = Ruta("Costa")

    una.agregar(plaza)

    print(f"{una.nombre}: {len(una.paradas)} paradas")
    print(f"{otra.nombre}: {len(otra.paradas)} paradas")
