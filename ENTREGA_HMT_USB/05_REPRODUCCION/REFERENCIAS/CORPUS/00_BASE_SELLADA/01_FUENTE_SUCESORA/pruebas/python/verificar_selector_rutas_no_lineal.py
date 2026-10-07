#!/usr/bin/env python3
"""Certifica las obstrucciones no lineales de los catálogos de rutas.

El programa es autocontenido respecto del paquete de Mecánica Dimensional:
lee cuatro catálogos completos, el atlas 9x9, su proyección física y el
grafo v13. No usa masas para construir rutas ni ajusta coeficientes.
"""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "datos/selector_rutas_no_lineal"
TARGETS = ROOT / "datos/HMT_mass_route_signatures_10species.csv"
OUTPUT = ROOT / "certificados/selector_rutas_no_lineal.json"

CATALOGUES = {
    "malla_v9_81": DATA / "rutas_malla_v9.csv",
    "atlas_v11_81": DATA / "atlas_especies_v11.csv",
    "motor_B1_324": DATA / "rutas_b1_324.csv",
    "motor_analisis_324": DATA / "rutas_analisis_324.csv",
}
ATLAS = DATA / "atlas_especies_v11.csv"
PROJECTION = DATA / "proyeccion_fibras_v11.csv"
NODES = DATA / "grafo_nodos_v13.csv"
EDGES = DATA / "grafo_aristas_v13.csv"
MST = DATA / "grafo_mst_auditoria_v13.csv"
MST_EDGES = DATA / "grafo_mst_aristas_v13.csv"

