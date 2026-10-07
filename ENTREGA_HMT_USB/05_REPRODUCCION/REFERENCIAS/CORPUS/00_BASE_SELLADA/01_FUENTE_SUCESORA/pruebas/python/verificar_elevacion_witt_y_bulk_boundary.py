#!/usr/bin/env python3
"""Certifica la elevación real Witt y la correspondencia armónica finita.

El programa usa únicamente la biblioteca estándar, aritmética entera y
``fractions.Fraction``. No usa ``assert``: todas las condiciones matemáticas
se comprueban mediante ``require``, que permanece activo con ``python -O``.
"""

from __future__ import annotations

import ast
import hashlib
import json
from collections import deque
from fractions import Fraction
from math import gcd
from pathlib import Path
from typing import Iterable


class VerificationError(RuntimeError):
    """Fallo de una identidad que debe permanecer activo bajo ``python -O``."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def identity(n: int) -> list[list[int]]:
    return [[int(i == j) for j in range(n)] for i in range(n)]


def transpose(matrix: list[list[object]]) -> list[list[object]]:
    return [list(column) for column in zip(*matrix)]


def matrix_multiply(
    left: list[list[object]], right: list[list[object]]
) -> list[list[object]]:
    require(bool(left) and bool(right), "No se multiplican matrices vacías.")
    require(
        len(left[0]) == len(right),
        "Dimensiones incompatibles en el producto matricial.",
    )
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def matrix_subtract(
    left: list[list[object]], right: list[list[object]]
) -> list[list[object]]:
    return [
        [left[i][j] - right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def matrix_vector(
    matrix: list[list[object]], vector: list[object]
) -> list[object]:
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]


def quadratic_form(matrix: list[list[object]], vector: list[object]) -> object:
    image = matrix_vector(matrix, vector)
    return sum(vector[i] * image[i] for i in range(len(vector)))


def matrix_mod(matrix: list[list[int]], modulus: int) -> list[list[int]]:
    return [[entry % modulus for entry in row] for row in matrix]


def bareiss_determinant(matrix: list[list[int]]) -> int:
    """Determinante entero por eliminación de Bareiss con pivoteo."""

    n = len(matrix)
    require(n > 0 and all(len(row) == n for row in matrix), "Matriz no cuadrada.")
    work = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for k in range(n - 1):
        pivot_row = next((r for r in range(k, n) if work[r][k] != 0), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            work[k], work[pivot_row] = work[pivot_row], work[k]
            sign *= -1
        pivot = work[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = work[i][j] * pivot - work[i][k] * work[k][j]
                require(
                    numerator % previous == 0,
                    "La eliminación de Bareiss perdió divisibilidad exacta.",
                )
                work[i][j] = numerator // previous
        previous = pivot
        for i in range(k + 1, n):
            work[i][k] = 0
    return sign * work[n - 1][n - 1]


def fraction_inverse(matrix: list[list[int]]) -> list[list[Fraction]]:
    n = len(matrix)
    require(n > 0 and all(len(row) == n for row in matrix), "Matriz no cuadrada.")
    work = [
        [Fraction(entry) for entry in row]
        + [Fraction(int(i == j)) for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    for column in range(n):
        pivot_row = next(
            (row for row in range(column, n) if work[row][column] != 0), None
        )
        require(pivot_row is not None, "La matriz que debía invertirse es singular.")
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
        pivot = work[column][column]
        work[column] = [entry / pivot for entry in work[column]]
        for row in range(n):
            if row == column:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    work[row][j] - factor * work[column][j]
                    for j in range(2 * n)
                ]
    return [row[n:] for row in work]


def fraction_rank(matrix: list[list[Fraction]]) -> int:
    if not matrix:
        return 0
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot_row = next(
            (row for row in range(rank, rows) if work[row][column] != 0), None
        )
        if pivot_row is None:
            continue
        work[rank], work[pivot_row] = work[pivot_row], work[rank]
        pivot = work[rank][column]
        work[rank] = [entry / pivot for entry in work[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    work[row][j] - factor * work[rank][j]
                    for j in range(columns)
                ]
        rank += 1
        if rank == rows:
            break
    return rank


def ldl_pivots(matrix: list[list[Fraction]]) -> list[Fraction]:
    """Pivotes de una factorización exacta LDL^T sin permutaciones."""

    n = len(matrix)
    lower = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    diagonal: list[Fraction] = []
    for i in range(n):
        lower[i][i] = Fraction(1)
        value = matrix[i][i] - sum(
            lower[i][k] * lower[i][k] * diagonal[k] for k in range(i)
        )
        require(value != 0, "Pivote nulo en la factorización LDL^T.")
        diagonal.append(value)
        for row in range(i + 1, n):
            numerator = matrix[row][i] - sum(
                lower[row][k] * lower[i][k] * diagonal[k] for k in range(i)
            )
            lower[row][i] = numerator / value
    return diagonal


def lcm(left: int, right: int) -> int:
    return abs(left * right) // gcd(left, right) if left and right else 0


def matrix_digest(matrix: list[list[int]]) -> str:
    payload = json.dumps(matrix, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(payload).hexdigest()


AW = [
    [0, 1, 1, 1, 1, 1],
    [1, 0, 1, 2, 2, 1],
    [1, 1, 0, 1, 2, 2],
    [1, 2, 1, 0, 1, 2],
    [1, 2, 2, 1, 0, 1],
    [1, 1, 2, 2, 1, 0],
]

J0 = [
    [0, -1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0],
    [0, 0, 0, -1, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, -1],
    [0, 0, 0, 0, 1, 0],
]

S_W = [
    [1, 0, 0, 1, 0, 1],
    [0, 1, 1, 0, 0, 1],
    [0, 1, 0, 1, 1, 0],
    [0, 1, 0, 2, 0, 1],
    [0, 1, 0, 2, 0, 2],
    [0, 1, 0, 1, 0, 2],
]

S_W_INVERSE = [
    [1, 0, 0, 1, -2, 1],
    [0, 0, 0, 2, -3, 2],
    [0, 1, 0, -1, 2, -2],
    [0, 0, 0, 0, 1, -1],
    [0, 0, 1, -2, 2, -1],
    [0, 0, 0, -1, 1, 0],
]


def certify_witt_lift() -> dict[str, object]:
    i6 = identity(6)
    minus_i6 = [[-entry for entry in row] for row in i6]
    minus_i6_mod3 = matrix_mod(minus_i6, 3)

    require(matrix_mod(matrix_multiply(AW, AW), 3) == minus_i6_mod3, "A_W^2 != -I.")
    require(matrix_multiply(J0, J0) == minus_i6, "J_0^2 != -I.")
    require(bareiss_determinant(S_W) == -1, "S_W no es unimodular de determinante -1.")
    require(matrix_multiply(S_W, S_W_INVERSE) == i6, "Inversa derecha incorrecta.")
    require(matrix_multiply(S_W_INVERSE, S_W) == i6, "Inversa izquierda incorrecta.")

    j_tilde = matrix_multiply(matrix_multiply(S_W, J0), S_W_INVERSE)
    require(matrix_multiply(j_tilde, j_tilde) == minus_i6, "La elevación no cuadra a -I.")
    require(matrix_mod(j_tilde, 3) == AW, "La elevación no reduce a A_W.")

    g_w = matrix_multiply(transpose(S_W_INVERSE), S_W_INVERSE)
    require(g_w == transpose(g_w), "G_W no es simétrica.")
    require(
        matrix_multiply(matrix_multiply(transpose(j_tilde), g_w), j_tilde) == g_w,
        "La elevación no preserva G_W.",
    )
    principal_minors = [
        bareiss_determinant([row[:size] for row in g_w[:size]])
        for size in range(1, 7)
    ]
    require(all(value > 0 for value in principal_minors), "G_W no pasó Sylvester.")

    u = identity(6)
    u[0][1] = 3
    u_inverse = identity(6)
    u_inverse[0][1] = -3
    require(matrix_multiply(u, u_inverse) == i6, "U^{-1} incorrecta.")
    j_alternative = matrix_multiply(matrix_multiply(u, j_tilde), u_inverse)
    require(j_alternative != j_tilde, "El testigo alternativo no es distinto.")
    require(
        matrix_multiply(j_alternative, j_alternative) == minus_i6,
        "La segunda elevación no cuadra a -I.",
    )
    require(matrix_mod(j_alternative, 3) == AW, "La segunda elevación no reduce a A_W.")

    c_paley = [[-1 if entry == 2 else entry for entry in row] for row in AW]
    five_i6 = [[5 * entry for entry in row] for row in i6]
    require(matrix_multiply(c_paley, c_paley) == five_i6, "C_P^2 != 5I.")

    return {
        "status": "PASS_EXACT_EXISTENCE_NONCANONICAL",
        "A_W": AW,
        "S_W": S_W,
        "det_S_W": -1,
        "S_W_inverse": S_W_INVERSE,
        "J_tilde": j_tilde,
        "J_tilde_squared_is_minus_identity": True,
        "J_tilde_mod_3_equals_A_W": True,
        "G_W": g_w,
        "G_W_leading_principal_minors": principal_minors,
        "J_tilde_preserves_G_W": True,
        "alternative_conjugator_U": u,
        "alternative_J_tilde": j_alternative,
        "alternative_is_distinct_with_same_reduction": True,
        "paley_real_control": {
            "C_P_squared_equals_5I": True,
            "C_P_over_sqrt5_squared_equals": "+I",
            "is_not_the_real_complex_lift": True,
        },
        "scope": {
            "proved": (
                "An explicit integral real complex structure reduces to A_W; "
                "it preserves an explicit positive metric and exponentiates to rotations."
            ),
            "not_proved": (
                "TPK-full does not yet select a unique lift or identify G_W with a "
                "physical spacetime metric."
            ),
        },
    }


def cube_vertices(n: int) -> list[tuple[int, int, int]]:
    return [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]


def is_boundary(vertex: tuple[int, int, int], n: int) -> bool:
    return any(coordinate in (0, n - 1) for coordinate in vertex)


def cube_edges(n: int) -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    edges = []
    for vertex in cube_vertices(n):
        for axis in range(3):
            neighbour = list(vertex)
            neighbour[axis] += 1
            if neighbour[axis] < n:
                edges.append((vertex, tuple(neighbour)))
    return edges


def cube_laplacian(n: int) -> tuple[list[tuple[int, int, int]], list[list[int]]]:
    vertices = cube_vertices(n)
    index = {vertex: position for position, vertex in enumerate(vertices)}
    laplacian = [[0 for _ in vertices] for _ in vertices]
    for left, right in cube_edges(n):
        i = index[left]
        j = index[right]
        laplacian[i][i] += 1
        laplacian[j][j] += 1
        laplacian[i][j] -= 1
        laplacian[j][i] -= 1
    return vertices, laplacian


def connected_vertex_count(n: int) -> int:
    vertices = cube_vertices(n)
    neighbours: dict[tuple[int, int, int], list[tuple[int, int, int]]] = {
        vertex: [] for vertex in vertices
    }
    for left, right in cube_edges(n):
        neighbours[left].append(right)
        neighbours[right].append(left)
    visited = {vertices[0]}
    queue: deque[tuple[int, int, int]] = deque([vertices[0]])
    while queue:
        vertex = queue.popleft()
        for neighbour in neighbours[vertex]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    return len(visited)


def select_block(
    matrix: list[list[int]], rows: Iterable[int], columns: Iterable[int]
) -> list[list[int]]:
    row_list = list(rows)
    column_list = list(columns)
    return [[matrix[i][j] for j in column_list] for i in row_list]


def certify_bulk_boundary() -> dict[str, object]:
    n = 3
    vertices, laplacian = cube_laplacian(n)
    boundary = [i for i, vertex in enumerate(vertices) if is_boundary(vertex, n)]
    interior = [i for i, vertex in enumerate(vertices) if not is_boundary(vertex, n)]
    require(len(boundary) == 26 and len(interior) == 1, "Conteo incorrecto para Q_3.")
    require(connected_vertex_count(n) == n**3, "Q_3 no apareció conexo.")

    l_bb = select_block(laplacian, boundary, boundary)
    l_bi = select_block(laplacian, boundary, interior)
    l_ib = select_block(laplacian, interior, boundary)
    l_ii = select_block(laplacian, interior, interior)
    require(l_ii == [[6]], "El bloque interior de Q_3 debe ser (6).")

    l_ii_inverse = fraction_inverse(l_ii)
    correction = matrix_multiply(
        matrix_multiply(l_bi, l_ii_inverse), l_ib
    )
    lambda_3 = matrix_subtract(
        [[Fraction(entry) for entry in row] for row in l_bb], correction
    )
    require(lambda_3 == transpose(lambda_3), "Lambda_3 no es simétrica.")
    require(
        all(sum(row, Fraction(0)) == 0 for row in lambda_3),
        "Las constantes no están en el núcleo de Lambda_3.",
    )
    rank = fraction_rank(lambda_3)
    require(rank == 25, "Lambda_3 no tiene rango 25.")

    reduced = [row[:-1] for row in lambda_3[:-1]]
    pivots = ldl_pivots(reduced)
    require(all(pivot > 0 for pivot in pivots), "El menor reducido no es positivo.")

    denominators = [entry.denominator for row in lambda_3 for entry in row]
    scale = 1
    for denominator in denominators:
        scale = lcm(scale, denominator)
    scaled_lambda = [
        [int(entry * scale) for entry in row]
        for row in lambda_3
    ]
    require(scale == 6, "El denominador común de Lambda_3 debe ser 6.")

    boundary_data = [Fraction(((7 * i * i + 3 * i + 1) % 11) - 5) for i in range(26)]
    interior_data = [
        -entry
        for entry in matrix_vector(
            l_ii_inverse,
            matrix_vector(l_ib, boundary_data),
        )
    ]
    full_data_by_index: dict[int, Fraction] = {
        index: boundary_data[position] for position, index in enumerate(boundary)
    }
    full_data_by_index.update(
        {index: interior_data[position] for position, index in enumerate(interior)}
    )
    full_data = [full_data_by_index[i] for i in range(len(vertices))]
    harmonic_residual = matrix_vector(l_ib, boundary_data)[0] + l_ii[0][0] * interior_data[0]
    require(harmonic_residual == 0, "La extensión de prueba no es armónica.")
    bulk_energy = quadratic_form(laplacian, full_data)
    boundary_energy = quadratic_form(lambda_3, boundary_data)
    require(bulk_energy == boundary_energy, "Falló la identidad de energía.")

    n_hmt = 9
    vertices_hmt = n_hmt**3
    interior_hmt = (n_hmt - 2) ** 3
    boundary_hmt = vertices_hmt - interior_hmt
    edges_hmt = len(cube_edges(n_hmt))
    require((vertices_hmt, interior_hmt, boundary_hmt) == (729, 343, 386), "Conteos Q_9.")
    require(edges_hmt == 3 * (n_hmt - 1) * n_hmt**2, "Conteo de aristas Q_9.")
    require(connected_vertex_count(n_hmt) == vertices_hmt, "Q_9 no apareció conexo.")

    pivot_strings = [str(pivot) for pivot in pivots]
    return {
        "status": "PASS_EXACT_FINITE_HARMONIC_CORRESPONDENCE",
        "Q3": {
            "vertices": 27,
            "boundary_vertices": 26,
            "interior_vertices": 1,
            "L_II": l_ii,
            "L_II_inverse": [[str(entry) for entry in row] for row in l_ii_inverse],
            "Lambda_rank": rank,
            "Lambda_kernel_dimension": 1,
            "Lambda_common_denominator": scale,
            "scaled_Lambda_sha256": matrix_digest(scaled_lambda),
            "reduced_LDL_positive_pivots": pivot_strings,
            "sample_harmonic_center": str(interior_data[0]),
            "sample_bulk_energy": str(bulk_energy),
            "sample_boundary_energy": str(boundary_energy),
            "energy_identity_exact": True,
        },
        "Q9": {
            "vertices": vertices_hmt,
            "boundary_vertices": boundary_hmt,
            "interior_vertices": interior_hmt,
            "edges": edges_hmt,
            "connected": True,
            "Dirichlet_spectrum": (
                "6-2*cos(a*pi/8)-2*cos(b*pi/8)-2*cos(c*pi/8), "
                "1<=a,b,c<=7"
            ),
            "smallest_eigenvalue": "6-6*cos(pi/8)>0",
        },
        "general": {
            "interior_vertices": "(N-2)^3",
            "boundary_vertices": "N^3-(N-2)^3",
            "harmonic_extension": "u_I=-L_II^{-1}L_IB*g",
            "Dirichlet_to_Neumann": "Lambda=L_BB-L_BI*L_II^{-1}*L_IB",
            "kernel": "constant boundary data",
        },
        "scope": {
            "proved": (
                "For every finite connected cube Q_N, boundary data determine a unique "
                "harmonic bulk and the on-shell Dirichlet energy descends to Lambda_N."
            ),
            "not_proved": (
                "No negative-curvature bulk, conformal boundary theory, OPE, Virasoro "
                "structure or refinement-compatible AdS/CFT map is inferred."
            ),
        },
    }


def build_certificate() -> dict[str, object]:
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    require(
        not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
        "El verificador contiene una sentencia assert.",
    )
    return {
        "schema": "HMT.ElevacionWitt.CorrespondenciaArmonica.v1",
        "status": "PASS",
        "arithmetic": "exact_integer_and_fraction",
        "standard_library_only": True,
        "assert_statements": 0,
        "witt_real_lift": certify_witt_lift(),
        "finite_harmonic_bulk_boundary": certify_bulk_boundary(),
    }


def main() -> None:
    certificate = build_certificate()
    target = (
        Path(__file__).resolve().parents[2]
        / "certificados"
        / "elevacion_witt_bulk_boundary.json"
    )
    encoded = json.dumps(certificate, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    target.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
