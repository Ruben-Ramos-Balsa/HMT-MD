"""Controles exactos de la nota ACCION_MEMORIA_TRES_REGIMENES.

Álgebra diferencial racional normalizada por [Q,P]=1. Cada conmutador
homogéneo recupera el factor i*hbar en la representación física.
No prueba existencia de límites ni una teoría cuántica global.
"""
from fractions import Fraction as F
from math import comb, factorial

checks = 0


def clean(a):
    return {k: F(v) for k, v in a.items() if v}


def add(a, b):
    c = dict(a)
    for k, v in b.items():
        c[k] = c.get(k, F(0)) + v
    return clean(c)


def scale(t, a):
    return clean({k: F(t)*v for k, v in a.items()})


def mul(a, b):
    c = {}
    for (m, n), v in a.items():
        for (r, s), w in b.items():
            for j in range(min(n, r)+1):
                k = (m+r-j, n+s-j)
                c[k] = c.get(k, F(0)) + v*w*comb(n, j)*F(factorial(r), factorial(r-j))
    return clean(c)


def comm(a, b):
    return add(mul(a, b), scale(-1, mul(b, a)))


def eq(a, b):
    global checks
    assert a == b, (a, b)
    checks += 1


I = {(0, 0): F(1)}
Q = {(1, 0): F(1)}
P = {(0, 1): F(-1)}
A = scale(F(1, 2), mul(Q, Q))
B = scale(F(1, 2), add(mul(Q, P), mul(P, Q)))
C = scale(F(1, 2), mul(P, P))
eq(comm(Q, P), I)
eq(comm(A, B), scale(2, A))
eq(comm(B, C), scale(2, C))
eq(comm(A, C), B)

for tau in (-1, 0, 1):
    for a in (F(1, 9), F(1, 2), F(1), F(3), F(9)):
        invariant = add(scale(tau/a, A), scale(a, C))
        eta_derivative = add(scale(-tau/a, A), scale(a, C))
        for velocity in (F(-3), F(0), F(2, 9)):
            for omega in (F(1, 9), F(2)):
                h = add(scale(omega, invariant), scale(velocity/2, B))
                # (i/hbar)[H,I] = - normalized_commutator(H,I).
                eq(comm(h, invariant), scale(velocity, eta_derivative))
        eq(comm(invariant, invariant), {})
        assert eta_derivative  # Omitir conexión con dot_eta != 0 falla.
        checks += 1

for action in (F(1, 7), F(1), F(9)):
    memory = add(P, scale(-18*action, Q))
    hret = scale(4, memory)
    hmem = scale(1/(2*action), mul(memory, memory))
    eq(comm(memory, hmem), {})
    eq(comm(hret, hmem), {})
    eq(scale(-1, comm(hret, Q)), scale(4, I))
    eq(scale(-1, comm(hret, P)), scale(72*action, I))
    eq(comm(hret, memory), {})

# Dependencias escalares recibidas: no uso de datos metrológicos.
for hbar in (F(1, 3), F(7, 11)):
    for rho in (F(1, 9), F(1), F(9)):
        c, ell, y, tensor = F(5, 2), F(11, 7), F(3, 4), F(13, 8)
        energy, mass, grav = hbar*c*y/ell, hbar*y/(c*ell), c**3*ell**2/hbar
        hb = rho*hbar
        eb, mb, gb = hb*c*y/ell, hb*y/(c*ell), c**3*ell**2/hb
        eq(eb, rho*energy)
        eq(mb, rho*mass)
        eq(gb, grav/rho)
        eq(eb/hb, energy/hbar)
        eq(gb*(rho*tensor), grav*tensor)
        # Un defecto no nulo se escala, no desaparece.
        defect = F(7, 13)
        eq(rho**2*defect == 0, False)

# Composición área–torsión. Fixtures racionales, no evaluaciones físicas.
for pi in (F(22, 7), F(3)):
    for hbar in (F(1, 3), F(7, 11)):
        c, ell, gamma, a0 = F(5, 2), F(11, 7), F(2, 3), F(1, 9)
        grav = c**3*ell**2/hbar
        kappa = 8*pi*grav/c**4
        cg = 3*kappa*c*hbar**2*gamma**2/(16*(1+gamma**2))
        eq(cg/hbar, 3*pi*ell**2*gamma**2/(2*(1+gamma**2)))
        for nscreen in (0, 1, 72):
            area = ell**2*gamma*a0*nscreen
            eq(cg/hbar*nscreen, 3*pi*gamma*area/(2*a0*(1+gamma**2)))
        volume, lapse, current = F(13, 3), F(3, 2), F(-7, 5)
        t0 = pi*ell/(54*c)
        htor = -lapse*c*cg/volume*current
        eq(t0*htor/hbar,
           -pi**2/36*lapse*ell**3/volume*gamma**2/(1+gamma**2)*current)
        phi, ell0 = F(13, 8), F(2, 7)
        kav = (pi-phi**2)/((1+phi**2)*ell0)
        eq(t0*c*kav, pi/54*(ell/ell0)*(pi-phi**2)/(1+phi**2))

print(f'PASS_FOCAL_ACCION_MEMORIA: {checks} controles exactos; no cierre global.')
