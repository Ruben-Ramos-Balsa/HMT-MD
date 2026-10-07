#!/usr/bin/env python3
"""Verificador rector de las identidades aritméticas del bloque 243.

No afirma una partición geométrica ni una T-dualidad física. Comprueba
únicamente identidades tipadas, conteos de incidencia y la involución racional
visible/memoria declarada en el manuscrito.
"""

from __future__ import annotations

from fractions import Fraction
import json
from math import comb


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"HMT 243 FAIL: {message}")


def energy(scale: Fraction, visible: int, memory: int) -> Fraction:
    return Fraction(visible * visible, 1) / (scale * scale) + (
        Fraction(memory * memory, 1) * scale * scale
    )


def main() -> None:
    hamming_ball = 1 + 11 * 2 + comb(11, 2) * 4
    require(hamming_ball == 243, "V_3(11,2) no vale 243")
    require(3**6 * hamming_ball == 3**11, "falla 729*243=3^11")
    require(729 + 243 + 27 + 1 == 1000, "falla la completación decimal")

    typed_identity = {
        "return": 1,
        "hamming_shell_r1": 22,
        "hexad_flags": 6 * comb(6, 2),
        "octad_flags": 8 * comb(6, 2),
        "polarized_screen_dimension": 10,
    }
    require(sum(typed_identity.values()) == 243, "falla la identidad tipada")
    require(typed_identity["hexad_flags"] == 90, "falla 6*C(6,2)=90")
    require(typed_identity["octad_flags"] == 120, "falla 8*C(6,2)=120")

    require(26 == 24 + 2, "falla el conteo 26=24+2")
    require(12 == 1 + 3 + 3 + 5, "falla la descomposición 12")
    require(11 == 3 + 3 + 5, "falla la descomposición 11")
    require(10 == 2 + 3 + 5, "falla la pantalla 10")

    cases = (
        (Fraction(2), 5, 7),
        (Fraction(3, 2), 8, 1),
        (Fraction(5, 3), 11, 4),
    )
    duality_checks = []
    for scale, visible, memory in cases:
        lhs = energy(scale, visible, memory)
        rhs = energy(1 / scale, memory, visible)
        require(lhs == rhs, "falla la involución visible/memoria")
        duality_checks.append({
            "scale": str(scale),
            "visible": visible,
            "memory": memory,
            "energy": str(lhs),
        })

    result = {
        "schema": "HMT.bloque_243_rector.v1",
        "status": "PASS",
        "hamming_ball_V3_11_2": hamming_ball,
        "perfect_identity": "3^6*243=3^11",
        "decimal_completion": [729, 243, 27, 1],
        "typed_identity_not_set_partition": typed_identity,
        "dimension_counts": {
            "26_to_24_plus_hyperbolic_plane": [26, 24, 2],
            "A5_permutation_dimensions": [1, 3, 3, 5],
            "active_11": [3, 3, 5],
            "polarized_10": [2, 3, 5],
        },
        "visible_memory_involution": duality_checks,
        "logical_scope": (
            "Arithmetic and typed combinatorial identities only; "
            "no physical T-duality, mass spectrum, or set partition is inferred."
        ),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
