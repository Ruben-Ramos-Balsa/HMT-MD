#!/usr/bin/env python3
"""Compile the actual current fields after verified truncation and modes."""
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
BUILD = HERE / 'field_build'
LEAN = Path('/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    old = json.loads((BASE / 'resultados/lean_unificado/VERIFICATION.json').read_text())
    if old['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE':
        raise RuntimeError('The shared base has not passed')
    for row in old['modules']:
        assert sha(BASE / row['source']) == row['source_sha256']
        assert sha(BASE / 'resultados/lean_unificado/build' / (row['module'] + '.olean')) == row['object_sha256']
    env = dict(os.environ, LEAN_PATH=os.pathsep.join([
        str(BUILD), str(HERE / 'modes_build'), str(HERE / 'heisenberg_build'),
        str(HERE / 'fock_build'), str(HERE / 'algebra_build'), old['lean_path']]))
    rows = []
    for name in sys.argv[1:] or ['LatticeHeisenbergField']:
        source = HERE / (name + '.lean')
        snapshot = BUILD / source.name
        shutil.copy2(source, snapshot)
        obj = BUILD / (name + '.olean')
        command = [str(LEAN), '-DwarningAsError=true', '--root=' + str(BUILD),
                   '-o', str(obj), str(snapshot)]
        p = subprocess.run(command, cwd=old['mathlib'], env=env,
                           capture_output=True, text=True, timeout=240)
        output = p.stdout + p.stderr
        (BUILD / (name + '.log')).write_text(output)
        print(name + ': ' + str(p.returncode), flush=True)
        print(output, flush=True)
        axioms = sorted({a.strip() for group in re.findall(
            r'depends on axioms:\s*\[([^]]*)\]', output) for a in group.split(',') if a.strip()})
        okay = (p.returncode == 0 and not (set(axioms) -
                {'propext', 'Classical.choice', 'Quot.sound', 'Lean.ofReduceBool'}))
        row = dict(module=name, source=str(source), source_sha256=sha(source),
                   command=command, exit_code=p.returncode, output=output, axioms=axioms,
                   object_sha256=sha(obj) if p.returncode == 0 else None)
        rows.append(row)
        if not okay:
            return 1
    result = dict(status='PASS_HEISENBERG_FIELDS_INCREMENTAL', modules=rows,
                  lean_path=env['LEAN_PATH'], full_lattice_voa_claimed=False,
                  whole_flm_formalized=False)
    (HERE / 'HEISENBERG_FIELDS_VERIFICATION.json').write_text(json.dumps(result, indent=2) + '\n')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
