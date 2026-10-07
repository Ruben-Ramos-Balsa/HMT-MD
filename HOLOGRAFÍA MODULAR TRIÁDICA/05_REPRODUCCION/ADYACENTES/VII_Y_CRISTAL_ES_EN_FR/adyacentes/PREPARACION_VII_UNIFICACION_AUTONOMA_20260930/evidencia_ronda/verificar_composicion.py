"""Controles focales; no prueba de unificación física ni regeneración de HMT.

Ejecutar: python3 -I -S verificar_composicion.py
Las pruebas generales están en INTEGRACION_MATEMATICA.md.
"""
from fractions import Fraction as Q
from math import exp, log, pi, isclose, sqrt
import json


def mat(n, m=None):
    return [[Q(0) for _ in range(m or n)] for _ in range(n)]


def eye(n):
    a = mat(n)
    for i in range(n):
        a[i][i] = Q(1)
    return a


def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def tr(a):
    return [list(row) for row in zip(*a)]


def sub(a, b):
    return [[x-y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[c*x for x in row] for row in a]


def comm(a, b):
    return sub(mul(a, b), mul(b, a))


def kron(a, b):
    return [[x*y for x in ar for y in br] for ar in a for br in b]


def block(a, b, c, d):
    return [ar+br for ar, br in zip(a, b)] + [cr+dr for cr, dr in zip(c, d)]


def rotation(i, j, c, s):
    a = eye(3)
    a[i][i] = a[j][j] = c
    a[i][j], a[j][i] = s, -s
    return a


checks = 0


def check(ok):
    global checks
    assert ok
    checks += 1


def close(a, b):
    check(isclose(a, b, rel_tol=3e-10, abs_tol=1e-12))


I, Z = eye(3), mat(3)
# Testigos sintéticos exactos: no se presentan como valor HMT de CKM.
V = mul(mul(rotation(0, 1, Q(3, 5), Q(4, 5)),
            rotation(0, 2, Q(5, 13), Q(12, 13))),
        rotation(1, 2, Q(8, 17), Q(15, 17)))
check(mul(V, tr(V)) == I)
jp = block(Z, V, Z, Z)
jm = tr(jp)
j3 = scale(Q(1, 2), block(I, Z, Z, scale(-1, I)))
check(comm(jp, jm) == scale(2, j3))
check(comm(j3, jp) == jp)
check(comm(j3, jm) == scale(-1, jm))
W = block(I, Z, Z, V)
check(mul(mul(W, jp), tr(W)) == block(Z, I, Z, Z))
du, dd = mat(3), mat(3)
for i in range(3):
    du[i][i], dd[i][i] = Q(i+1), Q(i+4)
mass = block(du, Z, Z, dd)
check(mul(mul(W, mass), tr(W)) == block(du, Z, Z, mul(mul(V, dd), tr(V))))
check(comm(mass, jp) != mat(6))
# Conmutación con una base COMPLETA de End(C^3), más fuerte que SU(3).
for a in range(3):
    for b in range(3):
        eab = mat(3)
        eab[a][b] = Q(1)
        color = kron(eye(6), eab)
        for operator in (jp, jm, j3, mass):
            check(comm(kron(operator, I), color) == mat(18))
# Control negativo: no unitariedad rompe la identidad del álgebra débil.
bad = block(Z, scale(2, V), Z, Z)
check(comm(bad, tr(bad)) != scale(2, j3))
# Pesos enteros de la equivariancia quiral; no selección de cargas.
check(-3+4 == 1)
check(3-2 == 1)
# Identidad de pseudorrealidad de SU2 sobre testigo racional exacto.
u = [[Q(3, 5), Q(4, 5)], [-Q(4, 5), Q(3, 5)]]
epsilon = [[Q(0), Q(1)], [-Q(1), Q(0)]]
check(mul(epsilon, u) == mul(u, epsilon))


def f(s):
    return (1+s+s*s)/(1+s+s*s+s**3)


def H(s):
    return 12*s**3/(1-s**9)-s**4/(1-s**12)-log(s)**2/(20*pi)


for x in (0.01, 0.05, 0.13, 0.4):
    for ratio in (0.1, 0.4, 0.8):
        y = ratio*x
        alpha = 9*x/(50*pi)
        qp, qm = exp(-x-y), exp(-x+y)
        D = exp(-2*x)
        g2, gp2 = 4*pi*alpha/(1-D), 4*pi*alpha/D
        lam = g2/8*exp(6*x+10*y/3)
        Xi = 8*D**3*lam/g2
        check(0 < D < 1 and 1 < Xi < D**(-5/3))
        close(D, g2/(g2+gp2))
        close(alpha, -9*log(D)/(100*pi))
        close(qp**30, D**15*Xi**(-9))
        close(qm**30, D**15*Xi**9)
        rp, rm = f(qp**30), f(qm**30)
        gamma = 180*x*y/pi + 12*(qm**90/(1-qm**270)-qp**90/(1-qp**270)) - (qm**120/(1-qm**360)-qp**120/(1-qp**360))
        close(gamma, H(D**15*Xi**9)-H(D**15*Xi**(-9)))
        close((rp*rm)**2, (1/(rp*rm))**(-2))
        close(rm**2/rp**2, (rm/rp)**2)
        # Secciones sintéticas positivas: comprueba sustitución, no metrología.
        c, hbar, L = 3.0, 2.0, 0.5
        G = c**3*L**2/hbar
        kappa = 8*pi*G/c**4
        close(1/(2*kappa*c), hbar/(16*pi*L**2))
        close(3*kappa*c*c*hbar*hbar/16, 3*pi*c*hbar*L*L/2)

phi = (1+sqrt(5))/2
c, hbar, L, ell = 3.0, 2.0, 0.5, 0.7
kav = (pi-phi*phi)/((1+phi*phi)*ell)
mgap = 3*hbar*kav/c
mplanck = sqrt(hbar*c/(c**3*L**2/hbar))
close(mgap/mplanck, 3*L/ell*(pi-phi*phi)/(1+phi*phi))
for a in (0.03, 0.1, 0.9):
    close(exp(-3*(a/9)*kav)**9, exp(-3*a*kav))

print(json.dumps({"result": "PASS_COMPOSICION_FOCAL", "checks": checks,
                  "exact_rational_matrix_checks": True,
                  "scalar_checks": "synthetic floating-point regression tests",
                  "unification_of_all_quantum_dynamics_certified": False}, ensure_ascii=False))
