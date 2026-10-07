#!/usr/bin/env python3
"""Finite editorial preservation and local TPK checks; no global physics verdict."""
from pathlib import Path
from hashlib import sha256
from itertools import product, combinations
import json
import re

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.with_name('ARTICULO_REVISION_INTEGRADORA_20260908')
def digest(p): return sha256(p.read_bytes()).hexdigest()
rows=[]
for p in sorted([BASE/'main.tex', *(BASE/'sections').glob('*.tex'), *(BASE/'figures').rglob('*')]):
    if not p.is_file(): continue
    rel=p.relative_to(BASE)
    q=ROOT/rel
    assert q.is_file(), str(rel)
    old=p.read_bytes()
    new=q.read_bytes()
    if rel.as_posix()=='sections/nucleo.tex':
        expected=old.decode().replace(
            r'\subsection{TPK: selección, transporte y actualización de memoria}',
            r'\subsection{TPK: núcleo topológico de fase}')
        assert new.decode().startswith(expected), 'Original body changed'
        assert new.decode()[len(expected):].strip()==r'\input{sections/tpk_desarrollo_integrado.tex}'
        status='BODY_PRESERVED_HEADING_CHANGED_AND_INPUT_APPENDED'
    else:
        assert new==old, str(rel)
        status='BYTE_IDENTICAL'
    rows.append(dict(path=str(rel),old_sha256=digest(p),new_sha256=digest(q),status=status))

vectors=((0,1),(1,0),(0,-1),(-1,0))
def step(q):
    x,d,y,e,t=q
    phase=t%9
    if phase%3==0:
        x=tuple((a+b)%9 for a,b in zip(x,vectors[d]))
    elif phase%3==1:
        y=tuple((a+b)%9 for a,b in zip(y,vectors[e]))
    if (t+1)%27==0: d,e=(d+2)%4,(e+2)%4
    return x,d,y,e,(t+1)%108
def inverse(q):
    x,d,y,e,t=q
    t=(t-1)%108
    if (t+1)%27==0: d,e=(d+2)%4,(e+2)%4
    if t%3==0: x=tuple((a-b)%9 for a,b in zip(x,vectors[d]))
    elif t%3==1: y=tuple((a-b)%9 for a,b in zip(y,vectors[e]))
    return x,d,y,e,t

tested=0
for t,d,e in product(range(108),range(4),range(4)):
    q=((0,0),d,(0,0),e,t)
    assert inverse(step(q))==q
    r=q
    for i in range(108):
        r=step(r)
        if i==53: assert r[:4]==q[:4] and r[-1]==(t+54)%108
    assert r==q
    tested+=1
# Position-independent increments make this exhaustive modulo translations.
wind_cases=0
for x,d,a in product(product(range(1,10),repeat=2),range(4),range(2)):
    raw=tuple(x[i]+a*vectors[d][i] for i in range(2))
    out=tuple(1+(v-1)%9 for v in raw)
    b=tuple((raw[i]-out[i])//9 for i in range(2))
    assert all(out[i]+9*b[i]==raw[i] for i in range(2))
    wind_cases+=1
active={1,2,4,5,7,8}
pairs=list(combinations(sorted(active),2))
assert (len(active)*len(pairs),8*len(pairs),9*len(pairs))==(90,120,135)
assert (2*9*len(pairs),2*9*len(pairs)+1,3*len(pairs),21*len(pairs))==(270,271,45,315)
for shift in range(9):
    tr=lambda x:1+(x-1+shift)%9
    assert len({tr(x) for x in active})==6
    assert len({tuple(sorted((tr(a),tr(b)))) for a,b in pairs})==15

texts='\n'.join(p.read_text() for p in (ROOT/'sections').glob('*.tex'))
labels=re.findall(r'\\label\{([^}]+)\}',texts)
addition=(ROOT/'sections/tpk_desarrollo_integrado.tex').read_text()
refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',addition)
assert len(labels)==len(set(labels)), 'Duplicate labels'
assert not(set(refs)-set(labels)), sorted(set(refs)-set(labels))
record={
 'scope':'Exact source preservation and finite local operator checks; not a proof of all HMT claims',
 'status':'PASS_DELTA_TPK_EDITORIAL_Y_LOCAL',
 'sources':rows,'preserved_files':len(rows),
 'fobs_cases_modulo_position_translation':tested,
 'winding_cases':wind_cases,
 'phase_incidence_cardinals':[90,120,135,270,271,45,315],
 'new_cross_references_resolved':len(refs),
 'new_propositions':addition.count(r'\begin{proposition}'),
 'new_subsubsections':addition.count(r'\subsubsection{'),
 'source_sha256':digest(ROOT/'sections/tpk_desarrollo_integrado.tex')
}
(ROOT/'technical/DELTA_TPK_VERIFICADO.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
print('PASS_DELTA_TPK_EDITORIAL_Y_LOCAL '+json.dumps({k:v for k,v in record.items() if k!='sources'},ensure_ascii=False))
