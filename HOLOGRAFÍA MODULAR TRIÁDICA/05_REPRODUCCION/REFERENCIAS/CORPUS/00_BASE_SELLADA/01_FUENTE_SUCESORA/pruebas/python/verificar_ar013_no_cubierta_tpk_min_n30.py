#!/usr/bin/env python3
"""AR-013 autocontenido: obstruccion TPK-min -> N30.

El verificador codifica localmente las dos dinamicas finitas que compara. No
lee fuentes historicas, no usa constantes metrologicas y no presupone una
transicion ejecutable de TPK-full. Certifica:

* 104976 = 54 * 1944;
* el retorno de 54 ticks de los dos cursores de TPK-min es la identidad;
* cada estado de N30 posee cuatro sucesores distintos y ninguna autoarista;
* una proyeccion regular explicita F0 tiene fibras de tamano 54;
* F0 falla la semiconjugacion exactamente en 29160 semillas, y el unico
  componente que falla es la hoja.

El alcance es un no-go para una cubierta dirigida del N30 completo por el
motor determinista TPK-min vigente. No es un no-go para una futura
transicion enriquecida de TPK-full.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "certificados/AR-013_NO_CUBIERTA_TPK_MIN_N30.json"

DIRS = ("N", "E", "S", "O")
DIR_VECS = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "O": (0, -1),
}
DIR_INDEX = {name: index for index, name in enumerate(DIRS)}
INDEX_DIR = {index: name for name, index in DIR_INDEX.items()}
OPPOSITE = {"N": "S", "S": "N", "E": "O", "O": "E"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"AR-013 FAIL: {message}")


def one_cursor_seeds():
    return product(range(9), range(9), DIRS)


def seed_pairs():
    return product(range(9), range(9), DIRS, range(9), range(9), DIRS)


def mov3_sign(tick: int) -> int:
    residue = ((tick - 1) % 9) + 1
    if residue in (1, 4, 7):
        return 1
    if residue in (2, 5, 8):
        return -1
    return 0


def advance(position: tuple[int, int], direction: str) -> tuple[int, int]:
    di, dj = DIR_VECS[direction]
    return ((position[0] + di) % 9, (position[1] + dj) % 9)


def return54_one_cursor(
    seed: tuple[int, int, str], channel_sign: int
) -> tuple[int, int, str]:
    i, j, direction = seed
    for tick in range(1, 55):
        if mov3_sign(tick) == channel_sign:
            i, j = advance((i, j), direction)
        if tick in (27, 54):
            direction = OPPOSITE[direction]
    return (i, j, direction)


def n30_trit(mode: int, i: int, j: int) -> int:
    r = i % 3
    s = j % 3
    if mode == 0:
        return (r + s + 2) % 3
    return ((r + 1) * (s + 1)) % 3


def n30_next_mode(mode: int, trit: int) -> int:
    if trit == 1:
        return 0
    if trit == 2:
        return 1
    return mode


def n30_successor(
    state: tuple[int, int, int, int, int], next_direction: int
) -> tuple[int, int, int, int, int]:
    i, j, mode, _last_direction, tau = state
    direction = INDEX_DIR[next_direction]
    i2, j2 = advance((i, j), direction)
    trit = n30_trit(mode, i2, j2)
    return (
        i2,
        j2,
        n30_next_mode(mode, trit),
        next_direction,
        (tau + 1) % 3,
    )


def f0(source: tuple[int, int, str, int, int, str]):
    """Proyeccion cardinal regular: el segundo cursor queda en la fibra."""
    plus_i, plus_j, plus_direction, times_i, times_j, times_direction = source
    mode = 0 if times_direction in ("N", "S") else 1
    heading_i, heading_j = DIR_VECS[times_direction]
    tau = (heading_i * times_i + heading_j * times_j) % 3
    return (
        plus_i,
        plus_j,
        mode,
        DIR_INDEX[plus_direction],
        tau,
    )


def paired_step(source: tuple[int, int, str, int, int, str]):
    """Paso pareado favorable: cada cursor avanza una celda."""
    plus_i, plus_j, plus_direction, times_i, times_j, times_direction = source
    plus_i2, plus_j2 = advance((plus_i, plus_j), plus_direction)
    times_i2, times_j2 = advance((times_i, times_j), times_direction)
    return (
        plus_i2,
        plus_j2,
        plus_direction,
        times_i2,
        times_j2,
        times_direction,
    )


def main() -> None:
    source_count = (9 * 9 * 4) ** 2
    target_count = 9 * 9 * 2 * 4 * 3
    require(source_count == 104_976, "cardinal del espacio TPK-min")
    require(target_count == 1_944, "cardinal del espacio N30")
    require(source_count == 54 * target_count, "razon cardinal 54")

    cursor_seeds = list(one_cursor_seeds())
    require(len(cursor_seeds) == 324, "censo de un cursor")
    require(
        all(return54_one_cursor(seed, 1) == seed for seed in cursor_seeds),
        "el cursor aditivo no retorna en 54 ticks",
    )
    require(
        all(return54_one_cursor(seed, -1) == seed for seed in cursor_seeds),
        "el cursor multiplicativo no retorna en 54 ticks",
    )

    states = list(product(range(9), range(9), range(2), range(4), range(3)))
    require(len(states) == target_count, "enumeracion N30")
    outdegree_histogram: Counter[int] = Counter()
    self_loops = 0
    for state in states:
        successors = {n30_successor(state, direction) for direction in range(4)}
        outdegree_histogram[len(successors)] += 1
        self_loops += sum(
            n30_successor(state, direction) == state for direction in range(4)
        )
    require(
        outdegree_histogram == Counter({4: 1_944}),
        "N30 no tiene cuatro sucesores distintos por estado",
    )
    require(self_loops == 0, "N30 contiene una autoarista")

    fibre_counts: Counter[tuple[int, int, int, int, int]] = Counter()
    mismatch_components: Counter[tuple[str, ...]] = Counter()
    semiconjugacy_successes = 0
    first_failure = None
    for source in seed_pairs():
        image = f0(source)
        fibre_counts[image] += 1
        left = f0(paired_step(source))
        right = n30_successor(image, image[3])
        differing = tuple(
            name
            for name, lhs, rhs in zip(
                ("i", "j", "mode", "dlast", "tau"), left, right
            )
            if lhs != rhs
        )
        mismatch_components[differing] += 1
        if not differing:
            semiconjugacy_successes += 1
        elif first_failure is None:
            first_failure = {
                "source": list(source),
                "F0_after_source_step": list(left),
                "N30_after_F0": list(right),
                "differing_components": list(differing),
            }

    require(len(fibre_counts) == target_count, "F0 no es sobreyectiva")
    require(set(fibre_counts.values()) == {54}, "F0 no tiene grado regular 54")
    require(
        semiconjugacy_successes == 75_816,
        "censo inesperado de exitos de semiconjugacion",
    )
    require(
        mismatch_components == Counter({(): 75_816, ("mode",): 29_160}),
        "el defecto de F0 no esta aislado en la hoja",
    )

    witness = (1, 0, "N", 0, 0, "N")
    witness_left = f0(paired_step(witness))
    witness_right = n30_successor(f0(witness), f0(witness)[3])
    require(witness_left == (0, 0, 0, 0, 1), "imagen izquierda del testigo")
    require(witness_right == (0, 0, 1, 0, 1), "imagen derecha del testigo")

    report = {
        "status": "PASS_NO_DYNAMIC_COVER_CURRENT_TYPES",
        "self_contained": True,
        "uses_physical_target": False,
        "source_seed_count": source_count,
        "target_state_count": target_count,
        "cardinal_ratio": 54,
        "tpk_min_return_54": "identity_on_all_104976_seed_pairs",
        "n30_outdegree_histogram": {
            str(key): value for key, value in sorted(outdegree_histogram.items())
        },
        "n30_self_loops": self_loops,
        "F0_fibre_size": 54,
        "F0_semiconjugacy_successes": semiconjugacy_successes,
        "F0_semiconjugacy_failures": source_count - semiconjugacy_successes,
        "F0_failure_components": {
            "mode_only": mismatch_components[("mode",)]
        },
        "first_failure": first_failure,
        "explicit_witness": {
            "source": list(witness),
            "F0_after_source_step": list(witness_left),
            "N30_after_F0": list(witness_right),
        },
        "proof_obstruction": {
            "directed_cover": (
                "A deterministic source has outdegree one, whereas every N30 "
                "state has four distinct successors; a directed covering "
                "cannot preserve local outgoing stars."
            ),
            "return_semiconjugacy": (
                "The canonical 54-tick source return is the identity, while "
                "N30 has no self-loops; a surjective semiconjugacy to an N30 "
                "edge selection is therefore impossible."
            ),
        },
        "scope": (
            "No directed covering of full four-branch N30 by the current "
            "deterministic TPK-min graph. This does not constrain a future "
            "executable enriched TPK-full transition."
        ),
    }
    OUTPUT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    print("PASS_AR013_NO_DYNAMIC_COVER_CURRENT_TYPES")


if __name__ == "__main__":
    main()
