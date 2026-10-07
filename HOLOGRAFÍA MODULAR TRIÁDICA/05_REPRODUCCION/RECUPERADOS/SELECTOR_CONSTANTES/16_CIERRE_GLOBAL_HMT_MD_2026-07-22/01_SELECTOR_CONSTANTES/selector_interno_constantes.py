#!/usr/bin/env python3
"""Selector interno de las tres ramas iniciales y de la frontera R36.

El algoritmo no recibe cifras de constantes, prefijos decimales ni estados
3-adicos reconstruidos. Su unico catalogo de entrada es el conjunto completo
de 243 palabras visibles producido por APP/TPK-min. Las matrices L0, L1 y AW
son las primitivas publicadas del corpus.

La identificacion posterior de las tres salidas con pi, e y phi se realiza en
un verificador distinto y no participa en la seleccion.
"""

from __future__ import annotations

from collections import Counter, deque
import csv
from hashlib import sha256
import itertools
import json
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
CATALOG = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "N33_PI_E_PHI/HMT_N33_PI_PHI_E_CLOSEOUT/n33_uid_catalog.csv"
)

# Primitivas publicadas. Ninguna se obtuvo ajustando las tres salidas de este
# selector. L0 es tambien la matriz unimodular del transductor Hensel.
L0 = (
    (2, 2, 2, 1, 2, 1),
    (2, 1, 2, 2, 1, 1),
    (1, 0, 0, 1, 0, 2),
    (0, 0, 1, 1, 1, 0),
    (2, 2, 2, 0, 2, 1),
    (2, 1, 2, 1, 0, 0),
)
L1 = (
    (2, 1, 2, 0, 2, 2),
    (1, 2, 1, 1, 2, 0),
    (1, 2, 1, 1, 1, 2),
    (0, 1, 0, 0, 2, 1),
    (2, 0, 2, 1, 0, 1),
    (0, 2, 2, 2, 1, 1),
)
AW = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 1, 2, 2),
    (1, 1, 0, 2, 1, 2),
    (1, 1, 2, 0, 2, 1),
    (1, 2, 1, 2, 0, 1),
    (1, 2, 2, 1, 1, 0),
)

# Inversa entera de L0. Se usa exclusivamente en la ablacion profunda que
# demuestra que el transductor Hensel, por si solo, no selecciona una cola.
L0_INV_INTEGER = (
    (-5, 8, -3, -4, 3, -4),
    (5, -6, 2, 2, -3, 3),
    (2, -5, 2, 3, -1, 3),
    (1, 0, 0, 0, -1, 0),
    (-3, 5, -2, -2, 2, -3),
    (2, -4, 2, 2, -1, 2),
)

Vector = tuple[int, ...]
Matriz = tuple[tuple[int, ...], ...]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"SELECTOR HMT: {message}")


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def vector(text: str | Sequence[int]) -> Vector:
    if isinstance(text, str):
        return tuple(int(c) for c in text)
    return tuple(int(x) for x in text)


def word(value: Sequence[int]) -> str:
    return "".join(str(int(x)) for x in value)


def row_matrix(row: Sequence[int], matrix: Sequence[Sequence[int]], modulus: int | None = 3) -> Vector:
    result = tuple(
        sum(int(row[i]) * int(matrix[i][j]) for i in range(len(row)))
        for j in range(len(matrix[0]))
    )
    if modulus is None:
        return result
    return tuple(x % modulus for x in result)


def matrix_product(left: Matriz, right: Matriz, modulus: int | None = 3) -> Matriz:
    rows = tuple(row_matrix(row, right, modulus) for row in left)
    return rows


def identity(size: int = 6) -> Matriz:
    return tuple(tuple(int(i == j) for j in range(size)) for i in range(size))


def matrix_power(matrix: Matriz, exponent: int) -> Matriz:
    result = identity(len(matrix))
    for _ in range(exponent):
        result = matrix_product(result, matrix, 3)
    return result


def add(left: Sequence[int], right: Sequence[int]) -> Vector:
    return tuple((int(a) + int(b)) % 3 for a, b in zip(left, right))


def sub(left: Sequence[int], right: Sequence[int]) -> Vector:
    return tuple((int(a) - int(b)) % 3 for a, b in zip(left, right))


