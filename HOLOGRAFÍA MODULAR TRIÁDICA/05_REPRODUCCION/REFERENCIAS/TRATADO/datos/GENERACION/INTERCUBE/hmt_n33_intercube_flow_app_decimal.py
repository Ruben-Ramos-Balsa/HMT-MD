#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N33 -- Flujo entre cubos APP y generacion de triadas decimales.

Este script no asume que HMT ya genere infinitamente pi,e,phi.
Hace lo contrario: construye el espacio correcto de estados por triadas,
prueba invariantes exactos de APP cubica y somete varias hipoteses de flujo
local a falsadores. La intencion es separar:
  (i) geometria/estado (verde),
  (ii) flujos simples descartados (rojo),
  (iii) estructura espectral/proyectiva para el flujo real (amarillo fuerte).

Se trabaja con triadas decimales (000..999) como puntos del cubo 10^3.
La lectura interna por raiz digital sigue siendo mod 9 porque
100a+10b+c = a+b+c (mod 9).
"""
from __future__ import annotations
import itertools, json, math, random, hashlib
from collections import Counter, defaultdict
from pathlib import Path
from typing import List, Tuple, Dict
import numpy as np
import mpmath as mp

OUT = Path('/mnt/data')
JSON_OUT = OUT / 'hmt_n33_intercube_flow_results.json'
TEX_RESULTS = OUT / 'hmt_n33_intercube_flow_results.tex'

# -----------------------------------------------------------------------------
# Basic APP utilities
# -----------------------------------------------------------------------------
def dr9(n:int)->int:
    if n == 0:
        return 0
    return ((n-1) % 9) + 1

def triad_digits(v:int)->Tuple[int,int,int]:
    return (v//100, (v//10)%10, v%10)

def addr_mod3(v:int)->Tuple[int,int,int]:
    a,b,c = triad_digits(v)
    return (a%3,b%3,c%3)

def bulk(v:int)->bool:
    a,b,c = triad_digits(v)
    return a!=0 and b!=0 and c!=0

def triads_of_constant(name:str, n:int=720)->List[int]:
    mp.mp.dps = max(100, 3*n + 50)
    if name == 'pi':
        x = mp.pi
    elif name == 'e':
        x = mp.e
    elif name == 'phi':
        x = (1+mp.sqrt(5))/2
    else:
        raise ValueError(name)
    frac = str(x).split('.')[1]
    frac = (frac + '0'*(3*n))[:3*n]
    return [int(frac[3*i:3*i+3]) for i in range(n)]

# -----------------------------------------------------------------------------
# APP exact invariants
# -----------------------------------------------------------------------------
def app_invariants() -> Dict:
    Splus2 = Sprod2 = 0
    for i,j in itertools.product(range(1,10), repeat=2):
        Splus2 += dr9(i+j)
        Sprod2 += dr9(i*j)
    Splus3 = Sprod3 = 0
    for i,j,k in itertools.product(range(1,10), repeat=3):
        Splus3 += dr9(i+j+k)
        Sprod3 += dr9(i*j*k)
    strata = Counter()
    for a,b,c in itertools.product(range(10), repeat=3):
        z = (a==0)+(b==0)+(c==0)
        strata[int(z)] += 1
    return {
        'S_plus_2D': Splus2,
        'S_prod_2D': Sprod2,
        'Delta_2D': Sprod2-Splus2,
        'S_plus_3D': Splus3,
        'S_prod_3D': Sprod3,
        'Delta_3D': Sprod3-Splus3,
        'bulk_9cubed': 9**3,
        'decimal_cube': 10**3,
        'corona': 10**3-9**3,
        'corona_strata': {str(k): v for k,v in strata.items()},
        'moonshine_anchor': (Sprod2-Splus2)*(Splus3+1),
    }

# -----------------------------------------------------------------------------
# Search: deterministic first-order maps and LCGs
# -----------------------------------------------------------------------------
def conflict_map(seq:List, transform=lambda x:x) -> Dict:
    seen = {}
    repeats = conflicts = 0
    examples = []
    xs = [transform(x) for x in seq]
    ys = [transform(x) for x in seq[1:]]
    for a,b in zip(xs,ys):
        if a in seen:
            repeats += 1
            if seen[a] != b:
                conflicts += 1
                if len(examples)<5:
                    examples.append({'state': str(a), 'old_next': str(seen[a]), 'new_next': str(b)})
        else:
            seen[a] = b
    return {'unique_states': len(seen), 'repeats': repeats, 'conflicts': conflicts, 'examples': examples}

def lcg_exists(seq:List[int], mod:int, ncheck:int=24) -> Dict:
    # Search a,b with x_{n+1}=a x_n+b mod M for first ncheck transitions.
    xs = [x % mod for x in seq[:ncheck+1]]
    best = {'hits': -1, 'a': None, 'b': None}
    for a in range(mod):
        b = (xs[1] - a*xs[0]) % mod
        hits = sum(((a*xs[i]+b)%mod)==xs[i+1] for i in range(ncheck))
        if hits > best['hits']:
            best = {'hits': hits, 'a': a, 'b': b}
        if hits == ncheck:
            return {'exists': True, 'a': a, 'b': b, 'ncheck': ncheck, 'best_hits': hits}
    return {'exists': False, 'ncheck': ncheck, 'best_hits': best['hits'], 'best_a': best['a'], 'best_b': best['b']}

# -----------------------------------------------------------------------------
# Local CA over F3 for 12-triad blocks of residues.
# -----------------------------------------------------------------------------
def triad_residue_blocks(seq:List[int], nblocks:int=None)->List[List[int]]:
    vals = [sum(triad_digits(v)) % 3 for v in seq]
    nb = len(vals)//12 if nblocks is None else min(nblocks, len(vals)//12)
    return [vals[12*i:12*(i+1)] for i in range(nb)]

def best_linear_ca(blocks_by_name:Dict[str,List[List[int]]], radius:int=3)->Dict:
    pairs=[]
    for name, blocks in blocks_by_name.items():
        for i in range(len(blocks)-1):
            pairs.append((blocks[i], blocks[i+1]))
    def eval_rule(coeffs):
        hits=total=0
        r=radius
        for x,y in pairs:
            n=len(x)
            for i in range(n):
                val = coeffs[-1]
                for off,c in zip(range(-r,r+1), coeffs[:-1]):
                    val += c*x[(i+off)%n]
                if val % 3 == y[i]: hits += 1
                total += 1
        return hits,total
    # Exhaustive for radius<=3; 3^(2r+2) <= 6561.
    best = {'accuracy': -1, 'coeffs': None, 'hits': 0, 'total': 0}
    for coeffs in itertools.product(range(3), repeat=2*radius+2):
        h,t = eval_rule(coeffs)
        acc = h/t
        if acc > best['accuracy']:
            best = {'accuracy': acc, 'coeffs': coeffs, 'hits': h, 'total': t}
    return best

# -----------------------------------------------------------------------------
# A5 projectors from N32 minimal import-free implementation.
# -----------------------------------------------------------------------------
Perm=Tuple[int,...]
def compose(p:Perm,q:Perm)->Perm: return tuple(p[i] for i in q)
def inverse(p:Perm)->Perm:
    r=[0]*len(p)
    for i,j in enumerate(p): r[j]=i
    return tuple(r)
def parity(p:Perm)->int:
    inv=0
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: inv+=1
    return inv%2
def cycle_type(p:Perm)->Tuple[int,...]:
    seen=[False]*len(p); ty=[]
    for i in range(len(p)):
        if not seen[i]:
            j=i; L=0
            while not seen[j]:
                seen[j]=True; L+=1; j=p[j]
            if L>1: ty.append(L)
    return tuple(sorted(ty, reverse=True)) or (1,)
A5=[p for p in itertools.permutations(range(5)) if parity(p)==0]
ID=tuple(range(5))
g5=(1,2,3,4,0); g5sq=compose(g5,g5)
# conjugacy classes
unassigned=set(A5); classes=[]
while unassigned:
    g=next(iter(unassigned)); cls=set(compose(compose(h,g), inverse(h)) for h in A5)
    classes.append(cls); unassigned-=cls
cls_idx={g:i for i,cls in enumerate(classes) for g in cls}
class_of_g5=cls_idx[g5]; class_of_g5sq=cls_idx[g5sq]
label_by_class={}
for idx, cls in enumerate(classes):
    ty=cycle_type(next(iter(cls)))
    if ty==(1,): label_by_class[idx]='1A'
    elif ty==(3,): label_by_class[idx]='3A'
    elif ty==(2,2): label_by_class[idx]='2A'
    elif ty==(5,): label_by_class[idx]='5A' if idx==class_of_g5 else ('5B' if idx==class_of_g5sq else '5?')
# C5 cosets
H=set(); cur=ID
for _ in range(5): H.add(cur); cur=compose(g5,cur)
rem=set(A5); cosets=[]
while rem:
    rep=next(iter(rem)); cos=set(compose(rep,h) for h in H); cosets.append(cos); rem-=cos
coset_index={x:i for i,cos in enumerate(cosets) for x in cos}
def rep_matrix(g):
    P=np.zeros((12,12))
    for i,cos in enumerate(cosets):
        x=next(iter(cos)); y=compose(g,x); j=coset_index[y]; P[j,i]=1
    return P
phi=(1+math.sqrt(5))/2
def char_val(rep,g):
    label=label_by_class[cls_idx[g]]
    if rep=='1': return 1
    if rep=='3': return {'1A':3,'5A':phi,'5B':1-phi,'3A':0,'2A':-1}[label]
    if rep=="3'": return {'1A':3,'5A':1-phi,'5B':phi,'3A':0,'2A':-1}[label]
    if rep=='4': return {'1A':4,'5A':-1,'5B':-1,'3A':1,'2A':0}[label]
    if rep=='5': return {'1A':5,'5A':0,'5B':0,'3A':-1,'2A':1}[label]
projectors={}
dims={'1':1,'3':3,"3'":3,'4':4,'5':5}
for rep,d in dims.items():
    P=np.zeros((12,12))
    for g in A5: P += char_val(rep,inverse(g))*rep_matrix(g)
    projectors[rep]=P*d/60
Ps=[rep_matrix(g) for g in A5]

def block_energy(block:List[int])->Dict[str,float]:
    v=np.array(block,dtype=float); vc=v-np.mean(v); den=float(np.dot(vc,vc))
    if den<1e-12: return {rep:0.0 for rep in projectors}
    return {rep: float(np.dot(P@vc, P@vc)/den) for rep,P in projectors.items()}

def a5_transition_scores(blocks:List[List[int]])->Dict:
    corrs=[]; rms=[]
    for b,c in zip(blocks, blocks[1:]):
        b=np.array(b,dtype=float); c=np.array(c,dtype=float)
        bc=b-b.mean(); cc=c-c.mean()
        best_corr=-9; best_rmse=None
        for P in Ps:
            pb=P@bc
            den=float(np.linalg.norm(pb)*np.linalg.norm(cc))
            corr=float(np.dot(pb,cc)/den) if den>1e-12 else 0.0
            if corr>best_corr:
                best_corr=corr
                best_rmse=float(np.sqrt(np.mean((pb-cc)**2)))
        corrs.append(best_corr); rms.append(best_rmse)
    return {'mean_best_corr': float(np.mean(corrs)), 'min_best_corr': float(np.min(corrs)), 'max_best_corr': float(np.max(corrs)), 'mean_rmse_centered': float(np.mean(rms))}

# -----------------------------------------------------------------------------
# Main computation
# -----------------------------------------------------------------------------
def main():
    random.seed(33)
    consts=['pi','e','phi']
    ntri=360
    sequences={name: triads_of_constant(name,ntri) for name in consts}
    app=app_invariants()
    per_const={}
    blocks_by_res={}
    for name, seq in sequences.items():
        blocks=[seq[12*i:12*(i+1)] for i in range(len(seq)//12)]
        blocks_by_res[name]=triad_residue_blocks(seq, len(blocks))
        # bulk/corona counts by block
        bulk_counts=[sum(bulk(v) for v in block) for block in blocks]
        energy=[block_energy(block) for block in blocks]
        avg_energy={rep: float(np.mean([e[rep] for e in energy])) for rep in ['1','3',"3'",'4','5']}
        per_const[name]={
            'triad_memory1': conflict_map(seq, lambda x:x),
            'addr_mod3_memory1': conflict_map(seq, addr_mod3),
            'residue_mod3_memory1': conflict_map(seq, lambda x: sum(triad_digits(x))%3),
            'lcg_mod1000_first24': lcg_exists(seq,1000,24),
            'lcg_mod9_first24': lcg_exists([sum(triad_digits(x))%9 for x in seq],9,24),
            'bulk_counts_first10_blocks': bulk_counts[:10],
            'bulk_counts_mean': float(np.mean(bulk_counts)),
            'a5_energy_first5': energy[:5],
            'a5_energy_mean': avg_energy,
            'a5_best_transition': a5_transition_scores(blocks[:20]),
        }
    ca_results={}
    for r in [0,1,2,3]: ca_results[f'radius_{r}']=best_linear_ca(blocks_by_res, radius=r)
    # random baseline for bulk counts: expected p=(.9)^3; for comparison exact probabilities p>=10 etc.
    p=0.9**3
    from math import comb
    binom_tail={str(k): sum(comb(12,i)*p**i*(1-p)**(12-i) for i in range(k,13)) for k in range(0,13)}
    result={
        'app_invariants': app,
        'per_constant': per_const,
        'linear_CA_F3_residue_flow': ca_results,
        'random_bulk_binomial_tail': binom_tail,
        'projector_rank': {rep:int(round(np.trace(P))) for rep,P in projectors.items()},
        'method_verdict': {
            'state_space': 'green: triads are points in 10^3, with bulk 729 and corona 271',
            'simple_flows': 'red: memory-1, LCG, local F3 cellular rules do not generate the constants',
            'a5_projector_flow': 'yellow: spectral coordinates exist and are useful, but not yet a predictive digit map',
            'next_needed': 'canonical transition on APP/TPK/kappa27 classes or a non-circular generator for the next 12-triad block',
        }
    }
    JSON_OUT.write_text(json.dumps(result,indent=2),encoding='utf-8')
    # TeX snippet
    tex=[]
    tex.append(r"\begin{tabular}{lll}\toprule")
    tex.append(r"Invariante & Valor & Lectura\\\midrule")
    tex.append(fr"$S_{{+,2}}$ & {app['S_plus_2D']} & suma APP 2D\\")
    tex.append(fr"$S_{{\times,2}}$ & {app['S_prod_2D']} & producto APP 2D\\")
    tex.append(fr"$\Delta_{{2D}}$ & {app['Delta_2D']} & defecto 2D\\")
    tex.append(fr"$S_{{+,3}}$ & {app['S_plus_3D']} & bulk aditivo APP 3D\\")
    tex.append(fr"$9^3$ & {app['bulk_9cubed']} & bulk triadico\\")
    tex.append(fr"$10^3-9^3$ & {app['corona']} & corona decimal\\")
    tex.append(fr"$54(3645+1)$ & {app['moonshine_anchor']} & ancla $J$\\")
    tex.append(r"\bottomrule\end{tabular}")
    TEX_RESULTS.write_text('\n'.join(tex),encoding='utf-8')
    print(json.dumps(result['method_verdict'], indent=2))
    print('Wrote', JSON_OUT, TEX_RESULTS)
    return result

if __name__=='__main__':
    main()
