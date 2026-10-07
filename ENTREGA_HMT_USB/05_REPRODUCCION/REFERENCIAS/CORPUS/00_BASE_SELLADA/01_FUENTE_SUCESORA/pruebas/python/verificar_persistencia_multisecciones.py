#!/usr/bin/env python3
"""Certifica la persistencia finita de las multisecciones del atlas 9 x 9.

El dominio es exclusivamente el atlas activo de 81 celdas. La prueba enumera
las fibras de ruta, la involucion rho, el unico centro fijo, la anti-seccion
de palabras triticas y el observable de color. No usa masas ni etiquetas
metrologicas como entradas.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from itertools import product
from pathlib import Path


ARTICLE_ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ARTICLE_ROOT / "datos" / "atlas_especies_81_celdas_v11_rescate_tipado.csv"
CSV_RELATIVE_PATH = (
    "PUBLICACION_HMT/ARTICULO_NUCLEO_HMT_2026-07-22/datos/"
    "atlas_especies_81_celdas_v11_rescate_tipado.csv"
)
EXPECTED_CSV_SHA256 = "cac4f566c41b46781d6846348bb3a0ddc12edd709ed0336a4dd8d282dabf5b83"

ROUTE_FIELDS = ("nA", "sC", "kD4", "nu120", "nu270", "tau12")
EXPECTED_TYPE_SIZES = {
    ("charged_lepton", 0): 1,
    ("charged_lepton", 2): 8,
    ("charged_lepton", 4): 16,
    ("neutrino", 1): 2,
    ("neutrino", 2): 4,
    ("neutrino", 3): 6,
    ("neutrino", 4): 8,
    ("quark_down", 1): 2,
    ("quark_down", 2): 4,
    ("quark_down", 3): 6,
    ("quark_down", 4): 8,
    ("quark_up", 1): 4,
    ("quark_up", 3): 12,
}
EXPECTED_ROUTE_FIBRES = Counter({1: 41, 2: 10, 3: 2, 4: 1, 5: 2})
RESIDUE_TO_COLOR = {0: "R", 1: "G", 2: "B"}
COLOR_NEGATION = {"R": "R", "G": "B", "B": "G"}
TRIT_NEGATION = {"+": "-", "-": "+", "0": "0"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"FAIL_PERSISTENCIA_MULTISECCIONES: {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {
            "cell_id",
            "r",
            "c",
            "sector",
            "family",
            "generation",
            "color_r_minus_c",
            "rho_r",
            "rho_c",
            "rho_family",
            "rho_generation",
            "rho_color_r_minus_c",
            "nA",
            "sC",
            "kD4",
            "nu120",
            "nu270",
            "tau12",
            "CM_tau",
            "CM_tau_exists_as_shape",
        }
        require(reader.fieldnames is not None, "cabecera CSV ausente")
        require(required <= set(reader.fieldnames), "columnas requeridas ausentes")
        return list(reader)


def cell(row: dict[str, str]) -> tuple[int, int]:
    return int(row["r"]), int(row["c"])


def rho_cell(row: dict[str, str]) -> tuple[int, int]:
    return int(row["rho_r"]), int(row["rho_c"])


def coarse_type(row: dict[str, str]) -> tuple[str, int]:
    return row["family"], int(row["generation"])


def route_key(row: dict[str, str]) -> tuple[str, ...]:
    return tuple(row[field] for field in ROUTE_FIELDS)


def cm_tau(word: str) -> str:
    require(len(word) == 12, f"palabra tau no dodecafasica: {word}")
    require(set(word) <= set(TRIT_NEGATION), f"alfabeto tau invalido: {word}")
    return "".join(TRIT_NEGATION[trit] for trit in reversed(word))


def type_name(q_type: tuple[str, int]) -> str:
    return f"{q_type[0]}:G{q_type[1]}"


def main() -> None:
    csv_hash = sha256(CSV_PATH)
    require(csv_hash == EXPECTED_CSV_SHA256, "huella del atlas activo")
    table = load_rows(CSV_PATH)

    require(len(table) == 81, "el atlas no contiene 81 registros")
    require(len({row["cell_id"] for row in table}) == 81, "cell_id repetido")
    require({int(row["cell_id"]) for row in table} == set(range(1, 82)), "cell_id 1..81")

    rows_by_cell = {cell(row): row for row in table}
    full_grid = set(product(range(1, 10), repeat=2))
    require(len(rows_by_cell) == 81, "coordenada celular repetida")
    require(set(rows_by_cell) == full_grid, "el atlas no es la malla 9 x 9 completa")

    route_sizes = Counter(route_key(row) for row in table)
    route_fibre_histogram = Counter(route_sizes.values())
    require(len(route_sizes) == 56, "numero de familias de ruta")
    require(route_fibre_histogram == EXPECTED_ROUTE_FIBRES, "distribucion de fibras de ruta")

    type_sizes = Counter(coarse_type(row) for row in table)
    require(type_sizes == Counter(EXPECTED_TYPE_SIZES), "trece tipos gruesos y sus tamanos")

    fixed_cells: list[tuple[int, int]] = []
    rho_orbits: set[tuple[tuple[int, int], ...]] = set()
    fixed_by_type: Counter[tuple[str, int]] = Counter()
    quark_colors: Counter[str] = Counter()
    quark_rho_pairs: Counter[tuple[str, str]] = Counter()
    tau_words = {row["tau12"] for row in table}
    cm_word_closure = 0
    cm_matches_cellular_rho = 0

    for row in table:
        source = cell(row)
        target = rho_cell(row)
        q_type = coarse_type(row)

        require(target == (10 - source[0], 10 - source[1]), f"formula de rho en {source}")
        require(target in rows_by_cell, f"imagen rho ausente para {source}")
        target_row = rows_by_cell[target]
        require(rho_cell(target_row) == source, f"rho no involutiva en {source}")
        require(coarse_type(target_row) == q_type, f"rho cambia el tipo grueso en {source}")
        require(
            (row["rho_family"], int(row["rho_generation"])) == q_type,
            f"tipo rho declarado incoherente en {source}",
        )

        orbit = tuple(sorted({source, target}))
        rho_orbits.add(orbit)
        if source == target:
            fixed_cells.append(source)
            fixed_by_type[q_type] += 1

        cm_image = cm_tau(row["tau12"])
        cm_is_shape = cm_image in tau_words
        require(cm_is_shape, f"forma CM ausente en el conjunto de palabras para {source}")
        require(
            row["CM_tau_exists_as_shape"] == str(cm_is_shape),
            f"declaracion de clausura CM incoherente en {source}",
        )
        require(row["CM_tau"] == cm_image, f"CM_tau != -rev(tau) en {source}")
        cm_word_closure += int(cm_is_shape)
        cm_matches_cellular_rho += int(cm_image == target_row["tau12"])

        if row["sector"] == "quark":
            residue = (source[0] - source[1]) % 3
            rho_residue = (target[0] - target[1]) % 3
            color = row["color_r_minus_c"]
            rho_color = row["rho_color_r_minus_c"]
            require(color == RESIDUE_TO_COLOR[residue], f"color residual en {source}")
            require(rho_residue == (-residue) % 3, f"rho no niega el residuo en {source}")
            require(rho_color == RESIDUE_TO_COLOR[rho_residue], f"color rho declarado en {source}")
            require(rho_color == COLOR_NEGATION[color], f"rho no niega el color en {source}")
            quark_colors[color] += 1
            quark_rho_pairs[(color, rho_color)] += 1

    require(len(rho_orbits) == 41, "numero de orbitas de rho")
    require(fixed_cells == [(5, 5)], "rho debe tener un unico punto fijo (5,5)")
    require(fixed_by_type == Counter({("charged_lepton", 0): 1}), "tipo del centro fijo")

    # Como rho preserva q=(familia,generacion), un selector puntual
    # rho-equivariante s(q) debe satisfacer rho(s(q))=s(q). Por tanto existe
    # exactamente cuando la fibra q contiene un punto fijo de rho.
    selectable_types = {q_type for q_type in type_sizes if fixed_by_type[q_type] > 0}
    require(selectable_types == {("charged_lepton", 0)}, "selector puntual central unico")
    require(len(type_sizes) - len(selectable_types) == 12, "doce fibras sin selector puntual")
    require(cm_word_closure == 81, "clausura C_M sobre las palabras del atlas")
    require(
        cm_matches_cellular_rho == 49,
        "control de no identificacion entre C_M y la inversion celular rho_c",
    )

    require(quark_colors == Counter({"R": 12, "G": 12, "B": 12}), "balance de color quark")
    require(
        quark_rho_pairs == Counter({("R", "R"): 12, ("G", "B"): 12, ("B", "G"): 12}),
        "accion de rho sobre los colores",
    )

    result = {
        "schema": "HMT.MD.persistencia-multisecciones.v1",
        "status": "PASS_PERSISTENCIA_MULTISECCIONES",
        "canonical_revision": "2026-07-22.2",
        "input": {
            "path": CSV_RELATIVE_PATH,
            "sha256": csv_hash,
        },
        "atlas": {
            "cells": 81,
            "unique_cell_ids": 81,
            "unique_coordinates": 81,
            "route_families": 56,
            "route_fibre_size_distribution": {
                str(size): route_fibre_histogram[size]
                for size in sorted(route_fibre_histogram)
            },
        },
        "coarse_multisections": {
            "types": len(type_sizes),
            "sizes": {
                type_name(q_type): type_sizes[q_type]
                for q_type in sorted(type_sizes)
            },
        },
        "rho": {
            "definition": "rho(r,c)=(10-r,10-c)",
            "involution_verified_cells": 81,
            "preserves_q_family_generation_cells": 81,
            "orbits": len(rho_orbits),
            "fixed_cells": ["(5,5)"],
            "unique_fixed_type": "charged_lepton:G0",
            "rho_equivariant_point_selector_types": 1,
            "noncentral_types_without_rho_equivariant_point_selector": 12,
        },
        "trit_antisection": {
            "rule": "CM_tau=-rev(tau)",
            "verified_cells": 81,
            "word_closure_recomputed_cells": cm_word_closure,
            "matches_cellular_rho_cells": cm_matches_cellular_rho,
            "non_identification_control": "C_M sobre palabras no es rho_c sobre celdas",
        },
        "quark_color": {
            "residue_rule": "color=(r-c) mod 3",
            "residue_dictionary": {"0": "R", "1": "G", "2": "B"},
            "counts": {color: quark_colors[color] for color in sorted(quark_colors)},
            "rho_rule": "color_residue -> -color_residue mod 3",
            "rho_color_action": {color: COLOR_NEGATION[color] for color in sorted(COLOR_NEGATION)},
            "rho_negation_verified_cells": 36,
        },
        "provenance": {
            "architecture": "ARQUITECTURA_AUTORAL_PREEXISTENTE",
            "finite_atlas": "RESULTADO_RECUPERADO",
            "executable_proof": "CERTIFICADO_NUEVO",
        },
        "typed_scope": {
            "proved": "enumeracion exacta del atlas activo y obstruccion rho-equivariant de las doce multisecciones no centrales",
            "not_inferred": "identificacion fisica de una celda concreta dentro de cada multiseccion no central",
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
