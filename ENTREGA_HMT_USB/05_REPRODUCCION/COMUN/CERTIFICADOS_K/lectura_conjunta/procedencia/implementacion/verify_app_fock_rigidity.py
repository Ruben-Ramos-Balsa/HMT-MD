#!/usr/bin/env python3
"""Incremental Lean check of the recovered U030 arithmetic delta."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mathlib', required=True, type=Path)
    parser.add_argument('--dependency-build', required=True, type=Path)
    parser.add_argument('--lake', required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    src = root / 'APPFockRigidity.lean'
    obj = root / 'APPFockRigidity.olean'
    dep = args.dependency_build.resolve() / 'APPArithmetic.olean'
    if not dep.is_file():
        raise SystemExit('Unresolved APPArithmetic object')
    text = src.read_text()
    if re.search(r'\b(?:sorry|admit|axiom)\b', text):
        raise SystemExit('Unproved declaration or placeholder')
    env = dict(os.environ)
    env['LEAN_PATH'] = str(args.dependency_build.resolve())
    cmd = [str(args.lake), 'env', 'lean', '--root=' + str(root),
           '-DwarningAsError=true', '-o', str(obj), str(src)]
    start = time.monotonic()
    p = subprocess.run(cmd, cwd=args.mathlib, env=env, text=True,
                       capture_output=True)
    log = p.stdout + p.stderr
    (root / 'APPFockRigidity.log').write_text(log)
    queries = {}
    for name, values in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", log):
        queries[name] = [v.strip() for v in values.split(',') if v.strip()]
    for name in re.findall(r"'([^']+)' does not depend on any axioms", log):
        queries[name] = []
    allowed = {'propext', 'Classical.choice', 'Quot.sound'}
    bad = {a for values in queries.values() for a in values} - allowed
    expected = len(re.findall(r'^#print axioms ', text, re.M))
    success = p.returncode == 0 and not bad and len(queries) == expected
    receipt = {
        'status': 'PASS_APP_FOCK_RIGIDITY' if success else 'FAIL_APP_FOCK_RIGIDITY',
        'source': str(src), 'source_sha256': sha(src),
        'object_sha256': sha(obj) if success else None,
        'command': cmd, 'compiler_exit_code': p.returncode,
        'seconds': round(time.monotonic() - start, 3),
        'incremental': True, 'fresh_transitive_compilation': False,
        'reused_direct_object': {'path': str(dep), 'sha256': sha(dep)},
        'mathlib_commit': subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], cwd=args.mathlib, text=True).strip(),
        'checked_declarations': queries, 'checked_count': len(queries),
        'source_owner': 'Integral/U030, capitulo_21_c20_lineas_1_2612.tex:2274-2612',
        'scope': ['APP-generated two-leaf aggregate and balanced unit coefficient',
                  'Arithmetic consequence of the oriented index formula',
                  'Cyclotomic-radial polynomial equation and positive uniqueness',
                  'Zero-residue perturbation distinguishes index and digital weight'],
        'not_claimed': ['Operator trace identification on symmetric powers',
                        'Infinite Fock product identity', 'FLM or Moonshine theorem'],
        'target_54_not_input_to_histogram': True,
        'uses_native_decide': False,
        'pdf_and_latex_modified': False,
    }
    (root / 'APPFockRigidity.receipt.json').write_text(
        json.dumps(receipt, indent=2) + '\n')
    print(log)
    print(receipt['status'])
    if not success:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
