#!/usr/bin/env python3
"""Authenticate the unchanged base and compile the connected survival delta."""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'PAQUETE_ARTICULO_I_INTEGRACION_ESTADO_CAMPOS_20260919'
PEER = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_REFINAMIENTO_CONJUNTO_20260919')
RECEIVED = {
    'RegionalResidualDynamics': '0f422cdf013fec41b70662bc43e14b3239d8824562169838bfd7e7fb3257beaf',
    'RegionalResidualCylinderBridge': '6cad33c4f2538bd6f02aca5fd148084ef842562e55b3cffcb61c5411b56d1ff7',
}
ORDER = ['SurvivalCylinderSelection', 'CofinalCylinderSurvival',
         'SurvivingTransitionHistory', 'RegionalResidualDynamics',
         'RegionalResidualCylinderBridge', 'ResidualSurvivalSelection']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    baseline = BASE / 'recibos/integracion/LEAN_CONJUNTO.json'
    data = json.loads(baseline.read_text())
    if data['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE' or data['local_module_count'] != 251:
        raise RuntimeError('Unexpected integration baseline')
    for row in data['modules']:
        if sha(BASE / row['source']) != row['source_sha256']:
            raise RuntimeError('Changed source dependency: ' + row['module'])
        obj = BASE / 'resultados/lean_unificado/build' / (row['module'] + '.olean')
        if sha(obj) != row['object_sha256']:
            raise RuntimeError('Changed compiled dependency: ' + row['module'])
    compiler = data['compiler']
    if sha(compiler['executable']) != compiler['binary_sha256']:
        raise RuntimeError('Changed Lean executable')
    spec = importlib.util.spec_from_file_location('checked_lean', BASE / 'verificar_lean.py')
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    build = HERE / 'survival_chain_build'
    received = build / 'received'
    received.mkdir(parents=True, exist_ok=True)
    for name, expected in RECEIVED.items():
        source = PEER / (name + '.lean')
        if sha(source) != expected:
            raise RuntimeError('Peer source changed before import: ' + name)
        target = received / source.name
        if target.exists() and sha(target) != expected:
            raise RuntimeError('Preserved peer copy differs: ' + name)
        if not target.exists():
            shutil.copy2(source, target)
    path = str(build) + os.pathsep + data['lean_path']
    receipt = build / 'VERIFICATION.json'
    report = {
        'status': 'RUNNING', 'base_module_count': 251,
        'base_receipt_sha256': sha(baseline), 'compiler': compiler,
        'verifier_sha256': sha(__file__), 'modules': [],
        'scope': 'Selection by survival, cofinal observations, surviving transition registers, and the concrete residual realization after R36.',
        'not_claimed': 'Identification of the historical pre-R36 nine complete enriched updates; full-article or FLM/Moonshine closure.',
    }
    receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    for name in ORDER:
        source = (received if name in RECEIVED else HERE) / (name + '.lean')
        imports, query_count = verifier.inspect_source(source.read_bytes(), str(source))
        before = sha(source)
        obj = build / (name + '.olean')
        obj.unlink(missing_ok=True)
        cmd = [compiler['executable'], '-DwarningAsError=true',
               '--root=' + str(source.parent), '-o', str(obj), str(source)]
        run = subprocess.run(cmd, cwd=data['mathlib'], env=dict(os.environ, LEAN_PATH=path),
                             text=True, capture_output=True, timeout=180)
        output = run.stdout + run.stderr
        (build / (name + '.log')).write_text(output)
        try:
            declarations = verifier.axiom_reports(output)
        except RuntimeError:
            declarations = {}
        axioms = {a for aa in declarations.values() for a in aa}
        passed = (run.returncode == 0 and len(declarations) == query_count
                  and sha(source) == before
                  and not (axioms - {'propext', 'Classical.choice', 'Quot.sound'}))
        report['modules'].append({
            'module': name, 'source': str(source), 'source_sha256': before,
            'object_sha256': sha(obj) if passed else None, 'imports': imports,
            'declarations': declarations, 'exit_code': run.returncode,
            'status': 'PASS' if passed else 'FAIL', 'command': cmd,
        })
        print(name + ': ' + ('PASS' if passed else 'FAIL'), flush=True)
        if not passed:
            report['status'] = 'FAIL'
            receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
            print(output)
            return 1
    report['status'] = 'PASS_CONNECTED_SURVIVAL_CHAIN'
    report['axiom_query_count'] = sum(len(r['declarations']) for r in report['modules'])
    receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(report['status'], flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
