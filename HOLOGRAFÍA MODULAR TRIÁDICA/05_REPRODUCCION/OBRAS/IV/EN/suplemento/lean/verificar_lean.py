#!/usr/bin/env python3
"""Compile the selected local Lean units, audit axioms, optionally reject mutations.

Only stdlib. No Lake, Elan selection, network, historical campaigns or manuscript
writes. An explicit installed Lean binary is required. No output file is written
unless --output is requested. Negative controls use a temporary child of this folder.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
ALLOWED_AXIOMS = {"propext", "Quot.sound", "Classical.choice"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command):
    p = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=120)
    return {"command": [str(x) for x in command], "exit_code": p.returncode,
            "stdout": p.stdout, "stderr": p.stderr}


def check(args):
    lean = Path(args.lean_bin).expanduser().resolve(strict=True)
    if lean.name in {"elan", "lake"} or not lean.is_file():
        raise ValueError("Use the installed toolchain's bin/lean, not an Elan/Lake launcher")
    version = run([str(lean), "--version"])
    if version["exit_code"] or not re.search(r"version 4\.21\.0\b", version["stdout"]):
        raise ValueError("Expected installed Lean4.21.0: " + version["stdout"] + version["stderr"])
    manifest = ROOT / "MAPA_TEOREMAS.json"
    units = json.loads(manifest.read_text())["units"]
    selected = [u for u in units if args.article == "ALL" or args.article in u["articles"]]
    errors, results = [], []
    for unit in selected:
        source = ROOT / unit["file"]
        if not source.resolve().is_relative_to(ROOT):
            raise ValueError("Unit outside this supplement")
        code = source.read_text()
        declarations = re.findall(r"^theorem\s+(\w+)", code, re.M)
        expected = [unit["namespace"] + "." + name for name in unit["theorems"]]
        if declarations != unit["theorems"]:
            errors.append("Declaration inventory differs: " + unit["file"])
        if re.search(r"\b(sorry|admit|axiom|native_decide)\b", code):
            errors.append("Unpermitted proof placeholder or trusted shortcut: " + unit["file"])
        imports = re.findall(r"^import\s+(.+)$", code, re.M)
        if imports != ["Std"]:
            errors.append("Unexpected import dependency: " + unit["file"])
        command = [str(lean), "-DwarningAsError=true", str(source)]
        outcome = run(command)
        printed = {}
        for name, deps in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", outcome["stdout"]):
            printed[name] = [x.strip() for x in deps.split(",") if x.strip()]
        for name in re.findall(r"'([^']+)' does not depend on any axioms", outcome["stdout"]):
            printed[name] = []
        if outcome["exit_code"] != 0:
            errors.append("Lean compilation failed: " + unit["file"])
        if set(printed) != set(expected):
            errors.append("Axiom audit inventory differs: " + unit["file"])
        for name, deps in printed.items():
            if set(deps) - ALLOWED_AXIOMS:
                errors.append("Unpermitted axiom for " + name + ": " + repr(deps))
        if unit.get("certificate_reused_byte_identical") and sha(source) != unit["source"]["sha256"]:
            errors.append("Reused certificate differs from its owner: " + unit["file"])
        results.append({"file": unit["file"], "sha256": sha(source), "declarations": printed,
                        "domain": unit["domain"], "limits": unit["limits"], **outcome})
    mutations = []
    if args.negative_controls:
        tests = [
            ("IV", "IVRegistro.lean", "x.1 + x.2.1 + x.2.2.1 + x.2.2.2,", "x.1 + x.2.1 + x.2.2.1 - x.2.2.2,", "Hadamard sign"),
            ("V", "VAcoplamiento.lean", "a.val + 9 - b.val", "a.val + 9 + b.val", "Coupling inverse sign"),
            ("V", "VFermiones.lean", "(x.1,x.2.2.1,x.2.1,-x.2.2.2)", "(x.1,x.2.2.1,x.2.1,x.2.2.2)", "Exterior exchange sign"),
            ("V", "VFactores.lean", "(1+u) * factors us", "(1-u) * factors us", "Fermionic factor sign")
        ]
        with tempfile.TemporaryDirectory(prefix=".negative-lean-", dir=ROOT) as temporary:
            for article, name, before, after, description in tests:
                if args.article != "ALL" and args.article != article:
                    continue
                code = (ROOT/name).read_text()
                if code.count(before) != 1:
                    raise ValueError("Mutation anchor must occur exactly once: " + name)
                mutant = Path(temporary)/name
                mutant.write_text(code.replace(before, after))
                outcome = run([str(lean), "-DwarningAsError=true", str(mutant)])
                rejected = outcome["exit_code"] != 0 and "error:" in outcome["stdout"]
                if not rejected:
                    errors.append("Mutation was not rejected: " + description)
                mutations.append({"mutation": description, "rejected": rejected, **outcome})
    return {"schema": "hmt.lean.iv-v.receipt.v1", "status": "PASS_LEAN_IV_V_FOCAL" if not errors else "FAIL_LEAN_IV_V_FOCAL",
            "article": args.article, "lean_binary": str(lean), "lean_binary_sha256": sha(lean),
            "lean_version": version["stdout"].strip(), "map_sha256": sha(manifest),
            "verifier_sha256": sha(Path(__file__)), "units_checked": len(results),
            "declarations_checked": sum(len(r["declarations"]) for r in results),
            "allowed_standard_axioms": sorted(ALLOWED_AXIOMS), "results": results,
            "negative_controls": mutations, "errors": errors,
            "scope": "Lean kernel-checked focal statements in the declared domains; not formalization of the entire articles, analytic limits, physical realization or upstream generators."}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--lean-bin", required=True, help="Installed toolchain binary, never a downloader")
    p.add_argument("--article", choices=("IV", "V", "ALL"), default="ALL")
    p.add_argument("--negative-controls", action="store_true")
    p.add_argument("--output", type=Path, help="New receipt; existing files are never overwritten")
    args = p.parse_args()
    try:
        result = check(args)
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        result = {"status": "FAIL_LEAN_IV_V_FOCAL", "errors": [str(exc)]}
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(rendered)
    sys.stdout.write(rendered)
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
