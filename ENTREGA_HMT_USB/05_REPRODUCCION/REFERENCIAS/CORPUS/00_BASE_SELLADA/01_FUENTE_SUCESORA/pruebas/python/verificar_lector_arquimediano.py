#!/usr/bin/env python3
"""Audita la carta arquimediana finita condicionada a L0 y L1.

El programa certifica por separado dos hechos:

1. las propiedades exactas de la carta una vez fijadas las matrices;
2. el carácter calibrado de esas matrices: seis transiciones linealmente
   independientes determinan de manera única L0, y otras seis determinan L1.

El segundo hecho impide interpretar la auditoría como una derivación
independiente de L0 y L1 a partir de APP mínima.
"""

from __future__ import annotations

from collections import Counter
import csv
import itertools
import json
from pathlib import Path


P = 3
N = 6
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "certificados/lector_arquimediano_calibrado.json"
CATALOGUE = ROOT / "datos/catalogo_lector_arquimediano.csv"

L0 = [
    [2, 2, 2, 1, 2, 1],
    [2, 1, 2, 2, 1, 1],
    [1, 0, 0, 1, 0, 2],
    [0, 0, 1, 1, 1, 0],
    [2, 2, 2, 0, 2, 1],
    [2, 1, 2, 1, 0, 0],
]
L1 = [
    [2, 1, 2, 0, 2, 2],
    [1, 2, 1, 1, 2, 0],
    [1, 2, 1, 1, 1, 2],
    [0, 1, 0, 0, 2, 1],
    [2, 0, 2, 1, 0, 1],
    [0, 2, 2, 2, 1, 1],
]
TARGETS = {
    "pi": ("010211", (141, 592, 653, 589)),
    "e": ("201101", (718, 281, 828, 459)),
    "phi": ("121200", (618, 33, 988, 749)),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"LECTOR ARQUIMEDIANO FAIL: {message}")


def eye() -> list[list[int]]:
    return [[int(i == j) for j in range(N)] for i in range(N)]


def matmul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(N)) % P for j in range(N)]
        for i in range(len(a))
    ]


def row_mul(row: list[int], matrix: list[list[int]]) -> list[int]:
    return [sum(row[k] * matrix[k][j] for k in range(N)) % P for j in range(N)]


