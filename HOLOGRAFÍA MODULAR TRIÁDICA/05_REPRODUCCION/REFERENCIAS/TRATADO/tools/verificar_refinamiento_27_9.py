#!/usr/bin/env python3
"""Comprobación exacta del refinamiento APP y sus cocientes de acarreo."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument("--source",required=True)
p.add_argument("--receipt",required=True)
a=p.parse_args()

def require(test,message):
    if not test:
        raise RuntimeError(message)

def split(x):
    return x%9,x//9

fibres={}
for x,y in itertools.product(range(27),repeat=2):
    r,c=split(x)
    s,d=split(y)
    require(x==r+9*c and y==s+9*d,"Division euclidea")
    fibres.setdefault((r,s),set()).add((c,d))
require(len(fibres)==81 and all(len(v)==9 for v in fibres.values()),"Fibras")
for x,y in itertools.product(range(27),repeat=2):
    r,c=split(x)
    s,d=split(y)
    suma=((r+s)%9,(c+d+(r+s)//9)%3)
    producto=((r*s)%9,((r*s)//9+r*d+s*c)%3)
    require(suma==split((x+y)%27),"Suma con cociente")
    require(producto==split((x*y)%27),"Producto con cociente")
for r,s,t in itertools.product(range(9),repeat=3):
    left=(r+s)//9+((r+s)%9+t)//9
    right=(s+t)//9+(r+(s+t)%9)//9
    require(left==right==(r+s+t)//9,"Cociclo")
for x,y in itertools.product(range(27),repeat=2):
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        r,c=split(x)
        s,d=split(y)
        rx,cy=(r+dx)%9,(c+(r+dx)//9)%3
        sx,dyq=(s+dy)%9,(d+(s+dy)//9)%3
        require((rx+9*cy,sx+9*dyq)==((x+dx)%27,(y+dy)%27),"Desplazamiento")
receipt={
    "status":"PASS_EXACT_APP_27_TO_9_REFINEMENT",
    "source_sha256":hashlib.sha256(Path(a.source).read_bytes()).hexdigest(),
    "positions":729,"fibres":81,"positions_per_fibre":9,
    "one_coordinate_pairs_add_and_multiply":729,
    "cocycle_triples":729,"directional_updates":2916,
    "scope":"Soporte APP, suma/producto modular, fibra de dos trits y direcciones; lectores internos conservan sus dominios.",
    "lean_recompiled":False,
}
Path(a.receipt).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(receipt["status"])
