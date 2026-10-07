#!/usr/bin/env python3
"""Certificado exacto y autónomo del menor estatal APP--Witt.

Deriva las órbitas de multiplicación por cuatro, los vectores beta en
las bases de aumento y Psi; calcula el menor de 24 estados con Fraction.
El alcance es finito: rango de la matriz estatal, equivarianza en las
729 ternas y los datos del alineamiento. No certifica un resultado
infinito ni depende de numpy, sympy, un PDF o del modo de optimización.

Procedencia: source/sections/fibras_app_witt.tex, proposición
nuclear:psi-rango y construcción nuclear:alineamiento-witt.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
import sys


class VerificationFailure(Exception):
    """Discrepancia exacta del certificado."""


CHECKS = []


def require(condition, name, detail=""):
    if not condition:
        raise VerificationFailure(name + (": " + detail if detail else ""))
    CHECKS.append(name)


def identity(n):
    return [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def multiply(left, right):
    if not left or not right or len(left[0]) != len(right):
        raise VerificationFailure("Dimensiones incompatibles en producto")
    return [
        [
            sum((left[i][k] * right[k][j] for k in range(len(right))), Fraction(0))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def act(matrix, vector):
    if not matrix or len(matrix[0]) != len(vector):
        raise VerificationFailure("Dimensiones incompatibles en acción")
    return tuple(
        sum((a * b for a, b in zip(row, vector)), Fraction(0)) for row in matrix
    )


def orbit_under_four(seed):
    orbit = []
    value = seed
    while value not in orbit:
        orbit.append(value)
        value = (4 * value) % 9
    if value != seed:
        raise VerificationFailure("Órbita con cola inesperada")
    return tuple(orbit)


ORBITS = tuple(orbit_under_four(seed) for seed in (1, 2))


def standard_vector(index, dimension=3):
    return tuple(Fraction(int(j == index)) for j in range(dimension))


def subtract(left, right):
    return tuple(a - b for a, b in zip(left, right))


BASIS = (
    subtract(standard_vector(0), standard_vector(1)),
    subtract(standard_vector(1), standard_vector(2)),
)


def augmentation_coordinates(vector):
    """Resuelve a*b1+b*b2=vector exactamente, sin tabla de beta."""
    if len(vector) != 3 or sum(vector) != 0:
        raise VerificationFailure("El vector no pertenece al módulo de aumento")
    coordinates = (Fraction(vector[0]), -Fraction(vector[2]))
    reconstructed = tuple(
        coordinates[0] * BASIS[0][j] + coordinates[1] * BASIS[1][j]
        for j in range(3)
    )
    if reconstructed != tuple(vector):
        raise VerificationFailure("Falló la reconstrucción en la base de aumento")
    return coordinates


def beta(orbit, residue):
    residue %= 9
    if residue not in orbit:
        return (Fraction(0), Fraction(0))
    first = standard_vector(orbit.index(residue))
    second = standard_vector(orbit.index((4 * residue) % 9))
    return augmentation_coordinates(subtract(first, second))


def derive_coxeter(orbit):
    columns = []
    for basis_vector in BASIS:
        image = [Fraction(0)] * 3
        for j, coefficient in enumerate(basis_vector):
            target = orbit.index((4 * orbit[j]) % 9)
            image[target] += coefficient
        columns.append(augmentation_coordinates(tuple(image)))
    return transpose(columns)


PAIRS = ((0, 1), (1, 2), (2, 0))


def psi(state):
    if len(state) != 3 or any(not isinstance(x, int) or not 0 <= x < 9 for x in state):
        raise VerificationFailure("Estado fuera de (Z/9Z)^3")
    output = []
    for i, j in PAIRS:
        readings = ((state[i] + state[j]) % 9, (state[i] * state[j]) % 9)
        for reading in readings:
            for orbit in ORBITS:
                output.extend(beta(orbit, reading))
    return tuple(output)


STATES = (
    (0, 0, 1), (0, 0, 2), (0, 0, 4), (0, 0, 5),
    (0, 1, 0), (0, 1, 1), (0, 1, 2), (0, 1, 3),
    (0, 1, 4), (0, 1, 5), (0, 1, 6), (0, 2, 0),
    (0, 2, 2), (0, 2, 3), (0, 4, 0), (0, 5, 0),
    (1, 0, 1), (1, 0, 2), (1, 0, 4), (1, 0, 5),
    (1, 1, 0), (1, 2, 0), (1, 4, 0), (1, 5, 0),
)

EXPECTED_PIVOT_COLUMNS = (
    8, 10, 9, 11, 0, 12, 14, 16, 13, 15, 17, 2,
    18, 19, 1, 3, 20, 22, 21, 23, 4, 6, 5, 7,
)
EXPECTED_PIVOTS = (
    1, 1, 1, -1, 1, 1, 1, 1, 1, -1, 3, 1,
    1, 3, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1,
)


def sequential_rows(matrix):
    """Eliminación por filas anteriores en el orden impreso."""
    basis = []
    pivot_columns = []
    pivots = []
    for source_row in matrix:
        row = [Fraction(value) for value in source_row]
        for pivot_column, previous in basis:
            coefficient = row[pivot_column]
            row = [a - coefficient * b for a, b in zip(row, previous)]
        pivot_column = next((j for j, value in enumerate(row) if value), None)
        if pivot_column is None:
            continue
        pivot = row[pivot_column]
        normalized = [value / pivot for value in row]
        basis.append((pivot_column, normalized))
        pivot_columns.append(pivot_column)
        pivots.append(pivot)
    return tuple(pivot_columns), tuple(pivots)


def determinant(matrix):
    """Eliminación independiente con columnas en orden natural."""
    n = len(matrix)
    if not n or any(len(row) != n for row in matrix):
        raise VerificationFailure("El determinante requiere matriz cuadrada no vacía")
    rows = [[Fraction(value) for value in row] for row in matrix]
    result = Fraction(1)
    for column in range(n):
        selected = next((i for i in range(column, n) if rows[i][column]), None)
        if selected is None:
            return Fraction(0)
        if selected != column:
            rows[column], rows[selected] = rows[selected], rows[column]
            result = -result
        pivot = rows[column][column]
        result *= pivot
        for i in range(column + 1, n):
            factor = rows[i][column] / pivot
            for j in range(column, n):
                rows[i][j] -= factor * rows[column][j]
    return result


def permutation_sign(permutation):
    n = len(permutation)
    if sorted(permutation) != list(range(n)):
        raise VerificationFailure("Las columnas pivote no son una permutación")
    inversions = sum(
        permutation[i] > permutation[j] for i in range(n) for j in range(i + 1, n)
    )
    return -1 if inversions % 2 else 1


def require_determinant(matrix, expected):
    actual = determinant(matrix)
    if actual != expected:
        raise VerificationFailure(
            "Determinante incorrecto: obtenido " + str(actual) + ", esperado " + str(expected)
        )
    return actual


def fraction_text(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def verify():
    CHECKS.clear()
    require(ORBITS == ((1, 4, 7), (2, 8, 5)), "orbitas_derivadas")
    c = derive_coxeter(ORBITS[0])
    require(c == derive_coxeter(ORBITS[1]), "coxeter_comun_en_ambas_orbitas")
    require(c == [[0, -1], [1, -1]], "matriz_coxeter_derivada")
    gram = [[sum(a * b for a, b in zip(x, y)) for y in BASIS] for x in BASIS]
    require(gram == [[2, -1], [-1, 2]], "gram_derivado_de_base_ortogonal")
    require(multiply(multiply(transpose(c), gram), c) == gram, "isometria_coxeter")
    c_inverse = multiply(c, c)
    require(multiply(c, c_inverse) == identity(2), "orden_tres")
    beta_values = tuple(tuple(beta(orbit, value) for value in orbit) for orbit in ORBITS)
    require(
        all(values == ((1, 0), (0, 1), (-1, -1)) for values in beta_values),
        "beta_derivada_en_base_aumento",
    )
    for orbit in ORBITS:
        for value in range(9):
            if beta(orbit, (4 * value) % 9) != act(c, beta(orbit, value)):
                raise VerificationFailure("Equivarianza beta fallida")
    CHECKS.append("equivarianza_beta_18_casos")

    checked_states = 0
    for state in product(range(9), repeat=3):
        vector = psi(state)
        transformed_state = tuple((4 * value) % 9 for value in state)
        transformed_vector = []
        for pair_index in range(3):
            for sheet in range(2):
                operator = c if sheet == 0 else c_inverse
                for orbit_index in range(2):
                    offset = 2 * (4 * pair_index + 2 * sheet + orbit_index)
                    transformed_vector.extend(act(operator, vector[offset:offset + 2]))
        if psi(transformed_state) != tuple(transformed_vector):
            raise VerificationFailure("Equivarianza Psi fallida en " + str(state))
        checked_states += 1
    require(checked_states == 729, "equivarianza_psi_729_estados")

    require(len(STATES) == 24 and len(set(STATES)) == 24, "lista_24_estados_distintos")
    matrix = [list(psi(state)) for state in STATES]
    require(all(len(row) == 24 for row in matrix), "matriz_24_por_24")
    pivot_columns, pivots = sequential_rows(matrix)
    rank = len(pivot_columns)
    require(rank == 24, "rango_24_eliminacion_explicita")
    require(pivot_columns == EXPECTED_PIVOT_COLUMNS, "columnas_pivote_impresas")
    require(pivots == EXPECTED_PIVOTS, "pivotes_impresos")
    pivot_product = Fraction(1)
    for pivot in pivots:
        pivot_product *= pivot
    sign = permutation_sign(pivot_columns)
    det_from_pivots = sign * pivot_product
    require(det_from_pivots == 9, "determinante_9_por_pivotes")
    det_independent = require_determinant(matrix, Fraction(9))
    CHECKS.append("determinante_9_eliminacion_independiente")
    require(det_independent == det_from_pivots, "concordancia_dos_eliminaciones")

    singular = [row[:] for row in matrix]
    singular[-1] = singular[0][:]
    require(determinant(singular) == 0, "control_negativo_fila_repetida_singular")
    require(len(sequential_rows(singular)[0]) == 23, "control_negativo_rango_23")
    rejected = False
    try:
        require_determinant(singular, Fraction(9))
    except VerificationFailure:
        rejected = True
    require(rejected, "control_negativo_rechazo_explicito")

    r = [[Fraction(0), Fraction(1)], [Fraction(1), Fraction(0)]]
    require(multiply(multiply(r, c), r) == c_inverse, "reflexion_conjuga_inversa")
    require(multiply(multiply(transpose(r), gram), r) == gram, "reflexion_isometrica")
    alignment = [4 * i + 2 * mu + epsilon
                 for i in range(3) for mu in range(2) for epsilon in range(2)]
    require(alignment == list(range(12)), "alineamiento_doce_posiciones")

    encoded_matrix = [[fraction_text(value) for value in row] for row in matrix]
    canonical = json.dumps(encoded_matrix, separators=(",", ":"), ensure_ascii=True)
    return {
        "status": "PASS_MENOR_APP_WITT_FINITO",
        "scope": "Menor estatal 24x24, rango 24, equivarianza en 729 estados y alineamiento finito.",
        "source_locator": "source/sections/fibras_app_witt.tex#nuclear:psi-rango",
        "source_of_coefficients": "Suma y producto modulo 9; orbitas por multiplicacion por 4; modulo de aumento.",
        "optimization": sys.flags.optimize,
        "python_version": sys.version.split()[0],
        "arithmetic": "fractions.Fraction",
        "dependencies": "Python standard library only",
        "orbits": [list(orbit) for orbit in ORBITS],
        "basis": [[fraction_text(value) for value in vector] for vector in BASIS],
        "beta_in_orbit_order": [
            [[fraction_text(value) for value in vector] for vector in values]
            for values in beta_values
        ],
        "coxeter": [[fraction_text(value) for value in row] for row in c],
        "gram": [[fraction_text(value) for value in row] for row in gram],
        "states_in_printed_row_order": [list(state) for state in STATES],
        "coordinate_order": {
            "pairs_zero_based": [list(pair) for pair in PAIRS],
            "sheets": ["Sigma", "Pi"],
            "orbits": ["O0", "O1"],
            "augmentation_basis": ["b1", "b2"],
        },
        "matrix": encoded_matrix,
        "matrix_sha256": sha256(canonical.encode("ascii")).hexdigest(),
        "pivot_columns": list(pivot_columns),
        "pivots": [fraction_text(value) for value in pivots],
        "column_permutation_sign": sign,
        "pivot_product": fraction_text(pivot_product),
        "determinant": fraction_text(det_independent),
        "rank": rank,
        "equivariance_states_checked": checked_states,
        "negative_control_determinant": "0",
        "negative_control_rank": 23,
        "checks": CHECKS[:],
        "infinite_statement_certified": False,
    }


def main():
    if any(argument != "--json" for argument in sys.argv[1:]):
        print("Uso: python verificar_menor_app_witt.py [--json]", file=sys.stderr)
        return 2
    try:
        report = verify()
    except (VerificationFailure, ArithmeticError, ValueError, TypeError) as error:
        print(json.dumps({
            "status": "FAIL_MENOR_APP_WITT_FINITO",
            "error": str(error),
            "checks_completed": CHECKS,
            "optimization": sys.flags.optimize,
        }, ensure_ascii=False, indent=2))
        return 1
    if "--json" in sys.argv:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(report["status"])
        print("determinante=9; rango=24; estados_equivarianza=729; controles_negativos=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
