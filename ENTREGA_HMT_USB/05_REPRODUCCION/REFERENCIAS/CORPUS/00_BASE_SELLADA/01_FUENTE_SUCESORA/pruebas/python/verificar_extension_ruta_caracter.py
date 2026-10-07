#!/usr/bin/env python3
"""Certifica el descenso extensión–ruta–firma y la retícula angular.

El verificador usa sólo las cuatro tablas incluidas en la publicación. No
abre masas, firmas objetivo ni etiquetas físicas durante la selección.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from fractions import Fraction
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "datos"
FILES = {
    "transductor": DATA / "transductor_rutas_81.csv",
    "selector": DATA / "selector_interno_81_celdas.csv",
    "multisecciones": DATA / "multisecciones_hmt_13_tipos.csv",
    "periodo54": DATA / "obstrucciones_periodo54.csv",
}
EXPECTED_HASHES = {
    "transductor": "8c53ce492adbf147b51c56625df24df6e788831603a19e242f548aa713369261",
    "selector": "b837ed390a86d46aae785a3c87d7c8f9cd8c5e6fc2fe15e87e9c4e70f3f477be",
    "multisecciones": "ace1718bc023e5cf43f80233aa9adf22d882ba5059c3530ada422b6c31d9267e",
    "periodo54": "cf04ac0d7ecdde8060cfc6cd5b5f55b116da21729d19a47eab36918316c99a61",
}
STEP4 = ((0, 4, 8), (1, 5, 9), (2, 6, 10), (3, 7, 11))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"FAIL_EXTENSION_RUTA_CARACTER: {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def ints(value: str) -> tuple[int, ...]:
    return tuple(int(item) for item in value.split(","))


def sign(value: int) -> int:
    return int(value > 0) - int(value < 0)


def as_bool(value: str) -> bool:
    require(value in ("True", "False"), f"booleano inválido: {value}")
    return value == "True"


def reconstruct(total: int, relative: tuple[int, ...], anti: tuple[int, ...]) -> tuple[int, ...]:
    require(len(relative) == 5 and len(anti) == 6, "coordenadas 1+5+6")
    numerator = total - sum(relative)
    require(numerator % 6 == 0, "divisibilidad por seis")
    p5 = numerator // 6
    pair = tuple(p5 + value for value in relative) + (p5,)
    require(all((pair[i] + anti[i]) % 2 == 0 for i in range(6)), "paridad 1+5+6")
    return tuple((pair[i] + anti[i]) // 2 for i in range(6)) + tuple(
        (pair[i] - anti[i]) // 2 for i in range(6)
    )


def main() -> None:
    hashes = {name: sha256(path) for name, path in FILES.items()}
    require(hashes == EXPECTED_HASHES, "huella de una tabla incorporada")

    table = rows(FILES["transductor"])
    selector = rows(FILES["selector"])
    multisections = rows(FILES["multisecciones"])
    obstructions = rows(FILES["periodo54"])

    require(len(table) == 81, "el transductor no contiene 81 celdas")
    require(len(selector) == 81, "el selector no contiene 81 celdas")
    require(len(multisections) == 13, "no hay trece tipos gruesos")
    require(len(obstructions) == 10, "no hay diez controles de periodo 54")
    require(len({row["cell_id"] for row in table}) == 81, "cell_id repetido")
    require(len({(row["r"], row["c"]) for row in table}) == 81, "celda repetida")

    route_sizes = Counter(row["route_family_R"] for row in table)
    fibre_histogram = Counter(route_sizes.values())
    require(len(route_sizes) == 56, "número de familias de ruta")
    require(fibre_histogram == Counter({1: 41, 2: 10, 3: 2, 4: 1, 5: 2}), "histograma de fibras")
    require({int(row["kappa_minimal_memory"]) for row in table} == set(range(5)), "alfabeto kappa")
    require(
        len({(row["route_family_R"], row["kappa_minimal_memory"]) for row in table}) == 81,
        "(R,kappa) no es inyectivo",
    )
    require(len({row["internal_species_key"] for row in table}) == 81, "clave interna no inyectiva")
    require(all(row["physical_label"] == "NOT_READ_NOT_USED" for row in table), "etiqueta física leída")
    require(
        all(row["unit_status"] == "DIMENSIONLESS_NO_UNIT_ATTACHED" for row in table),
        "unidad introducida en el extractor",
    )

    selector_by_cell = {(row["r"], row["c"]): row for row in selector}
    require(len(selector_by_cell) == 81, "selector celular duplicado")

    disagreements = 0
    for row in table:
        events = ints(row["events_B1"])
        relative = ints(row["M5"])
        anti = ints(row["A6"])
        require(len(events) == 12, f"doce eventos en celda {row['cell_id']}")
        require(
            reconstruct(int(row["sC_B1_even"]), relative, anti) == events,
            f"reconstrucción 1+5+6 en celda {row['cell_id']}",
        )

        tau = tuple(sign(value) for value in events)
        nu_event = sum(sign(sum(events[index] for index in cycle)) for cycle in STEP4)
        nu_sign = sum(sign(sum(tau[index] for index in cycle)) for cycle in STEP4)
        nu270 = sum(tau[index] * tau[(index + 3) % 12] for index in range(12))
        require(nu_event == int(row["nu120_event_B1"]), "nu120 ponderado")
        require(nu_sign == int(row["nu120_sign_B1"]), "nu120 de signos")
        require(nu270 == int(row["nu270_B1"]), "nu270")
        disagreements += int(nu_event != nu_sign)

        n_action = int(row["nA_B1_parity"])
        s_charge = int(row["sC_B1_even"])
        w_plus = int(row["Wplus_B1"])
        w_minus = int(row["Wminus_B1"])
        require(w_plus == 6 * n_action + s_charge, "W+")
        require(w_minus == 6 * n_action - s_charge, "W-")
        # Verificación exacta de los coeficientes del exponente en la
        # factorización (q_+^-W+ q_-^-W-)^(1/12).
        require(Fraction(w_plus + w_minus, 12) == n_action, "coeficiente angular A")
        require(Fraction(w_plus - w_minus, 12) == Fraction(s_charge, 6), "coeficiente C*")
        require((w_plus + w_minus) % 12 == 0, "imagen de la retícula")

        require(
            int(row["kDelta4_F025"])
            == int(row["torsion_total_F025"]) - 2 * int(row["torsion_corona_F025"]),
            "cocadena torsional de predecesor par",
        )
        require(
            int(row["kDelta4_prospectivo04"])
            == int(row["torsion_total_prospectivo04"])
            - 2 * int(row["torsion_corona_prospectivo04"]),
            "cocadena torsional de control",
        )

        cell = selector_by_cell[(row["r"], row["c"])]
        route_key = "|".join(
            (
                cell["nA"], cell["sC"], cell["kD4"], cell["nu120_ruta"],
                cell["nu270_ruta"], cell["tau12"],
            )
        )
        require(route_key == row["route_family_R"], "empalme selector–familia por celda")
        require(cell["indice_memoria_minimo"] == row["kappa_minimal_memory"], "kappa por celda")

    require(disagreements == 25, "se colapsaron los dos observables nu120")

    matrix = ((6, 1), (6, -1))
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    entry_gcd = 0
    for matrix_row in matrix:
        for value in matrix_row:
            entry_gcd = gcd(entry_gcd, abs(value))
    require(determinant == -12 and entry_gcd == 1, "divisores invariantes (1,12)")

    point_types = [row for row in multisections if as_bool(row["selector_puntual_rho_equivariante"])]
    require(len(point_types) == 1, "número de tipos con selector puntual")
    require(point_types[0]["tipo_hmt_grueso"] == "charged_lepton_G0", "tipo central")
    require(point_types[0]["celdas_fijas_por_rho"] == "(5,5)", "centro fijo")

    obstructed_species: list[str] = []
    for row in obstructions:
        n_even = int(row["nA"]) % 2 == 0
        s_even = int(row["sC"]) % 2 == 0
        nu_four = int(row["nu270"]) % 4 == 0
        require(n_even == as_bool(row["nA_even_required"]), "congruencia nA")
        require(s_even == as_bool(row["sC_even_required"]), "congruencia sC")
        require(nu_four == as_bool(row["nu270_multiple_4_required"]), "congruencia nu270")
        require(not (n_even and s_even and nu_four), "firma admitida por periodo 54")
        require(row["violations"], "falta testigo de obstrucción")
        require(as_bool(row["proxy_K_comparison_forbidden"]), "se mezcló K proxy con k fuerte")
        obstructed_species.append(row["species"])

    result = {
        "schema": "HMT.MD.extension-ruta-caracter.v1",
        "status": "PASS_EXTENSION_ROUTE_CHARACTER",
        "canonical_revision": "2026-07-22.2",
        "input_hashes": hashes,
        "selector_internal": {
            "cells": 81,
            "route_families": 56,
            "fibre_size_distribution": {str(key): fibre_histogram[key] for key in sorted(fibre_histogram)},
            "maximum_fibre": 5,
            "kappa_alphabet": [0, 1, 2, 3, 4],
            "R_kappa_injective": True,
            "minimal_alphabet_cardinality": 5,
            "uses_mass_targets": False,
            "uses_physical_labels": False,
        },
        "dodecaphase_ledger": {
            "event_coordinates": "1+5+6=12",
            "all_81_event_records_reconstructed": True,
            "nu120_event_vs_sign_disagreements": disagreements,
            "torsion_formula": "k_Delta4=T-2*C",
        },
        "angular_lattice": {
            "matrix": [[6, 1], [6, -1]],
            "determinant": determinant,
            "smith_invariants": [1, 12],
            "two_way_factorization_checked_on_81_records": True,
        },
        "coarse_multisections": {
            "types": len(multisections),
            "point_selector_types": 1,
            "unique_fixed_type": point_types[0]["tipo_hmt_grueso"],
            "unique_fixed_cell": "(5,5)",
        },
        "period54_no_go": {
            "tested_signatures": len(obstructions),
            "all_obstructed": True,
            "species": sorted(obstructed_species),
            "scope": "reduced period-54 engine; not the enriched TPK dynamics",
        },
        "typed_scope": {
            "proved": [
                "internal cell selector (R,kappa) relative to the declared atlas and order",
                "exact reconstruction of the twelve event ledger",
                "tick-level torsion and distinct level-120 observables",
                "index-12 two-way angular factorization",
                "route-to-signature-to-dimensionless-character interface",
                "period-54 obstruction for the ten published signatures",
            ],
            "physical_realization_not_inferred": "physical species -> enriched survivor extension",
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
