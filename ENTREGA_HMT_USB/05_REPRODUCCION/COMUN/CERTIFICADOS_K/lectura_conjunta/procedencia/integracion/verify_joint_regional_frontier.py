#!/usr/bin/env python3
"""Compile the all-depth regional/signature bridge against authenticated sources."""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'PAQUETE_ARTICULO_I_PRODUCTOS_RETICULARES_20260919'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    baseline = BASE / 'recibos/productos/LEAN_CONJUNTO.json'
    data = json.loads(baseline.read_text())
    if not data['status'].startswith('PASS'):
        raise RuntimeError('Baseline is not verified')
    for row in data['modules']:
        source = BASE / row['source']
        obj = BASE / 'resultados/lean_unificado/build' / (row['module'] + '.olean')
        if sha(source) != row['source_sha256'] or sha(obj) != row['object_sha256']:
            raise RuntimeError('Changed authenticated dependency: ' + row['module'])
    compiler = data['compiler']
    if sha(compiler['executable']) != compiler['binary_sha256']:
        raise RuntimeError('Changed compiler')
    spec = importlib.util.spec_from_file_location('verified_reader', BASE / 'verificar_lean.py')
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    source = HERE / 'JointRegionalFrontier.lean'
    imports, queries = verifier.inspect_source(source.read_bytes(), str(source))
    before = sha(source)
    build = HERE / 'joint_regional_frontier_build'
    build.mkdir(exist_ok=True)
    receipt = build / 'VERIFICATION.json'
    receipt.write_text(json.dumps({'status': 'RUNNING', 'source_sha256': before}))
    obj = build / 'JointRegionalFrontier.olean'
    command = [compiler['executable'], '-DwarningAsError=true',
               '--root=' + str(HERE), '-o', str(obj), str(source)]
    result = subprocess.run(command, cwd=data['mathlib'],
                            env=dict(os.environ, LEAN_PATH=data['lean_path']),
                            text=True, capture_output=True, timeout=180)
    output = result.stdout + result.stderr
    (build / 'JointRegionalFrontier.log').write_text(output)
    try:
        declarations = verifier.axiom_reports(output)
    except RuntimeError:
        declarations = {}
    passed = result.returncode == 0 and len(declarations) == queries and sha(source) == before
    report = dict(status='PASS_JOINT_REGIONAL_FRONTIER' if passed else 'FAIL',
                  source_sha256=before, object_sha256=sha(obj) if passed else None,
                  compiler=compiler, imports=imports, declarations=declarations,
                  command=command, exit_code=result.returncode, output=output,
                  inherited_modules_authenticated=len(data['modules']),
                  baseline_receipt_sha256=sha(baseline), lean_path=data['lean_path'],
                  scope='All-depth regional block/signature generation, exact recovery from every longer prefix, and agreement with the 100 preserved blocks.',
                  not_claimed='Identification with nine full enriched Sel/Tra/Upd updates.')
    receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(output)
    print(report['status'])
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
