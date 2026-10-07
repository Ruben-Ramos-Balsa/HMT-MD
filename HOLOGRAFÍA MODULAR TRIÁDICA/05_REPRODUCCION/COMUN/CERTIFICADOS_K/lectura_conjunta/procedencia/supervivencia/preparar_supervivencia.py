#!/usr/bin/env python3
"""Preserve the sealed 251-module package and bind its six-module successor."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'PAQUETE_ARTICULO_I_INTEGRACION_ESTADO_CAMPOS_20260919'
ROOT = HERE.parent / 'PAQUETE_ARTICULO_I_SUPERVIVENCIA_REGISTROS_20260919'
KEY = 'survival_register_successor'
DELTA = HERE / 'survival_chain_build/VERIFICATION.json'
BASE_RECEIPT = 'recibos/integracion/LEAN_CONJUNTO.json'
MOVED_README = 'versiones_previas/README_INTEGRACION_SELLADO.md'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(path):
    return sha(Path(path).read_bytes())


def jb(data):
    return (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode()


def add(manifest, path, data, role, source='CONNECTED_SURVIVAL_DELTA'):
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
    receipt = json.loads((BASE / BASE_RECEIPT).read_text())
    if receipt['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE' or len(receipt['modules']) != 251:
        raise RuntimeError('Expected checked 251-module predecessor')
    for row in receipt['modules']:
        if digest(BASE / row['source']) != row['source_sha256']:
            raise RuntimeError('Inherited Lean source changed: ' + row['module'])
        if digest(BASE / 'resultados/lean_unificado/build' / (row['module'] + '.olean')) != row['object_sha256']:
            raise RuntimeError('Inherited Lean object changed: ' + row['module'])
    return raw, manifest, receipt


def metadata(manifest, owners):
    """Rebind existing, explicit-scope metadata to this portable entry."""
    readme = ROOT / 'README.md'
    genealogy = json.loads((HERE / 'RECIBO_SUPERVIVENCIA_GENEALOGICO.json').read_text())
    genealogy['artifact'].update(path=str(readme), sha256=digest(readme),
        lines='1-' + str(len(readme.read_text().splitlines())), anchors=[
            {'stage': 'APP', 'text': 'APP →'}, {'stage': 'TRIT', 'text': 'TRIT →'},
            {'stage': 'TPK', 'text': 'TPK →'},
            {'stage': 'ESTADO_ENRIQUECIDO', 'text': 'estado enriquecido →'},
            {'stage': 'ESTRUCTURA_DISCRETA_CONTINUO', 'text': 'estructura discreta conjunta'},
            {'stage': 'HMT_OUTPUT', 'text': '## Qué se incorpora'},
            {'stage': 'CONVENTIONAL', 'text': '## Una entrada de reproducción'}])
    genealogy['effective_result_record']['9_material_owners'] = owners
    genealogy['local_proof_owners'] = owners
    genealogy['previous_scope_preserved'] = 'Las 820 entradas de la base permanecen conservadas; no se modifica ningún PDF.'
    gp = 'recibos/supervivencia/RECIBO_GENEALOGICO.json'
    add(manifest, gp, jb(genealogy), 'GENEALOGICAL_METADATA_NOT_A_PROOF')
    causal = json.loads((HERE / 'RECIBO_SUPERVIVENCIA_CAUSAL.json').read_text())
    causal.update(artifact=str(readme), artifact_sha256=digest(readme))
    causal['genealogy']['source_locators'] += [str(ROOT / r['path']) for r in owners]
    causal['genealogical_result_record']['9_material_owners'] = owners
    cp = 'recibos/supervivencia/RECIBO_CAUSAL.json'
    add(manifest, cp, jb(causal), 'CAUSAL_METADATA_NOT_A_PROOF')
    commands = [
        ('GENEALOGIA', [sys.executable, '-I', '-S',
          str(HERE.parents[1] / 'tools/verificar_genealogia_unica_hmt.py'),
          '--receipt', str(ROOT / gp)], 'PASS_GENEALOGIA_UNICA_APP_TRIT_TPK'),
        ('CAUSALIDAD', [sys.executable, '-I', '-S',
          '/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py',
          '--audit', str(readme), '--receipt', str(ROOT / cp)],
          'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY')]
    for name, command, expected in commands:
        p = subprocess.run(command, text=True, capture_output=True)
        if p.returncode or expected not in p.stdout:
            raise RuntimeError(p.stdout + p.stderr)
        add(manifest, 'recibos/supervivencia/CONTROL_' + name + '.json', jb(dict(
            command=command, exit_code=p.returncode, output=p.stdout+p.stderr,
            artifact_sha256=digest(readme), metadata_not_a_mathematical_proof=True)),
            'METADATA_CHECK')


def prepare():
    if ROOT.exists():
        raise RuntimeError('Successor exists; refusing to overwrite')
    old_raw, manifest, baseline = validate_base()
    delta_raw = DELTA.read_bytes()
    delta = json.loads(delta_raw)
    if delta['status'] != 'PASS_CONNECTED_SURVIVAL_CHAIN' or len(delta['modules']) != 6:
        raise RuntimeError('Expected six checked delta modules')
    if delta['base_receipt_sha256'] != digest(BASE / BASE_RECEIPT):
        raise RuntimeError('Different base receipt')
    for row in delta['modules']:
        if row['exit_code'] or digest(row['source']) != row['source_sha256']:
            raise RuntimeError('Delta source no longer checked: ' + row['module'])
        if digest(DELTA.parent / (row['module'] + '.olean')) != row['object_sha256']:
            raise RuntimeError('Delta object changed: ' + row['module'])
    shutil.copytree(BASE, ROOT)
    add(manifest, 'versiones_previas/MANIFIESTO_INTEGRACION_SELLADO.json', old_raw,
        'EXACT_PREDECESSOR_MANIFEST')
    add(manifest, MOVED_README, (ROOT / 'README.md').read_bytes(), 'EXACT_PREDECESSOR_ENTRY')
    readme = (HERE / 'README_SUPERVIVENCIA_ENTREGA.md').read_bytes()
    (ROOT / 'README.md').write_bytes(readme)
    for row in manifest['files']:
        if row['path'] == 'README.md':
            row.update(sha256=sha(readme), bytes=len(readme), role='CURRENT_SURVIVAL_ENTRY')
    owners, probes = [], []
    for row in delta['modules']:
        raw = Path(row['source']).read_bytes()
        path = 'deltas/supervivencia/' + row['module'] + '.lean'
        add(manifest, path, raw, 'CHECKED_LEAN_SOURCE', row['source'])
        owners.append(dict(module=row['module'], path=path, sha256=sha(raw),
                           origin=row['source'], lines='1-' + str(len(raw.splitlines()))))
        probes.extend(re.findall(r'(?m)^#print axioms ([A-Za-z0-9_.]+)\s*$', raw.decode()))
    add(manifest, 'recibos/supervivencia/BLOQUE_FOCAL.json', delta_raw, 'FOCAL_COMPILATION_RECEIPT')
    for name in ['verify_survival_chain.py', 'preparar_supervivencia.py',
                 'README_SUPERVIVENCIA_INTEGRADA.md', 'emit_survival_receipt.py',
                 'RECIBO_SUPERVIVENCIA_GENEALOGICO.json', 'SURVIVAL_GENEALOGY_CHECK.json',
                 'RECIBO_SUPERVIVENCIA_CAUSAL.json', 'SUPERVIVENCIA_CAUSAL_CHECK.json']:
        add(manifest, 'procedencia/supervivencia/' + name, (HERE / name).read_bytes(), 'DELTA_PROVENANCE')
    add(manifest, 'reproducir_supervivencia.py', (HERE / 'reproducir_supervivencia_portable.py').read_bytes(),
        'PORTABLE_CHAIN_RUNNER')
    metadata(manifest, owners)
    add(manifest, 'recibos/supervivencia/PRESERVACION.json', jb(dict(
        status='PREDECESSOR_BYTES_PRESERVED', predecessor_manifest_sha256=sha(old_raw),
        preserved_files=len(json.loads(old_raw)['files']),
        moved_unchanged={'README.md': MOVED_README},
        preservation_is_not_mathematical_completeness=True)), 'FILE_CONTINUITY')
    manifest[KEY] = dict(status='PREPARED_NOT_SEALED', modules=[r['module'] for r in owners],
        axiom_queries=probes, expected_total_modules=257, predecessor_manifest_sha256=sha(old_raw),
        scope='Survival selects one regional history and its registers; the post-R36 residual trajectory satisfies survival and the same joint signature.',
        complete_flm_formalization_claimed=False, full_enriched_U_identification_claimed=False)
    (ROOT / 'MANIFIESTO.json').write_bytes(jb(manifest))
    # The predecessor cache is authenticated above. The six new modules are
    # compiled by the portable verifier itself: their new external imports
    # then receive its full dependency fingerprints and joint import probe.
    print(json.dumps(dict(status='SURVIVAL_SUCCESSOR_PREPARED', root=str(ROOT),
        added=len(owners), expected_modules=257, preserved_files=len(json.loads(old_raw)['files']))))


def resume_prepared():
    """Repair only an unsigned staging copy after interrupted preparation."""
    old_raw, old, _ = validate_base()
    manifest = json.loads((ROOT / 'MANIFIESTO.json').read_text())
    if manifest[KEY]['status'] != 'PREPARED_NOT_SEALED' or ROOT.with_suffix('.zip').exists():
        raise RuntimeError('Only an unsealed staging copy may be resumed')
    if manifest[KEY]['predecessor_manifest_sha256'] != sha(old_raw):
        raise RuntimeError('Different predecessor')
    for row in old['files']:
        path = MOVED_README if row['path'] == 'README.md' else row['path']
        if digest(ROOT / path) != row['sha256']:
            raise RuntimeError('Predecessor bytes changed: ' + path)
    path = 'procedencia/supervivencia/preparar_supervivencia.py'
    raw = Path(__file__).read_bytes()
    for row in manifest['files']:
        if row['path'] == path:
            row.update(sha256=sha(raw), bytes=len(raw))
            break
    else:
        raise RuntimeError('Staging assembler was not manifested')
    (ROOT / path).write_bytes(raw)
    for row in manifest['files']:
        if digest(ROOT / row['path']) != row['sha256']:
            raise RuntimeError('Staging bytes changed: ' + row['path'])
    (ROOT / 'MANIFIESTO.json').write_bytes(jb(manifest))
    print('SURVIVAL_SUCCESSOR_PREPARED')


def seal():
    old_raw, old, _ = validate_base()
    raw = (ROOT / 'MANIFIESTO.json').read_bytes()
    manifest = json.loads(raw)
    if manifest[KEY]['status'] != 'PREPARED_NOT_SEALED':
        raise RuntimeError('Not prepared or already sealed')
    rp = ROOT / 'resultados/lean_unificado/VERIFICATION.json'
    run = json.loads(rp.read_text())
    if (run['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE'
            or run['manifest_sha256'] != sha(raw) or run['local_module_count'] != 257):
        raise RuntimeError('No matching 257-module PASS')
    dp = ROOT / 'resultados/datos_incidencia/VERIFICATION.json'
    if json.loads(dp.read_text())['status'] != 'PASS_PACKAGE_INCIDENCE_DATA':
        raise RuntimeError('Incidence data check failed')
    for row in manifest['files']:
        if digest(ROOT / row['path']) != row['sha256']:
            raise RuntimeError('Manifested bytes changed: ' + row['path'])
    for row in old['files']:
        path = MOVED_README if row['path'] == 'README.md' else row['path']
        if digest(ROOT / path) != row['sha256']:
            raise RuntimeError('Predecessor bytes lost: ' + row['path'])
    if sha(old_raw) != manifest[KEY]['predecessor_manifest_sha256']:
        raise RuntimeError('Predecessor manifest changed')
    add(manifest, 'recibos/supervivencia/MANIFIESTO_COMPILADO.json', raw, 'FROZEN_COMPILED_MANIFEST')
    add(manifest, 'recibos/supervivencia/LEAN_CONJUNTO.json', rp.read_bytes(), 'FROZEN_COMPILATION_RECEIPT')
    add(manifest, 'recibos/supervivencia/DATOS_INCIDENCIA.json', dp.read_bytes(), 'FROZEN_DATA_RECEIPT')
    manifest[KEY].update(status='SEALED_VERIFIED_SURVIVAL_REGISTERS', modules_in_closure=257,
        previous_bytes_preserved=True, fresh_probe_declarations=len(run['axiom_probe']['declarations']))
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
    print(json.dumps(dict(status='PASS_SURVIVAL_SUCCESSOR_SEALED', modules=257,
        new_modules=6, fresh_probe_queries=len(run['axiom_probe']['declarations']),
        preserved_files=len(old['files']), zip=str(archive), zip_sha256=digest(archive),
        manifest_sha256=sha(final)), ensure_ascii=False))


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    elif sys.argv[1:] == ['--resume-prepared']:
        resume_prepared()
    elif sys.argv[1:] == ['--seal']:
        seal()
    else:
        raise SystemExit('Use --prepare, --resume-prepared or --seal')
