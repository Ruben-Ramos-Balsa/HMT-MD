"""Certifica por aritmética entera el teorema de paridad de las firmas.

Reconstruye los factores invariantes mediante divisores determinantales:
Delta_k es el máximo común divisor de todos los menores de orden k y
d_k=Delta_k/Delta_(k-1). El JSON publicado no se usa como evidencia.
"""
from __future__ import annotations
import csv
import itertools
import json
import math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'datos' / 'firmas_enteras_diez_especies.csv'
COORDINATES = ('nA', 'sC', 'k_D4', 'nu120', 'nu270')

def determinant(matrix: list[list[int]]) -> int:
    """Determinante exacto por eliminación de Bareiss."""
    n = len(matrix)
    if n == 0:
        return 1
    work = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for pivot_index in range(n - 1):
        pivot_row = next((row for row in range(pivot_index, n) if work[row][pivot_index]), None)
        if pivot_row is None:
            return 0
        if pivot_row != pivot_index:
            (work[pivot_index], work[pivot_row]) = (work[pivot_row], work[pivot_index])
            sign = -sign
        pivot = work[pivot_index][pivot_index]
        for i in range(pivot_index + 1, n):
            for j in range(pivot_index + 1, n):
                numerator = work[i][j] * pivot - work[i][pivot_index] * work[pivot_index][j]
                if not numerator % previous == 0:
                    raise AssertionError('comprobación ejecutable fallida')
                work[i][j] = numerator // previous
            work[i][pivot_index] = 0
        previous = pivot
    return sign * work[-1][-1]

def smith_diagonal(generators: list[tuple[int, ...]]) -> list[int]:
    row_count = len(generators)
    column_count = len(generators[0])
    deltas = [1]
    for order in range(1, column_count + 1):
        divisor = 0
        for row_indices in itertools.combinations(range(row_count), order):
            for column_indices in itertools.combinations(range(column_count), order):
                minor = [[generators[row][column] for column in column_indices] for row in row_indices]
                divisor = math.gcd(divisor, abs(determinant(minor)))
                if divisor == 1:
                    break
            if divisor == 1:
                break
        if divisor == 0:
            raise AssertionError(f'rango menor que {order}')
        deltas.append(divisor)
    diagonal = [deltas[k] // deltas[k - 1] for k in range(1, len(deltas))]
    if not all((diagonal[k + 1] % diagonal[k] == 0 for k in range(len(diagonal) - 1))):
        raise AssertionError('comprobación ejecutable fallida')
    return diagonal

def main() -> None:
    with DATA.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    if not len(rows) == 10:
        raise AssertionError('comprobación ejecutable fallida')
    vectors = [tuple((int(row[column]) for column in COORDINATES)) for row in rows]
    if not [(vector[1] + vector[3]) % 2 for vector in vectors] == [1] * 10:
        raise AssertionError('comprobación ejecutable fallida')
    base = vectors[0]
    differences = [tuple((value - origin for (value, origin) in zip(vector, base))) for vector in vectors[1:]]
    non_electron = smith_diagonal(differences)
    electron_edges = smith_diagonal(vectors)
    if not non_electron == [1, 1, 1, 1, 2]:
        raise AssertionError('comprobación ejecutable fallida')
    if not electron_edges == [1, 1, 1, 1, 1]:
        raise AssertionError('comprobación ejecutable fallida')
    print(json.dumps({'status': 'PASS', 'species': len(vectors), 'electron_action_origin': [0, 0, 0, 0, 0], 'all_non_electron_parity': 1, 'non_electron_difference_smith_diagonal': non_electron, 'electron_edge_smith_diagonal': electron_edges}, sort_keys=True, indent=2))
if __name__ == '__main__':
    main()
