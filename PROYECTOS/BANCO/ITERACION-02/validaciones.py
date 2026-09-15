"""Funciones de validacion reutilizables para la Iteracion 2.

Contrato general:
- devuelven el valor normalizado cuando corresponde;
- lanzan TypeError si el tipo recibido no corresponde;
- lanzan ValueError si el tipo es correcto pero el valor no cumple la regla;
- no usan input() ni print();
- no dependen de instancias de Persona ni Cuenta.

Esta es la implementacion de referencia de la catedra. Cada estudiante debe
escribir la suya; los tests de test.py fijan el contrato, no esta version.
"""

import re

# Una o mas "palabras" de letras (con tildes / ñ) separadas por un unico
# espacio, guion o apostrofo. Sin digitos, sin guion bajo, sin simbolos.
_PATRON_NOMBRE = re.compile(r"^[^\W\d_]+(?:[ '\-][^\W\d_]+)*$", re.UNICODE)


def validar_nombre(valor):
    """
    Normaliza un nombre o apellido: quita espacios sobrantes
    y aplica title().
    """
    if not isinstance(valor, str):
        raise TypeError("El nombre debe ser str")
    limpio = re.sub(r"\s+", " ", valor).strip()
    if not limpio:
        raise ValueError("El nombre no puede quedar vacio")
    if not _PATRON_NOMBRE.match(limpio):
        raise ValueError(f"Nombre con caracteres no permitidos: {valor!r}")
    return limpio.title()


def validar_dni(valor):
    """El DNI se recibe como str de 7 u 8 digitos y se devuelve tal cual."""
    if not isinstance(valor, str):
        raise TypeError("El DNI debe ser str")
    if not re.fullmatch(r"[0-9]{7,8}", valor):
        raise ValueError(f"DNI invalido: {valor!r} (se esperan 7 u 8 digitos)")
    return valor


def validar_numero_cuenta(valor):
    """Numero de cuenta: str de exactamente 14 digitos."""
    if not isinstance(valor, str):
        raise TypeError("El numero de cuenta debe ser str")
    if not re.fullmatch(r"[0-9]{14}", valor):
        raise ValueError(f"Numero de cuenta invalido: {valor!r} (14 digitos)")
    return valor


def _es_numero(valor):
    # bool es subclase de int: lo excluimos explicitamente.
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def validar_saldo_inicial(valor):
    """Saldo inicial: numerico y no negativo."""
    if not _es_numero(valor):
        raise TypeError("El saldo inicial debe ser int o float")
    if valor < 0:
        raise ValueError("El saldo inicial no puede ser negativo")
    return valor


def validar_monto(valor):
    """Monto de una operacion: numerico y estrictamente mayor que cero."""
    if not _es_numero(valor):
        raise TypeError("El monto debe ser int o float")
    if valor <= 0:
        raise ValueError("El monto debe ser mayor que cero")
    return valor
