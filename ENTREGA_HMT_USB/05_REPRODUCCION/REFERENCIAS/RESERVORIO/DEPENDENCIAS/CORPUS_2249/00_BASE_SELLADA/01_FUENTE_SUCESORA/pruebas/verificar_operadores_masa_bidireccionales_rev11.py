#!/usr/bin/env python3
"""Certifica los dos lectores bidireccionales de masa de REV.11.

La fase estructural abre exclusivamente tres tablas internas: el censo de
324 rutas, el registro 81x108 y el transductor de las 81 celdas. No abre
masas, etiquetas metrológicas, PDG ni CODATA. El certificado distingue el
lector de desplazamientos sobre CT108 del lector de autocorrelación
dodecafásica; su coincidencia electrónica no se promueve a equivalencia
global.
"""

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import io
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence


SCRIPT = Path(__file__).resolve()
ROOT = SCRIPT.parents[1]
ROUTES = (
    ROOT
    / "testigos_integracion/ley_masas_hmt_md_2026-07-30/"
    "datos/internos/persistencia/rutas_persistencia_324.csv"
)
LEDGER = ROOT / "datos/ledger_tpk_81x108.csv"
TRANSDUCTOR = ROOT / "datos/transductor_rutas_81.csv"
DEFAULT_CERTIFICATE = ROOT / "certificados/operadores_masa_bidireccionales_rev11.json"
ALLOWLIST = frozenset(path.resolve() for path in (ROUTES, LEDGER, TRANSDUCTOR))
OPENED: list[str] = []
EXPECTED_HASHES = {
    ROUTES.resolve(): "485e35da375870607f3d4b2c92241001a4d09237fe6b922aacabeb1f0832e522",
    LEDGER.resolve(): "d801d2430b23417d0e34c3bea5ed873fd0be06ec68250dd22224ff9b98071680",
    TRANSDUCTOR.resolve(): "8c53ce492adbf147b51c56625df24df6e788831603a19e242f548aa713369261",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def read_rows(path: Path) -> tuple[list[dict[str, str]], str]:
    resolved = path.resolve()
    require(resolved in ALLOWLIST, f"entrada fuera de allowlist: {resolved}")
    OPENED.append(resolved.relative_to(ROOT).as_posix())
    with resolved.open("rb") as stream:
        raw = stream.read()
    observed = hashlib.sha256(raw).hexdigest()
    require(observed == EXPECTED_HASHES[resolved], f"hash inesperado: {resolved}")
    text = raw.decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text, newline=""))), observed


def trits_from_words(value: str) -> tuple[int, ...]:
    result: list[int] = []
    for word_text in value.split():
        word = int(word_text)
        block = [0] * 6
        for index in range(5, -1, -1):
            block[index] = word % 3
            word //= 3
        require(word == 0, "palabra w6 fuera de F3^6")
        result.extend(block)
    require(len(result) == 108, "la ruta no contiene 108 trits")
    return tuple(result)


def displacement(word: Sequence[int], lag: int) -> int:
    size = len(word)
    return sum(word[index] != word[(index + lag) % size] for index in range(size))


def reader_d(word: tuple[int, ...]) -> tuple[int, int, int]:
    numerator = displacement(word, 4) - displacement(word, 3)
    require(numerator % 2 == 0, "(D4-D3)/2 no es entero")
    return (
        displacement(word, 27) + displacement(word, 36),
        displacement(word, 1),
        numerator // 2,
    )


def tau_word(value: str) -> tuple[int, ...]:
    mapping = {"+": 1, "-": -1, "0": 0}
    require(set(value) <= set(mapping), "símbolo fuera del alfabeto trítico")
    result = tuple(mapping[character] for character in value)
    require(len(result) == 12, "la palabra tau no tiene doce fases")
    return result


def correlation(word: Sequence[int], lag: int) -> int:
    size = len(word)
    return sum(word[index] * word[(index + lag) % size] for index in range(size))


def omega(word: tuple[int, ...]) -> int:
    return (
        -2 * correlation(word, 1)
        - 4 * correlation(word, 2)
        - 6 * correlation(word, 3)
    )


def window_energy(word: Sequence[int], length: int) -> int:
    size = len(word)
    return sum(
        sum(word[(index + offset) % size] for offset in range(length)) ** 2
        for index in range(size)
    )


