#!/usr/bin/env python3
"""Verifica los cierres algebraicos de Dirac real y caminos finitos.

La aritmética es entera y no usa bibliotecas externas. El script comprueba:

1. la representación real 4x4 de Cl(3,1);
2. la realificación de M_2(C) sobre una base real completa;
3. una expansión exacta de caminos y la conservación de norma para una
   evolución unitaria finita;
4. controles negativos para Clifford, suma de caminos y unitariedad.

Las comprobaciones computacionales acompañan las pruebas generales del
manuscrito; no seleccionan un operador físico de Dirac desde TPK.
"""

from __future__ import annotations

import ast
from itertools import product
from pathlib import Path
import sys
from typing import Iterable


Matrix = tuple[tuple[int, ...], ...]
ComplexMatrix = tuple[Matrix, Matrix]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def zero(rows: int, cols: int | None = None) -> Matrix:
    width = rows if cols is None else cols
    return tuple(tuple(0 for _ in range(width)) for _ in range(rows))


def identity(size: int) -> Matrix:
    return tuple(
        tuple(1 if row == col else 0 for col in range(size))
        for row in range(size)
    )


def add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(x + y for x, y in zip(row_left, row_right))
        for row_left, row_right in zip(left, right)
    )


def subtract(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(x - y for x, y in zip(row_left, row_right))
        for row_left, row_right in zip(left, right)
    )


def scale(coefficient: int, matrix: Matrix) -> Matrix:
    return tuple(
        tuple(coefficient * entry for entry in row)
        for row in matrix
    )


def transpose(matrix: Matrix) -> Matrix:
    return tuple(tuple(row) for row in zip(*matrix))


def matmul(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(
            sum(left[row][k] * right[k][col] for k in range(len(right)))
            for col in range(len(right[0]))
        )
        for row in range(len(left))
    )


def matvec(matrix: Matrix, vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sum(entry * coordinate for entry, coordinate in zip(row, vector))
        for row in matrix
    )


def power(matrix: Matrix, exponent: int) -> Matrix:
    result = identity(len(matrix))
    factor = matrix
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = matmul(result, factor)
        factor = matmul(factor, factor)
        remaining >>= 1
    return result


def kron(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(
            left[i][j] * right[r][s]
            for j in range(len(left[0]))
            for s in range(len(right[0]))
        )
        for i in range(len(left))
        for r in range(len(right))
    )


def block(top_left: Matrix, top_right: Matrix,
          bottom_left: Matrix, bottom_right: Matrix) -> Matrix:
    top = tuple(
        tuple(left_row) + tuple(right_row)
        for left_row, right_row in zip(top_left, top_right)
    )
    bottom = tuple(
        tuple(left_row) + tuple(right_row)
        for left_row, right_row in zip(bottom_left, bottom_right)
    )
    return top + bottom


def complex_mul(left: ComplexMatrix, right: ComplexMatrix) -> ComplexMatrix:
    real_left, imag_left = left
    real_right, imag_right = right
    return (
        subtract(
            matmul(real_left, real_right),
            matmul(imag_left, imag_right),
        ),
        add(
            matmul(real_left, imag_right),
            matmul(imag_left, real_right),
        ),
    )


def realify(matrix: ComplexMatrix) -> Matrix:
    real, imag = matrix
    return block(real, scale(-1, imag), imag, real)


def matrix_unit(size: int, row: int, col: int) -> Matrix:
    return tuple(
        tuple(1 if (i, j) == (row, col) else 0 for j in range(size))
        for i in range(size)
    )


def verify_clifford() -> tuple[Matrix, ...]:
    i2 = identity(2)
    j2: Matrix = ((0, 1), (-1, 0))
    r2: Matrix = ((0, 1), (1, 0))
    z2: Matrix = ((1, 0), (0, -1))
    gamma = (
        kron(j2, i2),
        kron(r2, i2),
        kron(z2, r2),
        kron(z2, z2),
    )
    metric = (-1, 1, 1, 1)
    i4 = identity(4)
    for mu in range(4):
        for nu in range(4):
            anticommutator = add(
                matmul(gamma[mu], gamma[nu]),
                matmul(gamma[nu], gamma[mu]),
            )
            expected = (
                scale(2 * metric[mu], i4)
                if mu == nu
                else zero(4)
            )
            require(
                anticommutator == expected,
                f"relación de Clifford fallida para {(mu, nu)}",
            )

    bad_gamma = list(gamma)
    mutated = [list(row) for row in bad_gamma[3]]
    mutated[0][0] += 1
    bad_gamma[3] = tuple(tuple(row) for row in mutated)
    bad_square = matmul(bad_gamma[3], bad_gamma[3])
    require(
        bad_square != i4,
        "el control negativo de Clifford no fue detectado",
    )
    return gamma


