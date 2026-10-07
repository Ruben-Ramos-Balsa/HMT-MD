"""Check and execute the self-contained focal reproduction package."""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
TESTS = (
    "verificar_transporte_radial_polar.py",
    "verificar_composicion_metrica.py",
    "verificar_rigidez_simultanea.py",
    "verificar_sustitucion_estructural.py",
    "verificar_sustitucion_contraangulo.py",
)
AUDITED_STANDARD_MODULES = {
    "decimal", "fractions", "pathlib", "hashlib", "json", "itertools", "importlib",
}
LOCAL_DEPENDENCIES = {
    TESTS[0]: [],
    TESTS[1]: ["pruebas/" + TESTS[0]],
    TESTS[2]: ["pruebas/" + TESTS[0]],
    TESTS[3]: [
        "datos/EVALUACION_VACIO.json",
        "datos/datos_generados/pi_1000_decimales.txt",
        "datos/datos_generados/phi_1000_decimales.txt",
        "datos/datos_generados/e_1000_decimales.txt",
    ],
    TESTS[4]: [
        "pruebas/" + TESTS[3],
        "propietarios/composicion_contraangulo.tex",
        "demostraciones/SUSTITUCION_CONTRAANGULO_Y_G.md",
    ],
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def relative_files():
    return sorted(
        p for p in ROOT.rglob("*")
        if p.is_file() and p.name != "MANIFIESTO_LOCAL.json"
        and "resultados" not in p.relative_to(ROOT).parts
        and "__pycache__" not in p.parts
    )


def register_provenance():
    """Maintenance operation; never called by the ordinary check."""
    origins = json.loads((ROOT / "procedencia/ORIGENES.json").read_text(encoding="utf-8"))
    records = []
    for record in origins["records"]:
        source = Path(record["source"])
        copy = ROOT / record["copy"]
        original_hash, copy_hash = digest(source), digest(copy)
        if record["adaptation"] == "Copia exacta." and original_hash != copy_hash:
            raise RuntimeError("Copia alterada: " + record["copy"])
        diff = ""
        if original_hash != copy_hash:
            diff = "".join(difflib.unified_diff(
                source.read_text(encoding="utf-8").splitlines(keepends=True),
                copy.read_text(encoding="utf-8").splitlines(keepends=True),
                fromfile="original/" + source.name,
                tofile=record["copy"],
            ))
        records.append({**record, "source_sha256": original_hash,
                        "copy_sha256": copy_hash, "exact_copy": original_hash == copy_hash,
                        "adaptation_diff": diff})
    write_json(ROOT / "procedencia/PROCEDENCIA_SHA256.json", {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "records": records,
        "original_paths_are_runtime_dependencies": False,
    })
    write_json(ROOT / "MANIFIESTO_LOCAL.json", {
        "algorithm": "SHA-256",
        "files": {str(p.relative_to(ROOT)).replace("\\", "/"): {
            "sha256": digest(p), "bytes": p.stat().st_size} for p in relative_files()},
        "excluded": ["resultados/**", "**/__pycache__/**", "MANIFIESTO_LOCAL.json"],
    })


def verify_inventory():
    manifest = json.loads((ROOT / "MANIFIESTO_LOCAL.json").read_text(encoding="utf-8"))
    failures = []
    for rel, entry in manifest["files"].items():
        p = ROOT / rel
        if not p.is_file() or digest(p) != entry["sha256"] or p.stat().st_size != entry["bytes"]:
            failures.append(rel)
    if failures:
        raise RuntimeError("Integridad local: " + ", ".join(failures))
    return {"verified_files": len(manifest["files"]),
            "verified_bytes": sum(e["bytes"] for e in manifest["files"].values())}


def verify_imports():
    imports = {}
    for name in TESTS:
        path = ROOT / "pruebas" / name
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module.split(".")[0])
        external = modules - AUDITED_STANDARD_MODULES
        if external:
            raise RuntimeError("Import externo: " + name + ": " + repr(external))
        if "/Users/" in source or "/home/" in source or "C:\\" in source:
            raise RuntimeError("Ruta absoluta en verificador: " + name)
        for rel in LOCAL_DEPENDENCIES[name]:
            if not (ROOT / rel).is_file():
                raise RuntimeError("Dependencia local ausente: " + rel)
        imports[name] = {"standard_library": sorted(modules),
                         "local_dependencies": LOCAL_DEPENDENCIES[name]}
    return imports


def run_tests():
    if not __debug__:
        raise RuntimeError("No ejecutar con -O: las pruebas necesitan aserciones activas.")
    inventory = verify_inventory()
    imports = verify_imports()
    results = ROOT / "resultados"
    results.mkdir(exist_ok=True)
    summary = []
    with tempfile.TemporaryDirectory(prefix="hmt_focal_cwd_") as temp:
        for name in TESTS:
            command = [sys.executable, "-I", "-B", "-S", str(ROOT / "pruebas" / name)]
            run = subprocess.run(command, cwd=temp, capture_output=True, text=True, check=False)
            if run.returncode:
                raise RuntimeError(name + "\n" + run.stdout + "\n" + run.stderr)
            result = json.loads(run.stdout)
            if not result.get("status", "").startswith("PASS_"):
                raise RuntimeError(name + ": " + run.stdout)
            write_json(results / (Path(name).stem + ".json"), result)
            summary.append({"script": "pruebas/" + name, "status": result["status"],
                            "exit_code": run.returncode,
                            "exact_checks": result.get("exact_checks"),
                            "exact_radial_cases": result.get("exact_radial_cases"),
                            "stable_significant_digits": result.get("stable_significant_digits"),
                            "checks_at_each_precision": result.get("checks_at_each_precision"),
                            "command_flags": ["-I", "-B", "-S"],
                            "cwd_outside_package": not Path(temp).is_relative_to(ROOT),
                            "stderr": run.stderr})
    report = {
        "status": "PASS_REPRODUCCION_FOCAL_PORTABLE",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "invocation_cwd": str(Path.cwd()),
        "package": str(ROOT),
        "inventory": inventory,
        "imports_and_local_dependencies": imports,
        "tests": summary,
        "runtime_source_machine_paths_required": False,
        "APP_TRIT_TPK_regenerated": False,
        "K_selection_reexecuted": False,
        "Lean_certification_performed": False,
        "native_Windows_execution_performed": platform.system() == "Windows",
        "PDFs_modified": False,
    }
    write_json(results / "INFORME_REPRODUCCION.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registrar-procedencia", action="store_true",
                        help="Mantenimiento: registra originales disponibles y sella la copia local.")
    args = parser.parse_args()
    if args.registrar_procedencia:
        register_provenance()
    run_tests()


if __name__ == "__main__":
    main()
