# Funciones y métodos utilizados en capitulo_04_Bucles

Documento de referencia que agrupa las funciones built-in y los métodos
utilizados en los ejercicios y enunciados del capítulo, organizados por tipo
de dato y en orden alfabético.

---

## Funciones generales

### `enumerate(iterable, start=0)`

**¿Qué realiza?**  
Permite recorrer un iterable obteniendo simultáneamente el índice y el
elemento correspondiente.

**¿Qué retorna?**  
Un objeto `enumerate` que produce pares de la forma `(índice, elemento)`.

**Ejemplos típicos:**

```python
nombres = ["Ana", "Juan", "Pedro"]

for i, nombre in enumerate(nombres):
    print(f"{i}: {nombre}")
# 0: Ana
# 1: Juan
# 2: Pedro
