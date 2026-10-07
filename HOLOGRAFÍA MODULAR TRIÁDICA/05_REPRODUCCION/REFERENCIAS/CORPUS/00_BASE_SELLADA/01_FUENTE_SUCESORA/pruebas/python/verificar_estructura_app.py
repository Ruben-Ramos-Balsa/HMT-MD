"""Verificación independiente de las identidades estructurales de APP.

El programa usa únicamente la biblioteca estándar. Los censos conjuntos de
los observables suma y producto se calculan por recurrencia sobre 81 estados,
sin enumerar 9**d palabras cuando d es grande.
"""
from __future__ import annotations
import json
import math
from collections import deque
from fractions import Fraction
from itertools import product
from pathlib import Path
OUT = Path(__file__).resolve().parents[2] / 'certificados' / 'estructura_app.json'

def dr9(n: int) -> int:
    return 1 + (n - 1) % 9

def det3(a: list[list[int]]) -> int:
    return a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0]) + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])

def joint_counts(d: int) -> list[list[int]]:
    counts = [[0] * 9 for _ in range(9)]
    counts[0][1] = 1
    for _ in range(d):
        nxt = [[0] * 9 for _ in range(9)]
        for s in range(9):
            for p in range(9):
                c = counts[s][p]
                if not c:
                    continue
                for x in range(9):
                    nxt[(s + x) % 9][p * x % 9] += c
        counts = nxt
    return counts

def connected_support(n: list[list[int]]) -> bool:
    graph = [set() for _ in range(18)]
    for s in range(9):
        for p in range(9):
            if n[s][p]:
                graph[s].add(9 + p)
                graph[9 + p].add(s)
    seen = {0}
    q = deque([0])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
    return len(seen) == 18

def jacobi_eigenvalues(a: list[list[float]], tolerance: float=1e-15) -> list[float]:
    """Eigenvalues of a real symmetric 9x9 matrix by Jacobi rotations."""
    a = [row[:] for row in a]
    n = len(a)
    for _ in range(20000):
        (p, q) = max(((i, j) for i in range(n) for j in range(i + 1, n)), key=lambda ij: abs(a[ij[0]][ij[1]]))
        if abs(a[p][q]) < tolerance:
            break
        phi = 0.5 * math.atan2(2.0 * a[p][q], a[q][q] - a[p][p])
        (c, s) = (math.cos(phi), math.sin(phi))
        (app, aqq, apq) = (a[p][p], a[q][q], a[p][q])
        for k in range(n):
            if k in (p, q):
                continue
            (akp, akq) = (a[k][p], a[k][q])
            a[k][p] = a[p][k] = c * akp - s * akq
            a[k][q] = a[q][k] = s * akp + c * akq
        a[p][p] = c * c * app - 2 * s * c * apq + s * s * aqq
        a[q][q] = s * s * app + 2 * s * c * apq + c * c * aqq
        a[p][q] = a[q][p] = 0.0
    return sorted((a[i][i] for i in range(n)), reverse=True)

def commutator_norm(d: int) -> float:
    n = joint_counts(d)
    rows = [sum(row) for row in n]
    cols = [sum((n[s][p] for s in range(9))) for p in range(9)]
    c = [[n[s][p] / math.sqrt(rows[s] * cols[p]) for p in range(9)] for s in range(9)]
    cct = [[sum((c[i][k] * c[j][k] for k in range(9))) for j in range(9)] for i in range(9)]
    eigenvalues = jacobi_eigenvalues(cct)
    candidates = [math.sqrt(max(0.0, x * (1.0 - x))) for x in eigenvalues]
    return max(candidates)

def rational_cct(d: int) -> list[list[Fraction]]:
    """Matriz C C^T exacta asociada a la tabla conjunta de dimensión d."""
    n = joint_counts(d)
    rows = [sum(row) for row in n]
    cols = [sum((n[s][p] for s in range(9))) for p in range(9)]
    return [[sum((Fraction(n[i][p] * n[j][p], rows[i] * cols[p]) for p in range(9)), Fraction(0)) for j in range(9)] for i in range(9)]

def matrix_product(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Fraction(0)) for j in range(len(b[0]))] for i in range(len(a))]

def characteristic_coefficients(a: list[list[Fraction]]) -> list[Fraction]:
    """Coeficientes exactos por Faddeev--LeVerrier.

    Devuelve los coeficientes de det(lambda I-A), comenzando por el término
    mónico. Toda la aritmética se realiza con Fraction.
    """
    size = len(a)
    b = [[Fraction(int(i == j)) for j in range(size)] for i in range(size)]
    coefficients = [Fraction(1)]
    for k in range(1, size + 1):
        ab = matrix_product(a, b)
        coefficient = -sum((ab[i][i] for i in range(size))) / k
        coefficients.append(coefficient)
        b = [[ab[i][j] + (coefficient if i == j else 0) for j in range(size)] for i in range(size)]
    return coefficients

def polynomial_from_roots(roots: list[Fraction]) -> list[Fraction]:
    coefficients = [Fraction(1)]
    for root in roots:
        nxt = [Fraction(0)] * (len(coefficients) + 1)
        for (i, coefficient) in enumerate(coefficients):
            nxt[i] += coefficient
            nxt[i + 1] -= root * coefficient
        coefficients = nxt
    return coefficients

