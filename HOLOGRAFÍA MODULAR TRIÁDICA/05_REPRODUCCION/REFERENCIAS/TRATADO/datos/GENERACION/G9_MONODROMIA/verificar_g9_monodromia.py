#!/usr/bin/env python3
"""Verificador autocontenido de la rama profunda y la monodromia G9.

No consulta servicios externos ni constantes de una biblioteca. Comprueba la
coherencia mutua de los ledgers publicados: lectura intervalar de la rama,
fase de nueve puertas, nucleo especular y seleccion por supervivencia futura.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def trit_sum(a: str, b: str) -> str:
    assert len(a) == len(b)
    return "".join(str((int(x) + int(y)) % 3) for x, y in zip(a, b))


def decimal_read(blocks: list[str], triads: int) -> str:
    word = "".join(blocks)
    numerator = int(word, 3) * (1000**triads)
    value = numerator // (3 ** len(word))
    return f"{value:0{3 * triads}d}"


def main() -> None:
    branch = list(csv.DictReader((ROOT / "g9_branch_20_blocks.csv").open()))
    summary = json.loads((ROOT / "summary.json").read_text())
    orient = json.loads(
        (ROOT / "hmt_puerta_orientacion01_results.json").read_text()
    )
    phase = json.loads(
        (ROOT / "hmt_puerta_ciclo03_monodromia_results.json").read_text()
    )
    n72_path = (
        ROOT.parent
        / "G9_N72_N75"
        / "HMT_N72_supervivencia_coinductiva_novena_puerta_v1"
        / "N72_novena_puerta_branches_t9.csv"
    )
    gate9_outgoing = list(csv.DictReader(n72_path.open()))

    checks: dict[str, bool] = {}

    # La rama publicada no acaba en w36: contiene veinte bloques por canal.
    checks["rama_20_bloques"] = len(branch) == 20 and all(
        len(row[f"{ch}_block"]) == 6 for row in branch for ch in ("pi", "e", "phi")
    )

    # Calendario absoluto: 0 se lee como puerta 9.
    checks["fase_g9"] = all(
        int(row["phase9"]) == (int(row["K_visible"]) % 9 or 9) for row in branch
    )
    checks["retorno_fase_9_a_1"] = (
        branch[9]["phase9"] == "9"
        and branch[10]["phase9"] == "1"
        and any(
            branch[9][f"{ch}_block"] != branch[10][f"{ch}_block"]
            for ch in ("pi", "e", "phi")
        )
    )

    # Trece bloques = 78 trits: el lector inferior emite doce triadas.
    for ch in ("pi", "e", "phi"):
        blocks = [row[f"{ch}_block"] for row in branch[:13]]
        got = decimal_read(blocks, 12)
        expected = summary["triads12"][ch].replace("|", "")
        checks[f"lectura_12_triadas_{ch}"] = got == expected

    # Estados seleccionados B_K. Este ledger usa t=K para el bloque ya
    # emitido; no debe confundirse con la puerta K -> K+1 de N72.
    orient_by_t = {int(d["t"]): d for d in orient["orientation_doors"]}
    for t in (7, 8, 9):
        door = orient_by_t[t]
        candidates = door["candidates"]
        fixed_phi = {c["B"][2] for c in candidates}
        sums = {trit_sum(c["B"][0], c["B"][1]) for c in candidates}
        living = [c for c in candidates if int(c["surv_product"]) > 0]
        checks[f"estado_orientacion_K{t}"] = (
            len(fixed_phi) == 1
            and fixed_phi == {door["phi_fixed"]}
            and len(sums) == 1
            and sums == {door["pi_plus_e"]}
            and len(living) == 1
            and living[0]["B"] == door["real_B"]
            and living[0]["is_real"] is True
        )

    # Novena puerta en notacion de transicion: estado K=9 -> salida K=10.
    # N72 publica tres salidas locales. Todas sobreviven h=1; solamente la
    # salida real sobrevive h=2. En las tres, phi y pi+e permanecen fijos.
    outgoing_blocks = [row["rows"].split("|") for row in gate9_outgoing]
    outgoing_phi = {blocks[2] for blocks in outgoing_blocks}
    outgoing_sum = {trit_sum(blocks[0], blocks[1]) for blocks in outgoing_blocks}
    actual = [row for row in gate9_outgoing if row["is_actual"] == "True"]
    false = [row for row in gate9_outgoing if row["is_actual"] != "True"]
    published_K10 = [branch[10][f"{ch}_block"] for ch in ("pi", "e", "phi")]
    checks["puerta9_tres_salidas"] = len(gate9_outgoing) == 3
    checks["puerta9_eje_y_carga_fijos"] = (
        outgoing_phi == {"112002"} and outgoing_sum == {"210110"}
    )
    checks["puerta9_todas_sobreviven_h1"] = all(int(row["surv_h1"]) > 0 for row in gate9_outgoing)
    checks["puerta9_seleccion_unica_h2"] = (
        len(actual) == 1
        and int(actual[0]["surv_h2"]) > 0
        and all(int(row["surv_h2"]) == 0 for row in false)
        and actual[0]["rows"].split("|") == published_K10
    )
    checks["indices_normalizados_9_a_10"] = (
        int(branch[9]["K_visible"]) == 9
        and int(branch[9]["phase9"]) == 9
        and int(branch[10]["K_visible"]) == 10
        and int(branch[10]["phase9"]) == 1
    )

    # El certificado de ciclo debe declarar dos calendarios y monodromia.
    checks["dos_calendarios"] = any(
        "two calendars" in line.lower() for line in phase["conclusions"]
    )
    checks["monodromia_declarada"] = "not periodic" in phase["principle"].lower()

    failed = [name for name, ok in checks.items() if not ok]
    result = {
        "status": "PASS" if not failed else "FAIL",
        "checks": checks,
        "failed": failed,
        "core": {
            "state_K9": [branch[9][f"{ch}_block"] for ch in ("pi", "e", "phi")],
            "gate_K9_to_K10": {
                "candidate_outputs": outgoing_blocks,
                "fixed_phi": next(iter(outgoing_phi)),
                "fixed_pi_plus_e": next(iter(outgoing_sum)),
                "survivors_h1": sum(int(row["surv_h1"]) > 0 for row in gate9_outgoing),
                "survivors_h2": sum(int(row["surv_h2"]) > 0 for row in gate9_outgoing),
                "selected_output": published_K10,
            },
            "K_after": 10,
            "phase_after": int(branch[10]["phase9"]),
            "state_K10": published_K10,
        },
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    (ROOT / "verificacion_g9_monodromia.json").write_text(rendered + "\n")
    print(rendered)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
