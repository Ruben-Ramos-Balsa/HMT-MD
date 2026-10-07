#!/usr/bin/env python3
"""Incremental compilation of the lattice oscillator carrier and its CCR."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'PAQUETE_CONTINUIDAD_K_UNIDAD_20260918_BASE_COMPARTIDA'
SOURCE = HERE.parent / 'AMPLIACION_FORMAL_LEAN_SERIE_20260916/contributions/reviewer/V_FockTransport/SymmetricTransport.lean'
BUILD = HERE / 'fock_build'
LEAN = Path('/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    old = json.loads((BASE / 'resultados/lean_unificado/VERIFICATION.json').read_text())
    assert old['status'] == 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE'
    for row in old['modules']:
        assert sha(BASE / row['source']) == row['source_sha256']
        assert sha(BASE / 'resultados/lean_unificado/build' / (row['module'] + '.olean')) == row['object_sha256']
    BUILD.mkdir(exist_ok=True)
    env = dict(os.environ, LEAN_PATH=os.pathsep.join([
        str(BUILD), str(HERE / 'algebra_build'), old['lean_path']]))
    names = sys.argv[1:] or ['SymmetricTransport', 'LatticeOscillatorFock']
    rows = []
    for name in names:
        source = SOURCE if name == 'SymmetricTransport' else HERE / (name + '.lean')
        target = BUILD / source.name
        shutil.copy2(source, target)
        command = [str(LEAN), '-DwarningAsError=true', '--root=' + str(BUILD),
            '-o', str(BUILD / (name + '.olean')), str(target)]
        p = subprocess.run(command, cwd=old['mathlib'], env=env, capture_output=True,
            text=True, timeout=240)
        log = p.stdout + p.stderr
        (BUILD / (name + '.log')).write_text(log)
        axioms = sorted({a.strip() for group in re.findall(
            r'depends on axioms:\s*\[([^]]*)\]', log) for a in group.split(',') if a.strip()})
        row = dict(module=name, source=str(source), source_sha256=sha(source),
            exit_code=p.returncode, output=log, axioms=axioms, command=command)
        rows.append(row)
        print(name + ': ' + str(p.returncode), flush=True)
        print(log, flush=True)
        if p.returncode or set(axioms) - {'propext', 'Classical.choice', 'Quot.sound', 'Lean.ofReduceBool'}:
            raise SystemExit(1)
        row['object_sha256'] = sha(BUILD / (name + '.olean'))
    (HERE / 'FOCK_VERIFICATION.json').write_text(json.dumps(dict(
        status='PASS_LATTICE_OSCILLATOR_FOCK_INCREMENTAL', compiled=rows,
        base_receipt=str(BASE / 'resultados/lean_unificado/VERIFICATION.json'),
        whole_flm_formalized=False, lean_path=env['LEAN_PATH']), indent=2) + '\n')

if __name__ == '__main__':
    main()