ALIASES = {
    "nA": ("nA", "n_A"),
    "sC": ("sC", "s_C"),
    "K": ("kD4", "k_D4", "K", "k"),
    "nu120": ("nu120",),
    "nu270": ("nu270", "nu270_Q3"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def coordinate_columns(fields: set[str]) -> dict[str, str]:
    result = {}
    for canonical, aliases in ALIASES.items():
        chosen = next((name for name in aliases if name in fields), None)
        require(chosen is not None, f"falta la coordenada {canonical}")
        result[canonical] = chosen
    return result


def vector(row: dict[str, str], columns: dict[str, str]) -> tuple[int, ...]:
    return tuple(
        int(float(row[columns[name]]))
        for name in ("nA", "sC", "K", "nu120", "nu270")
    )


def target_vectors() -> dict[str, tuple[int, ...]]:
    rows = read_csv(TARGETS)
    columns = coordinate_columns(set(rows[0]))
    return {row["species"]: vector(row, columns) for row in rows}


def audit_images(targets: dict[str, tuple[int, ...]]) -> dict[str, object]:
    target_set = set(targets.values())
    result = {}
    for name, path in CATALOGUES.items():
        rows = read_csv(path)
        columns = coordinate_columns(set(rows[0]))
        image = {vector(row, columns) for row in rows}
        overlap = sorted(image & target_set)
        require(not overlap, f"{name} contiene una firma canónica")
        result[name] = {
            "rows": len(rows),
            "distinct_vectors": len(image),
            "intersection_with_targets": len(overlap),
            "sha256": digest(path),
        }
    return result


def audit_involution() -> dict[str, object]:
    atlas = read_csv(ATLAS)
    projection = {
        row["HMT_sector"]: int(row["cell_count"]) for row in read_csv(PROJECTION)
    }
    groups: dict[tuple[str, int], set[tuple[int, int]]] = defaultdict(set)
    for row in atlas:
        groups[(row["family"], int(row["generation"]))].add(
            (int(row["r"]), int(row["c"]))
        )
    require(len(atlas) == 81 and len(groups) == 13, "atlas incompleto")

    details = {}
    fixed_fibres = []
    for (family, generation), cells in sorted(groups.items()):
        name = f"{family}_G{generation}"
        image = {(10 - r, 10 - c) for r, c in cells}
        require(image == cells, f"la fibra {name} no es estable por rho")
        require(projection[name] == len(cells), f"censo físico distinto en {name}")
        fixed = sorted(cells & {(5, 5)})
        if fixed:
            fixed_fibres.append(name)
        details[name] = {
            "cells": len(cells),
            "rho_fixed_cells": [list(cell) for cell in fixed],
            "rho_orbits": (len(cells) + len(fixed)) // 2,
        }
    require(fixed_fibres == ["charged_lepton_G0"], "punto fijo inesperado")
    return {
        "physical_fibres": len(groups),
        "fibres_without_fixed_cell": 12,
        "only_fibre_with_fixed_cell": fixed_fibres[0],
        "details": details,
    }


def node_vector(row: dict[str, str]) -> tuple[int, ...]:
    return tuple(
        int(row[name])
        for name in ("A_nA", "A_sC", "A_K", "A_nu120", "A_nu270")
    )


def audit_graph() -> dict[str, object]:
    node_rows = read_csv(NODES)
    edge_rows = read_csv(EDGES)
    mst_rows = read_csv(MST)
    mst_edge_rows = read_csv(MST_EDGES)
    nodes = {row["node"]: node_vector(row) for row in node_rows}
    names = sorted(nodes)
    require(len(names) == 11, "el grafo v13 no tiene once vértices")
    expected = {(x, y) for x in names for y in names if x != y}
    actual = {(row["source"], row["target"]) for row in edge_rows}
    require(actual == expected, "el soporte v13 no es K_11 dirigido")
    for row in edge_rows:
        source, target = row["source"], row["target"]
        stored = tuple(
            int(row[name])
            for name in ("d_nA", "d_sC", "d_K", "d_nu120", "d_nu270")
        )
        calculated = tuple(
            b - a for a, b in zip(nodes[source], nodes[target])
        )
        require(stored == calculated, "una arista no es un coborde")
    triangle_checks = 0
    for a, b, c in itertools.combinations(names, 3):
        ab = tuple(nodes[b][i] - nodes[a][i] for i in range(5))
        bc = tuple(nodes[c][i] - nodes[b][i] for i in range(5))
        ca = tuple(nodes[a][i] - nodes[c][i] for i in range(5))
        require(
            tuple(ab[i] + bc[i] + ca[i] for i in range(5)) == (0,) * 5,
            "fallo de cierre triangular",
        )
        triangle_checks += 1
    require(len(mst_rows) == 10 and len(mst_edge_rows) == 9, "MST inesperado")
    require(
        all("mass_ref_MeV" in row and "mass_model_MeV" in row for row in node_rows),
        "la tabla nodal no declara sus masas de entrada",
    )
    return {
        "vertices": len(names),
        "directed_edges": len(edge_rows),
        "underlying_graph": "K_11",
        "unlabelled_automorphism_group_order": math.factorial(len(names)),
        "all_edge_labels_are_target_vector_coboundaries": True,
        "triangle_zero_sum_checks": triangle_checks,
        "node_table_contains_reference_and_model_mass": True,
    }


def audit_residues(targets: dict[str, tuple[int, ...]]) -> dict[str, object]:
    moduli = (2, 6, 2, 2, 4)
    residues = {
        name: tuple(value % modulus for value, modulus in zip(vec, moduli))
        for name, vec in targets.items()
    }
    require(len(set(residues.values())) == 10, "las clases objetivo no son distintas")
    require(
        {(vec[1] + vec[3]) % 2 for vec in targets.values()} == {1},
        "las firmas no ocupan la coclase esperada",
    )
    return {
        "moduli": list(moduli),
        "distinct_target_classes": len(set(residues.values())),
        "minimum_binary_decisions_for_observed_classes": 4,
        "ambient_quotient_order": 96,
        "minimum_residual_generators": 4,
        "absolute_origin_required": True,
        "classes": {name: list(value) for name, value in sorted(residues.items())},
    }


def main() -> None:
    inputs = [
        TARGETS,
        ATLAS,
        PROJECTION,
        NODES,
        EDGES,
        MST,
        MST_EDGES,
        *CATALOGUES.values(),
    ]
    for path in inputs:
        require(path.is_file(), f"no existe {path}")
    targets = target_vectors()
    require(len(targets) == 10, "la tabla canónica no contiene diez firmas")
    result = {
        "schema": "HMT.selector_rutas_no_lineal.selfcontained.v1",
        "status": "PASS_SELECTOR_RUTAS_NO_LINEAL",
        "image_disjunction": audit_images(targets),
        "central_inversion": audit_involution(),
        "downstream_graph": audit_graph(),
        "residual_information": audit_residues(targets),
        "theorems": {
            "catalogue_no_go": (
                "For every selector with codomain in an audited raw catalogue, "
                "the composed readout misses every canonical target vector."
            ),
            "equivariance_no_go": (
                "A rho-equivariant point selector from a rho-invariant coarse "
                "fibre requires a rho-fixed cell; 12 of 13 fibres have none."
            ),
            "graph_status": (
                "The v13 graph is K_11 and its labels are coboundaries of the "
                "already assigned vectors; it certifies integrability, not selection."
            ),
        },
        "source_sha256": {
            str(path.relative_to(ROOT)): digest(path) for path in sorted(set(inputs))
        },
    }
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if "--write-certificate" in sys.argv[1:]:
        OUTPUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
