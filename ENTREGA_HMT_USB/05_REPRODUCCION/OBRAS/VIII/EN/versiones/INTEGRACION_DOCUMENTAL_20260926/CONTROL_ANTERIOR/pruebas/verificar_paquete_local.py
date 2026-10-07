#!/usr/bin/env python3
"""Reproduce los controles locales de VII con biblioteca estándar.

No necesita conexión, skills ni el corpus original. Las comprobaciones son
focales: los recibos describen su alcance y no certifican todos los teoremas.
La conservación documental se contrasta separadamente de la matemática.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TESTS = [
    ("verificar_integracion.py", []),
    ("verificar_pantalla_y_rebote.py", ["--json"]),
    ("verificar_inversas_torsion.py", ["--json"]),
    ("verificar_respuesta_memoria.py", []),
    ("verificar_composicion_corriente.py", []),
    ("verificar_extension_minima.py", ["--json"]),
    ("verificar_tensor_residual.py", ["--json"]),
    ("verificar_observador_respuesta.py", []),
    ("verificar_portador_tensorial.py", []),
    ("verificar_eliminacion_torsional_no_lineal.py", []),
    ("verificar_corriente_espinorial.py", ["--json"]),
    ("verificar_rebote_polvo.py", []),
    ("verificar_propagacion_bidireccional.py", []),
]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    checks, failures = [], []
    for name, options in TESTS:
        script = ROOT / "pruebas" / name
        pair = []
        for optimized in (False, True):
            command = [sys.executable, "-I", "-S"]
            if optimized:
                command.append("-O")
            command.extend([str(script), *options])
            run = subprocess.run(command, cwd=ROOT, capture_output=True,
                                 text=True, timeout=180)
            try:
                data = json.loads(run.stdout)
            except ValueError:
                data = {"status": "INVALID_JSON", "stdout": run.stdout}
            status = data.get("status", data.get("result", ""))
            passed = run.returncode == 0 and not run.stderr and status.startswith("PASS_")
            pair.append(data)
            checks.append({"script": "pruebas/" + name,
                "sha256": digest(script), "optimized": optimized,
                "passed": passed, "returncode": run.returncode,
                "stderr": run.stderr, "result": data})
            if not passed:
                failures.append({"script": name, "optimized": optimized, "status": status})
        comparable = json.loads(json.dumps(pair))
        for item in comparable:
            if isinstance(item.get("execution"), dict):
                item["execution"].pop("python_optimization", None)
        if comparable[0] != comparable[1]:
            failures.append({"script": name, "normal_optimized_differ": True})
    result = {"schema": "hmt.vii.local_checks.v1",
        "status": "PASS_CONTROLES_LOCALES_VII" if not failures else "FAIL_CONTROLES_LOCALES_VII",
        "scripts": len(TESTS), "runs": len(checks), "checks": checks,
        "failures": failures, "network_required": False,
        "skills_required": False, "original_corpus_required": False,
        "whole_article_mathematical_certification": False,
        "scope": "Controles algebraicos focales y conservación documental; las pruebas generales residen en el manuscrito."}
    if args.receipt:
        args.receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "scripts", "runs", "failures")}, ensure_ascii=False))
    return 0 if not failures else 1

if __name__ == "__main__":
    sys.exit(main())
