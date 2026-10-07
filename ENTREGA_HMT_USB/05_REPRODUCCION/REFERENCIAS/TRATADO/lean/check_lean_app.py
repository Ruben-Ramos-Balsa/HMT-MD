#!/usr/bin/env python3
"""Ejecuta el núcleo Lean local y registra exclusivamente el resultado APP."""

from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
LEAN = Path(os.environ.get('LEAN', shutil.which('lean') or str(Path.home() / '.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean')))
SOURCE = ROOT / "lean/APPRestitution.lean"
BUILD = ROOT / "lean/build"
RECEIPT = ROOT / "metadata/RECIBO_LEAN_APP.json"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    content = SOURCE.read_text(encoding="utf-8")
    forbidden = re.findall(r"\b(?:sorry|admit|axiom|native_decide)\b", content)
    if forbidden:
        raise RuntimeError(f"Construcciones excluidas en la fuente: {forbidden}")
    imports = re.findall(r"^import\s+(.+)$", content, re.MULTILINE)
    if imports != ["Std"]:
        raise RuntimeError(f"Dependencias distintas de Std: {imports}")
    BUILD.mkdir(parents=True, exist_ok=True)
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    version = subprocess.run([str(LEAN), "--version"], text=True, capture_output=True, check=True).stdout.strip()
    if "version 4.21.0" not in version:
        raise RuntimeError(f"Versión inesperada: {version}")
    output = BUILD / "APPRestitution.olean"
    command = [str(LEAN), "-o", str(output), str(SOURCE)]
    proc = subprocess.run(command, cwd=ROOT / "lean", text=True, capture_output=True)
    log = BUILD / "lean-output.txt"
    log.write_text(proc.stdout + proc.stderr, encoding="utf-8")
    axioms = {}
    for line in proc.stdout.splitlines():
        match = re.match(r"'([^']+)' depends on axioms: \[(.*)\]", line)
        if match:
            axioms[match.group(1)] = [x.strip() for x in match.group(2).split(",") if x.strip()]
    names = [
        "rho9_bounds", "reconstruct", "recover_residue", "recover_quotient",
        "reconstruction_unique", "decode_encode", "encode_decode",
        "encode_injective", "encode_surjective", "encode_bijective",
    ]
    expected = {"HMT.APP." + name for name in names}
    complete = proc.returncode == 0 and expected == set(axioms) and output.exists()
    prohibited_axioms = sorted({a for xs in axioms.values() for a in xs if a not in {"propext", "Classical.choice", "Quot.sound"}})
    passed = complete and not prohibited_axioms
    receipt = {
        "schema_version": "1.0",
        "status": "PASS_LEAN_APP_RESTITUCION_UNIVERSAL" if passed else "FAIL_LEAN_APP_RESTITUCION_UNIVERSAL",
        "scope": "APP_INTERNAL",
        "causal_cutoff": "APP",
        "provenance_status": "CERTIFICADO_NUEVO",
        "lean_version": version,
        "runtime": str(LEAN),
        "imports": imports,
        "command": command,
        "exit_code": proc.returncode,
        "source": {"path": str(SOURCE), "sha256": digest(SOURCE)},
        "compiled_object": {"path": str(output), "sha256": digest(output) if output.exists() else None},
        "log": {"path": str(log), "sha256": digest(log)},
        "axioms_by_theorem": axioms,
        "unexpected_axioms": prohibited_axioms,
        "universal_statements": {
            "rho9_bounds": "forall n:Nat, 1 <= rho9(n) and rho9(n) <= 9",
            "reconstruct": "forall n:Nat, 0<n -> n=rho9(n)+9*q9(n)",
            "recover_residue": "forall r,q:Nat, 1<=r -> r<=9 -> rho9(r+9*q)=r",
            "recover_quotient": "forall r,q:Nat, 1<=r -> r<=9 -> q9(r+9*q)=q",
            "reconstruction_unique": "forall n,r,q:Nat, 0<n -> 1<=r -> r<=9 -> n=r+9*q -> (rho9(n)=r and q9(n)=q)",
            "decode_encode": "forall n:Positive, decode(encode(n))=n",
            "encode_decode": "forall rq:Digit9 x Nat, encode(decode(rq))=rq",
            "encode_bijective": "encode:Positive -> Digit9 x Nat is injective and surjective",
        },
        "definitions": {"rho9(n)": "(n-1)%9+1", "q9(n)": "(n-1)/9", "Positive": "{n:Nat // 0<n}", "Digit9": "{r:Nat // 1<=r and r<=9}", "decode(r,q)": "r+9*q"},
        "chapter_correspondence": {"path": str(ROOT / "source/integral/fuente/manuscrito/ampliacion_20260919/01_app.tex"), "anchors": ["def:app-residuo", "eq:app-rho-q", "thm:app-reconstruccion"]},
        "verification_kind": "UNIVERSAL_LEAN_KERNEL_PROOFS",
        "finite_testing_used_as_proof": False,
        "new_axioms_declared": False,
        "network_used": False,
        "mathlib_used": False,
        "global_HMT_certification": False,
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    print(receipt["status"])
    print(RECEIPT)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
