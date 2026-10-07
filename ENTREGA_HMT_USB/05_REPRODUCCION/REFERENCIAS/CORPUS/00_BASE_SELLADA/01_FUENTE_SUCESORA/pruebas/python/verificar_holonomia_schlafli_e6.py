"""Certificado exacto APP--Heisenberg--Schläfli--E6.

La construcción primaria NO usa el grafo de Schläfli como entrada:

1. una polarización mixta declarada de los potenciales APP determina una
   clase alternante;
2. fijadas polarización, orientación central y gauge, se toma la extensión
   de Heisenberg estándar asociada y se reduce a H_3;
3. la sección simétrica es D(a,b)=(a,b,ab/2);
4. se toman todos los ocho desplazamientos D(a,b), (a,b) != (0,0), y
   las dos fases centrales no triviales.

Sólo después se calculan grado, números de vecinos comunes, identidad
cuadrática, triángulos, automorfismos e isomorfía con las 27 rectas.

El archivo usa únicamente la biblioteca estándar de Python. Escribe las
tablas en la carpeta de datos y el resultado en la de certificados.
"""
from __future__ import annotations
import csv
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Sequence, Set, Tuple
HERE = Path(__file__).resolve().parent
PACKAGE_ROOT = HERE.parents[1]
DATA_DIR = PACKAGE_ROOT / 'datos'
CERTIFICATE = PACKAGE_ROOT / 'certificados/holonomia_schlafli_e6.json'
SOURCE_PATHS = (
    'manuscrito/sections/hmt/03_app_ortograma.tex',
    'manuscrito/sections/hmt/15b_holonomia_schlafli_e6.tex',
)
H3Element = Tuple[int, int, int]
PairElement = Tuple[int, int]

def add3(x: int, y: int) -> int:
    return (x + y) % 3

def half3(x: int) -> int:
    """División por dos en F_3; 2^{-1}=2."""
    return 2 * x % 3

def h3_mul(p: H3Element, q: H3Element) -> H3Element:
    """Producto de H_3 en la convención Weyl del cierre APP.

    Si p=(a,b,z), q=(c,d,w), el término b*c es la reducción del cociclo
    que aparece en (X^a Z^b)(X^c Z^d).
    """
    (a, b, z) = p
    (c, d, w) = q
    return ((a + c) % 3, (b + d) % 3, (z + w + b * c) % 3)

def h3_inv(p: H3Element) -> H3Element:
    (a, b, z) = p
    return (-a % 3, -b % 3, (-z + a * b) % 3)

def weyl_section(a: int, b: int) -> H3Element:
    return (a % 3, b % 3, half3(a * b))

def canonical_connection_h3() -> Set[H3Element]:
    displacements = {weyl_section(a, b) for (a, b) in itertools.product(range(3), repeat=2) if (a, b) != (0, 0)}
    central_phases = {(0, 0, 1), (0, 0, 2)}
    return displacements | central_phases

def to_symmetric_coordinates(p: H3Element) -> H3Element:
    """Pasa del cociclo polarizado bc a la carta alternante simétrica."""
    (a, b, z) = p
    return (a, b, (z - half3(a * b)) % 3)

def from_symmetric_coordinates(p: H3Element) -> H3Element:
    (a, b, t) = p
    return (a, b, (t + half3(a * b)) % 3)

def linear_gauge(ell: Tuple[int, int], p: H3Element) -> H3Element:
    """Automorfismo central phi_ell(a,b,z)=(a,b,z+ell(a,b))."""
    (a, b, z) = p
    return (a, b, (z + ell[0] * a + ell[1] * b) % 3)

def gl2_matrices() -> List[Tuple[int, int, int, int]]:
    matrices = []
    for (a, b, c, d) in itertools.product(range(3), repeat=4):
        if (a * d - b * c) % 3:
            matrices.append((a, b, c, d))
    if not len(matrices) == 48:
        raise AssertionError('comprobación ejecutable fallida')
    return matrices

def h3_automorphism(matrix: Tuple[int, int, int, int], ell: Tuple[int, int], p: H3Element) -> H3Element:
    """Los 432 automorfismos (M,ell) en coordenadas alternantes."""
    (a, b, t) = to_symmetric_coordinates(p)
    (m00, m01, m10, m11) = matrix
    a2 = (m00 * a + m01 * b) % 3
    b2 = (m10 * a + m11 * b) % 3
    determinant = (m00 * m11 - m01 * m10) % 3
    t2 = (determinant * t + ell[0] * a + ell[1] * b) % 3
    return from_symmetric_coordinates((a2, b2, t2))

