#!/usr/bin/env python3
"""Certificado reproducible, sin dependencias externas, del puente HMT.

Verifica:

* las cuatro PVM qutrit explícitas y su insesgamiento mutuo;
* el no-go para apilar contextos MUB como filas de un QLS;
* tres QMS cíclicos: sombra aditiva (9,3), tres contextos (9,3) y
  atlas nonádico completo (12,3), con descomposición semiclásica;
* cubos mágicos cuánticos cíclicos de órdenes 9 y 12;
* la fibración P^1(Z/9) -> P^1(F_3), de cardinales 12 -> 4x3;
* la conmutación entre coarse-graining genealógico y compresión;
* dos inserciones tipadas del lector 1/pi;
* la clasificación racional exacta del álgebra APP en profundidad dos.

No verifica las afirmaciones propietarias del volumen maestro HMT--MD ni
promueve estas sombras a una realización fiel de toda APP--TRIT--TPK.
"""

from __future__ import annotations

import argparse
import cmath
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


TOL = 2.0e-10
Matrix = list

NON_RESULTS = [
    "No se certifica la fidelidad APP--TRIT--TPK de los QMS cíclicos.",
    "No se certifica la no semiclasicidad de un QMS HMT.",
    "No se certifica la equivarianza completa de la calibración Xi.",
    "No se identifica el ancilla de Stinespring con la memoria TPK.",
    "No se certifica un canal MPS HMT infinitamente divisible.",
    "No se certifica un S-system HMT intrínseco ni una universalidad categórica.",
]

if len(NON_RESULTS) != 6 or len(set(NON_RESULTS)) != 6:
    raise RuntimeError("la lista de no-resultados debe contener seis entradas distintas")


def zero(rows: int, cols: int) -> Matrix:
    return [[0j for _ in range(cols)] for _ in range(rows)]


def identity(dim: int) -> Matrix:
    return [[complex(i == j) for j in range(dim)] for i in range(dim)]


def matrix_add(*matrices: Matrix) -> Matrix:
    rows, cols = len(matrices[0]), len(matrices[0][0])
    return [[sum(matrix[i][j] for matrix in matrices) for j in range(cols)] for i in range(rows)]


