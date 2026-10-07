#!/usr/bin/env python3
"""Controles racionales de la expectativa en los modos uniforme y de acarreo.

El control no prueba positividad de Weil. Verifica únicamente las identidades
de historia de la nota AGENTE_CARTAS_Y_EXPECTATIVA.md, ecuaciones (2)--(4).
No usa assert: los mismos 25 controles se ejecutan con Python normal y -O.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def verify() -> list[dict]:
    checks = []
    for n in (2, 3, 9, 81, 729):
        m = 9 * n
        # Vector de acarreo sin normalizar: v_m = m*e_0 - 1.
        v = [Fraction(m - 1)] + [Fraction(-1)] * (m - 1)
        pv = []
        for k in range(n):
            average = sum(v[9 * k : 9 * k + 9]) / 9
            pv.extend([average] * 9)
        expected = []
        for k in range(n):
            expected.extend([Fraction(n - 1 if k == 0 else -1)] * 9)
        qv = [x - y for x, y in zip(v, pv)]
        norm_v = sum(x * x for x in v)
        projected_ratio = sum(x * x for x in pv) / norm_v
        detail_ratio = sum(x * x for x in qv) / norm_v
        records = [
            ("promedio_bloques", pv == expected, "P v_(9N) = v_N tensor 1_9"),
            (
                "fraccion_publicada",
                projected_ratio == Fraction(n - 1, 9 * n - 1),
                fraction_text(projected_ratio),
            ),
            ("media_nula", sum(pv) == 0, fraction_text(sum(pv))),
            (
                "ortogonalidad_detalle",
                sum(x * y for x, y in zip(qv, pv)) == 0,
                fraction_text(sum(x * y for x, y in zip(qv, pv))),
            ),
            (
                "fraccion_memoria",
                detail_ratio == Fraction(8 * n, 9 * n - 1),
                fraction_text(detail_ratio),
            ),
        ]
        for name, passed, value in records:
            checks.append(
                {
                    "id": f"N{n}.{name}",
                    "N": n,
                    "nonadic_level": n in (9, 81, 729),
                    "passed": bool(passed),
                    "exact_value": value,
                }
            )
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    checks = verify()
    passed = len(checks) == 25 and all(row["passed"] for row in checks)
    script = Path(__file__).resolve()
    receipt = {
        "schema": "HMT_FOCAL_EXPECTATION_MODES_1",
        "status": "PASS_EXPECTATIVA_MODOS_RACIONALES" if passed else "FAIL",
        "scope": (
            "Ecuaciones (2)--(4): promedio, fraccion de norma, media nula, "
            "ortogonalidad y complemento; no verifica positividad global de Weil."
        ),
        "script": script.name,
        "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "python_version": sys.version.split()[0],
        "optimization_level": sys.flags.optimize,
        "uses_assert": False,
        "check_count": len(checks),
        "passed_count": sum(row["passed"] for row in checks),
        "checks": checks,
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"{receipt['status']}: {receipt['passed_count']}/{len(checks)}; "
          f"optimize={sys.flags.optimize}; receipt={args.receipt}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