def verify_app_translation_holonomy() -> dict:
    """Cierra el Wilson general sin elegir una representación W(a,b).

    Las hojas se usan como potenciales de vértice y sus diferencias como
    enlaces. Para la mezcla S/P: A_x=Delta_x S=1, A_y=Delta_y P=x.
    La mezcla inversa intercambia ambos potenciales.
    """

    def ax_sp(x: int, y: int) -> int:
        return 1

    def ay_sp(x: int, y: int) -> int:
        return x % 9

    def ax_ps(x: int, y: int) -> int:
        return y % 9

    def ay_ps(x: int, y: int) -> int:
        return 1

    def curvature(ax: Callable[[int, int], int], ay: Callable[[int, int], int], x: int, y: int) -> int:
        return (ay((x + 1) % 9, y) - ay(x, y) - ax(x, (y + 1) % 9) + ax(x, y)) % 9

    def rectangle(ax: Callable[[int, int], int], ay: Callable[[int, int], int], x: int, y: int, width: int, height: int) -> int:
        value = 0
        for i in range(width):
            value += ax((x + i) % 9, y)
        for j in range(height):
            value += ay((x + width) % 9, (y + j) % 9)
        for i in range(width):
            value -= ax((x + i) % 9, (y + height) % 9)
        for j in range(height):
            value -= ay(x, (y + j) % 9)
        return value % 9

    def coordinate_path(dx: int, dy: int) -> List[Tuple[str, int, int, int]]:
        """Camino de (0,0) a (dx,dy): primero x y después y."""
        edges: List[Tuple[str, int, int, int]] = []
        x = y = 0
        for _ in range(dx):
            edges.append(('x', x % 9, y % 9, 1))
            x += 1
        for _ in range(dy):
            edges.append(('y', x % 9, y % 9, 1))
            y += 1
        return edges

    def translate_path(edges: Sequence[Tuple[str, int, int, int]], offset: Tuple[int, int]) -> List[Tuple[str, int, int, int]]:
        (ox, oy) = offset
        return [(axis, (x + ox) % 9, (y + oy) % 9, sign) for (axis, x, y, sign) in edges]

    def reverse_path(edges: Sequence[Tuple[str, int, int, int]]) -> List[Tuple[str, int, int, int]]:
        return [(axis, x, y, -sign) for (axis, x, y, sign) in reversed(edges)]

    def parallelogram(ax: Callable[[int, int], int], ay: Callable[[int, int], int], u: Tuple[int, int], v: Tuple[int, int]) -> int:
        """Circulación sobre gamma_u gamma_v gamma_u^-1 gamma_v^-1."""
        path_u = coordinate_path(*u)
        path_v = coordinate_path(*v)
        boundary = path_u + translate_path(path_v, u) + reverse_path(translate_path(path_u, v)) + reverse_path(path_v)
        return sum((sign * (ax(x, y) if axis == 'x' else ay(x, y)) for (axis, x, y, sign) in boundary)) % 9
    curvature_sp = {curvature(ax_sp, ay_sp, x, y) for x in range(9) for y in range(9)}
    curvature_ps = {curvature(ax_ps, ay_ps, x, y) for x in range(9) for y in range(9)}
    rectangle_sp = all((rectangle(ax_sp, ay_sp, x, y, a, b) == a * b % 9 for (x, y, a, b) in itertools.product(range(9), repeat=4)))
    rectangle_ps = all((rectangle(ax_ps, ay_ps, x, y, a, b) == -a * b % 9 for (x, y, a, b) in itertools.product(range(9), repeat=4)))
    parallelogram_sp = all((parallelogram(ax_sp, ay_sp, (a, b), (c, d)) == (a * d - b * c) % 9 for (a, b, c, d) in itertools.product(range(9), repeat=4)))
    parallelogram_ps = all((parallelogram(ax_ps, ay_ps, (a, b), (c, d)) == (b * c - a * d) % 9 for (a, b, c, d) in itertools.product(range(9), repeat=4)))
    if not (curvature_sp == {1} and curvature_ps == {8}):
        raise AssertionError('comprobación ejecutable fallida')
    if not (rectangle_sp and rectangle_ps and parallelogram_sp and parallelogram_ps):
        raise AssertionError('comprobación ejecutable fallida')
    return {'SP_curvature_mod9': 1, 'PS_curvature_mod9': -1, 'all_81_plaquettes_checked_per_order': True, 'all_6561_rectangles_checked_per_order': True, 'all_6561_parallelograms_checked_per_order': True, 'Wilson_SP_rectangle': 'a*b mod 9', 'Wilson_PS_rectangle': '-a*b mod 9', 'general_alternating_class': 'sigma((a,b),(c,d))=a*d-b*c mod 9', 'general_SP_boundary_sum': 'sigma(u,v)', 'general_PS_boundary_sum': '-sigma(u,v)', 'Weyl_representation_selected_by_this_check': False}

