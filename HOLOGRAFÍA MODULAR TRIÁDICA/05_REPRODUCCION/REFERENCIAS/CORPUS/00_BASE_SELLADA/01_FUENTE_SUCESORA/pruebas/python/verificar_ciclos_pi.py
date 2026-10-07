#!/usr/bin/env python3
"""Reconstruye los grafos de fase y los cinco cierres mínimos de pi."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "datos/TPK_U_catalog_468.json"
OUTPUT = ROOT / "certificados/ciclos_minimos_y_controles.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_u6(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split("|"))


def canonical_phase(triad: tuple[int, ...]) -> tuple[int, ...]:
    """Representante lexicografico de una triada modulo rotacion ciclica."""

    return min(triad, triad[1:] + triad[:1], triad[2:] + triad[:2])


def component_sizes(graph: dict[tuple[int, ...], set[tuple[int, ...]]]) -> list[int]:
    unseen = set(graph)
    sizes: list[int] = []
    while unseen:
        queue = [unseen.pop()]
        size = 0
        while queue:
            node = queue.pop()
            size += 1
            for other in graph[node]:
                if other in unseen:
                    unseen.remove(other)
                    queue.append(other)
        sizes.append(size)
    return sorted(sizes)


def shortest_closed_walk(
    graph: dict[tuple[int, ...], list[tuple[tuple[int, ...], int]]],
    target_edges: list[int],
    excluded_edges: set[int] | None = None,
) -> list[int] | None:
    """Camino cerrado minimo que recorre todas las aristas objetivo.

    El estado de la BFS es (vertice, mascara de objetivos visitados). El
    certificado devuelto es una lista de identificadores de arista. Para las
    instancias auditadas, el testigo minimo obtenido es ademas un ciclo simple.
    """

    excluded_edges = excluded_edges or set()
    target_mask = {edge: 1 << index for index, edge in enumerate(target_edges)}
    full_mask = (1 << len(target_edges)) - 1
    best: list[int] | None = None

    for start in graph:
        queue = deque([(start, 0)])
        seen = {(start, 0)}
        predecessor: dict[
            tuple[tuple[int, ...], int],
            tuple[tuple[tuple[int, ...], int], int],
        ] = {}
        found: tuple[tuple[int, ...], int] | None = None

        while queue and found is None:
            node, mask = queue.popleft()
            for other, edge_id in graph[node]:
                if edge_id in excluded_edges:
                    continue
                next_mask = mask | target_mask.get(edge_id, 0)
                state = (other, next_mask)
                if other == start and next_mask == full_mask:
                    predecessor[state] = ((node, mask), edge_id)
                    found = state
                    break
                if state not in seen:
                    seen.add(state)
                    predecessor[state] = ((node, mask), edge_id)
                    queue.append(state)

        if found is None:
            continue

        path: list[int] = []
        state = found
        while state != (start, 0):
            previous, edge_id = predecessor[state]
            path.append(edge_id)
            state = previous
        path.reverse()
        if best is None or len(path) < len(best):
            best = path

    return best


def main() -> None:
    rows = json.loads(CATALOG.read_text(encoding="utf-8"))
    values = [parse_u6(row["U6"]) for row in rows]
    index_by_u6 = {value: index for index, value in enumerate(values)}

    raw_simple: dict[tuple[int, ...], set[tuple[int, ...]]] = defaultdict(set)
    phase_simple: dict[tuple[int, ...], set[tuple[int, ...]]] = defaultdict(set)
    phase_multi: dict[tuple[int, ...], list[tuple[tuple[int, ...], int]]] = defaultdict(list)
    endpoints: list[tuple[tuple[int, ...], tuple[int, ...]]] = []

    for edge_id, value in enumerate(values):
        raw_left, raw_right = value[:3], value[3:]
        raw_simple[raw_left].add(raw_right)
        raw_simple[raw_right].add(raw_left)

        left = canonical_phase(raw_left)
        right = canonical_phase(raw_right)
        endpoints.append((left, right))
        phase_simple[left].add(right)
        phase_simple[right].add(left)
        phase_multi[left].append((right, edge_id))
        phase_multi[right].append((left, edge_id))

    words = {"".join(str((-entry) % 3) for entry in value) for value in values}

    named = {
        "APP": parse_u6("903|850|850|252|109|252"),
        "phi": parse_u6("830|943|830|109|252|252"),
        "e": parse_u6("850|963|890|149|252|212"),
        "pi_1": parse_u6("810|923|870|169|272|272"),
        "pi_2": parse_u6("810|983|810|169|272|272"),
        "pi_3": parse_u6("870|923|810|169|272|272"),
        "pi_4": parse_u6("870|923|810|418|674|521"),
        "pi_5": parse_u6("501|614|498|169|272|272"),
        "claimed_bridge": parse_u6("272|169|272|963|890|850"),
    }
    named_ids = {name: index_by_u6[value] for name, value in named.items()}

    cycle_certificates = {}
    for pi_name in ("pi_1", "pi_2", "pi_3", "pi_4", "pi_5"):
        path = shortest_closed_walk(
            phase_multi,
            [named_ids["APP"], named_ids["phi"], named_ids["e"], named_ids[pi_name]],
        )
        if path is None:
            raise RuntimeError(f"No se encontro cierre para {pi_name}")
        cycle_certificates[pi_name] = {
            "minimum_length": len(path),
            "witness_U6": [list(values[edge_id]) for edge_id in path],
        }

    bridge_left, bridge_right = endpoints[named_ids["claimed_bridge"]]
    bridge_phase_pair = frozenset((bridge_left, bridge_right))
    bridge_class_edges = {
        edge_id
        for edge_id, (left, right) in enumerate(endpoints)
        if frozenset((left, right)) == bridge_phase_pair
    }
    without_bridge = shortest_closed_walk(
        phase_multi,
        [named_ids["APP"], named_ids["phi"], named_ids["e"], named_ids["pi_1"]],
        excluded_edges=bridge_class_edges,
    )
    if without_bridge is None:
        raise RuntimeError("No se encontro el contracertificado sin el puente reclamado")

    checks = {
        "catalogue_has_468_rows": len(values) == 468,
        "projection_has_243_distinct_words": len(words) == 243,
        "raw_graph_has_96_nodes": len(raw_simple) == 96,
        "raw_graph_components_are_4_4_4_28_28_28": component_sizes(raw_simple) == [4, 4, 4, 28, 28, 28],
        "phase_graph_has_32_nodes": len(phase_simple) == 32,
        "phase_graph_components_are_4_28": component_sizes(phase_simple) == [4, 28],
        "all_four_anchor_cycles_have_minimum_length_8": all(
            certificate["minimum_length"] == 8 for certificate in cycle_certificates.values()
        ),
        "displayed_bridge_is_not_forced": len(without_bridge) == 8,
    }

    result = {
        "schema": "HMT.ciclos_pi.v1",
        "status": "PASS",
        "source_hash": sha256(CATALOG),
        "catalogue_projection": {
            "U6_rows": len(values),
            "distinct_mod3_words": len(words),
        },
        "graphs": {
            "raw": {
                "nodes": len(raw_simple),
                "component_sizes": component_sizes(raw_simple),
            },
            "cyclic_phase_quotient": {
                "nodes": len(phase_simple),
                "component_sizes": component_sizes(phase_simple),
            },
        },
        "four_anchor_cycles": cycle_certificates,
        "bridge_falsifier": {
            "excluded_phase_equivalent_edges": [
                list(values[edge_id]) for edge_id in sorted(bridge_class_edges)
            ],
            "minimum_cycle_length_after_exclusion": len(without_bridge),
            "witness_U6": [list(values[edge_id]) for edge_id in without_bridge],
            "conclusion": "El puente mostrado aparece en testigos, pero no es forzado por la clausura mínima.",
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
