#!/usr/bin/env python3
"""Preserve the frozen package and seal one source-checked successor."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import zipfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'PAQUETE_ARTICULO_I_LOCALIDAD_CAMPOS_20260919'
ROOT = HERE.parent / 'PAQUETE_ARTICULO_I_INTEGRACION_ESTADO_CAMPOS_20260919'
KEY = 'generated_enrichment_mixed_successor'
DELTA = HERE / 'mixed_enriched_delta_build/VERIFICATION.json'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(path):
    return sha(Path(path).read_bytes())


def jb(data):
    return (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode()


def add(manifest, path, data, role, source='GENERATED_ENRICHMENT_DELTA'):
    if (ROOT / path).exists() or any(r['path'] == path for r in manifest['files']):
        raise RuntimeError('Will not replace preserved file: ' + path)
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    manifest['files'].append(dict(path=path, sha256=sha(data), bytes=len(data),
                                 role=role, source=source))


def validate_base():
    raw = (BASE / 'MANIFIESTO.json').read_bytes()
    manifest = json.loads(raw)
    for row in manifest['files']:
        if digest(BASE / row['path']) != row['sha256']:
            raise RuntimeError('Predecessor file changed: ' + row['path'])
    receipt = json.loads((BASE / 'recibos/localidad/LEAN_CONJUNTO.json').read_text())
    if receipt['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE' or len(receipt['modules']) != 238:
        raise RuntimeError('Expected checked 238-module predecessor')
    for row in receipt['modules']:
        if digest(BASE / row['source']) != row['source_sha256']:
            raise RuntimeError('Inherited Lean source changed: ' + row['module'])
        if digest(BASE / 'resultados/lean_unificado/build' / (row['module'] + '.olean')) != row['object_sha256']:
            raise RuntimeError('Inherited Lean object changed: ' + row['module'])
    return raw, manifest, receipt


def prepare():
    if ROOT.exists():
        raise RuntimeError('Successor exists; refusing to overwrite')
    old_raw, manifest, baseline = validate_base()
    delta_raw = DELTA.read_bytes()
    delta = json.loads(delta_raw)
    if delta['status'] != 'PASS_MIXED_FIELDS_AND_REGIONAL_ENRICHMENT_DELTA' or len(delta['modules']) != 13:
        raise RuntimeError('Expected thirteen checked delta modules')
    if delta['base_receipt_sha256'] != digest(BASE / 'recibos/localidad/LEAN_CONJUNTO.json'):
        raise RuntimeError('Different base receipt')
    for row in delta['modules']:
        if row['exit_code'] or digest(row['source']) != row['source_sha256']:
            raise RuntimeError('Delta source no longer checked: ' + row['module'])
        if digest(DELTA.parent / (row['module'] + '.olean')) != row['object_sha256']:
            raise RuntimeError('Delta object changed: ' + row['module'])
    shutil.copytree(BASE, ROOT)
    add(manifest, 'versiones_previas/MANIFIESTO_LOCALIDAD_SELLADO.json', old_raw,
        'EXACT_PREDECESSOR_MANIFEST')
    add(manifest, 'versiones_previas/README_LOCALIDAD_SELLADO.md', (ROOT / 'README.md').read_bytes(),
        'EXACT_PREDECESSOR_ENTRY')
    readme = (HERE / 'README_INTEGRACION_ESTADO_ENTREGA.md').read_bytes()
    (ROOT / 'README.md').write_bytes(readme)
    for row in manifest['files']:
        if row['path'] == 'README.md':
            row.update(sha256=sha(readme), bytes=len(readme), role='CURRENT_INTEGRATION_ENTRY')
    owners, probes = [], []
    for row in delta['modules']:
        raw = Path(row['source']).read_bytes()
        path = 'deltas/integracion/' + row['module'] + '.lean'
        add(manifest, path, raw, 'CHECKED_LEAN_SOURCE', row['source'])
        owners.append(dict(module=row['module'], path=path, sha256=sha(raw), origin=row['source']))
        probes.extend(re.findall(r'(?m)^#print axioms ([A-Za-z0-9_.]+)\s*$', raw.decode()))
    add(manifest, 'recibos/integracion/BLOQUE_FOCAL.json', delta_raw, 'FOCAL_COMPILATION_RECEIPT')
    for name in ['RegionalRecordDependencyAudit.lean', 'verify_mixed_and_enriched_delta.py',
                 'verify_joint_regional_frontier.py', 'verify_generated_transition_records.py',
                 'preparar_integracion_estado.py', 'README_REGISTROS.md',
                 'RECIBO_REGISTROS_GENEALOGICO.json', 'RECIBO_REGISTROS_CAUSAL.json', 'REGISTROS_GATES.json']:
        add(manifest, 'procedencia/integracion/' + name, (HERE / name).read_bytes(), 'DELTA_PROVENANCE')
    add(manifest, 'reproducir_integracion.py', (HERE / 'reproducir_integracion_portable.py').read_bytes(),
        'PORTABLE_CHAIN_RUNNER')
    scope = ('Generated all-depth regional transition records and their unique ternary lifts; '
             'joint rational-cylinder selection, exact prefix/carry/signature/Witt compatibility; '
             'APP winding; all-mode mixed-field commutators and mixed locality on the same selected lattice.')
    causal = json.loads((BASE / 'recibos/localidad/RECIBO_CAUSAL.json').read_text())
    causal.update(artifact=str(ROOT / 'README.md'), artifact_sha256=sha(readme),
        result_id='GENERATED_REGIONAL_ENRICHMENT_MIXED_LOCALITY_20260919', scope=scope,
        mathematical_result=scope, predecessor_receipt=dict(
            path='recibos/localidad/RECIBO_CAUSAL.json',
            sha256=digest(BASE / 'recibos/localidad/RECIBO_CAUSAL.json')))
    causal['genealogy']['source_locators'] += [str(ROOT / r['path']) for r in owners]
    causal['genealogical_result_record']['9_material_owners'] += owners
    causal['genealogical_result_record']['7_hmt_output_before_recognition'] += (
        ' The all-depth regional publications now construct the transition records directly; '
        'rationally admissible joint children give the same carry, signature and Witt charge; '
        'mixed locality is proved for fields on the previously selected carrier.')
    causal['formalization_scope'] = dict(whole_pdf=False, full_U_nine_step_identification=False,
        full_FLM_Moonshine=False, local_claim=scope, inherited_finite_selector_axiom='Lean.ofReduceBool')
    add(manifest, 'recibos/integracion/RECIBO_CAUSAL.json', jb(causal), 'CAUSAL_METADATA_NOT_A_PROOF')
    command = [sys.executable, '-I', '-S',
        '/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py',
        '--audit', str(ROOT / 'README.md'), '--receipt', str(ROOT / 'recibos/integracion/RECIBO_CAUSAL.json')]
    p = subprocess.run(command, text=True, capture_output=True)
    if p.returncode or 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY' not in p.stdout:
        raise RuntimeError(p.stdout + p.stderr)
    add(manifest, 'recibos/integracion/CONTROL_CAUSAL.txt', (p.stdout + p.stderr).encode(), 'CAUSAL_METADATA_CHECK')
    add(manifest, 'recibos/integracion/PRESERVACION.json', jb(dict(
        status='PREDECESSOR_BYTES_PRESERVED', predecessor_manifest_sha256=sha(old_raw),
        preserved_files=len(json.loads(old_raw)['files']),
        moved_unchanged={'README.md': 'versiones_previas/README_LOCALIDAD_SELLADO.md'},
        preservation_is_not_mathematical_completeness=True)), 'FILE_CONTINUITY')
    manifest[KEY] = dict(status='PREPARED_NOT_COMPILED', modules=[r['module'] for r in owners],
        axiom_queries=probes, expected_total_modules=251, predecessor_manifest_sha256=sha(old_raw),
        scope=scope, complete_flm_formalization_claimed=False, full_enriched_U_identification_claimed=False)
    (ROOT / 'MANIFIESTO.json').write_bytes(jb(manifest))
    # Authenticate and adapt only the focal compilation cache to the portable
    # verifier's exact fingerprint format; its final probe will run afresh.
    spec = importlib.util.spec_from_file_location('portable_v', ROOT / 'verificar_lean.py')
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    report_dir = ROOT / 'resultados/lean_unificado'
    cache_path = report_dir / 'CACHE.json'
    cache = json.loads(cache_path.read_text())
    done = {r['module']: r for r in baseline['modules']}
    for row, owner in zip(delta['modules'], owners):
        raw = (ROOT / owner['path']).read_bytes()
        imports, queries = verifier.inspect_source(raw, owner['path'])
        dependencies = {name: (dict(fingerprint=done[name]['fingerprint'],
            object_sha256=done[name]['object_sha256']) if name in done
            else baseline['external_objects'][name]) for name in imports}
        fingerprint = verifier.digest_json(dict(source_sha256=row['source_sha256'],
            dependencies=dependencies, compiler=baseline['compiler']))
        record = dict(row, source=owner['path'], dependencies=dependencies, fingerprint=fingerprint)
        if len(record['axioms']) != queries:
            raise RuntimeError('Incomplete focal axiom queries')
        for suffix in ['.olean', '.log']:
            shutil.copyfile(DELTA.parent / (row['module'] + suffix),
                            report_dir / 'build' / (row['module'] + suffix))
        (report_dir / 'build' / (row['module'] + '.lean')).write_bytes(raw)
        cache['modules'][row['module']] = record
        done[row['module']] = record
    cache_path.write_bytes(jb(cache))
    print(json.dumps(dict(status='INTEGRATION_PREPARED', root=str(ROOT), added=len(owners),
        expected_modules=251, original_files=len(json.loads(old_raw)['files']))))


def seal():
    old_raw, old, _ = validate_base()
    raw = (ROOT / 'MANIFIESTO.json').read_bytes()
    manifest = json.loads(raw)
    if manifest[KEY]['status'] != 'PREPARED_NOT_COMPILED':
        raise RuntimeError('Not prepared or already sealed')
    rp = ROOT / 'resultados/lean_unificado/VERIFICATION.json'
    run = json.loads(rp.read_text())
    if (run['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE'
            or run['manifest_sha256'] != sha(raw) or run['local_module_count'] != 251):
        raise RuntimeError('No matching 251-module PASS')
    dp = ROOT / 'resultados/datos_incidencia/VERIFICATION.json'
    if json.loads(dp.read_text())['status'] != 'PASS_PACKAGE_INCIDENCE_DATA':
        raise RuntimeError('Incidence data check failed')
    for row in manifest['files']:
        if digest(ROOT / row['path']) != row['sha256']:
            raise RuntimeError('Manifested bytes changed: ' + row['path'])
    for row in old['files']:
        path = 'versiones_previas/README_LOCALIDAD_SELLADO.md' if row['path'] == 'README.md' else row['path']
        if digest(ROOT / path) != row['sha256']:
            raise RuntimeError('Predecessor bytes lost: ' + row['path'])
    if sha(old_raw) != manifest[KEY]['predecessor_manifest_sha256']:
        raise RuntimeError('Predecessor manifest changed')
    add(manifest, 'recibos/integracion/MANIFIESTO_COMPILADO.json', raw, 'FROZEN_COMPILED_MANIFEST')
    add(manifest, 'recibos/integracion/LEAN_CONJUNTO.json', rp.read_bytes(), 'FROZEN_COMPILATION_RECEIPT')
    add(manifest, 'recibos/integracion/DATOS_INCIDENCIA.json', dp.read_bytes(), 'FROZEN_DATA_RECEIPT')
    manifest[KEY].update(status='SEALED_VERIFIED_GENERATED_ENRICHMENT_AND_MIXED_LOCALITY',
        modules_in_closure=251, previous_bytes_preserved=True,
        fresh_probe_declarations=len(run['axiom_probe']['declarations']))
    final = jb(manifest)
    (ROOT / 'MANIFIESTO.json').write_bytes(final)
    archive = ROOT.with_suffix('.zip')
    if archive.exists():
        raise RuntimeError('Will not overwrite existing archive')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for name in sorted({r['path'] for r in manifest['files']} | {'MANIFIESTO.json'}):
            z.write(ROOT / name, Path(ROOT.name) / name)
        if z.testzip():
            raise RuntimeError('ZIP CRC failure')
        for row in manifest['files']:
            if sha(z.read(str(Path(ROOT.name) / row['path']))) != row['sha256']:
                raise RuntimeError('ZIP bytes differ: ' + row['path'])
    print(json.dumps(dict(status='PASS_INTEGRATION_SUCCESSOR_SEALED', modules=251,
        new_modules=13, fresh_probe_queries=len(run['axiom_probe']['declarations']),
        preserved_files=len(old['files']), zip=str(archive), zip_sha256=digest(archive),
        manifest_sha256=sha(final)), ensure_ascii=False))


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    elif sys.argv[1:] == ['--seal']:
        seal()
    else:
        raise SystemExit('Use --prepare or --seal')
