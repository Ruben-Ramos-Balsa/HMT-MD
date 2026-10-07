#!/usr/bin/env python3
"""Comprueba siete teoremas focales con un ejecutable Lean local.

No instala Lean, Lake, Mathlib ni dependencias. La prueba sólo importa Std.
El resultado registra la ejecución real y el alcance de las declaraciones.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "BalanceBilateral.lean"
THEOREMS = (
    "HMT.Bilateral.balance_polynomial",
    "HMT.Bilateral.scalar_norm_preserving",
    "HMT.Bilateral.finite_balance",
    "HMT.Bilateral.finite_norm_preserving",
    "HMT.Bilateral.recovery_x",
    "HMT.Bilateral.recovery_y",
    "HMT.Bilateral.readers_injective",
)
ALLOWED_AXIOMS = {"propext", "Quot.sound", "Classical.choice"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean-bin", help="Ejecutable Lean existente; por defecto busca lean en PATH.")
    parser.add_argument("--output", type=Path, default=ROOT / "RESULTADO_LEAN.json")
    args = parser.parse_args()
    report = {
        "status": "NOT_CHECKED",
        "utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Siete teoremas sobre coordenadas enteras y vectores enteros de dimensión finita; no formaliza el balance general de Hilbert ni la producción APP--TRIT--TPK.",
        "expected_theorems": list(THEOREMS),
        "required_version": "4.21.0",
        "dependency": "Std de Lean 4.21.0; no Mathlib",
        "axiom_policy": {
            "allowed_standard_axioms": sorted(ALLOWED_AXIOMS),
            "sorryAx_allowed": False,
            "new_declared_axioms_allowed": False,
        },
        "verifier_sha256": sha(Path(__file__).resolve()),
    }
    code = 1
    try:
        found = args.lean_bin or shutil.which("lean")
        if not found:
            raise RuntimeError("Lean no está disponible: indique --lean-bin con un ejecutable ya instalado.")
        binary = Path(shutil.which(found) or found).expanduser().resolve()
        if not binary.is_file() or not os.access(binary, os.X_OK):
            raise RuntimeError("El ejecutable Lean indicado no existe o no es ejecutable.")
        env = os.environ.copy()
        env.pop("LEAN_PATH", None)
        env.pop("LEAN_SRC_PATH", None)
        report["lean_binary"] = {"path": str(binary), "sha256": sha(binary)}
        version = subprocess.run([str(binary), "--version"], cwd=ROOT, env=env,
                                 capture_output=True, text=True, timeout=15, check=False)
        report["version"] = {"returncode": version.returncode,
                             "stdout": version.stdout, "stderr": version.stderr}
        if version.returncode != 0 or not re.search(r"version 4\.21\.0(?:,|\))", version.stdout):
            raise RuntimeError("Esta formalización se comprobó con Lean 4.21.0; versión local incompatible o no ejecutable.")
        before = sha(SOURCE)
        source_text = SOURCE.read_text(encoding="utf-8")
        if re.search(r"^\s*(?:axiom|constant|opaque)\s", source_text, re.M):
            raise RuntimeError("La fuente contiene una declaración no admitida por este verificador focal.")
        if re.search(r"\b(?:sorry|admit|sorryAx)\b", source_text):
            raise RuntimeError("La fuente contiene una admisión no permitida.")
        command = [str(binary), "-DwarningAsError=true", SOURCE.name]
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True,
                                text=True, timeout=180, check=False)
        report["source"] = {"path": SOURCE.name, "sha256": before,
                            "unchanged_during_run": before == sha(SOURCE)}
        report["execution"] = {"argv": command, "cwd": str(ROOT),
                               "returncode": result.returncode,
                               "stdout": result.stdout, "stderr": result.stderr}
        printed = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", result.stdout)
        axioms = {name: [part.strip() for part in used.split(",") if part.strip()]
                  for name, used in printed}
        report["declaration_axioms"] = axioms
        if result.returncode != 0:
            raise RuntimeError("Lean rechazó la fuente; consulte stdout/stderr en este resultado.")
        if before != sha(SOURCE):
            raise RuntimeError("La fuente cambió durante la comprobación.")
        if len(printed) != len(THEOREMS) or set(axioms) != set(THEOREMS):
            raise RuntimeError("La salida no declara exactamente los siete teoremas esperados.")
        unknown = {axiom for used in axioms.values() for axiom in used} - ALLOWED_AXIOMS
        if unknown:
            raise RuntimeError("Dependencias axiomáticas no admitidas: " + ", ".join(sorted(unknown)))
        report["checked_theorems"] = len(THEOREMS)
        report["status"] = "LEAN_KERNEL_CHECK_PASSED_FOCAL_ONLY"
        code = 0
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        report["status"] = "LEAN_FOCAL_CHECK_FAILED"
        report["error"] = str(error)
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(report["status"])
    print(output)
    if code:
        print(report.get("error", "Error de comprobación"), file=sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