def cayley_adjacency(elements: Sequence[tuple], mul: Callable[[tuple, tuple], tuple], connection: Set[tuple]) -> List[List[int]]:
    index = {g: i for (i, g) in enumerate(elements)}
    adjacency = [[0 for _ in elements] for _ in elements]
    for (i, g) in enumerate(elements):
        for s in connection:
            adjacency[i][index[mul(g, s)]] = 1
    return adjacency

def matmul(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]) -> List[List[int]]:
    n = len(a)
    return [[sum((a[i][k] * b[k][j] for k in range(n))) for j in range(n)] for i in range(n)]

def graph_metrics(adjacency: Sequence[Sequence[int]]) -> dict:
    n = len(adjacency)
    degrees = [sum(row) for row in adjacency]
    common_adjacent: Counter[int] = Counter()
    common_nonadjacent: Counter[int] = Counter()
    for i in range(n):
        for j in range(i + 1, n):
            common = sum((adjacency[i][k] * adjacency[j][k] for k in range(n)))
            if adjacency[i][j]:
                common_adjacent[common] += 1
            else:
                common_nonadjacent[common] += 1
    triangles = sum((1 for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n) if adjacency[i][j] and adjacency[i][k] and adjacency[j][k]))
    regular = len(set(degrees)) == 1
    srg = regular and len(common_adjacent) == 1 and (len(common_nonadjacent) == 1)
    return {'vertices': n, 'degree_distribution': dict(sorted(Counter(degrees).items())), 'common_neighbors_adjacent': dict(sorted(common_adjacent.items())), 'common_neighbors_nonadjacent': dict(sorted(common_nonadjacent.items())), 'triangles': triangles, 'regular': regular, 'strongly_regular': srg, 'parameters': [n, degrees[0], next(iter(common_adjacent)), next(iter(common_nonadjacent))] if srg else None}

def triangles_of(adjacency: Sequence[Sequence[int]]) -> List[Tuple[int, int, int]]:
    n = len(adjacency)
    return [(i, j, k) for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n) if adjacency[i][j] and adjacency[i][k] and adjacency[j][k]]

def complement(adjacency: Sequence[Sequence[int]]) -> List[List[int]]:
    n = len(adjacency)
    return [[0 if i == j else 1 - adjacency[i][j] for j in range(n)] for i in range(n)]

def verify_quadratic_identities(adjacency: Sequence[Sequence[int]]) -> dict:
    n = len(adjacency)
    a2 = matmul(adjacency, adjacency)
    schlafli = complement(adjacency)
    b2 = matmul(schlafli, schlafli)
    identity_intersection = all((a2[i][j] == 5 * (i == j) - 4 * adjacency[i][j] + 5 for i in range(n) for j in range(n)))
    identity_complement = all((b2[i][j] == 8 * (i == j) + 2 * schlafli[i][j] + 8 for i in range(n) for j in range(n)))
    return {'A2_equals_5I_minus_4A_plus_5J': identity_intersection, 'B2_equals_8I_plus_2B_plus_8J': identity_complement}

def standard_line_labels() -> List[tuple]:
    labels: List[tuple] = [('E', i) for i in range(6)]
    labels.extend((('L', i, j) for (i, j) in itertools.combinations(range(6), 2)))
    labels.extend((('Q', i) for i in range(6)))
    return labels

def line_label_text(label: tuple) -> str:
    if label[0] in {'E', 'Q'}:
        return f'{label[0]}{label[1] + 1}'
    return f'L{label[1] + 1}{label[2] + 1}'

def lines_intersect(x: tuple, y: tuple) -> bool:
    if x == y:
        return False
    (tx, ty) = (x[0], y[0])
    if tx == ty == 'E' or tx == ty == 'Q':
        return False
    if tx == 'E' and ty == 'L':
        return x[1] in y[1:]
    if tx == 'L' and ty == 'E':
        return y[1] in x[1:]
    if tx == 'E' and ty == 'Q':
        return x[1] != y[1]
    if tx == 'Q' and ty == 'E':
        return y[1] != x[1]
    if tx == ty == 'L':
        return not set(x[1:]) & set(y[1:])
    if tx == 'L' and ty == 'Q':
        return y[1] in x[1:]
    if tx == 'Q' and ty == 'L':
        return x[1] in y[1:]
    raise AssertionError((x, y))

