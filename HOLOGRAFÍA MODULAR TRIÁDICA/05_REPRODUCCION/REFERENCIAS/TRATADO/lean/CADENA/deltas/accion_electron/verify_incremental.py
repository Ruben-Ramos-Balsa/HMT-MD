#!/usr/bin/env python3
"""Compile only this delta; accurately record the reused dependency objects."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--dependency-path", default=os.environ.get("LEAN_PATH", ""))
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--modules", nargs="+", default=[
        "SelectedActionDomain", "ElectronOrientationBridge",
        "SelectedElectronPublication", "SelectedArticleIComposition"])
    parser.add_argument("--result-id", default="PASS_SELECTED_ACTION_ELECTRON_INCREMENTAL")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    build = out / "build"
    build.mkdir(exist_ok=True)
    if any(build.iterdir()):
        raise SystemExit("Output build directory must be empty; use a new output directory")
    names = args.modules
    if len(set(names)) != len(names):
        raise SystemExit("Duplicate module in compilation order")
    for name in names:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            raise SystemExit("Invalid local module name: " + name)
        if not (root / (name + ".lean")).is_file():
            raise SystemExit("Required source is missing: " + name)
    dep_dirs = [Path(p) for p in args.dependency_path.split(os.pathsep) if p]
    if not dep_dirs:
        raise SystemExit("Supply the already verified dependency object path")
    env = dict(os.environ)
    env["LEAN_PATH"] = os.pathsep.join(map(str, [build] + dep_dirs))
    source_inputs = {}
    reused = {}
    for index, name in enumerate(names):
        source = root / (name + ".lean")
        body = source.read_text()
        if re.search(r"^\s*(?:axiom|constant)\s|\b(?:sorry|admit|sorryAx)\b", body,
                     re.MULTILINE):
            raise SystemExit("Unproved declaration or placeholder in " + name)
        source_inputs[name] = {"path": str(source), "sha256": digest(source)}
        for imp in re.findall(r"^import\s+([\w.]+)\s*$", body, re.MULTILINE):
            if imp in names:
                if names.index(imp) >= index:
                    raise SystemExit("Local dependencies must precede their consumers: " + imp)
                continue
            target = Path(*imp.split(".")).with_suffix(".olean")
            found = next((folder / target for folder in dep_dirs
                          if (folder / target).is_file()), None)
            if found is None:
                raise SystemExit("Unresolved dependency " + imp)
            reused[imp] = {"path": str(found), "sha256": digest(found)}
    allowed = {"propext", "Classical.choice", "Quot.sound", "Lean.ofReduceBool"}
    results = []
    version = subprocess.run([str(args.lean), "--version"], check=True,
                             capture_output=True, text=True).stdout.strip()
    for name in names:
        command = [str(args.lean), "-DwarningAsError=true", "-o",
                   str(build / (name + ".olean")), name + ".lean"]
        start = time.monotonic()
        process = subprocess.run(command, cwd=root, env=env, text=True,
                                 capture_output=True)
        log = process.stdout + process.stderr
        (out / (name + ".log")).write_text(log)
        axioms = {}
        for decl, block in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",
                                      log, re.DOTALL):
            values = [x.strip() for x in block.split(",") if x.strip()]
            unexpected = set(values) - allowed
            if unexpected:
                raise SystemExit("Unexpected axioms: " + repr(unexpected))
            axioms[decl] = values
        record = {"module": name, "source_sha256": source_inputs[name]["sha256"],
                  "exit_code": process.returncode,
                  "seconds": round(time.monotonic() - start, 3),
                  "command": command, "axiom_queries": axioms,
                  "log_sha256": digest(out / (name + ".log"))}
        results.append(record)
        if process.returncode or not axioms:
            print(log)
            raise SystemExit("Compilation or axiom-query failure: " + name)
        print("PASS " + name, flush=True)
    receipt = {
        "status": args.result_id,
        "lean_version": version,
        "verifier_sha256": digest(Path(__file__).resolve()),
        "verification_kind": "new_sources_compiled_with_reused_dependency_objects",
        "fresh_transitive_dependency_rebuild": False,
        "source_inputs": source_inputs,
        "reused_direct_objects": reused,
        "results": results,
        "trust_boundary": "Finite terminal selector uses Lean.ofReduceBool; remaining queries are explicit.",
        "remaining_upstream_interface": "Unordered S8 in the imported regional orbital selector.",
        "no_fitted_ledger_constructed": True,
        "physical_basis_and_mass_refinement": "Explicit typed parameters, not inferred from numerical agreement.",
        "pdf_and_latex_modified": False,
    }
    (out / "VERIFICATION.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(receipt["status"])


if __name__ == "__main__":
    main()
