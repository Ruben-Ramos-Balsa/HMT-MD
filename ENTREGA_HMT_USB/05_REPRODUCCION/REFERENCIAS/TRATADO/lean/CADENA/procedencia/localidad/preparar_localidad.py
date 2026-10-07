#!/usr/bin/env python3
"""Build one successor; preserve the sealed predecessor and seal only after PASS."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent/'PAQUETE_ARTICULO_I_PRODUCTOS_RETICULARES_20260919'
ROOT = HERE.parent/'PAQUETE_ARTICULO_I_LOCALIDAD_CAMPOS_20260919'
REVIEWER = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_PRODUCTO_CAMPOS_20260919')
KEY = 'charged_locality_successor'
OWN = ['LatticeContractionPascal', 'LatticeTwoRegionFactor', 'LatticeFactorConvolution',
       'LatticeNormalProduct', 'LatticeProductCocycle', 'LatticeConvolutionFinite',
       'LatticeConvolutionSwap', 'LatticeNormalCoefficients', 'LatticeNormalSymmetry',
       'LatticeDressedSymmetry', 'LatticeFieldNormalBridge', 'LatticeChargedLocality',
       'LatticeFieldBiOperators', 'LatticeChargedLocalityFull', 'SelectedFieldLocality']
EXTERNAL = ['LatticeWeightFiltration', 'LatticeFieldCutoff', 'LatticeOperatorCutoff',
            'LatticeFieldProductCutoff', 'LatticeAntidiagonalRectangle',
            'LatticeFieldProductRectangle', 'LatticeFieldProductLinearity']

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def digest(path):
    return sha(Path(path).read_bytes())

def jb(value):
    return (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode()

def add(manifest, name, raw, role, source='CHECKED_LOCALITY_CONTINUATION'):
    if any(row['path'] == name for row in manifest['files']):
        raise RuntimeError('Existing manifested path: '+name)
    path = ROOT/name
    if path.exists():
        raise RuntimeError('Existing destination: '+name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    manifest['files'].append(dict(path=name, sha256=sha(raw), bytes=len(raw),
                                  role=role, source=source))

def validate_base():
    raw = (BASE/'MANIFIESTO.json').read_bytes()
    manifest = json.loads(raw)
    for row in manifest['files']:
        if digest(BASE/row['path']) != row['sha256']:
            raise RuntimeError('Changed predecessor file: '+row['path'])
    r = json.loads((BASE/'recibos/productos/LEAN_CONJUNTO.json').read_text())
    if r['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE' or len(r['modules']) != 216:
        raise RuntimeError('Expected verified 216-module predecessor')
    for row in r['modules']:
        if digest(BASE/row['source']) != row['source_sha256']:
            raise RuntimeError('Changed predecessor Lean source: '+row['module'])
        if digest(BASE/'resultados/lean_unificado/build'/(row['module']+'.olean')) != row['object_sha256']:
            raise RuntimeError('Changed predecessor cached object: '+row['module'])
    return raw, manifest

def validate_locality():
    path = HERE/'locality_block_build/VERIFICATION.json'
    raw = path.read_bytes()
    result = json.loads(raw)
    if result['status'] != 'PASS_LOCALITY_BLOCK_CURRENT_MODULES':
        raise RuntimeError('Locality block is not PASS: '+result['status'])
    if [r['module'] for r in result['modules']] != OWN:
        raise RuntimeError('Unexpected root-module selection')
    if [r['module'] for r in result['reviewer_modules']] != EXTERNAL:
        raise RuntimeError('Unexpected reviewer-module selection')
    if result['base_receipt_sha256'] != digest(BASE/'recibos/productos/LEAN_CONJUNTO.json'):
        raise RuntimeError('Locality block names another predecessor receipt')
    for row in result['modules']:
        name = row['module']
        if row['exit_code'] or digest(HERE/(name+'.lean')) != row['source_sha256']:
            raise RuntimeError('Unverified root source: '+name)
        if digest(HERE/'locality_block_build'/(name+'.olean')) != row['object_sha256']:
            raise RuntimeError('Changed root object: '+name)
    for row in result['reviewer_modules']:
        name = row['module']
        rp = REVIEWER/(name+'.receipt.json')
        receipt = json.loads(rp.read_text())
        if (receipt['status'] != 'PASS_FOCUSED_FIELD_MODULE' or
                digest(rp) != row['receipt_sha256'] or
                digest(REVIEWER/(name+'.lean')) != row['source_sha256'] or
                digest(REVIEWER/(name+'.olean')) != row['object_sha256']):
            raise RuntimeError('Unverified reviewer source/object/receipt: '+name)
    if (HERE/'LatticeFieldBiOperators.lean').read_bytes() != (REVIEWER/'LatticeFieldBiOperators.lean').read_bytes():
        raise RuntimeError('BiOperators copies differ')
    return raw, result

def prepare():
    if ROOT.exists():
        raise RuntimeError('Successor already exists; will not overwrite')
    predecessor_raw, mf = validate_base()
    block_raw, block = validate_locality()
    # Local caches are copied only to avoid recompiling the verified base.
    # They never enter the manifested ZIP and are reauthenticated by the runner.
    shutil.copytree(BASE, ROOT)
    add(mf, 'versiones_previas/MANIFIESTO_PRODUCTOS_SELLADO.json', predecessor_raw,
        'EXACT_PREDECESSOR_MANIFEST')
    add(mf, 'versiones_previas/README_PRODUCTOS_SELLADO.md', (ROOT/'README.md').read_bytes(),
        'EXACT_PREDECESSOR_ENTRY')
    new = (HERE/'README_LOCALIDAD_ENTREGA.md').read_bytes()
    (ROOT/'README.md').write_bytes(new)
    for row in mf['files']:
        if row['path'] == 'README.md':
            row.update(sha256=sha(new), bytes=len(new), role='CURRENT_LOCALITY_ENTRY')
    modules = OWN + EXTERNAL
    queries = []
    owners = []
    for name in modules:
        origin = HERE if name in OWN else REVIEWER
        src = origin/(name+'.lean')
        raw = src.read_bytes()
        target = 'deltas/localidad/'+name+'.lean'
        add(mf, target, raw, 'PROVED_OPERATOR_SOURCE', str(src))
        queries += re.findall(r'(?m)^#print axioms ([A-Za-z0-9_.]+)\s*$', raw.decode())
        owners.append(dict(module=name, path=target, sha256=sha(raw), origin=str(src)))
    add(mf, 'recibos/localidad/BLOQUE_FOCAL.json', block_raw, 'FOCUSED_COMPILATION_RECEIPT')
    for name in EXTERNAL:
        for suffix in ['.receipt.json', '.log']:
            src = REVIEWER/(name+suffix)
            add(mf, 'recibos/localidad/revisor/'+src.name, src.read_bytes(),
                'REVIEWER_COMPILATION_EVIDENCE', str(src))
    for directory in ['normal_symmetry_build', 'dressed_symmetry_build']:
        for filename in ['VERIFICATION.json', 'COMPILE.log']:
            src = HERE/directory/filename
            add(mf, 'recibos/localidad/'+directory+'/'+filename, src.read_bytes(),
                'FOCUSED_COMPILATION_EVIDENCE', str(src))
    for src, dest, role in [
        ('reproducir_localidad_portable.py', 'reproducir_localidad.py', 'PORTABLE_RUNNER'),
        ('preparar_localidad.py', 'procedencia/localidad/preparar_localidad.py', 'ASSEMBLY_PROVENANCE'),
        ('verify_locality_block.py', 'procedencia/localidad/verify_locality_block.py', 'FOCUSED_RUNNER_PROVENANCE')]:
        add(mf, dest, (HERE/src).read_bytes(), role)
    add(mf, 'procedencia/localidad/compile_focused.py', (REVIEWER/'compile_focused.py').read_bytes(),
        'REVIEWER_RUNNER_PROVENANCE')
    c = json.loads((ROOT/'recibos/productos/RECIBO_CAUSAL.json').read_text())
    scope = ('Uniform charged-field locality on the original selected carrier, all charges and all states; '
             'preserved incidence and generation; no full VOA, orbifold or FLM assertion.')
    c.update(artifact=str(ROOT/'README.md'), artifact_sha256=sha(new),
             result_id='SELECTED_CHARGED_FIELD_LOCALITY_20260919', scope=scope,
             mathematical_result=scope,
             predecessor_receipt=dict(path='recibos/productos/RECIBO_CAUSAL.json',
                                      sha256=digest(ROOT/'recibos/productos/RECIBO_CAUSAL.json')))
    c['genealogy']['source_locators'] += [str(ROOT/x['path']) for x in owners]
    c['genealogical_result_record']['9_material_owners'] += owners
    c['genealogical_result_record']['7_hmt_output_before_recognition'] += (
        ' Uniform locality is proved for the actual charged fields on this same selected carrier.')
    add(mf, 'recibos/localidad/RECIBO_CAUSAL.json', jb(c),
        'CAUSAL_METADATA_NOT_MATHEMATICAL_PROOF')
    command = [sys.executable, '-I', '-S',
        '/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py',
        '--audit', str(ROOT/'README.md'), '--receipt', str(ROOT/'recibos/localidad/RECIBO_CAUSAL.json')]
    p = subprocess.run(command, text=True, capture_output=True)
    if p.returncode or 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY' not in p.stdout:
        raise RuntimeError(p.stdout+p.stderr)
    add(mf, 'recibos/localidad/CONTROL_CAUSAL.txt', (p.stdout+p.stderr).encode(), 'CAUSAL_METADATA_CHECK')
    preservation = dict(status='PREDECESSOR_MANIFESTED_BYTES_PRESERVED',
        predecessor_manifest_sha256=sha(predecessor_raw), file_count=len(json.loads(predecessor_raw)['files']),
        moved_unchanged={'README.md': 'versiones_previas/README_PRODUCTOS_SELLADO.md'},
        compiler_verifies_sources_separately=True)
    add(mf, 'recibos/localidad/PRESERVACION.json', jb(preservation), 'FILE_PRESERVATION_NOT_PROOF')
    mf[KEY] = dict(status='PREPARED_NOT_COMPILED', modules=modules, axiom_queries=queries,
        predecessor_manifest_sha256=sha(predecessor_raw), expected_total_modules=238,
        entry='SelectedFieldLocality', scope=scope, complete_flm_formalization_claimed=False)
    (ROOT/'MANIFIESTO.json').write_bytes(jb(mf))
    print(json.dumps(dict(status='LOCALITY_SUCCESSOR_PREPARED', modules_added=len(modules),
                          new_axiom_queries=len(queries), root=str(ROOT))))

def refresh_editorial():
    """Refresh an unsealed README, causal metadata and assembly source only."""
    prior_manifest = (ROOT/'MANIFIESTO.json').read_bytes()
    mf = json.loads(prior_manifest)
    if mf[KEY]['status'] != 'PREPARED_NOT_COMPILED':
        raise RuntimeError('Only an unsealed prepared package may be refreshed')
    prior_run = (ROOT/'resultados/lean_unificado/VERIFICATION.json').read_bytes()
    checked = json.loads(prior_run)
    if (checked['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE' or
            checked['manifest_sha256'] != sha(prior_manifest)):
        raise RuntimeError('Refresh requires the completed matching proof run')
    add(mf, 'recibos/localidad/PRIMERA_COMPILACION_22.json', prior_run,
        'CHECKED_FIRST_PASS_BEFORE_METADATA_PRECISION')
    add(mf, 'recibos/localidad/MANIFIESTO_PRIMERA_COMPILACION.json', prior_manifest,
        'FROZEN_FIRST_PASS_MANIFEST')
    add(mf, 'recibos/localidad/README_PRIMERA_COMPILACION.md',
        (ROOT/'README.md').read_bytes(), 'FIRST_PASS_EDITORIAL_ANTECEDENT')
    new = (HERE/'README_LOCALIDAD_ENTREGA.md').read_bytes()
    (ROOT/'README.md').write_bytes(new)
    (ROOT/'procedencia/localidad/preparar_localidad.py').write_bytes(Path(__file__).read_bytes())
    cp = ROOT/'recibos/localidad/RECIBO_CAUSAL.json'
    c = json.loads(cp.read_text())
    c['artifact_sha256'] = sha(new)
    cp.write_bytes(jb(c))
    p = subprocess.run([sys.executable, '-I', '-S',
        '/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py',
        '--audit', str(ROOT/'README.md'), '--receipt', str(cp)], text=True, capture_output=True)
    if p.returncode or 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY' not in p.stdout:
        raise RuntimeError(p.stdout+p.stderr)
    (ROOT/'recibos/localidad/CONTROL_CAUSAL.txt').write_text(p.stdout+p.stderr)
    changed = {'README.md', 'procedencia/localidad/preparar_localidad.py',
               'recibos/localidad/RECIBO_CAUSAL.json', 'recibos/localidad/CONTROL_CAUSAL.txt'}
    for row in mf['files']:
        if row['path'] in changed:
            data = (ROOT/row['path']).read_bytes()
            row.update(sha256=sha(data), bytes=len(data))
    (ROOT/'MANIFIESTO.json').write_bytes(jb(mf))
    print('EDITORIAL_METADATA_REFRESHED_REVERIFICATION_REQUIRED')

def clarify_cache_scope():
    """Preserve the first seal and correct only the documented cache scope."""
    final_raw = (ROOT/'MANIFIESTO.json').read_bytes()
    mf = json.loads(final_raw)
    if mf[KEY]['status'] != 'SEALED_VERIFIED_CHARGED_FIELD_LOCALITY':
        raise RuntimeError('Expected a sealed locality package')
    archive = ROOT.with_suffix('.zip')
    old_zip_hash = digest(archive)
    for row in mf['files']:
        if digest(ROOT/row['path']) != row['sha256']:
            raise RuntimeError('First-seal file changed: '+row['path'])
    add(mf, 'recibos/localidad/primer_sello/MANIFIESTO.json', final_raw,
        'EXACT_FIRST_SEAL_MANIFEST')
    add(mf, 'recibos/localidad/primer_sello/README.md', (ROOT/'README.md').read_bytes(),
        'EXACT_FIRST_SEAL_README')
    add(mf, 'recibos/localidad/primer_sello/preparar_localidad.py',
        (ROOT/'procedencia/localidad/preparar_localidad.py').read_bytes(),
        'EXACT_FIRST_SEAL_ASSEMBLY_SOURCE')
    for filename in ['MANIFIESTO_COMPILADO.json', 'LEAN_CONJUNTO.json', 'DATOS_INCIDENCIA.json']:
        source = 'recibos/localidad/'+filename
        target = 'recibos/localidad/primer_sello/'+filename
        (ROOT/target).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(ROOT/source), str(ROOT/target))
        row = next(r for r in mf['files'] if r['path'] == source)
        row['path'] = target
        row['role'] = 'PRESERVED_FIRST_SEAL_RECEIPT'
    stored_zip = ROOT/'resultados/primer_sello'/archive.name
    stored_zip.parent.mkdir(parents=True, exist_ok=True)
    if stored_zip.exists():
        raise RuntimeError('First-seal ZIP antecedent already exists')
    shutil.move(str(archive), str(stored_zip))
    add(mf, 'recibos/localidad/primer_sello/SELLO_Y_CORRECCION.json', jb(dict(
        first_zip_sha256=old_zip_hash, first_manifest_sha256=sha(final_raw),
        preserved_zip_local_only=str(stored_zip),
        correction='README explicitly distinguishes excluded current cache from three preserved historical FoundationContract objects.',
        lean_sources_changed=False)), 'FIRST_SEAL_HASH_AND_EDITORIAL_CORRECTION')
    new = (HERE/'README_LOCALIDAD_ENTREGA.md').read_bytes()
    (ROOT/'README.md').write_bytes(new)
    (ROOT/'procedencia/localidad/preparar_localidad.py').write_bytes(Path(__file__).read_bytes())
    cp = ROOT/'recibos/localidad/RECIBO_CAUSAL.json'
    c = json.loads(cp.read_text())
    c['artifact_sha256'] = sha(new)
    cp.write_bytes(jb(c))
    p = subprocess.run([sys.executable, '-I', '-S',
        '/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py',
        '--audit', str(ROOT/'README.md'), '--receipt', str(cp)], text=True, capture_output=True)
    if p.returncode or 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY' not in p.stdout:
        raise RuntimeError(p.stdout+p.stderr)
    (ROOT/'recibos/localidad/CONTROL_CAUSAL.txt').write_text(p.stdout+p.stderr)
    changed = {'README.md', 'procedencia/localidad/preparar_localidad.py',
               'recibos/localidad/RECIBO_CAUSAL.json', 'recibos/localidad/CONTROL_CAUSAL.txt'}
    for row in mf['files']:
        if row['path'] in changed:
            data = (ROOT/row['path']).read_bytes()
            row.update(sha256=sha(data), bytes=len(data))
    mf[KEY]['status'] = 'PREPARED_NOT_COMPILED'
    mf[KEY]['editorial_correction'] = 'Explicit current-cache versus historical-object distinction; no proof-source changes.'
    (ROOT/'MANIFIESTO.json').write_bytes(jb(mf))
    print('CACHE_SCOPE_CLARIFIED_REVERIFICATION_REQUIRED')

def seal():
    predecessor_raw, predecessor = validate_base()
    raw = (ROOT/'MANIFIESTO.json').read_bytes()
    mf = json.loads(raw)
    run_path = ROOT/'resultados/lean_unificado/VERIFICATION.json'
    run = json.loads(run_path.read_text())
    if mf[KEY]['status'] != 'PREPARED_NOT_COMPILED':
        raise RuntimeError('Not prepared or already sealed')
    if (run['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE' or
            run['manifest_sha256'] != sha(raw) or run['local_module_count'] != 238):
        raise RuntimeError('No current 238-module PASS')
    data_path = ROOT/'resultados/datos_incidencia/VERIFICATION.json'
    if json.loads(data_path.read_text())['status'] != 'PASS_PACKAGE_INCIDENCE_DATA':
        raise RuntimeError('Data reproduction did not pass')
    for row in mf['files']:
        if digest(ROOT/row['path']) != row['sha256']:
            raise RuntimeError('Manifested file changed: '+row['path'])
    for row in predecessor['files']:
        dest = ('versiones_previas/README_PRODUCTOS_SELLADO.md'
                if row['path'] == 'README.md' else row['path'])
        if digest(ROOT/dest) != row['sha256']:
            raise RuntimeError('Predecessor bytes not preserved: '+row['path'])
    if sha(predecessor_raw) != mf[KEY]['predecessor_manifest_sha256']:
        raise RuntimeError('Predecessor manifest changed')
    for module in OWN+EXTERNAL:
        record = next(r for r in run['modules'] if r['module'] == module)
        allowed = {'propext', 'Classical.choice', 'Quot.sound'}
        if module == 'SelectedFieldLocality':
            allowed.add('Lean.ofReduceBool')  # Preserved finite-selector dependency.
        if set(a for aa in record['axioms'].values() for a in aa) - allowed:
            raise RuntimeError('Unexpected new-block axiom: '+module)
    add(mf, 'recibos/localidad/MANIFIESTO_COMPILADO.json', raw, 'FROZEN_COMPILED_MANIFEST')
    add(mf, 'recibos/localidad/LEAN_CONJUNTO.json', run_path.read_bytes(), 'FROZEN_COMPILE_RECEIPT')
    add(mf, 'recibos/localidad/DATOS_INCIDENCIA.json', data_path.read_bytes(), 'FROZEN_DATA_CHECK')
    mf[KEY].update(status='SEALED_VERIFIED_CHARGED_FIELD_LOCALITY',
        modules_in_closure=run['local_module_count'], compiled=run['compiled_modules'],
        reused=len(run['cached_modules']), previous_bytes_preserved=True,
        fresh_probe_declarations=len(run['axiom_probe']['declarations']))
    final = jb(mf)
    (ROOT/'MANIFIESTO.json').write_bytes(final)
    archive = ROOT.with_suffix('.zip')
    if archive.exists():
        raise RuntimeError('ZIP already exists; will not overwrite')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        paths = {r['path'] for r in mf['files']} | {'MANIFIESTO.json'}
        for path in sorted(paths):
            z.write(ROOT/path, Path(ROOT.name)/path)
        if z.testzip():
            raise RuntimeError('ZIP CRC failure')
        for row in mf['files']:
            if sha(z.read(str(Path(ROOT.name)/row['path']))) != row['sha256']:
                raise RuntimeError('ZIP content mismatch: '+row['path'])
    print(json.dumps(dict(status='PASS_LOCALITY_SUCCESSOR_SEALED', modules=run['local_module_count'],
        compiled=len(run['compiled_modules']), reused=len(run['cached_modules']),
        source_axiom_queries=sum(len(r['axioms']) for r in run['modules']),
        fresh_probe_queries=len(run['axiom_probe']['declarations']),
        preserved_files=len(predecessor['files']), zip=str(archive),
        zip_sha256=digest(archive), manifest_sha256=sha(final)), ensure_ascii=False))

if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    elif sys.argv[1:] == ['--seal']:
        seal()
    elif sys.argv[1:] == ['--refresh-editorial']:
        refresh_editorial()
    elif sys.argv[1:] == ['--clarify-cache-scope']:
        clarify_cache_scope()
    else:
        raise SystemExit('Use --prepare, --refresh-editorial or --seal')
