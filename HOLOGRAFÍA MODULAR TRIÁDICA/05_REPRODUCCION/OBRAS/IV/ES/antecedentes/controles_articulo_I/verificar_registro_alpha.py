#!/usr/bin/env python3
"""Controles posteriores exactos del registro y la clausura; no genera U desde TPK."""
from fractions import Fraction as F
from itertools import combinations, product
from functools import reduce
from math import gcd
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
B = 1000
K = (234,543,140,729,659,824,621,58,914,794,146,601)
U = (2378,1406,2479,-452,998,-551,-668,-204,-371,-322,-28,-997)
D90 = (-495,-116,-684,108,601,-90,-173,-88,313,560,-397,461)
D120 = (-425,-281,-481,671,-255,30,475,-543,680,251,6,-128)
H = ((1,1,1,1),(1,1,-1,-1),(1,-1,1,-1),(1,-1,-1,1))


def det(matrix):
    a = [[F(x) for x in row] for row in matrix]
    answer = F(1)
    for i in range(len(a)):
        pivot = next((j for j in range(i,len(a)) if a[j][i]), None)
        if pivot is None:
            return F(0)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            answer = -answer
        d = a[i][i]
        answer *= d
        for j in range(i+1,len(a)):
            factor = a[j][i]/d
            for k in range(i+1,len(a)):
                a[j][k] -= factor*a[i][k]
    return answer


def rank(matrix):
    a = [[F(x) for x in row] for row in matrix]
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r,len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        d = a[r][col]
        a[r] = [x/d for x in a[r]]
        for i in range(r+1,len(a)):
            f = a[i][col]
            a[i] = [x-f*y for x,y in zip(a[i],a[r])]
        r += 1
    return r


def matvec(m, x):
    return tuple(sum(a*b for a,b in zip(row,x)) for row in m)


def incidence(step):
    out = []
    for i in range(12):
        row = [0]*12
        row[i], row[(i+step)%12] = 1, -1
        out.append(row)
    return out


def closure(t):
    p = (141,592,653,589,793,238,462,643,383,279,502,884)
    e = (718,281,828,459,45,235,360,287,471,352,662,497)
    f = (618,33,988,749,894,848,204,586,834,365,638,117)
    c, a = [0]*12+[t], [0]*12
    z = [p[j]+e[j]-f[j]-K[j] for j in range(12)]
    for j in reversed(range(12)):
        c[j], a[j] = divmod(z[j]+c[j+1],B)
        assert z[j]-a[j] == B*c[j]-c[j+1]
    assert sum((z[j]-a[j])*B**(11-j) for j in range(12)) == B**12*c[0]-c[12]
    return tuple(a),tuple(c)


