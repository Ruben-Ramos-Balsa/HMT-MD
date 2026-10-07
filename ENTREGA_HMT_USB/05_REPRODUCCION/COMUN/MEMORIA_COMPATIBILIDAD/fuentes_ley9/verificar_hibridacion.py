"""Controles exactos focales; no certifican generadores o identificaciones físicas.

Biblioteca estándar. No lee datos metrológicos ni escribe archivos.
"""
from fractions import Fraction as F
import json


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def tr(a):
    return [list(row) for row in zip(*a)]


def add(*arrays):
    return [[sum(a[i][j] for a in arrays) for j in range(2)] for i in range(2)]


def diag(a, b):
    return [[a, F(0)], [F(0), b]]


def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def f(s):
    return (1 - s**3) / (1 - s**4)


counts = {"masa_frecuencia_radios": 0, "convexidad_respuesta": 0,
          "transporte_discreto": 0, "invariante_diferencial": 0,
          "positividad_determinante": 0, "pesos_termicos": 0,
          "transporte_accion_normalizada": 0}
zero = diag(F(0), F(0))
falsifiers = {"omitir_conexion": False, "invertir_signo_conexion": False,
              "promediar_antes_de_respuesta": False, "omitir_prefactor_electronico": False}

for h in (F(2, 3), F(7, 5), F(11, 4)):
    for w in (F(3, 5), F(2), F(9, 7)):
        for c in (F(4, 3), F(8, 5)):
            for be in (F(2, 7), F(3, 2)):
                for chi in (F(3, 8), F(5, 4)):
                    for ratio in (F(6, 5), F(9, 8)):
                        for kappa in (-2, 0, 3):
                            xi = be * chi * ratio**kappa
                            m = h * w * xi / c**2
                            energy = m * c**2
                            radius = c / w
                            grav = c**3 * radius**2 / h
                            rg = grav * m / c**2
                            wavelength = h / (m * c)
                            assert energy / h == w * xi
                            assert rg == radius * xi
                            assert wavelength == radius / xi
                            assert rg * wavelength == radius**2
                            assert (chi * ratio**kappa) != xi
                            falsifiers["omitir_prefactor_electronico"] = True
                            counts["masa_frecuencia_radios"] += 1

# a=exp(-30x), b=exp(-30y); comparación exacta sin logaritmos.
for denominator in range(3, 20):
    for numerator in range(1, denominator):
        a = F(numerator, denominator)
        for b in (F(1), F(2, 3), F(3, 4), F(4, 5), F(5, 6)):
            if a < b <= 1:
                left, right = f(a*b) * f(a/b), f(a)**2
                assert left <= right
                assert (left == right) == (b == 1)
                if b < 1:
                    falsifiers["promediar_antes_de_respuesta"] = left < right
                counts["convexidad_respuesta"] += 1

for d0 in (F(1, 3), F(2, 3), F(1), F(2), F(5, 2)):
    for d1 in (F(1, 4), F(3, 4), F(1), F(3), F(7, 2)):
        for t in (F(0), F(1, 3), F(1), F(5, 3), F(2)):
            co, si = (1-t*t)/(1+t*t), 2*t/(1+t*t)
            rot = [[co, si], [-si, co]]
            transport = mm(mm(diag(d1, 1/d1), rot), diag(1/d0, d0))
            g0, g1 = diag(1/d0**2, d0**2), diag(1/d1**2, d1**2)
            assert mm(mm(tr(transport), g1), transport) == g0
            assert det(transport) == 1
            counts["transporte_discreto"] += 1
            for scale in (F(1, 2), F(1), F(3, 2)):
                conformal = [[scale*v for v in row] for row in transport]
                expected = [[scale**2*v for v in row] for row in g0]
                assert mm(mm(tr(conformal), g1), conformal) == expected
                assert det(conformal) == scale**2
                counts["transporte_accion_normalizada"] += 1

for d in (F(1, 3), F(2, 3), F(1), F(2), F(5, 2)):
    for w in (F(1, 2), F(1), F(7, 3)):
        for rate in (F(-5), F(-1), F(0), F(1), F(5)):
            g = diag(1/d**2, d**2)
            gdot = diag(-rate/d**2, rate*d**2)
            for sign in (1, 0, -1):
                lmat = [[sign*rate/2, w*d**2], [-w/d**2, -sign*rate/2]]
                defect = add(gdot, mm(tr(lmat), g), mm(g, lmat))
                if sign == 1:
                    assert defect == zero
                    counts["invariante_diferencial"] += 1
                elif rate:
                    assert defect != zero
                    falsifiers["omitir_conexion" if sign == 0 else "invertir_signo_conexion"] = True
            hessian = [[w/d**2, rate/2], [rate/2, w*d**2]]
            assert det(hessian) == w*w-rate*rate/4
            assert (det(hessian) > 0) == (abs(rate) < 2*w)
            counts["positividad_determinante"] += 1

# Casos enteros para comprobar exactamente la normalización ternaria.
for size in range(2, 10):
    weights = [F(1, 3**i) for i in range(size)]
    multiplicities = [i+1 for i in range(size)]
    z = sum(g*v for g, v in zip(multiplicities, weights))
    probabilities = [g*v/z for g, v in zip(multiplicities, weights)]
    assert sum(probabilities) == 1
    for i in range(size):
        for j in range(size):
            assert (probabilities[j]/multiplicities[j]) / (probabilities[i]/multiplicities[i]) == F(3)**(i-j)
            counts["pesos_termicos"] += 1

assert all(falsifiers.values())
print(json.dumps({"status": "PASS_CONTROLES_FOCALES_HIBRIDACION",
                  "arithmetic": "rational_exact",
                  "counts": counts, "negative_controls": falsifiers,
                  "scope": "Controles finitos de identidades y desigualdades; pruebas generales en la nota. No certificación global ni interacción física nueva."},
                 ensure_ascii=False, indent=2))
