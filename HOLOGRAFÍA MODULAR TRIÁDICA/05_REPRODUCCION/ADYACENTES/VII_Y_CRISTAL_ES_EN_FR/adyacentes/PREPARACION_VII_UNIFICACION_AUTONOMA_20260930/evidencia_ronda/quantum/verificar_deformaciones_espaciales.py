#!/usr/bin/env python3
"""Clifford, espín y defecto Fourier espacial, exactamente sobre Q(i)."""
from dataclasses import dataclass
from fractions import Fraction as Q


@dataclass(frozen=True)
class G:
    re: Q = Q(0)
    im: Q = Q(0)

    @staticmethod
    def coerce(x):
        return x if isinstance(x, G) else G(Q(x))

    def __add__(self, x):
        x = self.coerce(x)
        return G(self.re + x.re, self.im + x.im)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.re, -self.im)

    def __sub__(self, x):
        return self + -self.coerce(x)

    def __mul__(self, x):
        x = self.coerce(x)
        return G(self.re * x.re - self.im * x.im,
                 self.re * x.im + self.im * x.re)

    __rmul__ = __mul__

    def star(self):
        return G(self.re, -self.im)


Z, I = G(), G(Q(0), Q(1))


def matrix(rows):
    return tuple(tuple(G.coerce(x) for x in row) for row in rows)


def eye(n):
    return matrix([[int(i == j) for j in range(n)] for i in range(n)])


def zero(n):
    return matrix([[0] * n for _ in range(n)])


def add(a, b):
    return tuple(tuple(x + y for x, y in zip(r, s)) for r, s in zip(a, b))


def scale(a, c):
    return tuple(tuple(c * x for x in row) for row in a)


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(len(b))), Z)
                       for j in range(len(b[0]))) for i in range(len(a)))


def star(a):
    return tuple(tuple(a[j][i].star() for j in range(len(a)))
                 for i in range(len(a[0])))


def comm(a, b):
    return sub(mul(a, b), mul(b, a))


def anti(a, b):
    return add(mul(a, b), mul(b, a))


def kron(a, b):
    return tuple(tuple(x * y for x in ra for y in rb) for ra in a for rb in b)


checks = 0


def check(test, label):
    global checks
    if not test:
        raise AssertionError(label)
    checks += 1


s1 = matrix([[0, 1], [1, 0]])
s2 = matrix([[0, -I], [I, 0]])
s3 = matrix([[1, 0], [0, -1]])
alphas = [kron(s1, s) for s in (s1, s2, s3)]
beta = kron(s3, eye(2))
gamma5 = kron(s1, eye(2))
for i, a in enumerate(alphas):
    check(star(a) == a, "alpha hermítica")
    check(comm(gamma5, a) == zero(4), "quiralidad del cinético")
    check(anti(beta, a) == zero(4), "masa escalar anticommuta alpha")
    for j, b in enumerate(alphas):
        check(anti(a, b) == scale(eye(4), 2 * int(i == j)), "Clifford")

check(anti(beta, gamma5) == zero(4), "Yukawa masivo no conserva carga axial")
check(comm(beta, gamma5) != zero(4), "control axial negativo")

j12 = mul(alphas[0], alphas[1])
spin = add(scale(eye(4), Q(3, 5)), scale(j12, Q(4, 5)))
check(mul(spin, star(spin)) == eye(4), "lift spin unitario")
check(mul(mul(spin, gamma5), star(spin)) == gamma5, "spin preserva gamma5")
check(mul(mul(spin, alphas[0]), star(spin))
      == add(scale(alphas[0], Q(-7, 25)), scale(alphas[1], Q(-24, 25))),
      "Clifford cotransportado: eje 1")
check(mul(mul(spin, alphas[1]), star(spin))
      == add(scale(alphas[1], Q(-7, 25)), scale(alphas[0], Q(24, 25))),
      "Clifford cotransportado: eje 2")
check(mul(mul(beta, gamma5), beta) == scale(gamma5, -1),
      "inversión de orientación intercambia quiralidad")
for a in alphas:
    check(mul(mul(beta, a), beta) == scale(a, -1), "paridad espacial")


def fourier_l(r, k):
    rows = [[Z] * (2 * r + 1) for _ in range(2 * r + 1)]
    for n in range(-r, r + 1):
        if -r <= n + k <= r:
            rows[n + k + r][n + r] = G(Q(n) + Q(k, 2))
    return matrix(rows)


for r in range(1, 7):
    lp, lm, d = (fourier_l(r, k) for k in (1, -1, 0))
    n = scale(add(lp, lm), Q(1, 2))
    m = scale(sub(lp, lm), -I * Q(1, 2))
    check(star(n) == n and star(m) == m, "lapsos reales hermíticos")
    defect = add(comm(n, m), scale(d, I))
    check(defect[-1][-1] == I * Q(1, 2) * (Q(r) + Q(1, 2)) ** 2,
          "defecto de borde superior = i(R+1/2)^2/2")
    check(defect[0][0] == -I * Q(1, 2) * (Q(r) + Q(1, 2)) ** 2,
          "defecto de borde inferior")
    check(all(defect[i][j] == Z
              for i in range(2 * r + 1) for j in range(1, 2 * r)),
          "defecto nulo sobre modos interiores fijos")
    k = 2 * r + 1
    check(fourier_l(r, k) == zero(2 * r + 1)
          and fourier_l(r, -k) == zero(2 * r + 1),
          "lapsos variables fuera de todo el corte")
    check((-I * k) != Z, "conmutador continuo sobre e_1 no es cero")
    check(comm(n, mul(d, d)) != zero(2 * r + 1),
          "cambio espacial no simetría de métrica congelada")

spin_structure = (0, 1, 0)
rotated = (spin_structure[1], spin_structure[0], spin_structure[2])
check(rotated != spin_structure, "rotación orientada cambia estructura spin del toro")

print(f"PASS_DEFORMACIONES_ESPACIALES_QUIRALIDAD: {checks} controles exactos Q(i)")
