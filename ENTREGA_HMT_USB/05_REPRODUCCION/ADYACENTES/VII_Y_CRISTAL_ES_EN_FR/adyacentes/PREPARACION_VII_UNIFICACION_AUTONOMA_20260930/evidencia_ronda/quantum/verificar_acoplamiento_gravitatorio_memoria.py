#!/usr/bin/env python3
"""Exact tests of the coupled transport and nine-step memory reduction.

This is not a certificate of Einstein's full constraint algebra. All physical
scales stay symbolic in the note; rational matrices here are falsifiers.
"""

from fractions import Fraction as F


class C:
    def __init__(self, a=0, b=0):
        self.a, self.b = F(a), F(b)

    @staticmethod
    def of(x):
        return x if isinstance(x, C) else C(x)

    def __add__(self, other):
        other = C.of(other)
        return C(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return C(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-C.of(other))

    def __mul__(self, other):
        other = C.of(other)
        return C(self.a * other.a - self.b * other.b,
                 self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def conj(self):
        return C(self.a, -self.b)

    def __eq__(self, other):
        other = C.of(other)
        return self.a == other.a and self.b == other.b

    def __bool__(self):
        return bool(self.a or self.b)


class M:
    """Sparse matrices over exact Gaussian rationals."""

    def __init__(self, n, m, entries):
        self.n, self.m = n, m
        self.d = {key: C.of(value) for key, value in entries.items() if value}

    def __add__(self, other):
        assert (self.n, self.m) == (other.n, other.m)
        d = self.d.copy()
        for key, value in other.d.items():
            d[key] = d.get(key, C()) + value
        return M(self.n, self.m, d)

    def __neg__(self):
        return self.scale(-1)

    def __sub__(self, other):
        return self + (-other)

    def scale(self, c):
        return M(self.n, self.m, {key: c * v for key, v in self.d.items()})

    def __matmul__(self, other):
        assert self.m == other.n
        rows, d = {}, {}
        for (j, k), value in other.d.items():
            rows.setdefault(j, []).append((k, value))
        for (j, r), value in self.d.items():
            for k, b in rows.get(r, []):
                d[j, k] = d.get((j, k), C()) + value * b
        return M(self.n, other.m, d)

    def adj(self):
        return M(self.m, self.n, {(k, j): v.conj() for (j, k), v in self.d.items()})

    def kron(self, other):
        return M(self.n * other.n, self.m * other.m,
                 {(j * other.n + r, k * other.m + s): a * b
                  for (j, k), a in self.d.items()
                  for (r, s), b in other.d.items()})

    def __eq__(self, other):
        return (self.n, self.m, self.d) == (other.n, other.m, other.d)


def matrix(rows):
    return M(len(rows), len(rows[0]),
             {(j, k): v for j, row in enumerate(rows) for k, v in enumerate(row)})


def eye(n):
    return M(n, n, {(j, j): 1 for j in range(n)})


def diag(a, b):
    d = a.d.copy()
    d.update({(a.n + j, a.m + k): v for (j, k), v in b.d.items()})
    return M(a.n + b.n, a.m + b.m, d)


def horizontal(a, b):
    assert a.n == b.n
    d = a.d.copy()
    d.update({(j, a.m + k): v for (j, k), v in b.d.items()})
    return M(a.n, a.m + b.m, d)


def comm(a, b):
    return a @ b - b @ a


checks = 0


def check(condition, label):
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1


I2, I3 = eye(2), eye(3)
spin = matrix([[F(3, 5), -F(4, 5)], [F(4, 5), F(3, 5)]])
weak = matrix([[F(5, 13), -F(12, 13)], [F(12, 13), F(5, 13)]])
color = matrix([[F(3, 5), -F(4, 5), 0], [F(4, 5), F(3, 5), 0], [0, 0, 1]])
color2 = matrix([[1, 0, 0], [0, F(5, 13), -F(12, 13)], [0, F(12, 13), F(5, 13)]])
phase = C(F(3, 5), F(4, 5))


def transport(s, w, c, p=1):
    return s.kron(w).kron(c).scale(p)


def response(t):
    d = horizontal(-t, eye(t.n))
    return d.adj() @ d


t = transport(spin, weak, color, phase)
check(t.adj() @ t == eye(12), "tensor transport unitarity")
d = horizontal(-t, eye(12))
b = d.adj() @ d
check(b.adj() == b, "coupled response self-adjoint")
source_g = transport(I2, weak, color2, phase)
target_g = transport(I2, spin, color, phase.conj())
tg = target_g @ t @ source_g.adj()
dg = horizontal(-tg, eye(12))
vertex_g = diag(source_g, target_g)
check(dg @ vertex_g == target_g @ d, "covariant difference square")
check((dg.adj() @ dg) @ vertex_g == vertex_g @ b, "coupled gauge covariance")

base = response(transport(I2, I2, I3))
geom = response(transport(spin, I2, I3))
for label, w, c, p in (("weak", weak, I3, 1),
                      ("strong", I2, color, 1),
                      ("phase", I2, I3, phase)):
    internal = response(transport(I2, w, c, p))
    both = response(transport(spin, w, c, p))
    mixed = both - geom - internal + base
    check(bool(mixed.d), f"nonseparable spin-{label} mixed interaction")

b0 = response(transport(I2, weak, color, phase))
b1 = response(transport(spin, weak, color, phase))
clock = matrix([[0, 1], [1, 0]]).kron(eye(24))
coupling = diag(b0, b1)
joint = clock + coupling
check(joint.adj() == joint, "common quantum Hamiltonian self-adjoint")
check(bool(comm(clock, coupling).d), "geometry clock exchanges with coupling")
check(bool(comm(coupling, matrix([[0, C(0, -1)], [C(0, 1), 0]]).kron(eye(24))).d),
      "matter-dependent response on geometry conjugate observable")

# Ordered nonabelian holonomy is retained; order cannot be reversed.
t1 = transport(spin, weak, color)
t2 = transport(weak, spin, color2, phase)
check(t2 @ t1 != t1 @ t2, "nonabelian path ordering")
check((t2 @ t1).adj() @ (t2 @ t1) == eye(12), "composed holonomy unitary")


def dense_eye(n):
    return [[F(int(j == k)) for k in range(n)] for j in range(n)]


def dense_mul(a, b):
    return [[sum(a[j][r] * b[r][k] for r in range(len(b)))
             for k in range(len(b[0]))] for j in range(len(a))]


def dense_sub(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def inverse(a):
    n = len(a)
    a = [list(row) + identity for row, identity in zip(a, dense_eye(n))]
    for k in range(n):
        pivot = next(j for j in range(k, n) if a[j][k])
        a[k], a[pivot] = a[pivot], a[k]
        q = a[k][k]
        a[k] = [v / q for v in a[k]]
        for j in range(n):
            if j != k:
                q = a[j][k]
                a[j] = [v - q * w for v, w in zip(a[j], a[k])]
    return [row[n:] for row in a]


def submatrix(a, rows, columns):
    return [[a[j][k] for k in columns] for j in rows]


def schur(a, kept):
    removed = [j for j in range(len(a)) if j not in kept]
    aa = submatrix(a, kept, kept)
    ab = submatrix(a, kept, removed)
    bb = submatrix(a, removed, removed)
    ba = submatrix(a, removed, kept)
    return dense_sub(aa, dense_mul(dense_mul(ab, inverse(bb)), ba))


def chain(n):
    a = [[F(0) for _ in range(n + 1)] for _ in range(n + 1)]
    for j in range(n):
        a[j][j] += n
        a[j + 1][j + 1] += n
        a[j][j + 1] -= n
        a[j + 1][j] -= n
    return a


l = chain(9)
expected_static = [[F(1), F(-1)], [F(-1), F(1)]]
check(schur(l, [0, 9]) == expected_static, "nine-step static response")
for z in (F(-1), F(-2), F(-1, 3), F(0)):
    full = [[v - (z if j == k else 0) for k, v in enumerate(row)]
            for j, row in enumerate(l)]
    direct = schur(full, [0, 9])
    staged = schur(schur(full, [0, 3, 6, 9]), [0, 3])
    check(direct == staged, "exact nonadic Schur refinement by stages")

interior = list(range(1, 9))
v = submatrix(l, [0, 9], interior)
hi_inv = inverse(submatrix(l, interior, interior))
norm_extra = dense_mul(dense_mul(dense_mul(v, hi_inv), hi_inv),
                       submatrix(l, interior, [0, 9]))
z = [[norm_extra[j][k] + int(j == k) for k in range(2)] for j in range(2)]
expected_z = [[F(95, 27), F(40, 27)], [F(40, 27), F(95, 27)]]
check(z == expected_z, "nonadic temporal norm 95/27,40/27")
harmonic = [[F(9 - j, 9), F(j, 9)] for j in range(10)]
harmonic_star = [list(row) for row in zip(*harmonic)]
check(dense_mul(harmonic_star, harmonic) == expected_z,
      "norm of full harmonic extension")
check(dense_mul(dense_mul(harmonic_star, l), harmonic) == expected_static,
      "energy of full harmonic extension")
check(z != dense_eye(2), "negative autonomous-coarse-clock test")

# Exact local density commutator, before any identification with Einstein constraints.
b1 = matrix([[1, -1, 0], [-1, 1, 0], [0, 0, 0]])
b2 = matrix([[0, 0, 0], [0, 1, -1], [0, -1, 1]])
cn = b1.scale(2) + b2.scale(3)
cm = b1.scale(5) + b2.scale(7)
check(comm(cn, cm) == comm(b1, b2).scale(2 * 7 - 3 * 5),
      "coupled energy-density commutator")
check(bool(comm(b1, b2).d), "adjacent densities do not commute")

print(f"PASS_ACOPLAMIENTO_GRAVITATORIO_MEMORIA: {checks} exact checks")
print("N=9 temporal metric: diag=95/27, cross=40/27; static response preserved.")
print("Scope: coupled finite operator, Gauss covariance, and exact memory refinement.")
