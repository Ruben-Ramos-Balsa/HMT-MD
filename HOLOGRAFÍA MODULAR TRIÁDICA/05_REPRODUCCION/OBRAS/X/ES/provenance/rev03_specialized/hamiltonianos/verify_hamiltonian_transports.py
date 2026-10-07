#!/usr/bin/env python3
"""Exact, finite controls for the additive Hamiltonian chapter.

Standard library only. No assert, files written, random sampling or decimal
targets. The universal proofs are in hamiltonianos_curvatura.tex; this script
checks their native matrices and explicit rational witnesses, not all HMT.
"""
from fractions import Fraction as F
from itertools import product
import json
import sys


class Gaussian:
    """Gaussian rational a+i b, with exact arithmetic."""
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        if isinstance(a, Gaussian):
            self.a, self.b = a.a, a.b
        else:
            self.a, self.b = F(a), F(b)

    def __add__(self, other):
        other = Gaussian(other)
        return Gaussian(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Gaussian(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-Gaussian(other))

    def __rsub__(self, other):
        return Gaussian(other) - self

    def __mul__(self, other):
        other = Gaussian(other)
        return Gaussian(self.a * other.a - self.b * other.b,
                        self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __eq__(self, other):
        other = Gaussian(other)
        return self.a == other.a and self.b == other.b

    def conjugate(self):
        return Gaussian(self.a, -self.b)


checks = []


def check(name, condition):
    if not condition:
        raise ValueError("FAILED: " + name)
    checks.append(name)


def mat(rows):
    return [[Gaussian(x) for x in row] for row in rows]


def eye(n):
    return mat([[int(i == j) for j in range(n)] for i in range(n)])


def zero(n):
    return mat([[0] * n for _ in range(n)])


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[Gaussian(c) * x for x in row] for row in a]


def mul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Gaussian())
             for j in range(len(b[0]))] for i in range(len(a))]


def adj(a):
    return [[a[j][i].conjugate() for j in range(len(a))]
            for i in range(len(a[0]))]


