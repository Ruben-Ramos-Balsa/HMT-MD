#!/usr/bin/env python3
"""Control focal exacto en Q(i); no certifica toda la teoría física."""
from fractions import Fraction as F
from dataclasses import dataclass
import json


@dataclass(frozen=True)
class G:
    a: F = F(0)
    b: F = F(0)

    def __add__(self, other):
        other = other if isinstance(other, G) else G(F(other))
        return G(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        other = other if isinstance(other, G) else G(F(other))
        return G(self.a * other.a - self.b * other.b,
                 self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def conj(self):
        return G(self.a, -self.b)


zero, one, ii = G(), G(F(1)), G(F(0), F(1))
I = ((one, zero), (zero, one))
Z = ((zero, zero), (zero, zero))
S = ((one, zero), (zero, -one))
J = ((zero, one), (-one, zero))


def add(A, B):
    return tuple(tuple(A[r][c] + B[r][c] for c in range(2)) for r in range(2))


def scale(z, A):
    return tuple(tuple(z * x for x in row) for row in A)


def mul(A, B):
    return tuple(tuple(sum((A[r][k] * B[k][c] for k in range(2)), zero)
                       for c in range(2)) for r in range(2))


def adj(A):
    return tuple(tuple(A[c][r].conj() for c in range(2)) for r in range(2))


def tr(A):
    return A[0][0] + A[1][1]


def sigma(v):
    out = Z
    for x, A in zip(v, SIGMA):
        out = add(out, scale(x, A))
    return out


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def cross(x, y):
    return (x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2], x[0]*y[1]-x[1]*y[0])


checks = []


def check(name, ok):
    if not ok:
        raise AssertionError(name)
    checks.append(name)


check("S_squared", mul(S, S) == I)
check("J_squared", mul(J, J) == scale(-1, I))
check("SJ_anticommutation", add(mul(S, J), mul(J, S)) == Z)
SIGMA = (mul(S, J), scale(-ii, J), S)
for a in range(3):
    check(f"hermitian_{a}", adj(SIGMA[a]) == SIGMA[a])
    check(f"traceless_{a}", tr(SIGMA[a]) == zero)
    for b in range(3):
        expected = I if a == b else Z
        if a != b:
            c = 3 - a - b
            orientation = 1 if (a, b, c) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1
            expected = scale(orientation * ii, SIGMA[c])
        check(f"product_{a}_{b}", mul(SIGMA[a], SIGMA[b]) == expected)
        check(f"trace_pair_{a}_{b}", F(1, 2) * tr(mul(SIGMA[a], SIGMA[b])) == G(F(a == b)))

casimir = Z
for A in SIGMA:
    casimir = add(casimir, scale(F(1, 4), mul(A, A)))
check("casimir_3_over_4", casimir == scale(F(3, 4), I))

directions = []
for p in range(-2, 3):
    for q in range(-2, 3):
        den = 1 + p*p + q*q
        directions.append((F(2*p, den), F(2*q, den), F(1-p*p-q*q, den)))
directions.append((F(0), F(0), F(-1)))

for k, n in enumerate(directions):
    check(f"unit_{k}", dot(n, n) == 1)
    H = sigma(n)
    Pp = scale(F(1, 2), add(I, H))
    Pm = scale(F(1, 2), add(I, scale(-1, H)))
    check(f"H_square_{k}", mul(H, H) == I)
    check(f"projector_plus_{k}", mul(Pp, Pp) == Pp and adj(Pp) == Pp and tr(Pp) == one)
    check(f"projector_minus_{k}", mul(Pm, Pm) == Pm and adj(Pm) == Pm and tr(Pm) == one)
    check(f"orthogonality_{k}", mul(Pp, Pm) == Z and add(Pp, Pm) == I)
    check(f"eigen_plus_{k}", scale(F(1, 2), mul(H, Pp)) == scale(F(1, 2), Pp))
    check(f"eigen_minus_{k}", scale(F(1, 2), mul(H, Pm)) == scale(F(-1, 2), Pm))
    check(f"direction_reversal_{k}", sigma(tuple(-x for x in n)) == scale(-1, H))
    for t, (c, s) in enumerate(((F(1), F(0)), (F(0), F(1)), (F(-1), F(0)),
                               (F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)))):
        U = add(scale(c, I), scale(-ii * s, H))
        check(f"unitary_{k}_{t}", mul(U, adj(U)) == I)
        v = (F(2), F(-3), F(5))
        ct, st = c*c-s*s, 2*c*s
        nv, nxv = dot(n, v), cross(n, v)
        Rv = tuple(ct*v[j] + st*nxv[j] + (1-ct)*nv*n[j] for j in range(3))
        check(f"adjoint_rotation_{k}_{t}", mul(mul(U, sigma(v)), adj(U)) == sigma(Rv))
    Ua = add(scale(F(3, 5), I), scale(-ii * F(4, 5), H))
    Ub = add(scale(F(5, 13), I), scale(-ii * F(12, 13), H))
    Uab = add(scale(F(-33, 65), I), scale(-ii * F(56, 65), H))
    check(f"angle_composition_{k}", mul(Ua, Ub) == Uab)

print(json.dumps({
    "status": "PASS_HELICIDAD_BLOQUE_ELECTRONICO_FOCAL",
    "exact_field": "Q(i), fractions only; no decimal target data",
    "checks": len(checks),
    "rational_unit_directions": len(directions),
    "scope": "Electronic matrix block, Pauli relations, projectors, adjoint rotations",
    "analytic_proof": "helicidad_electron.tex contains the proof for arbitrary real directions and angles",
    "not_certified": ["physical momentum selector from a TPK history", "charge conjugation map",
                      "CAR/statistics", "global correctness of HMT or all Article I results"],
    "controls": checks,
}, ensure_ascii=False, indent=2))
