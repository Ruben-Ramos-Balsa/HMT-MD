"""Controles focales posteriores a los lectores HMT; no genera constantes.

Parte exacta: identidades en Q[r,r^-1]. Parte numérica: puntos sintéticos de
la familia constitutiva, no datos experimentales ni estados HMT certificados.
La prueba general de inversión está en CONTRAANGULO_ELECTRON_BARBERO_CATALAN.md.
"""
from fractions import Fraction as F
import json
import math


def p(c=0, k=0):
    return {k: F(c)} if c else {}


def add(a, b):
    c = a.copy()
    for k, v in b.items():
        c[k] = c.get(k, F(0)) + v
    return {k: v for k, v in c.items() if v}


def mul(a, b):
    c = {}
    for k, v in a.items():
        for j, w in b.items():
            c[k+j] = c.get(k+j, F(0)) + v*w
    return {k: v for k, v in c.items() if v}


def mm(a, b):
    return [[add(mul(a[i][0], b[0][j]), mul(a[i][1], b[1][j]))
             for j in range(2)] for i in range(2)]


def ma(a, b):
    return [[add(a[i][j], b[i][j]) for j in range(2)] for i in range(2)]


def tr(a):
    return [list(x) for x in zip(*a)]


zero = [[p(), p()], [p(), p()]]
identity = [[p(1), p()], [p(), p(1)]]
g = [[p(1, -2), p()], [p(), p(1, 2)]]
gi = [[p(1, 2), p()], [p(), p(1, -2)]]
np = [[p(F(1, 2)), p(F(1, 2), 2)],
      [p(F(-1, 2), -2), p(F(-1, 2))]]
nm = [[p(F(1, 2)), p(F(-1, 2), 2)],
      [p(F(1, 2), -2), p(F(-1, 2))]]
j = [[p(), p(1)], [p(-1), p()]]
je = [[p(), p(1, 2)], [p(-1, -2), p()]]
exact = {
    "nilpotencia_mas": mm(np, np) == zero,
    "nilpotencia_menos": mm(nm, nm) == zero,
    "anticomutador_unidad": ma(mm(np, nm), mm(nm, np)) == identity,
    "adjunto_metrico": mm(mm(gi, tr(np)), g) == nm,
    "compatibilidad_geometrica": mm(g, je) == j,
    "metrica_inversa": mm(g, gi) == identity,
}
assert all(exact.values())


def f(s):
    return (1+s+s*s)/(1+s+s*s+s**3)


def psi(r):
    assert 0.75 < r < 1
    lo, hi = 0.0, 1.0
    for _ in range(70):
        mid = (lo+hi)/2
        if f(mid) > r:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2


def h(s):
    # π aquí evalúa un lector analítico posterior en pruebas sintéticas.
    return 12*s**3/(1-s**9)-s**4/(1-s**12)-math.log(s)**2/(20*math.pi)


def gamma(rp, rm):
    return h(psi(rm))-h(psi(rp))


def invert(c, gam):
    bound = min(math.log(c), math.log(16/(9*c)))
    lo, hi = -bound, bound
    for _ in range(65):
        z = (lo+hi)/2
        rp, rm = math.exp(-z/2)/math.sqrt(c), math.exp(z/2)/math.sqrt(c)
        if gamma(rp, rm) > gam:
            lo = z
        else:
            hi = z
    z = (lo+hi)/2
    return math.exp(-z/2)/math.sqrt(c), math.exp(z/2)/math.sqrt(c)


points = [0.79, 0.83, 0.88, 0.93, 0.97]
worst = 0.0
checks = 0
for rp in points:
    for rm in points:
        c = 1/(rp*rm)
        gam = gamma(rp, rm)
        ap, am = invert(c, gam)
        err = max(abs(ap-rp), abs(am-rm))
        worst = max(worst, err)
        assert err < 2e-12, (rp, rm, err)
        sp, sm = psi(rp), psi(rm)
        qp, qm = sp**(1/30), sm**(1/30)
        x = -math.log(qp*qm)/2
        y = math.log(qm/qp)/2
        adeg, cdeg = 180*x/math.pi, 180*y/math.pi
        angular = math.pi*adeg*cdeg/180
        logarithmic = (math.log(sp)**2-math.log(sm)**2)/(20*math.pi)
        assert math.isclose(angular, logarithmic, rel_tol=1e-10, abs_tol=1e-12)
        assert math.isclose(adeg, -3*math.log(sp*sm)/math.pi, abs_tol=1e-11)
        assert math.isclose(cdeg, 3*math.log(sm/sp)/math.pi, abs_tol=1e-11)
        assert math.isclose(gamma(rm, rp), -gam, abs_tol=1e-12)
        checks += 1

# Componente racional de la prueba de H'>0, evaluada exactamente.
positive_checks = 0
for n in range(1, 100):
    s = F(n, 100)
    ratio = (9/s)*(1+2*s**9)/(1+2*s**12)*((1-s**12)/(1-s**9))**2
    assert ratio > 9
    positive_checks += 1

print(json.dumps({
    "status": "PASS_CONTROLES_FOCALES_COMPOSICION",
    "exact_laurent_identities": exact,
    "synthetic_inverse_cases": checks,
    "max_absolute_channel_error": worst,
    "exact_rational_derivative_checks": positive_checks,
    "scope": "Identidades locales exactas y diagnósticos de la inversión; prueba general en Markdown. No certificación global HMT ni metrología.",
}, ensure_ascii=False, indent=2))
