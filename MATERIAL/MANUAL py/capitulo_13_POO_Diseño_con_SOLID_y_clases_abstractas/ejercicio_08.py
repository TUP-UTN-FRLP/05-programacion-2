# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Dataclass y assert: escribí Punto como @dataclass con x e y, y
# Poligono como dataclass con nombre y una lista de vértices, usando
# field(default_factory=list). Verificá con assert que dos puntos con
# los mismos valores son iguales y que dos polígonos recién creados no
# comparten la misma lista.
# -------------------------------------------------------------------------

from dataclasses import dataclass, field


@dataclass
class Punto:
    """Punto del plano, comparable por valor."""

    x: float
    y: float


@dataclass
class Poligono:
    """Polígono con nombre y su propia lista de vértices."""

    nombre: str
    vertices: list[Punto] = field(default_factory=list)

    def agregar(self, punto: Punto) -> None:
        """Suma un vértice al polígono."""
        self.vertices.append(punto)


if __name__ == "__main__":
    uno = Punto(3, 5)
    otro = Punto(3, 5)

    print(uno)
    assert uno == otro, "dataclass debería comparar por valor"
    assert uno is not otro, "son dos objetos distintos"

    # Si vertices fuera "list = []", las dos instancias compartirían
    # la misma lista. default_factory crea una nueva por objeto.
    triangulo = Poligono("triángulo")
    cuadrado = Poligono("cuadrado")

    triangulo.agregar(uno)

    assert triangulo.vertices is not cuadrado.vertices, (
        "cada polígono debe tener su propia lista"
    )
    assert len(cuadrado.vertices) == 0, (
        "el cuadrado no debería haber recibido el vértice"
    )

    print(f"{triangulo.nombre}: {len(triangulo.vertices)} vértices")
    print(f"{cuadrado.nombre}: {len(cuadrado.vertices)} vértices")
