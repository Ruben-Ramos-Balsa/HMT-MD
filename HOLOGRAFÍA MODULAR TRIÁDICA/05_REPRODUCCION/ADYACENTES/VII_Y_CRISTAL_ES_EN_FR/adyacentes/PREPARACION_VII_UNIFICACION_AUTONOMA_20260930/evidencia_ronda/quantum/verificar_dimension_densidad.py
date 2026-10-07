#!/usr/bin/env python3
"""Exact finite falsifiers for DIMENSION_DENSIDAD_ENTRELAZAMIENTO.md.

No numerical physical constant is supplied. The script checks positional
transport, memory reconstruction, Gram/energy refinement and metric connection.
It is not a certificate of a physical AdS/CFT duality or continuum closure.
"""
from fractions import Fraction as F
from math import factorial


def matrix(rows):
    return [[F(x) for x in r] for r in rows]


def transpose(a):
    return list(map(list, zip(*a)))


def mul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b):
    return [[x+y for x, y in zip(r, s)] for r, s in zip(a, b)]


def scale(c, a):
    return [[c*x for x in row] for row in a]


def inv2(a):
    d = a[0][0]*a[1][1]-a[0][1]*a[1][0]
    return scale(1/d, [[a[1][1], -a[0][1]], [-a[1][0], a[0][0]]])


checks = 0


def check(value, description):
    global checks
    if not value:
        raise AssertionError(description)
    checks += 1


def beta(x):
    r = [d for y in x for d in (y % 3, y // 3)]
    return (r[0]+3*r[1]+9*r[2], r[3]+3*r[4]+9*r[5])


def beta_inverse(y):
    r = [d for v in y for d in (v % 3, (v // 3) % 3, v // 9)]
    return tuple(r[2*j]+3*r[2*j+1] for j in range(3))


seen = set()
for i in range(9):
    for j in range(9):
        for k in range(9):
            x = (i, j, k)
            y = beta(x)
            check(beta_inverse(y) == x, "positional inverse")
            seen.add(y)
check(len(seen) == 729, "complete bijection")
check(beta((0, 3, 0)) != tuple((a+b) % 27 for a, b in
                              zip(beta((0, 2, 0)), beta((0, 1, 0)))),
      "negative: positional transport is not torus-additive")

K = list(map(F, [234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601]))


def shift(v, n):
    return v[n:]+v[:n]


def t3(v):
    return [(8*x+y)/9 for x, y in zip(v, shift(v, 3))]


def t3_inverse(v):
    return [(512*v[i]-64*v[(i+3) % 12]+8*v[(i+6) % 12]-v[(i+9) % 12])/455
            for i in range(12)]


# mbar denotes m/sqrt(8), keeping arithmetic rational without changing types.
m0 = [(y-x)/9 for x, y in zip(K, shift(K, 3))]
TK = t3(K)
m1 = [(y-x)/9 for x, y in zip(TK, shift(TK, 4))]
b = [-9*x for x in m0]
c = [-9*x for x in t3_inverse(m1)]
w = [c[i]-b[(i+1) % 12] for i in range(12)]
B = [sum(w[:i]) for i in range(12)]
reconstructed = [(sum(K)+sum(B))/12-x for x in B]
check(t3_inverse(t3(K)) == K, "ordered compression inverse")
check(reconstructed == K, "memory and charge recover complete K")


def nodal(lengths, densities):
    n = len(lengths)+1
    energy = [[F(0) for _ in range(n)] for _ in range(n)]
    gram = [[F(0) for _ in range(n)] for _ in range(n)]
    for j, (d, rho) in enumerate(zip(lengths, densities)):
        for a in range(2):
            for b_ in range(2):
                energy[j+a][j+b_] += F(1 if a == b_ else -1)/d
                gram[j+a][j+b_] += rho*d*F(2 if a == b_ else 1, 6)
    return energy, gram


for n in (3, 9):
    fractions = [F(j, n*(n+1)//2) for j in range(1, n+1)]
    positions = [F(0)] + [sum(fractions[:j]) for j in range(1, n+1)]
    E = [[1-t, t] for t in positions]
    for d in [x/sum(K) for x in K]:
        nu = F(7, 5)
        rho = nu/d
        Lf, Qf = nodal([d*x for x in fractions], [rho]*n)
        Lc, Qc = nodal([d], [rho])
        check(mul(mul(transpose(E), Lf), E) == Lc, "energy naturality")
        check(mul(mul(transpose(E), Qf), E) == Qc, "Gram naturality")
        check(Qc == scale(nu/F(6), matrix([[2, 1], [1, 2]])),
              "conserved weight despite changing density and length")
        check(sum(rho*d*x for x in fractions) == nu, "weight conservation")

# Metric connection test, with positive S and arbitrary symmetric derivative.
S = matrix([[2, 1], [1, 3]])
dS = matrix([[1, 2], [2, -1]])
L = matrix([[3, -1], [-1, 2]])
Sinv = inv2(S)
Q = mul(S, S)
dQ = add(mul(dS, S), mul(S, dS))
A = mul(Sinv, dS)
check(add(mul(transpose(A), Q), mul(Q, A)) == dQ,
      "metric-compatible connection")
H = mul(mul(Sinv, L), Sinv)
check(H == transpose(H), "normalized generator is symmetric")
check(dQ != matrix([[0, 0], [0, 0]]), "negative: dropping connection changes norm")

# Volterra memory in an exactly solvable two-mode reduction.
# w is a symbolic rational frequency used for the algebraic test only.
wfreq = F(3, 2)
coef = [F(0)]*12
for n in range(6):
    coef[2*n] = (-1)**n*wfreq**(2*n)/factorial(2*n)
check(coef[0] == 1 and coef[1] == 0, "initial retained mode")
for n in range(1, 11):
    check((n+1)*coef[n+1] == -wfreq**2*coef[n-1]/n,
          "causal memory integral Taylor identity")
check(coef[2] != 0, "negative: retained instantaneous block alone misses dynamics")

print(f"PASS_FOCAL_DIMENSION_DENSIDAD: {checks} exact checks")
print("Scope: finite algebraic falsifiers; proofs of temporal transport and elimination are in the note.")
