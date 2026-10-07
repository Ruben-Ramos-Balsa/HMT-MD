#!/usr/bin/env python3
"""Verificación independiente y determinista del núcleo rector HMT V2.

No usa CODATA ni cifras objetivo para construir K. Comprueba las identidades
finitas publicadas y escribe un certificado JSON junto al programa.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


K = (234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601)
U_EXPECTED = (2378, 1406, 2479, -452, 998, -551, -668, -204, -371, -322, -28, -997)
D3_EXPECTED = (-495, -116, -684, 108, 601, -90, -173, -88, 313, 560, -397, 461)
D4_EXPECTED = (-425, -281, -481, 671, -255, 30, 475, -543, 680, 251, 6, -128)
ALPHA_EXPECTED = (7, 297, 352, 569, 283, 800, 997, 285, 105, 472, 380, 663)
STATE_K9 = ("100100", "020112", "010122")
GATE9_OUTPUTS = (
    ("101222", "112221", "112002"),
    ("102221", "111222", "112002"),
    ("111221", "102222", "112002"),
)
STATE_K10 = GATE9_OUTPUTS[0]

PI_TRIADS = (141, 592, 653, 589, 793, 238, 462, 643, 383, 279, 502, 884)
E_TRIADS = (718, 281, 828, 459, 45, 235, 360, 287, 471, 352, 662, 497)
PHI_TRIADS = (618, 33, 988, 749, 894, 848, 204, 586, 834, 365, 638, 117)

H4 = (
    (1, 1, 1, 1),
    (1, 1, -1, -1),
    (1, -1, 1, -1),
    (1, -1, -1, 1),
)

C_PALEY = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 1, -1, -1),
    (1, 1, 0, -1, 1, -1),
    (1, 1, -1, 0, -1, 1),
    (1, -1, 1, -1, 0, 1),
    (1, -1, -1, 1, 1, 0),
)

P_ATLAS = (0, 1, 2, 4, 5, 3)
A_W_ATLAS = tuple(
    tuple(C_PALEY[P_ATLAS[i]][P_ATLAS[j]] % 3 for j in range(6))
    for i in range(6)
)


def dr9(value: int) -> int:
    return 1 + ((value - 1) % 9)


def mat_vec(matrix, vector):
    return tuple(sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix)


def mat_mul(a, b):
    bt = tuple(zip(*b))
    return tuple(tuple(sum(x * y for x, y in zip(row, col)) for col in bt) for row in a)


def transpose(matrix):
    return tuple(zip(*matrix))


def cyclic_difference(vector, step):
    n = len(vector)
    return tuple(vector[i] - vector[(i + step) % n] for i in range(n))


def difference_matrix(n, step):
    rows = []
    for i in range(n):
        row = [0] * n
        row[i] = 1
        row[(i + step) % n] -= 1
        rows.append(row)
    return rows


def rational_rank(rows):
    matrix = [[Fraction(value) for value in row] for row in rows]
    rank = 0
    column_count = len(matrix[0]) if matrix else 0
    for column in range(column_count):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for r in range(len(matrix)):
            if r != rank and matrix[r][column]:
                factor = matrix[r][column]
                matrix[r] = [x - factor * y for x, y in zip(matrix[r], matrix[rank])]
        rank += 1
    return rank


def alpha_carry():
    digits = [0] * 12
    carries = [0] * 13
    for m in range(11, -1, -1):
        value = PI_TRIADS[m] + E_TRIADS[m] - PHI_TRIADS[m] - K[m] + carries[m + 1]
        digits[m] = value % 1000
        carries[m] = (value - digits[m]) // 1000
    return tuple(digits), tuple(carries)


def trit_add(left: str, right: str) -> str:
    return "".join(str((int(a) + int(b)) % 3) for a, b in zip(left, right))


def golay_witt_certificate(a_w):
    weights = Counter()
    hexad_supports = set()
    for q in product(range(3), repeat=6):
        right = tuple(sum(q[i] * a_w[i][j] for i in range(6)) % 3 for j in range(6))
        word = q + right
        weight = sum(value != 0 for value in word)
        weights[weight] += 1
        if weight == 6:
            hexad_supports.add(tuple(i for i, value in enumerate(word) if value))

    lambda_values = {}
    for t in range(6):
        counts = Counter()
        for subset in combinations(range(12), t):
            counts[sum(set(subset).issubset(hexad) for hexad in hexad_supports)] += 1
        if len(counts) != 1:
            raise AssertionError(f"Las incidencias no son uniformes para t={t}: {counts}")
        lambda_values[t] = next(iter(counts))
    return dict(sorted(weights.items())), len(hexad_supports), lambda_values


def main():
    additive = tuple(tuple(dr9(i + j - 1) for j in range(1, 10)) for i in range(1, 10))
    multiplicative = tuple(tuple(dr9(i * j) for j in range(1, 10)) for i in range(1, 10))
    app = {
        "additive_total": sum(map(sum, additive)),
        "multiplicative_total": sum(map(sum, multiplicative)),
    }
    app["defect"] = app["multiplicative_total"] - app["additive_total"]
    assert app == {"additive_total": 405, "multiplicative_total": 459, "defect": 54}

    orbits = tuple(tuple(K[start + 3 * j] for j in range(4)) for start in range(3))
    blocks = tuple(mat_vec(H4, orbit) for orbit in orbits)
    u_signed = tuple(blocks[m % 3][m // 3] for m in range(12))
    assert u_signed == U_EXPECTED
    assert mat_mul(H4, H4) == tuple(tuple(4 if i == j else 0 for j in range(4)) for i in range(4))

    d3 = cyclic_difference(K, 3)
    d4 = cyclic_difference(K, 4)
    assert d3 == D3_EXPECTED
    assert d4 == D4_EXPECTED
    assert sum(K) == 6263

    rows_34 = difference_matrix(12, 3) + difference_matrix(12, 4)
    ranks = {
        "D3": rational_rank(difference_matrix(12, 3)),
        "D4": rational_rank(difference_matrix(12, 4)),
        "D3_D4": rational_rank(rows_34),
        "D3_D4_Q": rational_rank(rows_34 + [[1] * 12]),
    }
    assert ranks == {"D3": 9, "D4": 8, "D3_D4": 11, "D3_D4_Q": 12}

    alpha_digits, carries = alpha_carry()
    assert alpha_digits == ALPHA_EXPECTED

    paley_product = mat_mul(C_PALEY, transpose(C_PALEY))
    assert paley_product == tuple(tuple(5 if i == j else 0 for j in range(6)) for i in range(6))
    a_w = A_W_ATLAS
    weights, support_count, lambda_values = golay_witt_certificate(a_w)
    assert weights == {0: 1, 6: 264, 9: 440, 12: 24}
    assert support_count == 132
    assert lambda_values == {0: 132, 1: 66, 2: 30, 3: 12, 4: 4, 5: 1}

    hamming_243 = sum(__import__("math").comb(11, k) * 2**k for k in range(3))
    assert hamming_243 == 243
    assert 729 * 243 == 3**11
    assert 1000 == 729 + 243 + 27 + 1
    assert 196884 == 54 * (5 * 729 + 1)

    cube = {
        "ambient_F3_6": 3**6,
        "catalog_TPK": 468,
        "corona_HMT": 243 + 27 + 1,
        "topological_boundary": 9**3 - 7**3,
    }
    assert cube == {
        "ambient_F3_6": 729,
        "catalog_TPK": 468,
        "corona_HMT": 271,
        "topological_boundary": 386,
    }

    assert {output[2] for output in GATE9_OUTPUTS} == {"112002"}
    assert {trit_add(output[0], output[1]) for output in GATE9_OUTPUTS} == {"210110"}
    assert STATE_K10 != STATE_K9

    b_k = tuple(i + 1 for i, value in enumerate(K) if value >= 729)
    h_alpha_minus = tuple(i + 1 for i, value in enumerate(
        tuple(a + b - c - k for a, b, c, k in zip(PI_TRIADS, E_TRIADS, PHI_TRIADS, K))
    ) if value < 0)
    assert b_k == (4, 6, 9, 10)
    assert h_alpha_minus == (4, 5, 6, 7, 9, 10)

    result = {
        "schema": "HMT.nucleo_rector.v2",
        "status": "PASS",
        "app": app,
        "dodecaphase": {
            "K": K,
            "U12_signed": u_signed,
            "D3K": d3,
            "D4K": d4,
            "Q": sum(K),
            "ranks": ranks,
            "Pi_plus": tuple(max(value, 0) for value in u_signed),
            "Pi_minus": tuple(max(-value, 0) for value in u_signed),
        },
        "alpha": {
            "triads": alpha_digits,
            "decimal": "0." + "".join(f"{value:03d}" for value in alpha_digits),
            "carries_right_to_left": carries,
        },
        "paley_witt": {
            "CCt_diagonal": 5,
            "weight_enumerator": weights,
            "hexad_supports": support_count,
            "lambda": lambda_values,
        },
        "dimension_block": {
            "V3_11_2": hamming_243,
            "perfect_tiling": 729 * 243,
            "three_power_11": 3**11,
            "completion": [729, 243, 27, 1],
            "moonshine_identity": 196884,
        },
        "cube": cube,
        "g9_local": {
            "state_K9": STATE_K9,
            "gate_K9_to_K10_outputs": GATE9_OUTPUTS,
            "phi_fixed_on_outputs": GATE9_OUTPUTS[0][2],
            "pi_plus_e_fixed_on_outputs": trit_add(GATE9_OUTPUTS[0][0], GATE9_OUTPUTS[0][1]),
            "state_K10_selected": STATE_K10,
            "same_phase_new_state": True,
        },
        "witt_supports": {
            "B_K": b_k,
            "H_alpha_minus": h_alpha_minus,
            "H_alpha_plus": tuple(i for i in range(1, 13) if i not in h_alpha_minus),
        },
    }
    output = Path(__file__).with_name("verificacion_nucleo_rector.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
