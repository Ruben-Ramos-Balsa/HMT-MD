#!/usr/bin/env python3
"""Verifica exactamente el cierre qutrit -> álgebra de color.

Los escalares se calculan en Q(omega), con omega^2 + omega + 1 = 0.
No se usan números de coma flotante ni bibliotecas externas.
"""

from __future__ import annotations

import ast
from fractions import Fraction
import pathlib
import sys
from typing import Iterable


Scalar = tuple[Fraction, Fraction]
Matrix = tuple[tuple[Scalar, ...], ...]

ZERO: Scalar = (Fraction(0), Fraction(0))
ONE: Scalar = (Fraction(1), Fraction(0))
OMEGA: Scalar = (Fraction(0), Fraction(1))
OMEGA2: Scalar = (Fraction(-1), Fraction(-1))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def add(x: Scalar, y: Scalar) -> Scalar:
    return (x[0] + y[0], x[1] + y[1])


def mul(x: Scalar, y: Scalar) -> Scalar:
    # (a+bw)(c+dw) = (ac-bd) + (ad+bc-bd)w, pues w^2=-1-w.
    a, b = x
    c, d = y
    return (a * c - b * d, a * d + b * c - b * d)


def conj(x: Scalar) -> Scalar:
    # w-bar = w^2 = -1-w.
    a, b = x
    return (a - b, -b)


def omega_power(exponent: int) -> Scalar:
    return (ONE, OMEGA, OMEGA2)[exponent % 3]


def scalar_mul(x: Scalar, matrix: Matrix) -> Matrix:
    return tuple(tuple(mul(x, entry) for entry in row) for row in matrix)


def identity(size: int) -> Matrix:
    return tuple(
        tuple(ONE if row == col else ZERO for col in range(size))
        for row in range(size)
    )


def matmul(left: Matrix, right: Matrix) -> Matrix:
    size = len(left)
    return tuple(
        tuple(
            sum_scalar(mul(left[row][k], right[k][col]) for k in range(size))
            for col in range(size)
        )
        for row in range(size)
    )


def sum_scalar(values: Iterable[Scalar]) -> Scalar:
    result = ZERO
    for value in values:
        result = add(result, value)
    return result


def power(matrix: Matrix, exponent: int) -> Matrix:
    result = identity(len(matrix))
    factor = matrix
    n = exponent
    while n:
        if n & 1:
            result = matmul(result, factor)
        factor = matmul(factor, factor)
        n >>= 1
    return result


def dagger(matrix: Matrix) -> Matrix:
    size = len(matrix)
    return tuple(
        tuple(conj(matrix[col][row]) for col in range(size))
        for row in range(size)
    )


def trace(matrix: Matrix) -> Scalar:
    return sum_scalar(matrix[index][index] for index in range(len(matrix)))


def main() -> int:
    ident = identity(3)
    x_matrix: Matrix = (
        (ZERO, ZERO, ONE),
        (ONE, ZERO, ZERO),
        (ZERO, ONE, ZERO),
    )
    z_matrix: Matrix = (
        (ONE, ZERO, ZERO),
        (ZERO, OMEGA, ZERO),
        (ZERO, ZERO, OMEGA2),
    )

    require(power(x_matrix, 3) == ident, "X^3 != I")
    require(power(z_matrix, 3) == ident, "Z^3 != I")
    require(
        matmul(z_matrix, x_matrix)
        == scalar_mul(OMEGA, matmul(x_matrix, z_matrix)),
        "ZX != omega XZ",
    )

    weyl: dict[tuple[int, int], Matrix] = {}
    for a in range(3):
        for b in range(3):
            weyl[(a, b)] = matmul(power(x_matrix, a), power(z_matrix, b))

    three: Scalar = (Fraction(3), Fraction(0))
    for key_left, left in weyl.items():
        for key_right, right in weyl.items():
            gram = trace(matmul(dagger(left), right))
            expected = three if key_left == key_right else ZERO
            require(gram == expected, f"Gram incorrecto para {key_left}, {key_right}")

    non_identity = [
        matrix for key, matrix in weyl.items() if key != (0, 0)
    ]
    require(len(weyl) == 9, "base de Weyl no tiene nueve elementos")
    require(len(non_identity) == 8, "sector traceless no tiene ocho elementos")
    require(
        all(trace(matrix) == ZERO for matrix in non_identity),
        "un monomio no trivial posee traza no nula",
    )
    representatives = ((1, 0), (0, 1), (1, 1), (1, 2))
    adjoint_pairs: set[frozenset[tuple[int, int]]] = set()
    for a, b in representatives:
        opposite = ((-a) % 3, (-b) % 3)
        expected_dagger = scalar_mul(
            omega_power(a * b),
            weyl[opposite],
        )
        require(
            dagger(weyl[(a, b)]) == expected_dagger,
            f"fórmula de adjunción incorrecta para {(a, b)}",
        )
        adjoint_pairs.add(frozenset({(a, b), opposite}))
    require(len(adjoint_pairs) == 4, "el sector no trivial no forma cuatro pares")
    covered = set().union(*(set(pair) for pair in adjoint_pairs))
    require(
        covered == set(weyl) - {(0, 0)},
        "los cuatro pares adjuntos no cubren el sector traceless",
    )

    source = pathlib.Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    require(
        not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
        "assert detectado",
    )

    print(
        "PASS_ALGEBRA_COLOR_TRIT "
        "weyl_basis=9 traceless_generators=8 adjoint_pairs=4 "
        "su3_real_dimension=8 relation=ZX_omega_XZ"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
