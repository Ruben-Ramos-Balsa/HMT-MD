#!/usr/bin/env python3
"""Preservation and exact cyclic-projector checks; no global scientific verdict."""
from pathlib import Path
from fractions import Fraction as F
import argparse, hashlib, json, sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OLD = ROOT.with_name('ARTICULO_III_VACIO_ELECTROMAGNETICO_20260910_REV03')
REGISTRY = HERE/'FUENTES_REV03.json'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(condition, message):
    if not condition: raise RuntimeError(message)
def write(path, value): path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def mm(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def power(a,n):
    z=[[F(i==j) for j in range(12)] for i in range(12)]
    for _ in range(n): z=mm(z,a)
    return z
def average(a,powers):
    matrices=[power(a,n) for n in powers]
    return [[sum(m[i][j] for m in matrices)/len(matrices) for j in range(12)] for i in range(12)]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--snapshot',action='store_true');ap.add_argument('--receipt',type=Path)
    args=ap.parse_args()
    if args.snapshot:
        require(not REGISTRY.exists(),'Snapshot immutable already exists')
        files=[OLD/'main.tex']
        for d in ('manuscrito','base_articulo_I','base_articulo_II'):
            files.extend(p for p in (OLD/d).rglob('*') if p.is_file() and p.suffix in ('.tex','.bib','.png','.jpg','.pdf'))
        write(REGISTRY,{'predecessor':str(OLD),'files':[{'path':str(p.relative_to(OLD)),'sha256':sha(p)} for p in sorted(set(files))]})
    record=json.loads(REGISTRY.read_text())
    changed={'main.tex':'main_rev03.tex','manuscrito/sections/05_ciclo_catalan.tex':'05_ciclo_catalan_rev03.tex'}
    rows=[]
    for r in record['files']:
        rel=r['path']; target=ROOT/rel
        require(target.is_file(),'Missing predecessor source '+rel)
        if rel in changed:
            witness=HERE/'origenes'/changed[rel]
            require(sha(witness)==r['sha256'],'Altered predecessor witness '+rel)
            old=witness.read_text();new=target.read_text()
            if rel=='main.tex':
                marker='\\input{manuscrito/sections/04c_velocidad_y_reloj.tex}\n'
                require(new.count(marker)==1,'One insertion required')
                require(new.replace(marker,'')==old,'Unexpected main change')
            else:
                note=('El superíndice $\\mathrm{cyc}$ identifica el promedio del ciclo dodecafásico:\n'
                    '$P_3^{\\mathrm{cyc}}$ es el proyector sobre las secuencias de período divisor\n'
                    'de $3$. Su dominio y su acción son distintos de los del proyector isótipo\n'
                    'tridimensional de la realización icosaédrica; la coincidencia de rango\n'
                    'no identifica ambos operadores.\n')
                require(new.count(note)==1,'One notational explanation required')
                restored=new.replace(note,'').replace('^{\\mathrm{cyc}}','')
                restored=restored.replace('\\qquad\n H_d=','\\qquad H_d=')
                require(restored==old,'Unexpected scientific change to cyclic projector section')
            state='exact_authorized_delta'
        else:
            require(sha(target)==r['sha256'],'Unexpected change '+rel);state='byte_identical'
        rows.append({'path':rel,'status':state,'sha256_current':sha(target)})
    c=[[F(i==(j+1)%12) for j in range(12)] for i in range(12)]
    p3=average(c,[0,3,6,9]);p4=average(c,[0,4,8]);ident=power(c,0)
    checks=0
    for d,p in [(3,p3),(4,p4)]:
        for condition,name in [(mm(p,p)==p,'idempotence'),(p==list(map(list,zip(*p))),'self-adjoint'),(sum(p[i][i] for i in range(12))==d,'rank by trace'),(mm(c,p)==mm(p,c),'cycle commutation'),(mm(power(c,d),p)==p,'period divides d')]:
            require(condition,f'P{d} {name}');checks+=1
    require(sum(p3[i][i]-p4[i][i] for i in range(12))/12==F(-1,12),'trace defect');checks+=1
    c6=power(c,6);pant=[[(ident[i][j]-c6[i][j])/2 for j in range(12)] for i in range(12)]
    q=mm(p4,pant)
    for condition,name in [(mm(q,q)==q,'Q projector'),(sum(q[i][i] for i in range(12))==2,'Q rank'),(mm(power(c,2),q)==[[-x for x in row] for row in q],'quarter turn')]:
        require(condition,name);checks+=1
    current=[]
    for d in ('manuscrito','base_articulo_I','base_articulo_II'):
        current.extend(p for p in (ROOT/d).rglob('*') if p.is_file() and p.suffix in ('.tex','.bib','.png','.jpg','.pdf'))
    current.append(ROOT/'main.tex')
    result={'status':'PASS_REV04_FOCAL_PRESERVATION_AND_CYCLIC_PROJECTORS',
      'predecessor_sources':len(rows),'unchanged':sum(r['status']=='byte_identical' for r in rows),
      'authorized_changed_sources':2,'exact_matrix_checks':checks,'checks_survive_optimization':True,
      'source_files':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in sorted(set(current))],
      'preservation':rows,'scope':'Local documentary preservation and rational matrix identities. No global autonomy or physical identification claim.'}
    if args.receipt: write(args.receipt,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('preservation','source_files')},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
