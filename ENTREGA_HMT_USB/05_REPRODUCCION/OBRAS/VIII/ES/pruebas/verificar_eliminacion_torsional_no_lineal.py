#!/usr/bin/env python3
"""Control racional focal de la eliminación torsional no afín.

Sin entradas metrológicas, paquetes externos ni lectura de fuentes. Por defecto
escribe únicamente JSON en stdout. --receipt permite guardar ese mismo JSON.
Los ejemplos controlan las identidades del desarrollo, no una realización
material APP--TRIT--TPK ni una amplitud cosmológica.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as R
import json
from pathlib import Path


@dataclass(frozen=True)
class Jet:
    """Valor, primera derivada y segunda derivada exactos en un punto."""

    v: R
    d: R = R(0)
    dd: R = R(0)

    def __post_init__(self):
        object.__setattr__(self, "v", R(self.v))
        object.__setattr__(self, "d", R(self.d))
        object.__setattr__(self, "dd", R(self.dd))

    @staticmethod
    def lift(x):
        return x if isinstance(x, Jet) else Jet(R(x))

    def __add__(self, other):
        b = self.lift(other)
        return Jet(self.v + b.v, self.d + b.d, self.dd + b.dd)

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.v, -self.d, -self.dd)

    def __sub__(self, other):
        return self + (-self.lift(other))

    def __rsub__(self, other):
        return self.lift(other) - self

    def __mul__(self, other):
        b = self.lift(other)
        return Jet(self.v * b.v,
                   self.d * b.v + self.v * b.d,
                   self.dd * b.v + 2 * self.d * b.d + self.v * b.dd)

    __rmul__ = __mul__

    def reciprocal(self):
        if self.v == 0:
            raise ZeroDivisionError("Jet con valor nulo")
        return Jet(1 / self.v, -self.d / self.v**2,
                   2 * self.d**2 / self.v**3 - self.dd / self.v**2)

    def __truediv__(self, other):
        return self * self.lift(other).reciprocal()

    def __rtruediv__(self, other):
        return self.lift(other) / self


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), R(0))


def mulmv(a, b):
    return [dot(row, b) for row in a]


def inverse2(a):
    determinant = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / determinant, -a[0][1] / determinant],
            [-a[1][0] / determinant, a[0][0] / determinant]]


def verify():
    checks = []

    def require(name, condition, group):
        if not condition:
            raise RuntimeError("FAIL: " + name)
        checks.append({"name": name, "group": group})

    def equal(name, actual, expected, group):
        require(name, actual == expected, group)

    # Diferenciación por jets, independiente de las fórmulas cerradas de s y H.
    sample_k = [R(-3), R(-2), R(-1, 2), R(0), R(1, 3), R(1), R(2), R(4)]
    sample_lambda = [R(1, 4), R(1), R(25, 2)]
    for lam in sample_lambda:
        for k in sample_k:
            name = "lambda=" + str(lam) + ";k=" + str(k)
            kj = Jet(k, 1)
            energy = lam / (1 + kj * kj)
            current = 4 * lam * k / (1 + k*k)**2
            current_derivative = 4 * lam * (1 - 3*k*k) / (1 + k*k)**3
            total = kj * kj / 2 + energy
            equal(name + ":corriente", -2 * energy.d, current, "diferencial")
            equal(name + ":hessiano", energy.dd,
                  -current_derivative / 2, "diferencial")
            equal(name + ":ecuacion", total.d, k - current / 2, "diferencial")
            equal(name + ":hessiano_total", total.dd,
                  1 - current_derivative / 2, "diferencial")
            # Integral exacta mediante primitiva racional, no cuadratura decimal.
            primitive = lambda t: -2 * lam / (1 + t*t*k*k)
            integral = primitive(R(1)) - primitive(R(0))
            equal(name + ":teorema_fundamental",
                  -integral / 2, energy.v - lam, "integral_radial")
            if k != 0:
                tj = Jet(R(2, 3), 1)
                pj = -2 * lam / (1 + tj * tj * k*k)
                equal(name + ":derivada_primitiva", pj.d,
                      k * 4 * lam * (R(2, 3)*k) /
                      (1 + (R(2, 3)*k)**2)**2, "integral_radial")

    # Soluciones exactas del modelo no afín, con rango completo en todo R.
    lam = R(25, 2)
    for k in [R(-2), R(0), R(2)]:
        current = 4 * lam * k / (1+k*k)**2
        residual = k - current / 2
        q = k*k / 2
        f = lam / (1+k*k)
        delta = q + f - lam
        integral = 2 * lam * (1 - 1/(1+k*k))
        equal("raiz=" + str(k), residual, 0, "soluciones_no_afines")
        equal("identidad_radial=" + str(k),
              delta, k*current/4 - integral/2, "soluciones_no_afines")
        equal("campo_restringido=" + str(k),
              dot([R(1), k], [1/(1+k*k), k/(1+k*k)]), 1,
              "soluciones_no_afines")
        total = Jet(k, 1) * Jet(k, 1) / 2 + lam/(1+Jet(k, 1)*Jet(k, 1))
        equal("H_total=" + str(k), total.dd,
              R(-24) if k == 0 else R(16, 5), "soluciones_no_afines")
        if k != 0:
            equal("Delta_no_afin=" + str(k), delta, R(-8), "soluciones_no_afines")
            equal("lectura_afin=" + str(k), -k*current/4, R(-2), "control_negativo")
            require("no_sustituir_formula_afin=" + str(k),
                    delta != -k*current/4, "control_negativo")

    # Ecuación polinómica exacta: (1+k²)²-25=(k²-4)(k²+6).
    for k in sample_k:
        equal("factorizacion=" + str(k),
              (1+k*k)**2 - 25, (k*k-4)*(k*k+6), "soluciones_no_afines")
        require("factor_sin_raiz_real=" + str(k), k*k+6 > 0, "dominio")

    # Derivada implícita y de envolvente en una rama que varía realmente.
    # k=2, lambda=25/2; R_lambda=-2k/(1+k²)² y H=16/5.
    k = R(2)
    hessian = R(16, 5)
    residual_lambda = -2*k / (1+k*k)**2
    dk = -residual_lambda / hessian
    equal("derivada_rama", dk, R(1, 20), "envolvente")
    lj = Jet(lam, 1)
    kj = Jet(k, dk)
    delta_jet = kj*kj/2 + lj/(1+kj*kj) - lj
    equal("envolvente_con_rama_variable", delta_jet.d,
          R(1, 5)-1, "envolvente")
    equal("derivada_accion_reducida", delta_jet.d, R(-4, 5), "envolvente")
    # A(p) variable: a=A, F=lambda/(1+k²); derivada respecto de A en A=1.
    dk_da = -k/hessian
    aj = Jet(R(1), 1)
    kj = Jet(k, dk_da)
    full = aj*kj*kj/2 + lam/(1+kj*kj) - lam
    equal("envolvente_con_forma_gravitatoria_variable", full.d, k*k/2, "envolvente")

    # Caso afín: F=F0-sk/2 y Q=Ak²/2, para varios racionales.
    for a, s in [(R(2), R(3)), (R(-3), R(5)), (R(5, 2), R(-7, 3))]:
        ka = s/(2*a)
        correction = a*ka*ka/2 - s*ka/2
        equal("afin=" + str((a, s)), correction, -ka*s/4, "especializacion_afin")
        equal("afin_Q=" + str((a, s)), correction, -a*ka*ka/2, "especializacion_afin")

    # Producto positivo variable, incidencia/frontera/normalización variables.
    hj = [[Jet(3, 1), Jet(1, -2)], [Jet(1, -2), Jet(4, 3)]]
    cj = [Jet(2, 1), Jet(-1, 2)]
    bj, chij = Jet(2, 3), Jet(5, -1)
    hinvj = inverse2(hj)
    lj = dot(cj, mulmv(hinvj, cj))
    ej = chij * bj*bj / lj
    h = [[x.v for x in row] for row in hj]
    dh = [[x.d for x in row] for row in hj]
    c, dc = [x.v for x in cj], [x.d for x in cj]
    hinv = inverse2(h)
    ell = dot(c, mulmv(hinv, c))
    y = bj.v / ell
    f = [x*y for x in mulmv(hinv, c)]
    require("producto_positivo_menores", h[0][0] > 0 and
            h[0][0]*h[1][1]-h[0][1]*h[1][0] > 0, "dominio")
    require("gramiano_rango_completo", ell > 0, "dominio")
    equal("restriccion_producto_variable", dot(c, f), bj.v, "producto_variable")
    equal("energia_producto_variable", ej.v,
          chij.v*dot(f, mulmv(h, f)), "producto_variable")
    product_term = chij.v * dot(f, mulmv(dh, f))
    frozen_product = chij.d*bj.v*y + 2*chij.v*y*(bj.d-dot(dc, f))
    equal("diferencial_producto_variable_completo", ej.d,
          frozen_product + product_term, "producto_variable")
    require("producto_variable_no_omitir", product_term != 0 and
            ej.d != frozen_product, "control_negativo")

    groups = {}
    for item in checks:
        groups[item["group"]] = groups.get(item["group"], 0) + 1
    return {
        "status": "PASS_ELIMINACION_TORSIONAL_NO_LINEAL_RACIONAL",
        "arithmetic": "fractions.Fraction; jets de orden dos; sin floats",
        "checks": len(checks),
        "groups": groups,
        "example": {
            "lambda": "25/2", "stationary_points": ["-2", "0", "2"],
            "selected_for_test_only": "k=2",
            "hessian": "16/5", "delta_action": "-8",
            "affine_expression_not_applicable": "-2",
            "radial_integral": "20", "branch_derivative_lambda": "1/20",
            "reduced_action_derivative_lambda": "-4/5"
        },
        "proof_scope": [
            "Comprobaciones finitas independientes de los coeficientes del diferencial.",
            "Identidad de eliminación no afín y especialización afín en ejemplos exactos.",
            "Derivada métrica por envolvente: parámetros materiales y forma gravitatoria.",
            "Contribución del producto positivo variable y control negativo de su omisión."
        ],
        "not_certified_by_this_test": [
            "Selección física de una representación de rutas o de una acción material.",
            "Existencia global, unicidad global o paso al límite de una rama torsional.",
            "Identificación de una corriente como espín físico o evaluación de s_0.",
            "Signo o homogeneidad cosmológica de la densidad métrica HMT."
        ],
        "checks_detail": checks
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    result = verify()
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.receipt is not None:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
