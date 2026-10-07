#!/usr/bin/env python3
"""Finite checks and exact preservation of the 107-page predecessor.

This is documentary/local arithmetic QA, not certification of global claims.
"""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction
import json
import re

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.with_name('ARTICULO_REVISION_TPK_20260909')
INSERTIONS={
 'sections/revision_monodromia.tex':'sections/recta_nonadica_recuperada.tex',
 'sections/excepcional.tex':'sections/estrella_pentadica_recuperada.tex',
 'sections/electron.tex':'sections/centro_electronico_registros.tex',
}
def digest(p): return sha256(p.read_bytes()).hexdigest()
rows=[]
for p in sorted([BASE/'main.tex',*(BASE/'sections').glob('*.tex'),*(BASE/'figures').rglob('*')]):
    if not p.is_file(): continue
    rel=p.relative_to(BASE)
    q=ROOT/rel
    assert q.is_file(), str(rel)
    old=p.read_text() if p.suffix=='.tex' else p.read_bytes()
    new=q.read_text() if p.suffix=='.tex' else q.read_bytes()
    if rel.as_posix() in INSERTIONS:
        command=r'\input{'+INSERTIONS[rel.as_posix()]+'}'
        assert new.count(command)==1
        reduced=new.replace(command+'\n\n','',1)
        assert reduced==old, 'Unexpected source change: '+str(rel)
        status='EXACT_PREDECESSOR_PLUS_ONE_INPUT'
    else:
        assert old==new, 'Unexpected source change: '+str(rel)
        status='BYTE_IDENTICAL'
    rows.append({'path':str(rel),'before':digest(p),'after':digest(q),'status':status})

rho=lambda n:1+(n-1)%9
qr=lambda n:(rho(n),(n-rho(n))//9)
app=lambda i,j:(qr(i+j),qr(i*j))
fixed=[(i,j) for i in range(1,10) for j in range(1,10) if (i,j)==(10-i,10-j)]
assert fixed==[(5,5)]
assert app(5,5)==((1,1),(7,2))
solutions=[(5+t,5-t) for t in range(-4,5) if rho(25-t*t)==rho(25)]
assert solutions==[(2,8),(5,5),(8,2)]
assert app(2,8)==app(8,2)==((1,1),(7,1))

regions=[
 ('perp',(501,614,498,169,272,272),'555555',432),
 ('++1',(810,923,870,169,272,272),'339555',144),
 ('++2',(810,983,810,169,272,272),'393555',144),
 ('++3',(870,923,810,169,272,272),'933555',144),
 ('--',(870,923,810,418,674,521),'933717',144),
]
for name,u,sig,count in regions:
    psi=''.join(str((-n)%3) for n in u)
    actual=''.join(str(((n//10)%10-n//100)%10) for n in u)
    assert psi=='010211' and actual==sig, name
assert sum(x[3] for x in regions)==1008
assert [Fraction(x[3],1008) for x in regions]==[Fraction(3,7)]+[Fraction(1,7)]*4
assert (20//4,8//2)==(5,4)

surv=[('111201','201202','012100'),('212121','222210','101001'),('200121','212212','112000')]
for a,b,s in surv:
    assert ''.join(str((int(x)+int(y))%3) for x,y in zip(a,b))==s
tau=[1 if (9*k)//27%2==0 else -1 for k in range(12)]
assert tau==[1,1,1,-1,-1,-1]*2

alltex=list((ROOT/'sections').glob('*.tex'))+list((ROOT/'figures').glob('*.tex'))
text='\n'.join(p.read_text() for p in alltex)
assert not re.search(r'TPK\s*(?:\([^)]*)?actualizad',text,re.I)
labels=re.findall(r'\\label\{([^}]+)\}',text)
assert len(labels)==len(set(labels)), 'Duplicate labels'
for name in INSERTIONS.values():
    refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',(ROOT/name).read_text())
    assert not(set(refs)-set(labels)), (name,sorted(set(refs)-set(labels)))
record={'status':'PASS_DELTA_FIGURAS_CENTRO','scope':'Editorial preservation and exact finite arithmetic only',
 'predecessor_files':len(rows),'preservation':rows,'central_fixed_points':fixed,
 'central_vacancies':solutions,'regional_signatures_verified':5,'regional_mass':1008,
 'regional_ternary_image':'010211','tau_e':tau,
 'TPK_actualizado_in_body':False}
(ROOT/'technical/DELTA_FIGURAS_CENTRO.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print('PASS_DELTA_FIGURAS_CENTRO files='+str(len(rows)))
