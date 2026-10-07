#!/usr/bin/env python3
"""Append the checked product step without changing sealed predecessors."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'PAQUETE_ARTICULO_I_CADENA_EXCEPCIONAL_20260919'
ROOT=HERE.parent/'PAQUETE_ARTICULO_I_PRODUCTOS_RETICULARES_20260919'
KEY='vacuum_products_successor'

def sha(b): return hashlib.sha256(b).hexdigest()
def jb(v): return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def add(mf,name,b,role):
    if any(r['path']==name for r in mf['files']): raise RuntimeError('Existing path '+name)
    p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    mf['files'].append(dict(path=name,sha256=sha(b),bytes=len(b),role=role,source='VACUUM_PRODUCTS_CONTINUATION'))

def prepare():
    if ROOT.exists(): raise RuntimeError('Successor exists')
    raw=(BASE/'MANIFIESTO.json').read_bytes();mf=json.loads(raw)
    for row in mf['files']:
        if sha((BASE/row['path']).read_bytes())!=row['sha256']: raise RuntimeError('Changed base')
    r=json.loads((HERE/'VACUUM_CONTRACTION_VERIFICATION.json').read_text())
    if r['status']!='PASS_VACUUM_CONTRACTION' or sha((HERE/'LatticeVacuumContraction.lean').read_bytes())!=r['source_sha256']:
        raise RuntimeError('Unverified coefficient step')
    shutil.copytree(BASE,ROOT)
    add(mf,'versiones_previas/MANIFIESTO_UNION_SELLADO.json',raw,'EXACT_PREDECESSOR_MANIFEST')
    old=(ROOT/'README.md').read_bytes()
    add(mf,'versiones_previas/README_UNION_SELLADO.md',old,'EXACT_PREDECESSOR_ENTRY')
    new=('''# Continuación comprobada: productos reticulares

Entrada actual: `deltas/productos/SelectedFieldProducts.lean`.
Ejecutor: `python3 -I -S reproducir_productos.py --mathlib /ruta/a/mathlib4 --lean /ruta/a/lean`.

Se añade la evaluación exacta de los coeficientes de creación/aniquilación
sobre el vacío para todo par de grados naturales. Las cotas de anulación
proceden del grado y del emparejamiento integral, no de una lista de casos.
La entrada importa íntegramente la cadena anterior y conserva sus teoremas.
No se afirma todavía localidad completa en las dos regiones, orbifold ni FLM.

''').encode()+old
    (ROOT/'README.md').write_bytes(new)
    for row in mf['files']:
        if row['path']=='README.md': row.update(sha256=sha(new),bytes=len(new))
    modules=['LatticeVacuumContraction','SelectedFieldProducts'];queries=[]
    for name in modules:
        b=(HERE/(name+'.lean')).read_bytes()
        add(mf,'deltas/productos/'+name+'.lean',b,'PROVED_OPERATOR_SOURCE')
        queries+=re.findall(r'(?m)^#print axioms ([A-Za-z0-9_.]+)\s*$',b.decode())
    for src,dest,role in [('VACUUM_CONTRACTION_VERIFICATION.json','recibos/productos/INDIVIDUAL.json','INDIVIDUAL_COMPILATION'),
            ('reproducir_productos_portable.py','reproducir_productos.py','PORTABLE_RUNNER'),
            ('comprobar_datos_incidencia.py','comprobar_datos_incidencia.py','PORTABLE_DATA_CHECK'),
            ('preparar_productos.py','procedencia/productos/preparar_productos.py','ASSEMBLY_PROVENANCE')]:
        add(mf,dest,(HERE/src).read_bytes(),role)
    c=json.loads((ROOT/'recibos/union/RECIBO_CAUSAL.json').read_text())
    c.update(artifact=str(ROOT/'README.md'),artifact_sha256=sha(new),result_id='SELECTED_VACUUM_PRODUCTS_20260919',
        scope='All-degree vacuum contraction on the conserved selected carrier; no full FLM assertion.')
    c['genealogy']['source_locators'].append(str(ROOT/'deltas/productos/SelectedFieldProducts.lean'))
    add(mf,'recibos/productos/RECIBO_CAUSAL.json',jb(c),'CAUSAL_METADATA_NOT_MATHEMATICAL_PROOF')
    p=subprocess.run([sys.executable,'-I','-S','/Users/ruben/.codex/skills/enforce-hmt-generated-constants/scripts/verify_generated_constants.py',
        '--audit',str(ROOT/'README.md'),'--receipt',str(ROOT/'recibos/productos/RECIBO_CAUSAL.json')],capture_output=True,text=True)
    if p.returncode or 'PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY' not in p.stdout: raise RuntimeError(p.stdout+p.stderr)
    add(mf,'recibos/productos/CONTROL_CAUSAL.txt',(p.stdout+p.stderr).encode(),'CAUSAL_METADATA_CHECK')
    mf[KEY]=dict(status='PREPARED_NOT_COMPILED',modules=modules,axiom_queries=queries,
        predecessor_manifest_sha256=sha(raw),complete_flm_formalization_claimed=False)
    (ROOT/'MANIFIESTO.json').write_bytes(jb(mf))
    print('PRODUCT_STEP_PREPARED')

def seal():
    raw=(ROOT/'MANIFIESTO.json').read_bytes();mf=json.loads(raw)
    rpath=ROOT/'resultados/lean_unificado/VERIFICATION.json';run=json.loads(rpath.read_text())
    if mf[KEY]['status']!='PREPARED_NOT_COMPILED': raise RuntimeError('Not prepared')
    if run['status']!='PASS_PORTABLE_LEAN_SOURCE_CLOSURE' or run['manifest_sha256']!=sha(raw): raise RuntimeError('No current PASS')
    dpath=ROOT/'resultados/datos_incidencia/VERIFICATION.json'
    data=json.loads(dpath.read_text())
    if data['status']!='PASS_PACKAGE_INCIDENCE_DATA': raise RuntimeError('Data check not passed')
    for row in mf['files']:
        if sha((ROOT/row['path']).read_bytes())!=row['sha256']: raise RuntimeError('Source changed')
    for row in json.loads((BASE/'MANIFIESTO.json').read_text())['files']:
        dest='versiones_previas/README_UNION_SELLADO.md' if row['path']=='README.md' else row['path']
        if sha((ROOT/dest).read_bytes())!=row['sha256']: raise RuntimeError('Predecessor not conserved')
    add(mf,'recibos/productos/MANIFIESTO_COMPILADO.json',raw,'FROZEN_MANIFEST')
    add(mf,'recibos/productos/LEAN_CONJUNTO.json',rpath.read_bytes(),'FROZEN_COMPILE_RECEIPT')
    add(mf,'recibos/productos/DATOS_INCIDENCIA.json',dpath.read_bytes(),'FROZEN_DATA_CHECK')
    add(mf,'procedencia/productos/sellado.py',Path(__file__).read_bytes(),'FINAL_SEAL_PROVENANCE')
    mf[KEY].update(status='SEALED_VERIFIED_PRODUCT_CONTINUATION',modules_in_closure=run['local_module_count'],
        compiled=run['compiled_modules'],reused=len(run['cached_modules']),previous_bytes_preserved=True)
    final=jb(mf);(ROOT/'MANIFIESTO.json').write_bytes(final)
    archive=ROOT.with_suffix('.zip')
    if archive.exists(): raise RuntimeError('ZIP exists')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for path in sorted({r['path'] for r in mf['files']}|{'MANIFIESTO.json'}):
            z.write(ROOT/path,Path(ROOT.name)/path)
        if z.testzip(): raise RuntimeError('CRC failure')
        for row in mf['files']:
            if sha(z.read(str(Path(ROOT.name)/row['path'])))!=row['sha256']: raise RuntimeError('ZIP mismatch')
    print(json.dumps(dict(status='PASS_PRODUCT_CONTINUATION_SEALED',modules=run['local_module_count'],
        compiled=run['compiled_modules'],reused=len(run['cached_modules']),zip=str(archive),
        zip_sha256=sha(archive.read_bytes()),manifest_sha256=sha(final))))

if __name__=='__main__':
    if sys.argv[1:]==['--prepare']: prepare()
    elif sys.argv[1:]==['--seal']: seal()
    else: raise SystemExit('Use --prepare or --seal')
