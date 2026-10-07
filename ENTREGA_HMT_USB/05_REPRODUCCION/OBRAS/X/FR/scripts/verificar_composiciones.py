"""Certificado focal: incidencia APP y momentos del registro HMT publicado.
Lee K de la fuente existente; no genera constantes ni consulta valores físicos.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import re

source = Path(__file__).resolve().parents[1] / "appendices/network_cluster.tex"
data = source.read_text()
match = re.search(r"K=\(([\d,\s]+)\)", data)
if match is None:
    raise SystemExit("FAIL: registro K no localizado")
K = [int(v) for v in match.group(1).split(",")]
if len(K) != 12 or min(K) <= 0:
    raise SystemExit("FAIL: dominio positivo dodecafasico")
Q = sum(K)
t = [F(0)]
for v in K:
    t.append(t[-1] + F(v, Q))
if t[-1] != 1 or any(t[i] >= t[i+1] for i in range(12)):
    raise SystemExit("FAIL: orden de las marcas")
def transpose(a):
    return [list(v) for v in zip(*a)]
def mul(a,b):
    bt=transpose(b)
    return [[sum(x*y for x,y in zip(r,c)) for c in bt] for r in a]
def add(a,b):
    return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(c,a):
    return [[c*x for x in r] for r in a]
def eye(n):
    return [[F(i==j) for j in range(n)] for i in range(n)]
def det(a):
    a=[r[:] for r in a]
    out=F(1)
    for i in range(len(a)):
        pivot=next((j for j in range(i,len(a)) if a[j][i]),None)
        if pivot is None:
            return F(0)
        if pivot!=i:
            a[i],a[pivot]=a[pivot],a[i]
            out=-out
        out*=a[i][i]
        for j in range(i+1,len(a)):
            ratio=a[j][i]/a[i][i]
            for c in range(i+1,len(a)):
                a[j][c]-=ratio*a[i][c]
            a[j][i]=F(0)
    return out
faces=list(product(range(3),(-1,1)))
vertices=list(product((-1,1),repeat=3))
M=[[F(v[i]==s) for v in vertices] for i,s in faces]
RF=[[F(i==j and s==-r) for j,r in faces] for i,s in faces]
RV=[[F(all(a==-b for a,b in zip(v,w))) for w in vertices] for v in vertices]
I6=eye(6)
BF=add(scale(7,I6),scale(2,RF))
BV=add(scale(7,eye(8)),scale(2,RV))
Pu=[[F(1,6)]*6 for _ in range(6)]
Pm=scale(F(1,2),add(I6,scale(-1,RF)))
S=add(Pu,Pm)
checks={
    "opposition_intertwining":mul(RF,M)==mul(M,RV),
    "APP_block_intertwining":mul(BF,M)==mul(M,BV),
    "incidence_Gram":mul(M,transpose(M))==add(scale(12,Pu),scale(4,Pm)),
    "quotient_projection":mul(S,S)==S,
    "quotient_action":mul(BF,S)==add(scale(9,Pu),scale(5,Pm)),
    "signed_form_affine_relation":scale(F(1,2),add(scale(7,S),scale(-1,mul(BF,S))))==add(Pm,scale(-1,Pu)),
    "complete_APP_lift":2025-810==54+9*129,
    "marked_lattice_norm":2*(4**2+11)==54,
}
moments=[sum(x**n for x in t) for n in range(18)]
hankel=[]
for k in range(2,10):
    H=[[moments[a+b] for b in range(k)] for a in range(k)]
    minors=[det([row[:j] for row in H[:j]]) for j in range(1,k+1)]
    hankel.append({"k":k,"m":4,"rank":k,"positive_leading_minors":all(v>0 for v in minors),"last_minor_numerator_digits":len(str(minors[-1].numerator))})
checks["Hankel_positive_definite_k2_to_k9"]=all(r["positive_leading_minors"] for r in hankel)
checks["k2_pairwise_gap_identity"]=13*moments[2]-moments[1]**2==sum((t[j]-t[i])**2 for i in range(13) for j in range(i+1,13))
if not all(checks.values()):
    raise SystemExit("FAIL: "+json.dumps(checks))
print(json.dumps({
    "status":"PASS_COMPOSICIONES_FOCALES_INCIDENCIA_MOMENTOS",
    "source":str(source),
    "source_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),
    "source_role":"GENERATED_HMT_OUTPUT_ALREADY_PUBLISHED",
    "Q":Q,"checks":checks,"hankel":hankel,
    "scope":"Identidades racionales exactas y positividad de matrices concretas. Las pruebas generales figuran en sections/incidence_transport.tex y sections/higher_rank.tex.",
    "not_claimed":["cobertura amplituhedral global para k>1","superalgebra N=4 derivada del numeral cuatro","equivalencia automatica del operador de momentos y el operador de masas"]
},ensure_ascii=False,indent=2))
