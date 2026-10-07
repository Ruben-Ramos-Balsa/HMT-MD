#!/usr/bin/env python3
"""Ensayo aislado del reproductor; manifiesto de prueba, no sello de entrega."""
import argparse
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(condition,message):
    if not condition: raise RuntimeError(message)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt',type=Path)
    args=parser.parse_args()
    inventory=runpy.run_path(str(ROOT/'technical/empaquetar_iv.py'),run_name='iv_test_inventory')['inventory']()
    before={str(p.relative_to(ROOT)):sha(p) for p in inventory}
    results=[]
    with tempfile.TemporaryDirectory(prefix='hmt_iv_rev02_reproduction_') as temporary:
        isolated=Path(temporary)/ROOT.name
        for rel,expected in before.items():
            target=isolated/rel;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT/rel,target)
            require(sha(target)==expected,'Diferencia de copia: '+rel)
        test_manifest={'schema':'TEST_FIXTURE_NOT_DELIVERY',
            'files':[{'path':rel,'sha256':h} for rel,h in before.items()]}
        (isolated/'MANIFIESTO_ENTREGA.json').write_text(json.dumps(test_manifest,indent=2)+'\n',encoding='utf-8')
        bad=Path(temporary)/'bad_preflight.json';bad.write_text('{}\n',encoding='utf-8')
        for optimized in (False,True):
            base=[sys.executable]+(['-O'] if optimized else [])+['-I','-S','-B']
            commands=[(base+[str(isolated/'reproducir.py')],0,'reproduccion_completa'),
                (base+[str(isolated/'technical/compilar_iv.py'),'--check-only','--preflight',str(bad)],1,'rechazo_preflight'),
                (base+[str(isolated/'technical/empaquetar_iv.py'),'--seal'],1,'rechazo_sellado_sin_qa')]
            for command,expected,name in commands:
                call=subprocess.run(command,cwd=isolated,capture_output=True,text=True,check=False)
                require(call.returncode==expected,name+': '+call.stdout+call.stderr)
                if name=='reproduccion_completa':
                    require(json.loads(call.stdout)['status']=='PASS_REPRODUCCION_FOCAL_IV','Reproductor no satisfactorio')
                if name=='rechazo_preflight':
                    state=json.loads(call.stdout)
                    require(not state['compilation_authorized'] and not state['files_written'] and not state['tex_invoked'], 'Rechazo ineficaz')
                results.append({'name':name,'optimized':optimized,'command':command,'returncode':call.returncode,
                    'stdout':call.stdout if name!='rechazo_preflight' else 'SOURCE_GRAPH_CHECK_ONLY; preflight inválido rechazado; no escritura ni TeX',
                    'stderr':call.stderr})
        for rel,h in before.items():
            require(sha(isolated/rel)==h,'La reproducción modificó un miembro inventariado: '+rel)
        require(json.loads((isolated/'MANIFIESTO_ENTREGA.json').read_text())==test_manifest,'Se sobrescribió el manifiesto de ensayo')
        require(not list(Path(temporary).glob('*.zip')),'Se creó un ZIP sin QA')
    for rel,h in before.items(): require(sha(ROOT/rel)==h,'Se modificó el paquete de trabajo: '+rel)
    result={'status':'PASS_ENSAYO_AISLADO_REPRODUCTOR_IV_REV02','executions':results,
        'inventoried_members':len(before),'source_and_package_members_unchanged':True,
        'test_manifest_was_delivery_seal':False,'tex_invoked':False,'zip_created':False,
        'scope':'Movilidad de los programas, controles locales y rechazos efectivos normal/-O. No recompilación ni auditoría matemática global.'}
    if args.receipt:
        args.receipt.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'cases':len(results),'members':len(before)},ensure_ascii=False))

if __name__=='__main__': main()
