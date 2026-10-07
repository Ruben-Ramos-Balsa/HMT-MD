#!/usr/bin/env python3
"""Pruebas universales focales de la aritmética del calendario."""
from pathlib import Path
from hashlib import sha256
import json
import os
import re
import subprocess
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
LEAN = Path(os.environ.get('LEAN', shutil.which('lean') or str(Path.home() / '.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean')))
SOURCE = ROOT / 'lean/NonadicCalendar.lean'
BUILD = ROOT / 'lean/build'
NAMES = ['decomposition', 'phase_bounds', 'phase_return', 'memory_advance',
         'inverse_boundary_zero', 'inverse_boundary_interior',
         'non_split_generator', 'carry_cocycle']


def main():
    version = subprocess.run([str(LEAN), '--version'], capture_output=True, text=True, check=True).stdout.strip()
    if 'version 4.21.0' not in version:
        raise RuntimeError('Se requiere Lean 4.21.0: ' + version)
    content = SOURCE.read_text(encoding='utf-8')
    assert not re.search(r'\b(sorry|admit|axiom|native_decide)\b', content)
    assert re.findall(r'^import\s+(.+)$', content, re.MULTILINE) == ['Std']
    BUILD.mkdir(exist_ok=True)
    output = BUILD / 'NonadicCalendar.olean'
    cmd = [str(LEAN), '-o', str(output), str(SOURCE)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    log = BUILD / 'calendar-output.txt'
    log.write_text(proc.stdout + proc.stderr, encoding='utf-8')
    axioms = {}
    for line in proc.stdout.splitlines():
        match = re.fullmatch(r"'([^']+)' depends on axioms: \[(.*)\]", line)
        if match:
            axioms[match[1]] = [a.strip() for a in match[2].split(',') if a.strip()]
    expected = {'HMT.Calendar.' + n for n in NAMES}
    allowed = {'propext', 'Classical.choice', 'Quot.sound'}
    ok = proc.returncode == 0 and set(axioms) == expected and output.exists()
    ok = ok and all(set(values) <= allowed for values in axioms.values())
    receipt = {
        'status': 'PASS_LEAN_CALENDARIO_NONADICO' if ok else 'FAIL_LEAN_CALENDARIO_NONADICO',
        'verification_kind': 'UNIVERSAL_LEAN_KERNEL_PROOFS',
        'scope': 'Euclidean phase and integer turn counter; cocycle and non-splitting obstruction',
        'lean_version': version,
        'command': cmd,
        'source_sha256': sha256(SOURCE.read_bytes()).hexdigest(),
        'compiled_sha256': sha256(output.read_bytes()).hexdigest() if output.exists() else None,
        'axioms_by_theorem': axioms,
        'global_HMT_certification': False,
        'new_axioms_declared': False,
        'finite_checks_used_as_universal_proof': False,
        'chapter': str(ROOT / 'source/integral/fuente/manuscrito/ampliacion_20260919/05_calendario_memoria.tex'),
    }
    path = ROOT / 'metadata/RECIBO_LEAN_CALENDARIO.json'
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(proc.stdout + proc.stderr)
    print(receipt['status'])
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
