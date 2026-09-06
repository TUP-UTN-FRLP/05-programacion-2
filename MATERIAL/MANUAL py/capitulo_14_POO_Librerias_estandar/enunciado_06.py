# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Escribí tamanio_carpeta(carpeta) que devuelva el tamaño total en bytes
# de los archivos directos de una carpeta, usando stat().st_size. Sumale
# tamanio_recursivo(carpeta), que use rglob("*") para incluir también las
# subcarpetas, y compará los dos resultados sobre una carpeta de prueba
# que el propio programa cree.
# -------------------------------------------------------------------------

from pathlib import Path


def tamanio_carpeta(carpeta):
    """Suma el tamaño de los archivos directos de una carpeta."""
    return sum(
        item.stat().st_size
        for item in carpeta.iterdir()
        if item.is_file()
    )


def tamanio_recursivo(carpeta):
    """Suma el tamaño de todos los archivos, incluidas subcarpetas."""
    return sum(
        item.stat().st_size
        for item in carpeta.rglob("*")
        if item.is_file()
    )


def preparar_carpeta_de_prueba(raiz):
    """Crea una carpeta con archivos de ejemplo y la devuelve."""
    (raiz / "subcarpeta").mkdir(parents=True, exist_ok=True)

    (raiz / "notas.txt").write_text(
        "hola " * 100, encoding="utf-8"
    )
    (raiz / "datos.csv").write_text(
        "a,b\n1,2\n", encoding="utf-8"
    )
    (raiz / "subcarpeta" / "anexo.txt").write_text(
        "x" * 500, encoding="utf-8"
    )

    return raiz


if __name__ == "__main__":
    # write_text y read_text NO usan UTF-8 por defecto: toman la
    # codificación del sistema. Siempre hay que pasarla explícita.
    carpeta = preparar_carpeta_de_prueba(Path("prueba_tamanio"))

    directo = tamanio_carpeta(carpeta)
    total = tamanio_recursivo(carpeta)

    print(f"Solo archivos directos: {directo} bytes")
    print(f"Incluyendo subcarpetas: {total} bytes")
    print(f"Diferencia:             {total - directo} bytes")
