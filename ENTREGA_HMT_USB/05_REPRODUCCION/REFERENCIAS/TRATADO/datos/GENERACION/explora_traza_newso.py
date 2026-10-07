#!/usr/bin/env python3
"""Exploración reproducible de las cuatro rutas κ27/TPK NEWSO.

No usa K_R12 ni constantes reales. Compara varias lecturas explícitas del
corpus para localizar qué parte del extractor 90/120 está determinada.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import json


DIRS = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
STARTS = {
    "N": (0, 0, 1),
    "E": (0, 3, 2),
    "S": (3, 0, 0),
    "O": (3, 3, 3),
}
TARGET = (234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601)


def digit(i: int, j: int) -> int:
    return 1 + (i % 3) + 3 * (j % 3)


def mov3(d: int) -> int:
    if d in (1, 4, 7):
        return 1
    if d in (2, 5, 8):
        return -1
    return 0


def tau(i: int, j: int) -> int:
    return {0: 0, 1: 1, 2: -1}[(i + j) % 3]


@dataclass(frozen=True)
class Row:
    route: str
    tick: int
    event: int
    i: int
    j: int
    heading: int
    digit: int
    move: int
    leaf: int


def trace(route: str, turn_sign: int = 1) -> list[Row]:
    i, j, h = STARTS[route]
    rows = []
    for t in range(1, 109):
        d = digit(i, j)
        mv = mov3(d)
        rows.append(Row(route, t, (t - 1) // 9, i, j, h, d, mv, tau(i, j)))
        if mv:
            h = (h - turn_sign * mv) % 4
        di, dj = DIRS[h]
        i, j = (i + di) % 9, (j + dj) % 9
    return rows


def event_digits(rows: list[Row]) -> list[int]:
    return [int(f"{TARGET[m]:03d}"[0]) for m in range(12)]


def audit(turn_sign: int) -> dict[str, object]:
    rows = [x for route in "NESO" for x in trace(route, turn_sign)]
    a = []
    nines = []
    nines_border = []
    leaf_balance = []
    move_balance = []
    for m in range(12):
        window = [x for x in rows if x.event == m]
        a.append(sum(x.digit in (1, 3, 5, 7) for x in window) % 10)
        nines.append(sum(x.digit == 9 for x in window))
        nines_border.append(
            (sum(x.digit == 9 and (x.i in (0, 8) or x.j in (0, 8)) for x in window)
             - sum(x.digit == 9 and not (x.i in (0, 8) or x.j in (0, 8)) for x in window))
            % 10
        )
        leaf_balance.append(sum(x.leaf for x in window) % 10)
        move_balance.append(sum(x.move for x in window) % 10)
    return {
        "turn_sign": turn_sign,
        "A_hits_all_four_routes_mod10": a,
        "target_hundreds": [x // 100 for x in TARGET],
        "nines_all_four_routes": nines,
        "crown_minus_internal_9_border_convention_mod10": nines_border,
        "target_units": [x % 10 for x in TARGET],
        "tau_balance_mod10": leaf_balance,
        "mov3_balance_mod10": move_balance,
        "route_blocks": {
            route: [
                "".join(str(x.digit) for x in trace(route, turn_sign) if x.event == m)
                for m in range(12)
            ]
            for route in "NESO"
        },
    }


def claimed_gate_extractor() -> tuple[int, ...]:
    """Algoritmo literal del módulo APP/SU--12/TPK del corpus."""

    def dr9(x: int) -> int:
        r = x % 9
        return 9 if r == 0 else r

    p = [[dr9(i + j) for j in range(9)] for i in range(9)]
    x = [[dr9((i + 1) * (j + 1)) for j in range(9)] for i in range(9)]
    heads = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "O": (0, -1)}
    starts = {"N": (0, 0), "E": (0, 3), "S": (3, 0), "O": (3, 3)}
    pos = {w: list(starts[w]) for w in starts}
    p_bit = 0
    digits: list[int] = []
    result: list[int] = []
    for t in range(1, 109):
        r = ((t - 1) % 9) + 1
        delta = 1 if r in (1, 4, 7) else (-1 if r in (2, 5, 8) else 0)
        for w in pos:
            hi, hj = heads[w]
            i, j = pos[w]
            pos[w] = ((i + delta * hi) % 9, (j + delta * hj) % 9)
        if r in (3, 6, 9):
            vals_p = [p[pos[w][0]][pos[w][1]] for w in "NESO"]
            vals_x = [x[pos[w][0]][pos[w][1]] for w in "NESO"]
            a = sum(vals_p) % 10
            prod9 = 1
            for value in vals_x:
                prod9 = (prod9 * (value % 9)) % 9
            c = 9 if prod9 == 0 else prod9 % 10
            digits.append((2 * a + 5 * c + p_bit) % 10)
        if t in (27, 54, 81, 108):
            p_bit = 1 - p_bit
        if t % 9 == 0:
            d1, d2, d3 = digits[-3:]
            result.append(100 * d1 + 10 * d2 + d3)
    return tuple(result)


def rotor_gate_variant(
    headings: tuple[int, int, int, int],
    turn_sign: int,
    read_after_move: bool,
    plus_offset: int,
    flip_before_gate: bool,
) -> tuple[int, ...]:
    """Cruza el lector de puertas con el rotor autónomo del corpus."""
    starts = ((0, 0), (0, 3), (3, 0), (3, 3))
    states = [[i, j, h] for (i, j), h in zip(starts, headings)]

    def dr9(value: int) -> int:
        residue = value % 9
        return 9 if residue == 0 else residue

    out: list[int] = []
    event_digits: list[int] = []
    p_bit = 0
    for t in range(1, 109):
        r = ((t - 1) % 9) + 1
        before = [s[:] for s in states]
        for state in states:
            i, j, h = state
            mv = mov3(digit(i, j))
            if mv:
                h = (h - turn_sign * mv) % 4
            di, dj = DIRS[h]
            state[:] = ((i + di) % 9, (j + dj) % 9, h)
        if flip_before_gate and t in (27, 54, 81, 108):
            p_bit = 1 - p_bit
        if r in (3, 6, 9):
            selected = states if read_after_move else before
            plus_values = [dr9(i + j + plus_offset) for i, j, _ in selected]
            times_values = [dr9((i + 1) * (j + 1)) for i, j, _ in selected]
            a = sum(plus_values) % 10
            c_residue = 1
            for value in times_values:
                c_residue = (c_residue * (value % 9)) % 9
            c = 9 if c_residue == 0 else c_residue
            event_digits.append((2 * a + 5 * c + p_bit) % 10)
        if not flip_before_gate and t in (27, 54, 81, 108):
            p_bit = 1 - p_bit
        if t % 9 == 0:
            d1, d2, d3 = event_digits[-3:]
            out.append(100 * d1 + 10 * d2 + d3)
    return tuple(out)


def search_rotor_gate_variants() -> dict[str, object]:
    target_digits = "".join(f"{x:03d}" for x in TARGET)
    best: list[tuple[int, tuple[int, ...], tuple[object, ...]]] = []
    exact: list[tuple[tuple[int, ...], tuple[object, ...]]] = []
    for headings in product(range(4), repeat=4):
        for turn_sign in (1, -1):
            for read_after in (False, True):
                for plus_offset in (0, 2):
                    for flip_before in (False, True):
                        output = rotor_gate_variant(
                            headings, turn_sign, read_after, plus_offset, flip_before
                        )
                        digits = "".join(f"{x:03d}" for x in output)
                        distance = sum(a != b for a, b in zip(digits, target_digits))
                        params = (headings, turn_sign, read_after, plus_offset, flip_before)
                        best.append((distance, output, params))
                        if distance == 0:
                            exact.append((output, params))
    best.sort(key=lambda row: (row[0], row[2]))
    return {
        "variants_tested": len(best),
        "exact_matches": [
            {"output": list(output), "parameters": repr(params)}
            for output, params in exact
        ],
        "best_five": [
            {"digit_hamming_distance": distance, "output": list(output), "parameters": repr(params)}
            for distance, output, params in best[:5]
        ],
    }


def main() -> None:
    rotor_variants = [audit(1), audit(-1)]
    legacy = claimed_gate_extractor()
    search = search_rotor_gate_variants()
    expected_collapse = (
        222, 222, 222, 333, 333, 333,
        222, 222, 222, 333, 333, 333,
    )
    checks = {
        "pseudocodigo_reiniciado_colapsa_como_publicado": legacy == expected_collapse,
        "pseudocodigo_reiniciado_no_reproduce_K": legacy != TARGET,
        "barrido_cubre_4096_variantes": search["variants_tested"] == 4096,
        "ninguna_variante_reproduce_K": search["exact_matches"] == [],
        "distancia_minima_publicada_26": (
            bool(search["best_five"])
            and search["best_five"][0]["digit_hamming_distance"] == 26
        ),
        "dos_orientaciones_y_doce_bloques": (
            len(rotor_variants) == 2
            and all(
                len(audit_row["route_blocks"][route]) == 12
                for audit_row in rotor_variants
                for route in "NESO"
            )
        ),
    }
    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "status": "PASS" if not failed else "FAIL",
        "checks": checks,
        "failed": failed,
        "rotor_variants": rotor_variants,
        "claimed_gate_extractor": list(legacy),
        "claimed_gate_matches_target": legacy == TARGET,
        "rotor_gate_search": search,
        "target": list(TARGET),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if failed:
        raise SystemExit(1)
    print("PASS — ablación del pseudocódigo histórico verificada")


if __name__ == "__main__":
    main()
