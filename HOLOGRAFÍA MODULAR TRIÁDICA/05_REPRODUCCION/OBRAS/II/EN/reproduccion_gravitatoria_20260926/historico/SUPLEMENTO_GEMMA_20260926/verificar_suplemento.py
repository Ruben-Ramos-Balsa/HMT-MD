"""Verify the supplemental portable joint evaluator without resealing the base."""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_ast(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    tree.body = [n for n in tree.body if not (
        isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "UPSTREAM"
                                         for t in n.targets))]
    return ast.dump(tree, include_attributes=False)


def main():
    if not __debug__:
        raise RuntimeError("Assertions must be enabled.")
    manifest = json.loads((HERE / "MANIFIESTO_SUPLEMENTARIO.json").read_text())
    base_path = PACKAGE / "MANIFIESTO_LOCAL.json"
    if sha(base_path) != manifest["base_manifest_sha256"]:
        raise RuntimeError("Original base manifest changed.")
    base = json.loads(base_path.read_text())
    for rel, record in base["files"].items():
        path = PACKAGE / rel
        if sha(path) != record["sha256"] or path.stat().st_size != record["bytes"]:
            raise RuntimeError("Base file mismatch: " + rel)
    for rel, record in manifest["supplement_files"].items():
        path = HERE / rel
        if sha(path) != record["sha256"] or path.stat().st_size != record["bytes"]:
            raise RuntimeError("Supplement file mismatch: " + rel)
    original = HERE / "originales/gravedad_estructural.py"
    adapted = HERE / "gravedad_estructural.py"
    if normalized_ast(original) != normalized_ast(adapted):
        raise RuntimeError("AST differs beyond UPSTREAM path adaptation.")
    command = [sys.executable, "-I", "-B", "-S", str(adapted)]
    with tempfile.TemporaryDirectory(prefix="hmt_joint_portable_") as temp:
        completed = subprocess.run(command, cwd=temp, capture_output=True, text=True, check=False)
        execution_cwd = temp
    if completed.returncode:
        raise RuntimeError(completed.stdout + completed.stderr)
    report = json.loads(completed.stdout)
    reference = json.loads((HERE / "referencia/EVALUACION_CONJUNTA_ORIGEN.json").read_text())
    compared = ["status", "working_precisions", "stable_significant_digits", "G_measured_input",
                "Planck_length_tabulated_input", "full_generator_rerun", "physical_realization", "result"]
    for field in compared:
        if report[field] != reference[field]:
            raise RuntimeError("Reproduced field differs from archived result: " + field)
    if len(report["result"]["identities"]) != 9 or report["stable_significant_digits"] != 71:
        raise RuntimeError("Unexpected verification scope.")
    for path, expected in report["sha256"].items():
        local = Path(path).resolve()
        if not local.is_relative_to(PACKAGE.resolve()):
            raise RuntimeError("Evaluator used a file outside local package: " + path)
        if sha(local) != expected:
            raise RuntimeError("Runtime input hash mismatch: " + path)
    outputs = HERE / "resultados"
    outputs.mkdir(exist_ok=True)
    (outputs / "EVALUACION_CONJUNTA_PORTABLE.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {
        "status": "PASS_SUPLEMENTO_CONJUNTO_PORTABLE", "created_utc": datetime.now(timezone.utc).isoformat(),
        "command": command, "cwd": execution_cwd, "exit_code": completed.returncode,
        "stderr": completed.stderr, "compared_fields": compared,
        "values_identical_to_archived": len(report["result"]["values"]),
        "identities": report["result"]["identities"], "stable_significant_digits": 71,
        "AST_unchanged_except_UPSTREAM": True, "base_manifest_preserved": True,
        "base_manifest_sha256": sha(base_path), "supplement_manifest_sha256": sha(HERE / "MANIFIESTO_SUPLEMENTARIO.json"),
        "scope": {"archived_upstream_outputs_reused": True, "full_generator_rerun": False,
                  "K_selection_reexecuted": False, "Lean_checked": False,
                  "experimental_precision_claimed": False, "final_distribution": False},
    }
    (outputs / "RECIBO_SUPLEMENTO.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
