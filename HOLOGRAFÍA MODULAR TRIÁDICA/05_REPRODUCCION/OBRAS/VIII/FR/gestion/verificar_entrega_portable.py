#!/usr/bin/env python3
"""Reproduce los controles de VII en una copia temporal independiente."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def require(ok, msg):
    if not ok:
        raise RuntimeError(msg)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight", required=True, type=Path)
    parser.add_argument("--receipt", required=True, type=Path)
    a = parser.parse_args()
    preflight = a.preflight.resolve()
    require(preflight.is_relative_to(ROOT), "Preflight debe estar dentro del paquete.")
    selected = []
    for p in sorted(ROOT.rglob("*")):
        r = p.relative_to(ROOT)
        require(not p.is_symlink(), "Enlace simbólico: " + str(r))
        if not p.is_file() or any(x in {"tmp", "__pycache__", ".DS_Store"} for x in r.parts):
            continue
        if r.parts[:3] == ("output", "pdf", "historial") or p.suffix == ".zip":
            continue
        selected.append(p)
    with tempfile.TemporaryDirectory(prefix="hmt_vii_portable_") as temporary:
        target = Path(temporary) / "ARTICULO_VII"
        for p in selected:
            dest = target / p.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)
            require(hashlib.sha256(dest.read_bytes()).digest() ==
                    hashlib.sha256(p.read_bytes()).digest(), "Copia divergente.")
        commands = [
            [sys.executable, "-I", "-S", str(target / "pruebas/verificar_paquete_local.py")],
            [sys.executable, "-I", "-S", str(target / "gestion/compilar_portable_VII.py"),
             "--check-only", "--preflight", str(target / preflight.relative_to(ROOT))]
        ]
        results = []
        for cmd in commands:
            result = subprocess.run(cmd, cwd=temporary, capture_output=True, text=True, timeout=300)
            require(result.returncode == 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            results.append(payload)
        require(results[0]["status"] == "PASS_CONTROLES_LOCALES_VII", "Controles locales no superados.")
        require(results[1]["compilation_authorized"] is True, "Binding del manuscrito no reproducido.")
        require(results[1]["source_graph"]["errors"] == [], "Dependencias no resueltas.")
        report = {
            "status": "PASS_REPRODUCCION_PORTABLE_VII",
            "files_copied": len(selected),
            "local_scripts": results[0]["scripts"],
            "local_runs": results[0]["runs"],
            "preflight": preflight.relative_to(ROOT).as_posix(),
            "preflight_sha256": hashlib.sha256(preflight.read_bytes()).hexdigest(),
            "compilation_binding_reproduced": True,
            "tex_executed_in_temporary_copy": False,
            "local_tests_usable_without_skills": True,
            "external_canonical_gates_rerun": False,
            "whole_article_mathematical_certification": False,
            "scope": "Copia independiente; 13 verificadores, 26 ejecuciones y comprobación del ensamblado y sus huellas. No prueba matemática global."
        }
    a.receipt.parent.mkdir(parents=True, exist_ok=True)
    a.receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))

if __name__ == "__main__":
    main()
