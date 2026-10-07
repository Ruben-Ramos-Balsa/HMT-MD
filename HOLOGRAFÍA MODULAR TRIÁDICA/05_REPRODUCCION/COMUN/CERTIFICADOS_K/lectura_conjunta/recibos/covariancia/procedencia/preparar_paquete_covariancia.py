#!/usr/bin/env python3
"""Preserve the sealed field closure and append checked operator links."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent/'PAQUETE_ARTICULO_I_CAMPOS_RETICULARES_20260918'
ROOT = HERE.parent/'PAQUETE_ARTICULO_I_COVARIANCIA_RETICULAR_20260918'
STAGE = 'field_covariance_successor'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def register(mf, path, data, role):
    if any(r['path'] == path for r in mf['files']):
        raise RuntimeError('Attempt to replace manifested source: '+path)
    target = ROOT/path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    mf['files'].append(dict(path=path, sha256=sha(data), bytes=len(data),
        role=role, source='OPERATOR_COVARIANCE_CONTINUATION_20260918'))

def prepare():
    if ROOT.exists():
        raise RuntimeError('Successor exists; do not overwrite')
    config = json.loads((HERE/'COVARIANCE_MODULES.json').read_text())
    previous = (BASE/'MANIFIESTO.json').read_bytes()
    mf = json.loads(previous)
    for row in mf['files']:
        if sha((BASE/row['path']).read_bytes()) != row['sha256']:
            raise RuntimeError('Predecessor changed: '+row['path'])
    for row in config:
        receipt = json.loads((HERE/row['receipt']).read_text())
        if not receipt['status'].startswith('PASS'):
            raise RuntimeError('Unverified continuation: '+row['module'])
        source = HERE/(row['module']+'.lean')
        if sha(source.read_bytes()) != receipt['source_sha256']:
            raise RuntimeError('Source changed after verification: '+row['module'])
    shutil.copytree(BASE,ROOT)
    register(mf,'versiones_previas/MANIFIESTO_CAMPOS_SELLADO.json',previous,'EXACT_PREDECESSOR_MANIFEST')
    register(mf,'versiones_previas/README_CAMPOS_SELLADO.md',(ROOT/'README.md').read_bytes(),'EXACT_PREDECESSOR_ENTRY')
    readme = (HERE/'README_COVARIANCIA_ENTREGA.md').read_bytes()
    (ROOT/'README.md').write_bytes(readme)
    for row in mf['files']:
        if row['path'] == 'README.md':
            row.update(sha256=sha(readme),bytes=len(readme),role='CURRENT_ENTRY_PREVIOUS_PRESERVED')
    queries = []
    for row in config:
        raw = (HERE/(row['module']+'.lean')).read_bytes()
        register(mf,'deltas/covariancia/'+row['module']+'.lean',raw,'OPERATOR_SOURCE')
        register(mf,'recibos/covariancia/individuales/'+row['receipt'],
            (HERE/row['receipt']).read_bytes(),'INDIVIDUAL_COMPILATION_PROVENANCE')
        queries.extend(re.findall(r'(?m)^#print axioms ([A-Za-z0-9_.]+)\s*$',raw.decode()))
    if len(queries) != len(set(queries)):
        raise RuntimeError('Duplicate query')
    register(mf,'reproducir_covariancia.py',(HERE/'reproducir_covariancia_portable.py').read_bytes(),'PORTABLE_RUNNER')
    for name in ('COVARIANCE_MODULES.json','preparar_paquete_covariancia.py'):
        register(mf,'recibos/covariancia/procedencia/'+name,(HERE/name).read_bytes(),'ASSEMBLY_PROVENANCE')
    causal = json.loads((ROOT/'recibos/campos/RECIBO_CAUSAL.json').read_text())
    causal.update(artifact=str(ROOT/'README.md'),artifact_sha256=sha(readme),
        result_id='SELECTED_LATTICE_FIELD_COVARIANCE_20260918',
        scope='Operator covariance on the previously constructed selected lattice carrier. No complete FLM/Monster claim.',
        mathematical_result='Charge and parity covariance, charged translation, mixed oscillator commutator and corrected Coxeter lift on the preserved selected lattice.')
    causal['genealogy']['source_locators'].extend(str(ROOT/'deltas/covariancia'/(r['module']+'.lean')) for r in config)
    causalpath = 'recibos/covariancia/RECIBO_CAUSAL.json'
    register(mf,causalpath,(json.dumps(causal,indent=2,ensure_ascii=False)+'\n').encode(),'CAUSAL_METADATA_NOT_MATHEMATICAL_PROOF')
    check = subprocess.run([sys.executable,'-I','-S','/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py','--audit',str(ROOT/'README.md'),'--receipt',str(ROOT/causalpath)],capture_output=True,text=True)
    if check.returncode or 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY' not in check.stdout:
        raise RuntimeError(check.stdout+check.stderr)
    register(mf,'recibos/covariancia/CONTROL_CAUSAL.txt',(check.stdout+check.stderr).encode(),'CAUSAL_METADATA_CHECK')
    mf[STAGE] = dict(status='PREPARED_NOT_YET_JOINTLY_VERIFIED',
        modules=[r['module'] for r in config],axiom_queries=queries,
        predecessor_manifest_sha256=sha(previous),predecessor_files=len(json.loads(previous)['files']),
        preserved_files_relocated={'README.md':'versiones_previas/README_CAMPOS_SELLADO.md'},
        complete_flm_formalization_claimed=False)
    (ROOT/'MANIFIESTO.json').write_text(json.dumps(mf,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(dict(status='COVARIANCE_PREPARED',modules=len(config),queries=len(queries))))

def seal():
    raw=(ROOT/'MANIFIESTO.json').read_bytes()
    mf=json.loads(raw)
    if mf[STAGE]['status'] != 'PREPARED_NOT_YET_JOINTLY_VERIFIED':
        raise RuntimeError('Not an unsealed prepared successor')
    runpath=ROOT/'resultados/lean_unificado/VERIFICATION.json'
    run=json.loads(runpath.read_text())
    if run['status'] != 'PASS_PORTABLE_LEAN_SOURCE_CLOSURE' or run['manifest_sha256'] != sha(raw):
        raise RuntimeError('No verification for this exact manifest')
    if not set(mf[STAGE]['axiom_queries']).issubset(run['axiom_probe']['declarations']):
        raise RuntimeError('Missing axiom queries')
    for row in mf['files']:
        if sha((ROOT/row['path']).read_bytes()) != row['sha256']:
            raise RuntimeError('Source changed: '+row['path'])
    for row in json.loads((BASE/'MANIFIESTO.json').read_text())['files']:
        dest='versiones_previas/README_CAMPOS_SELLADO.md' if row['path']=='README.md' else row['path']
        if sha((ROOT/dest).read_bytes()) != row['sha256']:
            raise RuntimeError('Lost predecessor bytes: '+row['path'])
    register(mf,'recibos/covariancia/MANIFIESTO_COMPILADO.json',raw,'FROZEN_COMPILED_MANIFEST')
    register(mf,'recibos/covariancia/LEAN_CONJUNTO.json',runpath.read_bytes(),'FROZEN_JOINT_LEAN_RECEIPT')
    mf[STAGE].update(status='SEALED_VERIFIED_COVARIANCE',modules_in_closure=run['local_module_count'],
        verified_declarations=len(run['axiom_probe']['declarations']),predecessor_bytes_preserved=True)
    final=(json.dumps(mf,indent=2,ensure_ascii=False)+'\n').encode()
    (ROOT/'MANIFIESTO.json').write_bytes(final)
    archive=ROOT.with_suffix('.zip')
    if archive.exists():
        raise RuntimeError('Archive exists')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for path in sorted({r['path'] for r in mf['files']}|{'MANIFIESTO.json'}):
            z.write(ROOT/path,Path(ROOT.name)/path)
        if z.testzip():
            raise RuntimeError('Bad CRC')
        for row in mf['files']:
            if sha(z.read(str(Path(ROOT.name)/row['path']))) != row['sha256']:
                raise RuntimeError('ZIP content differs: '+row['path'])
    print(json.dumps(dict(status='PASS_OPERATOR_COVARIANCE_SEALED',modules=run['local_module_count'],
        declarations=len(run['axiom_probe']['declarations']),files=len(mf['files']),
        zip=str(archive),zip_sha256=sha(archive.read_bytes()),manifest_sha256=sha(final))))

if __name__ == '__main__':
    if sys.argv[1:]==['--prepare']: prepare()
    elif sys.argv[1:]==['--seal']: seal()
    else: raise SystemExit('Use --prepare or --seal')