def rref(matrix: list[list[int]]) -> tuple[list[list[int]], int]:
    work = [[entry % P for entry in row] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, P)
        work[pivot_row] = [(inverse * value) % P for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    (left - factor * right) % P
                    for left, right in zip(work[row], work[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return work, pivot_row


def inverse(matrix: list[list[int]]) -> list[list[int]]:
    augmented = [row[:] + unit for row, unit in zip(matrix, eye())]
    reduced, rank = rref(augmented)
    require(rank == N, "matriz de vectores de calibración singular")
    require([row[:N] for row in reduced] == eye(), "inversa modular incorrecta")
    return [row[N:] for row in reduced]


def determinant_mod3(matrix: list[list[int]]) -> int:
    work = [[entry % P for entry in row] for row in matrix]
    determinant = 1
    for column in range(N):
        pivot = next(
            (row for row in range(column, N) if work[row][column]), None
        )
        require(pivot is not None, "matriz singular")
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = (-determinant) % P
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % P
        inv_pivot = pow(pivot_value, -1, P)
        work[column] = [(inv_pivot * value) % P for value in work[column]]
        for row in range(column + 1, N):
            factor = work[row][column]
            if factor:
                work[row] = [
                    (left - factor * right) % P
                    for left, right in zip(work[row], work[column])
                ]
    return determinant


def matrix_order(matrix: list[list[int]], limit: int = 10000) -> int:
    value = eye()
    for exponent in range(1, limit + 1):
        value = matmul(value, matrix)
        if value == eye():
            return exponent
    raise RuntimeError("orden no encontrado dentro de la cota")


def word_to_triads(
    word: str, schedule: list[list[list[int]]], number: int = 4
) -> tuple[int, ...]:
    state = [int(character) for character in word]
    digits = state[:]
    for matrix in schedule:
        state = row_mul(state, matrix)
        digits.extend(state)
    numerator = 0
    for digit in digits:
        numerator = 3 * numerator + digit
    denominator = 3 ** len(digits)
    return tuple(
        ((1000**index * numerator) // denominator) % 1000
        for index in range(1, number + 1)
    )


def main() -> None:
    baseline = [L0, L0, L1, L1]
    words = [
        "".join(map(str, word))
        for word in itertools.product(range(P), repeat=N)
    ]
    outputs = {word: word_to_triads(word, baseline) for word in words}
    require(len(set(outputs.values())) == 729, "la carta no es inyectiva")

    with CATALOGUE.open(newline="", encoding="utf-8") as handle:
        catalogue_words = {row["w6"] for row in csv.DictReader(handle)}
    require(len(catalogue_words) == 243, "censo de palabras del catálogo")
    complement_hits = sorted(
        word
        for word in catalogue_words
        if outputs[word][0] + outputs[word][1] == 999
    )
    require(
        complement_hits == [TARGETS["e"][0]],
        "complementariedad nonádica no única en el catálogo",
    )

    matches: dict[str, list[str]] = {}
    for name, (expected_word, target) in TARGETS.items():
        hits = [word for word, output in outputs.items() if output == target]
        require(hits == [expected_word], f"reconocimiento no único de {name}")
        matches[name] = hits

    calendar_scores: dict[str, int] = {}
    for bits in itertools.product((0, 1), repeat=4):
        schedule = [L0 if bit == 0 else L1 for bit in bits]
        key = "".join(map(str, bits))
        calendar_scores[key] = sum(
            word_to_triads(word, schedule) == target
            for word, target in TARGETS.values()
        )
    simultaneous = [key for key, score in calendar_scores.items() if score == 3]
    require(simultaneous == ["0011"], "calendario simultáneo no único")

    perturbations: Counter[int] = Counter()
    for matrix_number, matrix in enumerate((L0, L1)):
        for row in range(N):
            for column in range(N):
                for value in range(P):
                    if value == matrix[row][column]:
                        continue
                    changed = [matrix_row[:] for matrix_row in matrix]
                    changed[row][column] = value
                    schedule = (
                        [changed, changed, L1, L1]
                        if matrix_number == 0
                        else [L0, L0, changed, changed]
                    )
                    score = sum(
                        word_to_triads(word, schedule) == target
                        for word, target in TARGETS.values()
                    )
                    perturbations[score] += 1
    require(sum(perturbations.values()) == 144, "censo de perturbaciones")
    require(perturbations[3] == 0, "una perturbación conserva el triple")

    initial = [[int(character) for character in word] for word, _ in TARGETS.values()]
    u1 = [row_mul(word, L0) for word in initial]
    u2 = [row_mul(word, L0) for word in u1]
    u3 = [row_mul(word, L1) for word in u2]
    u4 = [row_mul(word, L1) for word in u3]
    source_l0, target_l0 = initial + u1, u1 + u2
    source_l1, target_l1 = u2 + u3, u3 + u4
    rank_l0 = rref(source_l0)[1]
    rank_l1 = rref(source_l1)[1]
    require((rank_l0, rank_l1) == (6, 6), "rangos de calibración")
    reconstructed_l0 = matmul(inverse(source_l0), target_l0)
    reconstructed_l1 = matmul(inverse(source_l1), target_l1)
    require(reconstructed_l0 == L0, "L0 no coincide con la interpolación")
    require(reconstructed_l1 == L1, "L1 no coincide con la interpolación")

    result = {
        "schema": "HMT.lector-arquimediano-calibrado.v1",
        "status": "PASS",
        "logical_scope": {
            "proved": (
                "propiedades finitas exactas condicionadas a L0, L1, "
                "el calendario y el lector de base mil declarados"
            ),
            "not_proved": (
                "derivación independiente de L0 y L1 desde APP-min ni "
                "emisión autónoma a profundidad arbitraria"
            ),
        },
        "matrices": {"L0": L0, "L1": L1},
        "determinants_mod3": {
            "L0": determinant_mod3(L0),
            "L1": determinant_mod3(L1),
        },
        "orders": {
            "L0": matrix_order(L0),
            "L1": matrix_order(L1),
            "L0L1": matrix_order(matmul(L0, L1)),
        },
        "finite_reader": {
            "words_checked": len(words),
            "distinct_outputs": len(set(outputs.values())),
            "catalogue_words_checked": len(catalogue_words),
            "first_two_triads_sum_999": complement_hits,
            "unique_matches": matches,
            "unique_simultaneous_calendar": simultaneous[0],
            "calendar_scores": calendar_scores,
            "single_entry_perturbations": {
                "checked": sum(perturbations.values()),
                "hit_histogram": dict(sorted(perturbations.items())),
            },
        },
        "calibration_audit": {
            "source_rank_L0": rank_l0,
            "source_rank_L1": rank_l1,
            "unique_matrix_from_declared_transitions": True,
            "reconstructed_L0": reconstructed_l0,
            "reconstructed_L1": reconstructed_l1,
            "interpretation": (
                "the six independent transition rows uniquely interpolate "
                "each matrix; uniqueness is not independent provenance"
            ),
        },
    }
    OUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    print("PASS_LECTOR_ARQUIMEDIANO_CALIBRADO")


if __name__ == "__main__":
    main()
