#!/usr/bin/env python3
"""Análisis posterior del calendario de vacancias, no generador de constantes.

Enumera los intervalos de fase de una palabra mecánica; ilustra la prueba
analítica de NOTA.md. Decimal no certifica una pendiente irracional infinita.
Se repite el cálculo con dos precisiones y se enumeran palabras completas
en los tamaños pequeños. No consulta ni modifica los manuscritos.
"""
import argparse
import json
import math
from decimal import Decimal, ROUND_FLOOR, localcontext
from fractions import Fraction as F
from itertools import product
from pathlib import Path


def floor(x):
    return int(x.to_integral_value(rounding=ROUND_FLOOR))


def frac(x):
    return x - floor(x)


def entropy(probabilities):
    return -math.fsum(float(p) * math.log2(float(p))
                      for p in probabilities if p > 0)


def check_app_mode():
    """Exact downstream recovery of the documented APP incidence sector."""
    matrix = [[0] * 9 for _ in range(9)]
    dr = lambda x: 1 + (x - 1) % 9
    for x, y, z in product(range(1, 10), repeat=3):
        matrix[dr(x + y + z) - 1][dr(x * y * z) - 1] += 1
    columns = [sum(row[b] for row in matrix) for b in range(9)]
    assert all(sum(row) == 81 for row in matrix)
    assert columns == [36, 36, 108, 36, 36, 108, 36, 36, 297]
    mode = [1, -1, 0] * 3
    # Active components all have normalization sqrt(81*36)=54.
    for a in range(9):
        assert sum(F(matrix[a][b] * mode[b], 54)
                   for b in range(9) if mode[b]) == -F(mode[a], 2)
    for b in range(9):
        numerator = sum(matrix[a][b] * mode[a] for a in range(9))
        assert numerator == -27 * mode[b]  # zero in the other columns
    gram = [[sum(F(matrix[a][b] * matrix[c][b], 81 * columns[b])
                 for b in range(9)) for c in range(9)] for a in range(9)]
    eigens = [(F(1), [1] * 9), (F(1, 4), mode),
              (F(7, 132), [1, 1, -2] * 3)]
    for support, eigen in [([2, 5, 8], F(1, 18)),
                           ([0, 3, 6], F(0)), ([1, 4, 7], F(0))]:
        for end in support[1:]:
            vector = [0] * 9
            vector[support[0]], vector[end] = 1, -1
            eigens.append((eigen, vector))
    for eigen, vector in eigens:
        assert all(sum(gram[a][b] * vector[b] for b in range(9))
                   == eigen * vector[a] for a in range(9))
    # The three class-constant vectors and two differences on each disjoint
    # class form a basis. Hence all nine spectral modes are accounted for.
    assert len(eigens) == 9
    assert max(eigen * (1 - eigen) for eigen, _ in eigens) == F(3, 16)
    j = [[F(0), F(1)], [F(-1), F(0)]]
    assert [[sum(j[a][c] * j[c][b] for c in range(2))
             for b in range(2)] for a in range(2)] == [[-1, 0], [0, -1]]
    return {"triples_APP": 729, "arithmetic": "exact rational",
            "selector_mode": mode, "singular_value": "1/2",
            "commutator_norm_squared": "3/16", "J_squared": "-I",
            "scope": "incidence and local algebra only; not physical mass or charge"}