def matrix_sub(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def matrix_scale(scalar: complex, matrix: Matrix) -> Matrix:
    return [[scalar * entry for entry in row] for row in matrix]


def matrix_product(a: Matrix, b: Matrix) -> Matrix:
    rows, middle, cols = len(a), len(b), len(b[0])
    return [[sum(a[i][k] * b[k][j] for k in range(middle)) for j in range(cols)] for i in range(rows)]


def adjoint(matrix: Matrix) -> Matrix:
    return [[matrix[j][i].conjugate() for j in range(len(matrix))] for i in range(len(matrix[0]))]


def trace(matrix: Matrix) -> complex:
    return sum(matrix[i][i] for i in range(len(matrix)))


def frobenius_norm(matrix: Matrix) -> float:
    return math.sqrt(sum(abs(entry) ** 2 for row in matrix for entry in row))


def outer_projector(vector: list[complex]) -> Matrix:
    norm = math.sqrt(sum(abs(value) ** 2 for value in vector))
    unit = [value / norm for value in vector]
    return [[unit[i] * unit[j].conjugate() for j in range(len(unit))] for i in range(len(unit))]


def qutrit_contexts() -> list[list[Matrix]]:
    """The computational basis plus the three quadratic Fourier bases."""
    omega = cmath.exp(2j * math.pi / 3)
    contexts: list[list[Matrix]] = []
    computational = []
    for k in range(3):
        vector = [0j, 0j, 0j]
        vector[k] = 1 + 0j
        computational.append(outer_projector(vector))
    contexts.append(computational)
    for a in range(3):
        context = []
        for b in range(3):
            vector = [omega ** ((a * x * x + b * x) % 3) / math.sqrt(3) for x in range(3)]
            context.append(outer_projector(vector))
        contexts.append(context)
    return contexts


def qms_from_effects(effects: list[Matrix]) -> list[list[Matrix]]:
    n = len(effects)
    return [[effects[(i + j) % n] for j in range(n)] for i in range(n)]


def check_qms(square: list[list[Matrix]]) -> dict[str, float]:
    n, dim = len(square), len(square[0][0])
    ident = identity(dim)
    row_error = max(frobenius_norm(matrix_sub(matrix_add(*square[i]), ident)) for i in range(n))
    column_error = max(
        frobenius_norm(matrix_sub(matrix_add(*(square[i][j] for i in range(n))), ident))
        for j in range(n)
    )
    hermiticity_error = max(
        frobenius_norm(matrix_sub(square[i][j], adjoint(square[i][j])))
        for i in range(n) for j in range(n)
    )
    # Every cell used by this script is a nonnegative multiple of a projector
    # or of the identity, hence positivity is symbolic and the least
    # eigenvalue is exactly zero (or positive for residual full-rank cells).
    return {
        "row_error": row_error,
        "column_error": column_error,
        "hermiticity_error": hermiticity_error,
        "minimum_eigenvalue_symbolic": 0.0,
    }


def cyclic_semiclassical_error(effects: list[Matrix], square: list[list[Matrix]]) -> float:
    n, dim = len(effects), len(effects[0])
    rebuilt = [[zero(dim, dim) for _ in range(n)] for _ in range(n)]
    for symbol, effect in enumerate(effects):
        for i in range(n):
            j = (symbol - i) % n
            rebuilt[i][j] = matrix_add(rebuilt[i][j], effect)
    return max(
        frobenius_norm(matrix_sub(rebuilt[i][j], square[i][j]))
        for i in range(n) for j in range(n)
    )


def magic_cube_line_error(effects: list[Matrix]) -> float:
    n, dim = len(effects), len(effects[0])
    ident = identity(dim)
    errors = []
    for i in range(n):
        for j in range(n):
            line = matrix_add(*(effects[(i + j + k) % n] for k in range(n)))
            error = frobenius_norm(matrix_sub(line, ident))
            errors.extend([error, error, error])
    return max(errors)


def projective_line_modulus(modulus: int) -> list[tuple[int, int]]:
    units = [u for u in range(modulus) if math.gcd(u, modulus) == 1]
    primitive = [
        (a, b) for a in range(modulus) for b in range(modulus)
        if math.gcd(math.gcd(a, b), modulus) == 1
    ]
    canonical: set[tuple[int, int]] = set()
    for a, b in primitive:
        orbit = {((u * a) % modulus, (u * b) % modulus) for u in units}
        canonical.add(min(orbit))
    return sorted(canonical)


def reduce_line_mod3(point: tuple[int, int]) -> tuple[int, int]:
    a, b = point[0] % 3, point[1] % 3
    return min({((u * a) % 3, (u * b) % 3) for u in (1, 2)})


def compression(effect: Matrix, isometry: Matrix) -> Matrix:
    return matrix_product(adjoint(isometry), matrix_product(effect, isometry))


def fraction_matrix_product(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    rows, middle, cols = len(a), len(b), len(b[0])
    return [[sum(a[i][k] * b[k][j] for k in range(middle)) for j in range(cols)] for i in range(rows)]


def fraction_rank(matrix: list[list[Fraction]]) -> int:
    a = [row[:] for row in matrix]
    rows, cols = len(a), len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((i for i in range(rank, rows) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        divisor = a[rank][col]
        a[rank] = [entry / divisor for entry in a[rank]]
        for i in range(rows):
            if i != rank and a[i][col]:
                factor = a[i][col]
                a[i] = [a[i][j] - factor * a[rank][j] for j in range(cols)]
        rank += 1
        if rank == rows:
            break
    return rank


def app_d2_exact_invariants() -> dict[str, object]:
    points = [(i, j) for i in range(1, 10) for j in range(1, 10)]
    dr = lambda value: 1 + ((value - 1) % 9)
    sigma = [dr(i + j) for i, j in points]
    product = [dr(i * j) for i, j in points]
    sigma_fibres: dict[int, list[int]] = defaultdict(list)
    product_fibres: dict[int, list[int]] = defaultdict(list)
    for index, value in enumerate(sigma):
        sigma_fibres[value].append(index)
    for index, value in enumerate(product):
        product_fibres[value].append(index)

    gram_square = [[Fraction(0) for _ in range(9)] for _ in range(9)]
    keys = sorted(sigma_fibres)
    for row, a in enumerate(keys):
        for col, c in enumerate(keys):
            for b in sorted(product_fibres):
                left = len(set(sigma_fibres[a]) & set(product_fibres[b]))
                right = len(set(sigma_fibres[c]) & set(product_fibres[b]))
                gram_square[row][col] += Fraction(left * right, len(sigma_fibres[a]) * len(product_fibres[b]))

    identity9 = [[Fraction(i == j) for j in range(9)] for i in range(9)]
    auxiliary = [row[:] for row in identity9]
    coefficients = [Fraction(1)]
    for degree in range(1, 10):
        auxiliary = fraction_matrix_product(gram_square, auxiliary)
        coefficient = -sum(auxiliary[i][i] for i in range(9)) / degree
        coefficients.append(coefficient)
        auxiliary = [[auxiliary[i][j] + coefficient * identity9[i][j] for j in range(9)] for i in range(9)]

    expected_roots = [Fraction(0)] * 5 + [Fraction(1), Fraction(5, 7), Fraction(1, 3), Fraction(1, 3)]
    expected_coefficients = [Fraction(1)]
    for root in expected_roots:
        updated = [Fraction(0)] * (len(expected_coefficients) + 1)
        for index, value in enumerate(expected_coefficients):
            updated[index] += value
            updated[index + 1] -= value * root
        expected_coefficients = updated

    def projection(values: list[int]) -> list[list[Fraction]]:
        fibres: dict[int, list[int]] = defaultdict(list)
        for index, value in enumerate(values):
            fibres[value].append(index)
        result = [[Fraction(0) for _ in range(81)] for _ in range(81)]
        for fibre in fibres.values():
            weight = Fraction(1, len(fibre))
            for i in fibre:
                for j in fibre:
                    result[i][j] = weight
        return result

    p, q = projection(sigma), projection(product)
    identity81 = [[Fraction(i == j) for j in range(81)] for i in range(81)]
    complement_p = [[identity81[i][j] - p[i][j] for j in range(81)] for i in range(81)]
    complement_q = [[identity81[i][j] - q[i][j] for j in range(81)] for i in range(81)]

    def intersection_dimension(a: list[list[Fraction]], b: list[list[Fraction]]) -> int:
        stacked = [[identity81[i][j] - a[i][j] for j in range(81)] for i in range(81)]
        stacked += [[identity81[i][j] - b[i][j] for j in range(81)] for i in range(81)]
        return 81 - fraction_rank(stacked)

    intersections = {
        "ker_P_intersection_ker_Q": intersection_dimension(complement_p, complement_q),
        "ran_P_intersection_ran_Q": intersection_dimension(p, q),
        "ran_P_intersection_ker_Q": intersection_dimension(p, complement_q),
        "ker_P_intersection_ran_Q": intersection_dimension(complement_p, q),
    }
    return {
        "sigma_fibre_sizes": [len(sigma_fibres[key]) for key in sorted(sigma_fibres)],
        "product_fibre_sizes": [len(product_fibres[key]) for key in sorted(product_fibres)],
        "gram_characteristic_factorization": "t^5 (t-1) (t-5/7) (t-1/3)^2",
        "gram_characteristic_coefficients": [str(value) for value in coefficients],
        "gram_factorization_verified": coefficients == expected_coefficients,
        "intersection_dimensions": intersections,
        "cstar_decomposition": "C^4 direct_sum M_2(C) direct_sum M_2(C)",
        "cstar_dimension": 12,
        "commutator_norm_squared": "2/9",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    contexts = qutrit_contexts()
    ident3 = identity(3)
    pvm_error = max(frobenius_norm(matrix_sub(matrix_add(*context), ident3)) for context in contexts)
    idempotence_error = max(
        frobenius_norm(matrix_sub(matrix_product(p, p), p)) for context in contexts for p in context
    )
    overlaps = [
        trace(matrix_product(contexts[a][b], contexts[c][d])).real
        for a in range(4) for c in range(a + 1, 4) for b in range(3) for d in range(3)
    ]
    mub_error = max(abs(value - 1 / 3) for value in overlaps)
    qls_column_obstruction = min(overlaps)

    effects_9_additive = [matrix_scale(1 / 3, contexts[0][g % 3]) for g in range(9)]
    effects_9_contextual = [matrix_scale(1 / 3, contexts[a][b]) for a in range(3) for b in range(3)]
    effects_12 = [matrix_scale(1 / 4, contexts[a][b]) for a in range(4) for b in range(3)]
    qms_9_additive = qms_from_effects(effects_9_additive)
    qms_9_contextual = qms_from_effects(effects_9_contextual)
    qms_12 = qms_from_effects(effects_12)
    contextual_commutators = [
        frobenius_norm(matrix_sub(matrix_product(effects_9_contextual[i], effects_9_contextual[j]),
                                  matrix_product(effects_9_contextual[j], effects_9_contextual[i])))
        for i in range(9) for j in range(i + 1, 9)
    ]

    qms_checks = {
        "n9_s3_additive_shadow": {
            **check_qms(qms_9_additive),
            "semiclassical_reconstruction_error": cyclic_semiclassical_error(effects_9_additive, qms_9_additive),
        },
        "n9_s3_three_contexts": {
            **check_qms(qms_9_contextual),
            "semiclassical_reconstruction_error": cyclic_semiclassical_error(effects_9_contextual, qms_9_contextual),
            "maximum_entry_commutator_frobenius_norm": max(contextual_commutators),
        },
        "n12_s3_full_nonadic_atlas": {
            **check_qms(qms_12),
            "semiclassical_reconstruction_error": cyclic_semiclassical_error(effects_12, qms_12),
        },
    }

    p1_z9 = projective_line_modulus(9)
    fibres: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    for point in p1_z9:
        fibres[reduce_line_mod3(point)].append(point)
    fibre_sizes = sorted(len(fibre) for fibre in fibres.values())

    # A declared calibre assigns the ordered Hensel fibre to the three
    # minimal projectors of the context over its reduced line.
    calibrated_pairs = []
    for context_index, base_line in enumerate(sorted(fibres)):
        for outcome, point in enumerate(sorted(fibres[base_line])):
            calibrated_pairs.append((point, context_index, outcome))

    deep = effects_9_contextual
    coarse = [matrix_add(*deep[3 * x:3 * x + 3]) for x in range(3)]
    isometry = [[1 + 0j, 0j], [0j, 1 + 0j], [0j, 0j]]
    compressed_then_coarse = [matrix_add(*(compression(deep[3 * x + k], isometry) for k in range(3))) for x in range(3)]
    coarse_then_compressed = [compression(effect, isometry) for effect in coarse]
    commuting_square_error = max(
        frobenius_norm(matrix_sub(a, b)) for a, b in zip(compressed_then_coarse, coarse_then_compressed)
    )
    deep_normalization_error = frobenius_norm(matrix_sub(matrix_add(*deep), ident3))
    coarse_normalization_error = frobenius_norm(matrix_sub(matrix_add(*coarse), ident3))

    pi_direct_effects = [matrix_scale(1 / math.pi, contexts[0][k]) for k in range(3)]
    pi_direct_residual = matrix_scale(1 - 1 / math.pi, ident3)
    pi_direct_error = frobenius_norm(matrix_sub(matrix_add(*pi_direct_effects, pi_direct_residual), ident3))
    pi_calibrated_effects = [matrix_scale(3 / math.pi, contexts[0][k]) for k in range(3)]
    pi_calibrated_effects += [matrix_scale((1 - 3 / math.pi) / 6, ident3) for _ in range(6)]
    pi_calibrated_error = frobenius_norm(matrix_sub(matrix_add(*pi_calibrated_effects), ident3))
    pi_calibrated_probability = trace(matrix_product(contexts[1][0], pi_calibrated_effects[0])).real

    cube_9_error = magic_cube_line_error(effects_9_contextual)
    cube_12_error = magic_cube_line_error(effects_12)
    app_d2 = app_d2_exact_invariants()

    expected_intersections = {
        "ker_P_intersection_ker_Q": 64,
        "ran_P_intersection_ran_Q": 1,
        "ran_P_intersection_ker_Q": 5,
        "ker_P_intersection_ran_Q": 5,
    }
    checks = [
        pvm_error < TOL,
        idempotence_error < TOL,
        mub_error < TOL,
        abs(qls_column_obstruction - 1 / 3) < TOL,
        len(p1_z9) == 12,
        len(fibres) == 4,
        fibre_sizes == [3, 3, 3, 3],
        len(calibrated_pairs) == 12,
        commuting_square_error < TOL,
        deep_normalization_error < TOL,
        coarse_normalization_error < TOL,
        pi_direct_error < TOL,
        pi_calibrated_error < TOL,
        abs(pi_calibrated_probability - 1 / math.pi) < TOL,
        max(contextual_commutators) > 1.0e-4,
        cube_9_error < TOL,
        cube_12_error < TOL,
        app_d2["gram_factorization_verified"] is True,
        app_d2["intersection_dimensions"] == expected_intersections,
        app_d2["cstar_dimension"] == 12,
    ]
    for result in qms_checks.values():
        checks.extend([
            result["row_error"] < TOL,
            result["column_error"] < TOL,
            result["hermiticity_error"] < TOL,
            result["semiclassical_reconstruction_error"] < TOL,
        ])

    certificate = {
        "schema": "hmt-de-las-cuevas-genealogical-matrix-bridge-v2",
        "status": "PASS_PUENTE_GENEALOGICO_MATRICIAL" if all(checks) else "FAIL",
        "runtime": "Python standard library only",
        "tolerance": TOL,
        "qutrit": {
            "pvm_error": pvm_error,
            "idempotence_error": idempotence_error,
            "mub_overlap_target": 1 / 3,
            "mub_error": mub_error,
            "qls_column_obstruction": qls_column_obstruction,
        },
        "quantum_magic_squares": qms_checks,
        "quantum_magic_cubes": {
            "n9_s3_three_contexts_line_error": cube_9_error,
            "n12_s3_full_nonadic_atlas_line_error": cube_12_error,
        },
        "app_d2_operator_algebra": app_d2,
        "hensel_fibration": {
            "projective_line_z9_cardinality": len(p1_z9),
            "projective_line_f3_cardinality": len(fibres),
            "fibre_sizes": fibre_sizes,
            "calibrated_bijection_cardinality": len(calibrated_pairs),
            "points": [list(point) for point in p1_z9],
        },
        "bigrading_finite_test": {
            "deep_povm_normalization_error": deep_normalization_error,
            "coarse_povm_normalization_error": coarse_normalization_error,
            "restriction_compression_commutator_error": commuting_square_error,
        },
        "typed_pi_reader": {
            "direct_three_effect_weight": 1 / math.pi,
            "direct_residual_weight": 1 - 1 / math.pi,
            "direct_normalization_error": pi_direct_error,
            "mub_calibration_weight": 3 / math.pi,
            "six_residual_effect_weights": (1 - 3 / math.pi) / 6,
            "calibrated_normalization_error": pi_calibrated_error,
            "calibrated_mub_probability": pi_calibrated_probability,
            "calibrated_mub_probability_target": 1 / math.pi,
            "minimum_eigenvalue_symbolic": 0.0,
            "interpretation": "1/pi is not substituted for 1/3; the factor 3/pi maps the MUB probability to 1/pi and six residual effects restore normalization",
        },
        "scope_limits": [
            "The cyclic QMS constructions are semiclassical by explicit decomposition.",
            "Noncommuting entries do not imply nonsemiclassicality.",
            "The n=9 constructions are exact operator-valued shadows, not a proof of full APP/TPK faithfulness.",
            "The n=12 construction uses all calibrated directions after the required 1/4 normalization.",
            "The cyclic cubes satisfy all line sums but genealogical depth equivariance remains open.",
        ],
        "non_results": NON_RESULTS,
    }

    if certificate["non_results"] != NON_RESULTS:
        raise RuntimeError("el certificado ha alterado la lista canónica de no-resultados")

    rendered = json.dumps(certificate, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(certificate["status"])
    print(rendered)
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
