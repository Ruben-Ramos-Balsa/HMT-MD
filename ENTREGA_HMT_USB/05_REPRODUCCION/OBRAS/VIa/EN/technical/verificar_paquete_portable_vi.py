#!/usr/bin/env python3
"""Controles documentales y finitos de VI sobre una copia temporal mínima.

Uso: python3 -I -S technical/verificar_paquete_portable_vi.py
La comparación del núcleo usa sólo el recibo incluido en el paquete. No abre
su source_manifest histórico, no compila PDF ni ejecuta gates genealógicos.
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
import tempfile
import time

CORE = {
    "figures/app.tex", "figures/regimenes_trit.tex",
    "sections/memoria_resolvente.tex", "sections/nucleo.tex",
    "sections/tpk_desarrollo_integrado.tex", "sections/trit_desarrollo.tex",
}
CHECKS = [
    ("verificar_fuentes_vi.py", ["--check"], "STATIC_REVIEW_COMPLETE_NOT_COMPILATION"),
    ("generar_apendices_catalogo.py", ["--check"], "PASS_FUENTES_APENDICES_DOCUMENTALES_VI"),
    ("verificar_construcciones_finitas.py", [], "PASS_CONTROLES_FINITOS_VI"),
    ("verificar_particula_mobius_kepler.py", [], "PASS_FOCAL_PARTICULA_MOBIUS_KEPLER"),
    ("verificar_fock_pauli.py", [], "PASS_FINITE_FOCK_PAULI_NOT_PHYSICAL_CERTIFICATION"),
    ("verificar_controles_dependencias_09.py", [], "PASS_CONTROLES_FINITOS_DEPENDENCIAS_09"),
    ("verificar_controles_historias_15.py", [], "PASS_CONTROLES_FINITOS_HISTORIAS_15"),
]


def require(test, message):
    if not test:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_file(root, relative):
    path = root / relative
    require(path.is_file(), "Archivo local ausente: " + relative)
    require(not path.is_symlink(), "Enlace simbólico no admitido: " + relative)
    require(path.resolve().is_relative_to(root), "Ruta fuera del paquete: " + relative)
    return path


def copy_minimal(root, target):
    # No recorre subdirectorios técnicos históricos o de generación/QA.
    selected = set(root.glob("*.tex"))
    for directory in ("sections", "figures", "figuras"):
        folder = root / directory
        if folder.is_dir():
            selected.update(p for p in folder.iterdir() if p.is_file())
    technical = root / "technical"
    selected.update(p for p in technical.iterdir()
                    if p.is_file() and p.suffix in {".py", ".json", ".csv", ".md", ".tex"})
    records = []
    for source in sorted(selected):
        relative = source.relative_to(root).as_posix()
        source = local_file(root, relative)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        raw = source.read_bytes()
        destination.write_bytes(raw)
        records.append({"path": relative, "sha256": hashlib.sha256(raw).hexdigest(),
                        "bytes": len(raw)})
    return records


def compare_core(root):
    receipt_path = local_file(root, "technical/NUCLEO_COMUN_RECIBO.json")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    rows = receipt.get("files")
    require(isinstance(rows, list) and len(rows) == 6, "Se requieren seis fuentes del núcleo")
    names = [r.get("path") for r in rows if isinstance(r, dict)]
    require(len(names) == 6 and set(names) == CORE, "Lista del núcleo distinta de las seis fuentes")
    result = []
    for row in rows:
        expected = row.get("sha256", "")
        require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected),
                "Huella SHA256 no válida en el recibo")
        actual = digest(local_file(root, row["path"]))
        result.append({"path": row["path"], "expected_sha256": expected,
                       "actual_sha256": actual, "matches": actual == expected})
    return {"receipt_sha256": digest(receipt_path), "files": result,
            "all_six_match": all(r["matches"] for r in result),
            "comparison_basis": "Las seis huellas del recibo local incluido",
            "external_source_manifest_opened": False,
            "common_core_original_rechecked": False}


def run_check(root, name, args, expected, timeout):
    script = local_file(root, "technical/" + name)
    command = [sys.executable, "-I", "-S", "-B", str(script), *args]
    environment = dict(os.environ)
    for key in ("PYTHONPATH", "PYTHONHOME", "PYTHONOPTIMIZE"):
        environment.pop(key, None)
    started = time.monotonic()
    record = {"script": "technical/" + name, "script_sha256": digest(script),
              "arguments": args, "python_flags": ["-I", "-S", "-B"],
              "executed": True, "expected_local_status": expected}
    try:
        process = subprocess.run(command, cwd=root, env=environment, text=True,
                                 capture_output=True, timeout=timeout, check=False)
        stdout, stderr = process.stdout, process.stderr
        record["returncode"] = process.returncode
        # Elimina únicamente la ruta efímera; conserva el resultado sustantivo.
        record["stdout"] = stdout.replace(str(root), "<COPIA_PORTABLE>")
        record["stderr"] = stderr.replace(str(root), "<COPIA_PORTABLE>")
        if name == "verificar_construcciones_finitas.py":
            observed = stdout.strip().split()[0] if stdout.strip() else ""
        else:
            try:
                payload = json.loads(stdout)
                observed = payload.get("status", payload.get("result", ""))
            except (ValueError, AttributeError):
                observed = "SALIDA_NO_JSON"
        record["observed_local_status"] = observed
        record["ok"] = process.returncode == 0 and observed == expected
    except subprocess.TimeoutExpired as error:
        record.update({"returncode": None, "ok": False, "error": "TIMEOUT",
                       "timeout_seconds": error.timeout})
    record["elapsed_seconds"] = round(time.monotonic() - started, 3)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--timeout", type=int, default=600,
                        help="Tiempo máximo en segundos por control")
    parser.add_argument("--skip-source-audit", action="store_true",
                        help="Registra como pendiente la revisión estática; nunca marca la serie completa")
    args = parser.parse_args()
    root = args.root.resolve()
    receipt = args.receipt or root / "technical/RECIBO_PAQUETE_PORTABLE_VI.json"
    report = {
        "schema": "HMT.VI.PORTABLE_LOCAL_CHECKS.v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": digest(Path(__file__)),
        "scope": "Identidad documental local y controles finitos ejecutados sobre una copia trasladada",
        "reading_order": "APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo → salida HMT–MD → reconocimiento y contraste convencional posterior",
        "E108_scope": "Se verifica el cálculo posterior del registro declarado. La selección y enumeración canónica de su libro incidencial no se ejecuta en estos controles.",
        "canonical_E108_produced": False,
        "full_generator_executed": False,
        "scientific_autonomy_certified": False,
        "genealogical_gate_executed": False,
        "pdf_compiled": False,
        "checks": [],
        "copy_policy": "Sólo fuentes maestras, secciones, figuras y archivos técnicos inmediatos; sin caches, cortes, qa, output ni árboles externos",
    }
    code = 1
    try:
        require(sys.flags.optimize == 0,
                "Ejecutar sin -O: un control heredado contiene assert y debe conservarlos activos")
        require(args.timeout > 0, "El tiempo máximo debe ser positivo")
        with tempfile.TemporaryDirectory(prefix="hmt_vi_portable_") as temporary:
            target = Path(temporary).resolve() / "VI"
            target.mkdir()
            report["copied_files"] = copy_minimal(root, target)
            report["core"] = compare_core(target)
            require(report["core"]["all_six_match"], "Divergencia de una o más fuentes del núcleo")
            for name, options, expected in CHECKS:
                if name == "verificar_fuentes_vi.py" and args.skip_source_audit:
                    report["checks"].append({"script": "technical/" + name,
                                              "executed": False,
                                              "status": "PENDIENTE_POR_OPCION_EXPLICITA"})
                    continue
                report["checks"].append(run_check(target, name, options, expected, args.timeout))
            executed = [r for r in report["checks"] if r["executed"]]
            report["executed_count"] = len(executed)
            report["successful_count"] = sum(r["ok"] for r in executed)
            report["all_requested_checks_executed"] = len(executed) == len(CHECKS)
            successful = all(r["ok"] for r in executed)
            report["status"] = ("CONTROLES_PORTABLES_COMPLETOS_SATISFACTORIOS" if successful and len(executed) == 7
                                else "CONTROLES_PORTABLES_PARCIALES_SATISFACTORIOS" if successful
                                else "FALLO_CONTROLES_PORTABLES")
            code = 0 if successful else 1
        report["temporary_copy_removed"] = True
    except Exception as error:
        report["status"] = "FALLO_CONTROLES_PORTABLES"
        report["error"] = f"{type(error).__name__}: {error}"
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "receipt": str(receipt),
                      "executed_count": report.get("executed_count", 0),
                      "successful_count": report.get("successful_count", 0),
                      "scientific_autonomy_certified": False}, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
