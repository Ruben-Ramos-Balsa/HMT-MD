#!/usr/bin/env python3
"""Verificación racional del defecto de proyectores cíclicos.

La prueba construye, sin datos procedentes de las otras realizaciones de
-1/12, los proyectores sobre los invariantes de S^3 y S^4 en Q^12.
Todas las puertas permanecen activas bajo ``python -O``.
"""

from __future__ import annotations

import json
from fractions import Fraction
from math import gcd
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "certificados" / "proyectores_ciclicos_menos_un_doce.json"
PASS_TOKEN = "PASS_PROYECTORES_CICLICOS_MENOS_UN_DOCE"


class VerificationError(RuntimeError):
    """Fallo exacto o documental."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


Matrix = list[list[Fraction]]


def identity(n: int) -> Matrix:
    return [
        [Fraction(int(i == j)) for j in range(n)]
        for i in range(n)
    ]


def matmul(left: Sequence[Sequence[Fraction]],
           right: Sequence[Sequence[Fraction]]) -> Matrix:
    require(bool(left) and bool(right), "matriz vacía")
    require(len(left[0]) == len(right), "dimensiones incompatibles")
    return [
        [
            sum(
                (left[i][k] * right[k][j] for k in range(len(right))),
                Fraction(0),
            )
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def transpose(matrix: Sequence[Sequence[Fraction]]) -> Matrix:
    return [list(column) for column in zip(*matrix)]


def matrix_equal(left: Sequence[Sequence[Fraction]],
                 right: Sequence[Sequence[Fraction]]) -> bool:
    return list(map(list, left)) == list(map(list, right))


def cyclic_shift(n: int, step: int) -> Matrix:
    matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for column in range(n):
        matrix[(column + step) % n][column] = Fraction(1)
    return matrix


def add(left: Sequence[Sequence[Fraction]],
        right: Sequence[Sequence[Fraction]]) -> Matrix:
    return [
        [a + b for a, b in zip(row_left, row_right)]
        for row_left, row_right in zip(left, right)
    ]


def scale(value: Fraction, matrix: Sequence[Sequence[Fraction]]) -> Matrix:
    return [[value * entry for entry in row] for row in matrix]


def matrix_power(matrix: Matrix, exponent: int) -> Matrix:
    require(exponent >= 0, "exponente negativo")
    result = identity(len(matrix))
    base = matrix
    power = exponent
    while power:
        if power & 1:
            result = matmul(result, base)
        base = matmul(base, base)
        power //= 2
    return result


def invariant_projector(n: int, step: int) -> Matrix:
    orbit_order = n // gcd(n, step)
    shift = cyclic_shift(n, step)
    total = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for exponent in range(orbit_order):
        total = add(total, matrix_power(shift, exponent))
    return scale(Fraction(1, orbit_order), total)


def trace(matrix: Sequence[Sequence[Fraction]]) -> Fraction:
    return sum(
        (matrix[i][i] for i in range(len(matrix))),
        Fraction(0),
    )


def rank(matrix: Sequence[Sequence[Fraction]]) -> int:
    work = [list(row) for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (
                row for row in range(pivot_row, rows)
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    entry - factor * pivot_entry
                    for entry, pivot_entry
                    in zip(work[row], work[pivot_row])
                ]
        pivot_row += 1
    return pivot_row


def fraction_pair(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def main() -> None:
    require(CERTIFICATE.is_file(), f"falta el certificado: {CERTIFICATE}")
    documented = json.loads(CERTIFICATE.read_text(encoding="utf-8"))

    n = 12
    p3 = invariant_projector(n, 3)
    p4 = invariant_projector(n, 4)

    require(matrix_equal(matmul(p3, p3), p3), "P3 no es idempotente")
    require(matrix_equal(matmul(p4, p4), p4), "P4 no es idempotente")
    require(matrix_equal(transpose(p3), p3), "P3 no es ortogonal")
    require(matrix_equal(transpose(p4), p4), "P4 no es ortogonal")

    rank3 = rank(p3)
    rank4 = rank(p4)
    trace3 = trace(p3)
    trace4 = trace(p4)
    defect = (trace3 - trace4) / n

    require(rank3 == gcd(n, 3) == 3, "rango incorrecto para P3")
    require(rank4 == gcd(n, 4) == 4, "rango incorrecto para P4")
    require(trace3 == rank3, "traza y rango difieren para P3")
    require(trace4 == rank4, "traza y rango difieren para P4")
    require(defect == Fraction(-1, 12), "el defecto no vale -1/12")

    computed = {
        "ambient_dimension": n,
        "projector_step_3": {
            "orbit_order": n // gcd(n, 3),
            "rank": rank3,
            "trace": fraction_pair(trace3),
        },
        "projector_step_4": {
            "orbit_order": n // gcd(n, 4),
            "rank": rank4,
            "trace": fraction_pair(trace4),
        },
        "normalized_trace_defect": fraction_pair(defect),
    }
    require(
        documented["exact_results"] == computed,
        "el certificado no coincide con la reconstrucción exacta",
    )
    require(
        documented["independence"]["uses_other_minus_one_twelfth_routes"]
        is False,
        "el certificado no declara independencia de las otras rutas",
    )
    print(PASS_TOKEN)


if __name__ == "__main__":
    main()
