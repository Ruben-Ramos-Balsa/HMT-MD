#!/usr/bin/env python3
"""One preserved successor: recursive selection, records and joint signature."""
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
BASE = HERE.parent / 'PAQUETE_ARTICULO_I_SUPERVIVENCIA_REGISTROS_20260919'
ROOT = HERE.parent / 'PAQUETE_ARTICULO_I_SELECTOR_ITERADO_20260919'
PEER = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_SELECTOR_ITERADO_20260919')
KEY = 'iterated_selector_signature_successor'
DELTA = HERE / 'selector_chain_build/VERIFICATION.json'
BASE_RECEIPT = BASE / 'recibos/supervivencia/LEAN_CONJUNTO.json'
OLD_README = 'versiones_previas/README_SUPERVIVENCIA_SELLADO.md'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(path):
    return sha(Path(path).read_bytes())


def jb(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def add(manifest, path, raw, role, source='ITERATED_SELECTOR_SIGNATURE'):
    if (ROOT / path).exists() or any(row['path'] == path for row in manifest['files']):
        raise RuntimeError('Refusing replacement: ' + path)
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    manifest['files'].append(dict(path=path, sha256=sha(raw), bytes=len(raw), role=role, source=source))


def baseline():
    raw = (BASE / 'MANIFIESTO.json').read_bytes()
    manifest = json.loads(raw)
    for row in manifest['files']:
        if digest(BASE / row['path']) != row['sha256']:
            raise RuntimeError('Changed predecessor: ' + row['path'])
    receipt = json.loads(BASE_RECEIPT.read_text())
    if receipt['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE' or receipt['local_module_count'] != 257:
        raise RuntimeError('Expected authenticated package257')
    for row in receipt['modules']:
        if digest(BASE / row['source']) != row['source_sha256']:
            raise RuntimeError('Changed Lean source: ' + row['module'])
        if digest(BASE / 'resultados/lean_unificado/build' / (row['module'] + '.olean')) != row['object_sha256']:
            raise RuntimeError('Changed Lean object: ' + row['module'])
    return raw, manifest


def current_genealogy_scope(genealogy):
    record = genealogy['effective_result_record']
    record.update({
        '3_tpk_operator_domain_codomain_action': 'Selector finito max/min, guard inicial de parte entera, búsqueda de cotas y ejecución recursiva desde el padre anterior; composición con registros, elevaciones y firma de los mismos hijos. La igualdad a la publicación es conclusión, no entrada.',
        '4_coefficient_origin': 'Bases729=3^6 y1000 y los tres canales heredados; no se suministran valores objetivo, registrosX/Y ni elevacionesL como entradas del constructor.',
        '5_conservation': 'Recuperación exacta de ambos prefijos, compatibilidad cilíndrica, defecto entero, residuos y acarreo, eje y cargaWitt derivados de los mismos bloques seleccionados.',
        '6_enriched_state_and_continuum_residence': 'Componentes cilíndrico e incidencial del estado enriquecido, con su acoplamiento demostrado. No se identifica esta ejecución con nueve microactualizaciones de todas las fibras ni se construye un estado completo por producto independiente.',
        '7_hmt_output_before_recognition': 'Palabras y registros emitidos por la recursión, elevaciones únicas, cilindros y firma conjunta; el reconocimiento de las publicaciones se demuestra después.',
        '8_posterior_recognition_and_falsifier': 'Ambigüedad devuelve none; se prueba nofallo en la trayectoria regional y se comprueban ejemplos de hijoúnico/ambigüedad. Los recibos describen alcance; la prueba corresponde a los teoremas Lean.'})
    genealogy['foundation']['inheritance_boundary'] = record['6_enriched_state_and_continuum_residence']


def prepare():
    if ROOT.exists():
        raise RuntimeError('Successor exists; refusing overwrite')
    old_raw, manifest = baseline()
    raw_delta = DELTA.read_bytes()
    delta = json.loads(raw_delta)
    if delta['status'] != 'PASS_ITERATED_SELECTOR_SIGNATURE_CHAIN' or len(delta['modules']) != 4:
        raise RuntimeError('Four-module compilation has not passed')
    if delta['base_receipt_sha256'] != digest(BASE_RECEIPT):
        raise RuntimeError('Different predecessor receipt')
    for row in delta['modules']:
        if row['exit_code'] or digest(row['source']) != row['source_sha256']:
            raise RuntimeError('Changed delta source: ' + row['module'])
        if digest(DELTA.parent / (row['module'] + '.olean')) != row['object_sha256']:
            raise RuntimeError('Changed delta object: ' + row['module'])
    shutil.copytree(BASE, ROOT)
    add(manifest, 'versiones_previas/MANIFIESTO_SUPERVIVENCIA_SELLADO.json', old_raw,
        'EXACT_PREDECESSOR_MANIFEST')
    add(manifest, OLD_README, (ROOT / 'README.md').read_bytes(), 'EXACT_PREDECESSOR_ENTRY')
    new_readme = (HERE / 'README_SELECTOR_ITERADO_ENTREGA.md').read_bytes()
    (ROOT / 'README.md').write_bytes(new_readme)
    for row in manifest['files']:
        if row['path'] == 'README.md':
            row.update(sha256=sha(new_readme), bytes=len(new_readme), role='CURRENT_ITERATED_SELECTOR_ENTRY')
    owners, probes = [], []
    for row in delta['modules']:
        raw = Path(row['source']).read_bytes()
        path = 'deltas/selector/' + row['module'] + '.lean'
        add(manifest, path, raw, 'CHECKED_LEAN_SOURCE', row['source'])
        owners.append(dict(module=row['module'], path=path, sha256=sha(raw),
                           origin=row['source'], lines='1-' + str(len(raw.splitlines()))))
        probes.extend(re.findall(r'(?m)^#print axioms ([A-Za-z0-9_.]+)\s*$', raw.decode()))
    add(manifest, 'recibos/selector/BLOQUE_FOCAL.json', raw_delta, 'FOCAL_COMPILATION_RECEIPT')
    for filename in ['verify_selector_chain.py', 'preparar_selector_iterado.py']:
        add(manifest, 'procedencia/selector/' + filename, (HERE / filename).read_bytes(), 'DELTA_PROVENANCE')
    for filename in ['IteratedCylinderSelector.receipt.json', 'IteratedCylinderSelector.causal.json',
                     'README.md']:
        add(manifest, 'procedencia/selector/revisor/' + filename, (PEER / filename).read_bytes(),
            'INDEPENDENT_REVIEW_PROVENANCE')
    add(manifest, 'reproducir_selector.py', (HERE / 'reproducir_selector_portable.py').read_bytes(),
        'PORTABLE_CHAIN_RUNNER')
    # Context/provenance metadata is deliberately separate from the Lean receipt.
    genealogy = json.loads((BASE / 'recibos/supervivencia/RECIBO_GENEALOGICO.json').read_text())
    genealogy['artifact'].update(path=str(ROOT / 'README.md'), sha256=sha(new_readme),
        lines='1-' + str(len(new_readme.splitlines())), anchors=[
            {'stage':'APP','text':'APP →'}, {'stage':'TRIT','text':'TRIT →'},
            {'stage':'TPK','text':'TPK →'}, {'stage':'ESTADO_ENRIQUECIDO','text':'estado enriquecido'},
            {'stage':'ESTRUCTURA_DISCRETA_CONTINUO','text':'estructura discreta conjunta'},
            {'stage':'HMT_OUTPUT','text':'## Resultado comprobado'},
            {'stage':'CONVENTIONAL','text':'## Reproducción desde las fuentes'}])
    genealogy['effective_result_record']['9_material_owners'] = owners
    genealogy['local_proof_owners'] = owners
    genealogy['previous_scope_preserved'] = 'Preservación íntegra de las 846 entradas de paquete257; ningún PDF modificado.'
    genealogy['effective_result_record']['delta_scope'] = (
        'Current-parent iteration produces records/lifts and the same cylinder/signature fields; '
        'not nine enriched micro-updates and not full FLM.')
    current_genealogy_scope(genealogy)
    gp = 'recibos/selector/RECIBO_GENEALOGICO.json'
    add(manifest, gp, jb(genealogy), 'CONTEXT_METADATA_NOT_MATHEMATICAL_PROOF')
    for name in ['IteratedCylinderSelector', 'SelectedCylinderSignature']:
        causal = json.loads((PEER / (name + '.causal.json')).read_text())
        artifact = ROOT / 'deltas/selector' / (name + '.lean')
        causal.update(artifact=str(artifact), artifact_sha256=digest(artifact))
        cp = 'recibos/selector/' + name + '.causal.json'
        add(manifest, cp, jb(causal), 'CAUSAL_METADATA_NOT_MATHEMATICAL_PROOF')
        command = [sys.executable, '-I', '-S',
            '/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py',
            '--audit', str(artifact), '--receipt', str(ROOT / cp)]
        run = subprocess.run(command, text=True, capture_output=True)
        if run.returncode or 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY' not in run.stdout:
            raise RuntimeError(run.stdout + run.stderr)
        add(manifest, 'recibos/selector/' + name + '.causal_check.json',
            jb(dict(command=command, exit_code=run.returncode, output=run.stdout + run.stderr,
                    metadata_not_mathematical_proof=True)), 'METADATA_CHECK')
    cmd = [sys.executable, '-I', '-S', str(HERE.parents[1] / 'tools/verificar_genealogia_unica_hmt.py'),
           '--receipt', str(ROOT / gp)]
    run = subprocess.run(cmd, text=True, capture_output=True)
    if run.returncode or 'PASS_GENEALOGIA_UNICA_APP_TRIT_TPK' not in run.stdout:
        raise RuntimeError(run.stdout + run.stderr)
    add(manifest, 'recibos/selector/CONTROL_GENEALOGIA.json',
        jb(dict(command=cmd, exit_code=run.returncode, output=run.stdout + run.stderr,
                metadata_not_mathematical_proof=True)), 'METADATA_CHECK')
    add(manifest, 'recibos/selector/PRESERVACION.json', jb(dict(
        status='PREDECESSOR_BYTES_PRESERVED', predecessor_manifest_sha256=sha(old_raw),
        preserved_files=len(json.loads(old_raw)['files']), moved_unchanged={'README.md': OLD_README},
        preservation_is_not_mathematical_completeness=True)), 'FILE_CONTINUITY')
    manifest[KEY] = dict(status='PREPARED_NOT_SEALED', modules=[r['module'] for r in owners],
        axiom_queries=probes, expected_total_modules=261, predecessor_manifest_sha256=sha(old_raw),
        scope='Recursive rational selection, emitted records/lifts and same-block cylinder/signature fields.',
        full_flm_claimed=False, full_enriched_U_identification_claimed=False)
    (ROOT / 'MANIFIESTO.json').write_bytes(jb(manifest))
    print('ITERATED_SELECTOR_SUCCESSOR_PREPARED')


def amend_prepared_metadata():
    """Update only explicit-scope staging metadata before compilation/sealing."""
    manifest = json.loads((ROOT / 'MANIFIESTO.json').read_text())
    if manifest[KEY]['status'] != 'PREPARED_NOT_SEALED' or ROOT.with_suffix('.zip').exists():
        raise RuntimeError('Not an unsealed staging copy')
    path = 'recibos/selector/RECIBO_GENEALOGICO.json'
    genealogy = json.loads((ROOT / path).read_text())
    current_genealogy_scope(genealogy)
    replacements = {path: jb(genealogy),
        'procedencia/selector/preparar_selector_iterado.py': Path(__file__).read_bytes()}
    cmd = [sys.executable, '-I', '-S', str(HERE.parents[1] / 'tools/verificar_genealogia_unica_hmt.py'),
           '--receipt', str(ROOT / path)]
    for p, raw in replacements.items():
        (ROOT / p).write_bytes(raw)
    run = subprocess.run(cmd, text=True, capture_output=True)
    if run.returncode or 'PASS_GENEALOGIA_UNICA_APP_TRIT_TPK' not in run.stdout:
        raise RuntimeError(run.stdout + run.stderr)
    check = 'recibos/selector/CONTROL_GENEALOGIA.json'
    replacements[check] = jb(dict(command=cmd, exit_code=run.returncode,
        output=run.stdout + run.stderr, metadata_not_mathematical_proof=True))
    (ROOT / check).write_bytes(replacements[check])
    for row in manifest['files']:
        if row['path'] in replacements:
            raw = replacements[row['path']]
            row.update(sha256=sha(raw), bytes=len(raw))
        if digest(ROOT / row['path']) != row['sha256']:
            raise RuntimeError('Staging inconsistency: ' + row['path'])
    (ROOT / 'MANIFIESTO.json').write_bytes(jb(manifest))
    print('ITERATED_SELECTOR_STAGING_METADATA_CHECKED')


def seal():
    old_raw, old = baseline()
    raw = (ROOT / 'MANIFIESTO.json').read_bytes()
    manifest = json.loads(raw)
    if manifest[KEY]['status'] != 'PREPARED_NOT_SEALED':
        raise RuntimeError('Not an unsealed successor')
    receipt = ROOT / 'resultados/lean_unificado/VERIFICATION.json'
    run = json.loads(receipt.read_text())
    if (run['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE'
            or run['manifest_sha256'] != sha(raw) or run['local_module_count'] != 261):
        raise RuntimeError('No matching joint 261-module PASS')
    data = ROOT / 'resultados/datos_incidencia/VERIFICATION.json'
    if json.loads(data.read_text())['status'] != 'PASS_PACKAGE_INCIDENCE_DATA':
        raise RuntimeError('Incidence check failed')
    for row in manifest['files']:
        if digest(ROOT / row['path']) != row['sha256']:
            raise RuntimeError('Changed manifested bytes: ' + row['path'])
    for row in old['files']:
        path = OLD_README if row['path'] == 'README.md' else row['path']
        if digest(ROOT / path) != row['sha256']:
            raise RuntimeError('Lost predecessor bytes: ' + path)
    add(manifest, 'recibos/selector/MANIFIESTO_COMPILADO.json', raw, 'FROZEN_COMPILED_MANIFEST')
    add(manifest, 'recibos/selector/LEAN_CONJUNTO.json', receipt.read_bytes(), 'FROZEN_COMPILATION_RECEIPT')
    add(manifest, 'recibos/selector/DATOS_INCIDENCIA.json', data.read_bytes(), 'FROZEN_DATA_RECEIPT')
    manifest[KEY].update(status='SEALED_VERIFIED_ITERATED_SELECTOR_SIGNATURE',
        modules_in_closure=261, previous_bytes_preserved=True,
        fresh_probe_declarations=len(run['axiom_probe']['declarations']))
    final = jb(manifest)
    (ROOT / 'MANIFIESTO.json').write_bytes(final)
    archive = ROOT.with_suffix('.zip')
    if archive.exists():
        raise RuntimeError('Refusing to overwrite archive')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zip:
        for name in sorted({r['path'] for r in manifest['files']} | {'MANIFIESTO.json'}):
            zip.write(ROOT / name, Path(ROOT.name) / name)
        if zip.testzip():
            raise RuntimeError('ZIP CRC failure')
        for row in manifest['files']:
            if sha(zip.read(str(Path(ROOT.name) / row['path']))) != row['sha256']:
                raise RuntimeError('ZIP byte mismatch: ' + row['path'])
    print(json.dumps(dict(status='PASS_ITERATED_SELECTOR_SUCCESSOR_SEALED', modules=261,
        new_modules=4, preserved_files=len(old['files']),
        fresh_probe_queries=len(run['axiom_probe']['declarations']),
        zip=str(archive), zip_sha256=digest(archive), manifest_sha256=sha(final)), ensure_ascii=False))


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    elif sys.argv[1:] == ['--seal']:
        seal()
    elif sys.argv[1:] == ['--amend-prepared-metadata']:
        amend_prepared_metadata()
    else:
        raise SystemExit('Use --prepare or --seal')
