#!/usr/bin/env python3
"""Controles portables REV02, normales y optimizados; no compila ni sella.

El control de originales se desactiva mediante un directorio temporal vacío:
se prueban las copias y programas locales, no la disponibilidad del ordenador
de origen. --require-manifest añade la identidad de una entrega ya sellada.
Los recibos anteriores permanecen intactos. La biblioteca estándar es suficiente.
"""
import argparse
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt',type=Path)
    parser.add_argument('--require-manifest',action='store_true')
    parser.add_argument('--preflight',type=Path)
    args=parser.parse_args()
    result={'schema':'HMT_IV_REV02_PORTABLE_CONTROLS_V1',
        'status':'RUNNING','python':sys.version,'executions':[],
        'scope':'Reproducción local finita, integridad y referencias; no certificación matemática global ni revisión visual.',
        'compiled':False,'source_documents_modified':False}
    if args.require_manifest:
        result['manifest']=runpy.run_path(str(ROOT/'reproducir.py'),run_name='iv_manifest')['verify_manifest']()
    with tempfile.TemporaryDirectory(prefix='hmt_iv_rev02_checks_') as temporary:
        directory=Path(temporary)
        empty=directory/'sin_originales';empty.mkdir()
        tasks=[
            ('focal','technical/verificar_focal.py',['--source-root',str(empty)],'PASS_CONTROLES_FOCALES_IV'),
            ('radio','technical/verificar_radio_elipse.py',[],'PASS_RADIO_ELIPSE_IV_REV02'),
            ('antecedentes_II','technical/antecedente_II_REV10/verificar_antecedentes.py',[],None),
            ('driver','technical/compilar_iv.py',['--check-only']+(['--preflight',str(args.preflight.resolve())] if args.preflight else []),'SOURCE_GRAPH_CHECK_ONLY')]
        for name,relative,arguments,expected in tasks:
            program=ROOT/relative
            results=[]
            for optimized in (False,True):
                command=[sys.executable]+(['-O'] if optimized else [])+['-I','-S','-B',str(program)]+arguments
                process=subprocess.run(command,cwd=directory,capture_output=True,text=True,check=False)
                require(process.returncode==0, name+': '+process.stdout+process.stderr)
                require(not process.stderr.strip(),name+': stderr inesperado: '+process.stderr)
                if name=='antecedentes_II':
                    require(process.stdout.startswith('PASS_CONSERVACION_FOCAL_II_REV10 files=7 binary_hashes=7 '),
                            'Cotejo local de II incompleto')
                    payload={'status':'PASS_CONSERVACION_FOCAL_II_REV10','stdout':process.stdout}
                else:
                    payload=json.loads(process.stdout)
                if expected:
                    require(payload.get('status')==expected,name+': estado incorrecto')
                else:
                    require(str(payload.get('status','')).startswith('PASS'),name+': sin PASS focal')
                if name=='focal':
                    require(payload['source_originals_compared']==0,'Se consultó un original externo')
                    require(payload['source_copies_verified']==6,'Copias focales incompletas')
                results.append(payload)
                result['executions'].append({'name':name,'optimized':optimized,'command':command,
                    'program':relative,'program_sha256':sha(program),'returncode':0,
                    'stdout_sha256':hashlib.sha256(process.stdout.encode()).hexdigest(),'result':payload})
            require(results[0]==results[1],name+': normal y -O difieren')
    result['status']='PASS_CONTROLES_PORTABLES_IV_REV02'
    result['normal_optimized_equal']=True
    result['sources_available_outside_package_required']=False
    if args.receipt:
        args.receipt.parent.mkdir(parents=True,exist_ok=True)
        args.receipt.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'executions':len(result['executions']),
        'receipt':str(args.receipt) if args.receipt else None,'scope':result['scope']},ensure_ascii=False))

if __name__=='__main__':
    try:
        main()
    except (RuntimeError,ValueError,KeyError,OSError) as error:
        print(str(error),file=sys.stderr)
        raise SystemExit(1)
