#!/usr/bin/env python3
"""Verificador focal exacto del fragmento 33 de VII.

Biblioteca estándar, aritmética racional, sin assert, red ni valores objetivo.
Matrices de Clifford, corriente, contracción de Holst, CAR y segundo momento.
La realización material, el orden normal y la celda homogénea son explícitos.
No identifica la acción de pantalla con Dirac ni selecciona un universo.
--json imprime el recibo; --receipt RUTA lo guarda además si se solicita.
"""

import argparse
import hashlib
import json
import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path


PASS = "PASS_CORRIENTE_ESPINORIAL_Y_DENSIDAD_FOCAL"
ETA = (-1, 1, 1, 1)
TRIPLES = tuple(combinations(range(4), 3))


def ident(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def zero(n):
    return [[F(0) for unused in range(n)] for unused in range(n)]


def transpose(a):
    return [list(column) for column in zip(*a)]


def scale(c, a):
    return [[c * v for v in row] for row in a]


def plus(a, b):
    return [[x + y for x, y in zip(row, other)] for row, other in zip(a, b)]


def minus(a, b):
    return plus(a, scale(-1, b))


def mul(a, b):
    return [[sum(x * y for x, y in zip(row, column))
             for column in zip(*b)] for row in a]


def comm(a, b):
    return minus(mul(a, b), mul(b, a))


def anti(a, b):
    return plus(mul(a, b), mul(b, a))


def tensor(a, b):
    return [[x * y for x in row_a for y in row_b]
            for row_a in a for row_b in b]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def permutation_sign(indices):
    if len(set(indices)) != len(indices):
        return 0
    return (-1) ** sum(indices[i] > indices[j]
                       for i in range(len(indices))
                       for j in range(i + 1, len(indices)))


def form_add(a, b, coefficient=F(1)):
    result = dict(a)
    for mask, value in b.items():
        result[mask] = result.get(mask, F(0)) + coefficient * value
    return {mask: value for mask, value in result.items() if value}


def wedge(a, b):
    result = {}
    for x, v in a.items():
        for y, w in b.items():
            if x & y:
                continue
            inversions = sum(i > j for i in range(4) for j in range(4)
                             if (x >> i) & 1 and (y >> j) & 1)
            mask = x | y
            result[mask] = result.get(mask, F(0)) + (-1) ** inversions * v * w
    return {mask: value for mask, value in result.items() if value}


def interior(i, form):
    return {mask ^ (1 << i): (-1) ** bin(mask & ((1 << i) - 1)).count("1") * v
            for mask, v in form.items() if (mask >> i) & 1}


def torsion_inverse(y):
    e = [{1 << i: F(1)} for i in range(4)]
    b = []
    for i in range(4):
        component = {}
        for j in range(4):
            component = form_add(component, interior(j, y[i][j]))
        b.append(component)
    contracted = {}
    for i in range(4):
        contracted = form_add(contracted, interior(i, b[i]), F(1, 4))
    return [form_add(b[i], wedge(e[i], contracted), F(-1)) for i in range(4)]


def spin_contraction(values, mode, current_multiplier=F(1)):
    """Coefficient of vol in -K sigma/4, after kappa*c=hbar=1.

    mode selects -star or identity; linearity proves the dependence on gamma.
    No sample value of gamma is needed for the coefficient calculation.
    """
    def bilinear(i, j, k):
        return permutation_sign((i, j, k)) * values.get(tuple(sorted((i, j, k))), F(0))

    lower = [[{} for unused in range(4)] for unused in range(4)]
    for j in range(4):
        for k in range(4):
            for i in range(4):
                lower[j][k] = form_add(
                    lower[j][k], interior(i, {15: F(1)}),
                    -F(1, 2) * current_multiplier * ETA[j] * ETA[k] * bilinear(i, j, k))
    upper = [[{mask: ETA[i] * ETA[j] * value for mask, value in lower[i][j].items()}
              for j in range(4)] for i in range(4)]
    y = [[{} for unused in range(4)] for unused in range(4)]
    for i in range(4):
        for j in range(4):
            if mode == "identity":
                y[i][j] = upper[i][j]
            else:
                sign = -1 if mode == "minus_star" else 1
                for k in range(4):
                    for l in range(4):
                        y[i][j] = form_add(y[i][j], upper[k][l],
                            sign * F(1, 2) * ETA[i] * ETA[j] * permutation_sign((i, j, k, l)))
    torsion = torsion_inverse(y)

    def component(i, j, k):
        if j == k:
            return F(0)
        return ETA[i] * (1 if j < k else -1) * torsion[i].get((1 << j) | (1 << k), F(0))

    result = {}
    for i in range(4):
        for j in range(4):
            contorsion = {1 << k: F(ETA[i] * ETA[j], 2) *
                         (component(k, i, j) - component(i, j, k) - component(j, k, i))
                         for k in range(4)}
            result = form_add(result, wedge(contorsion, lower[i][j]), -F(1, 4))
    return result.get(15, F(0))


class Checks:
    def __init__(self):
        self.counts = {}
        self.mutations = []

    def equal(self, group, got, expected, detail):
        if got != expected:
            raise ValueError("%s / %s: obtenido %r; esperado %r" % (group, detail, got, expected))
        self.counts[group] = self.counts.get(group, 0) + 1

    def reject(self, label, mutated, expected):
        if mutated == expected:
            raise ValueError("Mutación no detectada: " + label)
        self.mutations.append(label)


def run():
    check = Checks()
    i2 = ident(2)
    j2 = [[F(0), F(-1)], [F(1), F(0)]]
    r2 = [[F(0), F(1)], [F(1), F(0)]]
    z2 = [[F(1), F(0)], [F(0), F(-1)]]
    g = [tensor(j2, i2), tensor(r2, i2), tensor(z2, r2), tensor(z2, z2)]
    for i in range(4):
        for j in range(4):
            check.equal("Clifford", anti(g[i], g[j]),
                        scale(2 * ETA[i], ident(4)) if i == j else zero(4), (i, j))
    b = [[scale(F(ETA[i] * ETA[j], 4), comm(g[i], g[j]))
          for j in range(4)] for i in range(4)]
    pairs = tuple(combinations(range(4), 2))
    for i, j in pairs:
        for k in range(4):
            expected = plus(scale(int(j == k) * ETA[i], g[i]),
                            scale(-int(i == k) * ETA[j], g[j]))
            check.equal("Diferencial_Lorentz", comm(b[i][j], g[k]), expected, (i, j, k))
            triple = zero(4) if k in (i, j) else scale(ETA[i] * ETA[j], mul(g[k], mul(g[i], g[j])))
            check.equal("Corriente_trivector", anti(g[k], b[i][j]), triple, (i, j, k))
        for k, l in pairs:
            expected = plus(plus(scale(ETA[j] * int(j == k), b[i][l]),
                                 scale(-ETA[i] * int(i == k), b[j][l])),
                            plus(scale(-ETA[j] * int(j == l), b[i][k]),
                                 scale(ETA[i] * int(i == l), b[j][k])))
            check.equal("Algebra_Lorentz", comm(b[i][j], b[k][l]), expected, (i, j, k, l))
    # A_D=-i*g0: A_D is Hermitian iff g0 is antisymmetric;
    # A_D*gI is anti-Hermitian iff g0*gI is real symmetric.
    check.equal("Adjunto", transpose(g[0]), scale(-1, g[0]), "A_D")
    for i in range(4):
        check.equal("Adjunto", transpose(mul(g[0], g[i])), mul(g[0], g[i]), i)

    for mode in ("minus_star", "identity"):
        diagonal = []
        for triple in TRIPLES:
            expected = F(3, 16) * ETA[triple[0]] * ETA[triple[1]] * ETA[triple[2]] if mode == "minus_star" else F(0)
            got = spin_contraction({triple: F(1)}, mode)
            check.equal("Contraccion_exterior", got, expected, (mode, triple))
            diagonal.append(got)
        for i, j in combinations(range(4), 2):
            mixed = spin_contraction({TRIPLES[i]: F(1), TRIPLES[j]: F(1)}, mode)
            check.equal("Contraccion_exterior", mixed - diagonal[i] - diagonal[j], F(0), (mode, i, j))
    check.reject("suprimir_media_corriente", spin_contraction({TRIPLES[0]: F(1)}, "minus_star", F(2)), -F(3, 16))
    check.reject("invertir_signo_dualidad", spin_contraction({TRIPLES[0]: F(1)}, "plus_star"), -F(3, 16))

    annihilation = []
    for k in range(4):
        a = zero(16)
        for state in range(16):
            if (state >> k) & 1:
                a[state ^ (1 << k)][state] = F((-1) ** bin(state & ((1 << k) - 1)).count("1"))
        annihilation.append(a)
    creation = [transpose(a) for a in annihilation]
    for i in range(4):
        for j in range(4):
            check.equal("CAR", anti(annihilation[i], creation[j]), ident(16) if i == j else zero(16), ("mixed", i, j))
            check.equal("CAR", anti(annihilation[i], annihilation[j]), zero(16), ("aa", i, j))
            check.equal("CAR", anti(creation[i], creation[j]), zero(16), ("cc", i, j))

    elementary = [[mul(creation[i], annihilation[j]) for j in range(4)] for i in range(4)]

    def second(matrix):
        answer = zero(16)
        for i in range(4):
            for j in range(4):
                if matrix[i][j]:
                    answer = plus(answer, scale(matrix[i][j], elementary[i][j]))
        return answer

    def normal_real(matrix):
        answer = zero(16)
        entries = [(i, j, matrix[i][j]) for i in range(4) for j in range(4) if matrix[i][j]]
        for i, j, x in entries:
            for k, l, y in entries:
                answer = plus(answer, scale(-x * y, mul(mul(creation[i], creation[k]),
                                                    mul(annihilation[j], annihilation[l]))))
        return answer

    # M_abc=i*C_abc, so every product is evaluated over the rationals:
    # dGamma(M)^2=-dGamma(C)^2; M^2=-C^2=I.
    real_b = [tensor(j2, r2), tensor(j2, z2), tensor(i2, j2), tensor(z2, j2)]
    q = zero(16)
    raw_q = zero(16)
    observables_real = []
    for index, triple in enumerate(TRIPLES):
        cmat = real_b[index]
        expected = scale(-1, mul(g[0], mul(g[triple[0]], mul(g[triple[1]], g[triple[2]]))))
        check.equal("Bilineales", cmat, expected, (triple, "matrix"))
        check.equal("Bilineales", transpose(cmat), scale(-1, cmat), (triple, "Hermitian_iC"))
        check.equal("Bilineales", mul(cmat, cmat), scale(-1, ident(4)), (triple, "square"))
        check.equal("Bilineales", trace(cmat), F(0), (triple, "trace"))
        op = second(cmat)
        observables_real.append(op)
        direct = normal_real(cmat)
        check.equal("Orden_normal", direct, minus(mul(op, op), second(mul(cmat, cmat))), triple)
        weight = ETA[triple[0]] * ETA[triple[1]] * ETA[triple[2]]
        q = plus(q, scale(-weight, direct))
        raw_q = plus(raw_q, scale(-weight, mul(op, op)))
    number = second(ident(4))
    check.equal("Observable_cuartico", q, plus(raw_q, scale(2, number)), "normal_order")
    check.equal("Observable_cuartico", q, transpose(q), "self_adjoint")
    check.equal("Observable_cuartico", comm(q, number), zero(16), "number")
    sectors = {n: [state for state in range(16) if bin(state).count("1") == n] for n in range(5)}
    expected2 = [[0, 0, 0, 0, 0, -4], [0, 2, 0, 0, 6, 0], [0, 0, 2, -6, 0, 0],
                 [0, 0, -6, 2, 0, 0], [0, 6, 0, 0, 2, 0], [-4, 0, 0, 0, 0, 0]]
    for n, states in sectors.items():
        expected = expected2 if n == 2 else scale({0: 0, 1: 0, 3: 4, 4: 8}[n], ident(len(states)))
        check.equal("Sectores", [[q[i][j] for j in states] for i in states], expected, n)
    p3 = zero(16)
    for state in sectors[3]:
        p3[state][state] = F(1)
    rho3 = scale(F(1, 4), p3)
    check.equal("Estado_testigo", mul(p3, p3), p3, "projection")
    check.equal("Estado_testigo", trace(rho3), F(1), "trace")
    check.equal("Estado_testigo", trace(mul(rho3, q)), F(4), "quartic_moment")
    check.equal("Estado_testigo", trace(mul(rho3, number)), F(3), "occupation")
    for index, op in enumerate(observables_real):
        check.equal("Estado_testigo", trace(mul(rho3, op)), F(0), (index, "mean"))
        check.equal("Estado_testigo", -trace(mul(rho3, mul(op, op))), F(1), (index, "variance"))
    for i in sectors[3]:
        for j in sectors[3]:
            h = zero(16)
            h[i][j] = F(1)
            check.equal("Conservacion_sector_tres", comm(h, q), zero(16), (i, j))
    negative = (q[3][3] + q[12][12] + q[3][12] + q[12][3]) / 2
    check.equal("Signo_estado", negative, F(-4), "two_particle_counterexample")
    check.reject("omitir_orden_normal", raw_q[15][15], F(8))
    h = zero(16)
    h[3][5] = h[5][3] = F(1)
    check.equal("Conservacion_distinta", comm(h, number), zero(16), "H_number_preserving")
    check.reject("numero_implica_momento_cuartico", comm(h, q), zero(16))

    # Exact powers: reduced action N*c*C*q/(a^3*Vc).
    # Lapse derivative gives E=-c*C*q/(a^3*Vc);
    # a derivative divided by 3*N*a^2*Vc gives p=-c*C*q/(a^6*Vc^2).
    for a, vc, moment in ((F(2), F(3), F(4)), (F(3, 2), F(5, 2), F(-4))):
        energy = -moment / (a ** 3 * vc)
        density = energy / (a ** 3 * vc)
        pressure = (-3 * moment / (a ** 4 * vc)) / (3 * a ** 2 * vc)
        check.equal("Variacion_homogenea", density, -moment / (a ** 6 * vc ** 2), "density")
        check.equal("Variacion_homogenea", pressure, density, "pressure")
        check.reject("perder_cuadrado_volumen_%s" % vc, -moment / (a ** 6 * vc), density)
    # Dimensions (M,L,T): kappa=(-1,-1,2), c=(0,1,-1), hbar=(1,2,-1).
    kappa, c, hbar = (-1, -1, 2), (0, 1, -1), (1, 2, -1)
    cg = tuple(kappa[i] + c[i] + 2 * hbar[i] for i in range(3))
    s0 = tuple(cg[i] + c[i] - (6 if i == 1 else 0) for i in range(3))
    check.equal("Dimensiones", cg, (1, 4, -1), "C_gamma")
    check.equal("Dimensiones", s0, (1, -1, -2), "energy_density")
    return check


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent.parent / "manuscrito/33_corriente_espinorial_y_densidad.tex"
    receipt = {
        "schema": "hmt.vii.corriente_espinorial.focal.v1",
        "status": "FAIL_CORRIENTE_ESPINORIAL_Y_DENSIDAD_FOCAL",
        "source": "manuscrito/33_corriente_espinorial_y_densidad.tex",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest() if source.exists() else None,
        "arithmetic": "fractions.Fraction; M=i*C evaluado mediante matrices C racionales",
        "realization": ["Clifford (-+++), adjunto A_D=-i*g0", "acción Dirac mínima afín; campos fijos al variar conexión",
                        "Fock finita Lambda(C^4), vacío de ocupación y orden normal declarados",
                        "celda comóvil periódica Vc>0, modo homogéneo, observador fijado",
                        "G,c,hbar,gamma internos; gamma real no nulo; normalización kappa=8*pi*G/c^4"],
        "result": "s0[rho,Vc]=(3*kappa*c^2*hbar^2/16)*gamma^2/(1+gamma^2)*Tr(rho*Q)/Vc^2",
        "conservation_scope": "Q constante si su esperanza se conserva; probado Q=4I en N=3 y evolución que preserve ese sector",
        "not_certified": ["igualdad entre acción Dirac y acción de extensión mínima de pantalla",
                          "selección del estado de un universo observado o positividad de Q en todos los estados",
                          "conservación del cuarto momento por mera conservación de la ocupación media",
                          "derivación de todos los antecedentes HMT o verificación global del artículo"],
        "network_access": False,
    }
    try:
        check = run()
        receipt.update(status=PASS, identity_checks=sum(check.counts.values()), checks_by_group=check.counts,
                       mutation_checks=len(check.mutations), mutations_rejected=check.mutations)
    except Exception as error:
        receipt["error"] = "%s: %s" % (type(error).__name__, error)
    data = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True)
    if args.receipt:
        args.receipt.write_text(data + "\n", encoding="utf-8")
    if args.json:
        print(data)
    else:
        print(receipt["status"])
        print("Identidades: %s; mutaciones: %s" % (receipt.get("identity_checks", 0), receipt.get("mutation_checks", 0)))
        print("Alcance: corriente afín, contracción exacta y realización material finita explícita.")
    return 0 if receipt["status"] == PASS else 1


if __name__ == "__main__":
    sys.exit(main())