def exact_commutator_data() -> dict[int, dict[str, object]]:
    spectra = {2: [Fraction(1), Fraction(5, 7), Fraction(1, 3), Fraction(1, 3), *[Fraction(0)] * 5], 3: [Fraction(1), Fraction(1, 4), Fraction(1, 18), Fraction(1, 18), Fraction(7, 132), *[Fraction(0)] * 4], 4: [Fraction(1), Fraction(643, 4716), Fraction(1, 108), Fraction(1, 108), *[Fraction(0)] * 5]}
    result: dict[int, dict[str, object]] = {}
    for (dimension, eigenvalues) in spectra.items():
        actual = characteristic_coefficients(rational_cct(dimension))
        expected = polynomial_from_roots(eigenvalues)
        if not actual == expected:
            raise AssertionError('comprobación ejecutable fallida')
        norm_squared = max((value * (1 - value) for value in eigenvalues))
        result[dimension] = {'eigenvalues': eigenvalues, 'commutator_norm_squared': norm_squared}
    if not result[2]['commutator_norm_squared'] == Fraction(2, 9):
        raise AssertionError('comprobación ejecutable fallida')
    if not result[3]['commutator_norm_squared'] == Fraction(3, 16):
        raise AssertionError('comprobación ejecutable fallida')
    if not result[4]['commutator_norm_squared'] == Fraction(2618939, 22240656):
        raise AssertionError('comprobación ejecutable fallida')
    return result

def primitive_orbit_lengths_mod_81() -> list[int]:
    """Órbitas exactas de H sobre pares no divisibles simultáneamente por 3."""
    modulus = 81
    h = ((3, 2), (4, 3))
    remaining = {(a, b) for a in range(modulus) for b in range(modulus) if not (a % 3 == 0 and b % 3 == 0)}
    lengths: list[int] = []
    while remaining:
        initial = next(iter(remaining))
        current = initial
        length = 0
        while True:
            remaining.discard(current)
            length += 1
            current = ((h[0][0] * current[0] + h[0][1] * current[1]) % modulus, (h[1][0] * current[0] + h[1][1] * current[1]) % modulus)
            if current == initial:
                break
            if not length <= 108:
                raise AssertionError('comprobación ejecutable fallida')
        lengths.append(length)
    return sorted(lengths)

