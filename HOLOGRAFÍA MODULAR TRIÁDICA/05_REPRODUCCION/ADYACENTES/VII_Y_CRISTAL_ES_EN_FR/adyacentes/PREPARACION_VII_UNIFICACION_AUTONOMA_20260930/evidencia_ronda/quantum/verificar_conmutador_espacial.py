#!/usr/bin/env python3
"""Jets polinómicos exactos en Q(i)[x,y,z]; no certifica dominios analíticos.

Reproduce el conmutador espacial de la nota contigua con el módulo Clifford
del propietario VIII/33. Los racionales de prueba no son entradas físicas.
"""
from dataclasses import dataclass
from fractions import Fraction as F
import json


@dataclass(frozen=True)
class G:
    re: F = F(0)
    im: F = F(0)

    @staticmethod
    def c(x):
        return x if isinstance(x, G) else G(F(x))

    def __add__(self, x):
        x = self.c(x)
        return G(self.re+x.re, self.im+x.im)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.re, -self.im)

    def __sub__(self, x):
        return self+-self.c(x)

    def __rsub__(self, x):
        return self.c(x)+-self

    def __mul__(self, x):
        x = self.c(x)
        return G(self.re*x.re-self.im*x.im, self.re*x.im+self.im*x.re)

    __rmul__ = __mul__


Z, I = G(), G(F(0), F(1))
ONE = {(0, 0, 0): G(F(1))}


def pclean(p):
    return {k: G.c(v) for k, v in p.items() if G.c(v) != Z}


def ps(p, c):
    return pclean({k: G.c(c)*v for k, v in p.items()})


def pa(p, q):
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, Z)+v
    return pclean(r)


def pm(p, q):
    r = {}
    for k, v in p.items():
        for l, w in q.items():
            t = tuple(a+b for a, b in zip(k, l))
            r[t] = r.get(t, Z)+v*w
    return pclean(r)


def pd(p, j):
    r = {}
    for k, v in p.items():
        if k[j]:
            t = list(k)
            t[j] -= 1
            r[tuple(t)] = v*k[j]
    return pclean(r)


def ms(a, c):
    return tuple(tuple(G.c(c)*x for x in r) for r in a)


def mm(a, b):
    return tuple(tuple(sum((a[i][k]*b[k][j] for k in range(len(b))), Z)
                       for j in range(len(b[0]))) for i in range(len(a)))


def ma(a, b):
    return tuple(tuple(x+y for x, y in zip(r, s)) for r, s in zip(a, b))


def kron(a, b):
    return tuple(tuple(G.c(x)*y for x in r for y in s) for r in a for s in b)


def ident(n):
    return tuple(tuple(G.c(int(i == j)) for j in range(n)) for i in range(n))


def va(a, b):
    return tuple(pa(x, y) for x, y in zip(a, b))


def vs(a, c):
    return tuple(ps(x, c) for x in a)


def vp(p, a):
    return tuple(pm(p, x) for x in a)


def vd(a, j):
    return tuple(pd(x, j) for x in a)


def mv(a, f):
    r = []
    for row in a:
        p = {}
        for x, y in zip(row, f):
            p = pa(p, ps(y, x))
        r.append(p)
    return tuple(r)


id2, id4 = ident(2), ident(4)
j = ((0, -1), (1, 0))
r = ((0, 1), (1, 0))
z = ((1, 0), (0, -1))
gs = (kron(j, id2), kron(r, id2), kron(z, r), kron(z, z))
alpha = tuple(ms(mm(gs[0], g), -1) for g in gs[1:])
beta = ms(gs[0], -I)
chir = ms(mm(mm(mm(gs[0], gs[1]), gs[2]), gs[3]), I)
a = F(3, 2)
zero_v = ({}, {}, {}, {})
zero_m = ms(id4, 0)
checks = 0


def check(test, label):
    global checks
    if not test:
        raise AssertionError(label)
    checks += 1


def cgrad(n, f):
    out = zero_v
    for k in range(3):
        out = va(out, vp(pd(n, k), mv(alpha[k], f)))
    return out


def h(f, mass, potential=None):
    out = zero_v
    for k in range(3):
        out = va(out, vs(mv(alpha[k], vd(f, k)), -I*a))
    out = va(out, vp(mass, mv(beta, f)))
    return va(out, vp(potential or {}, f))


def hn(n, f, mass, potential=None):
    return vs(va(vp(n, h(f, mass, potential)),
                 h(vp(n, f), mass, potential)), F(1, 2))


def rhs(n, m, f):
    out, div = zero_v, {}
    for k in range(3):
        v = pa(pm(n, pd(m, k)), ps(pm(m, pd(n, k)), -1))
        out = va(out, vp(v, vd(f, k)))
        div = pa(div, pd(v, k))
    out = va(out, vs(vp(div, f), F(1, 2)))
    spin = va(cgrad(n, cgrad(m, f)), vs(cgrad(m, cgrad(n, f)), -1))
    return vs(va(out, vs(spin, F(1, 4))), -a*a)


for u in range(3):
    for v in range(3):
        check(ma(mm(alpha[u], alpha[v]), mm(alpha[v], alpha[u]))
              == ms(id4, 2*int(u == v)), 'Clifford spatial')
    check(ma(mm(beta, alpha[u]), mm(alpha[u], beta)) == zero_m,
          'Mass anticommutes with spatial Clifford')
    check(mm(chir, alpha[u]) == mm(alpha[u], chir), 'Chirality kinetic')
check(ma(mm(chir, beta), mm(beta, chir)) == zero_m, 'Mass flips chirality')
check(mm(chir, chir) == id4, 'Chirality squares to identity')

x, y, zz = (pclean({k: 1}) for k in ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
lapses = [ONE, x, y, pa(ONE, pm(x, zz)), pa(pm(y, y), zz),
          pa(pm(x, y), ps(pm(zz, zz), F(1, 2)))]
masses = [{}, pa(ONE, pm(x, y))]
vectors = [(ONE, {}, {}, {}), (pa(x, ps(y, I)), zz, pm(x, y), ONE)]
for mass in masses:
    for n in lapses:
        for m in lapses:
            for f in vectors:
                actual = va(hn(n, hn(m, f, mass), mass),
                            vs(hn(m, hn(n, f, mass), mass), -1))
                check(actual == rhs(n, m, f), 'Arbitrary lapse commutator')
                check(mv(chir, rhs(n, m, f)) == rhs(n, m, mv(chir, f)),
                      'Bracket preserves chirality, including variable mass')

# A scalar potential is not silently classified as an anticommuting mass.
for potential in [ONE, pa(ONE, y)]:
    n, m, mass, f = x, y, masses[1], vectors[0]
    actual = va(hn(n, hn(m, f, mass, potential), mass, potential),
                vs(hn(m, hn(n, f, mass, potential), mass, potential), -1))
    expected_defect = vs(vp(potential,
        va(vp(n, cgrad(m, f)), vs(vp(m, cgrad(n, f)), -1))), -I*a)
    check(actual == va(rhs(n, m, f), expected_defect), 'Scalar potential defect')
    check(expected_defect != zero_v, 'Negative control is nonzero')

print(json.dumps({'status': 'PASS_CONMUTADOR_ESPACIAL_ESPINORIAL',
                  'exact_checks': checks, 'arithmetic': 'Q(i)[x,y,z]',
                  'global_four_interaction_closure': False}, ensure_ascii=False))
