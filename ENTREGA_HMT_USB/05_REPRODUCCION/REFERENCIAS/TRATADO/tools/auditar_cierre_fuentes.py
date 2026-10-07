#!/usr/bin/env python3
"""Audita el cierre material leído por TeX y la preservación del antecedente."""
from pathlib import Path
import hashlib
import argparse
import json
import re

ROOT=Path(__file__).resolve().parents[1]
MAN=ROOT/'source/integral/fuente/manuscrito'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--fls',type=Path,default=ROOT/'build/main.fls')
    args=parser.parse_args()
    paths=set()
    for line in args.fls.read_text().splitlines():
        if not line.startswith('INPUT '): continue
        path=Path(line[6:])
        if not path.is_absolute(): path=MAN/path
        if path.is_file(): paths.add(path.resolve())
    sources=[];external=[]
    for path in sorted(paths):
        if str(path).startswith(('/usr/local/texlive/','/Library/TeX/')): continue
        if path.suffix in {'.aux','.toc','.out','.idx','.ind','.ilg','.log','.fls'}: continue
        row={'path':str(path),'sha256':sha(path),'bytes':path.stat().st_size}
        if path.suffix in {'.tex','.bbl'}:
            text=path.read_text(errors='replace')
            visible='\n'.join(re.split(r'(?<!\\)%',line,maxsplit=1)[0] for line in text.splitlines())
            row['proof_environments']=len(re.findall(r'\\begin\{proof\}',visible))
            row['statement_environments']=len(re.findall(r'\\begin\{(?:theorem|lemma|proposition|corollary|teorema|lema|proposicion|corolario)\}',visible))
        sources.append(row)
        if ROOT not in path.parents: external.append(row)
    preserved=json.loads((ROOT/'metadata/PRESERVACION_BASE_INTEGRAL.json').read_text())
    changed=[];missing=[];unchanged=0
    for row in preserved['files']:
        path=ROOT/row['destination']
        if not path.is_file(): missing.append(row)
        elif sha(path)==row['sha256']: unchanged+=1
        else: changed.append({'path':str(path),'original':row['sha256'],'current':sha(path)})
    report={'scope':'Cierre de compilación e integridad material. Independiente de completitud demostrativa y corrección matemática.',
            'fls':str(args.fls.resolve()),'fls_sha256':sha(args.fls),
            'files_read':sources,'external_non_texlive':external,
            'antecedent':{'unchanged':unchanged,'changed':changed,'missing':missing},
            'status':'PASS_LOCAL_MATERIAL_CLOSURE' if not external and not missing else 'REVIEW_MATERIAL_CLOSURE'}
    (ROOT/'metadata/CIERRE_MATERIAL_FLS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'read':len(sources),'external':len(external),'unchanged':unchanged,'changed':len(changed),'missing':len(missing)},ensure_ascii=False))
    for row in external: print('EXTERNAL',row['path'])

if __name__=='__main__': main()
