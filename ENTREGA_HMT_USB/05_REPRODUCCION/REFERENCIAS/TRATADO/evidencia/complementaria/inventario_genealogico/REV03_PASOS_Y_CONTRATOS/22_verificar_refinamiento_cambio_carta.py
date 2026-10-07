#!/usr/bin/env python3
"""Comprobación focal exacta del cambio de carta 3/1000.

No selecciona semillas, constantes ni trayectorias HMT. Prueba identidades,
inversas, intervalos semiabiertos y un ejemplo racional de carta explícito.
Ejecuta sólo las definiciones require/encode_trits/Cylinder extraídas del
propietario previo; no importa ni ejecuta su programa completo.
"""
from __future__ import annotations

import ast
import hashlib
import json
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any


OWNER = Path(
    "/Users/ruben/Documents/New project/output/"
    "INVESTIGACION_XTERM_S12_TARGET_FREE_20260914/construir_libro_pleno.py"
)


def residual(N: int, L: int, D: int, r: int) -> int:
    return 1000**r * N - D * 3**L


def candidate_prefixes(N: int, L: int, r_next: int) -> tuple[int, int]:
    """Índices mínimo y máximo de celdas que intersectan el cilindro."""
    T, S = 3**L, 1000**r_next
    return N * S // T, ((N + 1) * S - 1) // T


def intersects(N: int, L: int, D: int, r: int) -> bool:
    A = residual(N, L, D, r)
    B = A + 1000**r
    return A < 3**L and B > 0


def contained(N: int, L: int, D: int, r: int) -> bool:
    A = residual(N, L, D, r)
    B = A + 1000**r
    return A >= 0 and B <= 3**L


def trits_of_index(nu: int) -> list[int]:
    assert 0 <= nu < 729
    digits = [0] * 6
    for j in range(5, -1, -1):
        nu, d = divmod(nu, 3)
        digits[j] = -1 if d == 2 else d
    assert nu == 0
    return digits


def owner_cylinder():
    raw = OWNER.read_bytes()
    tree = ast.parse(raw, filename=str(OWNER))
    names = {"require", "encode_trits", "Cylinder"}
    selected = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in names
    ]
    assert {node.name for node in selected} == names
    namespace = {"dataclass": dataclass, "field": field, "Any": Any}
    module = ast.Module(body=selected, type_ignores=[])
    exec(compile(ast.fix_missing_locations(module), str(OWNER), "exec"), namespace)
    return namespace["Cylinder"], hashlib.sha256(raw).hexdigest()


