#!/usr/bin/env python3
"""Controles cruzados V2 para cubo, G9, M12 y dimensiones.

Este programa no sustituye los verificadores generadores de cada paquete.
Comprueba que sus salidas congeladas son mutuamente compatibles con el
manuscrito rector y escribe un resumen determinista.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    cube = read_json(ROOT / "CUBO_MACRO" / "cubo_macro_audit_summary.json")
    g9 = read_json(ROOT / "G9_MONODROMIA" / "summary.json")
    n72 = read_json(
        ROOT
        / "G9_N72_N75"
        / "HMT_N72_supervivencia_coinductiva_novena_puerta_v1"
        / "summary.json"
    )
    m12 = read_json(ROOT / "M12_WITT" / "verificacion_m12_witt.json")

    atlas = cube["atlas"]
    assert atlas["U6_size"] == 729
    assert atlas["boundary_points_side9"] == 386
    assert atlas["growth_shell_10^3_minus_9^3"] == 271
    assert atlas["shell_decomp_cubic"]["sum"] == 271
    assert cube["hensel"]["carry_cocycle_ok"] is True

    assert all(len(g9["blocks"][channel]) == 20 for channel in ("pi", "e", "phi"))
    state_K9 = tuple(g9["blocks"][channel][9] for channel in ("pi", "e", "phi"))
    state_K10 = tuple(g9["blocks"][channel][10] for channel in ("pi", "e", "phi"))
    assert state_K9 == ("100100", "020112", "010122")
    assert state_K10 == ("101222", "112221", "112002")
    assert all(len(g9["triads12"][channel].split("|")) == 12 for channel in ("pi", "e", "phi"))

    survival = n72["resolution_statistics"]
    assert survival["max_resolution_depth"] == 3
    assert survival["all_resolved_by_h3"] is True
    assert survival["all_actual_survives_to_h9"] is True
    ninth = n72["novena_t9"][0]
    assert ninth["selected_count_h0"] == 3
    assert ninth["survivors_h1"] == 3
    assert ninth["survivors_h2"] == 1
    assert ninth["actual_rows"].split("|") == list(state_K10)

    assert m12["all_star_involutions_preserve_W12"] is True
    assert m12["generated_group_order"] == 95040
    assert m12["ordered_HMT_frame_stabilizer"] == 1

    dimensions = {
        "V3_11_2": 1 + 11 * 2 + 55 * 4,
        "perfect_product": 3**6 * 243,
        "F6": 6 * 15,
        "F8": 8 * 15,
        "normalized_defect": [90 - 120, 24 * 15],
        "A5_active": [3, 3, 5],
        "polarized_screen": [2, 3, 5],
    }
    assert dimensions["V3_11_2"] == 243
    assert dimensions["perfect_product"] == 3**11
    assert dimensions["F6"] == 90 and dimensions["F8"] == 120
    assert dimensions["normalized_defect"] == [-30, 360]
    assert sum(dimensions["A5_active"]) == 11
    assert sum(dimensions["polarized_screen"]) == 10

    result = {
        "schema": "HMT.extensiones_rectoras.v2",
        "status": "PASS",
        "cube": {
            "ambient": 729,
            "boundary": 386,
            "corona": 271,
            "carry_cocycle": True,
        },
        "g9": {
            "blocks_per_channel": 20,
            "state_K9": state_K9,
            "gate_K9_to_K10_candidates": 3,
            "survivors_h1": 3,
            "survivors_h2": 1,
            "state_K10": state_K10,
            "max_resolution_depth": 3,
            "survives_to_h9": True,
        },
        "M12": {
            "generated_group_order": 95040,
            "ordered_frame_stabilizer": 1,
        },
        "dimensions": dimensions,
    }
    output = ROOT / "verificacion_extensiones_rectoras.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
