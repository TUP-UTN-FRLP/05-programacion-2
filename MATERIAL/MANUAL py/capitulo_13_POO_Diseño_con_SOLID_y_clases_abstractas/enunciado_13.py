# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# DIP y testeo: hacé una clase LogicaNegocio que necesita algo capaz de
# persistir datos. Definí Repositorio como ABC y dos implementaciones:
# RepositorioMemoria, que guarda en un dict, y RepositorioFalso, un
# doble de prueba que no guarda nada y solo cuenta las llamadas.
# Comprobá con assert que la lógica llama al repositorio como promete.
# -------------------------------------------------------------------------

from abc import ABC, abstractmethod
from typing import Any, Optional


class Repositorio(ABC):
    """Abstracción para guardar y recuperar valores por clave."""

    @abstractmethod
    def guardar(self, clave: str, valor: Any) -> None:
        """Persiste el valor bajo esa clave."""

    @abstractmethod
    def obtener(self, clave: str) -> Optional[Any]:
        """Devuelve el valor guardado o None si no está."""


class RepositorioMemoria(Repositorio):
    """Repositorio real, en memoria."""

    def __init__(self) -> None:
        self._datos: dict[str, Any] = {}

    def guardar(self, clave: str, valor: Any) -> None:
        self._datos[clave] = valor

    def obtener(self, clave: str) -> Optional[Any]:
        return self._datos.get(clave)


class RepositorioFalso(Repositorio):
    """Doble de prueba: no guarda nada, cuenta las llamadas."""

    def __init__(self) -> None:
        self.llamadas_guardar = 0
        self.llamadas_obtener = 0

    def guardar(self, clave: str, valor: Any) -> None:
        self.llamadas_guardar += 1

    def obtener(self, clave: str) -> Optional[Any]:
        self.llamadas_obtener += 1
        return None


class LogicaNegocio:
    """Lógica que depende de la abstracción, no de la implementación."""

    def __init__(self, repositorio: Repositorio) -> None:
        self._repositorio = repositorio

    def procesar(self, clave: str, valor: Any) -> Optional[Any]:
        """Guarda el valor y lo vuelve a leer."""
        self._repositorio.guardar(clave, valor)
        return self._repositorio.obtener(clave)


if __name__ == "__main__":
    real = LogicaNegocio(RepositorioMemoria())
    print(real.procesar("A", 100))

    # El doble permite verificar el comportamiento sin tocar disco ni
    # base de datos. Eso es lo que DIP habilita.
    falso = RepositorioFalso()
    LogicaNegocio(falso).procesar("A", 100)

    assert falso.llamadas_guardar == 1, "debería guardar una vez"
    assert falso.llamadas_obtener == 1, "debería leer una vez"

    print("La lógica usa el repositorio como promete")