def standard_line_graph() -> Tuple[List[tuple], List[List[int]]]:
    labels = standard_line_labels()
    adjacency = [[int(lines_intersect(x, y)) for y in labels] for x in labels]
    return (labels, adjacency)

def local_data(adjacency: Sequence[Sequence[int]], base: int) -> tuple:
    n = len(adjacency)
    neighbors = [i for i in range(n) if adjacency[base][i]]
    remote = [i for i in range(n) if i != base and (not adjacency[base][i])]
    seen: Set[int] = set()
    matching: List[Tuple[int, int]] = []
    for u in neighbors:
        if u in seen:
            continue
        mate = next((v for v in neighbors if adjacency[u][v]))
        matching.append((u, mate))
        seen.update({u, mate})
    signatures = {r: frozenset((u for u in neighbors if adjacency[r][u])) for r in remote}
    return (neighbors, remote, matching, signatures)

def find_graph_isomorphism(source: Sequence[Sequence[int]], target: Sequence[Sequence[int]], source_base: int, target_base: int) -> Dict[int, int]:
    (_, source_remote, source_pairs, source_signatures) = local_data(source, source_base)
    (_, _, target_pairs, target_signatures) = local_data(target, target_base)
    signature_to_target = {signature: r for (r, signature) in target_signatures.items()}
    for pair_permutation in itertools.permutations(range(5)):
        for flip_mask in range(32):
            mapping = {source_base: target_base}
            for (i, (u, v)) in enumerate(source_pairs):
                (x, y) = target_pairs[pair_permutation[i]]
                if flip_mask >> i & 1:
                    (x, y) = (y, x)
                mapping[u] = x
                mapping[v] = y
            valid = True
            for r in source_remote:
                image_signature = frozenset((mapping[u] for u in source_signatures[r]))
                if image_signature not in signature_to_target:
                    valid = False
                    break
                mapping[r] = signature_to_target[image_signature]
            if not valid or len(set(mapping.values())) != len(source):
                continue
            if all((source[i][j] == target[mapping[i]][mapping[j]] for i in range(len(source)) for j in range(len(source)))):
                return mapping
    raise AssertionError('No se encontró la isomorfía')

def vertex_stabilizer_order(adjacency: Sequence[Sequence[int]], base: int=0) -> dict:
    (_, remote, matching, signatures) = local_data(adjacency, base)
    signature_to_remote = {signature: r for (r, signature) in signatures.items()}
    if not len(matching) == 5:
        raise AssertionError('comprobación ejecutable fallida')
    if not len(signature_to_remote) == 16:
        raise AssertionError('comprobación ejecutable fallida')
    if not {len(signature) for signature in signatures.values()} == {5}:
        raise AssertionError('comprobación ejecutable fallida')
    accepted = 0
    for pair_permutation in itertools.permutations(range(5)):
        for flip_mask in range(32):
            mapping = {base: base}
            for (i, (u, v)) in enumerate(matching):
                (x, y) = matching[pair_permutation[i]]
                if flip_mask >> i & 1:
                    (x, y) = (y, x)
                mapping[u] = x
                mapping[v] = y
            valid = True
            for r in remote:
                image_signature = frozenset((mapping[u] for u in signatures[r]))
                if image_signature not in signature_to_remote:
                    valid = False
                    break
                mapping[r] = signature_to_remote[image_signature]
            if not valid or len(set(mapping.values())) != len(adjacency):
                continue
            if all((adjacency[i][j] == adjacency[mapping[i]][mapping[j]] for i in range(len(adjacency)) for j in range(len(adjacency)))):
                accepted += 1
    return {'local_matching_permutations_tested': 120 * 32, 'identity_stabilizer_order': accepted, 'vertex_orbit_order_from_regular_H3_action': 27, 'full_automorphism_order': 27 * accepted, 'signature_separates_all_16_remote_vertices': True}

