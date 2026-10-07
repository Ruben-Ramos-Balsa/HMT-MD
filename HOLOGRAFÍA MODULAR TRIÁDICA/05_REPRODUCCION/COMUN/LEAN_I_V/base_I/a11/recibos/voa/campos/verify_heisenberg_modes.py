#!/usr/bin/env python3
"""Verify the all-integer Heisenberg relation; keep an independent receipt."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'PAQUETE_CONTINUIDAD_K_UNIDAD_20260918_BASE_COMPARTIDA'
LEAN = Path('/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    base_receipt = BASE / 'resultados/lean_unificado/VERIFICATION.json'
    base = json.loads(base_receipt.read_text())
    if base['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE':
        raise SystemExit('Base closure does not carry its expected receipt')
    source = HERE / 'LatticeHeisenbergModes.lean'
    target = HERE / 'fock_build/LatticeHeisenbergModes.olean'
    text = source.read_text()
    if re.search(r'\b(?:sorry|admit|axiom|native_decide)\b', text):
        raise SystemExit('Forbidden placeholder or external computation found')
    deps = [HERE / 'fock_build/LatticeOscillatorFock.olean',
            HERE / 'fock_build/SymmetricTransport.olean',
            HERE / 'fock_build/WittLatticeZeroModes.olean']
    if not all(p.is_file() for p in deps):
        raise SystemExit('Unresolved imported object')
    before = {str(p): sha(p) for p in deps}
    env = dict(os.environ, LEAN_PATH=os.pathsep.join([
        str(HERE / 'fock_build'), str(HERE / 'algebra_build'), base['lean_path']]))
    command = [str(LEAN), '-DwarningAsError=true', '--root=' + str(HERE),
               '-o', str(target), str(source)]
    start = time.monotonic()
    run = subprocess.run(command, cwd=base['mathlib'], env=env,
                         text=True, capture_output=True, timeout=180)
    log = run.stdout + run.stderr
    (HERE / 'LatticeHeisenbergModes.log').write_text(log)
    declarations = {}
    for name, values in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", log):
        declarations[name] = [a.strip() for a in values.split(',') if a.strip()]
    for name in re.findall(r"'([^']+)' does not depend on any axioms", log):
        declarations[name] = []
    allowed = {'propext', 'Classical.choice', 'Quot.sound'}
    unexpected = {a for group in declarations.values() for a in group} - allowed
    expected = len(re.findall(r'^#print axioms ', text, re.M))
    stable = before == {str(p): sha(p) for p in deps}
    success = run.returncode == 0 and not unexpected and len(declarations) == expected and stable
    receipt = {
        'status': 'PASS_LATTICE_HEISENBERG_MODES' if success else 'FAIL_LATTICE_HEISENBERG_MODES',
        'source': str(source), 'source_sha256': sha(source),
        'object': str(target), 'object_sha256': sha(target) if success else None,
        'compiler_exit_code': run.returncode, 'command': command,
        'seconds': round(time.monotonic()-start, 3),
        'checked_count': len(declarations), 'checked_declarations': declarations,
        'incremental': True, 'fresh_transitive_compilation': False,
        'imported_object_hashes': before, 'dependencies_stable_during_check': stable,
        'base_receipt': str(base_receipt), 'base_receipt_sha256': sha(base_receipt),
        'lean_path': env['LEAN_PATH'],
        'scope': [
            'Negative, zero and positive modes on the same algebraic lattice carrier',
            'Commuting creations, annihilations and lattice zero modes',
            'Heisenberg commutator for all integer indices and all lattice-basis directions',
            'Gram coefficients inherited from the generated marked-neighbor lattice'],
        'not_claimed': ['Vertex-operator locality', 'FLM orbifold theorem', 'Monster automorphism group'],
    }
    (HERE / 'HEISENBERG_MODES_VERIFICATION.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(log)
    print(receipt['status'])
    if not success:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
