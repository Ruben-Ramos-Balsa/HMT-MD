#!/usr/bin/env python3
"""Exact local controls for the article-X incidence maps.

This is NOT a terminal-register generator.  The displayed K is used solely
to test whether the specified downstream conditions distinguish registers.
The alternative vector is not asserted to be an admissible TPK history.

Independently of either vector, the script generates all 132 ternary-code
hexads from the source matrix, greedily selects 12 independent incidence
rows in lexicographic order, and gives their rational inverse and encoding
witnesses.  No K or channel data enter that basis selection.

Only the explicit --output destination is written.  The imported source
owner is executed under a non-main name, so its certificate writer is not
called.  All tests remain active under python -O.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from math import lcm
from pathlib import Path
import runpy


ROOT = Path("/Users/ruben/Documents/New project")
ARTICLE = ROOT / "output/EXTREMA_MEDIA_RAZON_NARRACION_Y_REVISION_20260916/ARTICULO/ES"
SOURCE = ARTICLE / "source/sections"
OWNER = ARTICLE / "supplement/vendor/variacional/controles_articulo_I/propietarios_k_moonshine/variacional.py"
AW = [
    [0, 1, 1, 1, 1, 1],
    [1, 0, 1, 2, 2, 1],
    [1, 1, 0, 1, 2, 2],
    [1, 2, 1, 0, 1, 2],
    [1, 2, 2, 1, 0, 1],
    [1, 1, 2, 2, 1, 0],
]
K = [234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601]
Z = [7, 297, 353, -430, -715, -1199, -3, 286, -894, -528, 380, 663]
DIRECTION = [0, -1, -1, 0, 0, 1, 1, 0, 0, 0, 0, 0]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def encode(word):
    return tuple(word) + tuple(sum(word[i] * AW[i][j] for i in range(6)) % 3 for j in range(6))


def support(word):
    return tuple(i for i, x in enumerate(encode(word)) if x)


def rref(matrix):
    a = [[F(x) for x in row] for row in matrix]
    pivots = []
    if not a:
        return a, pivots
    r = 0
    for c in range(len(a[0])):
        p = next((i for i in range(r, len(a)) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        q = a[r][c]
        a[r] = [x / q for x in a[r]]
        for i in range(len(a)):
            if i != r:
                q = a[i][c]
                a[i] = [x - q * y for x, y in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
        if r == len(a):
            break
    return a, pivots


def rank(matrix):
    return len(rref(matrix)[1])


def inverse(matrix):
    n = len(matrix)
    augmented = [list(row) + [int(i == j) for j in range(n)] for i, row in enumerate(matrix)]
    reduced, pivots = rref(augmented)
    require(pivots[:n] == list(range(n)), "noninvertible selected matrix")
    return [row[n:] for row in reduced]


def matmul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def matvec(a, v):
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def hadamard(v):
    h = [[1, 1, 1, 1], [1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]]
    out = [0] * 12
    for r in range(3):
        indices = [r + 3 * j for j in range(4)]
        for i in range(4):
            out[indices[i]] = sum(h[i][j] * v[indices[j]] for j in range(4))
    return out


def differences(v, p):
    return [v[i] - v[(i + p) % 12] for i in range(12)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    # Independent finite generation: neither K nor Z enters this block.
    witnesses = {}
    weight_census = {}
    for word in product(range(3), repeat=6):
        supp = support(word)
        weight_census[len(supp)] = weight_census.get(len(supp), 0) + 1
        if len(supp) == 6:
            witnesses.setdefault(supp, word)
    require(weight_census == {0: 1, 6: 264, 9: 440, 12: 24}, "source weight census")
    hexads = sorted(witnesses)
    require(len(hexads) == 132, "source hexad count")
    incidence = [[int(i in h) for i in range(12)] for h in hexads]
    gram = matmul(list(zip(*incidence)), incidence)
    require(gram == [[36 * int(i == j) + 30 for j in range(12)] for i in range(12)], "incidence Gram identity")
    full_recovery = [[F(11 * row[i] - 5, 396) for row in incidence] for i in range(12)]
    require(matmul(full_recovery, incidence) == [[int(i == j) for j in range(12)] for i in range(12)],
            "396 k_i = 11 sum_{H contains i} y_H - 5 sum_H y_H")

    selected = []
    rows = []
    for h, row in zip(hexads, incidence):
        if rank(rows + [row]) > len(rows):
            selected.append(h)
            rows.append(row)
        if len(rows) == 12:
            break
    require(len(rows) == 12, "twelve independent rows")
    inv = inverse(rows)
    identity = [[int(i == j) for j in range(12)] for i in range(12)]
    require(matmul(inv, rows) == identity, "left inverse")
    require(matmul(rows, inv) == identity, "right inverse")
    denominator = lcm(*(x.denominator for row in inv for x in row))
    inverse_integer = [[int(x * denominator) for x in row] for row in inv]

    # Local countermodel to the downstream constraints, NOT another generated history.
    delta = [36 * x for x in DIRECTION]
    other = [k + d for k, d in zip(K, delta)]
    other_z = [z - d for z, d in zip(Z, delta)]
    high = lambda v: {i for i, x in enumerate(v) if x >= 729}
    negative = lambda v: {i for i, x in enumerate(v) if x < 0}
    p_pi = set(support((0, 1, 0, 2, 1, 1)))
    h_e = set(support((2, 0, 1, 1, 0, 1)))
    h_phi = set(support((1, 2, 1, 2, 0, 0)))
    h_app = set(support((0, 2, 2, 0, 2, 0)))
    b = high(K)
    compatible = [set(h) for h in hexads if b <= set(h) <= p_pi and
                  (len(set(h) & h_e), len(set(h) & h_phi), len(set(h) & h_app)) == (4, 3, 2)]
    require(len(compatible) == 1, "unique selected hexad")
    h_alpha = compatible[0]
    origin = (h_e & h_phi) - (h_alpha | h_app)
    require(origin == {0}, "same marked origin")
    require(high(other) == b == h_e & p_pi, "same marked tetrad")
    require(negative(other_z) == negative(Z) == h_alpha, "same signed hexad with regional inputs fixed")
    require(sum(other) == sum(K) == 6263, "same uniform charge")
    require(all(0 <= x < 1000 for x in other), "legal three-digit blocks")
    require(len(set(other)) == 12, "exact twelve-block period")
    require(all((x - y) % 36 == 0 for x, y in zip(other, K)), "same residues mod 36")
    require(hadamard(hadamard(other)) == [4 * x for x in other], "same Hadamard integral image condition")

    owner = runpy.run_path(str(OWNER), run_name="hmt_incidence_control_read_only")
    p3 = owner["projector_three"]()
    qvector = lambda v: [(F(x), F(0)) for x in v]
    qmv = owner["matrix_vector"]
    require(qmv(p3, qvector(DIRECTION)) == [owner["ZERO"]] * 12, "source P3 kernel vector")
    require(qmv(p3, qvector(other)) == qmv(p3, qvector(K)), "same full projected vector, hence same P10")
    weighted_delta = matvec(incidence, delta)
    require(any(weighted_delta), "full weighted incidence distinguishes the two registers")
    first_weight_change = next(i for i, x in enumerate(weighted_delta) if x)
    kernel_matrix = [[entry[j] for entry in row] for j in range(2) for row in p3] + [[F(1)] * 12]
    require(rank(kernel_matrix) == 7, "five-dimensional rational kernel after fixing charge and P3")

    source_files = [SOURCE / name for name in (
        "registro_k.tex", "registro_imagen_integral.tex", "excepcional.tex",
        "incidencia_registro.tex", "incidencia_normalizacion.tex", "incidencia_bandera.tex",
        "incidencia_reticulo.tex", "k_direccion_dimensional.tex", "fibras_app_witt.tex")]
    report = {
        "status": "PASS_EXACT_LOCAL_INCIDENCE_CONTROL",
        "arithmetic": "Python standard-library Fraction; exact Q and Q(sqrt(5))",
        "scope": {
            "is_terminal_generator": False,
            "alternative_is_claimed_TPK_history": False,
            "same_marked_lattice": "Same source code, metric, positive chamber, marked origin and radial vector; therefore the exact defining lattice N_alpha is unchanged, without relabeling.",
            "same_octad_lift": "With the same binary code, dodecad and incidence chart, the same selected hexad has the same unique octad lift.",
            "not_preserved": ["the fixed canonical signed vector U", "the fixed canonical 90/120 channels", "the full weighted incidence I*K", "the value of kappa and the alpha positional readout"],
            "conclusion": "The enumerated downstream conditions do not alone determine twelve integer blocks. The basis/inverse is a separate recovery map from complete weighted incidence, not a producer of those weights.",
        },
        "sources": {str(path): sha256(path.read_bytes()).hexdigest() for path in source_files + [OWNER]},
        "source_locators": {
            "Hadamard_integral_isomorphism": "sections/registro_k.tex:353-373",
            "fixed_channels_unique_inverse": "sections/registro_imagen_integral.tex:24-96",
            "marked_hexad_selector": "sections/excepcional.tex:278-330",
            "incidence_matrix_and_Gram": "sections/excepcional.tex:337-376",
            "hexad_not_register_octad_injection": "sections/excepcional.tex:513-555",
            "fixed_marked_lattice_definition": "sections/excepcional.tex:653-691",
            "P3_and_P10": "sections/k_direccion_dimensional.tex:34-154",
        },
        "independent_incidence_basis": {
            "selection": "Greedy exact-rank increase over lexicographically ordered zero-based supports generated from AW; no K, U or channel data used.",
            "encoder_matrix": AW,
            "weight_census": weight_census,
            "hexad_count": len(hexads),
            "hexads_per_point": 66,
            "hexads_per_distinct_pair": 30,
            "gram_matrix": gram,
            "full_incidence_recovery": "396*k_i = 11*sum_{H contains i} y_H - 5*sum_H y_H; y=I*k",
            "full_incidence_left_inverse_verified": True,
            "selected_supports_zero_based": [list(h) for h in selected],
            "selected_supports_one_based": [[i + 1 for i in h] for h in selected],
            "word_witnesses": [list(witnesses[h]) for h in selected],
            "encoded_word_witnesses": [list(encode(witnesses[h])) for h in selected],
            "matrix": rows,
            "inverse_rational_strings": [[str(x) for x in row] for row in inv],
            "inverse_common_denominator": denominator,
            "inverse_integer_numerator": inverse_integer,
            "left_and_right_inverse_verified": True,
        },
        "local_control": {
            "displayed_K": K,
            "delta": delta,
            "alternative_K": other,
            "original_precarry": Z,
            "alternative_precarry_with_same_regions": other_z,
            "same_marked_tetrad_one_based": sorted(i + 1 for i in b),
            "same_marked_hexad_one_based": sorted(i + 1 for i in h_alpha),
            "same_marked_origin_one_based": sorted(i + 1 for i in origin),
            "same_full_P3_projection": True,
            "same_P10_projector": True,
            "rational_kernel_dimension_of_P3_and_charge": 5,
            "same_charge": sum(other),
            "alternative_U": hadamard(other),
            "delta_channel_90": differences(delta, 3),
            "delta_channel_120": differences(delta, 4),
            "number_changed_weighted_hexads": sum(x != 0 for x in weighted_delta),
            "first_changed_weighted_hexad_one_based": [i + 1 for i in hexads[first_weight_change]],
            "first_weight_change": weighted_delta[first_weight_change],
        },
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(report["status"])
    print("Independent incidence inverse common denominator:", denominator)
    print("Twelve hexad witnesses and inverse:", args.output)


if __name__ == "__main__":
    main()
