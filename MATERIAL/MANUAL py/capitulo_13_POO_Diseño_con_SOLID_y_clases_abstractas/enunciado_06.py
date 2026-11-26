# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Dataclass: reescribí Producto como @dataclass con codigo, nombre,
# precio y stock. Dos productos son iguales si tienen el mismo codigo,
# sin importar el resto. Cuidado con una trampa: si definís __eq__ a
# mano, Python pone __hash__ en None y la clase deja de poder usarse
# como clave de diccionario o dentro de un set. Resolvelo sin escribir
# __eq__ a mano.
# -------------------------------------------------------------------------

from dataclasses import dataclass, field


@dataclass(unsafe_hash=True)
class Producto:
    """Producto cuya identidad depende únicamente del código."""

    codigo: str
    nombre: str = field(compare=False)
    precio: float = field(compare=False)
    stock: int = field(compare=False)

    def __post_init__(self):
        """Valida los datos apenas se construye el producto."""
        if self.precio <= 0:
            raise ValueError("El precio debe ser positivo")


if __name__ == "__main__":
    # compare=False deja fuera de __eq__ a todo menos el código, y
    # unsafe_hash=True pide el __hash__ que un __eq__ propio habría
    # roto. Se llama "unsafe" porque hashear objetos mutables es
    # riesgoso; acá es seguro porque el codigo nunca cambia.
    uno = Producto("P-001", "Yerba", 3500, 20)
    otro = Producto("P-001", "Yerba en oferta", 3000, 5)
    tercero = Producto("P-002", "Leche", 800, 15)

    print(uno)
    print(f"uno == otro:     {uno == otro}")
    print(f"uno == tercero:  {uno == tercero}")

    # Como no rompimos __hash__, el producto sirve de clave.
    stock_por_producto = {uno: 20, tercero: 15}
    print(stock_por_producto[otro])

    try:
        Producto("P-003", "Fallido", 0, 1)
    except ValueError as error:
        print(f"Error: {error}")
