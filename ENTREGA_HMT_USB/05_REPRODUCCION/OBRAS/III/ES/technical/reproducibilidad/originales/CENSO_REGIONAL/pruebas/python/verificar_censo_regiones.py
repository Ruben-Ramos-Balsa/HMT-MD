#!/usr/bin/env python3
"""Certifica el censo de regiones, rutas repetidas y grafo de bloques."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
from collections import Counter, defaultdict, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "datos/TPK_U_catalog_468.json"
ROUTE_CATALOG = ROOT / "datos/hmt_u_route_catalog_full.csv"
OUTPUT = ROOT / "certificados/censo_regiones_grafo.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_u6(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split("|"))


def psi(u6: tuple[int, ...]) -> str:
    return "".join(str((-value) % 3) for value in u6)


def components(graph: dict[tuple[int, ...], set[tuple[int, ...]]]) -> list[list[tuple[int, ...]]]:
    unseen = set(graph)
    result: list[list[tuple[int, ...]]] = []
    while unseen:
        start = min(unseen)
        queue = deque([start])
        unseen.remove(start)
        component: list[tuple[int, ...]] = []
        while queue:
            node = queue.popleft()
            component.append(node)
            for other in graph[node]:
                if other in unseen:
                    unseen.remove(other)
                    queue.append(other)
        result.append(sorted(component))
    return sorted(result, key=lambda comp: (-len(comp), comp))


def main() -> None:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = []
    for item in data:
        u6 = parse_u6(item["U6"])
        entries.append({**item, "u6_tuple": u6, "psi": psi(u6)})

    multiplicity_distribution = Counter(int(item["count"]) for item in entries)
    weighted_total = sum(int(item["count"]) for item in entries)

    fibers = {}
    for name, word in {"pi": "010211", "e": "201101", "phi": "121200"}.items():
        fiber = [item for item in entries if item["psi"] == word]
        fibers[name] = [
            {
                "U6": list(item["u6_tuple"]),
                "multiplicity": int(item["count"]),
                "energy_signature": item["Esig"],
                "diag_c": int(item["diag_c"]),
                "heading_type": item["hplus_type"],
                "px_size": int(item["px_size"]),
            }
            for item in fiber
        ]

    expected_pi = {
        (501, 614, 498, 169, 272, 272),
        (810, 923, 870, 169, 272, 272),
        (810, 983, 810, 169, 272, 272),
        (870, 923, 810, 169, 272, 272),
        (870, 923, 810, 418, 674, 521),
    }
    actual_pi = {tuple(item["U6"]) for item in fibers["pi"]}

    route_rows = []
    with ROUTE_CATALOG.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            values = tuple(int(value) for value in ast.literal_eval(row["U"]))
            route_rows.append(values)
    repeated_u12 = sum(1 for values in route_rows if values[:6] == values[6:])
    route_u6 = {values[:6] for values in route_rows}
    catalogue_u6 = {item["u6_tuple"] for item in entries}

    graph: dict[tuple[int, ...], set[tuple[int, ...]]] = defaultdict(set)
    for item in entries:
        a = item["u6_tuple"][:3]
        b = item["u6_tuple"][3:]
        graph[a].add(b)
        graph[b].add(a)
    comps = components(graph)

    canonical_cycle = [
        (830, 943, 830),
        (109, 252, 252),
        (810, 923, 870),
        (169, 272, 272),
        (850, 963, 890),
        (149, 252, 212),
    ]
    cycle_edges = []
    for index, left in enumerate(canonical_cycle):
        right = canonical_cycle[(index + 1) % len(canonical_cycle)]
        cycle_edges.append({"left": list(left), "right": list(right), "present": right in graph[left]})

    checks = {
        "catalogue_has_468_U6": len(entries) == 468,
        "weighted_seed_total_is_104976": weighted_total == 104_976,
        "multiplicity_distribution_is_432_18_18": multiplicity_distribution == Counter({144: 432, 432: 18, 1944: 18}),
        "pi_fiber_has_five_regions": len(fibers["pi"]) == 5,
        "pi_fiber_matches_current_vectors": actual_pi == expected_pi,
        "pi_multiplicities_are_432_144x4": sorted(item["multiplicity"] for item in fibers["pi"]) == [144, 144, 144, 144, 432],
        "e_fiber_is_singleton": len(fibers["e"]) == 1,
        "phi_fiber_is_singleton": len(fibers["phi"]) == 1,
        "route_catalogue_has_468_U12": len(route_rows) == 468,
        "minimal_U12_repeats_U6": repeated_u12 == 468,
        "U6_sets_agree_between_catalogues": route_u6 == catalogue_u6,
        "block_graph_has_96_nodes": len(graph) == 96,
        "block_graph_components_are_28_28_28_4_4_4": sorted(len(comp) for comp in comps) == [4, 4, 4, 28, 28, 28],
        "pi_e_phi_cycle_is_present": all(edge["present"] for edge in cycle_edges),
    }

    result = {
        "schema": "HMT.censo_regiones.v1",
        "status": "RESULTADOS_FINITOS_VERIFICADOS",
        "source_hashes": {
            CATALOG.relative_to(ROOT).as_posix(): sha256(CATALOG),
            ROUTE_CATALOG.relative_to(ROOT).as_posix(): sha256(ROUTE_CATALOG),
        },
        "catalogue": {
            "distinct_U6": len(entries),
            "weighted_seed_total": weighted_total,
            "multiplicity_distribution": {str(key): value for key, value in sorted(multiplicity_distribution.items())},
        },
        "fibers": fibers,
        "minimal_U12": {
            "rows": len(route_rows),
            "rows_equal_U6_concat_U6": repeated_u12,
            "typing_warning": "This minimal repeated U12 is not the complete signed dodecaphase state.",
        },
        "block_graph": {
            "nodes": len(graph),
            "component_sizes": [len(comp) for comp in comps],
            "cycle": cycle_edges,
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
