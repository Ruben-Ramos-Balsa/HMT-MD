#!/usr/bin/env python3
"""Controles racionales locales; no es una prueba de positividad de Weil."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys


def determinant(matrix):
    a = [row[:] for row in matrix]
    value = F(1)
    for k in range(len(a)):
        pivot = next((i for i in range(k, len(a)) if a[i][k]), None)
        if pivot is None:
            return F(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            value = -value
        diagonal = a[k][k]
        value *= diagonal
        for i in range(k + 1, len(a)):
            ratio = a[i][k] / diagonal
            for j in range(k + 1, len(a)):
                a[i][j] -= ratio * a[k][j]
            a[i][k] = F(0)
    return value


def run():
    counts = {}

    def check(group, actual, expected, context):
        if actual != expected:
            raise ArithmeticError(
                "%s: %s; obtenido %s, esperado %s"
                % (group, context, actual, expected)
            )
        counts[group] = counts.get(group, 0) + 1

    q = F(5, 9)
    # Dimensiones 1--13: 819 entradas y 13 determinantes.
    for size in range(1, 14):
        t = [[q ** abs(i - j) for j in range(size)] for i in range(size)]
        lower = [
            [q ** (i - j) if i >= j else F(0) for j in range(size)]
            for i in range(size)
        ]
        diagonal = [F(1)] + [1 - q * q] * (size - 1)
        for i in range(size):
            for j in range(size):
                entry = sum(
                    (lower[i][k] * diagonal[k] * lower[j][k] for k in range(size)),
                    F(0),
                )
                check("LDL_entries", entry, t[i][j], (size, i, j))
        check(
            "determinants", determinant(t), (1 - q * q) ** (size - 1), size
        )

    # No se representa sqrt(1-q^2): sus dos factores se multiplican exactamente.
    # n=0 comprueba tambien la norma truncada y su terminal.
    for length in range(1, 21):
        for shift in range(length):
            correlation = (1 - q * q) * sum(
                (q ** j * q ** (j + shift) for j in range(length - shift)), F(0)
            )
            expected = q ** shift * (1 - q ** (2 * (length - shift)))
            check("truncated_correlations", correlation, expected, (length, shift))

    for a in (F(2, 3), F(3, 4), F(1), F(2)):
        plus = -(a - F(1, 2)) / (a + F(1, 2))
        minus = -(a + F(1, 2)) / (a - F(1, 2))
        check("polar_reciprocal_factors", plus * minus, F(1), str(a))

    source = Path(__file__).resolve()
    return {
        "status": "PASS_IDENTIDADES_RACIONALES_LOCALES",
        "optimization_level": sys.flags.optimize,
        "python": sys.version.split()[0],
        "checks": counts,
        "checks_total": sum(counts.values()),
        "inputs": {"q": "5/9", "source": "normalizacion del bloque APP 9/5"},
        "scope": [
            "LDL y determinantes Toeplitz de memoria en dimensiones 1 a 13",
            "correlaciones truncadas y terminales hasta 20 posiciones",
            "reciprocidad de factores polares para cuatro parametros racionales",
        ],
        "not_certified": [
            "identificacion de los momentos de memoria con los momentos aritmeticos",
            "positividad global de la forma de Weil",
            "seleccion del Cayley auxiliar por el TPK",
        ],
        "script": source.name,
        "script_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, help="guardar recibo JSON focal")
    args = parser.parse_args()
    result = run()
    serialized = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.receipt is not None:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(serialized, encoding="utf-8")
    print(serialized, end="")


if __name__ == "__main__":
    main()
