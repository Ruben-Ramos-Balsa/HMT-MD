#!/usr/bin/env python3
"""Check the all-integer-mode delta using authenticated predecessor objects."""
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import time

HERE = pathlib.Path(__file__).resolve().parent
BASE = pathlib.Path('/Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_INCIDENCIAS_ORIENTACIONES_20260920')
SOURCE = HERE / 'LatticeCoxeterHeisenbergCovariance.lean'
BUILD = HERE / 'coxeter_heisenberg_covariance_build'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    prior_path = BASE / 'resultados/lean_unificado/VERIFICATION.json'
    prior = json.loads(prior_path.read_text())
    assert prior['status'] == 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE'
    assert len(prior['modules']) == 270
    authenticated = []
    for row in prior['modules']:
        src = BASE / row['source']
        obj = BASE / 'resultados/lean_unificado/build' / (row['module'].replace('.', '/') + '.olean')
        assert sha(src) == row['source_sha256'], src
        assert sha(obj) == row['object_sha256'], obj
        authenticated += [(src, row['source_sha256']), (obj, row['object_sha256'])]
    joint_path = HERE / 'COXETER_COVARIANCE_VERIFICATION.json'
    joint = json.loads(joint_path.read_text())
    assert joint['status'] == 'PASS_COXETER_CHARGE_FIELD_COVARIANCE'
    imports = BUILD / 'imports'
    imports.mkdir(parents=True, exist_ok=True)
    for mod in ['CoxeterChargeCovariance', 'LatticeCoxeterFieldCovariance']:
        row = next(r for r in joint['sources'] if pathlib.Path(r['path']).stem == mod)
        step = next(r for r in joint['steps'] if r.get('kind') == 'compile' and r.get('module') == mod)
        src = pathlib.Path(row['path'])
        obj = HERE / (mod+'.olean')
        assert sha(src) == row['sha256'], src
        assert sha(obj) == step['olean_sha256'], obj
        authenticated += [(src, row['sha256']), (obj, step['olean_sha256'])]
        shutil.copy2(obj, imports / obj.name)
    lean = pathlib.Path(prior['compiler']['executable'])
    assert sha(lean) == prior['compiler']['binary_sha256']
    before = sha(SOURCE)
    target = BUILD / (SOURCE.stem + '.olean')
    command = [str(lean), '-DwarningAsError=true', '--root='+str(HERE), '-o', str(target), str(SOURCE)]
    env = dict(os.environ)
    env['LEAN_PATH'] = str(BUILD)+':'+str(imports)+':'+prior['lean_path']
    start = time.time()
    proc = subprocess.run(command, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (BUILD / (SOURCE.stem+'.log')).write_text(proc.stdout)
    axioms = {name: sorted(re.findall(r'[\w.]+', deps)) for name, deps in
              re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", proc.stdout)}
    allowed = {'propext', 'Classical.choice', 'Quot.sound'}
    unchanged = sha(SOURCE) == before and all(sha(p) == h for p,h in authenticated)
    ok = proc.returncode == 0 and unchanged and axioms and all(set(v) <= allowed for v in axioms.values())
    record = dict(status='PASS_COXETER_HEISENBERG_COVARIANCE' if ok else 'FAIL_COXETER_HEISENBERG_COVARIANCE',
                  source=str(SOURCE), source_sha256=before,
                  base_receipt_sha256=sha(prior_path), focal_receipt_sha256=sha(joint_path),
                  inherited_modules_authenticated=270, focal_imports_authenticated=2,
                  sources_and_objects_unchanged=unchanged,
                  command=command, lean_path=env['LEAN_PATH'], compiler=prior['compiler'],
                  elapsed_seconds=time.time()-start, exit_code=proc.returncode,
                  declarations=axioms, output=proc.stdout,
                  scope='All integer Heisenberg modes and already constructed charged fields transform under the same order-three lift, with fixed vacuum.',
                  not_claimed=['vertex-algebra reconstruction', 'Jacobi identity', 'orbifold', 'FLM theorem'],
                  object_sha256=sha(target) if proc.returncode == 0 else None)
    (BUILD / 'VERIFICATION.json').write_text(json.dumps(record, indent=2)+'\n')
    print(proc.stdout)
    print(record['status'])
    return 0 if ok else 1

if __name__ == '__main__':
    raise SystemExit(main())
