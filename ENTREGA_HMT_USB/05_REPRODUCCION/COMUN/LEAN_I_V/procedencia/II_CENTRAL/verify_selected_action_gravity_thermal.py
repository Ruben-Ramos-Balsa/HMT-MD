"""Compile only the selected II delta against the preserved Article I build."""
from pathlib import Path
import hashlib
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'SelectedActionGravityThermal.lean'
LEAN = Path('/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean')
BASE = Path('/Users/ruben/Documents/New project/output/ARTICLE_I_PUBLICACION_PRINCIPAL_20260922/reproduction/exceptional/build')
PACKAGE = Path('/Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_PUBLICACION_PRINCIPAL_20260922')
REGISTRY = json.loads((PACKAGE / 'REGISTRO_REPRODUCCION.json').read_text())
IMPORTED_SOURCE = PACKAGE / REGISTRY['modules']['SelectedActionDomain']['source']
MATHLIB = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/FORMALIZACION_PRINCIPALES_20260916/deps/mathlib4')
OUT = ROOT / 'verification_action_gravity_thermal'
OUT.mkdir(exist_ok=True)
OBJECT = OUT / 'SelectedActionGravityThermal.olean'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

paths = [ROOT, BASE, MATHLIB / '.lake/build/lib/lean']
paths.extend(sorted((MATHLIB / '.lake/packages').glob('*/.lake/build/lib/lean')))
env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, paths)))
command = [str(LEAN), '-DwarningAsError=true', '-o', str(OBJECT), str(SOURCE)]
result = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True)
log = result.stdout + result.stderr
(OUT / 'compilation.log').write_text(log)
receipt = {
    'status': 'PASS_SELECTED_ACTION_GRAVITY_THERMAL' if result.returncode == 0 else 'FAIL_COMPILATION',
    'exit_code': result.returncode,
    'source': str(SOURCE), 'source_sha256': sha(SOURCE),
    'object': str(OBJECT), 'object_sha256': sha(OBJECT) if OBJECT.exists() and result.returncode == 0 else None,
    'lean': str(LEAN), 'lean_sha256': sha(LEAN),
    'lean_version': subprocess.run([str(LEAN), '--version'], text=True, capture_output=True).stdout.strip(),
    'mathlib_commit': subprocess.run(['git', '-C', str(MATHLIB), 'rev-parse', 'HEAD'], text=True, capture_output=True).stdout.strip(),
    'imported_selected_source': str(IMPORTED_SOURCE),
    'imported_selected_source_sha256': sha(IMPORTED_SOURCE),
    'imported_selected_object_sha256': sha(BASE / 'SelectedActionDomain.olean'),
    'command': command, 'lean_path': list(map(str, paths)),
    'terminal': 'HMT.II.SelectedActionGravityThermal.selected_action_gravity_thermal_chain',
    'hypotheses': ['U > 0', 'c > 0', 't0 > 0', 'Theta > 0'],
    'scope': 'Circular realization and unique transducer on the same selected regional action; no numerical SI selection or new Ledger.',
    'axiom_output': log,
    'antecedents_modified': False,
}
(OUT / 'VERIFICATION.json').write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n')
print(log)
print(receipt['status'])
raise SystemExit(result.returncode)