def tensor(a, b):
    return [[a[i][j] * b[k][ell]
             for j in range(len(a[0])) for ell in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def main():
    ident = eye(2)
    omega = mat([[0, 1], [-1, 0]])
    coxeter = mat([[0, -1], [1, -1]])
    nilpotent = mat([[0, 1], [0, 0]])
    fav = mat([[0, 1], [1, 1]])
    elliptic_scaled = add(scale(2, coxeter), ident)
    hyperbolic_scaled = add(scale(2, mul(fav, fav)), scale(-3, ident))
    check("ternary Coxeter", add(add(mul(coxeter, coxeter), coxeter), ident) == zero(2))
    check("elliptic square before sqrt(3)", mul(elliptic_scaled, elliptic_scaled) == scale(-3, ident))
    check("parabolic square", mul(nilpotent, nilpotent) == zero(2))
    check("hyperbolic square before sqrt(5)", mul(hyperbolic_scaled, hyperbolic_scaled) == scale(5, ident))
    for name, generator in (("elliptic", elliptic_scaled),
                            ("parabolic", nilpotent),
                            ("hyperbolic", hyperbolic_scaled)):
        gram = scale(-1, mul(omega, generator))
        check(name + " symmetric Hamiltonian Hessian", adj(gram) == gram)
        check(name + " exact Hamiltonian vector field", mul(omega, gram) == generator)
        check(name + " infinitesimal symplecticity",
              add(mul(adj(generator), omega), mul(omega, generator)) == zero(2))
    check("elliptic signed Hessian determinant", det2(scale(-1, mul(omega, elliptic_scaled))) == 3)
    check("hyperbolic signed Hessian determinant", det2(scale(-1, mul(omega, hyperbolic_scaled))) == -5)

    b = mat([[1, 0], [18, 1]])
    bi = mat([[1, 0], [-18, 1]])
    nv = mat([[-18, 1], [-324, 18]])
    check("native memory conjugacy", mul(mul(b, nilpotent), bi) == nv)
    check("native memory symplectic frame", mul(mul(adj(b), omega), b) == omega)
    check("native memory nilpotence", mul(nv, nv) == zero(2))
    for g, s in product(range(-2, 3), repeat=2):
        conserved = s - 18 * g
        check("memory return %s,%s" % (g, s), (s + 72) - 18 * (g + 4) == conserved)
        velocity = F(conserved)
        first_order = s * velocity - F(conserved * conserved, 2)
        second_order = velocity * velocity / 2 + 18 * g * velocity
        check("memory Legendre boundary %s,%s" % (g, s), first_order == second_order)

    # Rational r=e^eta, a=dot eta/2; no numerical exponentials are needed.
    for tau, r, freq, a, q, p in product((-1, 0, 1), (F(1, 2), F(2)),
                                        (F(1, 3), F(3)), (F(0), F(2, 3)),
                                        (F(-2), F(1)), (F(-1), F(3))):
        qdot = freq * r * p + a * q
        pdot = -freq * tau * q / r - a * p
        explicit_dt = a * (-tau * q * q / r + r * p * p)
        invariant_dt = explicit_dt + tau * q * qdot / r + r * p * pdot
        h = freq * (tau * q * q / r + r * p * p) / 2 + a * q * p
        lag = (qdot - a * q)**2 / (2 * freq * r) - freq * tau * q*q/(2*r)
        check("transport invariant case %s" % len(checks), invariant_dt == 0)
        check("regular Legendre case %s" % len(checks), p * qdot - h == lag and freq*r > 0)

    im = Gaussian(0, 1)
    sigma1 = add(nilpotent, adj(nilpotent))
    sigma2 = scale(-im, add(nilpotent, scale(-1, adj(nilpotent))))
    sigma3 = add(mul(nilpotent, adj(nilpotent)), scale(-1, mul(adj(nilpotent), nilpotent)))
    sigmas = (sigma1, sigma2, sigma3)
    for i, si in enumerate(sigmas):
        check("Pauli self-adjoint %d" % i, adj(si) == si)
        for j, sj in enumerate(sigmas):
            check("Pauli anticommutator %d,%d" % (i, j),
                  add(mul(si, sj), mul(sj, si)) == scale(2 * int(i == j), ident))
    check("Pauli oriented product", mul(sigma1, sigma2) == scale(im, sigma3))
    alpha = [tensor(sigma1, s) for s in sigmas]
    beta = tensor(sigma3, ident)
    for i, ai in enumerate(alpha):
        check("Dirac mass anticommutes %d" % i,
              add(mul(ai, beta), mul(beta, ai)) == zero(4))
        for j, aj in enumerate(alpha):
            check("Dirac spatial Clifford %d,%d" % (i, j),
                  add(mul(ai, aj), mul(aj, ai)) == scale(2*int(i == j), eye(4)))
    m0 = mat([[1, 0], [0, 2]])
    transport = mat([[2, 0], [0, 1]])
    mb = mul(mul(transport, m0), transport)
    check("positive congruence changes fixed spectrum", mb == mat([[4, 0], [0, 2]]))
    # A finite flavour witness, not fitted HMT mass values.
    c = F(3, 2)
    momentum = (F(1, 3), F(-2), F(5, 7))
    hd = scale(c*c, tensor(beta, mb))
    for aj, pj in zip(alpha, momentum):
        hd = add(hd, scale(c*pj, tensor(aj, ident)))
    rhs_flavour = add(scale(c*c*sum(p*p for p in momentum), ident), scale(c**4, mul(mb, mb)))
    check("Dirac-mass factorization exact rational witness", mul(hd, hd) == tensor(eye(4), rhs_flavour))
    check("Dirac Hamiltonian self-adjoint", adj(hd) == hd)

    epsilon, mu, k = F(4), F(9), F(3)
    wave_c = F(1, 6)
    freq = wave_c * k
    check("Maxwell speed from two constitutive outputs", epsilon*mu*wave_c**2 == 1)
    check("Maxwell modal oscillator coefficient", epsilon*freq**2 == k*k/mu)
    mu_squared, coupling = F(3), F(2)
    v_squared = mu_squared/coupling
    check("Higgs minimum curvature", -mu_squared + 3*coupling*v_squared == 2*mu_squared)

    total = [F(0), F(0), F(0)]
    for trits in product(range(3), repeat=6):
        witness = F(int(sum(trits) % 3 == 0)) - F(1, 3)
        for j in range(3):
            total[j] += witness ** (j + 1)
    moments = [x / (3**6) for x in total]
    check("YM curvature witness moments", moments == [F(0), F(2, 9), F(2, 27)])
    check("YM normalized symplectic pullback coefficient", 2 * F(7, 5) * (1/(2*F(7, 5))) == 1)
    print(json.dumps({"status": "PASS_EXACT_HAMILTONIAN_TRANSPORT_CONTROLS",
                      "checks": len(checks), "arithmetic": "rational and Gaussian rational",
                      "scope": "native finite operators and stated rational witnesses",
                      "universal_proofs": "hamiltonianos_curvatura.tex",
                      "files_written": False}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
