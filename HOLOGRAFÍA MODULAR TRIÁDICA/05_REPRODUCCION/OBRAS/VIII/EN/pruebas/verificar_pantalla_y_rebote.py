#!/usr/bin/env python3
"""Controles exactos de identidades de pantalla incorporadas al artículo VII.

Sólo biblioteca estándar. No genera constantes, no selecciona corriente física,
no calcula s0 y no certifica por sí solo la completitud del artículo.
El teorema de refinamiento a profundidad arbitraria reside en el manuscrito;
los casos finitos de este programa son controles de regresión.
"""
from fractions import Fraction as F
from itertools import product
import json
import sys


def mat(rows):
    return [[F(v) for v in row] for row in rows]


def identity(n):
    return mat([[int(i == j) for j in range(n)] for i in range(n)])


def transpose(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)]
            for row in a]


def add(a, b):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def scale(q, a):
    return [[q * x for x in row] for row in a]


def sub(a, b):
    return add(a, scale(-1, b))


def rank(a):
    a = [row[:] for row in a]
    r = 0
    for c in range(len(a[0])):
        p = next((i for i in range(r, len(a)) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        d = a[r][c]
        a[r] = [x / d for x in a[r]]
        for i in range(len(a)):
            if i != r:
                q = a[i][c]
                a[i] = [x - q * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def main():
    checks = []

    def check(name, condition):
        if not condition:
            raise ArithmeticError(name)
        checks.append({"name": name, "pass": True})

    faces = list(product(range(3), (-1, 1)))
    vertices = list(product((-1, 1), repeat=3))
    m = mat([[int(v[i] == sign) for v in vertices] for i, sign in faces])
    ident = identity(6)
    r = mat([[int(i == j and s == -t) for j, t in faces] for i, s in faces])
    pu = mat([[F(1, 6)] * 6 for _ in faces])
    pm = scale(F(1, 2), sub(ident, r))
    p0 = sub(scale(F(1, 2), add(ident, r)), pu)
    pq = add(pu, pm)
    gram = mul(m, transpose(m))
    check("incidencia_12Pu_4Pmenos", gram == add(scale(12, pu), scale(4, pm)))
    check("rangos_1_3_2_4", [rank(x) for x in (pu, pm, p0, gram)] == [1, 3, 2, 4])
    check("proyectores_ortogonales",
          all(mul(p, p) == p for p in (pu, pm, p0)) and
          mul(pu, pm) == scale(0, ident) and add(pq, p0) == ident)
    green = add(scale(F(1, 12), pu), scale(F(1, 4), pm))
    check("inversa_restringida", mul(gram, green) == pq == mul(green, gram))
    # ell = 1. W*W = 6 Pu + 2 Pmenos; todos los factores conmutan.
    w2 = add(scale(6, pu), scale(2, pm))
    response = scale(F(28, 243), add(pu, scale(3, pm)))
    defect = scale(F(56, 81), pq)
    check("congruencia_56_81", mul(w2, response) == defect)
    check("respuesta_green", response == scale(F(112, 81), green))
    check("compresion", 1 - F(5, 9) ** 2 == F(56, 81))
    # Operador de mínima extensión A = M^T (M M^T)|Q^{-1}.
    extension = mul(transpose(m), green)
    check("extension_resuelve", mul(m, extension) == pq)
    check("energia_minima", mul(transpose(extension), extension) == green)
    for depth in (0, 1, 2, 3, 8):
        factor = F(1, 9 ** depth) ** 2 * 81 ** depth
        check("refinamiento_factor_" + str(depth), factor == 1)
        check("traza_normalizada_" + str(depth),
              9 ** depth * F(1, 9 ** depth) * F(56, 81) == F(56, 81))
    # Caso racional de regresión del umbral: n=3(1+w), w=0;
    # rho0=2, s0=16, 8 pi G/3 normalizado a 1, ab=2.
    rho, spin, ab = F(2), F(16), F(2)
    f = lambda a: rho / a ** 3 - spin / a ** 6
    df = lambda a: -3 * rho / a ** 4 + 6 * spin / a ** 7
    check("umbral_regresion", f(ab) == 0 and df(ab) > 0)
    check("aceleracion_umbral", ab * df(ab) / 2 == F(3, 8))
    receipt = {
        "status": "PASS_IDENTIDADES_PANTALLA_Y_UMBRAL",
        "checks": checks,
        "checks_count": len(checks),
        "scope": "Identidades racionales de pantalla y un caso de umbral",
        "proof_of_arbitrary_depth_by_testing": False,
        "physical_current_evaluated": False,
        "torsional_amplitude_evaluated": False,
        "article_complete": False,
    }
    print(json.dumps(receipt, ensure_ascii=False, indent=2) if "--json" in sys.argv
          else receipt["status"] + " (" + str(len(checks)) + " controles exactos)")


if __name__ == "__main__":
    main()