def omega_from_window_energies(word: tuple[int, ...]) -> int:
    return 4 * window_energy(word, 3) - 3 * window_energy(word, 4)


def p6(word: tuple[int, ...]) -> int:
    return sum(word[index] * word[index + 6] for index in range(6))


def reader_omega(word: tuple[int, ...]) -> tuple[int, int, int]:
    require(correlation(word, 6) == 2 * p6(word), "C6 != 2 P6")
    return omega(word), 54, p6(word)


def dr9(value: int) -> int:
    residue = value % 9
    return 9 if residue == 0 else residue


def mov3(phase: int) -> int:
    if phase in (1, 4, 7):
        return 1
    if phase in (2, 5, 8):
        return -1
    return 0


def simulated_route(
    seed: tuple[int, int], h0: int, v0: int, sheet_policy: str
) -> tuple[int, ...]:
    """Reconstruye la palabra trítica para la ablación declarada de hojas."""

    require(sheet_policy in {"normal", "sum_only", "product_only"}, "política de hoja")
    r, c = seed
    h, v = h0, v0
    trits: list[int] = []
    for tick in range(1, 109):
        move = mov3(1 + ((tick - 1) % 9))
        if move == 1:
            raw = r + c if sheet_policy != "product_only" else r * c
            c = 1 + ((c - 1 + h) % 9)
        elif move == -1:
            raw = r * c if sheet_policy != "sum_only" else r + c
            r = 1 + ((r - 1 + v) % 9)
        else:
            raw = 9
        trits.append(dr9(raw) % 3)
        if tick in (27, 54, 81):
            h, v = -h, -v
    require((r, c) == seed, "la ruta simulada no cierra posicionalmente")
    require((h, v) == (-h0, -v0), "holonomía simulada inesperada")
    return tuple(trits)


def add(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(left, right))


