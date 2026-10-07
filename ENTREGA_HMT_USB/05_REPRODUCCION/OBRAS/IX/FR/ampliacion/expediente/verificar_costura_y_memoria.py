#!/usr/bin/env python3
"""Controles racionales focales. No certifican la positividad global de Weil."""
from fractions import Fraction as F
import argparse
import json
from pathlib import Path
import sys

CHECKS = 0


def require(value, label):
    global CHECKS
    if not value:
        raise RuntimeError(label)
    CHECKS += 1


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def scale(a, c):
    return [[c * x for x in row] for row in a]


def add(a, b):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def sub(a, b):
    return add(a, scale(b, -1))


def power(a, n):
    out = eye(len(a))
    for _ in range(n):
        out = mul(out, a)
    return out


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def run():
    q = F(5, 9)
    bc = [[F(7), F(2)], [F(2), F(7)]]
    plus = [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]]
    minus = sub(eye(2), plus)
    require(bc == add(scale(plus, 9), scale(minus, 5)), "APP 9/5")
    require(1 - q*q == F(56, 81), "defecto radial")
    matrices = [eye(2), scale(eye(2), -1), scale(eye(2), 0),
                [[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]],
                [[F(2), F(1)], [F(0), F(1, 2)]],
                [[F(1), F(0)], [F(0), F(-1)]],
                [[F(1, 3), F(2, 7)], [F(-3, 2), F(4, 9)]]]
    for case, c in enumerate(matrices):
        s = [[F(0) for _ in range(18)] for _ in range(18)]
        for i in range(2):
            for j in range(2):
                s[i][16+j] = c[i][j]
        for k in range(1, 9):
            for i in range(2):
                s[2*k+i][2*(k-1)+i] = F(1)
        jmap = [[F(int(i % 2 == j), 3) for j in range(2)] for i in range(18)]
        jt = transpose(jmap)
        require(mul(jt, jmap) == eye(2), f"J isometría {case}")
        t = mul(mul(jt, s), jmap)
        require(t == scale(add(scale(eye(2), 8), c), F(1, 9)), f"compresión {case}")
        eta = mul(sub(eye(18), mul(jmap, jt)), mul(s, jmap))
        variance = mul(transpose(eta), eta)
        imc = sub(eye(2), c)
        require(variance == scale(mul(transpose(imc), imc), F(8, 81)), f"varianza {case}")
        costura = sub(eye(2), mul(transpose(c), c))
        require(sub(eye(2), mul(transpose(t), t)) == add(variance, scale(costura, F(1, 9))), f"balance completo {case}")
        require(mul(jt, eta) == [[F(0)]*2 for _ in range(2)], f"ortogonalidad {case}")
        expected = [[F(0) for _ in range(18)] for _ in range(18)]
        for k in range(9):
            for i in range(2):
                for j in range(2):
                    expected[2*k+i][2*k+j] = c[i][j]
        require(power(s, 9) == expected, f"vuelta completa {case}")
        if mul(transpose(c), c) == eye(2):
            terminal = eye(2)
            archive = scale(eye(2), 0)
            for n in range(1, 33):
                archive = add(archive, scale(eye(2), (1-q*q)*q**(2*(n-1))))
                terminal = scale(mul(transpose(power(c, n)), power(c, n)), q**(2*n))
                require(add(archive, terminal) == eye(2), f"terminal positivo {case}/{n}")

    # Control negativo focal: la varianza visible sigue siendo positiva aun
    # cuando el defecto de costura es negativo. No es un contraejemplo HMT.
    c = scale(eye(2), F(2))
    t = scale(add(scale(eye(2), 8), c), F(1, 9))
    require(trace(sub(eye(2), mul(transpose(t), t))) < 0, "no omitir defecto de costura")
    require(q**9 != q, "una vuelta no es nueve factores q")

    # Balance firmado antes de promoverlo a positividad: se verifica incluso
    # para una forma indefinida y su isometría hiperbólica racional.
    forms_and_maps = [
        (eye(2), [[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]]),
        ([[F(1), F(0)], [F(0), F(-1)]],
         [[F(5, 3), F(4, 3)], [F(4, 3), F(5, 3)]])]
    for case, (g, c) in enumerate(forms_and_maps):
        require(mul(mul(transpose(c), g), c) == g, f"isometría firmada {case}")
        t = scale(add(scale(eye(2), 8), c), F(1, 9))
        d = sub(eye(2), c)
        energy = lambda v: mul(mul(transpose(v), g), v)
        require(add(energy(t), scale(energy(d), F(8, 81))) == g,
                f"balance aritmético previo al signo {case}")
        archive = scale(g, 0)
        for n in range(1, 17):
            archive = add(archive, scale(energy(mul(d, power(t, n-1))), F(8, 81)))
            require(add(energy(power(t, n)), archive) == g,
                    f"telescopía firmada {case}/{n}")
    return {"status": "PASS_CONTROLES_RACIONALES_COSTURA_MEMORIA",
            "checks": CHECKS, "arithmetic": "exact rational",
            "optimization_level": sys.flags.optimize,
            "claims": ["identidad completa de costura", "archivo finito con terminal",
                       "separación fase/vuelta", "control de omisión del defecto",
                       "balance firmado nonádico y telescopía finita"],
            "global_weil_positivity_proved": False,
            "target_zero_heights_used": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    report = run()
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.receipt:
        args.receipt.write_text(rendered)
    print(rendered, end="")
