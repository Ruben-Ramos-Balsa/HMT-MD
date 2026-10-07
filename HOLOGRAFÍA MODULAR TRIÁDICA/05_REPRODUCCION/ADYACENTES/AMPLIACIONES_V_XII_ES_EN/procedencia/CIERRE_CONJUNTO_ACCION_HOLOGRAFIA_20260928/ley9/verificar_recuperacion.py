#!/usr/bin/env python3
"""Finite recovery identities; exact rational and separate decimal checks."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import hashlib
import json
import mpmath as mp

ROOT = Path(__file__).resolve().parent
PREV = ROOT.parents[1] / 'BEKENSTEIN_HAWKING_COMPOSICION_HMT_20260928/DELTA_02_HOLOGRAFIA/RESULTADOS_INFORMACION_INTRAFIBRA.json'
checks = []

def check(name, condition, kind):
    checks.append(dict(name=name, passed=bool(condition), kind=kind))
    if not condition:
        raise AssertionError(name)

def push(p, q):
    out = defaultdict(lambda: F(0))
    for x, v in p.items():
        out[q(x)] += v
    return dict(out)

def restore(r, pi, q):
    marginal = push(pi, q)
    return {x: r[q(x)]*v/marginal[q(x)] for x, v in pi.items()}

def num(x):
    return mp.mpf(x.numerator)/x.denominator if isinstance(x, F) else mp.mpf(x)

def kl(p, q):
    return mp.fsum(num(v)*mp.log(num(v)/num(q[x])) for x, v in p.items() if v)

mp.mp.dps = 90
tol = mp.mpf('1e-80')
omega = list(product(range(3), repeat=4))
weights = {x: F(2, 3)**sum(x[:2])*F(3, 5)**sum(x[2:]) for x in omega}
z = sum(weights.values())
pi = {x: w/z for x, w in weights.items()}
arbitrary = {x: F(i+1) for i, x in enumerate(omega)}
za = sum(arbitrary.values())
p = {x: w/za for x, w in arbitrary.items()}
swapped = {x: pi[x[2:]+x[:2]] for x in omega}
qs = {'N': lambda x: sum(x),
      'NM': lambda x: (sum(x), sum(x[:2])-sum(x[2:])),
      'M': lambda x: sum(x[:2])-sum(x[2:]),
      'parity': lambda x: sum(x) % 2}

for qname, q in qs.items():
    for pname, prob in [('arbitrary', p), ('swap', swapped)]:
        marginal = push(prob, q)
        piq = push(pi, q)
        rec = restore(marginal, pi, q)
        prefix = f'{qname}:{pname}:'
        check(prefix+'marginal_recovery', push(rec, q) == marginal, 'rational_exact')
        check(prefix+'normalization', sum(rec.values()) == 1, 'rational_exact')
        check(prefix+'likelihood_factorization', all(prob[x]/pi[x] == marginal[q(x)]/piq[q(x)]*prob[x]/rec[x] for x in omega), 'rational_exact')
        check(prefix+'relative_entropy_chain', abs(kl(prob, pi)-kl(marginal, piq)-kl(prob, rec)) < tol, 'decimal_90')
        # H=-log pi, epsilon=1, Z=1: exact stated Gibbs realization.
        energy = lambda distribution: -mp.fsum(num(v)*mp.log(num(pi[x])) for x, v in distribution.items())
        entropy = lambda distribution: -mp.fsum(num(v)*mp.log(num(v)) for v in distribution.values() if v)
        check(prefix+'free_energy_difference', abs(energy(prob)-entropy(prob)-energy(rec)+entropy(rec)-kl(prob, rec)) < tol, 'decimal_90')
        reduced_energy = -mp.fsum(num(v)*mp.log(num(piq[y])) for y, v in marginal.items())
        check(prefix+'boundary_potential', abs(energy(rec)-entropy(rec)-reduced_energy+entropy(marginal)) < tol, 'decimal_90')

check('swap_identical_N_distribution', push(pi, qs['N']) == push(swapped, qs['N']), 'rational_exact')
check('Gibbs_N_restorer_returns_pi', restore(push(swapped, qs['N']), pi, qs['N']) == pi, 'rational_exact')
for name in ['M', 'NM']:
    check(name+'_recovers_swapped', restore(push(swapped, qs[name]), pi, qs[name]) == swapped, 'rational_exact')
check('N_does_not_recover_swapped', pi != swapped, 'rational_exact')

source = json.loads(PREV.read_text())
d_text = source['evaluation']['d']
d = mp.mpf(d_text)
g = [1]
for _ in range(18):
    next_g = [0]*(len(g)+2)
    for i, v in enumerate(g):
        for j in range(3):
            next_g[i+j] += v
    g = next_g
check('trinomial_total', sum(g) == 3**18, 'integer_exact')
Z = (1+mp.exp(-3*d)+mp.exp(-6*d))**18*(1+mp.exp(-4*d)+mp.exp(-8*d))**18
rho = {(x,y): g[x]*g[y]*mp.exp(-d*(3*x+4*y))/Z for x in range(37) for y in range(37)}
sigma = {(x,y): rho[y,x] for x,y in rho}
rN = defaultdict(lambda: mp.mpf(0))
sN = defaultdict(lambda: mp.mpf(0))
for (x,y), v in rho.items():
    rN[x+y] += v
    sN[x+y] += sigma[x,y]
check('thermal_N_equal', max(abs(rN[n]-sN[n]) for n in rN) < tol, 'decimal_90')
J = kl(sigma, rho)
mu = lambda a: (mp.exp(-a)+2*mp.exp(-2*a))/(1+mp.exp(-a)+mp.exp(-2*a))
J_formula = 18*d*(mu(3*d)-mu(4*d))
check('J_formula', abs(J-J_formula) < tol, 'decimal_90')
check('J_prior_continuity', abs(J-mp.mpf(source['evaluation']['totals']['J'])) < mp.mpf('1e-60'), 'decimal_90')
recN = {xy: sN[sum(xy)]*rho[xy]/rN[sum(xy)] for xy in rho}
check('all_J_conditional', abs(kl(sigma, recN)-J) < tol, 'decimal_90')

u, theta = 7*d/2, d/2
potentials = {}
for n in range(73):
    fiber = [(x,n-x) for x in range(37) if 0 <= n-x <= 36]
    Zplus = mp.fsum(g[x]*g[y]*mp.exp(theta*(x-y)) for x,y in fiber)
    Zminus = mp.fsum(g[x]*g[y]*mp.exp(-theta*(x-y)) for x,y in fiber)
    check(f'even_potential_fiber_{n}', abs(Zplus-Zminus)/Zplus < tol, 'decimal_90')
    potentials[str(n)] = mp.nstr(u*n-mp.log(Zplus), 45)

tv = mp.fsum(abs(sigma[x]-rho[x]) for x in rho)/2
check('detector_Pinsker_bound', tv**2 <= J/2, 'decimal_90')
result = dict(status='PASS_RECOVERY_FREE_ENERGY_FINITE',
              source=dict(path=str(PREV), sha256=hashlib.sha256(PREV.read_bytes()).hexdigest(), d=d_text),
              assumptions='Finite diagonal thermal realization, inherited d; fixed H and T. Rational arbitrary distributions test identities, not constant generation.',
              checks=checks, checks_count=len(checks),
              exact_count=sum(c['kind'].endswith('exact') for c in checks),
              decimal_count=sum(c['kind']=='decimal_90' for c in checks),
              numerical_policy='90-digit evaluation, not interval certification; proof is in RECUPERACION_Y_ENERGIA_LIBRE.md.',
              J=mp.nstr(J,65), TV=mp.nstr(tv,65), H_N_over_epsilon=potentials)
(ROOT/'RESULTADOS_RECUPERACION.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(result['status'], len(checks), 'checks; J=',mp.nstr(J,30))
