"""Exact checks of the marked K -> moments -> Jacobi realization.

Uses a generated register already published by the HMT corpus. It does not
claim to re-execute its upstream generation or certify a physical spectrum.
All assertions are explicit checks, active also under python -O.
"""
from fractions import Fraction as F
import json
import re
from pathlib import Path
from hashlib import sha256

# Read the already generated internal register from its included source.
OWNER = Path(__file__).resolve().parents[1] / 'foundation/sections/registro_k.tex'
match = re.search(r"K=\(([0-9,\s]+)\)", OWNER.read_text())
if match is None:
    raise RuntimeError("Published K not found")
K = [int(x) for x in match.group(1).replace('\n', '').split(',')]

def check(value, message):
    if not value:
        raise RuntimeError(message)

def add(a, b):
    c = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a): c[i] += x
    for i, x in enumerate(b): c[i] += x
    return c

def scale(a, x): return [x*v for v in a]
def mul(a, b):
    c = [F(0)] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): c[i+j] += x*y
    return c

def mv(A, x): return [sum(a*b for a,b in zip(row,x)) for row in A]
def solve(A,b):
    B = [list(row)+[x] for row,x in zip(A,b)]
    n = len(B)
    for j in range(n):
        p = next((i for i in range(j,n) if B[i][j]), None)
        check(p is not None, "singular matrix")
        B[j],B[p] = B[p],B[j]
        d = B[j][j]; B[j] = [x/d for x in B[j]]
        for i in range(n):
            if i != j:
                v = B[i][j]; B[i] = [x-v*y for x,y in zip(B[i],B[j])]
    return [row[-1] for row in B]

def run(register, n):
    Q = sum(register)
    d = [F(x,Q) for x in register]
    t = [F(0)]
    for x in d: t.append(t[-1]+x)
    check(t[-1] == 1 and min(d)>0, "positive marked partition")
    m = [sum((b**(r+1)-a**(r+1))/x for a,b,x in zip(t,t[1:],d))/(12*(r+1)) for r in range(2*n+2)]
    def inner(a,b): return sum(x*m[j] for j,x in enumerate(mul(a,b)))
    p=[]; h=[]; alpha=[]; beta=[F(0)]
    for j in range(n+1):
        q=[F(0)]*j+[F(1)]
        for v,hv in zip(p,h): q=add(q,scale(v,-inner(q,v)/hv))
        p.append(q); h.append(inner(q,q))
        check(h[-1]>0,"positive squared norm")
        alpha.append(inner([F(0)]+q,q)/h[-1])
        if j: beta.append(h[j]/h[j-1])
    for j in range(1,n):
        rhs=add(add([F(0)]+p[j],scale(p[j],-alpha[j])),scale(p[j-1],-beta[j]))
        check(rhs==p[j+1],"monic three-term recurrence")
    # T is the rational monic-basis version of the symmetric Jacobi matrix.
    T=[[F(0) for _ in range(n)] for _ in range(n)]
    for j in range(n):
        T[j][j]=alpha[j]
        if j+1<n: T[j+1][j]=1
        if j: T[j-1][j]=beta[j]
    for i in range(n):
        for j in range(n):
            check(h[i]*T[i][j]==h[j]*T[j][i],"self-adjointness for the Gram metric")
    v=[F(1)]+[F(0)]*(n-1)
    for r in range(2*n):
        check(v[0]==m[r],"Gaussian moment identity degree "+str(r))
        v=mv(T,v)
    z=F(2)
    A=[[(z if i==j else F(0))-T[i][j] for j in range(n)] for i in range(n)]
    g=solve(A,[F(1)]+[F(0)]*(n-1))[0]
    den=z-alpha[-2]
    for j in range(n-2,-1,-1): den=z-alpha[j]-beta[j+1]/den
    check(g==1/den,"continued fraction from the Schur complement")
    # An unweighted replacement measure must not silently stand for mu_K.
    wrong=sum(t)/len(t)
    check(wrong != m[1],"negative control: nodal counting changes the measure")
    return {"degree":n,"Q":Q,"moments_checked":2*n,"a0":str(alpha[0]),"beta1":str(beta[1]),"resolvent_at_2":str(g)}

if __name__ == "__main__":
    report=run(K,4)
    check(report['Q']==6263, 'published register total')
    print(json.dumps({"status":"PASS_JACOBI_EXACT", "owner":str(OWNER), "owner_sha256":sha256(OWNER.read_bytes()).hexdigest(), "scope":"general positive-register theorem, exact specialization at the published HMT register; upstream generation not re-executed", "result":report},ensure_ascii=False))
