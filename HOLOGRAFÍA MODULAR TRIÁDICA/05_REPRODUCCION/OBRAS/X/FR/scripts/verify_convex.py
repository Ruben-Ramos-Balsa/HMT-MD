#!/usr/bin/env python3
"""Exact exponential-polynomial checks for the K-directed convex potential.

Finite algebra checks supplement, and do not replace, the all-real-parameter
proofs in appendices/convex_refinement.tex. No target values are inputs.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import runpy

N = runpy.run_path(str(Path(__file__).with_name('verify_network_cluster.py')))
add, mul, scale, sign = (N[x] for x in ('qadd', 'qmul', 'qscale', 'qsign'))
zero = (F(0), F(0))
checks = 0

def require(ok, label):
    global checks
    if not ok:
        raise ArithmeticError(label)
    checks += 1

def accumulate(p, exponent, coefficient):
    p[exponent] = add(p.get(exponent, zero), coefficient)
    if p[exponent] == zero:
        del p[exponent]

def product(p, q):
    ans = {}
    for a, ca in p.items():
        for b, cb in q.items():
            accumulate(ans, add(a, b), mul(ca, cb))
    return ans

def derivative(p):
    return {u: mul(c, u) for u, c in p.items() if mul(c, u) != zero}

k = N['recover_k']()
u = N['recover_direction'](k)
d = [F(x, sum(k)) for x in k]
z = {}
for w, velocity in zip(d, u):
    accumulate(z, velocity, (w, F(0)))
dz, ddz = derivative(z), derivative(derivative(z))
left = product(z, ddz)
for exp, coef in product(dz, dz).items():
    accumulate(left, exp, scale(coef, -1))
right = {}
for i in range(12):
    for j in range(i+1, 12):
        diff = add(u[i], scale(u[j], -1))
        coef = scale(mul(diff, diff), d[i]*d[j])
        require(sign(coef) >= 0, 'nonnegative variance coefficient')
        accumulate(right, add(u[i], u[j]), coef)
require(left == right, 'Z Zsecond - Zfirst squared identity')
require(any(sign(c) > 0 for c in right.values()), 'strict variance')
for b in (2, 3, 9, 10):
    for depth in (1, 2):
        refined = {}
        for w, velocity in zip(d, u):
            for _ in range(b**depth):
                accumulate(refined, velocity, (w/F(b**depth), F(0)))
        require(refined == z, f'partition invariance B={b},depth={depth}')
        require(derivative(refined) == dz, 'first moment')
        require(derivative(derivative(refined)) == ddz, 'second moment')
require(sum(d) == 1, 'normalization')
require(N['qsum'](u) == zero, 'direction mean over positions')
print(json.dumps({'result':'PASS_K_CONVEX_REFINEMENT_EXACT',
                  'checks':checks, 'arithmetic':'Q(sqrt(5))',
                  'scope':'finite exponential-polynomial identities; analytic proof in text'},
                 ensure_ascii=False))
