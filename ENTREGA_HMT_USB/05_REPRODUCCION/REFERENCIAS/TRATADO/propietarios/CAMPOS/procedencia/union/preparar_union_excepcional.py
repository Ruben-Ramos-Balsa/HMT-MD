#!/usr/bin/env python3
"""Immutable source union and explicit adoption of independently checked objects."""
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
BASE = HERE.parent/'PAQUETE_ARTICULO_I_GENERACION_Y_ORDEN_NORMAL_20260919'
ROOT = HERE.parent/'PAQUETE_ARTICULO_I_CADENA_EXCEPCIONAL_20260919'
PEER = Path('/Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_GOLAY_STEINER_20260919')
P = PEER/'entrega'
STAGE = 'exceptional_union_successor'

def sha(data): return hashlib.sha256(data).hexdigest()
def hashfile(path): return sha(Path(path).read_bytes())
def jsonbytes(data): return (json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()

def register(mf, path, data, role):
    if any(r['path']==path for r in mf['files']):
        raise RuntimeError('No silent replacement: '+path)
    target=ROOT/path
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
    mf['files'].append(dict(path=path,sha256=sha(data),bytes=len(data),role=role,
        source='CHECKED_EXCEPTIONAL_UNION_20260919'))

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def prepare():
    if ROOT.exists(): raise RuntimeError('Successor already exists')
    raw=(BASE/'MANIFIESTO.json').read_bytes()
    mf=json.loads(raw)
    for row in mf['files']:
        if hashfile(BASE/row['path'])!=row['sha256']:
            raise RuntimeError('Changed base: '+row['path'])
    pm=json.loads((P/'MANIFEST.json').read_text())
    if hashfile(P/'MANIFEST.json')!='befd1b9ab5df0df98badff14879ab4d0d96779f34c2f4dd63a3d682e2e1852bf':
        raise RuntimeError('Peer final manifest changed')
    for path,h in pm['files'].items():
        if hashfile(P/path)!=h: raise RuntimeError('Changed peer: '+path)
    peerzip=json.loads((PEER/'ZIP_VERIFICATION.json').read_text())
    if peerzip['status']!='PASS_EXTRACTED_ZIP_ELEVEN_DELTAS':
        raise RuntimeError('Peer ZIP not verified')
    closure=json.loads((P/'SOURCE_CLOSURE.json').read_text())
    run=json.loads((PEER/'package_build/VERIFICATION.json').read_text())
    if run['status']!='PASS_GOLAY_STEINER_SPIN_T_SOURCE_BUNDLE':
        raise RuntimeError('Peer compilation not verified')
    shutil.copytree(BASE,ROOT)
    register(mf,'versiones_previas/MANIFIESTO_GENERACION_SELLADO.json',raw,'EXACT_PREDECESSOR_MANIFEST')
    register(mf,'versiones_previas/README_GENERACION_SELLADO.md',(ROOT/'README.md').read_bytes(),'EXACT_PREDECESSOR_ENTRY')
    readme=(HERE/'README_CADENA_ENTREGA.md').read_bytes()
    (ROOT/'README.md').write_bytes(readme)
    for row in mf['files']:
        if row['path']=='README.md': row.update(sha256=sha(readme),bytes=len(readme))
    available={}
    for row in mf['files']:
        if row['path'].endswith('.lean'):
            available.setdefault(Path(row['path']).stem,[]).append(row)
    transferred=[]
    needed=[r for r in closure['base_modules'] if r['origin_receipt']=='II_III']+closure['deltas']
    for row in needed:
        name=row['module']
        matches=[r for r in available.get(name,[]) if r['sha256']==row['source_sha256']]
        if not matches:
            register(mf,'deltas/union/'+name+'.lean',(P/row['source']).read_bytes(),'RECOVERED_VERIFIED_SOURCE')
        transferred.append(dict(module=name,source_sha256=row['source_sha256'],
            source_preexisting=bool(matches),peer_source=row['source']))
    for source,target,role in [
        (P/'SOURCE_CLOSURE.json','procedencia/union/PEER_SOURCE_CLOSURE.json','SOURCE_CLOSURE_PROVENANCE'),
        (P/'MANIFEST.json','procedencia/union/PEER_MANIFEST.json','PEER_MANIFEST'),
        (PEER/'package_build/VERIFICATION.json','procedencia/union/PEER_COMPILATION.json','PEER_COMPILATION'),
        (PEER/'ZIP_VERIFICATION.json','procedencia/union/PEER_ZIP_VERIFICATION.json','PEER_ZIP_VERIFICATION'),
        (PEER/'ZIP_VERIFICATION_EVIDENCE/VERIFICATION.json','procedencia/union/PEER_EXTRACTED_COMPILATION.json','PEER_EXTRACTED_COMPILATION'),
        (P/'provenance/II_III_RECEIPT.json','procedencia/union/II_III_RECEIPT.json','DEPENDENCY_COMPILATION'),
        (P/'data/incidence_chart_132.json','datos/union/incidence_chart_132.json','EXPLICIT_INCIDENCE_CHART'),
        (P/'documentation/excepcional.tex','fuentes/union/excepcional.tex','LATEX_SOURCE_PROVENANCE'),
        (P/'binary/check_golay.py','python/union/check_golay.py','INDEPENDENT_CHECK'),
        (P/'chart/check_incidence_chart.py','python/union/check_incidence_chart.py','INDEPENDENT_CHECK'),
        (HERE/'reproducir_cadena_portable.py','reproducir_cadena.py','PORTABLE_RUNNER'),
        (HERE/'SelectedExceptionalChain.lean','deltas/union/SelectedExceptionalChain.lean','COMPOSITION_ENTRY'),
        (HERE/'preparar_union_excepcional.py','procedencia/union/preparar_union_excepcional.py','ASSEMBLY_PROVENANCE')]:
        register(mf,target,source.read_bytes(),role)
    queries=re.findall(r'(?m)^#print axioms ([A-Za-z0-9_.]+)\s*$',
        (HERE/'SelectedExceptionalChain.lean').read_text())
    mf[STAGE]=dict(status='PREPARED_NOT_YET_JOINTLY_VERIFIED',
        modules=[r['module'] for r in needed]+['SelectedExceptionalChain'],
        axiom_queries=queries,transfer=transferred,predecessor_manifest_sha256=sha(raw),
        peer_manifest_sha256=hashfile(P/'MANIFEST.json'),
        complete_flm_formalization_claimed=False)
    causal=json.loads((ROOT/'recibos/generacion/RECIBO_CAUSAL.json').read_text())
    causal.update(artifact=str(ROOT/'README.md'),artifact_sha256=sha(readme),
        result_id='SELECTED_EXCEPTIONAL_CHAIN_UNION_20260919',
        scope='Same selected origin, concrete residual Golay chart and all-degree reticular fields; no complete FLM or Monster assertion.')
    causal['genealogy']['source_locators'].append(str(ROOT/'deltas/union/SelectedExceptionalChain.lean'))
    register(mf,'recibos/union/RECIBO_CAUSAL.json',jsonbytes(causal),'CAUSAL_METADATA_NOT_MATHEMATICAL_PROOF')
    p=subprocess.run([sys.executable,'-I','-S','/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py',
        '--audit',str(ROOT/'README.md'),'--receipt',str(ROOT/'recibos/union/RECIBO_CAUSAL.json')],capture_output=True,text=True)
    if p.returncode or 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY' not in p.stdout:
        raise RuntimeError(p.stdout+p.stderr)
    register(mf,'recibos/union/CONTROL_CAUSAL.txt',(p.stdout+p.stderr).encode(),'CAUSAL_METADATA_CHECK')
    (ROOT/'MANIFIESTO.json').write_bytes(jsonbytes(mf))
    print(json.dumps(dict(status='PREPARED_EXCEPTIONAL_UNION',added_or_reused=len(needed))))

def adopt():
    mf=json.loads((ROOT/'MANIFIESTO.json').read_text())
    runner=load_module(ROOT/'reproducir_cadena.py','unionrunner')
    v=runner.configure(ROOT)
    plan=v.load_plan(ROOT)
    prior=json.loads((BASE/'recibos/generacion/LEAN_CONJUNTO.json').read_text())
    closure=json.loads((P/'SOURCE_CLOSURE.json').read_text())
    peer=json.loads((PEER/'package_build/VERIFICATION.json').read_text())
    ii=json.loads((P/'provenance/II_III_RECEIPT.json').read_text())
    if prior['status']!='PASS_PORTABLE_LEAN_SOURCE_CLOSURE' or not ii['status'].startswith('PASS'):
        raise RuntimeError('Unverified predecessor')
    compiler=prior['compiler']
    if hashfile(compiler['executable'])!=compiler['binary_sha256'] or compiler['verifier_sha256']!=hashfile(ROOT/'verificar_lean.py'):
        raise RuntimeError('Compiler/verifier changed')
    if peer['compiler']['binary_sha256']!=compiler['binary_sha256'] or closure['cache_compiler_sha256']!=compiler['binary_sha256']:
        raise RuntimeError('Peer compiler mismatch')
    if closure['mathlib_commit']!=compiler['mathlib_commit']:
        raise RuntimeError('Peer mathlib mismatch')
    for label in ['BASE178','II_III']:
        if hashfile(P/('provenance/'+label+'_RECEIPT.json'))!=closure['origin_receipts'][label]:
            raise RuntimeError('Peer dependency receipt changed')
    external=dict(prior['external_objects'])
    paths=[Path(p) for p in prior['lean_path'].split(':')[1:]]
    for name in plan['external_modules']:
        rel=Path(*name.split('.')).with_suffix('.olean')
        obj=next((p/rel for p in paths if (p/rel).is_file()),None)
        if obj is None: raise RuntimeError('External object missing: '+name)
        external[name]=dict(path=str(obj),object_sha256=hashfile(obj))
    base={r['module']:r for r in prior['modules']}
    addition={r['module']:r for r in ii['results']}
    addition.update({r['module']:r for r in peer['results']})
    peer_names={r['module'] for r in peer['results']}
    report=ROOT/'resultados/lean_unificado'
    build=report/'build'
    cache=json.loads((report/'CACHE.json').read_text())
    completed={}
    adopted=[]
    for name in plan['compile_order']:
        if name=='SelectedExceptionalChain': continue
        node=plan['graph'][name]
        deps={n:(dict(fingerprint=completed[n]['fingerprint'],object_sha256=completed[n]['object_sha256'])
            if n in completed else external[n]) for n in node['imports']}
        fp=v.digest_json(dict(source_sha256=node['sha256'],dependencies=deps,compiler=compiler))
        if name in base:
            row=base[name]
            if row['fingerprint']!=fp or hashfile(build/(name+'.olean'))!=row['object_sha256']:
                raise RuntimeError('Base fingerprint mismatch: '+name)
            completed[name]=row
            continue
        old=addition[name]
        if old['exit_code']!=0 or old['source_sha256']!=node['sha256']:
            raise RuntimeError('Peer source not verified: '+name)
        obj=(PEER/'package_build/build' if name in peer_names else P/'cache/base')/(name+'.olean')
        log=(PEER/'package_build/logs' if name in peer_names else P/'provenance/import_logs')/(name+'.log')
        if hashfile(obj)!=old['object_sha256'] or hashfile(log)!=old['log_sha256']:
            raise RuntimeError('Object/log mismatch: '+name)
        if set(old['dependencies'])!=set(deps):
            raise RuntimeError('Import list mismatch: '+name)
        for n,d in deps.items():
            expected=old['dependencies'][n]
            if d['object_sha256']!=expected.get('sha256',expected.get('object_sha256')):
                raise RuntimeError('Dependency object mismatch: '+name+' -> '+n)
        output=log.read_text()
        axioms=v.axiom_reports(output)
        expected=old.get('axioms',old.get('axiom_queries'))
        if {k:sorted(x) for k,x in axioms.items()}!={k:sorted(x) for k,x in expected.items()}:
            raise RuntimeError('Axiom evidence mismatch: '+name)
        if len(axioms)<node['query_count']:
            raise RuntimeError('Axiom query missing: '+name)
        shutil.copy2(obj,build/(name+'.olean'))
        shutil.copy2(node['source'],build/(name+'.lean'))
        shutil.copy2(log,build/(name+'.log'))
        row=dict(module=name,source=node['path'],source_sha256=node['sha256'],dependencies=deps,
            fingerprint=fp,exit_code=0,object_sha256=old['object_sha256'],output=output,
            axioms=axioms,cache_adoption='INDEPENDENT_PASS_SOURCE_AND_DEPENDENCY_HASHES',
            original_command=old['command'],origin_receipt='PEER_COMPILATION' if name in peer_names else 'II_III_RECEIPT')
        completed[name]=row
        cache['modules'][name]=row
        adopted.append({k:row[k] for k in ['module','source_sha256','object_sha256','fingerprint','origin_receipt']})
        register(mf,'recibos/union/logs/'+name+'.log',log.read_bytes(),'ADOPTED_COMPILATION_LOG')
    (report/'CACHE.json').write_bytes(jsonbytes(cache))
    data=dict(status='PASS_INDEPENDENT_OBJECT_ADOPTION',base_modules_reused=len(base),
        adopted_modules=adopted,compiler=compiler,policy='Source, imports, every dependency object, proof log and original PASS checked; no new compilation claimed.')
    register(mf,'recibos/union/ADOPCION.json',jsonbytes(data),'VERIFIED_CACHE_ADOPTION_NOT_RECOMPILATION')
    (ROOT/'MANIFIESTO.json').write_bytes(jsonbytes(mf))
    print(json.dumps(dict(status=data['status'],adopted=len(adopted),base=len(base),plan_modules=len(plan['compile_order']))))

def seal():
    raw=(ROOT/'MANIFIESTO.json').read_bytes()
    mf=json.loads(raw)
    rpath=ROOT/'resultados/lean_unificado/VERIFICATION.json'
    run=json.loads(rpath.read_text())
    if mf[STAGE]['status']!='PREPARED_NOT_YET_JOINTLY_VERIFIED': raise RuntimeError('Already sealed')
    if run['status']!='PASS_PORTABLE_LEAN_SOURCE_CLOSURE' or run['manifest_sha256']!=sha(raw):
        raise RuntimeError('No PASS for current manifest')
    for row in mf['files']:
        if hashfile(ROOT/row['path'])!=row['sha256']: raise RuntimeError('Changed: '+row['path'])
    for row in json.loads((BASE/'MANIFIESTO.json').read_text())['files']:
        dest='versiones_previas/README_GENERACION_SELLADO.md' if row['path']=='README.md' else row['path']
        if hashfile(ROOT/dest)!=row['sha256']: raise RuntimeError('Lost previous bytes: '+dest)
    register(mf,'recibos/union/MANIFIESTO_COMPILADO.json',raw,'FROZEN_COMPILED_MANIFEST')
    register(mf,'recibos/union/LEAN_CONJUNTO.json',rpath.read_bytes(),'FROZEN_JOINT_COMPILATION')
    mf[STAGE].update(status='SEALED_VERIFIED_SOURCE_UNION',modules_in_closure=run['local_module_count'],
        compiled=run['compiled_modules'],reused=len(run['cached_modules']),previous_bytes_preserved=True)
    final=jsonbytes(mf)
    (ROOT/'MANIFIESTO.json').write_bytes(final)
    archive=ROOT.with_suffix('.zip')
    if archive.exists(): raise RuntimeError('ZIP already exists')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for path in sorted({r['path'] for r in mf['files']}|{'MANIFIESTO.json'}):
            z.write(ROOT/path,Path(ROOT.name)/path)
        if z.testzip(): raise RuntimeError('CRC failure')
        for row in mf['files']:
            if sha(z.read(str(Path(ROOT.name)/row['path'])))!=row['sha256']:
                raise RuntimeError('ZIP mismatch: '+row['path'])
    print(json.dumps(dict(status='PASS_EXCEPTIONAL_UNION_SEALED',modules=run['local_module_count'],
        compiled=run['compiled_modules'],reused=len(run['cached_modules']),
        zip=str(archive),zip_sha256=hashfile(archive),manifest_sha256=sha(final))))

if __name__=='__main__':
    if sys.argv[1:]==['--prepare']: prepare()
    elif sys.argv[1:]==['--adopt']: adopt()
    elif sys.argv[1:]==['--seal']: seal()
    else: raise SystemExit('Use --prepare, --adopt, or --seal')
