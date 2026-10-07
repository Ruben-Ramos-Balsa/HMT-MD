"""Verificación exacta de la pantalla 12→11→10 asociada a A5.

La acción de doce puntos se realiza sobre los cosets izquierdos A5/C5.  La
lista COS_REPS congela la biyección entre las doce posiciones dodecafásicas y
los cosets; por ello el proyector tridimensional y la norma de P3 K son
reproducibles y no dependen del orden de iteración de un conjunto de Python.
Todos los cálculos se efectúan en Q(sqrt(5)) mediante pares de fracciones.
"""
from __future__ import annotations
import itertools
import json
from fractions import Fraction
from pathlib import Path
Perm = tuple[int, ...]
Q5 = tuple[Fraction, Fraction]
ZERO: Q5 = (Fraction(0), Fraction(0))
ONE: Q5 = (Fraction(1), Fraction(0))
ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'certificados' / 'pantalla_a5.json'

def compose(p: Perm, q: Perm) -> Perm:
    return tuple((p[i] for i in q))

def inverse(p: Perm) -> Perm:
    result = [0] * len(p)
    for (i, value) in enumerate(p):
        result[value] = i
    return tuple(result)

def parity(p: Perm) -> int:
    return sum((p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))) % 2

def cycle_type(p: Perm) -> tuple[int, ...]:
    seen: set[int] = set()
    lengths: list[int] = []
    for initial in range(len(p)):
        if initial in seen:
            continue
        current = initial
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = p[current]
        if length > 1:
            lengths.append(length)
    return tuple(sorted(lengths, reverse=True)) or (1,)

def q5_add(x: Q5, y: Q5) -> Q5:
    return (x[0] + y[0], x[1] + y[1])

def q5_sub(x: Q5, y: Q5) -> Q5:
    return (x[0] - y[0], x[1] - y[1])

def q5_scale(x: Q5, scalar: Fraction | int) -> Q5:
    scalar = Fraction(scalar)
    return (x[0] * scalar, x[1] * scalar)

def q5_mul(x: Q5, y: Q5) -> Q5:
    return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])

def q5_inv(x: Q5) -> Q5:
    denominator = x[0] * x[0] - 5 * x[1] * x[1]
    if denominator == 0:
        raise ZeroDivisionError('elemento nulo de Q(sqrt(5))')
    return (x[0] / denominator, -x[1] / denominator)

def matmul(left: list[list[Q5]], right: list[list[Q5]]) -> list[list[Q5]]:
    rows = len(left)
    middle = len(right)
    columns = len(right[0])
    result = [[ZERO for _ in range(columns)] for _ in range(rows)]
    for i in range(rows):
        for k in range(middle):
            if left[i][k] == ZERO:
                continue
            for j in range(columns):
                result[i][j] = q5_add(result[i][j], q5_mul(left[i][k], right[k][j]))
    return result

