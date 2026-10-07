#!/usr/bin/env python3
"""Compile the recovered seven-module algebra and its selected-origin adapter.

The unchanged common base is reused only after checking its source/object
hashes against its successful receipt. This is an incremental verification,
not a claim that the whole base was recompiled during this invocation.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parent
BASE = OUTPUT / 'PAQUETE_CONTINUIDAD_K_UNIDAD_20260918_BASE_COMPARTIDA'
OLD = OUTPUT / 'AMPLIACION_FORMAL_LEAN_SERIE_20260916/stage14_contributions'
BUILD = HERE / 'algebra_build'
BASE_BUILD = BASE / 'resultados/lean_unificado/build'
RECEIPT = BASE / 'resultados/lean_unificado/VERIFICATION.json'
LEAN = Path('/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean')
ORDER = [
    ('iv_lattice_cocycle', 'WittPairingParity'),
    ('iv_lattice_cocycle', 'IntegralBasisParity'),
    ('iv_lattice_cocycle', 'TriangularSignCocycle'),
    ('iv_lattice_cocycle', 'WittLatticeCocycle'),
    ('iv_twisted_group_algebra', 'WittCentralExtension'),
    ('iv_twisted_group_algebra', 'WittTwistedAlgebra'),
    ('iv_twisted_group_algebra', 'WittComplexAlgebra'),
    (None, 'SelectedLatticeAlgebra'),
]
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound', 'Lean.ofReduceBool'}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    BUILD.mkdir(exist_ok=True)
    previous = json.loads(RECEIPT.read_text())
    if previous['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE':
        raise RuntimeError('The common-base receipt is not successful')
    reused = []
    for row in previous['modules']:
        if row['exit_code'] != 0:
            raise RuntimeError('Unsuccessful antecedent: ' + row['module'])
        source = BASE / row['source']
        obj = BASE_BUILD / (row['module'].replace('.', '/') + '.olean')
        if sha(source) != row['source_sha256'] or sha(obj) != row['object_sha256']:
            raise RuntimeError('Changed common antecedent: ' + row['module'])
        reused.append({'module': row['module'], 'source': str(source),
            'source_sha256': sha(source), 'object_sha256': sha(obj)})
    env = dict(os.environ, LEAN_PATH=str(BUILD) + os.pathsep + previous['lean_path'])
    result = {'status': 'RUNNING', 'scope': 'selected lattice central extension and twisted algebra',
        'base_receipt': str(RECEIPT), 'base_receipt_sha256': sha(RECEIPT),
        'reused_base_modules': reused, 'base_recompiled': False,
        'whole_voa_formalized': False, 'lean_path': env['LEAN_PATH'], 'compiled': []}
    out = HERE / 'SELECTED_ALGEBRA_VERIFICATION.json'
    for subdir, name in ORDER:
        source = (OLD / subdir / (name + '.lean')) if subdir else HERE / (name + '.lean')
        target = BUILD / (name + '.lean')
        shutil.copy2(source, target)
        cmd = [str(LEAN), '-DwarningAsError=true', '--root=' + str(BUILD),
            '-o', str(BUILD / (name + '.olean')), str(target)]
        start = time.monotonic()
        proc = subprocess.run(cmd, env=env, cwd=previous['mathlib'],
            capture_output=True, text=True, timeout=180)
        log = proc.stdout + proc.stderr
        (BUILD / (name + '.log')).write_text(log)
        axioms = {a.strip() for group in re.findall(r'depends on axioms:\s*\[([^]]*)\]', log)
            for a in group.split(',') if a.strip()}
        row = {'module': name, 'source': str(source), 'source_sha256': sha(source),
            'command': cmd, 'elapsed_seconds': round(time.monotonic() - start, 3),
            'exit_code': proc.returncode, 'axioms': sorted(axioms), 'output': log}
        result['compiled'].append(row)
        if proc.returncode or axioms - ALLOWED or 'sorryAx' in log:
            result['status'] = 'FAIL_SELECTED_LATTICE_ALGEBRA'
            out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
            print(log)
            raise SystemExit(1)
        row['object_sha256'] = sha(BUILD / (name + '.olean'))
        print(name + ': PASS', flush=True)
    result['status'] = 'PASS_SELECTED_LATTICE_ALGEBRA_INCREMENTAL'
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(result['status'])

if __name__ == '__main__':
    main()
