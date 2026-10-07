#!/usr/bin/env python3
"""Testigos racionales exactos; no evalúa ni genera constantes HMT."""
from fractions import Fraction as F
from itertools import product


def mat(rows):
    return [[F(x) for x in row] for row in rows]


def tr(a):
    return [list(x) for x in zip(*a)]


def mul(a, b):
    return [[sum(x * y for x, y in zip(row, col))
             for col in zip(*b)] for row in a]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(s, a):
    return [[s * x for x in row] for row in a]


def inv2(a):
    d = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    assert d != 0
    return scale(1 / d, [[a[1][1], -a[0][1]], [-a[1][0], a[0][0]]])


def kron(a, b):
    return [[x * y for x in ar for y in br] for ar in a for br in b]


def schur4(a):
    aa = [r[:2] for r in a[:2]]
    bb = [r[2:] for r in a[:2]]
    cc = [r[2:] for r in a[2:]]
    return add(aa, scale(-1, mul(mul(bb, inv2(cc)), tr(bb))))


checks = 0


def eq(a, b):
    global checks
    assert a == b, (a, b)
    checks += 1


ident = mat([[1, 0], [0, 1]])
o = mat([[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]])
eq(mul(o, tr(o)), ident)
for p, f, length, c, hbar, yp, a, b in product(
        [F(2), F(7, 3)], [F(3, 2)], [F(5), F(9, 2)],
        [F(3), F(5, 2)], [F(2), F(11, 3)],
        [F(2, 3), F(4)], [F(1), F(3)], [F(1), F(2)]):
    wa, wv = p**4 / (p**4 + f**5), f**5 / (p**4 + f**5)
    eq(wa + wv, F(1))
    rav, ravj = p / f**2, f / p**2
    eq(wa, rav**2 / (rav**2 + ravj))
    q, g = hbar * c / length, c**3 * length**2 / hbar
    mp, ep = hbar * yp / (c * length), q * yp
    lp = length / yp
    y = mat([[a*a + 1, a*b], [a*b, b*b + 2]])
    w = mul(mul(o, mat([[wa, 0], [0, wv]])), tr(o))
    ham, mass, radius = scale(q, y), scale(q / c**2, y), scale(length, y)
    response = scale(yp, kron(y, w))
    eq(response, scale(ep / q**2, kron(ham, w)))
    eq(response, scale(1 / lp, kron(radius, w)))
    eq(response, scale(g * mp / (hbar * c), kron(mass, w)))
    eq(g * mp * mp / (hbar * c), yp**2)
    yef = y[0][0] - y[0][1]**2 / y[1][1]
    assert yef > 0
    eq(schur4(response), scale(yp * yef, w))
    # Resolvente de memoria exacto en ambos sectores; z<0 evita polos.
    z = F(-3, 2)
    ky = y[0][0] - z - y[0][1]**2 / (y[1][1] - z)
    for ws in (wa, wv):
        s = yp * ws
        ks = s*y[0][0] - s*z - (s*y[0][1])**2 / (s*y[1][1] - s*z)
        eq(ks, s * ky)
    # Conjugación del carácter; no se altera el espacio de respuesta.
    yt = mul(mul(o, y), tr(o))
    transport = kron(o, ident)
    eq(scale(yp, kron(yt, w)), mul(mul(transport, response), tr(transport)))
    # Inscripción isométrica efectiva Y'K=KY.
    k = mat([[1, 0], [0, 1], [0, 0], [0, 0]])
    yprime = mat([[y[0][0], y[0][1], 0, 0],
                 [y[1][0], y[1][1], 0, 0],
                 [0, 0, 2, 0], [0, 0, 0, 3]])
    jk = kron(k, ident)
    eq(mul(scale(yp, kron(yprime, w)), jk), mul(jk, response))
    # Reescala conjunta de la sección de acción, con caracteres fijos.
    rho = F(7, 4)
    eq((g / rho) * (rho * mp)**2 / ((rho * hbar) * c), yp**2)
    eq((rho * ep)**2 / (rho * q)**2, yp**2)
    # Falsador: borrar el bloque de memoria modifica la respuesta efectiva.
    assert yef != y[0][0]
    checks += 1

print(f"PASS_AUTOINERCIA_ACOPLAMIENTO checks={checks} exact=rational global_flatness_claim=false")
