#!/usr/bin/env python3
"""Controles racionales finitos. No certifica una amplitud física."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json


def mat(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


def transpose(a):
    return tuple(zip(*a))


def add(a, b):
    return tuple(tuple(x + y for x, y in zip(ar, br))
                 for ar, br in zip(a, b))


def scale(c, a):
    return tuple(tuple(c * x for x in row) for row in a)


def mul(a, b):
    return tuple(tuple(sum(x * y for x, y in zip(row, col))
                       for col in transpose(b)) for row in a)


def trace(a):
    return sum(a[k][k] for k in range(len(a)))


def inv2(a):
    d = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if not d:
        raise ValueError("Matriz singular")
    return scale(1 / d, mat([[a[1][1], -a[0][1]],
                            [-a[1][0], a[0][0]]]))


def pair(a, b):
    return trace(mul(transpose(a), b))


def outer(a, b):
    return mul(a, transpose(b))


def quadratic(r, w):
    return mul(mul(transpose(r), w), r)[0][0]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--receipt", type=Path)
    args = p.parse_args()
    checks = []

    def equal(name, actual, expected):
        if actual != expected:
            raise RuntimeError(f"{name}: {actual!r} != {expected!r}")
        checks.append({"name": name, "passed": True})

    def different(name, actual, wrong):
        if actual == wrong:
            raise RuntimeError(f"Control negativo ineficaz: {name}")
        checks.append({"name": name, "passed": True,
                       "kind": "negative_control"})

    identity = mat([[1, 0], [0, 1]])
    zero = mat([[0, 0], [0, 0]])
    s = mat([[1, 0], [0, -1]])
    j = mat([[0, 1], [-1, 0]])
    h = mul(s, j)
    n = scale(F(1, 2), add(h, j))
    equal("TRIT_eliptico", mul(j, j), scale(-1, identity))
    equal("TRIT_hiperbolico", mul(h, h), identity)
    equal("TRIT_parabolico", mul(n, n), zero)
    v = mat([[1], [1]])
    g = scale(-2, outer(v, v))
    skew_g = scale(F(1, 2), add(g, scale(-1, transpose(g))))
    equal("ejemplo_representante_antihermitico_nulo", skew_g, zero)
    equal("respuesta_hiperbolica", pair(g, h), F(-4))
    equal("respuesta_parabolica", pair(g, n), F(-2))
    different("no_proyectar_boost_a_sector_unitario", pair(g, h),
              pair(skew_g, h))
    different("no_proyectar_nilpotente_a_sector_unitario", pair(g, n),
              pair(skew_g, n))

    matrices = [
        identity, mat([[2, 1], [0, 1]]),
        mat([[1, 0], [1, 2]]), mat([[3, 1], [1, 1]])
    ]
    tangents = [j, h, n, s, mat([[1, 2], [-3, 4]])]
    weights = [identity, mat([[2, 1], [1, 3]])]
    fields = [
        (mat([[1], [1]]), mat([[2], [2]])),
        (mat([[2], [-1]]), mat([[3], [4]]))
    ]
    for ui, u in enumerate(matrices):
        ui_inv = inv2(u)
        for ai, a in enumerate(tangents):
            du = mul(a, u)
            for wi, w in enumerate(weights):
                for fi, (fs, ft) in enumerate(fields):
                    name = f"U{ui}_A{ai}_W{wi}_F{fi}"
                    v = mul(u, fs)
                    r = add(ft, scale(-1, v))
                    q = mul(w, r)
                    dr = scale(-1, mul(du, fs))
                    # Coeficiente de epsilon en (r+eps*dr)^T W(r+eps*dr).
                    first_jet = (mul(mul(transpose(dr), w), r)[0][0]
                                 + mul(mul(transpose(r), w), dr)[0][0])
                    covector = -2 * mul(transpose(q), mul(a, v))[0][0]
                    g = scale(-2, outer(q, v))
                    equal(name + "_diferencial", first_jet, covector)
                    equal(name + "_representante", pair(g, a), covector)
                    am = F(7, 3)
                    current = 4 * am * mul(transpose(q), mul(a, v))[0][0]
                    equal(name + "_normalizacion_corriente",
                          -F(1, 2) * current, am * first_jet)

                    # Inversion por congruencia, incluida la derivada del peso.
                    rbar = scale(-1, mul(ui_inv, r))
                    wbar = mul(mul(transpose(u), w), u)
                    equal(name + "_energia_inversa", quadratic(rbar, wbar),
                          quadratic(r, w))
                    dinv = scale(-1, mul(ui_inv, a))
                    drbar = scale(-1, mul(dinv, ft))
                    dwbar = add(mul(mul(transpose(du), w), u),
                                mul(mul(transpose(u), w), du))
                    reverse_jet = (
                        2 * mul(mul(transpose(rbar), wbar), drbar)[0][0]
                        + quadratic(rbar, dwbar))
                    equal(name + "_diferencial_inverso",
                          reverse_jet, first_jet)

    # Regla del producto y pullback no unitario, en 2 incidencias.
    for bi, b in enumerate(matrices):
        b_inv = inv2(b)
        for ai, a in enumerate(tangents):
            g = mat([[2, -1], [3, 4]])
            pulled = mul(mul(transpose(b), g), transpose(b_inv))
            equal(f"pullback_B{bi}_A{ai}", pair(pulled, a),
                  pair(g, mul(mul(b, a), b_inv)))
            u1 = matrices[(bi + 1) % len(matrices)]
            a2 = tangents[(ai + 1) % len(tangents)]
            u_total = mul(b, u1)
            derivative = add(mul(mul(a2, b), u1),
                             mul(b, mul(a, u1)))
            expected = add(a2, mul(mul(b, a), b_inv))
            equal(f"producto_B{bi}_A{ai}",
                  mul(derivative, inv2(u_total)), expected)
    b = matrices[1]
    g = mat([[2, -1], [3, 4]])
    correct = mul(mul(transpose(b), g), transpose(inv2(b)))
    wrong = mul(mul(transpose(b), g), b)
    different("no_eliminar_inversa_en_pullback", correct, wrong)

    pairing = mat([[2, 1], [0, 3]])
    current = mat([[F(8, 3)], [-4]])
    sigma = mul(inv2(pairing), current)
    theta = mat([[F(1, 2)], [2]])
    equal("emparejamiento_conexion_corriente",
          mul(transpose(theta), mul(pairing, sigma)),
          mul(transpose(theta), current))
    equal("homogeneidad_cuadratica_covector",
          scale(9, outer(fields[0][0], fields[1][0])),
          outer(scale(3, fields[0][0]), scale(3, fields[1][0])))
    result = {
        "status": "PASS_CONTROLES_FINITOS_COMPOSICION_VARIACIONAL",
        "scope": "Instancias racionales reales de formulas finitas",
        "checks": checks,
        "count": len(checks),
        "physical_amplitude_certified": False,
        "global_hmt_certification": False,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    if args.receipt:
        args.receipt.write_text(json.dumps(result, indent=2) + "\n",
                                encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "checks"}))


if __name__ == "__main__":
    main()
