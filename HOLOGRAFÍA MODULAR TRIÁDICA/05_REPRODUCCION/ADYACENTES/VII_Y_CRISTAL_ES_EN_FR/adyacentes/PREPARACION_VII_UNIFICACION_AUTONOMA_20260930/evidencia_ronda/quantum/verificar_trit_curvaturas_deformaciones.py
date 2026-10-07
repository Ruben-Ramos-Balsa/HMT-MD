#!/usr/bin/env python3
"""Exact focal checks of Cartan/TRIT, memory and screen-deformation identities."""
from fractions import Fraction as F


def zero(n, m=None):
    return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]


def eye(n):
    return [[F(int(j == k)) for k in range(n)] for j in range(n)]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def sub(a, b):
    return add(a, scale(-1, b))


def mul(a, b):
    return [[sum(a[j][r] * b[r][k] for r in range(len(b)))
             for k in range(len(b[0]))] for j in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def comm(a, b):
    return sub(mul(a, b), mul(b, a))


checks = 0


def check(condition, label):
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1


d = 4
eta = [-1, 1, 1, 1]


def metric(a, b):
    return eta[a] if a == b else 0


def lorentz(a, b):
    j = zero(d + 1)
    j[a][b] += eta[b]
    j[b][a] -= eta[a]
    return j


def translation(a, tau):
    p = zero(d + 1)
    p[a][d] = 1
    p[d][a] = -tau * eta[a]
    return p


for tau in (-1, 0, 1):
    ps = [translation(a, tau) for a in range(d)]
    for a in range(d):
        for b in range(d):
            check(comm(ps[a], ps[b]) == scale(-tau, lorentz(a, b)),
                  "tritic translation bracket")
            for c in range(d):
                expected = sub(scale(metric(b, c), ps[a]),
                               scale(metric(a, c), ps[b]))
                check(comm(lorentz(a, b), ps[c]) == expected,
                      "Lorentz action on translations")
    if tau:
        g = zero(d + 1)
        for a in range(d):
            g[a][a] = eta[a]
        g[d][d] = tau
        for p in ps:
            check(add(mul(transpose(p), g), mul(g, p)) == zero(d + 1),
                  "deSitter/antiDeSitter metric preservation")
    a, b, c = ps[0], ps[1], lorentz(0, 1)
    check(add(add(comm(a, comm(b, c)), comm(b, comm(c, a))),
              comm(c, comm(a, b))) == zero(d + 1), "Jacobi concrete curvature")

omega = [[F(0), F(1)], [F(-1), F(0)]]
id2 = eye(2)
regimes = [
    [[F(3, 5), F(4, 5)], [F(-4, 5), F(3, 5)]],
    [[F(1), F(2)], [F(0), F(1)]],
    [[F(5, 3), F(4, 3)], [F(4, 3), F(5, 3)]],
]
frames = [id2, [[F(2), F(0)], [F(0), F(1, 2)]], id2]
terminal = id2
memory = zero(2)
for e, b in zip(regimes, frames):
    check(mul(mul(transpose(e), omega), e) == omega, "regime symplectic")
    t = mul(b, scale(F(1, 9), add(scale(8, id2), e)))
    # D=sqrt(8)*s; avoid irrational arithmetic by retaining the exact factor8.
    s = mul(b, scale(F(1, 9), sub(e, id2)))
    check(add(mul(mul(transpose(t), omega), t),
              scale(8, mul(mul(transpose(s), omega), s))) == omega,
          "reading plus retained memory")
    sp = mul(s, terminal)
    memory = add(memory, scale(8, mul(mul(transpose(sp), omega), sp)))
    terminal = mul(t, terminal)
check(add(mul(mul(transpose(terminal), omega), terminal), memory) == omega,
      "mixed-regime full balance")

def standard(tau):
    return [[F(0), F(1)], [F(-tau), F(0)]]

check(standard(1) != standard(-1), "negative conjugacy with identity frame")
check(mul(standard(1), standard(1)) != mul(standard(-1), standard(-1)),
      "different tritic squares cannot be invertibly conjugated")

# Affine return, not a Schrodinger Hamiltonian: retain g and its increment4.
affine = [[F(1), F(0), F(4)], [F(0), F(1), F(72)], [F(0), F(0), F(1)]]
coarse = [[F(1), F(4)], [F(0), F(1)]]
p = [[F(1), F(0), F(0)], [F(0), F(0), F(1)]]
fine_power, coarse_power = eye(3), eye(2)
for n in range(1, 28):
    fine_power, coarse_power = mul(affine, fine_power), mul(coarse, coarse_power)
    check(mul(p, fine_power) == mul(coarse_power, p), "affine memory refinement")
    check(fine_power[0][2] == 4 * n and fine_power[1][2] == 72 * n,
          "full memory does not reset with phase")

# Exact screen-map defect, with a rank-reducing map.
f = [[F(1), F(0)]]
a = [[F(1), F(0)], [F(0), F(2)]]
b = [[F(0), F(1)], [F(1), F(0)]]
ap, bp = [[F(1)]], [[F(0)]]
da, db = sub(mul(f, a), mul(ap, f)), sub(mul(f, b), mul(bp, f))
lhs = sub(mul(f, comm(a, b)), mul(comm(ap, bp), f))
rhs = add(sub(mul(ap, db), mul(bp, da)), sub(mul(da, b), mul(db, a)))
check(lhs == rhs, "rank-changing bracket defect identity")
check(lhs != zero(1, 2), "negative naive quotient-bracket test")


def deriv(poly):
    return {k - 1: k * v for k, v in poly.items() if k}


def polymul(a, b):
    c = {}
    for k, x in a.items():
        for j, y in b.items():
            c[k + j] = c.get(k + j, F(0)) + x * y
    return {k: v for k, v in c.items() if v}


def polysub(a, b):
    c = a.copy()
    for k, v in b.items():
        c[k] = c.get(k, F(0)) - v
    return {k: v for k, v in c.items() if v}


n, m = {2: F(1)}, {3: F(1)}
normal_bracket = polysub(polymul(m, deriv(n)), polymul(n, deriv(m)))
check(normal_bracket == {4: F(-1)}, "Lorentz normal-lapse bracket")
check(bool(normal_bracket), "negative frozen-normal test")

print(f"PASS_TRIT_CURVATURAS_DEFORMACIONES: {checks} exact checks")
print("Scope: three Cartan sheets, retained affine memory, bracket naturality and lapse falsifiers.")
print("The affine return is not identified with the common quantum Hamiltonian.")