def rank(matrix: list[list[Q5]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column] != ZERO), None)
        if pivot is None:
            continue
        (work[pivot_row], work[pivot]) = (work[pivot], work[pivot_row])
        inverse_pivot = q5_inv(work[pivot_row][column])
        work[pivot_row] = [q5_mul(value, inverse_pivot) for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or work[row][column] == ZERO:
                continue
            factor = work[row][column]
            work[row] = [q5_sub(value, q5_mul(factor, pivot_value)) for (value, pivot_value) in zip(work[row], work[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row
A5 = tuple((p for p in itertools.permutations(range(5)) if parity(p) == 0))
IDENTITY: Perm = tuple(range(5))
G5: Perm = (1, 2, 3, 4, 0)
subgroup_c5: set[Perm] = set()
power = IDENTITY
for _ in range(5):
    subgroup_c5.add(power)
    power = compose(G5, power)
COS_REPS: tuple[Perm, ...] = ((3, 2, 4, 1, 0), (3, 1, 0, 2, 4), (0, 1, 3, 4, 2), (1, 4, 2, 3, 0), (3, 2, 0, 4, 1), (4, 0, 1, 2, 3), (4, 3, 2, 1, 0), (0, 2, 3, 1, 4), (3, 1, 2, 4, 0), (2, 1, 4, 3, 0), (3, 4, 1, 2, 0), (4, 2, 1, 3, 0))
COSETS = tuple((frozenset((compose(representative, h) for h in subgroup_c5)) for representative in COS_REPS))
COSET_INDEX = {element: i for (i, coset) in enumerate(COSETS) for element in coset}

def conjugacy_class(element: Perm) -> frozenset[Perm]:
    return frozenset((compose(compose(h, element), inverse(h)) for h in A5))
CLASS_5A = conjugacy_class(G5)
CLASS_5B = conjugacy_class(compose(G5, G5))

def character_three(element: Perm) -> Q5:
    kind = cycle_type(element)
    if kind == (1,):
        return (Fraction(3), Fraction(0))
    if kind == (3,):
        return ZERO
    if kind == (2, 2):
        return (Fraction(-1), Fraction(0))
    if element in CLASS_5A:
        return (Fraction(1, 2), Fraction(1, 2))
    if element in CLASS_5B:
        return (Fraction(1, 2), Fraction(-1, 2))
    raise AssertionError('clase de conjugación desconocida')

def permutation_matrix(element: Perm) -> list[list[Q5]]:
    matrix = [[ZERO for _ in range(12)] for _ in range(12)]
    for (source, coset) in enumerate(COSETS):
        representative = next(iter(coset))
        target = COSET_INDEX[compose(element, representative)]
        matrix[target][source] = ONE
    return matrix

def projector_three() -> list[list[Q5]]:
    projector = [[ZERO for _ in range(12)] for _ in range(12)]
    for element in A5:
        coefficient = q5_scale(character_three(inverse(element)), Fraction(3, 60))
        action = permutation_matrix(element)
        for i in range(12):
            for j in range(12):
                if action[i][j] != ZERO:
                    projector[i][j] = q5_add(projector[i][j], coefficient)
    return projector

def q5_text(value: Q5) -> dict[str, str]:
    return {'rational': str(value[0]), 'sqrt5': str(value[1])}

def main() -> None:
    if not len(A5) == 60:
        raise AssertionError('comprobación ejecutable fallida')
    if not len(subgroup_c5) == 5:
        raise AssertionError('comprobación ejecutable fallida')
    if not len(COSETS) == 12:
        raise AssertionError('comprobación ejecutable fallida')
    if not all((len(coset) == 5 for coset in COSETS)):
        raise AssertionError('comprobación ejecutable fallida')
    if not len(COSET_INDEX) == 60:
        raise AssertionError('comprobación ejecutable fallida')
    projector = projector_three()
    if not projector == [list(row) for row in zip(*projector)]:
        raise AssertionError('comprobación ejecutable fallida')
    if not matmul(projector, projector) == projector:
        raise AssertionError('comprobación ejecutable fallida')
    trace = ZERO
    for i in range(12):
        trace = q5_add(trace, projector[i][i])
    if not trace == (Fraction(3), Fraction(0)):
        raise AssertionError('comprobación ejecutable fallida')
    if not rank(projector) == 3:
        raise AssertionError('comprobación ejecutable fallida')
    k = (234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601)
    mean = Fraction(sum(k), 12)
    centered = [(Fraction(value) - mean, Fraction(0)) for value in k]
    vector = [[value] for value in centered]
    projected = [row[0] for row in matmul(projector, vector)]
    norm = ZERO
    for value in projected:
        norm = q5_add(norm, q5_mul(value, value))
    expected = (Fraction(6638585, 20), Fraction(2275584, 20))
    if not norm == expected:
        raise AssertionError('comprobación ejecutable fallida')
    certificate = {'schema': 'HMT.pantalla.A5.exacta.v1', 'status': 'PASS', 'group_order': len(A5), 'subgroup_order': len(subgroup_c5), 'coset_count': len(COSETS), 'position_to_coset_representative': [list(item) for item in COS_REPS], 'projector': {'field': 'Q(sqrt(5))', 'symmetric': True, 'idempotent': True, 'trace': 3, 'rank': rank(projector)}, 'K_sum': sum(k), 'projected_norm_squared': q5_text(norm), 'screen_dimensions': {'uniform_complement': 11, 'polarized': 10}, 'scope': 'La norma depende de la biyección explícita entre las doce posiciones y los cosets A5/C5; una permutación simultánea transporta la construcción.'}
    OUTPUT.write_text(json.dumps(certificate, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps(certificate, ensure_ascii=False, indent=2, sort_keys=True))
    print('PASS_PANTALLA_A5')
if __name__ == '__main__':
    main()
