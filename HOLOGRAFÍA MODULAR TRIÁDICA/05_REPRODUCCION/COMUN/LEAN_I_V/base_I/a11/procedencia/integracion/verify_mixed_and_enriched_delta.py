#!/usr/bin/env python3
"""Compile the new source delta, authenticating the frozen 238-module base."""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'PAQUETE_ARTICULO_I_LOCALIDAD_CAMPOS_20260919'
MIX = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_CAMPOS_MIXTOS_20260919')
WIND = MIX.parent / 'CIERRE_ENROLLAMIENTO_APP_20260919'
CYL = MIX.parent / 'CIERRE_REFINAMIENTO_CONJUNTO_20260919'
SOURCES = [HERE / 'RegionalTransitionRecords.lean',
           HERE / 'LatticePositiveMixedFields.lean',
           MIX / 'LatticeNegativeExponential.lean',
           MIX / 'LatticeNegativeMixedFields.lean',
           MIX / 'LatticeAllMixedFields.lean',
           HERE / 'LatticeMixedLocalityCriterion.lean',
           HERE / 'LatticeMixedLocality.lean',
           HERE / 'SelectedMixedFieldLocality.lean',
           WIND / 'APPRouteWinding.lean',
           HERE / 'JointRegionalFrontier.lean',
           CYL / 'RegionalCylinderTransition.lean',
           HERE / 'JointCylinderSignature.lean',
           HERE / 'GeneratedTransitionRecords.lean']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    baseline = BASE / 'recibos/localidad/LEAN_CONJUNTO.json'
    base = json.loads(baseline.read_text())
    if base['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE':
        raise RuntimeError('Base receipt is not a passing compilation')
    compiler = base['compiler']
    if sha(compiler['executable']) != compiler['binary_sha256']:
        raise RuntimeError('Compiler changed')
    for row in base['modules']:
        if sha(BASE / row['source']) != row['source_sha256']:
            raise RuntimeError('Inherited source changed: ' + row['module'])
        if sha(BASE / 'resultados/lean_unificado/build' / (row['module'] + '.olean')) != row['object_sha256']:
            raise RuntimeError('Inherited object changed: ' + row['module'])
    for module, obj in base['external_objects'].items():
        if sha(obj['path']) != obj['object_sha256']:
            raise RuntimeError('External object changed: ' + module)
    spec = importlib.util.spec_from_file_location('verified_reader', BASE / 'verificar_lean.py')
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    build = HERE / 'mixed_enriched_delta_build'
    build.mkdir(exist_ok=True)
    receipt_path = build / 'VERIFICATION.json'
    previous = json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
    previous_rows = {r['module']: r for r in previous.get('modules', [])}
    env = dict(os.environ, LEAN_PATH=str(build) + os.pathsep + base['lean_path'])
    receipt = dict(status='RUNNING', base_receipt_sha256=sha(baseline),
        compiler=compiler, mathlib=base['mathlib'], lean_path=env['LEAN_PATH'],
        inherited_modules_authenticated=len(base['modules']),
        modules=[], full_enriched_U_identification_claimed=False,
        full_FLM_or_Moonshine_claimed=False)
    def save():
        receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    save()
    known = {r['module']: r['object_sha256'] for r in base['modules']}
    try:
        for source in SOURCES:
            module = source.stem
            imports, queries = verifier.inspect_source(source.read_bytes(), str(source))
            source_hash = sha(source)
            deps = {}
            for name in imports:
                if name in known:
                    deps[name] = known[name]
                elif name in base['external_objects']:
                    deps[name] = base['external_objects'][name]['object_sha256']
                else:
                    raise RuntimeError('Unauthenticated import: ' + name)
            fingerprint = hashlib.sha256(json.dumps(dict(source=source_hash,
                dependencies=deps, compiler=compiler['binary_sha256']), sort_keys=True).encode()).hexdigest()
            obj = build / (module + '.olean')
            command = [compiler['executable'], '-DwarningAsError=true',
                       '--root=' + str(source.parent), '-o', str(obj), str(source)]
            old = previous_rows.get(module, {})
            cache_hit = (old.get('fingerprint') == fingerprint and old.get('exit_code') == 0
                and obj.exists() and sha(obj) == old.get('object_sha256'))
            print(module + (': authenticated cache' if cache_hit else ': compiling'), flush=True)
            if cache_hit:
                code, output = 0, old['output']
            else:
                process = subprocess.run(command, cwd=base['mathlib'], env=env,
                    text=True, capture_output=True, timeout=240)
                code, output = process.returncode, process.stdout + process.stderr
            (build / (module + '.log')).write_text(output)
            reports = verifier.axiom_reports(output)
            row = dict(module=module, source=str(source), source_sha256=source_hash,
                dependencies=deps, fingerprint=fingerprint, command=command,
                exit_code=code, output=output, axioms=reports, cache_hit=cache_hit)
            receipt['modules'].append(row)
            if code or len(reports) != queries or sha(source) != source_hash:
                raise RuntimeError('Compilation/query mismatch for ' + module + '\n' + output)
            row['object_sha256'] = sha(obj)
            known[module] = row['object_sha256']
            save()
        audit = HERE / 'RegionalRecordDependencyAudit.lean'
        code = subprocess.run([compiler['executable'], str(audit)], cwd=base['mathlib'],
            env=env, text=True, capture_output=True, timeout=240)
        output = code.stdout + code.stderr
        receipt['constructor_dependency_audit'] = dict(source=str(audit),
            source_sha256=sha(audit), exit_code=code.returncode, output=output)
        if code.returncode or output.count('PASS') != 4:
            raise RuntimeError('Regional constructor audit failed\n' + output)
        for row in receipt['modules']:
            if sha(row['source']) != row['source_sha256'] or sha(build / (row['module'] + '.olean')) != row['object_sha256']:
                raise RuntimeError('Changed delta source/object: ' + row['module'])
        receipt['status'] = 'PASS_MIXED_FIELDS_AND_REGIONAL_ENRICHMENT_DELTA'
        receipt['queried_declarations'] = sum(len(r['axioms']) for r in receipt['modules'])
        save()
        print(receipt['status'], receipt['queried_declarations'], flush=True)
        return 0
    except Exception as error:
        receipt.update(status='FAIL', error=str(error))
        save()
        print(str(error), flush=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
