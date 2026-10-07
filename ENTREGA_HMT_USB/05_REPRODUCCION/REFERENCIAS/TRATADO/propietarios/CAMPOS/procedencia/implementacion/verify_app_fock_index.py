#!/usr/bin/env python3
"""Incrementally verify the actual finite U030 APP--Fock operator and its trace."""
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
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mathlib', required=True, type=Path)
    p.add_argument('--dependency-build', required=True, type=Path)
    p.add_argument('--lake', required=True, type=Path)
    a = p.parse_args()
    root = Path(__file__).resolve().parent
    src, obj = root / 'APPFockIndex.lean', root / 'APPFockIndex.olean'
    text = src.read_text()
    if re.search(r'\b(?:sorry|admit|axiom|native_decide)\b', text):
        raise SystemExit('Unproved declaration, placeholder, or native certificate')
    dependencies = [root / 'APPFockRigidity.olean',
                    a.dependency_build / 'APPArithmetic.olean']
    if not all(d.is_file() for d in dependencies):
        raise SystemExit('Missing incremental dependency')
    env = dict(os.environ)
    env['LEAN_PATH'] = os.pathsep.join([str(root), str(a.dependency_build.resolve())])
    cmd = [str(a.lake), 'env', 'lean', '--root=' + str(root),
           '-DwarningAsError=true', '-o', str(obj), str(src)]
    start = time.monotonic()
    result = subprocess.run(cmd, cwd=a.mathlib, env=env, text=True, capture_output=True)
    log = result.stdout + result.stderr
    (root / 'APPFockIndex.log').write_text(log)
    checked = {}
    for name, values in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", log):
        checked[name] = [v.strip() for v in values.split(',') if v.strip()]
    for name in re.findall(r"'([^']+)' does not depend on any axioms", log):
        checked[name] = []
    allowed = {'propext', 'Classical.choice', 'Quot.sound'}
    unexpected = {x for axioms in checked.values() for x in axioms} - allowed
    expected = len(re.findall(r'^#print axioms ', text, re.M))
    success = result.returncode == 0 and not unexpected and len(checked) == expected
    receipt = {
        'status': 'PASS_APP_FOCK_INDEX' if success else 'FAIL_APP_FOCK_INDEX',
        'source': str(src), 'source_sha256': sha(src),
        'object_sha256': sha(obj) if success else None,
        'command': cmd, 'compiler_exit_code': result.returncode,
        'seconds': round(time.monotonic() - start, 3),
        'incremental': True, 'fresh_transitive_compilation': False,
        'dependencies': [{'path': str(d), 'sha256': sha(d)} for d in dependencies],
        'mathlib_commit': subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], cwd=a.mathlib, text=True).strip(),
        'checked_declarations': checked, 'checked_count': len(checked),
        'source_owner': 'Integral/U030, capitulo_21_c20_lineas_1_2612.tex:2274-2612',
        'scope': [
            '24-coordinate twelve-fibre oriented Coxeter matrix',
            'Full 300-by-300 symmetric-tensor matrix, not a supplied trace',
            'Compatibility of symmetric-square matrix with sheet parity',
            'Computed traces: g=-12, Eg=0, Sym2(g)=66, Sym2(Eg)=-6',
            '324-dimensional degree-two graded operator with trace 54',
            'Coupling from APP-generated aggregate with computed oriented index 54',
            'Equality with radial norm polynomial at m=12',
            'Zero-residue perturbation preserves coupling but changes digital weight'],
        'not_claimed': ['Infinite Fock product identity', 'FLM or Moonshine theorem'],
        'trace54_is_not_an_assumption': True,
        'uses_native_decide': False,
        'finite_matrix_traces_checked_by_kernel_reduction': True,
        'pdf_and_latex_modified': False,
    }
    (root / 'APPFockIndex.receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(log)
    print(receipt['status'])
    if not success:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
