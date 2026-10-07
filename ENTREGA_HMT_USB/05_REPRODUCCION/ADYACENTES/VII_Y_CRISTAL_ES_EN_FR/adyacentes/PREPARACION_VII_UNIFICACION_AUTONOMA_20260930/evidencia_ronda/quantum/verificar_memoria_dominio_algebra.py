#!/usr/bin/env python3
"""Exact focal falsifiers; not a certificate of four-interaction closure.

Arithmetic is Q(i,sqrt(2)). Test hbar=1 denotes algebraic units, not a
numerical choice for a generated HMT constant. General proofs and domains:
MEMORIA_DOMINIO_Y_ALGEBRA.md.
"""

from fractions import Fraction as F


class Q:
    """a + b sqrt(2) + i(c + d sqrt(2)), with rational coefficients."""

    def __init__(self, a=0, b=0, c=0, d=0):
        self.v = tuple(F(x) for x in (a, b, c, d))

    @staticmethod
    def asq(x):
        return x if isinstance(x, Q) else Q(x)

    def __add__(self, other):
        other = self.asq(other)
        return Q(*(x + y for x, y in zip(self.v, other.v)))

    __radd__ = __add__

    def __neg__(self):
        return Q(*(-x for x in self.v))

    def __sub__(self, other):
        return self + (-self.asq(other))

    def __rsub__(self, other):
        return self.asq(other) - self

    def __mul__(self, other):
        other = self.asq(other)
        out = [F(0)] * 4
        # Basis indices: sqrt(2) exponent is bit 0; i exponent is bit 1.
        for j, x in enumerate(self.v):
            for k, y in enumerate(other.v):
                factor = 2 if (j & 1 and k & 1) else 1
                if j & 2 and k & 2:
                    factor = -factor
                out[j ^ k] += factor * x * y
        return Q(*out)

    __rmul__ = __mul__

    def __truediv__(self, rational):
        return self * (F(1) / F(rational))

    def conj(self):
        a, b, c, d = self.v
        return Q(a, b, -c, -d)

    def __eq__(self, other):
        return self.v == self.asq(other).v


def mat(rows):
    return [[Q.asq(x) for x in row] for row in rows]


def eye(n):
    return mat([[int(j == k) for k in range(n)] for j in range(n)])


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(k, a):
    return [[k * x for x in row] for row in a]


def sub(a, b):
    return add(a, scale(-1, b))


def mul(a, b):
    assert len(a[0]) == len(b)
    return [[sum((a[j][r] * b[r][k] for r in range(len(b))), Q())
             for k in range(len(b[0]))] for j in range(len(a))]


def adj(a):
    return [[a[j][k].conj() for j in range(len(a))]
            for k in range(len(a[0]))]


def comm(a, b):
    return sub(mul(a, b), mul(b, a))


def kron(a, b):
    return [[x * y for x in ar for y in br] for ar in a for br in b]


checks = 0


def check(condition, name):
    global checks
    if not condition:
        raise AssertionError(name)
    checks += 1


I2 = eye(2)
I4 = eye(4)
i = Q(0, 0, 1)
r8 = Q(0, 2)
sx = mat([[0, 1], [1, 0]])
sy = mat([[0, -i], [i, 0]])
sz = mat([[1, 0], [0, -1]])
hs = [scale(F(1, 2), s) for s in (sx, sy, sz)]
P = scale(F(1, 9), mat([[1, r8], [r8, 8]]))
R = scale(F(1, 3), mat([[r8, 1], [-1, r8]]))
J = mat([[1, 0], [0, 1], [0, 0], [0, 0]])
E = sub(I4, mul(J, adj(J)))


def phi(a):
    return mul(mul(adj(J), a), J)


def lift(a):
    return kron(P, a)


def dilation(c):
    # I tensor I + P tensor (C-I) is exactly the owner's 8:1 block matrix.
    return add(I4, kron(P, sub(c, I2)))


check(mul(adj(R), R) == I2, "unitary R")
check(adj(P) == P, "self-adjoint P")
check(mul(P, P) == P, "idempotent P")
check(mul(mul(R, mat([[0, 0], [0, 1]])), adj(R)) == P,
      "spectral projection P")
active = lift(I2)
passive = sub(I4, active)
check(active != I4, "non-unital lift on full space")
check(mul(passive, passive) == passive, "passive projection")
check(mul(passive, lift(sx)) == scale(0, I4), "passive sector annihilates lift")
check(mul(lift(sx), lift(sy)) == lift(mul(sx, sy)), "star-homomorphism product")
check(adj(lift(sy)) == lift(adj(sy)), "star-homomorphism adjoint")

cs = [sx, sy, sz, mat([[F(3, 5), -F(4, 5)], [F(4, 5), F(3, 5)]])]
for a in cs:
    check(mul(adj(dilation(a)), dilation(a)) == I4, "unitary dilation")
    check(dilation(a) == add(passive, lift(a)), "passive plus active evolution")
    for b in cs:
        check(mul(dilation(a), dilation(b)) == dilation(mul(a, b)),
              "dilation composition")

# Generic exact compression identity, not restricted to Pauli matrices.
for seed in range(1, 33):
    a = mat([[Q(F((j + 2) * (k + seed) % 13 - 6, 7),
                   0, F((j - k + seed) % 5 - 2, 3))
              for k in range(4)] for j in range(4)])
    b = mat([[Q(F((j + seed) * (2 * k + 1) % 17 - 8, 5),
                   F((j + k + seed) % 3 - 1, 2))
              for k in range(4)] for j in range(4)])
    lhs = sub(comm(phi(a), phi(b)), phi(comm(a, b)))
    rhs = sub(phi(mul(mul(b, E), a)), phi(mul(mul(a, E), b)))
    check(lhs == rhs, "generic compression commutator defect")

for a, b, c in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
    check(comm(hs[a], hs[b]) == scale(i, hs[c]), "Pauli algebra")
    check(comm(lift(hs[a]), lift(hs[b])) == scale(i, lift(hs[c])),
          "full lifted Pauli algebra")
    check(phi(lift(hs[a])) == scale(F(1, 9), hs[a]), "visible generator")
    check(comm(phi(lift(hs[a])), phi(lift(hs[b])))
          == scale(F(1, 81), comm(hs[a], hs[b])), "visible commutator")
    defect = sub(comm(phi(lift(hs[a])), phi(lift(hs[b]))),
                 phi(comm(lift(hs[a]), lift(hs[b]))))
    check(defect == scale(-F(8, 81), comm(hs[a], hs[b])),
          "exact 8/81 memory defect")
    check(comm(phi(lift(hs[a])), phi(lift(hs[b])))
          != scale(i, phi(lift(hs[c]))), "negative visible closure test")

# Positive-semidefinite H' = I + sigma_x = vv*: compression is H=1,
# but neither generator nor its square intertwines.
hp = mat([[1, 1], [1, 1]])
j = mat([[1], [0]])
h = mat([[1]])
v = mat([[1], [1]])
check(hp == mul(v, adj(v)), "positive-semidefinite counterexample")
check(mul(mul(adj(j), hp), j) == h, "compatible compressed form")
check(sub(mul(hp, j), mul(j, h)) == mat([[0], [1]]), "nonzero leakage")
check(mul(mul(adj(j), mul(hp, hp)), j) == mat([[2]]),
      "compressed second derivative differs")
check(mul(h, h) == mat([[1]]), "small second derivative")

print(f"PASS_FOCAL_MEMORIA_DOMINIO_ALGEBRA: {checks} exact checks")
print("Scope: algebraic identities and finite falsifiers; infinite-domain proofs are in the note.")
