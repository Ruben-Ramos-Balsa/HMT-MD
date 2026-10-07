#!/usr/bin/env python3
"""Identidades locales del reloj parametrizado; sólo aritmética Q(i).

Los polinomios son jets formales, no dominios L2 autoadjuntos. Los valores
racionales son datos de control, no coeficientes físicos de la construcción.
"""

from dataclasses import dataclass
from fractions import Fraction as Q


@dataclass(frozen=True)
class G:
    re: Q = Q(0)
    im: Q = Q(0)

    @staticmethod
    def coerce(value):
        return value if isinstance(value, G) else G(Q(value))

    def __add__(self, other):
        other = self.coerce(other)
        return G(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.re, -self.im)

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) + -self

    def __mul__(self, other):
        other = self.coerce(other)
        return G(self.re * other.re - self.im * other.im,
                 self.re * other.im + self.im * other.re)

    __rmul__ = __mul__


ZERO = G()
I = G(Q(0), Q(1))
HBAR = Q(3, 2)


def poly(*coefficients):
    result = [G.coerce(c) for c in coefficients]
    while len(result) > 1 and result[-1] == ZERO:
        result.pop()
    return tuple(result or [ZERO])


def add(a, b):
    return poly(*(sum((p[k] if k < len(p) else ZERO for p in (a, b)), ZERO)
                  for k in range(max(len(a), len(b)))))


def scale(a, c):
    return poly(*(c * x for x in a))


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    result = [ZERO] * (len(a) + len(b) - 1)
    for j, x in enumerate(a):
        for k, y in enumerate(b):
            result[j + k] = result[j + k] + x * y
    return poly(*result)


def diff(a):
    return poly(*(k * a[k] for k in range(1, len(a))))


def vadd(a, b):
    return tuple(add(x, y) for x, y in zip(a, b))


def vsub(a, b):
    return tuple(sub(x, y) for x, y in zip(a, b))


def vscale(a, c):
    return tuple(scale(x, c) for x in a)


def vmul(a, n):
    return tuple(mul(n, x) for x in a)


def k_action(f):
    # Hermitian K = [[1,i],[-i,2]]; K is not scalar.
    return (add(f[0], scale(f[1], I)),
            add(scale(f[0], -I), scale(f[1], 2)))


def constraint(n, f):
    transport = tuple(add(mul(n, diff(x)), scale(mul(diff(n), x), Q(1, 2)))
                      for x in f)
    return vadd(vscale(transport, -I * HBAR), vmul(k_action(f), n))


def bracket(n, m):
    return sub(mul(n, diff(m)), mul(m, diff(n)))


checks = 0


def check(condition, label):
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1


lapses = [poly(0), poly(1), poly(0, 1), poly(1, 0, 1),
          poly(0, 1, 0, 2), poly(2, -1, Q(1, 2))]
vectors = [(poly(1), poly(0)), (poly(0), poly(1)),
           (poly(1, I, 2), poly(-I, 1)),
           (poly(0, 2, -1), poly(1, 0, I))]

for n in lapses:
    for m in lapses:
        for f in vectors:
            left = vsub(constraint(n, constraint(m, f)),
                        constraint(m, constraint(n, f)))
            right = vscale(constraint(bracket(n, m), f), -I * HBAR)
            check(left == right, "[C_N,C_M] = -i hbar C_[N,M]")

# The half-density term prevents imposing every C_N on a solution of C.
# A first-order Taylor jet of exp(-i r K / hbar) v suffices at r=0.
for initial in vectors[:2]:
    velocity = vscale(k_action(initial), -I * (1 / HBAR))
    jet = tuple(poly(x[0], dx[0]) for x, dx in zip(initial, velocity))
    check(all(x[0] == ZERO for x in constraint(poly(1), jet)), "C Psi(0)=0")
    for n in lapses:
        actual = tuple(x[0] for x in constraint(n, jet))
        expected = tuple((-I * HBAR * Q(1, 2)) * diff(n)[0] * x[0]
                         for x in initial)
        check(actual == expected, "C_N Psi(0) = -i hbar N'/2 Psi(0)")

# If N=A^2 then C_N=A C A, exactly, with no domain claim for these jets.
for a in [poly(1), poly(0, 1), poly(1, 0, 1)]:
    for f in vectors:
        check(constraint(mul(a, a), f)
              == vmul(constraint(poly(1), vmul(f, a)), a),
              "C_(A^2) = A C A")

print(f"PASS_LEGENDRE_RELOJ_PARAMETRIZADO: {checks} controles exactos Q(i)")
