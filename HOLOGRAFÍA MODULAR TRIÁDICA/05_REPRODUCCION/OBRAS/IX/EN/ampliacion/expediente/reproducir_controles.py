#!/usr/bin/env python3
"""Reproduce controles focales; su PASS no es un certificado de RH."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
TESTS = [
    ("costura", "verificar_costura_y_memoria.py", True, 210),
    ("momentos", "verificar_momentos_memoria.py", True, 1046),
    ("expectativa", "verificar_expectativa_modos.py", True, 25),
    ("schur", "verificar_schur_ventana_nonadica.py", False, 21),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True,
                        help="Nueva carpeta de recibos; no debe existir.")
    parser.add_argument("--centro-borde", action="store_true",
                        help="Añadir los controles del apunte centro–frontera y vacancias.")
    args = parser.parse_args()
    dest = args.output.resolve()
    dest.mkdir(parents=True, exist_ok=False)
    reports = []
    tests = list(TESTS)
    if args.centro_borde:
        tests.append(("centro_borde", "verificar_centro_borde_vacancias.py", True, 11430))
    for name, script, isolated, count in tests:
        for optimized in (False, True):
            receipt = dest / (name + ("_optimizado" if optimized else "_normal") + ".json")
            command = [sys.executable]
            if isolated:
                command += ["-I", "-S"]
            if optimized:
                command += ["-O"]
            command += [str(HERE / script)]
            # El lector de momentos publica JSON en stdout; los restantes
            # aceptan recibos explícitos. No se modifica ningún antecedente.
            if name != "momentos":
                command += ["--receipt", str(receipt)]
            proc = subprocess.run(command, text=True, capture_output=True, cwd=HERE)
            (dest / (receipt.stem + ".log")).write_text(proc.stdout + proc.stderr)
            if name == "momentos" and proc.returncode == 0:
                receipt.write_text(proc.stdout)
            try:
                report = json.loads(receipt.read_text())
            except (OSError, ValueError):
                report = {}
            if name == "momentos":
                buckets = report.get("checks", {})
                actual = report.get("checks_total")
                details_ok = isinstance(buckets, dict) and sum(buckets.values()) == actual
            elif name == "expectativa":
                details = report.get("checks", [])
                actual = report.get("check_count")
                details_ok = (isinstance(details, list) and len(details) == actual
                              and report.get("passed_count") == actual
                              and all(item.get("passed") is True for item in details))
            else:
                actual = report.get("checks")
                details_ok = isinstance(actual, int)
                if name == "centro_borde":
                    groups = report.get("checks_by_group", {})
                    details_ok = (details_ok and isinstance(groups, dict)
                                  and sum(groups.values()) == actual)
            status = report.get("status", "")
            passed = (proc.returncode == 0 and status.startswith("PASS")
                      and actual == count and details_ok
                      and report.get("optimization_level") == int(optimized))
            reports.append({"name": name, "optimized": optimized,
                            "command": command, "exit_code": proc.returncode,
                            "checks": actual, "expected_checks": count,
                            "receipt": receipt.name, "passed": passed})
    all_passed = all(r["passed"] for r in reports)
    report = {"status": "PASS_CONTROLES_FOCALES_DOBLE_CIRCULO" if all_passed else "FAIL_CONTROLES_FOCALES_DOBLE_CIRCULO",
              "runs": reports,
              "total_checks_if_all_passed": 2 * sum(t[3] for t in tests),
              "global_weil_positivity_certified": False,
              "center_boundary_included": args.centro_borde,
              "infinite_dimensional_proofs": "Written mathematical notes accompanying README.md; counts do not replace proofs",
              "sources": [{"path": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                          for p in sorted(HERE.glob("*.py")) + sorted(HERE.glob("*.md"))]}
    (dest / "RECIBO_CONJUNTO.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "runs": len(reports),
                      "passed": sum(r["passed"] for r in reports),
                      "receipt": str(dest / "RECIBO_CONJUNTO.json")}, ensure_ascii=False))
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
