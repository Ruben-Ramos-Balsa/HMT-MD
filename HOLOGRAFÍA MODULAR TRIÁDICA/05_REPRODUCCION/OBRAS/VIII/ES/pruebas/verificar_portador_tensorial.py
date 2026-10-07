#!/usr/bin/env python3
"""Control exacto Q(sqrt(5)) del portador de VII; biblioteca estándar.
Comprueba realización, momentos, rango y TT. No certifica dinámica física.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

def q(a=0,b=0): return (F(a),F(b))
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def neg(a): return (-a[0],-a[1])
def mul(a,b): return (a[0]*b[0]+5*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def sc(n,a): return mul(q(n),a)
def sm(items):
    out=q()
    for a in items: out=add(out,a)
    return out
def mm(a,b):
    return [[sm(mul(a[i][k],b[k][j]) for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]
def tp(a): return list(map(list,zip(*a)))
def trace(a): return sm(a[i][i] for i in range(len(a)))
def sub(a,b): return [[add(x,neg(y)) for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(n,a): return [[sc(n,x) for x in r] for r in a]
def eye(n): return [[q(int(i==j)) for j in range(n)] for i in range(n)]
def dot(a,b): return sm(mul(x,y) for x,y in zip(a,b))
def zero(a): return all(x==q() for r in a for x in r)

checks=[]
def check(name,condition):
    if not condition: raise RuntimeError(name)
    checks.append(name)

phi=q(F(1,2),F(1,2))
nu2=add(q(1),mul(phi,phi))
invnu2=q(F(1,2),F(-1,10))
check("inverse_norm",mul(nu2,invnu2)==q(1))
columns=[
[q(),q(-1),neg(phi)],[q(-1),neg(phi),q()],
[neg(phi),q(),q(-1)],[q(),q(1),neg(phi)],
[phi,q(),q(-1)],[q(1),neg(phi),q()]]
vectors=[[sc(sign,x) for x in col] for col in columns for sign in (1,-1)]
check("twelve_distinct",len({tuple(v) for v in vectors})==12)
def chi(a):
    a%=5
    return 0 if a==0 else 1 if a in (1,4) else -1
C=[[0 if i==j else 1 if 0 in (i,j) else chi(j-i) for j in range(6)] for i in range(6)]
check("conference",mm([[q(x) for x in r] for r in C],[[q(x) for x in r] for r in C])==scale(5,eye(6)))
for i in range(6):
    for j in range(6):
        expected=q(int(i==j),F(C[i][j],5))
        check("signed_Gram",mul(dot(columns[i],columns[j]),invnu2)==expected)
Q=[[[add(mul(mul(v[i],v[j]),invnu2),q(-F(int(i==j),3)))
      for j in range(3)] for i in range(3)] for v in vectors]
A=[[q(int(j==(i^1))) for j in range(12)] for i in range(12)]
P=[[add(sc(F(1,2),add(q(int(i==j)),A[i][j])),q(-F(1,12)))
    for j in range(12)] for i in range(12)]
check("antipodal_involution",mm(A,A)==eye(12))
check("projector",mm(P,P)==P)
check("trace_five",trace(P)==q(5))
gram=[[trace(mm(Q[i],Q[j])) for j in range(12)] for i in range(12)]
check("quadratic_Gram",gram==scale(F(8,5),P))
# Unnormalised rational basis avoids adjoining sqrt(2) and sqrt(6).
raw=[[[1,0,0],[0,-1,0],[0,0,0]],[[0,1,0],[1,0,0],[0,0,0]],
     [[0,0,1],[0,0,0],[1,0,0]],[[0,0,0],[0,0,1],[0,1,0]],
     [[-1,0,0],[0,-1,0],[0,0,2]]]
basis=[[[q(x) for x in r] for r in e] for e in raw]
Pi=[[q(int(i==j and i<2)) for j in range(3)] for i in range(3)]
for k,e in enumerate(basis):
    image=[[sm(mul(trace(mm(e,Qv)),Qv[i][j]) for Qv in Q)
            for j in range(3)] for i in range(3)]
    check("frame_operator",image==scale(F(8,5),e))
    eq=mm(mm(Pi,e),Pi)
    TT=[[add(eq[i][j],neg(mul(sc(F(1,2),trace(eq)),Pi[i][j])))
         for j in range(3)] for i in range(3)]
    check("TT",TT==(e if k<2 else [[q()]*3 for _ in range(3)]))
invnu4=mul(invnu2,invnu2)
for i in range(3):
    check("fourth_moment",mul(sm(mul(mul(v[i],v[i]),mul(v[i],v[i])) for v in vectors),invnu4)==q(F(12,5)))
    for j in range(i):
        check("mixed_moment",mul(sm(mul(mul(v[i],v[i]),mul(v[j],v[j])) for v in vectors),invnu4)==q(F(4,5)))
for r in range(9):
    for n in range(109):
        m=108-n
        check("carry_composition",(r+n+m)//9==(r+n)//9+((r+n)%9+m)//9)
# Negative control: omitting the constant-mode subtraction changes the trace.
check("reject_rank_six",trace([[sc(F(1,2),add(q(int(i==j)),A[i][j])) for j in range(12)] for i in range(12)])!=q(5))
print(json.dumps({"status":"PASS_PORTADOR_TENSORIAL_VII","exact_checks":len(checks),
    "arithmetic":"Q(sqrt(5)); Fraction","dependencies":"Python standard library",
    "physical_dynamics_certified":False,
    "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},ensure_ascii=False))
