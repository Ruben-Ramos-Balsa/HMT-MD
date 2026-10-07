#!/usr/bin/env python3
"""Verifica la elevación residual W12→W24 y su alineamiento con la fibra de pi.

El programa separa dos capas. Recalcula exhaustivamente el diseño W12
obtenido del código ternario y las cinco regiones decimales de la palabra
010211. Para W24 verifica las identidades paramétricas del teorema residual:
el espectro de intersección dodecada--octada, los valores lambda_4=4,5 y la
consecuencia forzada 4+1. La existencia de W24=S(5,8,24) y el espectro de
pesos del Golay binario extendido son las hipótesis clásicas declaradas.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "datos/TPK_U_catalog_468.json"
OUTPUT = ROOT / "certificados/w12_w24_elevacion.json"

AW = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 2, 2, 1),
    (1, 1, 0, 1, 2, 2),
    (1, 2, 1, 0, 1, 2),
    (1, 2, 2, 1, 0, 1),
    (1, 1, 2, 2, 1, 0),
)

PI_WORD = "010211"
B_K = frozenset((4, 6, 9, 10))
STAR_PAIRS = (
    frozenset((1, 3)),
    frozenset((2, 11)),
    frozenset((5, 7)),
    frozenset((8, 12)),
)
NEGATIVE_PAIR = frozenset((5, 7))

EXPECTED_PI = {
    "501|614|498|169|272|272": (432, (5, 5, 5, 5, 5, 5)),
    "810|923|870|169|272|272": (144, (3, 3, 9, 5, 5, 5)),
    "810|983|810|169|272|272": (144, (3, 9, 3, 5, 5, 5)),
    "870|923|810|169|272|272": (144, (9, 3, 3, 5, 5, 5)),
    "870|923|810|418|674|521": (144, (9, 3, 3, 7, 1, 7)),
}

POSITIVE_U6_ORDER = (
    "810|923|870|169|272|272",
    "810|983|810|169|272|272",
    "870|923|810|169|272|272",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"W12_W24 FAIL: {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def steiner_lambda(v: int, k: int, t: int, s: int) -> int:
    numerator = comb(v - s, t - s)
    denominator = comb(k - s, t - s)
    require(numerator % denominator == 0, "parámetro de Steiner no integral")
    return numerator // denominator


def codeword(q: tuple[int, ...]) -> tuple[int, ...]:
    right = tuple(
        sum(q[i] * AW[i][j] for i in range(6)) % 3 for j in range(6)
    )
    return q + right


def ternary_witt_design() -> set[frozenset[int]]:
    supports: set[frozenset[int]] = set()
    weight_enumerator: dict[int, int] = {}
    for q in itertools.product(range(3), repeat=6):
        word = codeword(q)
        support = frozenset(i + 1 for i, value in enumerate(word) if value)
        weight_enumerator[len(support)] = weight_enumerator.get(len(support), 0) + 1
        if len(support) == 6:
            supports.add(support)
    require(
        weight_enumerator == {0: 1, 6: 264, 9: 440, 12: 24},
        "enumerador ternario",
    )
    require(len(supports) == 132, "número de hexadas")
    for five_set in itertools.combinations(range(1, 13), 5):
        face = frozenset(five_set)
        require(
            sum(face <= hexad for hexad in supports) == 1,
            "W12 no satisface S(5,6,12)",
        )
    return supports


def multiplicative_signature(serialized: str) -> tuple[int, ...]:
    signature: list[int] = []
    for raw in serialized.split("|"):
        value = int(raw)
        first = value // 100
        second = value // 10 % 10
        signature.append((second - first) % 10)
    return tuple(signature)


def projected_word(serialized: str) -> str:
    return "".join(str((-int(value)) % 3) for value in serialized.split("|"))


def read_pi_regions() -> list[dict[str, object]]:
    rows = json.loads(CATALOG.read_text(encoding="utf-8"))
    require(len(rows) == 468, "el catálogo no contiene 468 filas")
    require(sum(int(row["count"]) for row in rows) == 104_976, "censo total")
    pi_rows = [row for row in rows if projected_word(row["U6"]) == PI_WORD]
    require(len(pi_rows) == 5, "la microfibra de pi no contiene cinco regiones")

    observed = {
        row["U6"]: (int(row["count"]), multiplicative_signature(row["U6"]))
        for row in pi_rows
    }
    require(observed == EXPECTED_PI, "las cinco regiones de pi no son las publicadas")

    maximum_multiplicity = max(int(row["count"]) for row in pi_rows)

    def role_of(row: dict[str, object]) -> str:
        signature = multiplicative_signature(str(row["U6"]))
        if row["hplus_type"] == "ES":
            return "positive"
        if (
            row["hplus_type"] == "NO"
            and int(row["count"]) == maximum_multiplicity
            and len(set(signature)) == 1
        ):
            return "transversal"
        require(row["hplus_type"] == "NO", "tipo de orientación regional")
        return "negative"

    role_rows = [(role_of(row), row) for row in pi_rows]
    require(
        [role for role, _ in role_rows].count("transversal") == 1,
        "región transversal derivada",
    )
    require(
        [role for role, _ in role_rows].count("positive") == 3,
        "regiones positivas derivadas",
    )
    require(
        [role for role, _ in role_rows].count("negative") == 1,
        "región negativa derivada",
    )

    positive_rank = {u6: index for index, u6 in enumerate(POSITIVE_U6_ORDER)}
    role_rank = {"transversal": 0, "positive": 1, "negative": 2}
    role_rows.sort(
        key=lambda item: (
            role_rank[item[0]],
            positive_rank.get(str(item[1]["U6"]), 0),
        )
    )

    result: list[dict[str, object]] = []
    for role, row in role_rows:
        u6 = str(row["U6"])
        count = int(row["count"])
        signature = multiplicative_signature(u6)
        values = [int(item) for item in u6.split("|")]
        result.append(
            {
                "multiplicity": count,
                "U6": u6,
                "multiplicative_signature": list(signature),
                "return_block": values[3:],
                "heading_type": row["hplus_type"],
                "incidence_role": role,
            }
        )
    require(sum(item["multiplicity"] for item in result) == 1008, "fibra de pi")
    return result


def audit() -> dict[str, object]:
    hexads = ternary_witt_design()

    lambda4_w12 = steiner_lambda(12, 6, 5, 4)
    lambda4_w24 = steiner_lambda(24, 8, 5, 4)
    require(lambda4_w12 == 4 and lambda4_w24 == 5, "valores lambda_4")
    for four_set in itertools.combinations(range(1, 13), 4):
        face = frozenset(four_set)
        require(
            sum(face <= hexad for hexad in hexads) == lambda4_w12,
            "incidencia de una 4-cara en W12",
        )

    intersection_sizes = [
        j
        for j in range(9)
        if 20 - 2 * j in {0, 8, 12, 16, 24}
    ]
    require(intersection_sizes == [2, 4, 6], "espectro dodecada--octada")
    require(lambda4_w24 - lambda4_w12 == 1, "residuo transversal")

    incident_hexads = [hexad for hexad in hexads if B_K <= hexad]
    require(len(incident_hexads) == 4, "estrella de B_K")
    observed_pairs = {hexad - B_K for hexad in incident_hexads}
    require(observed_pairs == set(STAR_PAIRS), "pares de la estrella HMT")
    h_alpha = B_K | NEGATIVE_PAIR
    require(h_alpha in hexads, "H_alpha no es hexada")

    regions = read_pi_regions()
    positive_pairs = ((1, 3), (2, 11), (8, 12))
    mapping: list[dict[str, object]] = []
    positive_index = 0
    for region in regions:
        role = region["incidence_role"]
        if role == "transversal":
            target = "unique octad O_perp with O_perp intersection D = ell(B_K)"
            residual_pair: list[int] | None = None
        elif role == "negative":
            target = "unique lift of ell(H_alpha_minus)"
            residual_pair = [5, 7]
        else:
            residual_pair = list(positive_pairs[positive_index])
            positive_index += 1
            target = "unique lift of ell(B_K union residual_pair)"
        mapping.append(
            {
                "U6": region["U6"],
                "role": role,
                "residual_pair_1based": residual_pair,
                "target": target,
            }
        )

    return {
        "schema": "HMT.exceptional.W12_W24.residual-lift.v1",
        "status": "PASS",
        "classical_input": {
            "binary_code": "extended binary Golay code G24",
            "weight_spectrum": [0, 8, 12, 16, 24],
            "octad_design": "S(5,8,24)",
            "chosen_dodecad": "support D of a weight-12 codeword",
        },
        "residual_theorem": {
            "definition": "H(D)={O intersection D: O octad, |O intersection D|=6}",
            "octad_dodecad_intersection_sizes": intersection_sizes,
            "design": "H(D)=S(5,6,12)",
            "number_of_hexads": len(hexads),
            "unique_octad_lift_for_every_hexad": True,
        },
        "steiner_parameters": {
            "lambda4_W12": lambda4_w12,
            "lambda4_W24": lambda4_w24,
            "four_plus_one": {
                "residual_octads": lambda4_w12,
                "transversal_octads": lambda4_w24 - lambda4_w12,
                "residual_intersection_size": 6,
                "transversal_intersection_size": 4,
            },
        },
        "HMT_alignment_type": {
            "data": [
                "a dodecad D",
                "an incidence isomorphism ell: [12]_HMT -> D",
                "an ordering of the three positive regions",
            ],
            "selected_face_B_K_1based": sorted(B_K),
            "star_pairs_1based": [sorted(pair) for pair in STAR_PAIRS],
            "negative_hexad_H_alpha_1based": sorted(h_alpha),
            "invariant_partition": "1_transversal + 3_positive + 1_negative",
            "positive_order_scope": "calibration; the unordered positive triple is invariant",
            "regional_role_rule": {
                "positive": "hplus_type == ES",
                "transversal": (
                    "hplus_type == NO, maximum multiplicity in the fibre, "
                    "and constant multiplicative signature"
                ),
                "negative": "the remaining hplus_type == NO row",
                "label_scope": (
                    "the partition is derived from catalogue columns; the sign names "
                    "and the ordering of the positive triple are alignment conventions"
                ),
            },
        },
        "pi_microfibre": {
            "word": PI_WORD,
            "catalog_sha256": sha256(CATALOG),
            "regions": regions,
            "total_multiplicity": sum(item["multiplicity"] for item in regions),
            "role_alignment": mapping,
        },
        "branch_separation": {
            "binary": "G24 with D and ell: W12 -> W24",
            "ternary": "C_W -> N(A2^12) -> index-3 neighbor -> Leech",
            "W24_to_Leech_asserted": False,
        },
    }


def main() -> None:
    result = audit()
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("PASS_W12_W24_ELEVACION")


if __name__ == "__main__":
    main()
