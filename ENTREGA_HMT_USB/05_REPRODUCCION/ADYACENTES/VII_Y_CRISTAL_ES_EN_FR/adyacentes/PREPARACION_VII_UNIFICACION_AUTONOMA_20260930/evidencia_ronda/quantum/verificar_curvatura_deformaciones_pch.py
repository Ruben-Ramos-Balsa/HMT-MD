#!/usr/bin/env python3
"""Variaciones de gráfica Dirac a f=0, exactamente sobre Q(i)[x,y,z].

Verifica el generador obtenido del flujo de la acción, no sólo el corchete
congelado. Los racionales son unidades de control, no constantes físicas.
"""
from dataclasses import dataclass
from fractions import Fraction as F


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

    def __mul__(self, x):
        x = self.c(x)
        return G(self.re*x.re-self.im*x.im, self.re*x.im+self.im*x.re)

    __rmul__ = __mul__


Z, I = G(), G(F(0), F(1))
ONE = {(0, 0, 0): G(F(1))}


def clean(p):
    return {k: G.c(v) for k, v in p.items() if G.c(v) != Z}


def ps(p, c):
    return clean({k: G.c(c)*v for k, v in p.items()})


def pa(p, q):
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, Z)+v
    return clean(r)


def pm(p, q):
    r = {}
    for k, v in p.items():
        for l, w in q.items():
            t = tuple(a+b for a, b in zip(k, l))
            r[t] = r.get(t, Z)+v*w
    return clean(r)


def pd(p, j):
    r = {}
    for k, v in p.items():
        if k[j]:
            t = list(k)
            t[j] -= 1
            r[tuple(t)] = v*k[j]
    return clean(r)


def ms(a, c):
    return tuple(tuple(G.c(c)*x for x in r) for r in a)


def mm(a, b):
    return tuple(tuple(sum((a[i][k]*b[k][j] for k in range(len(b))), Z)
                       for j in range(len(b[0]))) for i in range(len(a)))


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
    return tuple(sum_poly(ps(p, c) for c, p in zip(row, f)) for row in a)


def sum_poly(items):
    result = {}
    for p in items:
        result = pa(result, p)
    return result


id2, id4 = ident(2), ident(4)
j, r, z = ((0, -1), (1, 0)), ((0, 1), (1, 0)), ((1, 0), (0, -1))
gs = (kron(j, id2), kron(r, id2), kron(z, r), kron(z, z))
alpha = tuple(ms(mm(gs[0], g), -1) for g in gs[1:])
beta = ms(gs[0], -I)
chir = ms(mm(mm(mm(gs[0], gs[1]), gs[2]), gs[3]), I)
HBAR, C = F(3, 2), F(4, 5)
zero = ({}, {}, {}, {})
x, y, zz = (clean({k: 1}) for k in ((1, 0, 0), (0, 1, 0), (0, 0, 1)))


def agrad(n, f):
    out = zero
    for k in range(3):
        out = va(out, vp(pd(n, k), mv(alpha[k], f)))
    return out


def potential(f, terms):
    out = zero
    for p, matrix in terms:
        out = va(out, vp(p, mv(matrix, f)))
    return out


def h(f, terms):
    out = potential(f, terms)
    for k in range(3):
        out = va(out, vs(mv(alpha[k], vd(f, k)), -I*HBAR*C))
    return out


def hn(n, f, terms):
    return vs(va(vp(n, h(f, terms)), h(vp(n, f), terms)), F(1, 2))


def delta(n, m, f, terms, dot_terms=(), include_connection=True):
    # delta_N(M R H R), with R_N = c alpha(dN)/2.
    out = vp(m, vs(va(agrad(n, h(f, terms)), h(agrad(n, f), terms)), C/2))
    out = va(out, vp(pm(n, m), potential(f, dot_terms)))
    if include_connection:
        # i hbar (S_NM + S_M R_N): all matrix orders are retained.
        nm, mn = agrad(n, agrad(m, f)), agrad(m, agrad(n, f))
        second = va(vs(va(nm, mn), -C*C/8), vs(mn, -C*C/4))
        out = va(out, vs(second, I*HBAR))
    return out


def curvature(n, m, f, terms, dot_terms=(), include_connection=True):
    skew = va(delta(n, m, f, terms, dot_terms, include_connection),
              vs(delta(m, n, f, terms, dot_terms, include_connection), -1))
    bracket = va(hn(n, hn(m, f, terms), terms),
                 vs(hn(m, hn(n, f, terms), terms), -1))
    return va(skew, vs(bracket, I*(1/HBAR)))


checks = 0


def check(test, label):
    global checks
    if not test:
        raise AssertionError(label)
    checks += 1


lapses = [ONE, x, y, pa(ONE, pm(x, zz)), pa(pm(y, y), zz)]
vectors = [(ONE, {}, {}, {}), (pa(x, ps(y, I)), zz, pm(x, y), ONE)]
potentials = [[], [(pa(ONE, pm(x, y)), beta)],
              [(pa(ONE, y), id4), (pa(x, zz), alpha[0]), (pm(x, y), beta)]]
dot_potential = [(pa(ONE, x), chir), (y, id4)]

for terms in potentials:
    for n in lapses:
        for m in lapses:
            for f in vectors:
                check(curvature(n, m, f, terms, dot_potential) == zero,
                      "F_NM=0 con variación completa de gráfica y potencial")

# The spin part of S_M R_N is essential even at a flat reference slice.
bad = curvature(x, y, vectors[0], [], include_connection=False)
expected = vs(va(agrad(x, agrad(y, vectors[0])),
                 vs(agrad(y, agrad(x, vectors[0])), -1)), -I*(HBAR*C*C/4))
check(bad == expected and bad != zero, "omitir conexión de densidad deja rotación spin")

# A general Hermitian scalar potential contributes, but its variation cancels it.
f = vectors[0]
v = [(pa(ONE, y), id4)]
skew_v = va(delta(x, y, f, v), vs(delta(y, x, f, v), -1))
skew_0 = va(delta(x, y, f, []), vs(delta(y, x, f, []), -1))
check(va(skew_v, vs(skew_0, -1)) != zero, "potencial temporal no se omite")
check(curvature(x, y, f, v) == zero, "potencial temporal se cancela en F total Dirac")

# Time dependence is symmetric MN dot(V), not an unaccounted antisymmetric term.
check(curvature(x, y, vectors[1], potentials[-1], dot_potential)
      == curvature(x, y, vectors[1], potentials[-1]), "dot V simétrico cancela")

print(f"PASS_CURVATURA_DEFORMACIONES_DIRAC_PCH: {checks} controles exactos Q(i)[x,y,z]")
