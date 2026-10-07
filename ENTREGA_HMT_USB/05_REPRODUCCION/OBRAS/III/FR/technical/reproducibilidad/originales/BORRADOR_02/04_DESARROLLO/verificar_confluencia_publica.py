#!/usr/bin/env python3
"""Public runner of the preserved 44 algebraic checks.

The original verifier is preserved next to this file. This derivative omits
only the documentary hash of an external predecessor PDF; all mathematical
checks and all resident-source hashes remain unchanged.
"""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json


def poly_add(a, b):
    c = dict(a)
    for m, v in b.items():
        c[m] = c.get(m, Q(0)) + v
    return {m: v for m, v in c.items() if v}


def scale(a, k):
    return {m: v * k for m, v in a.items() if v * k}


def mul(a, b):
    c = {}
    for m, v in a.items():
        for n, w in b.items():
            key = tuple(x + y for x, y in zip(m, n))
            c[key] = c.get(key, Q(0)) + v * w
    return {m: v for m, v in c.items() if v}


def uni(*coefficients):
    return {(i,): Q(v) for i, v in enumerate(coefficients) if v}


def derivative(a):
    return {(m[0] - 1,): m[0] * v for m, v in a.items() if m[0]}


def eval_uni(a, x):
    return sum((v * x ** m[0] for m, v in a.items()), Q(0))


checks = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


# Identidades polinómicas para todos los valores del argumento.
P, T = uni(1, 1, 1), uni(1, 1, 1, 1)
check("factorizacion_denominador", mul(uni(1, 1), uni(1, 0, 1)) == T)
check("cancelacion_3_4", mul(P, uni(1, -1)) == uni(1, 0, 0, -1)
      and mul(T, uni(1, -1)) == uni(1, 0, 0, 0, -1))
derivative_numerator = poly_add(mul(derivative(P), T), scale(mul(P, derivative(T)), -1))
check("numerador_derivada_F", derivative_numerator == uni(0, 0, -3, -2, -1))
check("Catalan_resolvente_vacio", mul(mul(P, uni(0, 1)), T)
      == mul(mul(P, uni(0, 1, 1)), uni(1, 0, 1)))
check("ecuacion_cubica_inversa", poly_add(T, scale(P, -1)) == uni(0, 0, 0, 1))

# log(s+)=-pi(A+C)/6, log(s-)=-pi(A-C)/6.
# Variables formales (A,C,pi); comprobación exacta del coeficiente angular.
lp = {(1, 0, 1): Q(-1, 6), (0, 1, 1): Q(-1, 6)}
lm = {(1, 0, 1): Q(-1, 6), (0, 1, 1): Q(1, 6)}
log_difference = poly_add(mul(lp, lp), scale(mul(lm, lm), -1))
check("diferencia_cuadrados_logaritmicos", log_difference == {(1, 1, 2): Q(1, 9)})
check("coeficiente_gamma", log_difference[(1, 1, 2)] / 20 == Q(1, 180))
check("residuo_dodecafasico", 12 * Q(1, 270) - Q(1, 360) == Q(1, 24))
check("rechazo_denominador_erroneo", 12 * Q(1, 90) - Q(1, 120) != Q(1, 24))
check("exponentes_s_q30", (90 // 30, 270 // 30, 120 // 30, 360 // 30) == (3, 9, 4, 12))

# Matriz de recuperación de las dos ocupaciones, sin hipótesis estadísticas.
incidence = ((1, 1), (90, 120))
inverse = ((Q(120, 30), Q(-1, 30)), (Q(-90, 30), Q(1, 30)))
check("inversa_incidencia", all(sum(inverse[i][k] * incidence[k][j] for k in range(2))
      == int(i == j) for i in range(2) for j in range(2)))

# Reducción exacta en Q[rho]/(rho^2-4rho+1): rho/(1+rho^2)=1/4.
check("Pell_segunda_derivada", poly_add(uni(1, 0, 1), uni(0, -4)) == uni(1, -4, 1))


def F(s):
    return eval_uni(P, s) / eval_uni(T, s)


def rational_H(s):
    return 12 * s ** 3 / (1 - s ** 9) - s ** 4 / (1 - s ** 12)


# Casos de regresión: distintos de las pruebas polinómicas generales anteriores.
fixtures = ((Q(1, 2), Q(1, 3)), (Q(2, 5), Q(3, 7)),
            (Q(7, 8), Q(1, 9)), (Q(1, 4), Q(1, 4)))
for i, (sp, sm) in enumerate(fixtures):
    rp, rm = F(sp), F(sm)
    z, c = rm / rp, 1 / (rp * rm)
    check(f"caso_{i}_dominio", Q(3, 4) < rp < 1 and Q(3, 4) < rm < 1
          and 1 < z * c < Q(16, 9) and Q(9, 16) < z / c < 1)
    for sign, s, r in (("plus", sp, rp), ("minus", sm, rm)):
        check(f"caso_{i}_cubica_{sign}", r * s ** 3 + (r - 1) * (s ** 2 + s + 1) == 0)
        check(f"caso_{i}_Catalan_{sign}", F(s) == (1 + s + s*s) / (s*(1+s)) * s/(1+s*s))
    check(f"caso_{i}_reconstruccion", rm*rm == z/c and rp*rp == 1/(z*c))
    check(f"caso_{i}_orientacion", (rp/rm)*(1/(rp*rm)) == (1/z)*c
          and rational_H(sm)-rational_H(sp) == -(rational_H(sp)-rational_H(sm)))
    check(f"caso_{i}_traza_orientada", rational_H(sm)-rational_H(sp)
          == -(rational_H(sp)-rational_H(sm)))

root = Path(__file__).resolve().parent.parent
paths = [Path(__file__).resolve(), Path(__file__).with_name("CONFLUENCIA_ESPECTRAL_Y_JERARQUIA_20260907.md")]
paths += [root / p for p in (
    "01_FUENTES/A07/capitulo_14_apertura_causal_accion_parangular.tex",
    "01_FUENTES/D06/INTERRELACIONES_ESTRUCTURALES_VACIO.md",
    "01_FUENTES/D07/RED_LECTORES_MOMENTOS_Y_SUSTITUCIONES.md",
    "01_FUENTES/B06/c51_barbero_area_informacion.tex",
    "01_FUENTES/B03/c43_operador_area.tex",
    "01_FUENTES/B04/parte_iv_area_hamiltoniano_memoria.tex",
    "manuscrito/main.tex",
)]
hashes = {str(p.relative_to(root)): sha256(p.read_bytes()).hexdigest() for p in paths}
print(json.dumps({
    "status": "PASS_LOCAL_IDENTIDADES_CONFLUENCIA_ESPECTRAL",
    "count": len(checks), "checks": checks,
    "scope": "Identidades polinomicas generales y regresiones racionales separadas. No prueba de generacion primaria, ni de identificaciones fisicas. Analisis, logaritmos y calculo funcional demostrados en la nota, no formalizados por este programa.",
    "sha256": hashes,
}, ensure_ascii=False, indent=2))
