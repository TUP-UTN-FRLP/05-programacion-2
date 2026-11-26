# Índice de ejercicios

Cada carpeta corresponde a un concepto y contiene tres pares de archivos:

- `principal_1.py` / `validaciones_1.py`
- `principal_2.py` / `validaciones_2.py`
- `principal_3.py` / `validaciones_3.py`

La guía teórica general está en `GUIA_VALIDACIONES.md`.

## Cómo ejecutar

Cada `principal_N.py` importa desde el `validaciones_N.py` de su misma carpeta,
por lo que hay que ejecutarlo parado en esa carpeta:

```text
cd 01_re_patrones_basicos
python principal_1.py
```

Ejecutarlo desde otra carpeta da `ModuleNotFoundError`.

Los bloques están pensados para recorrerse en orden: cada uno usa solo lo visto
en los anteriores.

## Carpetas

1. `01_re_patrones_basicos`
2. `02_compile_y_patron_nombre`
3. `03_isinstance`
4. `04_raise_sin_except`
5. `05_re_sub_normalizacion`
6. `06_match`
7. `07_repr_en_fstrings`
8. `08_fullmatch_y_raw_strings`
9. `09_es_numero_y_bool`
10. `10_funcion_que_usa_funcion`

Total: **30 ejercicios**, organizados como **30 pares**
`principal_N.py` + `validaciones_N.py`.