def group_inverse_pairs(elements: Sequence[tuple], identity: tuple, inv: Callable[[tuple], tuple]) -> List[Tuple[tuple, tuple]]:
    pairs: List[Tuple[tuple, tuple]] = []
    seen = {identity}
    for g in elements:
        if g in seen:
            continue
        h = inv(g)
        pairs.append((g, h))
        seen.update({g, h})
    if not len(pairs) == 13:
        raise AssertionError('comprobación ejecutable fallida')
    return pairs

def schlafli_cayley_connections(elements: Sequence[tuple], identity: tuple, mul: Callable[[tuple, tuple], tuple], inv: Callable[[tuple], tuple]) -> List[Set[tuple]]:
    """Exhausta los C(13,5)=1287 subconjuntos inverso-cerrados de grado 10."""
    inverse_pairs = group_inverse_pairs(elements, identity, inv)
    solutions: List[Set[tuple]] = []
    for indices in itertools.combinations(range(13), 5):
        connection: Set[tuple] = set()
        for i in indices:
            connection.update(inverse_pairs[i])
        counts = {g: sum((1 for s in connection if mul(g, s) in connection)) for g in elements}
        if all((counts[g] == (10 if g == identity else 1 if g in connection else 5) for g in elements)):
            solutions.append(connection)
    return solutions

def groups_of_order_27() -> List[dict]:
    c27 = list(range(27))
    c9c3 = list(itertools.product(range(9), range(3)))
    c3cubed = list(itertools.product(range(3), repeat=3))

    def semidirect_mul(x: PairElement, y: PairElement) -> PairElement:
        return ((x[0] + pow(4, x[1], 9) * y[0]) % 9, (x[1] + y[1]) % 3)

    def semidirect_inv(x: PairElement) -> PairElement:
        return next((y for y in c9c3 if semidirect_mul(x, y) == (0, 0) and semidirect_mul(y, x) == (0, 0)))
    return [{'name': 'C27', 'elements': c27, 'identity': 0, 'mul': lambda x, y: (x + y) % 27, 'inv': lambda x: -x % 27, 'abelian': True}, {'name': 'C9xC3', 'elements': c9c3, 'identity': (0, 0), 'mul': lambda x, y: ((x[0] + y[0]) % 9, (x[1] + y[1]) % 3), 'inv': lambda x: (-x[0] % 9, -x[1] % 3), 'abelian': True}, {'name': 'C3xC3xC3', 'elements': c3cubed, 'identity': (0, 0, 0), 'mul': lambda x, y: tuple(((a + b) % 3 for (a, b) in zip(x, y))), 'inv': lambda x: tuple((-a % 3 for a in x)), 'abelian': True}, {'name': 'C9_semidirect_C3', 'elements': c9c3, 'identity': (0, 0), 'mul': semidirect_mul, 'inv': semidirect_inv, 'abelian': False}, {'name': 'Heisenberg_H3', 'elements': c3cubed, 'identity': (0, 0, 0), 'mul': h3_mul, 'inv': h3_inv, 'abelian': False}]

def natural_n30_graph() -> Tuple[List[H3Element], List[List[int]], Set[H3Element]]:
    """Ablación abeliana: incrementos de cruce grueso y fase de N30."""
    elements = list(itertools.product(range(3), repeat=3))
    forward = {(0, 0, 1), (1, 0, 1), (2, 0, 1), (0, 1, 1), (0, 2, 1)}
    connection = forward | {tuple((-x % 3 for x in g)) for g in forward}
    add = lambda x, y: tuple(((a + b) % 3 for (a, b) in zip(x, y)))
    return (elements, cayley_adjacency(elements, add, connection), connection)

def boundary_rook_graph() -> Tuple[List[PairElement], List[List[int]]]:
    """Estrato 27=(3 posiciones de borde)x(9 residuos), con incidencia obvia."""
    vertices = list(itertools.product(range(3), range(9)))
    adjacency = [[int(x != y and (x[0] == y[0] or x[1] == y[1])) for y in vertices] for x in vertices]
    return (vertices, adjacency)

def band_equality_graph() -> Tuple[List[H3Element], List[List[int]], dict]:
    """Clases espectrales exactas de N30 tras olvidar errores de redondeo."""
    vertices = list(itertools.product(range(3), repeat=3))

    def band_class(k: H3Element) -> str:
        (a, b, _) = k
        if (a, b) == (0, 0):
            return 'origin'
        if a == 0 or b == 0:
            return 'axis'
        if a == b:
            return 'diagonal'
        return 'antidiagonal'
    classes = {v: band_class(v) for v in vertices}
    adjacency = [[int(x != y and classes[x] == classes[y]) for y in vertices] for x in vertices]
    return (vertices, adjacency, dict(Counter(classes.values())))