def polar(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    numerator = omega(add(left, right)) - omega(left) - omega(right)
    require(numerator % 2 == 0, "polarización no integral")
    return numerator // 2


def distribution(
    values: Iterable[tuple[int, int, int]],
) -> list[dict[str, object]]:
    counts = collections.Counter(values)
    return [
        {"profile": list(profile), "multiplicity": counts[profile]}
        for profile in sorted(counts)
    ]


def profile_cardinalities(
    groups: dict[str, set[object]],
) -> dict[str, int]:
    counts = collections.Counter(len(values) for values in groups.values())
    return {str(cardinality): counts[cardinality] for cardinality in sorted(counts)}


def rational_string(numerator: int, denominator: int) -> str:
    value = Fraction(numerator, denominator)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def spectrum(values: Iterable[tuple[int, int, int]]) -> list[dict[str, object]]:
    return distribution(values)


def build_certificate() -> dict[str, object]:
    OPENED.clear()
    route_rows, routes_hash = read_rows(ROUTES)
    ledger_rows, ledger_hash = read_rows(LEDGER)
    transductor_rows, transductor_hash = read_rows(TRANSDUCTOR)
    expected_opened = sorted(path.relative_to(ROOT).as_posix() for path in ALLOWLIST)
    require(sorted(OPENED) == expected_opened, "el registro de aperturas difiere de la allowlist")
    require(len(route_rows) == 324, "dominio de rutas distinto de 324")
    require(len(ledger_rows) == 81 * 108, "registro distinto de 81x108")
    require(len(transductor_rows) == 81, "transductor distinto de 81 celdas")

    route_keys = {
        (int(row["seed_r"]), int(row["seed_c"]), int(row["h0"]), int(row["v0"]))
        for row in route_rows
    }
    require(
        route_keys
        == {
            (r, c, h, v)
            for r in range(1, 10)
            for c in range(1, 10)
            for h in (-1, 1)
            for v in (-1, 1)
        },
        "la cobertura de rutas no es 81x4",
    )

    words: dict[str, tuple[int, ...]] = {}
    taus: dict[str, tuple[int, ...]] = {}
    values_d: dict[str, tuple[int, int, int]] = {}
    values_omega: dict[str, tuple[int, int, int]] = {}
    for row in route_rows:
        candidate = row["candidate_id"]
        require(candidate not in words, f"ruta duplicada: {candidate}")
        word = trits_from_words(row["w6_words"])
        tau = tau_word(row["tau"])
        words[candidate] = word
        taus[candidate] = tau
        values_d[candidate] = reader_d(word)
        values_omega[candidate] = reader_omega(tau)

    routes_by_state = {
        (int(row["seed_r"]), int(row["seed_c"]), int(row["h0"]), int(row["v0"])):
        words[row["candidate_id"]]
        for row in route_rows
    }
    for (r, c, h, v), word in routes_by_state.items():
        require(word[54:] + word[:54] == word, "falla periodicidad de 54 pasos")
        opposite = routes_by_state[(r, c, -h, -v)]
        require(
            opposite == word[27:] + word[:27],
            "la inversión simultánea no coincide con el desplazamiento 27",
        )

    electron_id = "r5c5_h+1v+1"
    electron_word = words[electron_id]
    electron_displacements = {
        f"D{lag}": displacement(electron_word, lag)
        for lag in (1, 3, 4, 27, 36)
    }
    require(
        electron_displacements == {"D1": 54, "D3": 56, "D4": 68, "D27": 48, "D36": 32},
        "perfil CT108 electrónico inesperado",
    )
    require(values_d[electron_id] == (80, 54, 6), "K_D electrónico incorrecto")
    require(
        values_omega[electron_id] == (80, 54, 6),
        "K_Omega electrónico incorrecto",
    )
    electron_ablations = {
        policy: reader_d(simulated_route((5, 5), 1, 1, policy))
        for policy in ("normal", "sum_only", "product_only")
    }
    require(
        electron_ablations
        == {
            "normal": (80, 54, 6),
            "sum_only": (80, 84, -8),
            "product_only": (80, 60, 13),
        },
        "ablación electrónica de hojas inesperada",
    )

    # Naturalidad exacta del lector CT108.
    alphabet = (0, 1, 2)
    for candidate, word in words.items():
        base = values_d[candidate]
        for offset in range(108):
            require(reader_d(word[offset:] + word[:offset]) == base, "falla C108")
        require(reader_d(tuple(reversed(word))) == base, "falla reversión CT108")
        for image in itertools.permutations(alphabet):
            relabel = dict(zip(alphabet, image))
            require(
                reader_d(tuple(relabel[value] for value in word)) == base,
                "falla naturalidad S3",
            )

    # Naturalidad dodecafásica y cociclo sobre las 19 palabras realizadas.
    realized_taus = sorted(set(taus.values()))
    require(len(realized_taus) == 19, "censo de palabras tau distinto de 19")
    for word in realized_taus:
        base = reader_omega(word)
        require(
            omega_from_window_energies(word) == base[0],
            "la identidad 4 A3 - 3 A4 difiere de la forma de correlaciones",
        )
        for offset in range(12):
            rotated = word[offset:] + word[:offset]
            require(reader_omega(rotated) == base, "falla rotación dodecafásica")
            require(reader_omega(tuple(reversed(rotated))) == base, "falla reflexión")
        require(
            reader_omega(tuple(-value for value in reversed(word))) == base,
            "falla involución C_M",
        )
    cocycle_checks = 0
    for left in realized_taus:
        for right in realized_taus:
            for third in realized_taus:
                require(
                    polar(left, right) + polar(add(left, right), third)
                    == polar(right, third) + polar(left, add(right, third)),
                    "falla identidad de 2-cociclo",
                )
                cocycle_checks += 1

    # El registro 81x108 recompone las rutas de orientación positiva.
    by_cell: dict[int, list[tuple[int, int]]] = collections.defaultdict(list)
    for row in ledger_rows:
        by_cell[int(row["cell_id"])].append((int(row["t"]), int(row["trit"])))
    require(set(by_cell) == set(range(1, 82)), "IDs de celda fuera de 1..81")
    for cell, entries in by_cell.items():
        ticks = [tick for tick, _ in entries]
        require(len(ticks) == 108, f"celda {cell} sin 108 pasos")
        require(set(ticks) == set(range(1, 109)), f"pasos no únicos en celda {cell}")
    values_d_81 = {
        cell: reader_d(tuple(value for _, value in sorted(entries)))
        for cell, entries in by_cell.items()
    }
    require(len(values_d_81) == 81, "recomposición del registro incompleta")
    reversed_by_cell: dict[int, list[tuple[int, int]]] = collections.defaultdict(list)
    for row in reversed(ledger_rows):
        reversed_by_cell[int(row["cell_id"])].append((int(row["t"]), int(row["trit"])))
    values_d_reversed = {
        cell: reader_d(tuple(value for _, value in sorted(entries)))
        for cell, entries in reversed_by_cell.items()
    }
    require(values_d_reversed == values_d_81, "la permutación de filas altera K_D")

    transductor = {int(row["cell_id"]): row for row in transductor_rows}
    require(len(transductor) == 81, "IDs celulares no únicos")
    require(set(transductor) == set(range(1, 82)), "transductor fuera de 1..81")
    require(
        len({row["structural_class"] for row in transductor.values()}) == 13,
        "censo de multisecciones distinto de 13",
    )
    values_omega_81 = {
        cell: reader_omega(tau_word(row["tau_B1"]))
        for cell, row in transductor.items()
    }
    require(values_d_81[41] == (80, 54, 6), "celda electrónica CT108 incorrecta")
    require(values_omega_81[41] == (80, 54, 6), "celda electrónica tau incorrecta")

    route_row_by_state = {
        (
            int(row["seed_r"]),
            int(row["seed_c"]),
            int(row["h0"]),
            int(row["v0"]),
        ): row
        for row in route_rows
    }
    ledger_route_joins = 0
    tau_route_joins = 0
    for cell, row in transductor.items():
        state = (
            int(row["r"]),
            int(row["c"]),
            int(row["h0"]),
            int(row["v0"]),
        )
        require(state in route_row_by_state, f"ruta B1 ausente para celda {cell}")
        route_row = route_row_by_state[state]
        candidate = route_row["candidate_id"]
        ledger_word = tuple(value for _, value in sorted(by_cell[cell]))
        require(
            ledger_word == words[candidate],
            f"ledger y gamma_108 divergen en celda {cell}",
        )
        ledger_route_joins += 1
        require(
            tau_word(row["tau_B1"]) == taus[candidate],
            f"tau_B1 y tau de ruta divergen en celda {cell}",
        )
        tau_route_joins += 1
    require(ledger_route_joins == 81, "join ledger-ruta incompleto")
    require(tau_route_joins == 81, "join tau-ruta incompleto")

    central = transductor[41]
    require(
        (
            int(central["r"]),
            int(central["c"]),
            int(central["h0"]),
            int(central["v0"]),
        )
        == (5, 5, 1, 1),
        "la celda central no publica el estado (5,5,++)",
    )
    require(
        route_row_by_state[(5, 5, 1, 1)]["candidate_id"] == electron_id,
        "el identificador electrónico no corresponde a (5,5,++)",
    )

    family_d_b1: dict[str, set[tuple[int, int, int]]] = collections.defaultdict(set)
    family_omega_b1: dict[str, set[tuple[int, int, int]]] = collections.defaultdict(set)
    family_joint_b1: dict[str, set[object]] = collections.defaultdict(set)
    coarse_d_b1: dict[str, set[tuple[int, int, int]]] = collections.defaultdict(set)
    coarse_omega_b1: dict[str, set[tuple[int, int, int]]] = collections.defaultdict(set)
    for cell, row in transductor.items():
        family = row["route_family_R"]
        family_d_b1[family].add(values_d_81[cell])
        family_omega_b1[family].add(values_omega_81[cell])
        family_joint_b1[family].add((values_d_81[cell], values_omega_81[cell]))
        coarse = row["structural_class"]
        coarse_d_b1[coarse].add(values_d_81[cell])
        coarse_omega_b1[coarse].add(values_omega_81[cell])
    require(len(family_d_b1) == 56, "censo de familias distinto de 56")

    coordinate_family = {
        (int(row["r"]), int(row["c"])): row["route_family_R"]
        for row in transductor.values()
    }
    family_d_oriented: dict[str, set[tuple[int, int, int]]] = collections.defaultdict(set)
    family_omega_oriented: dict[str, set[tuple[int, int, int]]] = collections.defaultdict(set)
    family_joint_oriented: dict[str, set[object]] = collections.defaultdict(set)
    for row in route_rows:
        candidate = row["candidate_id"]
        family = coordinate_family[(int(row["seed_r"]), int(row["seed_c"]))]
        family_d_oriented[family].add(values_d[candidate])
        family_omega_oriented[family].add(values_omega[candidate])
        family_joint_oriented[family].add((values_d[candidate], values_omega[candidate]))

    profiles_d = set(values_d.values())
    profiles_omega = set(values_omega.values())
    coincidences = sum(
        values_d[candidate] == values_omega[candidate] for candidate in words
    )
    coincidence_values = {
        values_d[candidate]
        for candidate in words
        if values_d[candidate] == values_omega[candidate]
    }
    joint_profiles = set(
        (values_d[candidate], values_omega[candidate]) for candidate in words
    )
    joint_distribution_counter = collections.Counter(
        (values_d[candidate], values_omega[candidate]) for candidate in words
    )
    joint_distribution = [
        {
            "K_D": list(pair[0]),
            "K_Omega": list(pair[1]),
            "multiplicity": joint_distribution_counter[pair],
        }
        for pair in sorted(joint_distribution_counter)
    ]
    require(len(profiles_d) == 14, "K_D no produce 14 perfiles")
    require(len(profiles_omega) == 9, "K_Omega no produce 9 perfiles")
    require(coincidences == 18, "coincidencia global distinta de 18/324")
    require(coincidence_values == {(80, 54, 6)}, "la coincidencia no es únicamente electrónica")
    require(len(joint_profiles) == 40, "el par de lectores no produce 40 perfiles")
    require(
        profile_cardinalities(family_d_b1) == {"1": 41, "2": 11, "3": 2, "4": 2},
        "partición familiar B1 de K_D inesperada",
    )
    require(
        profile_cardinalities(family_omega_b1) == {"1": 50, "2": 6},
        "partición familiar B1 de K_Omega inesperada",
    )
    require(
        profile_cardinalities(family_joint_b1)
        == {"1": 41, "2": 11, "3": 2, "4": 1, "5": 1},
        "partición familiar B1 del par inesperada",
    )
    require(
        profile_cardinalities(family_d_oriented)
        == {"2": 41, "3": 2, "4": 10, "6": 3},
        "partición familiar orientada de K_D inesperada",
    )
    require(
        profile_cardinalities(family_omega_oriented)
        == {"1": 17, "2": 34, "3": 5},
        "partición familiar orientada de K_Omega inesperada",
    )
    require(
        profile_cardinalities(family_joint_oriented)
        == {"2": 41, "3": 1, "4": 10, "5": 1, "6": 1, "7": 1, "8": 1},
        "partición familiar orientada del par inesperada",
    )

    cells_by_multisection: dict[str, list[int]] = collections.defaultdict(list)
    for cell, row in transductor.items():
        cells_by_multisection[row["structural_class"]].append(cell)
    require(len(cells_by_multisection) == 13, "faltan multisecciones B1")
    multisection_payload: dict[str, object] = {}
    for name, cells in sorted(cells_by_multisection.items()):
        size = len(cells)
        multisection_payload[name] = {
            "rank_B1": size,
            "K_D_normalized_trace": [
                rational_string(sum(values_d_81[cell][index] for cell in cells), size)
                for index in range(3)
            ],
            "K_Omega_normalized_trace": [
                rational_string(sum(values_omega_81[cell][index] for cell in cells), size)
                for index in range(3)
            ],
            "K_D_spectrum": spectrum(values_d_81[cell] for cell in cells),
            "K_Omega_spectrum": spectrum(values_omega_81[cell] for cell in cells),
        }

    payload: dict[str, object] = {
        "schema": "hmt.mass_bidirectional_readers.rev11.v1",
        "epistemic_status": {
            "route_readers": "FORMALIZACION_NUEVA_EXACTO_INTERNO",
            "electron_reduction": "EXACTO_INTERNO_INDEPENDIENTE_DE_VALORES_OBJETIVO",
            "global_physical_selection": "OPEN_NO_SELECTION_THEOREM",
            "null_sector": "SCOPE_DECLARATION_OUTSIDE_POSITIVE_CHARACTER",
        },
        "inputs": {
            "allowlist": sorted(OPENED),
            "opened_files": sorted(OPENED),
            "forbidden_opened": [],
            "mass_pdg_codata_files_opened": 0,
            "routes_324_sha256": routes_hash,
            "ledger_81x108_sha256": ledger_hash,
            "transductor_81_sha256": transductor_hash,
        },
        "domain": {
            "routes": 324,
            "cells": 81,
            "families": 56,
            "multisections": 13,
        },
        "electron": {
            "route": electron_id,
            "route_state": [5, 5, 1, 1],
            "displacements": electron_displacements,
            "K_D": list(values_d[electron_id]),
            "K_Omega": list(values_omega[electron_id]),
            "sheet_ablations": {
                key: list(value) for key, value in electron_ablations.items()
            },
        },
        "K_D": {
            "profiles": len(profiles_d),
            "distribution": distribution(values_d.values()),
            "B1_family_profile_cardinalities": profile_cardinalities(family_d_b1),
            "B1_refined_classes": sum(map(len, family_d_b1.values())),
            "oriented_family_profile_cardinalities": profile_cardinalities(
                family_d_oriented
            ),
            "oriented_refined_classes": sum(map(len, family_d_oriented.values())),
            "B1_structural_class_profile_counts": {
                key: len(value) for key, value in sorted(coarse_d_b1.items())
            },
            "naturality_checks": {
                "C108_reversal_S3_routes": 324,
                "period_54_routes": 324,
                "simultaneous_orientation_inversion_shift_27_routes": 324,
                "ledger_row_permutation": "PASS",
                "ledger_to_route_joins": ledger_route_joins,
            },
        },
        "K_Omega": {
            "profiles": len(profiles_omega),
            "distribution": distribution(values_omega.values()),
            "B1_family_profile_cardinalities": profile_cardinalities(
                family_omega_b1
            ),
            "B1_refined_classes": sum(map(len, family_omega_b1.values())),
            "oriented_family_profile_cardinalities": profile_cardinalities(
                family_omega_oriented
            ),
            "oriented_refined_classes": sum(map(len, family_omega_oriented.values())),
            "B1_structural_class_profile_counts": {
                key: len(value) for key, value in sorted(coarse_omega_b1.items())
            },
            "naturality_checks": {
                "D12_CM_words": len(realized_taus),
                "polar_cocycle_identities": cocycle_checks,
                "full_pair_Omega_P6_checked": True,
                "window_energy_identity_words": len(realized_taus),
                "tau_to_route_joins": tau_route_joins,
            },
        },
        "joint": {
            "routewise_equal": coincidences,
            "routewise_unequal": 324 - coincidences,
            "coincidence_profile": [80, 54, 6],
            "joint_profiles": len(joint_profiles),
            "joint_distribution": joint_distribution,
            "joint_distribution_sha256": canonical_hash(joint_distribution),
            "B1_family_profile_cardinalities": profile_cardinalities(family_joint_b1),
            "B1_refined_classes": sum(map(len, family_joint_b1.values())),
            "oriented_family_profile_cardinalities": profile_cardinalities(
                family_joint_oriented
            ),
            "oriented_refined_classes": sum(map(len, family_joint_oriented.values())),
            "global_equivalence": False,
        },
        "multisections_B1": multisection_payload,
        "gates": [
            "PASS_DOMINIO_81_56_13_324",
            "PASS_DOS_LECTORES_INDEPENDIENTES_DE_VALORES_OBJETIVO",
            "PASS_REDUCCION_ELECTRONICA_80_54_6",
            "PASS_PERFILES_14_9_COINCIDENCIA_18_PARES_40",
            "PASS_DESCENSOS_TIPADOS_B1_Y_ORIENTADOS",
            "PASS_PERIODICIDAD_INVERSION_Y_ABLACION_DE_HOJAS",
            "PASS_JOINS_LEDGER_RUTA_TAU_81",
            "PASS_IDENTIDAD_ENERGIAS_CORRELACIONES_19",
            "SCOPE_SECTOR_NULO_FUERA_DEL_DOMINIO_POSITIVO",
        ],
    }
    payload["payload_sha256"] = canonical_hash(payload)
    return payload


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--certificate",
        type=Path,
        default=None,
        help="escribe el certificado JSON en esta ruta; sin opción sólo imprime",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parse_args(argv)
    payload = build_certificate()
    rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if arguments.certificate is not None:
        output = arguments.certificate
        if not output.is_absolute():
            output = ROOT / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
