#!/usr/bin/env python3
"""Controles exactos de los modelos finitos de cola y pliegue.

No evalúa ceros ni certifica RH o la positividad global de Weil.
Verifica identidades de matrices racionales y conserva controles negativos.
La prueba en espacios de funciones reside en el capítulo 03, sección 12.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import sys


def transpose(a):
    return [list(row) for row in zip(*a)]


def multiply(a, b):
    bt = transpose(b)
    return [[sum((x*y for x, y in zip(row, col)), F()) for col in bt] for row in a]


def act(a, x):
    return [sum((v*w for v, w in zip(row, x)), F()) for row in a]


def dot(x, y):
    return sum((v*w for v, w in zip(x, y)), F())


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def scale(a, s):
    return [[s*x for x in row] for row in a]


def shift(x, k):
    n = len(x)
    return [x[(i-k) % n] for i in range(n)]


def fold(rows, shifts):
    moved = [shift(row, k) for row, k in zip(rows, shifts)]
    return [sum(col, F()) for col in zip(*moved)]


def quadratic(a, x):
    return dot(x, act(a, x))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    counts = {}

    def check(group, condition):
        if not condition:
            raise ArithmeticError("Fallo exacto: " + group)
        counts[group] = counts.get(group, 0) + 1

    # I-T_a sobre un soporte cuyos dos desplazamientos son disjuntos.
    for width in range(1, 10):
        for displacement in (width, width+1, 2*width, 3*width):
            b = [[F(0) for _ in range(width)] for _ in range(displacement+width)]
            for j in range(width):
                b[j][j] = F(1)
                b[j+displacement][j] = F(-1)
            bt = transpose(b)
            check("cola_gram", multiply(bt, b) == scale(identity(width), F(2)))
            left = scale(bt, F(1, 2))
            check("inversa_izquierda", multiply(left, b) == identity(width))
            check("inversa_norma", multiply(left, transpose(left)) ==
                  scale(identity(width), F(1, 2)))
            # N representa filas negativas acotadas; no son datos de Weil.
            n = identity(width) + [[F((-1)**j, j+1) for j in range(width)]]
            c = multiply(n, left)
            check("salida_completa", multiply(c, b) == n)
            check("norma_ambiental", multiply(c, transpose(c)) ==
                  scale(multiply(n, transpose(n)), F(1, 2)))
            for seed in range(3):
                f = [F((seed+2*j) % 7-3, j+1) for j in range(width)]
                bf = act(b, f)
                check("defecto_forma", dot(bf, bf)-dot(act(c, bf), act(c, bf)) ==
                      dot(bf, bf)-dot(act(n, f), act(n, f)))

    # Pliegue coherente: se conserva un término por cada par de rutas.
    for q in (0, 1, 2, 3):
        m = 9**q
        for dim in (2, 3, 5):
            shifts = [(j*j+q) % dim for j in range(m)]
            f = [F(2*j-3, j+2) for j in range(dim)]
            right = [[v/m for v in shift(f, -k)] for k in shifts]
            check("pliegue_sobreyectivo", fold(right, shifts) == f)
            check("inversa_derecha_norma",
                  sum((dot(row, row) for row in right), F()) == dot(f, f)/m)
            a = [[F(2 if i == j else (-1)**(i+j), i+j+1)
                  for j in range(dim)] for i in range(dim)]
            # La congruencia se comprueba con una forma hermítica no supuesta positiva.
            folded = fold(right, shifts)
            check("congruencia_forma", quadratic(a, folded) == quadratic(a, f))

    for q in (0, 1, 2):
        m = 9**q
        for dim in (2, 3, 5):
            shifts = [(j+q) % dim for j in range(m)]
            increments = [[(2*j+r*r) % dim for r in range(9)] for j in range(m)]
            rows = [[[F((j+2*r+i) % 11-5, i+r+2) for i in range(dim)]
                     for r in range(9)] for j in range(m)]
            coarse = [fold(rows[j], increments[j]) for j in range(m)]
            fine_rows = [row for children in rows for row in children]
            fine_shifts = [shifts[j]+increments[j][r]
                           for j in range(m) for r in range(9)]
            check("naturalidad_refinamiento",
                  fold(fine_rows, fine_shifts) == fold(coarse, shifts))

    # Cruces explícitos de nueve hijos, antes de aplicar la forma.
    for seed in range(12):
        dim = 3
        rows = [[F((seed+2*j+i) % 13-6, i+j+2) for i in range(dim)]
                for j in range(9)]
        moved = [shift(row, j) for j, row in enumerate(rows)]
        total = fold(rows, list(range(9)))
        a = [[F(1), F(2), F(0)], [F(2), F(1), F(-1)],
             [F(0), F(-1), F(3)]]
        crosses = sum((dot(x, act(a, y)) for x in moved for y in moved), F())
        check("todos_los_cruces", quadratic(a, total) == crosses)

    # Controles negativos: no son contraejemplos a Weil.
    v = [F(x) for x in (1, 1, 1, 0, 0, 0, -1, -1, -1)]
    difference = [x-y for x, y in zip(v, shift(v, 1))]
    check("falsador_primo_aislado",
          sum(v) == 0 and dot(difference, difference) == 6 and 2*dot(v, v) == 12)
    x, y = [F(1), F(0)], [F(1), F(0)]
    check("falsador_ortogonalizacion",
          dot(x, x)+dot(y, y) == 2 and dot([a+b for a, b in zip(x, y)],
                                         [a+b for a, b in zip(x, y)]) == 4)
    a = [[F(1), F(2)], [F(2), F(1)]]
    check("falsador_positividad_por_celdas",
          quadratic(a, [F(1), F(0)]) > 0 and
          quadratic(a, [F(0), F(1)]) > 0 and
          quadratic(a, [F(1), F(-1)]) == -2)
    report = {
        "status": "PASS_IDENTIDADES_FINITAS_COLA_Y_PLIEGUE",
        "scope": "Modelos matriciales racionales; pruebas analíticas en capítulo 03 §12",
        "checks": sum(counts.values()), "groups": counts,
        "python_optimized": bool(sys.flags.optimize),
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "negative_controls_are_not_weil_counterexamples": True,
        "global_weil_positivity_proved": False,
        "external_constant_targets_used": False,
    }
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(text)
    print(text)


if __name__ == "__main__":
    main()