def verify_realification() -> int:
    size = 2
    z = zero(size)
    real_basis: list[ComplexMatrix] = []
    for row in range(size):
        for col in range(size):
            unit = matrix_unit(size, row, col)
            real_basis.append((unit, z))
            real_basis.append((z, unit))

    i_complex: ComplexMatrix = (z, identity(size))
    j_sp = realify(i_complex)
    require(
        matmul(j_sp, j_sp) == scale(-1, identity(2 * size)),
        "J_sp^2 != -I",
    )
    for basis_element in real_basis:
        represented = realify(basis_element)
        require(
            matmul(j_sp, represented) == matmul(represented, j_sp),
            "J_sp no conmuta con un elemento de la base realificada",
        )
    checked_products = 0
    for left in real_basis:
        for right in real_basis:
            require(
                realify(complex_mul(left, right))
                == matmul(realify(left), realify(right)),
                "la realificación no preserva un producto de la base",
            )
            checked_products += 1
    return checked_products


def path_sum_entry(matrix: Matrix, exponent: int,
                   start: int, finish: int) -> int:
    size = len(matrix)
    if exponent == 0:
        return int(start == finish)
    total = 0
    for intermediate in product(range(size), repeat=max(0, exponent - 1)):
        route = (start,) + intermediate + (finish,)
        weight = 1
        for step in range(1, len(route)):
            weight *= matrix[route[step]][route[step - 1]]
        total += weight
    return total


def verify_paths_and_norm() -> tuple[int, int]:
    matrix: Matrix = (
        (1, 2, 0),
        (-1, 1, 3),
        (2, 0, 1),
    )
    exponent = 4
    matrix_power = power(matrix, exponent)
    checked_entries = 0
    for finish in range(3):
        for start in range(3):
            require(
                matrix_power[finish][start]
                == path_sum_entry(matrix, exponent, start, finish),
                f"suma de caminos fallida para {(start, finish)}",
            )
            checked_entries += 1

    omitted_path_sum = path_sum_entry(matrix, exponent, 0, 2)
    route_weight = matrix[0][0] * matrix[0][0] * matrix[0][0] * matrix[2][0]
    require(
        omitted_path_sum - route_weight != matrix_power[2][0],
        "el control negativo de caminos no fue detectado",
    )

    unitary: Matrix = (
        (0, 1, 0),
        (0, 0, -1),
        (1, 0, 0),
    )
    require(
        matmul(transpose(unitary), unitary) == identity(3),
        "la matriz de control no es ortogonal",
    )
    vector = (2, -3, 5)
    evolved = matvec(power(unitary, 7), vector)
    norm_squared = sum(coordinate * coordinate for coordinate in vector)
    evolved_norm_squared = sum(coordinate * coordinate for coordinate in evolved)
    require(
        evolved_norm_squared == norm_squared,
        "una evolución unitaria no conservó la norma",
    )

    nonunitary: Matrix = ((2, 0, 0), (0, 1, 0), (0, 0, 1))
    bad_evolved = matvec(nonunitary, vector)
    bad_norm_squared = sum(coordinate * coordinate for coordinate in bad_evolved)
    require(
        bad_norm_squared != norm_squared,
        "el control negativo no unitario no alteró la norma",
    )
    return checked_entries, norm_squared


def verify_no_assert_nodes() -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    require(
        not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
        "assert detectado",
    )


def main() -> int:
    gamma = verify_clifford()
    realification_products = verify_realification()
    path_entries, norm_squared = verify_paths_and_norm()
    verify_no_assert_nodes()
    print(
        "PASS_DIRAC_REAL_CAMINOS "
        f"clifford_generators={len(gamma)} "
        f"realification_basis_products={realification_products} "
        f"path_entries={path_entries} "
        f"unitary_norm_squared={norm_squared} "
        "negative_controls=3"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
