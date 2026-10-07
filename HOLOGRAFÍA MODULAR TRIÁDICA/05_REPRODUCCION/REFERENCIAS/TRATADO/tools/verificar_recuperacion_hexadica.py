#!/usr/bin/env python3
"""Check the actual matrices printed in the weighted recovery insertion."""
import argparse
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import re

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    args = parser.parse_args()
    text = args.source.read_text(encoding='utf-8')
    matrix_strings = re.findall(r'\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}', text, re.S)
    matrices = []
    for raw in matrix_strings:
        rows = [r.strip() for r in raw.split(r'\\') if r.strip()]
        matrices.append([[int(x.strip()) for x in row.split('&')] for row in rows])
    a,b,m = matrices
    assert len(a) == 6 and all(len(row) == 6 for row in a)
    assert len(b) == len(m) == 12 and all(len(row) == 12 for row in b+m)
    witnesses = ('112210','122101','121200','111100','121012','111020',
                 '122020','112002','111001','110122','101221','011111')
    def support(w):
        v = tuple(map(int,w))
        code = v + tuple(sum(v[i]*a[i][j] for i in range(6)) % 3 for j in range(6))
        return tuple(i for i,x in enumerate(code) if x)
    generated = [[int(j in support(w)) for j in range(12)] for w in witnesses]
    assert generated == b
    assert all(sum(row) == 6 for row in b)
    def matmul(u,v):
        return [[sum(u[i][k]*v[k][j] for k in range(len(v)))
                 for j in range(len(v[0]))] for i in range(len(u))]
    identity18 = [[18*int(i == j) for j in range(12)] for i in range(12)]
    assert matmul(m,b) == matmul(b,m) == identity18
    hexads = {support(w) for w in product(range(3),repeat=6) if len(support(w)) == 6}
    assert len(hexads) == 132
    five = Counter(t for h in hexads for t in combinations(h,5))
    assert len(five) == 792 and set(five.values()) == {1}
    gram = [[sum(i in h and j in h for h in hexads) for j in range(12)] for i in range(12)]
    assert gram == [[36*int(i==j)+30 for j in range(12)] for i in range(12)]
    e12 = [0]*11+[1]
    y = [sum(u*v for u,v in zip(row,e12)) for row in b]
    assert y == [1,0,0,0,0,0,0,0,1,0,0,0]
    assert [sum(u*v for u,v in zip(row,y)) for row in m] == [18*x for x in e12]
    receipt = {'status':'PASS_EXACT_PRINTED_WEIGHTED_HEXAD_RECOVERY',
               'source':str(args.source),'ambient_words':729,'hexads':132,
               'five_subsets':792,'witness_hexads':12,
               'incidence_generated_from_encoder':True,'MB_and_BM_equal_18I':True,
               'gram_identity':True,'example_recovered':True,
               'Lean_recompiled':False,'K_used_to_select_witnesses':False}
    args.receipt.parent.mkdir(parents=True,exist_ok=True)
    args.receipt.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(receipt['status'])

if __name__ == '__main__':
    main()
