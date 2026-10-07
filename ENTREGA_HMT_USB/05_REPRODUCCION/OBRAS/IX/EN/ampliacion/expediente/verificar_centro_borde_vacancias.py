#!/usr/bin/env python3
"""Aritmetica finita de APP, centro-borde, vacancias y costura de nueve fases.

Solo biblioteca estandar y Fraction. Las condiciones se comprueban mediante
excepciones explicitas, tambien bajo -O. No construye el estado TPK completo,
la emision regional U desde semillas ni una prueba de Weil/RH.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path
import sys


def rho9(value):
    return 1 + (value - 1) % 9


def lifted(value):
    residue = rho9(value)
    return residue, (value - residue) // 9


def app_record(i, j):
    return lifted(i + j), lifted(i * j)


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def matadd(a, b, scale=F(1)):
    return [[x + scale * y for x, y in zip(row_a, row_b)]
            for row_a, row_b in zip(a, b)]


def matscale(a, scale):
    return [[scale * x for x in row] for row in a]


def matvec(a, vector):
    return [sum((x * y for x, y in zip(row, vector)), F(0)) for row in a]


def norm2(vector):
    return sum((x * x for x in vector), F(0))


def polynomial(coefficients, x, y):
    a, b, c, d = coefficients
    return a + b * x + c * y + d * x * y


def interpolate(corners, x, y):
    t, u = F(x - 3, 3), F(y - 3, 3)
    return ((1-t)*(1-u)*corners[0] + (1-t)*u*corners[1]
            + t*(1-u)*corners[2] + t*u*corners[3])


def nc_add(*polynomials):
    result = {}
    for p in polynomials:
        for word, value in p.items():
            result[word] = result.get(word, F(0)) + value
    return {word: value for word, value in result.items() if value}


def nc_scale(p, scale):
    return {word: scale * value for word, value in p.items() if scale * value}


def nc_mul(p, q):
    result = {}
    for word_p, coefficient_p in p.items():
        for word_q, coefficient_q in q.items():
            word = word_p + word_q
            result[word] = result.get(word, F(0)) + coefficient_p * coefficient_q
    return {word: value for word, value in result.items() if value}


def nc_star(p):
    swap = {"C": "Cs", "Cs": "C"}
    return {tuple(swap[letter] for letter in reversed(word)): coefficient
            for word, coefficient in p.items()}


def run():
    counts = {}

    def equal(group, actual, expected, context):
        if actual != expected:
            raise ArithmeticError("%s (%s): %r != %r"
                                  % (group, context, actual, expected))
        counts[group] = counts.get(group, 0) + 1

    def require(group, condition, context):
        if not condition:
            raise ArithmeticError("%s: %s" % (group, context))
        counts[group] = counts.get(group, 0) + 1

    d9 = range(1, 10)
    table = {(i, j): rho9(i*j) for i, j in product(d9, repeat=2)}
    for i in d9:
        accumulated = 0
        for j in d9:
            accumulated += i
            equal("APP_accumulation", table[i, j], rho9(accumulated), (i, j))
            residue, quotient = lifted(i*j)
            equal("APP_lift", residue + 9*quotient, i*j, (i, j))
            equal("APP_symmetry", table[i, j], table[j, i], (i, j))
    central = [[table[i, j] for j in (4, 5)] for i in (4, 5)]
    equal("central_block", central, [[7, 2], [2, 7]], "residual block")
    equal("central_modes", matvec(central, [1, 1]), [9, 9], "uniform")
    equal("central_modes", matvec(central, [1, -1]), [5, -5], "differential")

    q_points = list(product(range(3, 7), repeat=2))
    perimeter = [(i, j) for i, j in q_points if i in (3, 6) or j in (3, 6)]
    equal("corona_Q", len(perimeter), 12, "cardinality")
    equal("corona_Q", Counter(table[p] for p in perimeter),
          Counter({3: 4, 6: 4, 9: 4}), "residual histogram")
    equal("corona_Q", set(q_points) - set(perimeter),
          set(product((4, 5), repeat=2)), "interior")

    cross = [(i, j) for i, j in table if i % 3 == 0 or j % 3 == 0]
    intersection = [(i, j) for i, j in cross if i % 3 == 0 and j % 3 == 0]
    arms = set(cross) - set(intersection)
    equal("radical_cross", len(cross), 45, "union")
    equal("radical_cross", Counter(table[p] for p in cross),
          Counter({3: 12, 6: 12, 9: 21}), "histogram")
    equal("radical_cross", sum(table[p] for p in cross), 297, "sum")
    equal("radical_cross", len(intersection), 9, "intersection size")
    equal("radical_cross", [table[p] for p in intersection], [9]*9,
          "intersection values")
    equal("radical_cross", sum(table[p] for p in intersection), 9*9,
          "intersection sum")
    equal("radical_cross", len(arms), 36, "arms size")
    equal("radical_cross", sum(table[p] for p in arms), 216, "arms sum")

    corners_xy = [(3, 3), (3, 6), (6, 3), (6, 6)]
    basis = [tuple(F(i == j) for i in range(4)) for j in range(4)]
    coefficient_values = (F(-2), F(-1, 3), F(0), F(1, 2), F(3))
    combinations = list(product(coefficient_values, repeat=4))
    for coefficients in basis + combinations:
        corners = [polynomial(coefficients, i, j) for i, j in corners_xy]
        for i, j in q_points:
            equal("multiaffine_interpolation", interpolate(corners, i, j),
                  polynomial(coefficients, i, j), (coefficients, i, j))
        curvature = (corners[3]-corners[1]-corners[2]+corners[0])/9
        equal("multiaffine_curvature", curvature, coefficients[3], coefficients)
    product_corners = [i*j for i, j in corners_xy]
    equal("corner_lifts", product_corners, [9, 18, 18, 36], "product")
    equal("corner_lifts", [lifted(x) for x in product_corners],
          [(9, 0), (9, 1), (9, 1), (9, 3)], "residue and quotient")
    sum_corners = [i+j for i, j in corners_xy]
    equal("mixed_curvatures", F(product_corners[3]-product_corners[1]
          -product_corners[2]+product_corners[0], 9), F(1), "product")
    equal("mixed_curvatures", F(sum_corners[3]-sum_corners[1]
          -sum_corners[2]+sum_corners[0], 9), F(0), "sum")
    for i, j in q_points:
        f, shifted_f = i*j, i*j+9
        equal("residue_not_lift", rho9(f), rho9(shifted_f), (i, j, "residue"))
        equal("residue_not_lift", lifted(shifted_f)[1]-lifted(f)[1], 1,
              (i, j, "quotient"))
        require("residue_not_lift", f != shifted_f, (i, j, "different lifts"))
    equal("corner_residual_nonuniqueness", [rho9(v) for v in product_corners],
          [rho9(9)]*4, "constant 9 versus product at corners")
    require("corner_residual_nonuniqueness", product_corners != [9]*4,
            "corner residues alone do not select the multiaffine law")

    strata = Counter(sum(coordinate == 10 for coordinate in point)
                     for point in product(range(1, 11), repeat=3))
    equal("cubic_strata", strata, Counter({0: 729, 1: 243, 2: 27, 3: 1}),
          "number of new coordinates")
    equal("cubic_strata", sum(strata.values()), 1000, "whole cube")
    equal("cubic_strata", sum(strata[k] for k in (1, 2, 3)), 271, "corona")
    equal("cubic_strata", strata[0] + 271, 1000, "729+271")
    equal("cubic_strata", sum(strata[k] for k in (0, 1, 2)), 999,
          "all except the triple-new vertex")
    row_readings = [10*row[0]+row[1] for row in central]
    diagonal_readings = [10*central[0][0]+central[1][1],
                         10*central[0][1]+central[1][0]]
    equal("central_decimal_readings", row_readings, [72, 27], "rows")
    equal("central_decimal_readings", diagonal_readings, [77, 22], "diagonals")
    equal("central_decimal_readings", sum(row_readings), 99, "row sum")
    equal("central_decimal_readings", sum(diagonal_readings), 99, "diagonal sum")

    fibre = [(5+t, 5-t, t) for t in range(-4, 5)]
    for i, j, t in fibre:
        equal("F10_fibre", i+j, 10, t)
        equal("F10_fibre", i*j, 25-t*t, t)
        equal("F10_fibre", app_record(i, j)[0], (1, 1), t)
    equal("F10_centre", [t for i, j, t in fibre if i == j], [0], "inversion fixed")
    equal("F10_centre", [t for i, j, t in fibre if rho9(i*j) == 7],
          [-3, 0, 3], "same product residue as the centre")
    equal("F10_centre", app_record(5, 5), ((1, 1), (7, 2)), "centre record")
    vacancies = [(i, j, t) for i, j, t in fibre
                 if app_record(i, j) == ((1, 1), (7, 1))]
    equal("F10_vacancies", vacancies, [(2, 8, -3), (8, 2, 3)], "oriented vacancies")
    for i, j, t in vacancies:
        equal("F10_vacancies", 25-i*j, 9, t)

    # U is a declared emitted tuple. This checks its two readers, not its producer.
    emission = (501, 614, 498, 169, 272, 272)
    digits = [(value//100, (value//10) % 10, value % 10) for value in emission]
    signature = [(tens-hundreds) % 10 for hundreds, tens, units in digits]
    psi = [(-value) % 3 for value in emission]
    equal("emission_readers", signature, [5]*6, "multiplicative signature")
    equal("emission_readers", psi, [0, 1, 0, 2, 1, 1], "oriented ternary reader")
    for index, ((s, tens, units), e) in enumerate(zip(digits, signature)):
        equal("emission_congruences", tens, (s+e) % 10, (index, "second digit"))
        equal("emission_congruences", units, (3*s+5*e+1) % 10,
              (index, "third digit"))

    identity = [[F(1), F(0)], [F(0), F(1)]]
    cases = {
        "zero": ([[0, 0], [0, 0]], True, False),
        "scalar": ([[F(2, 3), 0], [0, F(2, 3)]], True, False),
        "diagonal": ([[F(3, 5), 0], [0, F(-4, 5)]], True, False),
        "nonnormal": ([[F(1, 3), F(1, 4)], [0, F(1, 3)]], True, False),
        "projection": ([[F(1, 2)]*2, [F(1, 2)]*2], True, False),
        "rotation": ([[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]], True, True),
        "identity": (identity, True, True),
        "reflection": ([[1, 0], [0, -1]], True, True),
        "expansive_control": ([[2, 0], [0, 1]], False, False),
    }
    v = [F(2, 3), F(-5, 7)]
    for name, (raw_c, contraction, isometry) in cases.items():
        c = [[F(value) for value in row] for row in raw_c]
        defect = matadd(identity, matmul(transpose(c), c), F(-1))
        positive = (defect[0][0] >= 0 and defect[1][1] >= 0 and
                    defect[0][0]*defect[1][1]-defect[0][1]*defect[1][0] >= 0)
        equal("seam_type", positive, contraction, name)
        equal("seam_type", defect == [[0, 0], [0, 0]], isometry, name)
        t_matrix = matscale(matadd(matscale(identity, F(8)), c), F(1, 9))
        z = [x-y for x, y in zip(matvec(c, v), v)]
        for phase in range(9):
            # Direct S_C J action. The seam enters the chosen output phase.
            sj = [matscale(c if r == phase else identity, F(1, 3))
                  for r in range(9)]
            eta_blocks = [matadd(block, matscale(t_matrix, F(1, 3)), F(-1))
                          for block in sj]
            eta = [row for block in eta_blocks for row in block]
            eta_v = matvec(eta, v)
            expected = [F(8 if r == phase else -1, 27)*coordinate
                        for r in range(9) for coordinate in z]
            equal("seam_nine_phases", eta_v, expected, (name, phase, "components"))
            equal("seam_nine_phases", norm2(eta_v), F(8, 81)*norm2(z),
                  (name, phase, "norm"))
            eta_gram = matmul(transpose(eta), eta)
            delta_c = matadd(c, identity, F(-1))
            expected_gram = matscale(matmul(transpose(delta_c), delta_c), F(8, 81))
            equal("seam_gram", eta_gram, expected_gram, (name, phase))
            visible_defect = matadd(identity, matmul(transpose(t_matrix), t_matrix), F(-1))
            balance = matadd(eta_gram, matscale(defect, F(1, 9)))
            equal("seam_full_balance", visible_defect, balance, (name, phase))
            if isometry:
                equal("seam_isometric_balance", visible_defect, eta_gram, (name, phase))

    # Coefficient identity in the free *-algebra: no finite sampling substitutes it.
    unit, symbol_c = {(): F(1)}, {("C",): F(1)}
    formal_t = nc_scale(nc_add(nc_scale(unit, F(8)), symbol_c), F(1, 9))
    one_minus_c = nc_add(unit, nc_scale(symbol_c, F(-1)))
    left = nc_add(unit, nc_scale(nc_mul(nc_star(formal_t), formal_t), F(-1)))
    right = nc_add(nc_scale(nc_mul(nc_star(one_minus_c), one_minus_c), F(8, 81)),
                   nc_scale(nc_add(unit, nc_scale(nc_mul(nc_star(symbol_c), symbol_c),
                                                       F(-1))), F(1, 9)))
    equal("free_star_polynomial", left, right, "full seam balance coefficients")

    source = Path(__file__).resolve()
    return {
        "status": "PASS_CENTRO_BORDE_VACANCIAS_ALGEBRA_FINITA",
        "checks": sum(counts.values()), "checks_by_group": counts,
        "optimization_level": sys.flags.optimize,
        "python": sys.version.split()[0],
        "script_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "scope": "Finite exact arithmetic and a finite free-star-polynomial identity; no RH",
        "coverage": {"APP_cells": 81, "Q_cells": 16, "perimeter_cells": 12,
                     "multiaffine_laws": len(basis)+len(combinations),
                     "fibre_F10_cells": len(fibre), "seam_phases": 9,
                     "rational_matrix_cases": len(cases)},
        "observations": {"corona_histogram": dict(Counter(table[p] for p in perimeter)),
                         "radical_histogram": dict(Counter(table[p] for p in cross)),
                         "signature": "".join(map(str, signature)),
                         "Psi": "".join(map(str, psi)),
                         "vacancy_parameters": [point[2] for point in vacancies]},
        "declared_input": {"regional_emission_U": list(emission),
                          "U_role": "input of the two finite readers, not regenerated from seeds"},
        "rules_source": ["Articulo I REV02, sections/centro_electronico_registros.tex",
                         "Articulo I REV02, sections/extension.tex, eq:psi-catalogo and eq:acoplamiento"],
        "not_certified": ["generation of the full TPK state", "regional U producer from seeds",
                          "identification of different occurrences of 72",
                          "Weil positivity or RH", "physical identification of the electron"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    try:
        report = run()
        exit_code = 0
    except Exception as error:
        report = {"status": "FAIL_CENTRO_BORDE_VACANCIAS_ALGEBRA_FINITA",
                  "optimization_level": sys.flags.optimize,
                  "error": type(error).__name__ + ": " + str(error)}
        exit_code = 1
    serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(serialized, encoding="utf-8")
    print(serialized, end="")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
