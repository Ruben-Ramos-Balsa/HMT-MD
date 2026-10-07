#!/usr/bin/env python3
"""Control focal de los pasos TRIT REV03; no genera constantes objetivo."""
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(__file__).resolve().parent / '../../../../../../COMUN/CERTIFICADOS_K/lectura_conjunta/fuentes/articulo_x/sections/trit_desarrollo.tex'
TRITS = (-1, 0, 1)

def balanced(n):
    c = (n + 1) // 3
    return (n - 3*c, c)

def lift(p):
    r, c = p
    return r + 3*c

def chi(r, s):
    return balanced(r+s)[1]

def add(p, q):
    r, c = p
    s, d = q
    return (balanced(r+s)[0], c+d+chi(r,s))

def mul(p, q):
    r, c = p
    s, d = q
    return (r*s, r*d+s*c+3*c*d)

def qmul(tau, z, w):
    a,b = z
    c,d = w
    return (a*c-tau*b*d, a*d+b*c)

def norm(tau, z):
    a,b = z
    return a*a+tau*b*b

def matrix(tau,z):
    a,b=z
    return ((a,-tau*b),(b,a))

def matmul(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))

def main():
    residual_pairs=[]
    for r,s in itertools.product(TRITS, repeat=2):
        u,c=balanced(r+s)
        assert u+3*c==r+s
        residual_pairs.append({'r':r,'s':s,'sum':r+s,'residue':u,'carry':c})
    triples=[]
    for r,s,t in itertools.product(TRITS, repeat=3):
        left=(chi(r,s),chi(balanced(r+s)[0],t))
        right=(chi(s,t),chi(r,balanced(s+t)[0]))
        assert sum(left)==sum(right)
        triples.append({'triple':[r,s,t],'left_ordered_carries':left,'right_ordered_carries':right,'total':sum(left)})
    beta=[]
    for n in range(9):
        r,c=balanced(n)
        beta.append({'class_mod9':n,'r':r,'c_mod3':c%3})
    assert len({(x['r'],x['c_mod3']) for x in beta})==9
    operations=[]
    for n,m in itertools.product(range(9),repeat=2):
        p=balanced(n);q=balanced(m)
        a=add(p,q);b=mul(p,q)
        assert lift(a)%9==(n+m)%9
        assert lift(b)%9==(n*m)%9
        operations.append({'inputs':[n,m],'sum_pair':[a[0],a[1]%3],'product_pair':[b[0],b[1]%3]})
    trace_examples={}
    for n in range(-100,101):
        r,c=balanced(n)
        assert r in TRITS and lift((r,c))==n
        assert balanced(-n)==(-r,-c)
        current=n; digits=[];trace=[]
        for k in range(1,10):
            rr,current=balanced(current);digits.append(rr)
            reconstruction=sum(x*3**i for i,x in enumerate(digits))+3**k*current
            assert reconstruction==n
            trace.append({'depth':k,'digits_low_to_high':digits.copy(),'terminal_quotient':current,'reconstruction':reconstruction})
        if n in (-8,-3,-2,0,2,4,8,81):
            trace_examples[str(n)]=trace
    for n,m in itertools.product(range(-100,101),repeat=2):
        assert add(balanced(n),balanced(m))==balanced(n+m)
        assert mul(balanced(n),balanced(m))==balanced(n*m)
    quadratic=0
    for tau,a,b,c,d in itertools.product(TRITS,range(-2,3),range(-2,3),range(-2,3),range(-2,3)):
        z=(a,b);w=(c,d);zw=qmul(tau,z,w)
        assert norm(tau,zw)==norm(tau,z)*norm(tau,w)
        assert matrix(tau,zw)==matmul(matrix(tau,z),matrix(tau,w))
        quadratic+=1
    assert qmul(1,(1,1),(1,1))==(0,2)
    assert qmul(-1,(1,1),(1,-1))==(0,0)
    result={
        'result':'PASS_TRIT_REV03_FOCAL',
        'scope':'FINITE_TABLES_AND_DECLARED_INTEGER_SAMPLE_NOT_GLOBAL_CORPUS_CERTIFICATION',
        'source':str(SOURCE),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'residual_pairs':residual_pairs,'cocycle_triples':triples,'mod9_inverse_table':beta,
        'mod9_operations':operations,'integer_sample':{'min':-100,'max':100,'ordered_pairs':201**2,'depths':9},
        'integer_trace_examples':trace_examples,'quadratic_cases':quadratic,
        'target_constant_inputs':[], 'lean_proof_claimed':False,
    }
    path=ROOT/'REV03_PASOS_Y_CONTRATOS/20_TRIT_COMPROBACION.json'
    raw=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if path.exists():
        assert path.read_text()==raw, 'El recibo previo difiere: conservar y crear revisión sucesora.'
    else:
        path.write_text(raw)
    print(json.dumps({k:result[k] for k in ('result','integer_sample','quadratic_cases','target_constant_inputs')},ensure_ascii=False))

if __name__=='__main__':
    main()