def evaluate(n, precision):
    with localcontext() as ctx:
        ctx.prec = precision
        zero, one = Decimal(0), Decimal(1)
        delta = (Decimal(10) / Decimal(9)).ln() / Decimal(10).ln()
        cuts = sorted({frac(-k * delta) for k in range(n + 1)} | {one})
        assert cuts[0] == 0 and len(cuts) == n + 2
        gaps = [b - a for a, b in zip(cuts, cuts[1:])]
        assert all(g > 0 for g in gaps)
        assert abs(sum(gaps) - one) < Decimal(10) ** (10 - precision)
        count_weights = {}
        words = {}
        for a, b in zip(cuts, cuts[1:]):
            phase = (a + b) / 2
            total = floor(n * delta + phase) - floor(phase)
            count_weights[total] = count_weights.get(total, zero) + b - a
            if n <= 108:
                word = tuple(floor((k + 1) * delta + phase)
                             - floor(k * delta + phase) for k in range(n))
                assert all(z in (0, 1) for z in word)
                assert sum(word) == total
                assert word not in words
                words[word] = b - a
                # Each oriented increment is exactly recoverable from its
                # current coordinate, once the common delta is retained.
                currents = [Decimal(z) - delta for z in word]
                assert all(j + delta == z for j, z in zip(currents, word))
                assert abs(sum(currents) - (total - n * delta)) < Decimal(10) ** (10 - precision)
        assert set(count_weights) == {floor(n * delta), floor(n * delta) + 1}
        if words:
            assert len(words) == n + 1
        h_word = entropy(gaps)
        h_count = entropy(count_weights.values())
        h_hidden = h_word - h_count
        assert 0 <= h_count <= 1 + 1e-12
        assert h_hidden >= h_word - 1 - 1e-12
        assert h_word <= math.log2(n + 1) + 1e-12
        assert h_word >= -math.log2(float(max(gaps))) - 1e-12
        return {
            "n": n, "admissible_words": len(gaps),
            "balance_values": sorted(count_weights),
            "H_word_bits": h_word, "H_balance_bits": h_count,
            "H_chronology_given_balance_bits": h_hidden,
            "H_word_per_step": h_word / n,
            "max_phase_interval": float(max(gaps)),
            "enumerated_full_words": len(words),
            "mean_square_current": float(delta * (1 - delta)),
        }


def check_k_orientation():
    """K is a published output received for a downstream observability test."""
    k = [234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601]
    shift = lambda x, j: x[j:] + x[:j]
    forward, backward = shift(k, 1), shift(k, 11)
    orbit = [[F(k[(i + j) % 12]) for j in range(12)] for i in range(12)]
    augmented = [row + [F(forward[i]), F(backward[i])]
                 for i, row in enumerate(orbit)]
    determinant = F(1)
    for col in range(12):
        pivot_row = next(i for i in range(col, 12) if augmented[i][col])
        if pivot_row != col:
            augmented[col], augmented[pivot_row] = augmented[pivot_row], augmented[col]
            determinant *= -1
        pivot = augmented[col][col]
        determinant *= pivot
        augmented[col] = [entry / pivot for entry in augmented[col]]
        for row in range(12):
            if row != col:
                coefficient = augmented[row][col]
                augmented[row] = [a - coefficient * b
                                  for a, b in zip(augmented[row], augmented[col])]
    assert determinant == 5483119259214020183850397930008283625
    recovered = [[augmented[i][12 + j] for i in range(12)] for j in range(2)]
    assert recovered == [[F(i == 1) for i in range(12)],
                         [F(i == 11) for i in range(12)]]
    autocorrelation = lambda x: [sum(x[i] * x[(i + j) % 12] for i in range(12))
                                for j in range(12)]
    assert autocorrelation(forward) == autocorrelation(backward) == autocorrelation(k)
    squared_distance = sum((a - b) ** 2 for a, b in zip(forward, backward))
    assert squared_distance == 2175744
    return {"arithmetic": "exact integer/rational",
            "determinant_O_K": str(determinant),
            "equal_power_spectra_via_autocorrelation": True,
            "squared_response_distance": squared_distance,
            "recovered_shift_indices": [1, 11],
            "scope": "published K as downstream reference; not full TPK dynamics"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows = []
    for n in (9, 108, 1000, 10000):
        a, b = evaluate(n, 70), evaluate(n, 100)
        for key in a:
            if isinstance(a[key], float):
                assert abs(a[key] - b[key]) < 1e-11, (n, key)
            else:
                assert a[key] == b[key], (n, key)
        rows.append(b)
    report = {
        "scope": "Calendario simbólico con fase uniforme; análisis posterior",
        "status": "COMPROBACIONES_FINITAS_SATISFACTORIAS",
        "precision_digits": [70, 100],
        "infinite_statement": "Demostración analítica en NOTA.md; no inferida del cálculo",
        "not_certified": ["generación de constantes", "masa/carga física", "disipación térmica", "entropía del TPK completo"],
        "results": rows,
        "APP_exact_checks": check_app_mode(),
        "K_orientation_checks": check_k_orientation(),
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
