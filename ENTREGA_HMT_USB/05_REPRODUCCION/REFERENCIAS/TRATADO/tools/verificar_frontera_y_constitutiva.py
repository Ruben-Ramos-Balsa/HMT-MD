#!/usr/bin/env python3
"""Exact finite regression for the two ampliative insertions.

The visible catalogue is generated upstream by APP--TRIT--TPK. This
verifier receives that catalogue, reconstructs the regional selection,
enumerates its first boundary, computes graph distances and checks the
incidence change of representation. It separately checks the rational
constitutive example. It does not certify general equivalence of boundary
selection criteria, a full Lean development, or any physical comparison.
"""
import argparse
from collections import Counter, deque
import csv
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path

L0 = ((2,2,2,1,2,1),(2,1,2,2,1,1),(1,0,0,1,0,2),
      (0,0,1,1,1,0),(2,2,2,0,2,1),(2,1,2,1,0,0))
L1 = ((2,1,2,0,2,2),(1,2,1,1,2,0),(1,2,1,1,1,2),
      (0,1,0,0,2,1),(2,0,2,1,0,1),(0,2,2,2,1,1))
AO = ((0,1,1,1,1,1),(1,0,1,1,2,2),(1,1,0,2,1,2),
      (1,1,2,0,2,1),(1,2,1,2,0,1),(1,2,2,1,1,0))
AA = ((0,1,1,1,1,1),(1,0,1,2,2,1),(1,1,0,1,2,2),
      (1,2,1,0,1,2),(1,2,2,1,0,1),(1,1,2,2,1,0))
PERM = (0,1,2,4,5,3)
I = tuple(tuple(int(i == j) for j in range(6)) for i in range(6))

def require(test, message):
    if not test:
        raise AssertionError(message)

def vec(s):
    return tuple(map(int, s))

def word(v):
    return ''.join(map(str, v))

def row(v, a):
    return tuple(sum(v[i] * a[i][j] for i in range(6)) % 3
                 for j in range(6))

def mul(a, b):
    return tuple(row(v, b) for v in a)

def power(a, n):
    r = I
    for _ in range(n):
        r = mul(r, a)
    return r

def add(a, b):
    return tuple((u + v) % 3 for u, v in zip(a, b))

def sub(a, b):
    return tuple((u - v) % 3 for u, v in zip(a, b))

def chain(v):
    result = [v]
    for a in (L0,L0,L1,L1):
        result.append(row(result[-1], a))
    return result

