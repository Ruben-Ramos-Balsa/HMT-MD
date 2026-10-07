#!/usr/bin/env python3
"""Focal derivative of verify_fock.py; independent receipt, no package edits."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'PAQUETE_CONTINUIDAD_K_UNIDAD_20260918_BASE_COMPARTIDA'
BUILD = HERE / 'field_build'
LEAN = Path('/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    old = json.loads((BASE / 'resultados/lean_unificado/VERIFICATION.json').read_text())
    assert old['status'] == 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE'
    for row in old['modules']:
        assert sha(BASE / row['source']) == row['source_sha256']
        assert sha(BASE / 'resultados/lean_unificado/build' / (row['module'] + '.olean')) == row['object_sha256']
    direct_source = HERE / 'LatticeOscillatorFock.lean'
    assert sha(direct_source) == sha(HERE / 'fock_build/LatticeOscillatorFock.lean')
    antecedents = {str(p): sha(p) for d in ('algebra_build', 'fock_build')
                   for p in (HERE / d).glob('*.olean')}
    BUILD.mkdir(exist_ok=True)
    source = HERE / 'LatticeFieldTruncation.lean'
    snapshot = BUILD / source.name
    shutil.copy2(source, snapshot)
    env = dict(os.environ, LEAN_PATH=os.pathsep.join([
        str(BUILD), str(HERE / 'fock_build'), str(HERE / 'algebra_build'), old['lean_path']]))
    obj = BUILD / 'LatticeFieldTruncation.olean'
    command = [str(LEAN), '-DwarningAsError=true', '--root=' + str(BUILD),
               '-o', str(obj), str(snapshot)]
    p = subprocess.run(command, cwd=old['mathlib'], env=env,
                       capture_output=True, text=True, timeout=240)
    output = p.stdout + p.stderr
    (BUILD / 'LatticeFieldTruncation.log').write_text(output)
    print(output, flush=True)
    axioms = sorted({a.strip() for group in re.findall(
        r'depends on axioms:\s*\[([^]]*)\]', output) for a in group.split(',') if a.strip()})
    unchanged = all(sha(Path(path)) == digest for path, digest in antecedents.items())
    okay = (p.returncode == 0 and unchanged and
            not (set(axioms) - {'propext', 'Classical.choice', 'Quot.sound'}) and
            sha(source) == sha(snapshot))
    receipt = dict(status='PASS_LATTICE_FIELD_TRUNCATION' if okay else 'FAIL',
                   source=str(source), source_sha256=sha(source), command=command,
                   exit_code=p.returncode, output=output, axioms=axioms,
                   object_sha256=sha(obj) if p.returncode == 0 else None,
                   antecedent_objects=antecedents, antecedents_unchanged=unchanged,
                   lean_path=env['LEAN_PATH'], source_modified=False,
                   proof_scope='Pointwise annihilation truncation on algebraic Fock and lattice carrier; no VOA locality or FLM claim.')
    (HERE / 'FIELD_TRUNCATION_VERIFICATION.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(receipt['status'], flush=True)
    return 0 if okay else 1

if __name__ == '__main__':
    raise SystemExit(main())
