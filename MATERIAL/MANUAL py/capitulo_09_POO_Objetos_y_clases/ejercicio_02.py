# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Ejercicio 2
# Definí una clase Producto con atributos nombre y precio, inicializados
# desde el constructor. Creá dos productos e imprimí sus atributos.
# -------------------------------------------------------------------------


class Producto:

    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio


pan = Producto("Pan", 500)
leche = Producto("Leche", 800)

print(f"{pan.nombre}: ${pan.precio}")
print(f"{leche.nombre}: ${leche.precio}")