def check_tex():
    paths = [ROOT/'sections/registro_k.tex', ROOT/'sections/alpha.tex']
    labels, refs, totals = set(), [], {}
    for path in paths:
        text = path.read_text(encoding='utf-8')
        stripped = '\n'.join(line.split('%',1)[0] for line in text.splitlines())
        depth = 0
        for ch in stripped:
            if ch == '{': depth += 1
            if ch == '}': depth -= 1
            assert depth >= 0, (path,'brace underflow')
        assert depth == 0, (path,'brace balance')
        stack = []
        for op,env in re.findall(r'\\(begin|end)\{([^}]+)\}',stripped):
            if op == 'begin': stack.append(env)
            else: assert stack.pop() == env, (path,env)
        assert not stack, (path,stack)
        assert stripped.count(r'\[') == stripped.count(r'\]')
        assert stripped.count(r'\(') == stripped.count(r'\)')
        local = re.findall(r'\\label\{([^}]+)\}',stripped)
        assert len(local) == len(set(local))
        assert not labels.intersection(local)
        labels.update(local)
        refs.extend(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',stripped))
        totals[path.name] = {'lines':len(text.splitlines()),'labels':len(local)}
    assert set(refs) <= labels, sorted(set(refs)-labels)
    return totals


def main():
    assert tuple(tuple(sum(H[i][k]*H[k][j] for k in range(4)) for j in range(4)) for i in range(4)) == tuple(tuple(4*int(i==j) for j in range(4)) for i in range(4))
    assert det(H) == -16
    divisors=[]
    for size in range(1,5):
        minors=[abs(int(det([[H[i][j] for j in cols] for i in rows])))
                for rows in combinations(range(4),size)
                for cols in combinations(range(4),size)]
        divisors.append(reduce(gcd,minors))
    assert divisors == [1,2,4,16]
    assert tuple(K[i]-K[(i+3)%12] for i in range(12)) == D90
    assert tuple(K[i]-K[(i+4)%12] for i in range(12)) == D120
    assert sum(K) == 6263
    br = [sum(D120[r+3*j] for j in range(4)) for r in range(3)]
    assert br == [972,-1073,101]
    s1 = F(6263+2*br[0]+br[1],3)
    s = [s1,s1-br[0],s1-br[0]-br[1]]
    reconstructed = [0]*12
    for r in range(3):
        d = [D90[r+3*j] for j in range(4)]
        ur = (s[r],d[1]-d[3],d[0]+d[2],d[0]-d[2])
        assert ur == tuple(U[r+3*j] for j in range(4))
        kr = tuple(x/4 for x in matvec(H,ur))
        assert all(x.denominator == 1 for x in kr)
        for j in range(4): reconstructed[r+3*j] = int(kr[j])
    assert tuple(reconstructed) == K
    inc = incidence(3)+incidence(4)
    assert rank(inc) == 11 and rank(inc+[[1]*12]) == 12
    # Un árbol generador: conservar sólo las aristas que unen componentes.
    parent=list(range(12))
    def find(i):
        while parent[i] != i: i=parent[i]
        return i
    tree=[]
    for row in inc:
        i,j=row.index(1),row.index(-1)
        a,b=find(i),find(j)
        if a != b:
            parent[a]=b
            tree.append(row)
    assert len(tree)==11 and abs(det(tree+[[1]*12])) == 12
    nk=sum(k*B**(11-i) for i,k in enumerate(K))
    assert nk == 234543140729659824621058914794146601
    k36,kper=F(nk,B**12),F(nk,B**12-1)
    assert kper-k36 == kper/B**12
    assert next(d for d in range(1,13) if all(K[i]==K[(i+d)%12] for i in range(12)))==12
    a0,c0=closure(0)
    ai,ci=closure(-1)
    assert a0 == (7,297,352,569,283,800,997,285,105,472,380,663)
    assert c0 == (0,0,0,-1,-1,-2,-1,0,-1,-1,0,0,0)
    assert ai[:-1] == a0[:-1] and ai[-1]==662
    assert ci[:-1] == c0[:-1] and ci[-1]==-1
    for t in range(-2,3):
        a,c=closure(t)
        assert set(c) <= set(range(-2,3)) and c[0]==0
    assert F(-1,120)*F(-8,3)==F(1,45)
    assert F(1,45)*F(2,11)==F(2,495)
    assert det(((85,112),(41,52))) == -172
    assert F(172,43)==4 and 3*7==21 and 3*7-1==20
    assert 7*7-2*2==45 and 8*15==120 and 45*11==495
    mu=F(628,100)-F(7,2)*F(1,100)-F(10,21)*F(1,10**8)-F(6,46)*F(1,10**10)-F(7,120)*F(1,10**12)
    assert mu > F(624,100)
    lower=F(628,100)*F(1,100)-F(7,4)*F(1,100**2)-F(2,21)*F(1,100**5)-F(1,46)*F(1,100**6)-F(1,120)*F(1,100**7)
    assert lower > F(626,10000) > F(46,1000)
    V=range(-2,3)
    edges={B*v-w:(v,w) for v,w in product(V,repeat=2)}
    assert len(edges)==25
    count=0
    for path in product(V,repeat=5):
        u=[B*path[i]-path[i+1] for i in range(4)]
        assert sum((F(u[i],B**(i+1)) for i in range(4)),F()) == path[0]-F(path[4],B**4)
        assert all(edges[u[i]][1]==edges[u[i+1]][0] for i in range(3))
        count+=1
    for v,actual_delta in product(V,range(-4,5)):
        if -1 < v-actual_delta < 1: assert v==actual_delta
    report={
        'status':'PASS_CONTROLES_POSTERIORES_REGISTRO_ALPHA',
        'scope':'Aritmética posterior de publicaciones previamente serializadas; no reconstruye E108 desde el estado TPK.',
        'hadamard_determinantal_divisors':divisors,
        'D3_D4_rank':11,'D3_D4_Q_rank':12,'spanning_tree_maximal_minor_absolute':12,
        'Pi_H_U_K_exact':True,'K_minimal_block_period':12,
        'kappa36':str(k36),'kappa_per':str(kper),'window_boundary_0_and_minus1':True,
        'nilpotent_coefficients_exact':True,'P9_coarse_derivative_and_sign_bounds':True,
        'carry_difference_edge_labels':len(edges),'carry_difference_paths_checked':count,
        'tex_static':check_tex(),
        'upstream_E108_generator_executed':False,'full_E21_22_coefficients_generated':False,
        'irrationality_proved':False,'target_digits_used_as_generator_inputs':False,
    }
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