def source_hashes() -> dict:
    result = {}
    for relative in SOURCE_PATHS:
        path = PACKAGE_ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        result[relative] = {'exists': True, 'sha256': actual, 'integrity_scope': 'the package-level MANIFEST.sha256 is verified by verify_all.py'}
    return result

def write_csvs(elements: List[H3Element], adjacency: List[List[int]], triangle_list: List[Tuple[int, int, int]], line_labels: List[tuple], isomorphism: Dict[int, int], exhaustive: List[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with (DATA_DIR / 'h3_adyacencia.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['vertex'] + [str(g) for g in elements])
        for (g, row) in zip(elements, adjacency):
            writer.writerow([str(g)] + row)
    with (DATA_DIR / 'h3_triangulos_45.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['triangle_id', 'vertex_1', 'vertex_2', 'vertex_3', 'line_1', 'line_2', 'line_3'])
        for (number, (i, j, k)) in enumerate(triangle_list, 1):
            writer.writerow([number, str(elements[i]), str(elements[j]), str(elements[k]), line_label_text(line_labels[isomorphism[i]]), line_label_text(line_labels[isomorphism[j]]), line_label_text(line_labels[isomorphism[k]])])
    with (DATA_DIR / 'h3_isomorfia_27_rectas.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['h3_id', 'a', 'b', 'z', 'line_id', 'line_label'])
        for (i, (a, b, z)) in enumerate(elements):
            line_id = isomorphism[i]
            writer.writerow([i, a, b, z, line_id, line_label_text(line_labels[line_id])])
    with (DATA_DIR / 'grupos_orden_27_cayley.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(exhaustive[0]))
        writer.writeheader()
        writer.writerows(exhaustive)
    connection = canonical_connection_h3()
    with (DATA_DIR / 'carta_hensel_schlafli_729.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['word', 'low_h3', 'high_h3', 'relative_h3', 'class'])
        for word in itertools.product(range(3), repeat=6):
            low = (word[0], word[2], word[4])
            high = (word[1], word[3], word[5])
            relative = h3_mul(h3_inv(low), high)
            role = 'diagonal' if relative == (0, 0, 0) else 'incident' if relative in connection else 'skew'
            writer.writerow([''.join(map(str, word)), str(low), str(high), str(relative), role])

def main() -> None:
    elements: List[H3Element] = list(itertools.product(range(3), repeat=3))
    identity = (0, 0, 0)
    connection = canonical_connection_h3()
    app_holonomy = verify_app_translation_holonomy()
    if not all((h3_mul(h3_mul(x, y), z) == h3_mul(x, h3_mul(y, z)) for x in elements for y in elements for z in elements)):
        raise AssertionError('comprobación ejecutable fallida')
    if not all((h3_mul(x, h3_inv(x)) == identity == h3_mul(h3_inv(x), x) for x in elements)):
        raise AssertionError('comprobación ejecutable fallida')
    if not all((h3_inv(s) in connection for s in connection)):
        raise AssertionError('comprobación ejecutable fallida')
    if not (len(connection) == 10 and identity not in connection):
        raise AssertionError('comprobación ejecutable fallida')
    if not all((weyl_section(a, b) != identity for (a, b) in itertools.product(range(3), repeat=2) if (a, b) != (0, 0))):
        raise AssertionError('comprobación ejecutable fallida')
    adjacency = cayley_adjacency(elements, h3_mul, connection)
    if not all((adjacency[i][i] == 0 for i in range(27))):
        raise AssertionError('comprobación ejecutable fallida')
    if not all((adjacency[i][j] == adjacency[j][i] for i in range(27) for j in range(27))):
        raise AssertionError('comprobación ejecutable fallida')
    intersection_metrics = graph_metrics(adjacency)
    schlafli_adjacency = complement(adjacency)
    schlafli_metrics = graph_metrics(schlafli_adjacency)
    identities = verify_quadratic_identities(adjacency)
    triangle_list = triangles_of(adjacency)
    if not intersection_metrics['parameters'] == [27, 10, 1, 5]:
        raise AssertionError('comprobación ejecutable fallida')
    if not schlafli_metrics['parameters'] == [27, 16, 10, 8]:
        raise AssertionError('comprobación ejecutable fallida')
    if not intersection_metrics['triangles'] == 45:
        raise AssertionError('comprobación ejecutable fallida')
    if not all(identities.values()):
        raise AssertionError('comprobación ejecutable fallida')
    common_by_element = {str(g): sum((1 for s in connection if h3_mul(g, s) in connection)) for g in elements}
    if not common_by_element[str(identity)] == 10:
        raise AssertionError('comprobación ejecutable fallida')
    if not all((common_by_element[str(g)] == (1 if g in connection else 5) for g in elements if g != identity)):
        raise AssertionError('comprobación ejecutable fallida')
    (line_labels, line_adjacency) = standard_line_graph()
    if not graph_metrics(line_adjacency)['parameters'] == [27, 10, 1, 5]:
        raise AssertionError('comprobación ejecutable fallida')
    isomorphism = find_graph_isomorphism(adjacency, line_adjacency, 0, 0)
    stabilizer = vertex_stabilizer_order(adjacency)
    if not stabilizer['identity_stabilizer_order'] == 1920:
        raise AssertionError('comprobación ejecutable fallida')
    if not stabilizer['full_automorphism_order'] == 51840:
        raise AssertionError('comprobación ejecutable fallida')
    exhaustive_rows: List[dict] = []
    canonical_found = False
    h3_solutions: List[Set[tuple]] = []
    for group in groups_of_order_27():
        solutions = schlafli_cayley_connections(group['elements'], group['identity'], group['mul'], group['inv'])
        if group['name'] == 'Heisenberg_H3':
            canonical_found = any((solution == connection for solution in solutions))
            h3_solutions = solutions
        exhaustive_rows.append({'group': group['name'], 'abelian': group['abelian'], 'inverse_closed_degree10_candidates': 1287, 'schlafli_intersection_solutions': len(solutions)})
    if not canonical_found:
        raise AssertionError('comprobación ejecutable fallida')
    if not [row['schlafli_intersection_solutions'] for row in exhaustive_rows] == [0, 0, 0, 9, 9]:
        raise AssertionError('comprobación ejecutable fallida')
    linear_forms = list(itertools.product(range(3), repeat=2))
    gauge_connections = {frozenset((linear_gauge(ell, s) for s in connection)) for ell in linear_forms}
    if not len(gauge_connections) == 9:
        raise AssertionError('comprobación ejecutable fallida')
    if not gauge_connections == {frozenset(solution) for solution in h3_solutions}:
        raise AssertionError('comprobación ejecutable fallida')
    matrices = gl2_matrices()
    automorphism_maps = {tuple((h3_automorphism(matrix, ell, p) for p in elements)) for matrix in matrices for ell in linear_forms}
    if not len(automorphism_maps) == 432:
        raise AssertionError('comprobación ejecutable fallida')
    if not all((h3_automorphism(matrix, ell, h3_mul(x, y)) == h3_mul(h3_automorphism(matrix, ell, x), h3_automorphism(matrix, ell, y)) for matrix in matrices for ell in linear_forms for x in elements for y in elements)):
        raise AssertionError('comprobación ejecutable fallida')
    orbit_connections = {frozenset((h3_automorphism(matrix, ell, s) for s in connection)) for matrix in matrices for ell in linear_forms}
    if not orbit_connections == gauge_connections:
        raise AssertionError('comprobación ejecutable fallida')
    (_, n30_adjacency, n30_connection) = natural_n30_graph()
    n30_metrics = graph_metrics(n30_adjacency)
    (boundary_vertices, boundary_adjacency) = boundary_rook_graph()
    boundary_metrics = graph_metrics(boundary_adjacency)
    (_, band_adjacency, band_classes) = band_equality_graph()
    band_metrics = graph_metrics(band_adjacency)
    if not not n30_metrics['strongly_regular']:
        raise AssertionError('comprobación ejecutable fallida')
    if not not boundary_metrics['strongly_regular']:
        raise AssertionError('comprobación ejecutable fallida')
    if not not band_metrics['regular']:
        raise AssertionError('comprobación ejecutable fallida')
    pair_counts = Counter()
    for word in itertools.product(range(3), repeat=6):
        low = (word[0], word[2], word[4])
        high = (word[1], word[3], word[5])
        relative = h3_mul(h3_inv(low), high)
        role = 'diagonal' if relative == identity else 'incident' if relative in connection else 'skew'
        pair_counts[role] += 1
    if not pair_counts == Counter({'skew': 432, 'incident': 270, 'diagonal': 27}):
        raise AssertionError('comprobación ejecutable fallida')
    write_csvs(elements, adjacency, triangle_list, line_labels, isomorphism, exhaustive_rows)
    result = {'schema': 'HMT.APP.Heisenberg.Schlafli.v2', 'status': 'PASS_RELATIVE_APP_HOLONOMY_H3_TO_27_LINES_GAUGE_INVARIANT', 'upstream_type_correction': {'translation_holonomy': app_holonomy, 'exact_statement': 'the declared mixed polarization of the APP vertex potentials gives constant translational curvature and the alternating Wilson class', 'calibration_scope': 'APP supplies S and P, but does not uniquely select which coordinate component of each potential enters the mixed connection', 'central_completion': 'the associated standard Heisenberg central extension, relative to polarization, central orientation, and gauge; it is not split as a group', 'open_statement_not_used': 'APP uniquely selects a Hilbert-space Weyl representation W(a,b), a character of the center, or a physical quantization'}, 'construction_without_target': {'source': 'declared mixed polarization of APP translational potentials; associated Heisenberg central class reduced modulo 3', 'group': 'H3={(a,b,z) in F3^3}, (a,b,z)(c,d,w)=(a+c,b+d,z+w+bc)', 'weyl_symmetric_section': 'D(a,b)=(a,b,ab/2), 1/2=2 in F3', 'connection': [list(g) for g in sorted(connection)], 'connection_description': 'all 8 nonzero Weyl displacements plus both nontrivial central phases', 'target_graph_used_to_define_connection': False}, 'gauge_canonicity': {'linear_sections': 9, 'formula': 'D_ell(a,b)=(a,b,ab/2+ell(a,b)), ell in (F3^2)^*', 'all_nine_exhaustive_H3_solutions_are_exactly_these_sections': True, 'Aut_H3_order': 432, 'single_Aut_H3_orbit_size': 9, 'connection_stabilizer_inside_Aut_H3': 48, 'conclusion': 'the labeled connection depends on gauge, but its graph is canonical up to isomorphism'}, 'intersection_graph': intersection_metrics, 'quadratic_identities': identities, 'exact_spectrum_intersection': {'10': 1, '1': 20, '-5': 6}, 'schlafli_complement': schlafli_metrics, 'exact_spectrum_complement': {'16': 1, '4': 6, '-2': 20}, 'ordered_pair_partition': {'identity_or_diagonal': 27, 'incident_or_oriented_edges': 270, 'skew_or_oriented_nonedges': 432, 'equation': '27^2=729=27+270+432'}, 'u6_hensel_chart_partition': dict(pair_counts), 'automorphisms': stabilizer, 'standard_27_lines_isomorphism_verified': True, 'standard_line_labels': [line_label_text(label) for label in line_labels], 'cayley_exhaustion_all_groups_order_27': exhaustive_rows, 'abelian_ablations': {'N30_natural_step_relation': {'connection': [list(g) for g in sorted(n30_connection)], 'metrics': n30_metrics}, 'boundary_completion_rook_relation_on_3x9': {'vertices': len(boundary_vertices), 'metrics': boundary_metrics}, 'N30_band_equality_relation': {'class_sizes': band_classes, 'metrics': band_metrics}}, 'interpretive_boundary': {'proved': ['constant curvature and Wilson alternating class for the declared APP mixed polarization', 'associated H3 central completion, relative to polarization, central orientation, and gauge', 'target-free connection from every symmetric linear gauge section', 'all nine gauges give the complete H3 solution orbit and isomorphic graphs', 'srg(27,10,1,5) and Schlaefli complement', '45 triangles', 'explicit isomorphism to the standard intersection graph of the 27 lines', 'full graph automorphism order 51840', 'exact Hensel-chart partition of all 729 six-trit words'], 'not_claimed': ['APP uniquely selects W(a,b), a central character, or a Hilbert-space quantization', 'a physical 27th dimension', 'an oriented exceptional Jordan cubic with certified signs', 'identity of the 432 graph nonedges with a particular 432-fold decimal fiber']}, 'source_provenance': source_hashes()}
    CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
    CERTIFICATE.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')
    print('PASS_RELATIVE_APP_HOLONOMY_H3_TO_27_LINES_GAUGE_INVARIANT')
    print('srg', intersection_metrics['parameters'], 'triangles', len(triangle_list))
    print('complement', schlafli_metrics['parameters'])
    print('automorphisms', stabilizer['full_automorphism_order'])
    print('order27_cayley_solutions', [row['schlafli_intersection_solutions'] for row in exhaustive_rows])
    print('u6_partition', dict(pair_counts))
if __name__ == '__main__':
    main()
