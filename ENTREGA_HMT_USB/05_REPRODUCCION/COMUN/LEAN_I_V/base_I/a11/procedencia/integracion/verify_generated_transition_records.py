#!/usr/bin/env python3
"""Verify the direct all-depth publication-to-transition-record composition."""
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
    if data['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE':
        raise RuntimeError('Baseline is not verified')
    for row in data['modules']:
        source = BASE / row['source']
        obj = BASE / 'resultados/lean_unificado/build' / (row['module'] + '.olean')
        if sha(source) != row['source_sha256'] or sha(obj) != row['object_sha256']:
            raise RuntimeError('Changed authenticated dependency: ' + row['module'])
    compiler = data['compiler']
    if sha(compiler['executable']) != compiler['binary_sha256']:
        raise RuntimeError('Changed compiler')
    paths = []
    dependencies = []
    for module, dirname, status in [
            ('JointRegionalFrontier', 'joint_regional_frontier_build', 'PASS_JOINT_REGIONAL_FRONTIER'),
            ('RegionalTransitionRecords', 'regional_records_build', 'PASS_REGIONAL_TRANSITION_RECORDS')]:
        receipt = HERE / dirname / 'VERIFICATION.json'
        r = json.loads(receipt.read_text())
        if (r['status'] != status or r['source_sha256'] != sha(HERE / (module + '.lean')) or
                r['object_sha256'] != sha(HERE / dirname / (module + '.olean')) or
                r['baseline_receipt_sha256'] != sha(baseline) or r['compiler'] != compiler):
            raise RuntimeError('Unauthenticated dependency: ' + module)
        paths.append(str(HERE / dirname))
        dependencies.append(dict(module=module, receipt_sha256=sha(receipt),
                                 source_sha256=r['source_sha256'], object_sha256=r['object_sha256']))
    spec = importlib.util.spec_from_file_location('verified_reader', BASE / 'verificar_lean.py')
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    source = HERE / 'GeneratedTransitionRecords.lean'
    imports, queries = verifier.inspect_source(source.read_bytes(), str(source))
    before = sha(source)
    build = HERE / 'generated_transition_records_build'
    build.mkdir(exist_ok=True)
    receipt = build / 'VERIFICATION.json'
    receipt.write_text(json.dumps({'status': 'RUNNING', 'source_sha256': before}))
    obj = build / 'GeneratedTransitionRecords.olean'
    command = [compiler['executable'], '-DwarningAsError=true',
               '--root=' + str(HERE), '-o', str(obj), str(source)]
    lean_path = ':'.join(paths + [data['lean_path']])
    result = subprocess.run(command, cwd=data['mathlib'],
                            env=dict(os.environ, LEAN_PATH=lean_path),
                            text=True, capture_output=True, timeout=180)
    output = result.stdout + result.stderr
    (build / 'GeneratedTransitionRecords.log').write_text(output)
    try:
        declarations = verifier.axiom_reports(output)
    except RuntimeError:
        declarations = {}
    used = {a for axioms in declarations.values() for a in axioms}
    allowed = {'propext', 'Classical.choice', 'Quot.sound'}
    passed = (result.returncode == 0 and len(declarations) == queries and
              sha(source) == before and not (used - allowed))
    report = dict(status='PASS_GENERATED_TRANSITION_RECORDS' if passed else 'FAIL',
                  source_sha256=before, object_sha256=sha(obj) if passed else None,
                  compiler=compiler, imports=imports, declarations=declarations,
                  dependencies=dependencies, command=command, exit_code=result.returncode,
                  output=output, inherited_modules_authenticated=len(data['modules']),
                  baseline_receipt_sha256=sha(baseline), lean_path=lean_path,
                  scope='Direct arbitrary-depth regional publication to consecutive transition records; finite agreement and unique first lift pair.',
                  not_claimed='Identity with nine complete enriched Sel/Tra/Upd updates.')
    receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(output)
    print(report['status'])
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
