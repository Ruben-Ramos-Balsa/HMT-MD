#!/usr/bin/env python3
"""Certifica la incidencia N69 de los nueve cociclos y el dato direccional mínimo.

El programa fija primero, sin consultar el sello K, tres objetos:

* el bosque canónico de pasos 90/120 sobre Z/12;
* el atlas de invariantes N69 obtenido de q, a, c y colw, junto con la
  acción de Witt J;
* dos familias uniformes de lectores construidas con fase, calendario,
  carga visible o Witt--dual y orientación two-way.

Sólo después carga K desde la autoridad vigente para efectuar el contraste.
El contraste demuestra que los nueve residuos orientados pertenecen al atlas,
pero también que ninguna regla uniforme de las familias declaradas los
selecciona todos. Por último, enumera todas las elevaciones a [0,999]^12 y
prueba que la corona excepcional H_e intersección P_pi selecciona por sí sola
la elevación canónica; no se usa Q=6263 como selector.

No se emplean ``assert`` y el certificado es idéntico bajo Python normal y
``python -O``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
from math import prod
from pathlib import Path
from typing import Callable, Iterable


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CURRENT = ROOT / "03_PAPER/HMT_MACROPAPER_V3/CURRENT.json"
N69 = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_CADENA_VIGENTE/N69_CALENDARIO_TRANSICION/"
    "HMT_N69_ley_transicion_o_axioma_cilindrico_v1/"
    "N69_signatures_t0_t99.csv"
)
WITT_SOURCE = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "M12_WITT/verificar_m12_witt.py"
)
PHASE_CERTIFICATE = HERE / "RESULTADO_OBSTRUCCION_Y_DATO_MINIMO_W72.json"
OUT = HERE / "RESULTADO_COCICLOS_N69_Y_SECCION_DIRECCIONAL.json"


# Matriz de rotación interna usada por la firma N69. Satisface J^2=-I.
J_WITT = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 1, 2, 2),
    (1, 1, 0, 2, 1, 2),
    (1, 1, 2, 0, 2, 1),
    (1, 2, 1, 2, 0, 1),
    (1, 2, 2, 1, 1, 0),
)

# Matriz Paley empleada por el lector excepcional de doce posiciones.
WITT_CODE_MATRIX = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 2, 2, 1),
    (1, 1, 0, 1, 2, 2),
    (1, 2, 1, 0, 1, 2),
    (1, 2, 2, 1, 0, 1),
    (1, 1, 2, 2, 1, 0),
)

H4 = (
    (1, 1, 1, 1),
    (1, 1, -1, -1),
    (1, -1, 1, -1),
    (1, -1, -1, 1),
)

# Raíces 1,2,3. El paso +4 descompone Z/12 en cuatro órbitas de longitud 3.
# La única arista +3, 1 -> 4, enraíza la cuarta órbita. Dos aristas +4 en
# cada órbita completan el bosque. El orden es topológico y los índices son 0.
ROOT_SECTORS = (0, 1, 2)
CANONICAL_FOREST = (
    (0, 3, 3),
    (0, 4, 4),
    (1, 5, 4),
    (2, 6, 4),
    (3, 7, 4),
    (4, 8, 4),
    (5, 9, 4),
    (6, 10, 4),
    (7, 11, 4),
)

CHANNELS = ("q", "a", "c", "colw_mod")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def transform(word: str, matrix: tuple[tuple[int, ...], ...]) -> str:
    require(len(word) == 6 and set(word) <= {"0", "1", "2"}, "palabra mal tipada")
    vector = tuple(int(value) for value in word)
    return "".join(
        str(sum(vector[i] * matrix[i][j] for i in range(6)) % 3)
        for j in range(6)
    )


def witt_power(word: str, exponent: int) -> str:
    output = word
    for _ in range(exponent % 4):
        output = transform(output, J_WITT)
    return output


def word_from_residue(value: int) -> str:
    residue = int(value) % (3 ** 6)
    digits = []
    for power in range(5, -1, -1):
        unit = 3 ** power
        digit, residue = divmod(residue, unit)
        digits.append(str(digit))
    return "".join(digits)


def linear_word(bands: tuple[str, str, str], coefficients: tuple[int, int, int]) -> str:
    return "".join(
        str(sum(coefficients[i] * int(bands[i][j]) for i in range(3)) % 3)
        for j in range(6)
    )


def visible_charge(bands: tuple[str, str, str]) -> tuple[int, int, int]:
    return tuple(sum(int(value) for value in band) % 3 for band in bands)  # type: ignore[return-value]


def dual_charge(bands: tuple[str, str, str]) -> tuple[int, int, int]:
    return tuple(
        sum(int(value) for value in transform(band, J_WITT)) % 3 for band in bands
    )  # type: ignore[return-value]


def read_rows() -> list[dict[str, str]]:
    with N69.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 100, "N69 ya no contiene cien estados")
    for expected_t, row in enumerate(rows):
        require(int(row["t"]) == expected_t, "el calendario N69 no está ordenado")
        bands_raw = tuple(row["B"].split("|"))
        require(len(bands_raw) == 3, "frontera N69 mal formada")
        bands = (bands_raw[0], bands_raw[1], bands_raw[2])
        require("".join(map(str, visible_charge(bands))) == row["r"].zfill(3),
                "carga visible N69 inconsistente")
        require("".join(map(str, dual_charge(bands))) == row["dual"].zfill(3),
                "carga Witt-dual N69 inconsistente")
    return rows


def cylinder_roots(w24: str) -> tuple[int, int, int]:
    require(len(w24) == 24 and set(w24) <= {"0", "1", "2"}, "W24 mal tipada")
    numerator = int(w24, 3)
    denominator = 3 ** len(w24)
    roots: list[int] = []
    for depth in range(1, 13):
        scale = 1000 ** depth
        lower = numerator * scale // denominator
        upper = ((numerator + 1) * scale - 1) // denominator
        if lower != upper:
            break
        rendered = f"{lower:0{3 * depth}d}"
        roots = [int(rendered[index:index + 3]) for index in range(0, len(rendered), 3)]
    require(roots == [234, 543, 140], "W24 ya no fuerza las tres raíces publicadas")
    return roots[0], roots[1], roots[2]


def determinant_bareiss(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for pivot_index in range(len(work) - 1):
        pivot_row = next(
            (row for row in range(pivot_index, len(work)) if work[row][pivot_index]),
            None,
        )
        require(pivot_row is not None, "matriz singular en la eliminación de Bareiss")
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = work[pivot_row], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, len(work)):
            for column in range(pivot_index + 1, len(work)):
                work[row][column] = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                ) // previous
        previous = pivot
    return sign * work[-1][-1]


def forest_structure_audit() -> dict[str, object]:
    adjacency: dict[int, set[int]] = {index: set() for index in range(12)}
    for source, target, step in CANONICAL_FOREST:
        require((target - source) % 12 == step, "arista incompatible con su paso")
        adjacency[source].add(target)
        adjacency[target].add(source)

    require(set().union(*adjacency.values()) == set(range(12)),
            "el bosque no cubre los doce sectores")
    require(len(CANONICAL_FOREST) == 12 - len(ROOT_SECTORS),
            "el número de aristas no corresponde a tres componentes")

    orbits_step4 = tuple(
        tuple((root + 4 * index) % 12 for index in range(3)) for root in range(4)
    )
    require(orbits_step4 == ((0, 4, 8), (1, 5, 9), (2, 6, 10), (3, 7, 11)),
            "órbitas de paso cuatro inesperadas")

    # Cada componente contiene exactamente una de las raíces 0,1,2.
    components: list[set[int]] = []
    remaining = set(range(12))
    while remaining:
        seed = min(remaining)
        component: set[int] = set()
        stack = [seed]
        while stack:
            vertex = stack.pop()
            if vertex in component:
                continue
            component.add(vertex)
            stack.extend(adjacency[vertex] - component)
        components.append(component)
        remaining -= component
    require(len(components) == 3, "el bosque no tiene tres componentes")
    require(all(len(component & set(ROOT_SECTORS)) == 1 for component in components),
            "una componente no contiene una única raíz")

    coordinate_matrix: list[list[int]] = []
    for root in ROOT_SECTORS:
        row = [0] * 12
        row[root] = 1
        coordinate_matrix.append(row)
    for source, target, _step in CANONICAL_FOREST:
        row = [0] * 12
        row[source] = 1
        row[target] = -1
        coordinate_matrix.append(row)
    determinant = determinant_bareiss(coordinate_matrix)
    require(determinant == -1, "la carta raíz--bosque dejó de ser unimodular")

    return {
        "roots_1based": [value + 1 for value in ROOT_SECTORS],
        "step4_orbits_1based": [[value + 1 for value in orbit] for orbit in orbits_step4],
        "edges_topological_1based": [
            {"source": source + 1, "target": target + 1, "step": step}
            for source, target, step in CANONICAL_FOREST
        ],
        "components_1based": [sorted(value + 1 for value in component) for component in components],
        "determinant_roots_plus_edges": determinant,
        "unimodular": True,
        "construction": (
            "el paso +4 da cuatro órbitas de tres sectores; las raíces 1,2,3 "
            "enraízan tres y la arista +3 de 1 a 4 enraíza la cuarta"
        ),
    }


def atlas_addresses(rows: list[dict[str, str]]) -> dict[str, list[dict[str, object]]]:
    for coordinate in range(6):
        basis = "".join("1" if index == coordinate else "0" for index in range(6))
        negative = "".join("2" if index == coordinate else "0" for index in range(6))
        require(witt_power(basis, 2) == negative, "J^2 dejó de ser -I")
        require(witt_power(basis, 4) == basis, "J dejó de tener orden cuatro")
    atlas: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        for channel in CHANNELS:
            source = row[channel]
            for power in range(4):
                output = witt_power(source, power)
                atlas.setdefault(output, []).append({
                    "t": int(row["t"]),
                    "K_calendar": int(row["K"]),
                    "dK_next": int(row["dK_next"]),
                    "channel": channel,
                    "Witt_power": power,
                })
    require(sum(len(values) for values in atlas.values()) == 1600,
            "el atlas no contiene 100 x 4 x 4 direcciones")
    return atlas


def fixed_channel_no_go(
    rows: list[dict[str, str]], target_words: tuple[str, ...]
) -> dict[str, object]:
    target = set(target_words)
    coverage: list[dict[str, object]] = []
    for channel in CHANNELS:
        for power in range(4):
            image = {witt_power(row[channel], power) for row in rows}
            hits = sorted(target & image)
            coverage.append({
                "channel": channel,
                "Witt_power": power,
                "covered": len(hits),
                "words": hits,
            })
    maximum = max(int(item["covered"]) for item in coverage)
    require(maximum == 3, "cambió el máximo de la familia canal--Witt fija")
    return {
        "family": (
            "fijar un canal x en {q,a,c,colw_mod} y una potencia k en Z/4; "
            "permitir cualquier tiempo t del calendario y emitir J^k x_t"
        ),
        "number_of_uniform_readers": len(coverage),
        "maximum_of_nine_residues_covered": maximum,
        "all_readers": coverage,
        "no_go": True,
    }


def linear_invariant_phase_no_go(
    rows: list[dict[str, str]], target_words: tuple[str, ...]
) -> dict[str, object]:
    """Agota combinaciones lineales de los cuatro invariantes y un reloj."""

    target = set(target_words)
    phase_sources: dict[str, Callable[[dict[str, str]], int]] = {
        "physical_predecessor": lambda row: (int(row["t"]) - 1) % 3,
        "frontier_phase": lambda row: int(row["t"]) % 3,
        "Beatty_calendar": lambda row: int(row["K"]) % 3,
        "Beatty_predecessor": lambda row: (int(row["K"]) - 1) % 3,
        "open_prune_bit": lambda row: int(row["dK_next"]) % 3,
    }
    maximum = -1
    best: list[dict[str, object]] = []
    readers = 0
    for phase_name, phase_function in phase_sources.items():
        for channel_coefficients in itertools.product(range(3), repeat=4):
            for phase_coefficient, constant, power in itertools.product(
                range(3), range(3), range(4)
            ):
                readers += 1
                image: set[str] = set()
                for row in rows:
                    combined = "".join(
                        str(sum(
                            channel_coefficients[index] * int(row[channel][coordinate])
                            for index, channel in enumerate(CHANNELS)
                        ) % 3)
                        for coordinate in range(6)
                    )
                    shift = (phase_coefficient * phase_function(row) + constant) % 3
                    shifted = "".join(str((int(value) + shift) % 3) for value in combined)
                    image.add(witt_power(shifted, power))
                words = sorted(target & image)
                record = {
                    "phase": phase_name,
                    "channel_coefficients_q_a_c_colw": list(channel_coefficients),
                    "phase_coefficient": phase_coefficient,
                    "constant": constant,
                    "Witt_power": power,
                    "covered": len(words),
                    "words": words,
                }
                if len(words) > maximum:
                    maximum = len(words)
                    best = [record]
                elif len(words) == maximum:
                    best.append(record)

    require(readers == 5 * (3 ** 4) * 3 * 3 * 4,
            "número inesperado de combinaciones lineales de invariantes")
    require(maximum == 5, "cambió el máximo de la familia lineal de invariantes")
    return {
        "family": (
            "J^k(lambda_q q_t+lambda_a a_t+lambda_c c_t+lambda_w w_t+"
            "(b p_t+c) 1), con todos los coeficientes en F3 y cinco relojes"
        ),
        "number_of_uniform_readers": readers,
        "maximum_of_nine_residues_covered": maximum,
        "number_of_best_readers": len(best),
        "best_readers": best,
        "no_go": True,
    }


def affine_phase_charge_no_go(
    rows: list[dict[str, str]], target_words: tuple[str, ...]
) -> dict[str, object]:
    target = set(target_words)
    phase_sources: dict[str, Callable[[dict[str, str]], int]] = {
        "physical_predecessor": lambda row: (int(row["t"]) - 1) % 3,
        "frontier_phase": lambda row: int(row["t"]) % 3,
        "Beatty_calendar": lambda row: int(row["K"]) % 3,
        "Beatty_predecessor": lambda row: (int(row["K"]) - 1) % 3,
        "open_prune_bit": lambda row: int(row["dK_next"]) % 3,
    }
    charge_sources: dict[
        str, Callable[[tuple[str, str, str]], tuple[int, int, int]]
    ] = {"visible": visible_charge, "Witt_dual": dual_charge}

    best: list[dict[str, object]] = []
    maximum = -1
    readers = 0
    for phase_name, phase_function in phase_sources.items():
        for charge_name, charge_function in charge_sources.items():
            for a, b, c, power in itertools.product(range(3), range(3), range(3), range(4)):
                readers += 1
                image: set[str] = set()
                for row in rows:
                    bands_raw = tuple(row["B"].split("|"))
                    bands = (bands_raw[0], bands_raw[1], bands_raw[2])
                    charge = charge_function(bands)
                    phase = phase_function(row)
                    coefficients = tuple((a * value + b * phase + c) % 3 for value in charge)
                    image.add(witt_power(linear_word(bands, coefficients), power))  # type: ignore[arg-type]
                words = sorted(target & image)
                record = {
                    "phase": phase_name,
                    "charge": charge_name,
                    "a": a,
                    "b": b,
                    "c": c,
                    "Witt_power": power,
                    "covered": len(words),
                    "words": words,
                }
                if len(words) > maximum:
                    maximum = len(words)
                    best = [record]
                elif len(words) == maximum:
                    best.append(record)

    require(readers == 5 * 2 * 27 * 4, "número inesperado de lectores afines")
    require(maximum == 4, "cambió el máximo de la familia afín fase--carga")
    return {
        "family": (
            "c_i=a chi_i+b p+c en F3, con chi visible o Witt-dual; "
            "p tomado de fase física, fase de frontera, calendario Beatty, "
            "predecesor Beatty o bit abrir/podar; salida J^k sum_i c_i B_i"
        ),
        "two_way_orientation_included": (
            "sí: la inversión de signo está contenida por los coeficientes en F3 "
            "y por J^2=-I"
        ),
        "number_of_uniform_readers": readers,
        "maximum_of_nine_residues_covered": maximum,
        "number_of_best_readers": len(best),
        "best_readers": best,
        "no_go": True,
    }


def comparison_phase_charge_no_go(
    rows: list[dict[str, str]], target_words: tuple[str, ...]
) -> dict[str, object]:
    target = set(target_words)
    phase_sources: dict[str, Callable[[dict[str, str]], int]] = {
        "physical_predecessor": lambda row: (int(row["t"]) - 1) % 3,
        "frontier_phase": lambda row: int(row["t"]) % 3,
        "Beatty_calendar": lambda row: int(row["K"]) % 3,
    }
    charge_sources: dict[
        str, Callable[[tuple[str, str, str]], tuple[int, int, int]]
    ] = {"visible": visible_charge, "Witt_dual": dual_charge}

    readers = 0
    maximum = -1
    best: list[dict[str, object]] = []
    for phase_name, phase_function in phase_sources.items():
        for charge_name, charge_function in charge_sources.items():
            for offset, orientation, power in itertools.product(range(3), (1, -1), range(4)):
                readers += 1
                image: set[str] = set()
                for row in rows:
                    bands_raw = tuple(row["B"].split("|"))
                    bands = (bands_raw[0], bands_raw[1], bands_raw[2])
                    charge = charge_function(bands)
                    selected = (phase_function(row) + offset) % 3
                    coefficients = tuple(
                        orientation * (1 if value == selected else -1) % 3
                        for value in charge
                    )
                    image.add(witt_power(linear_word(bands, coefficients), power))  # type: ignore[arg-type]
                words = sorted(target & image)
                record = {
                    "phase": phase_name,
                    "charge": charge_name,
                    "offset": offset,
                    "orientation": orientation,
                    "Witt_power": power,
                    "covered": len(words),
                    "words": words,
                }
                if len(words) > maximum:
                    maximum = len(words)
                    best = [record]
                elif len(words) == maximum:
                    best.append(record)
    require(readers == 3 * 2 * 3 * 2 * 4, "número inesperado de lectores de comparación")
    require(maximum == 3, "cambió el máximo de la familia de comparación")
    return {
        "family": (
            "c_i=epsilon cuando chi_i=p+delta y c_i=-epsilon en otro caso; "
            "chi visible o Witt-dual, delta en F3, epsilon two-way y salida J^k"
        ),
        "number_of_uniform_readers": readers,
        "maximum_of_nine_residues_covered": maximum,
        "number_of_best_readers": len(best),
        "best_readers": best,
        "no_go": True,
    }


def canonical_contrast(
    current: dict[str, object], rows: list[dict[str, str]], atlas: dict[str, list[dict[str, object]]]
) -> tuple[tuple[int, ...], tuple[str, ...], dict[str, object]]:
    # La familia, el bosque y el atlas ya están construidos cuando se lee K.
    k = tuple(int(value) for value in current["state_types"]["CanonicalSealK"]["coordinates"])  # type: ignore[index]
    require(len(k) == 12, "el sello canónico no tiene doce coordenadas")
    differences = tuple(k[source] - k[target] for source, target, _step in CANONICAL_FOREST)
    residues = tuple(value % (3 ** 6) for value in differences)
    words = tuple(word_from_residue(value) for value in residues)
    require(words == (
        "022200", "102021", "121121", "100012", "220212",
        "122120", "001010", "122121", "020220",
    ), "cambiaron los nueve residuos orientados")
    require(all(word in atlas for word in words), "un residuo orientado no pertenece al atlas N69")

    hits = []
    multiplicities = []
    for edge, difference, residue, word in zip(CANONICAL_FOREST, differences, residues, words):
        addresses = atlas[word]
        multiplicities.append(len(addresses))
        hits.append({
            "edge_1based": {"source": edge[0] + 1, "target": edge[1] + 1, "step": edge[2]},
            "oriented_integer_difference": difference,
            "residue_mod_729": residue,
            "six_trit_word": word,
            "N69_address_count": len(addresses),
            "N69_addresses": addresses,
        })
    require(tuple(multiplicities) == (5, 3, 2, 1, 3, 1, 1, 3, 5),
            "multiplicidades de incidencia N69 alteradas")
    require(prod(multiplicities) == 1350, "número de secciones representativas alterado")
    return differences, words, {
        "K_used_only_now_as_external_contrast": list(k),
        "oriented_differences": list(differences),
        "residues_mod_729": list(residues),
        "words": list(words),
        "incidences": hits,
        "address_multiplicities": multiplicities,
        "number_of_address_sections_with_same_ordered_outputs": prod(multiplicities),
        "exact_scope": (
            "incidencia completa: cada residuo aparece; no selección, porque N69 "
            "conserva 1350 secciones de direcciones con la misma salida ordenada"
        ),
    }


def possible_lifts(residue: int) -> tuple[int, ...]:
    base = residue % (3 ** 6)
    return tuple(range(base, 1000, 3 ** 6))


def enumerate_lifts(
    roots: tuple[int, int, int], residues: tuple[int, ...]
) -> list[tuple[int, ...]]:
    states: list[dict[int, int]] = [
        {sector: value for sector, value in zip(ROOT_SECTORS, roots)}
    ]
    for (source, target, _step), residue in zip(CANONICAL_FOREST, residues):
        next_states: list[dict[int, int]] = []
        for state in states:
            require(source in state and target not in state, "orden no topológico del bosque")
            target_residue = (state[source] - residue) % (3 ** 6)
            for value in possible_lifts(target_residue):
                extension = dict(state)
                extension[target] = value
                next_states.append(extension)
        states = next_states
    output = [tuple(state[index] for index in range(12)) for state in states]
    require(len(output) == len(set(output)) == 64, "la fibra de elevaciones ya no tiene tamaño 64")
    return output


def witt_codeword(word: tuple[int, ...]) -> tuple[int, ...]:
    require(len(word) == 6, "la palabra de canal no tiene seis trits")
    right = tuple(
        sum(word[i] * WITT_CODE_MATRIX[i][j] for i in range(6)) % 3
        for j in range(6)
    )
    return word + right


def high_crown(vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(index + 1 for index, value in enumerate(vector) if value >= 3 ** 6)


def hadamard_readout(k: tuple[int, ...]) -> tuple[int, ...]:
    output = [0] * 12
    for residue_class in range(3):
        block = [k[residue_class + 3 * index] for index in range(4)]
        transformed = [
            sum(row[index] * block[index] for index in range(4)) for row in H4
        ]
        for index, value in enumerate(transformed):
            output[residue_class + 3 * index] = value
    return tuple(output)


def lift_and_exceptional_audit(
    current: dict[str, object], roots: tuple[int, int, int], residues: tuple[int, ...]
) -> dict[str, object]:
    candidates = enumerate_lifts(roots, residues)

    p_pi_word = (0, 1, 0, 2, 1, 1)
    h_e_word = (2, 0, 1, 1, 0, 1)
    p_pi = tuple(index + 1 for index, value in enumerate(witt_codeword(p_pi_word)) if value)
    h_e = tuple(index + 1 for index, value in enumerate(witt_codeword(h_e_word)) if value)
    exceptional_face = tuple(sorted(set(p_pi) & set(h_e)))
    require(p_pi == (2, 4, 5, 6, 7, 8, 9, 10, 11), "P_pi inesperado")
    require(h_e == (1, 3, 4, 6, 9, 10), "H_e inesperado")
    require(exceptional_face == (4, 6, 9, 10), "cara excepcional inesperada")

    corona_survivors = [candidate for candidate in candidates if high_crown(candidate) == exceptional_face]
    residue_total_survivors = [candidate for candidate in candidates if sum(candidate) % 3 == 2]
    exact_total_survivors = [candidate for candidate in candidates if sum(candidate) == 6263]

    expected_positive_support = tuple(
        index + 1 for index, value in enumerate(
            current["state_types"]["SignedDodecaphaseState"]["coordinates"]  # type: ignore[index]
        ) if int(value) > 0
    )
    signed_support_survivors = [
        candidate for candidate in candidates
        if tuple(index + 1 for index, value in enumerate(hadamard_readout(candidate)) if value > 0)
        == expected_positive_support
    ]

    require(len(corona_survivors) == 1, "la corona excepcional dejó de seleccionar una elevación")
    require(len(residue_total_survivors) == 64, "el residuo total ya no es constante en la fibra")
    require(len(exact_total_survivors) == 15, "Q entero ya no deja quince elevaciones")
    require(len(signed_support_survivors) == 1, "el soporte firmado dejó de seleccionar una elevación")

    selected = corona_survivors[0]
    canonical_k = tuple(
        int(value) for value in current["state_types"]["CanonicalSealK"]["coordinates"]  # type: ignore[index]
    )
    canonical_u = tuple(
        int(value) for value in current["state_types"]["SignedDodecaphaseState"]["coordinates"]  # type: ignore[index]
    )
    require(selected == canonical_k, "la corona no selecciona el sello canónico")
    require(hadamard_readout(selected) == canonical_u, "la lectura Hadamard no reconoce U12")
    require(signed_support_survivors == [selected], "las dos lecturas no convergen")

    return {
        "roots_forced_by_W24": list(roots),
        "candidate_lifts_in_0_999_power_12": len(candidates),
        "two_way_ambiguity": "2^6=64 elevaciones; seis decisiones de hoja",
        "exceptional_reader": {
            "P_pi": list(p_pi),
            "H_e": list(h_e),
            "B_exc_equals_intersection": list(exceptional_face),
            "crown_rule": "B(x)={i:x_i>=3^6}",
            "survivors": len(corona_survivors),
        },
        "ablations": {
            "total_residue_mod3_equals_2": len(residue_total_survivors),
            "exact_total_Q_equals_6263": len(exact_total_survivors),
            "positive_support_of_H4_equals_1_2_3_5": len(signed_support_survivors),
            "exceptional_crown_only": len(corona_survivors),
        },
        "selected_K": list(selected),
        "selected_U12_signed": list(hadamard_readout(selected)),
        "exact_conclusion": (
            "dados los nueve residuos, la cara excepcional resuelve por sí sola "
            "todas las decisiones de elevación; Q=6263 no es premisa selectora"
        ),
    }


def build_result() -> dict[str, object]:
    current = json.loads(CURRENT.read_text(encoding="utf-8"))
    require(current["revision"] == "2026-07-22.2", "revisión canónica inesperada")
    phase = json.loads(PHASE_CERTIFICATE.read_text(encoding="utf-8"))
    require(str(phase["status"]).startswith("PASS"), "certificado de fase no válido")
    w24 = str(phase["minimal_dodecaphase_interface"]["W24"])

    rows = read_rows()
    forest = forest_structure_audit()
    roots = cylinder_roots(w24)
    atlas = atlas_addresses(rows)

    # El contraste canónico se ejecuta sólo después de fijar bosque, atlas y
    # familias de lectores. Sus palabras objetivo no intervienen en esas definiciones.
    differences, target_words, contrast = canonical_contrast(current, rows, atlas)
    residues = tuple(value % (3 ** 6) for value in differences)

    fixed_no_go = fixed_channel_no_go(rows, target_words)
    linear_invariant_no_go = linear_invariant_phase_no_go(rows, target_words)
    affine_no_go = affine_phase_charge_no_go(rows, target_words)
    comparison_no_go = comparison_phase_charge_no_go(rows, target_words)
    lift_audit = lift_and_exceptional_audit(current, roots, residues)

    return {
        "schema": "HMT.N69.cociclos-seccion-direccional.v1",
        "status": "PASS_INCIDENCIA_NO_GO_UNIFORME_Y_ELEVACION_UNICA",
        "canon_revision": current["revision"],
        "forest_defined_before_K": forest,
        "N69_Witt_atlas": {
            "states": len(rows),
            "channels": list(CHANNELS),
            "Witt_powers": 4,
            "indexed_addresses": 1600,
            "distinct_words": len(atlas),
        },
        "canonical_contrast_after_definitions": contrast,
        "uniform_reader_no_go": {
            "fixed_channel_and_Witt_power": fixed_no_go,
            "linear_combination_of_N69_invariants_and_phase": linear_invariant_no_go,
            "affine_phase_charge_calendar": affine_no_go,
            "comparison_phase_charge": comparison_no_go,
            "joint_conclusion": (
                "la pertenencia de las nueve palabras al atlas no equivale a una derivación: "
                "ningún lector uniforme de las familias declaradas contiene las nueve"
            ),
        },
        "integer_lifts_and_exceptional_selection": lift_audit,
        "minimal_missing_datum": {
            "type": "sección direccional del bosque en el atlas N69--Witt",
            "formula": (
                "sigma_F:E(F)->{0,...,99}x{q,a,c,colw_mod}xZ/4, "
                "omega_e=valor(J^k x_t) en F3^6"
            ),
            "not_an_additional_scalar": True,
            "not_Q_6263": True,
            "representatives_for_the_canonical_output": 1350,
            "why_it_is_missing": (
                "fase, carga, calendario y orientación determinan un atlas y restricciones, "
                "pero no distinguen una de las secciones representativas"
            ),
            "what_it_would_close": (
                "una vez emitidos en orden los nueve residuos, W24 fija tres raíces y "
                "B_exc=H_e intersección P_pi fija de manera única las seis hojas restantes"
            ),
        },
        "proof_strength": {
            "forest_and_lift_enumeration": "EXACTO_INTERNO",
            "N69_incidence": "EXACTO_INTERNO como incidencia, no como selección",
            "uniform_family_no_go": "EXACTO_INTERNO para las familias declaradas",
            "exceptional_crown_selection": "RELATIVO_A_PRIMITIVAS del lector Witt vigente",
            "global_directional_section": "NO_DERIVADA; localizada sin ambigüedad",
        },
        "provenance": {
            "canonical_90_120_forest": "FORMALIZACION_NUEVA",
            "N69_invariants_and_Witt_action": "ARQUITECTURA_AUTORAL_PREEXISTENTE",
            "nine_residue_incidence": "CERTIFICADO_NUEVO",
            "uniform_reader_no_go": "RESULTADO_NUEVO",
            "64_to_1_by_exceptional_crown": "RESULTADO_NUEVO",
        },
        "source_sha256": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in (CURRENT, N69, WITT_SOURCE, PHASE_CERTIFICATE)
        },
    }


def render(result: dict[str, object]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-certificate", action="store_true")
    arguments = parser.parse_args()
    payload = render(build_result())
    if arguments.check_certificate:
        require(OUT.exists(), "no existe el certificado congelado")
        require(OUT.read_text(encoding="utf-8") == payload, "el certificado no es reproducible")
    else:
        OUT.write_text(payload, encoding="utf-8")
    print("PASS — incidencia N69, no-go uniforme y elevación única por corona excepcional")


if __name__ == "__main__":
    main()
