# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Documento con titulo, contenido y método imprimir().
# Hacé Reporte(Documento) que sobrescriba imprimir() agregando
# encabezado y pie. Hacé ReporteAnual(Reporte) que sobrescriba de nuevo
# agregando un resumen ejecutivo antes del reporte. Cada nivel usa
# super() para incluir lo del padre en el medio de lo suyo.
# -------------------------------------------------------------------------

class Documento:
    """Documento base con título y contenido."""

    def __init__(self, titulo, contenido):
        self._titulo = titulo
        self._contenido = contenido

    def imprimir(self):
        """Muestra el título y el cuerpo del documento."""
        print(f"=== {self._titulo} ===")
        print(self._contenido)


class Reporte(Documento):
    """Documento con encabezado y pie propios de un reporte."""

    def imprimir(self):
        print("---- REPORTE ----")
        super().imprimir()
        print("--- Fin del reporte ---")


class ReporteAnual(Reporte):
    """Reporte que antepone un resumen ejecutivo."""

    def imprimir(self):
        print("### REPORTE ANUAL ###")
        print("### Resumen ejecutivo ###")
        super().imprimir()


documentos = [
    Documento("Nota", "Contenido cualquiera"),
    Reporte("Ventas Q3", "Facturación: $10M"),
    ReporteAnual("Ventas 2026", "Facturación: $50M"),
]

for documento in documentos:
    documento.imprimir()
    print()
