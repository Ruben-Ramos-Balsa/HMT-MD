#!/usr/bin/env python3
"""Reproduce N69 from exact regional readers, before opening the reference CSV.

This is a posterior publication of already specified regional functionals.
It removes N69's raw table as an independent computational input; it does not
select W24, S8, or a canonical terminal ledger. In particular, this program
does not read K, alpha, U12, W72, or a target decimal expansion.

Sources reused, not rediscovered:
  01_SELECTOR_CONSTANTES/selector_global_por_funcionales.py: regional readers;
  G9_MONODROMIA/hmt_puerta_ley01_taxonomia_ciclos.py:67-83: signatures;
  N69_ley_transicion_o_axioma_cilindrico.tex: mechanical calendar.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import runpy
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
READER = ROOT / (
    "16_CIERRE_GLOBAL_HMT_MD_2026-07-22/01_SELECTOR_CONSTANTES/"
    "selector_global_por_funcionales.py"
)
REFERENCE = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_CADENA_VIGENTE/N69_CALENDARIO_TRANSICION/"
    "HMT_N69_ley_transicion_o_axioma_cilindrico_v1/N69_signatures_t0_t99.csv"
)
SIGNATURE_OWNER = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_MONODROMIA/hmt_puerta_ley01_taxonomia_ciclos.py"
)
ROLES = ("cierre", "propagacion", "autoescala")
FIELDS = ("t", "K", "dK_next", "q", "a", "c", "colw", "colw_mod", "dual", "r", "B")
J_WITT = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 1, 2, 2),
    (1, 1, 0, 2, 1, 2),
    (1, 1, 2, 0, 2, 1),
    (1, 2, 1, 2, 0, 1),
    (1, 2, 2, 1, 1, 0),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def word(values: Any) -> str:
    return "".join(map(str, values))


def clock(time: int) -> int:
    """floor(log_1000(3^(6*(time+1)))) using integers only."""
    require(time >= 0, "Negative time")
    bound = 3 ** (6 * (time + 1))
    k = 0
    while 1000 ** (k + 1) <= bound:
        k += 1
    return k


def signature(time: int, bands: tuple[str, str, str]) -> dict[str, str]:
    require(all(len(b) == 6 and set(b) <= {"0", "1", "2"} for b in bands),
            "Expected three ternary words of length six")
    rows = tuple(tuple(map(int, b)) for b in bands)
    sums = tuple(sum(row[j] for row in rows) for j in range(6))
    widths = tuple(sum(row[j] != 0 for row in rows) for j in range(6))
    dual = tuple(
        sum(sum(row[i] * J_WITT[i][j] for i in range(6)) % 3
            for j in range(6)) % 3
        for row in rows
    )
    return {
        "t": str(time), "K": str(clock(time)),
        "dK_next": str(clock(time + 1) - clock(time)),
        "q": word(x % 3 for x in sums),
        "a": word((rows[0][j] + rows[1][j] - rows[2][j]) % 3 for j in range(6)),
        "c": word(x // 3 for x in sums),
        "colw": word(widths), "colw_mod": word(x % 3 for x in widths),
        "dual": word(dual), "r": word(sum(row) % 3 for row in rows),
        "B": "|".join(bands),
    }


def produce(count: int = 100) -> tuple[list[dict[str, str]], dict[str, Any]]:
    require(count > 0, "Positive count required")
    # run_name prevents the historical writer main() from executing.
    reader = runpy.run_path(str(READER), run_name="hmt_regional_reader_only")
    streams: dict[str, str] = {}
    enclosures: dict[str, Any] = {}
    for role in ROLES:
        digits, interval = reader["emitir"](reader["FUNCIONALES"][role], 3, 6 * count)
        streams[role] = reader["palabra"](digits)
        enclosures[role] = {
            "iteration": interval.iteraciones,
            "lower": [str(interval.inferior.numerator), str(interval.inferior.denominator)],
            "upper": [str(interval.superior.numerator), str(interval.superior.denominator)],
            "word_sha256": hashlib.sha256(streams[role].encode()).hexdigest(),
        }
    rows = [signature(t, tuple(streams[r][6*t:6*t+6] for r in ROLES))
            for t in range(count)]
    return rows, {"enclosures": enclosures, "streams": streams}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE)
    args = parser.parse_args()

    # Every generated field exists before the historical table is opened.
    generated, data = produce()
    with REFERENCE.open(encoding="utf-8", newline="") as handle:
        reference = list(csv.DictReader(handle))
    require(len(reference) == len(generated), "Different row counts")
    mismatches = [
        {"time": i, "field": field, "generated": a[field], "reference": b[field]}
        for i, (a, b) in enumerate(zip(generated, reference))
        for field in FIELDS if a[field] != b[field]
    ]
    require(not mismatches, f"N69 mismatch: {mismatches[:3]}")
    args.output.mkdir(parents=True, exist_ok=True)
    target = args.output / "N69_REGENERATED.csv"
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(generated)
    report = {
        "status": "PASS_N69_REGENERATED_FROM_REGIONAL_READERS",
        "scope": "Exact finite reproduction of the N69 table; not terminal-ledger selection.",
        "rows": len(generated), "fields_per_row": len(FIELDS),
        "equal_fields": len(generated) * len(FIELDS), "mismatches": mismatches,
        "generation_before_reference_read": True,
        "calendar_uses_floating_point": False,
        "reference_used_as_generator": False,
        "reads_K_alpha_U12_or_W72": False,
        "does_not_prove": ["upstream choice of W24 and S8", "canonical Family publication", "whole Article I"],
        "provenance_status": "CERTIFICADO_NUEVO of RESULTADO_RECUPERADO",
        "sources": [{"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                    for p in (READER, SIGNATURE_OWNER, REFERENCE, Path(__file__).resolve())],
        "output": {"path": str(target), "sha256": hashlib.sha256(target.read_bytes()).hexdigest()},
        **data,
    }
    receipt = args.output / "N69_REGENERATION.json"
    receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(report["status"], f"rows={len(generated)} equal_fields={report['equal_fields']}")
    print(receipt)


if __name__ == "__main__":
    main()
