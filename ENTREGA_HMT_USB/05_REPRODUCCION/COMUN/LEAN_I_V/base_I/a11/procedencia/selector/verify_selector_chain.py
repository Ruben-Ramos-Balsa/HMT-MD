#!/usr/bin/env python3
"""Compile the four connected selector modules over authenticated package257."""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'PAQUETE_ARTICULO_I_SUPERVIVENCIA_REGISTROS_20260919'
PEER = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_SELECTOR_ITERADO_20260919')
SOURCES = [HERE / 'RationalCellIntegerShift.lean', HERE / 'FiniteCylinderSelector.lean',
           PEER / 'IteratedCylinderSelector.lean', HERE / 'SelectedCylinderSignature.lean']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    receipt = BASE / 'recibos/supervivencia/LEAN_CONJUNTO.json'
    base = json.loads(receipt.read_text())
    if base['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE' or base['local_module_count'] != 257:
        raise RuntimeError('Wrong baseline')
    for row in base['modules']:
        if sha(BASE / row['source']) != row['source_sha256']:
            raise RuntimeError('Changed source: ' + row['module'])
        obj = BASE / 'resultados/lean_unificado/build' / (row['module'] + '.olean')
        if sha(obj) != row['object_sha256']:
            raise RuntimeError('Changed object: ' + row['module'])
    for name, row in base['external_objects'].items():
        if sha(row['path']) != row['object_sha256']:
            raise RuntimeError('Changed external object: ' + name)
    if sha(base['compiler']['executable']) != base['compiler']['binary_sha256']:
        raise RuntimeError('Changed compiler')
    spec = importlib.util.spec_from_file_location('checker', BASE / 'verificar_lean.py')
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    build = HERE / 'selector_chain_build'
    build.mkdir(exist_ok=True)
    env = dict(os.environ, LEAN_PATH=str(build) + os.pathsep + base['lean_path'])
    report = dict(status='RUNNING', base_receipt_sha256=sha(receipt), base_module_count=257,
                  compiler=base['compiler'], verifier_sha256=sha(__file__), modules=[],
                  scope='Actual parent recursion to records, lifts and the same cylinder/signature fields.',
                  full_micro_update_identification_claimed=False, full_flm_claimed=False)
    for source in SOURCES:
        name = source.stem
        before = sha(source)
        imports, count = checker.inspect_source(source.read_bytes(), str(source))
        obj = build / (name + '.olean')
        cmd = [base['compiler']['executable'], '-DwarningAsError=true',
               '--root=' + str(source.parent), '-o', str(obj), str(source)]
        run = subprocess.run(cmd, cwd=base['mathlib'], env=env, capture_output=True,
                             text=True, timeout=180)
        output = run.stdout + run.stderr
        (build / (name + '.log')).write_text(output)
        try:
            declarations = checker.axiom_reports(output)
        except RuntimeError:
            declarations = {}
        axioms = {a for values in declarations.values() for a in values}
        passed = run.returncode == 0 and len(declarations) == count and sha(source) == before
        passed = passed and not (axioms - {'propext', 'Classical.choice', 'Quot.sound'})
        if name == 'FiniteCylinderSelector':
            passed = passed and {'some 3', 'none'}.issubset(set(output.splitlines()))
        report['modules'].append(dict(module=name, source=str(source), source_sha256=before,
            object_sha256=sha(obj) if passed else None, imports=imports,
            declarations=declarations, command=cmd, exit_code=run.returncode,
            status='PASS' if passed else 'FAIL'))
        print(name + ': ' + ('PASS' if passed else 'FAIL'), flush=True)
        if not passed:
            print(output, flush=True)
            report['status'] = 'FAIL'
            (build / 'VERIFICATION.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
            return 1
    report['status'] = 'PASS_ITERATED_SELECTOR_SIGNATURE_CHAIN'
    report['axiom_query_count'] = sum(len(r['declarations']) for r in report['modules'])
    (build / 'VERIFICATION.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(report['status'], flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