def main() -> None:
    sigma = [[dr9(i + j) for j in range(1, 10)] for i in range(1, 10)]
    pi = [[dr9(i * j) for j in range(1, 10)] for i in range(1, 10)]
    if not sum(map(sum, sigma)) == 405:
        raise AssertionError('comprobación ejecutable fallida')
    if not sum(map(sum, pi)) == 459:
        raise AssertionError('comprobación ejecutable fallida')
    if not sum((i + j for i in range(1, 10) for j in range(1, 10))) == 810:
        raise AssertionError('comprobación ejecutable fallida')
    if not sum((i * j for i in range(1, 10) for j in range(1, 10))) == 2025:
        raise AssertionError('comprobación ejecutable fallida')
    if not 2025 - 810 == 459 - 405 + 9 * (174 - 45) == 1215:
        raise AssertionError('comprobación ejecutable fallida')
    classes = ([1, 4, 7], [2, 5, 8], [3, 6, 9])
    m_pi = [[sum((pi[i - 1][j - 1] for i in a for j in b)) // 9 for b in classes] for a in classes]
    m_sigma = [[sum((sigma[i - 1][j - 1] for i in a for j in b)) // 9 for b in classes] for a in classes]
    if not m_pi == [[4, 5, 6], [5, 4, 6], [6, 6, 9]]:
        raise AssertionError('comprobación ejecutable fallida')
    if not m_sigma == [[5, 6, 4], [6, 4, 5], [4, 5, 6]]:
        raise AssertionError('comprobación ejecutable fallida')
    if not det3(m_pi) == -9:
        raise AssertionError('comprobación ejecutable fallida')
    joint_visible = [[0] * 9 for _ in range(9)]
    for i in range(1, 10):
        for j in range(1, 10):
            joint_visible[dr9(i + j) - 1][dr9(i * j) - 1] += 1
    expected_joint_visible = [[0, 0, 2, 0, 0, 2, 3, 0, 2], [3, 0, 2, 0, 0, 2, 0, 0, 2], [0, 2, 0, 0, 2, 0, 0, 2, 3], [0, 0, 2, 3, 0, 2, 0, 0, 2], [0, 0, 2, 3, 0, 2, 0, 0, 2], [0, 2, 0, 0, 2, 0, 0, 2, 3], [3, 0, 2, 0, 0, 2, 0, 0, 2], [0, 0, 2, 0, 0, 2, 3, 0, 2], [0, 2, 0, 0, 2, 0, 0, 2, 3]]
    if not joint_visible == expected_joint_visible:
        raise AssertionError('comprobación ejecutable fallida')
    if not [sum(row) for row in joint_visible] == [9] * 9:
        raise AssertionError('comprobación ejecutable fallida')
    joint_column_sums = [sum((joint_visible[row][column] for row in range(9))) for column in range(9)]
    if not joint_column_sums == [6, 6, 12, 6, 6, 12, 6, 6, 21]:
        raise AssertionError('comprobación ejecutable fallida')
    equal_diagonal = []
    for k in range(1, 10):
        kp = dr9(k + 1)
        b = [[dr9(k * k), dr9(k * kp)], [dr9(kp * k), dr9(kp * kp)]]
        if b[0][0] == b[1][1]:
            equal_diagonal.append((k, b))
    if not equal_diagonal == [(4, [[7, 2], [2, 7]])]:
        raise AssertionError('comprobación ejecutable fallida')
    b = ((7, 2), (2, 7))
    eta = ((1, 0), (0, -1))
    bt_eta_b = tuple((tuple((sum((b[k][i] * eta[k][k] * b[k][j] for k in range(2))) for j in range(2))) for i in range(2)))
    if not bt_eta_b == ((45, 0), (0, -45)):
        raise AssertionError('comprobación ejecutable fallida')
    exact_spectra = exact_commutator_data()
    norms = {d: math.sqrt(float(exact_spectra[d]['commutator_norm_squared'])) for d in exact_spectra}
    connected = {d: connected_support(joint_counts(d)) for d in range(2, 16)}
    if not all(connected.values()):
        raise AssertionError('comprobación ejecutable fallida')
    h = ((3, 2), (4, 3))
    identity = ((1, 0), (0, 1))
    power = identity
    order = None
    for n in range(1, 1000):
        power = tuple((tuple((sum((power[i][k] * h[k][j] for k in range(2))) % 81 for j in range(2))) for i in range(2)))
        if power == identity:
            order = n
            break
    if not order == 108:
        raise AssertionError('comprobación ejecutable fallida')
    orbit_lengths = primitive_orbit_lengths_mod_81()
    if not len(orbit_lengths) == 54:
        raise AssertionError('comprobación ejecutable fallida')
    if not orbit_lengths == [108] * 54:
        raise AssertionError('comprobación ejecutable fallida')
    cube_vertices = list(product((-1, 1), repeat=3))
    cube_faces = [(axis, sign) for axis in range(3) for sign in (-1, 1)]
    cube_incidence = [[int(vertex[axis] == sign) for vertex in cube_vertices] for (axis, sign) in cube_faces]
    cube_row_sums = [sum(row) for row in cube_incidence]
    cube_column_sums = [sum((cube_incidence[row][column] for row in range(6))) for column in range(8)]
    if not cube_row_sums == [4] * 6:
        raise AssertionError('comprobación ejecutable fallida')
    if not cube_column_sums == [3] * 8:
        raise AssertionError('comprobación ejecutable fallida')
    if not sum(cube_row_sums) == sum(cube_column_sums) == 24:
        raise AssertionError('comprobación ejecutable fallida')
    cube_edges = sum((sum((left[i] != right[i] for i in range(3))) == 1 for (left_index, left) in enumerate(cube_vertices) for right in cube_vertices[left_index + 1:]))
    if not cube_edges == 12:
        raise AssertionError('comprobación ejecutable fallida')
    cube_gram = [[Fraction(sum((cube_incidence[i][column] * cube_incidence[j][column] for column in range(8)))) for j in range(6)] for i in range(6)]
    cube_spectrum = [Fraction(12), Fraction(4), Fraction(4), Fraction(4), Fraction(0), Fraction(0)]
    if not characteristic_coefficients(cube_gram) == polynomial_from_roots(cube_spectrum):
        raise AssertionError('comprobación ejecutable fallida')
    result = {'status': 'PASS', 'table_sums': {'Sigma': 405, 'Pi': 459}, 'quotient_sums': {'additive': 45, 'multiplicative': 174}, 'aggregated_matrices': {'Sigma': m_sigma, 'Pi': m_pi}, 'joint_visible_table': joint_visible, 'joint_visible_row_sums': [9] * 9, 'joint_visible_column_sums': joint_column_sums, 'number_of_oriented_paths': '81*4^r', 'det_M_Pi': -9, 'central_block': [[7, 2], [2, 7]], 'projector_commutator_norms': {str(d): {'squared_exact': str(exact_spectra[d]['commutator_norm_squared']), 'decimal': norms[d]} for d in norms}, 'support_graph_connected_d_2_to_15': all(connected.values()), 'pell_operator_order_mod_81': order, 'primitive_orbits_mod_81': {'number_of_orbits': len(orbit_lengths), 'common_length': orbit_lengths[0]}, 'cube_face_vertex_incidence': {'shape': [6, 8], 'row_sums': cube_row_sums, 'column_sums': cube_column_sums, 'flags': sum(cube_row_sums), 'edges': cube_edges, 'gram_spectrum': [str(value) for value in cube_spectrum], 'rank': 4, 'positive_rank_three_sector': 'opposite-face differences'}}
    serialized = json.dumps(result, indent=2, sort_keys=True) + '\n'
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(serialized, encoding='utf-8')
    print(serialized, end='')
if __name__ == '__main__':
    main()