def distances(source):
    found = {source: (0, '')}
    queue = deque([source])
    while queue:
        current = queue.popleft()
        n, route = found[current]
        for symbol, a in (('0', L0), ('1', L1)):
            following = row(current, a)
            if following not in found:
                found[following] = (n + 1, route + symbol)
                queue.append(following)
    return found

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    args = parser.parse_args()
    with args.catalog.open(newline='', encoding='utf-8') as stream:
        visible = sorted({vec(record['w6']) for record in csv.DictReader(stream)})
    require(len(visible) == 243, 'visible catalogue cardinal')
    require(all(len(w) == 6 and set(w) <= {0,1,2} for w in visible), 'visible type')
    chains = {w: chain(w) for w in visible}
    pairs = [(a,b) for a in visible for b in visible
             if chains[a][2] == a and chains[b][4] == chains[b][2]
             and chains[a][1] == chains[b][3]]
    require(len(pairs) == 1, 'regional selection uniqueness')
    closing, propagating = pairs[0]
    axis = chains[propagating][4]
    ai = tuple(tuple(-x % 3 for x in r) for r in AO)
    require(mul(AO, ai) == I, 'inverse incidence')
    left = mul(mul(ai, power(L0,3)), power(AO,3))
    right = mul(mul(mul(power(L0,2), power(L1,2)), AO), power(L1,3))
    d = tuple(sub(a,b) for a,b in zip(left,right))
    ambient_solutions = [v for v in product(range(3), repeat=6) if row(v,d) == axis]
    require(list(map(word,ambient_solutions)) == ['020010','121200','222120'],
            'compatibility solutions')
    candidates = []
    visible_solutions = [s for s in visible if row(s,d) == axis]
    for scale in visible_solutions:
        mobile = row(row(chains[scale][4], AO), power(L1,3))
        occupancy = tuple(2 + int(axis[j] != 0 and mobile[j] != 2) for j in range(6))
        for x in product(range(3), repeat=6):
            y = sub(mobile,x)
            rows = (x,y,axis)
            sums = tuple(sum(column) for column in zip(*rows))
            carries = tuple(s // 3 for s in sums)
            occupied = tuple(sum(v != 0 for v in column) for column in zip(*rows))
            if carries != (1,)*6 or occupied != occupancy:
                continue
            if any(sum(row(v,AO)) % 3 for v in rows):
                continue
            candidates.append({'scale':word(scale),'rows':list(map(word,rows)),
                               'margin':word(tuple(s % 3 for s in sums)),
                               'carry':word(carries),'occupancy':word(occupied)})
    require(len(candidates) == 2, 'boundary cardinal')
    require({c['scale'] for c in candidates} == {'121200'}, 'autoscale selection')
    sources = [chains[closing][4],chains[propagating][4],chains[vec('121200')][4]]
    tables = [distances(s) for s in sources]
    for c in candidates:
        entries = [table[vec(w)] for table,w in zip(tables,c['rows'])]
        c['distances'] = [e[0] for e in entries]
        c['routes'] = [e[1] for e in entries]
        c['length_sum'] = sum(c['distances'])
    selected = min(candidates, key=lambda c:c['length_sum'])
    require(selected['rows'] == ['222220','021222','102011'], 'selected boundary')
    require(sorted(c['length_sum'] for c in candidates) == [20,23], 'length sums')
    perm = lambda v: tuple(v[j] for j in PERM)
    require(tuple(tuple(AO[i][j] for j in PERM) for i in PERM) == AA, 'matrix transport')
    for v in product(range(3), repeat=6):
        require(perm(row(v,AO)) == row(perm(v),AA), 'incidence naturality')
    f = lambda s: (1+s+s*s)/(1+s+s*s+s*s*s)
    sigma = lambda s: 30*s**3*(3+2*s+s*s)/((1+s+s*s)*(1+s+s*s+s**3))
    r_minus, r_plus = f(F(1,2)), f(F(1,4))
    a,b = sigma(F(1,2)),sigma(F(1,4))
    require((r_minus,r_plus) == (F(14,15),F(84,85)), 'constitutive example')
    require(r_minus/r_plus == F(17,18), 'quotient example')
    require(1/(r_minus*r_plus) == F(425,392), 'inverse product example')
    require((a,b) == (F(34,7),F(114,119)), 'differential example')
    require((a-b)**2-(a+b)**2 == -4*a*b == F(-15504,833), 'Jacobian example')
    receipt = {
        'status':'PASS_EXACT_R36_AND_CONSTITUTIVE_EXAMPLE',
        'catalog_sha256':hashlib.sha256(args.catalog.read_bytes()).hexdigest(),
        'visible_word_count':len(visible),
        'regional_pair':list(map(word,pairs[0])),
        'ambient_compatibility':list(map(word,ambient_solutions)),
        'visible_compatibility':list(map(word,visible_solutions)),
        'boundary_candidates':candidates,
        'selected':selected,
        'layer_counts':{word(s):dict(sorted(Counter(n for n,_ in table.values()).items()))
                        for s,table in zip(sources,tables)},
        'naturality_cases':729,
        'transported_boundary':[word(perm(vec(w))) for w in selected['rows']],
        'constitutive_example':{'r_minus':str(r_minus),'r_plus':str(r_plus),
                                'a':str(a),'b':str(b),'jacobian':str(-4*a*b)},
        'general_boundary_criterion_equivalence_claimed':False,
        'full_Lean_recompilation_claimed':False,
        'target_constant_digits_used_as_input':False,
    }
    args.receipt.parent.mkdir(parents=True,exist_ok=True)
    args.receipt.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(receipt['status'])

if __name__ == '__main__':
    main()
