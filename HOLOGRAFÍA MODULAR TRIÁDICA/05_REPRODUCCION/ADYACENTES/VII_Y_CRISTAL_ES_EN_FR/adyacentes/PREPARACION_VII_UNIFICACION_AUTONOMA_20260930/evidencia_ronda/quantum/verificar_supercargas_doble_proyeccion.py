#!/usr/bin/env python3
"""Exact finite checks; does not replace the analytic domain/limit proofs."""
from dataclasses import dataclass
from fractions import Fraction as F


@dataclass(frozen=True)
class C:
    re: F = F(0)
    im: F = F(0)

    def __add__(self, other):
        other = cast(other)
        return C(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return C(-self.re, -self.im)

    def __sub__(self, other):
        return self + -cast(other)

    def __mul__(self, other):
        other = cast(other)
        return C(self.re * other.re - self.im * other.im,
                 self.re * other.im + self.im * other.re)

    __rmul__ = __mul__

    def star(self):
        return C(self.re, -self.im)


def cast(x):
    return x if isinstance(x, C) else C(F(x))


def mat(rows):
    return tuple(tuple(cast(x) for x in row) for row in rows)


def add(a, b):
    return mat([[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)])


def scale(c, a):
    return mat([[cast(c) * x for x in row] for row in a])


def mul(a, b):
    assert len(a[0]) == len(b)
    return mat([[sum((a[i][k] * b[k][j] for k in range(len(b))), C())
                 for j in range(len(b[0]))] for i in range(len(a))])


def star(a):
    return mat([[a[j][i].star() for j in range(len(a))]
                for i in range(len(a[0]))])


def eye(n):
    return mat([[int(i == j) for j in range(n)] for i in range(n)])


def blockdiag(a, b):
    z = C()
    return tuple(tuple(row) + (z,) * len(b[0]) for row in a) + tuple(
        (z,) * len(a[0]) + tuple(row) for row in b)


def qinc(d):
    n, p = len(d[0]), len(d)
    return tuple((C(),) * n + row for row in star(d)) + tuple(
        row + (C(),) * p for row in d)


checks = 0


def check(a, b):
    global checks
    assert a == b, (a, b)
    checks += 1


s1 = mat([[0, 1], [1, 0]])
s2 = mat([[0, C(F(0), F(-1))], [C(F(0), F(1)), 0]])
s3 = mat([[1, 0], [0, -1]])
identity = eye(2)
zero = scale(0, identity)
s = add(s1, s2)  # B=s/sqrt(2); check without algebraic-number rounding.
check(mul(s, s), scale(2, identity))
check(mul(mul(s, s1), s), scale(2, s2))
check(mul(mul(s, s2), s), scale(2, s1))
check(mul(mul(s, s3), s), scale(-2, s3))

for r in (F(1, 3), F(1, 2), F(1), F(3, 2), F(2), F(3)):
    for m in range(-5, 6):
        for w in range(-5, 6):
            q = add(scale(F(m) / r, s1), scale(F(w) * r, s2))
            e = F(m * m) / (r * r) + F(w * w) * r * r
            check(star(q), q)
            check(mul(q, q), scale(e, identity))
            check(add(mul(s3, q), mul(q, s3)), zero)
            swapped = add(scale(F(w) / r, s1), scale(F(m) * r, s2))
            target = add(scale(F(m) * r, s1), scale(F(w) / r, s2))
            check(mul(mul(s, swapped), s), scale(2, target))

d = mat([[-1, 1, 0], [0, -1, 1], [1, 0, -1]])
q = qinc(d)
gamma = blockdiag(eye(3), scale(-1, eye(3)))
check(star(q), q)
check(mul(q, q), blockdiag(mul(star(d), d), mul(d, star(d))))
check(add(mul(gamma, q), mul(q, gamma)), scale(0, eye(6)))

orient = mat([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])
transport = blockdiag(eye(3), orient)
check(qinc(mul(orient, d)), mul(mul(transport, q), star(transport)))
check(mul(transport, gamma), mul(gamma, transport))

df = blockdiag(d, mat([[2]]))
j0 = mat([[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0]])
j = blockdiag(j0, j0)
check(mul(star(j), j), eye(6))
check(mul(df, j0), mul(j0, d))
check(mul(star(df), j0), mul(j0, star(d)))
check(mul(qinc(df), j), mul(j, q))
check(mul(mul(qinc(df), qinc(df)), j), mul(j, mul(q, q)))

# Adversarial isometric cochain map: forward square alone is insufficient.
dc = mat([[1]])
df_bad = mat([[1, 2], [0, 3]])
j_bad = mat([[1], [0]])
check(mul(df_bad, j_bad), mul(j_bad, dc))
assert mul(star(df_bad), j_bad) != mul(j_bad, star(dc))
assert mul(qinc(df_bad), blockdiag(j_bad, j_bad)) != mul(blockdiag(j_bad, j_bad), qinc(dc))
checks += 2
print(f"PASS_FOCAL_SUPERCARGAS_DOBLE_PROYECCION exact_checks={checks}")
