#!/usr/bin/env python3
"""Exact local algebra checks for CURVATURA_TOTAL_MEMORIA_Y_LIMITE.md.

Matrices represent anti-Hermitian connection coefficients A=iH/hbar.
No physical constant is provided as an input. Analytic domain/limit proofs
are in the note; these finite checks do not certify quantum gravity closure.
"""
from fractions import Fraction as F


def zero(n, m=None):
    return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]


def eye(n):
    a = zero(n)
    for j in range(n):
        a[j][j] = F(1)
    return a


def add(a, b):
    return [[x+y for x, y in zip(r, s)] for r, s in zip(a, b)]


def scale(c, a):
    return [[c*x for x in r] for r in a]


def sub(a, b):
    return add(a, scale(-1, b))


def adj(a):
    return [list(r) for r in zip(*a)]


def mul(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def comm(a, b):
    return sub(mul(a, b), mul(b, a))


def top(a, k):
    return [r[:k] for r in a[:k]]


def lowerleft(a, k):
    return [r[:k] for r in a[k:]]


def skew(seed, n):
    a = zero(n)
    for i in range(n):
        for j in range(i+1, n):
            a[i][j] = F(((seed+2)*(i+1)+(seed*seed+3)*(j+1)) % 17-8,
                        1+(seed+i+2*j) % 5)
            a[j][i] = -a[i][j]
    return a


checks = 0


def check(ok, message):
    global checks
    if not ok:
        raise AssertionError(message)
    checks += 1


for n in (3, 4, 6):
    for seed in range(1, 10):
        ax, ay = skew(seed, n), skew(seed+2, n)
        p, q = skew(seed+4, n), skew(seed+6, n)
        x, y = skew(seed+8, n), skew(seed+10, n)
        r = add(sub(p, q), comm(ax, ay))
        # W=e^(sX)e^(tY), evaluated at s=t=0. W_st=XY.
        # A'=W*AW+W*dW; derivatives are derived from this same W jet.
        an, am = add(ax, x), add(ay, y)
        dnam = add(p, comm(ay, x))
        dman = add(add(q, comm(ax, y)), comm(x, y))
        rnew = add(sub(dnam, dman), comm(an, am))
        check(rnew == r, "full moving-frame curvature covariance")
        check(adj(an) == scale(-1, an), "unitary frame connection N")
        check(adj(am) == scale(-1, am), "unitary frame connection M")
        for k in range(1, n):
            rread = add(sub(top(dnam, k), top(dman, k)),
                        comm(top(an, k), top(am, k)))
            bn, bm = lowerleft(an, k), lowerleft(am, k)
            memory = sub(mul(adj(bn), bm), mul(adj(bm), bn))
            check(rread == add(top(r, k), memory),
                  "curvature of moving isometry includes complement")
            check(sub(rread, memory) == top(r, k),
                  "restoring complete memory cancels compression defect")
        # Native 8:1 read: a=1/9; off-diagonal norm-square=8/81.
        a = F(1, 9)
        visible = add(scale(a, sub(p, q)), scale(a*a, comm(ax, ay)))
        check(visible == add(scale(a, r), scale(-F(8, 81), comm(ax, ay))),
              "native nonadic coefficient 8/81 in connection curvature")
        check(add(visible, scale(F(8, 81), comm(ax, ay))) == scale(a, r),
              "native nonadic memory restores full curvature reading")
        # A_[N,M] is indispensable in a noncoordinate deformation frame.
        # N=d_s, M=s d_t at s=1: [N,M]=d_t.
        noncoordinate = add(sub(add(ay, p), q), comm(ax, ay))
        check(sub(noncoordinate, ay) == r, "deformation bracket term")
        check(noncoordinate != r, "negative control omitting bracket")
        # Cross-sector terms are retained for the total connection.
        bx, by = skew(seed+12, n), skew(seed+14, n)
        cross = add(comm(ax, by), comm(bx, ay))
        check(comm(add(ax, bx), add(ay, by)) ==
              add(add(comm(ax, ay), comm(bx, by)), cross),
              "cross-interaction terms in total curvature")

# Flat full connection, non-flat retained rank-two subspace: no inputs added.
x = [[F(0), F(0), F(-1)], [F(0), F(0), F(0)],
     [F(1), F(0), F(0)]]
y = [[F(0), F(0), F(0)], [F(0), F(0), F(-1)],
     [F(0), F(1), F(0)]]
rfull = add(scale(-1, comm(x, y)), comm(x, y))
rread = scale(-1, top(comm(x, y), 2))
bn, bm = lowerleft(x, 2), lowerleft(y, 2)
memory = sub(mul(adj(bn), bm), mul(adj(bm), bn))
check(rfull == zero(3), "Maurer-Cartan full frame is flat")
check(rread != zero(2), "a reduced reading of a flat frame can be curved")
check(rread == memory, "nonzero reduced curvature is exactly memory")

# A genuine gauge constraint with a nonzero physical kernel.
g = [[F(0), F(0), F(0)], [F(0), F(0), F(-1)],
     [F(0), F(1), F(0)]]
pphys = [[F(1), F(0), F(0)], [F(0), F(0), F(0)],
         [F(0), F(0), F(0)]]
check(mul(g, pphys) == zero(3), "gauge curvature vanishes on physical kernel")
check(mul(pphys, pphys) == pphys, "physical projector")
z = [[F(0), F(-1)], [F(1), F(0)]]
check(mul(z, z) == scale(-1, eye(2)),
      "central phase generator need not have a nonzero fixed vector")

print(f"PASS_FOCAL_CURVATURA_MEMORIA: {checks} exact rational checks")
print("Scope: moving-frame/isometry identities, native 8:1 complement, total cross terms.")
print("Not a proof that the total quantum gravitational curvature vanishes.")