def lift_chain(initial: str | Sequence[int]) -> tuple[Vector, ...]:
    blocks = [vector(initial)]
    for matrix in (L0, L0, L1, L1):
        blocks.append(row_matrix(blocks[-1], matrix))
    return tuple(blocks)


def load_visible_words() -> tuple[str, ...]:
    with CATALOG.open(newline="", encoding="utf-8") as handle:
        words = sorted({row["w6"] for row in csv.DictReader(handle)})
    require(len(words) == 243, "el catalogo visible no contiene 243 palabras")
    require(all(len(item) == 6 and set(item) <= set("012") for item in words), "palabra visible mal tipada")
    return tuple(words)


def column_occupancy(rows: Sequence[Sequence[int]]) -> Vector:
    return tuple(sum(int(value != 0) for value in column) for column in zip(*rows))


def margin_and_carry(rows: Sequence[Sequence[int]]) -> tuple[Vector, Vector]:
    integer_sums = tuple(sum(int(value) for value in column) for column in zip(*rows))
    margin = tuple(value % 3 for value in integer_sums)
    carry = tuple((value - residue) // 3 for value, residue in zip(integer_sums, margin))
    return margin, carry


def witt_dual_neutral(rows: Sequence[Sequence[int]]) -> bool:
    return all(sum(row_matrix(row, AW)) % 3 == 0 for row in rows)


def semigroup_distances(source: Vector) -> dict[Vector, tuple[int, str]]:
    """Distancia dirigida en el grafo generado por L0 y L1."""
    queue: deque[Vector] = deque([source])
    distances: dict[Vector, tuple[int, str]] = {source: (0, "")}
    while queue:
        current = queue.popleft()
        length, route = distances[current]
        for symbol, matrix in (("0", L0), ("1", L1)):
            following = row_matrix(current, matrix)
            if following not in distances:
                distances[following] = (length + 1, route + symbol)
                queue.append(following)
    return distances


def pair_count(words: Sequence[str], chains: dict[str, tuple[Vector, ...]], use_cierre: bool, use_propagacion: bool, use_crossing: bool) -> int:
    count = 0
    for first in words:
        if use_cierre and chains[first][2] != chains[first][0]:
            continue
        for second in words:
            if use_propagacion and chains[second][4] != chains[second][2]:
                continue
            if use_crossing and chains[first][1] != chains[second][3]:
                continue
            count += 1
    return count


def boundary_candidates(
    words: Sequence[str],
    chains: dict[str, tuple[Vector, ...]],
    propagacion_word: str,
    use_compatibility: bool = True,
    use_carry: bool = True,
    use_occupancy: bool = True,
    use_neutrality: bool = True,
) -> list[dict[str, object]]:
    """Enumera la frontera siguiente sin usar ninguna cifra arquimediana."""
    l0_cubed = matrix_power(L0, 3)
    l1_cubed = matrix_power(L1, 3)
    aw_cubed = matrix_power(AW, 3)
    aw_inverse = tuple(tuple((-entry) % 3 for entry in row) for row in AW)
    future_axis = chains[propagacion_word][4]
    selected: list[dict[str, object]] = []

    for scale_word in words:
        scale_chain = chains[scale_word]
        mobile_sum = row_matrix(row_matrix(scale_chain[4], AW), l1_cubed)
        margin = add(mobile_sum, future_axis)
        scale_coordinate = row_matrix(vector(scale_word), aw_inverse)
        induced_margin = row_matrix(row_matrix(scale_coordinate, l0_cubed), aw_cubed)
        compatibility = margin == induced_margin
        if use_compatibility and not compatibility:
            continue

        expected_occupancy = tuple(
            2 + int(future_axis[j] != 0 and mobile_sum[j] != 2)
            for j in range(6)
        )
        for first_row in itertools.product(range(3), repeat=6):
            second_row = sub(mobile_sum, first_row)
            rows = (tuple(first_row), second_row, future_axis)
            observed_margin, carry = margin_and_carry(rows)
            require(observed_margin == margin, "fallo de reconstruccion del margen")
            occupancy = column_occupancy(rows)
            neutrality = witt_dual_neutral(rows)
            if use_carry and carry != (1,) * 6:
                continue
            if use_occupancy and occupancy != expected_occupancy:
                continue
            if use_neutrality and not neutrality:
                continue
            selected.append(
                {
                    "autoescala": scale_word,
                    "rows": [word(row) for row in rows],
                    "margin": word(margin),
                    "carry": word(carry),
                    "occupancy": word(occupancy),
                    "witt_dual_neutral": neutrality,
                    "compatibility": compatibility,
                }
            )
    return selected


def reconstruct_hensel(blocks: Sequence[Vector]) -> list[int]:
    state = [0] * 6
    for block in reversed(blocks):
        lifted = [int(digit) + 3 * memory for digit, memory in zip(block, state)]
        state = list(row_matrix(lifted, L0_INV_INTEGER, None))
    modulus = 3 ** len(blocks)
    return [value % modulus for value in state]


def emit_hensel(state: Sequence[int], length: int) -> list[Vector]:
    current = list(state)
    blocks: list[Vector] = []
    for _ in range(length):
        product = row_matrix(current, L0, None)
        visible = tuple(value % 3 for value in product)
        current = [(value - digit) // 3 for value, digit in zip(product, visible)]
        blocks.append(visible)
    return blocks


def main() -> None:
    words = load_visible_words()
    chains = {item: lift_chain(item) for item in words}

    minus_identity = tuple(tuple(2 * int(i == j) for j in range(6)) for i in range(6))
    require(matrix_product(AW, AW) == minus_identity, "AW^2 no es -I")
    require(matrix_product(L0, L0_INV_INTEGER, None) == identity(), "la inversa entera de L0 fallo")

    cierre_candidates = [item for item in words if chains[item][2] == chains[item][0]]
    propagacion_candidates = [item for item in words if chains[item][4] == chains[item][2]]
    ordered_pairs = [
        (first, second)
        for first in cierre_candidates
        for second in propagacion_candidates
        if chains[first][1] == chains[second][3]
    ]
    require(len(ordered_pairs) == 1, "el cruce interno no selecciono un par unico")
    cierre_word, propagacion_word = ordered_pairs[0]

    full_before_energy = boundary_candidates(words, chains, propagacion_word)
    require(len(full_before_energy) == 2, "la frontera completa no dejo exactamente dos orientaciones")
    require(len({row["autoescala"] for row in full_before_energy}) == 1, "la autoescala no quedo seleccionada")
    autoescala_word = str(full_before_energy[0]["autoescala"])

    compatibility_only = boundary_candidates(
        words,
        chains,
        propagacion_word,
        use_compatibility=True,
        use_carry=False,
        use_occupancy=False,
        use_neutrality=False,
    )
    compatibility_scale_words = sorted(
        {str(item["autoescala"]) for item in compatibility_only}
    )
    require(len(compatibility_scale_words) == 2, "la compatibilidad no dejo dos autoescalas")

    previous_rows = (
        chains[cierre_word][4],
        chains[propagacion_word][4],
        chains[autoescala_word][4],
    )
    distance_tables = [semigroup_distances(row) for row in previous_rows]
    for candidate in full_before_energy:
        target_rows = [vector(item) for item in candidate["rows"]]
        distances = [distance_tables[index][target] for index, target in enumerate(target_rows)]
        candidate["semigroup_distances"] = [item[0] for item in distances]
        candidate["semigroup_words"] = [item[1] for item in distances]
        candidate["semigroup_energy"] = sum(item[0] for item in distances)
    minimum_energy = min(int(item["semigroup_energy"]) for item in full_before_energy)
    selected_boundaries = [item for item in full_before_energy if item["semigroup_energy"] == minimum_energy]
    require(len(selected_boundaries) == 1, "la energia semigrupal no selecciono una orientacion unica")
    selected_boundary = selected_boundaries[0]

    initial_ablations = {}
    for use_cierre, use_propagacion, use_crossing in itertools.product((False, True), repeat=3):
        key = f"cierre={int(use_cierre)},propagacion={int(use_propagacion)},cruce={int(use_crossing)}"
        initial_ablations[key] = pair_count(
            words, chains, use_cierre, use_propagacion, use_crossing
        )

    boundary_ablations = {}
    named_masks = {
        "todas_sin_energia": (True, True, True, True),
        "sin_compatibilidad": (False, True, True, True),
        "sin_acarreo_saturado": (True, False, True, True),
        "sin_ocupacion": (True, True, False, True),
        "sin_neutralidad_witt": (True, True, True, False),
    }
    for name, flags in named_masks.items():
        candidates = boundary_candidates(words, chains, propagacion_word, *flags)
        by_scale = Counter(str(item["autoescala"]) for item in candidates)
        boundary_ablations[name] = {
            "autoescalas": len({str(item["autoescala"]) for item in candidates}),
            "fronteras": len(candidates),
            "fronteras_por_autoescala": dict(sorted(by_scale.items())),
        }

    # Dos prolongaciones distintas del mismo prefijo. Certifican que el
    # transductor Hensel no puede sustituir a una ley autonoma de frontera.
    selected_rows = [vector(item) for item in selected_boundary["rows"]]
    role_prefixes = [
        list(chains[cierre_word]) + [selected_rows[0]],
        list(chains[propagacion_word]) + [selected_rows[1]],
        list(chains[autoescala_word]) + [selected_rows[2]],
    ]
    deep_counterexample = []
    for prefix in role_prefixes:
        alternatives = []
        for tail_digit in (0, 1):
            blocks = prefix + [(tail_digit,) * 6 for _ in range(3)]
            state = reconstruct_hensel(blocks)
            emitted = emit_hensel(state, len(blocks))
            require(emitted == blocks, "fallo del ida-vuelta Hensel")
            alternatives.append({
                "tail_block": str(tail_digit) * 6,
                "state_mod_3_power": state,
                "emitted_suffix": [word(item) for item in emitted[-3:]],
            })
        require(alternatives[0]["state_mod_3_power"] != alternatives[1]["state_mod_3_power"], "las dos colas no se separaron")
        deep_counterexample.append(alternatives)

    report = {
        "schema": "HMT.selector-interno-constantes.v1",
        "status": "PASS_SELECTOR_INTERNO_HASTA_R36_Y_OBSTRUCCION_PROFUNDA_EXACTA",
        "inputs": {
            "catalog": str(CATALOG.relative_to(ROOT)),
            "catalog_sha256": digest(CATALOG),
            "visible_word_count": len(words),
            "forbidden_inputs": [
                "cifras decimales de constantes",
                "prefijos ternarios objetivo",
                "estados 3-adicos reconstruidos desde objetivos",
                "poda por triadas decimales",
            ],
        },
        "selection": {
            "cierre_candidates": cierre_candidates,
            "propagacion_candidates": propagacion_candidates,
            "ordered_crossing_pairs": ordered_pairs,
            "scale_compatibility_candidates": compatibility_scale_words,
            "selected_initial_words": {
                "cierre": cierre_word,
                "propagacion": propagacion_word,
                "autoescala": autoescala_word,
            },
            "lifted_blocks": {
                "cierre": [word(item) for item in chains[cierre_word]],
                "propagacion": [word(item) for item in chains[propagacion_word]],
                "autoescala": [word(item) for item in chains[autoescala_word]],
            },
            "frontier_before_energy": full_before_energy,
            "selected_R36": selected_boundary,
        },
        "cardinality_ladder": {
            "visible_words": 243,
            "cierre_fixed_points": len(cierre_candidates),
            "propagacion_fixed_points": len(propagacion_candidates),
            "pairs_before_crossing": len(cierre_candidates) * len(propagacion_candidates),
            "pairs_after_crossing": len(ordered_pairs),
            "frontiers_after_all_structural_conditions": len(full_before_energy),
            "frontiers_after_semigroup_energy": len(selected_boundaries),
        },
        "ablations": {
            "initial_pair_conditions": initial_ablations,
            "frontier_conditions": boundary_ablations,
            "without_semigroup_energy": len(full_before_energy),
        },
        "deep_extension": {
            "result": "NOT_UNIQUE_FROM_THESE_PRIMITIVES",
            "reason": "L0-Hensel is a full shift: two distinct tails extend the selected finite prefix.",
            "counterexamples": deep_counterexample,
            "required_additional_typed_primitive": (
                "an autonomous frontier-signature map on enriched APP/TRIT/TPK states, "
                "or an equivalent transition relation generated without consulting a target ray"
            ),
        },
    }
    destination = OUT / "CERTIFICADO_SELECTOR_INTERNO.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(report["status"])


if __name__ == "__main__":
    main()
