#!/usr/bin/env python3
"""Incremental work on one locality block; no intermediate delivery ZIP."""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'PAQUETE_ARTICULO_I_PRODUCTOS_RETICULARES_20260919'
BUILD=HERE/'locality_block_build'
REVIEWER=Path('/Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_PRODUCTO_CAMPOS_20260919')
EXTERNAL=['LatticeWeightFiltration','LatticeFieldCutoff','LatticeOperatorCutoff',
          'LatticeFieldProductCutoff','LatticeAntidiagonalRectangle','LatticeFieldProductRectangle',
          'LatticeFieldProductLinearity']

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    r=json.loads((BASE/'recibos/productos/LEAN_CONJUNTO.json').read_text())
    if r['status']!='PASS_PORTABLE_LEAN_SOURCE_CLOSURE':raise RuntimeError('No checked base')
    spec=importlib.util.spec_from_file_location('v',BASE/'verificar_lean.py')
    v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    BUILD.mkdir(exist_ok=True)
    receipt=BUILD/'VERIFICATION.json'
    result=dict(status='RUNNING',base_receipt_sha256=sha(BASE/'recibos/productos/LEAN_CONJUNTO.json'),modules=[])
    receipt.write_text(json.dumps(result,indent=2)+'\n')
    env=dict(os.environ,LEAN_PATH=str(BUILD)+os.pathsep+str(REVIEWER)+os.pathsep+r['lean_path'])
    cachepath=BUILD/'CACHE.json'
    cache=json.loads(cachepath.read_text()) if cachepath.exists() else {}
    try:
        result['reviewer_modules']=[]
        for name in EXTERNAL:
            rp=REVIEWER/(name+'.receipt.json')
            er=json.loads(rp.read_text())
            src=REVIEWER/(name+'.lean');obj=REVIEWER/(name+'.olean')
            if er['status']!='PASS_FOCUSED_FIELD_MODULE' or sha(src)!=er['source_sha256'] or sha(obj)!=er['object_sha256']:
                raise RuntimeError('Unverified reviewer module '+name)
            result['reviewer_modules'].append(dict(module=name,receipt_sha256=sha(rp),
                source_sha256=sha(src),object_sha256=sha(obj)))
        for row in r['modules']:
            if sha(BASE/row['source'])!=row['source_sha256'] or sha(BASE/'resultados/lean_unificado/build'/(row['module']+'.olean'))!=row['object_sha256']:
                raise RuntimeError('Changed base '+row['module'])
        for name in ['LatticeContractionPascal','LatticeTwoRegionFactor','LatticeFactorConvolution','LatticeNormalProduct','LatticeProductCocycle','LatticeConvolutionFinite','LatticeConvolutionSwap','LatticeNormalCoefficients','LatticeNormalSymmetry','LatticeDressedSymmetry','LatticeFieldNormalBridge','LatticeChargedLocality','LatticeFieldBiOperators','LatticeChargedLocalityFull','SelectedFieldLocality']:
            src=HERE/(name+'.lean');imports,queries=v.inspect_source(src.read_bytes(),str(src))
            source_digest=sha(src)
            obj=BUILD/(name+'.olean')
            dependencies={}
            for imp in imports:
                relative=Path(*imp.split('.')).with_suffix('.olean')
                origin=next((Path(d)/relative for d in env['LEAN_PATH'].split(os.pathsep) if (Path(d)/relative).is_file()),None)
                if origin is None:raise RuntimeError('Dependency object absent: '+imp)
                dependencies[imp]=sha(origin)
            fingerprint=hashlib.sha256(json.dumps(dict(source=sha(src),dependencies=dependencies,
                compiler=r['compiler']),sort_keys=True).encode()).hexdigest()
            command=[r['compiler']['executable'],'-DwarningAsError=true','--root='+str(HERE),'-o',str(obj),str(src)]
            old=cache.get(name,{})
            hit=old.get('fingerprint')==fingerprint and obj.is_file() and old.get('object_sha256')==sha(obj)
            if hit:
                exit_code=0;output=old['output']
                print(name+': verified cache hit',flush=True)
            else:
                p=subprocess.run(command,cwd=r['mathlib'],env=env,text=True,capture_output=True,timeout=180)
                exit_code=p.returncode;output=p.stdout+p.stderr
                (BUILD/(name+'.log')).write_text(output)
            print(output,flush=True)
            report=v.axiom_reports(output)
            if exit_code or len(report)<queries:raise RuntimeError('Proof failed '+name)
            if sha(src)!=source_digest:raise RuntimeError('Source changed during proof '+name)
            for imp,digest in dependencies.items():
                relative=Path(*imp.split('.')).with_suffix('.olean')
                origin=next(Path(d)/relative for d in env['LEAN_PATH'].split(os.pathsep) if (Path(d)/relative).is_file())
                if sha(origin)!=digest:raise RuntimeError('Dependency changed during proof '+imp)
            result['modules'].append(dict(module=name,source_sha256=sha(src),object_sha256=sha(obj),
                declarations=report,command=command,exit_code=exit_code,output=output,cache_hit=hit,
                fingerprint=fingerprint,dependencies=dependencies))
            cache[name]=result['modules'][-1]
            cachepath.write_text(json.dumps(cache,indent=2)+'\n')
        result['status']='PASS_LOCALITY_BLOCK_CURRENT_MODULES';code=0
    except Exception as e:
        result.update(status='FAIL',error=str(e));code=1
    receipt.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],flush=True)
    return code

if __name__=='__main__':raise SystemExit(main())