def run() -> dict[str, Any]:
    identity_count = 0
    inverse_count = 0
    seeds = [(0, 0, 0, 0), (1, 6, 0, 0), (100, 6, 0, 0),
             (73100, 12, 137, 1), (-2, 3, -5, 1), (5, 4, 3, 2)]
    for N, L, D, r in seeds:
        A = residual(N, L, D, r)
        for nu in range(729):
            NN, LL = 729 * N + nu, L + 6
            AA = residual(NN, LL, D, r)
            assert AA == 729 * A + nu * 1000**r
            assert divmod(NN, 729) == (N, nu)
            assert (AA - nu * 1000**r) // 729 == A
            assert (AA - nu * 1000**r) % 729 == 0
            identity_count += 1
            inverse_count += 1
            for delta in (0, 7, 999):
                DD, rr = 1000 * D + delta, r + 1
                AAA = residual(NN, LL, DD, rr)
                recurrence = (
                    729000 * A + nu * 1000**(r + 1) - 729 * delta * 3**L
                )
                assert AAA == recurrence
                assert divmod(DD, 1000) == (D, delta)
                numerator = AAA - nu * 1000**(r + 1) + 729 * delta * 3**L
                assert numerator % 729000 == 0
                assert numerator // 729000 == A
                identity_count += 1
                inverse_count += 1

    interval_count = 0
    for L in (0, 2, 6):
        T = 3**L
        for N in (0, 1, T // 2, T - 1, T):
            for r in (0, 1, 2):
                S = 1000**r
                center = N * S // T
                for D in range(center - 2, center + 3):
                    t0, t1 = Fraction(N, T), Fraction(N + 1, T)
                    d0, d1 = Fraction(D, S), Fraction(D + 1, S)
                    assert intersects(N, L, D, r) == (max(t0, d0) < min(t1, d1))
                    assert contained(N, L, D, r) == (d0 <= t0 and t1 <= d1)
                    lo, hi = candidate_prefixes(N, L, r)
                    assert intersects(N, L, D, r) == (lo <= D <= hi)
                    interval_count += 1

    Cylinder, owner_hash = owner_cylinder()
    state = Cylinder()
    snapshots = [{"N": 0, "L": 0, "D": 0, "r": 0, "A": 0, "B": 1}]
    blocks = (100, 200, 300)
    for nu in blocks:
        result = None
        for t in trits_of_index(nu):
            result = state.append_trit(t)
        assert result is not None and result["block"]
        assert result["u6"] == nu
        assert state.A == residual(state.N, state.L, state.D, state.K_triads)
        assert contained(state.N, state.L, state.D, state.K_triads)
        lo, hi = candidate_prefixes(state.N, state.L, snapshots[-1]["r"] + 1)
        snapshots.append({
            "nu": nu, "trits_in_owner_chart": trits_of_index(nu),
            "delta": result["delta"] if result["delta"] != "" else None,
            "N": state.N, "L": state.L, "D": state.D, "r": state.K_triads,
            "A": state.A, "B": state.B,
            "next_cell_candidates_before_optional_emission": [lo, hi],
            "ternary_lower": str(Fraction(state.N, 3**state.L)),
            "ternary_upper": str(Fraction(state.N + 1, 3**state.L)),
            "decimal_lower": str(Fraction(state.D, 1000**state.K_triads)),
            "decimal_upper": str(Fraction(state.D + 1, 1000**state.K_triads)),
        })
    exact_fixture = Fraction(state.N, 3**state.L)
    assert [s.get("delta") for s in snapshots[1:]] == [None, 137, 551]
    assert state.N == 53290200 and state.L == 18
    assert state.D == 137551 and state.K_triads == 2

    # La ejecución del convertidor de prefijos no es un selector HMT de la ruta.
    # Para 1/2, todos los trits posicionales son 1: cada intervalo contiene
    # el punto de frontera decimal en su interior. La inclusión no decide lado.
    boundary = Cylinder()
    boundary_rows = []
    for block_index in range(1, 13):
        for _ in range(6):
            result = boundary.append_trit(1)
        T = 3**boundary.L
        assert boundary.N == (T - 1) // 2
        lo, hi = candidate_prefixes(boundary.N, boundary.L, 1)
        assert (lo, hi) == (499, 500)
        assert boundary.K_triads == 0
        assert result["delta"] == ""
        boundary_rows.append({
            "blocks": block_index, "L": boundary.L,
            "N": boundary.N, "decimal_candidate_range": [lo, hi],
            "emitted_blocks": boundary.K_triads,
        })

    # Control negativo: sustituir 729000 por 729 omite el cambio de escala decimal.
    N, L, D, r, nu, delta = 100, 6, 0, 0, 200, 137
    A = residual(N, L, D, r)
    direct = residual(729*N+nu, L+6, 1000*D+delta, r+1)
    wrong = 729*A + nu*1000**(r+1) - 729*delta*3**L
    assert wrong != direct

    return {
        "status": "PASS_FOCAL_REFINAMIENTO_CAMBIO_CARTA",
        "scope": (
            "Identidades e inversas enteras; criterios de intervalos semiabiertos; "
            "ejemplo racional de carta y control de frontera. "
            "No certifica selección de constantes, admisibilidad global ni CH."
        ),
        "integer_identity_cases": identity_count,
        "inverse_cases": inverse_count,
        "interval_cases": interval_count,
        "coefficient_negative_control": {"correct": direct, "wrong": wrong},
        "owner": str(OWNER),
        "owner_sha256": owner_hash,
        "owner_definitions_executed": ["require", "encode_trits", "Cylinder"],
        "declared_positional_fixture": {
            "blocks": list(blocks),
            "selection_role": "Ejemplo de carta elegido explícitamente; no selector de constante HMT.",
            "rational_at_final_lower_endpoint": str(exact_fixture),
            "states": snapshots,
        },
        "decimal_boundary_fixture": {
            "value_role": "Control racional de frontera, no generador HMT.",
            "value": "1/2", "states": boundary_rows,
            "conclusion": "El criterio de inclusión por prefijos no decide un punto de frontera exacto."
        },
        "not_checked": [
            "Identificación de esta instancia prospectiva con la trayectoria terminal histórica.",
            "Selección de los bloques de una constante desde APP–TRIT–TPK.",
            "Compatibilidad global de todos los campos del estado enriquecido.",
            "Formalización Lean del cambio de carta.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))

