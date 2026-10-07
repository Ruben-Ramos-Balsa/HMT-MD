#!/usr/bin/env python3
"""Compile the selected-field composition without changing prior receipts."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'PAQUETE_CONTINUIDAD_K_UNIDAD_20260918_BASE_COMPARTIDA'
BUILD = HERE / 'selected_field_build'
LEAN = Path('/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    old = json.loads((BASE / 'resultados/lean_unificado/VERIFICATION.json').read_text())
    assert old['status'] == 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE'
    for row in old['modules']:
        assert sha(BASE / row['source']) == row['source_sha256']
        assert sha(BASE / 'resultados/lean_unificado/build' / (row['module'] + '.olean')) == row['object_sha256']
    directories = [HERE / name for name in ('field_build', 'modes_build', 'fock_build', 'algebra_build')]
    for name in ('SelectedVOAInput', 'LatticeHeisenbergField', 'LatticeHeisenbergModes'):
        directory = next((d for d in directories if (d / (name + '.olean')).is_file()), None)
        if directory is None:
            raise RuntimeError('Awaiting antecedent compilation: ' + name)
        snapshot = directory / (name + '.lean')
        if snapshot.is_file():
            if sha(HERE / (name + '.lean')) != sha(snapshot):
                raise RuntimeError('Compiled antecedent source snapshot differs: ' + name)
        elif name == 'LatticeHeisenbergModes':
            proof = json.loads((HERE / 'HEISENBERG_MODES_VERIFICATION.json').read_text())
            assert proof['status'] == 'PASS_LATTICE_HEISENBERG_MODES'
            assert sha(HERE / (name + '.lean')) == proof['source_sha256']
            assert sha(directory / (name + '.olean')) == proof['object_sha256']
        else:
            raise RuntimeError('No source snapshot or focal receipt: ' + name)
    antecedents = {str(p): sha(p) for d in directories for p in d.glob('*.olean')}
    BUILD.mkdir(exist_ok=True)
    source = HERE / 'SelectedHeisenbergInput.lean'
    snapshot = BUILD / source.name
    shutil.copy2(source, snapshot)
    env = dict(os.environ, LEAN_PATH=os.pathsep.join([str(BUILD), *map(str, directories), old['lean_path']]))
    obj = BUILD / 'SelectedHeisenbergInput.olean'
    command = [str(LEAN), '-DwarningAsError=true', '--root=' + str(BUILD),
               '-o', str(obj), str(snapshot)]
    p = subprocess.run(command, cwd=old['mathlib'], env=env,
                       capture_output=True, text=True, timeout=240)
    output = p.stdout + p.stderr
    (BUILD / 'SelectedHeisenbergInput.log').write_text(output)
    print(output, flush=True)
    axioms = sorted({a.strip() for group in re.findall(
        r'depends on axioms:\s*\[([^]]*)\]', output) for a in group.split(',') if a.strip()})
    unchanged = all(sha(Path(path)) == digest for path, digest in antecedents.items())
    okay = (p.returncode == 0 and unchanged and
            not (set(axioms) - {'propext', 'Classical.choice', 'Quot.sound', 'Lean.ofReduceBool'}) and
            sha(source) == sha(snapshot))
    receipt = dict(status='PASS_SELECTED_HEISENBERG_INPUT' if okay else 'FAIL',
                   source=str(source), source_sha256=sha(source), command=command,
                   exit_code=p.returncode, output=output, axioms=axioms,
                   object_sha256=sha(obj) if p.returncode == 0 else None,
                   antecedent_objects=antecedents, antecedents_unchanged=unchanged,
                   lean_path=env['LEAN_PATH'], source_modified=False,
                   proof_scope='Selected-lattice Heisenberg generating fields and their coefficientwise locality, retaining the existing action/electronic publication; not FLM or Moonshine.')
    (HERE / 'SELECTED_HEISENBERG_VERIFICATION.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(receipt['status'], flush=True)
    return 0 if okay else 1

if __name__ == '__main__':
    raise SystemExit(main())
