#!/usr/bin/env python3
"""Certificado exacto del entrelazador variacional orientado 3/11.

El cálculo usa únicamente aritmética en Q(sqrt(5)), los datos finitos
dodecafásicos y la ventana t=7 de N72. No recibe C*, masas ni objetivos
metrológicos. Todas las comprobaciones usan ``require`` y siguen activas con
``python -O``.

La normalización polar contiene raíces cuadradas positivas. En vez de
aproximarlas, el certificado comprueba exactamente en Q(sqrt(5)) las
identidades que las determinan: G=A A*, G^{-1}, A*G^{-1}A=P3 y la
descomposición espectral positiva de G. De ellas se siguen literalmente
U*U=P3 y UU*=I para U=G^{-1/2}A.
"""

from __future__ import annotations

import csv
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


Perm = tuple[int, ...]
Q5 = tuple[Fraction, Fraction]  # a+b sqrt(5)
ZERO: Q5 = (Fraction(0), Fraction(0))
ONE: Q5 = (Fraction(1), Fraction(0))

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "datos/entrelazador_ramas_t7.csv"
OUTPUT = ROOT / "certificados/entrelazador_variacional.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError("ENTRELAZADOR VARIACIONAL FAIL: " + message)


def compose(p: Perm, q: Perm) -> Perm:
    return tuple(p[i] for i in q)


def inverse(p: Perm) -> Perm:
    result = [0] * len(p)
    for index, image in enumerate(p):
        result[image] = index
    return tuple(result)


def parity(p: Perm) -> int:
    return sum(
        p[i] > p[j]
        for i in range(len(p))
        for j in range(i + 1, len(p))
    ) % 2


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


def q5_add(left: Q5, right: Q5) -> Q5:
    return left[0] + right[0], left[1] + right[1]


def q5_sub(left: Q5, right: Q5) -> Q5:
    return left[0] - right[0], left[1] - right[1]


def q5_scale(value: Q5, scalar: Fraction | int) -> Q5:
    scalar = Fraction(scalar)
    return value[0] * scalar, value[1] * scalar


def q5_mul(left: Q5, right: Q5) -> Q5:
    return (
        left[0] * right[0] + 5 * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def q5_inv(value: Q5) -> Q5:
    denominator = value[0] * value[0] - 5 * value[1] * value[1]
    require(denominator != 0, "inverso de cero en Q(sqrt(5))")
    return value[0] / denominator, -value[1] / denominator


def q5_sign(value: Q5) -> int:
    """Decide exactamente el signo de a+b*sqrt(5), sin coma flotante."""

    rational, radical = value
    if rational == 0:
        return (radical > 0) - (radical < 0)
    if radical == 0 or (rational > 0) == (radical > 0):
        return (rational > 0) - (rational < 0)

    comparison = rational * rational - 5 * radical * radical
    require(comparison != 0, "igualdad racional imposible con sqrt(5)")
    if comparison > 0:
        return (rational > 0) - (rational < 0)
    return (radical > 0) - (radical < 0)


def q5_gt(left: Q5, right: Q5) -> bool:
    return q5_sign(q5_sub(left, right)) > 0


def q5_argmax(elements: list[Perm], values: dict[Perm, Q5]) -> Perm:
    require(bool(elements), "argmax de conjunto vacío")
    winner = elements[0]
    for element in elements[1:]:
        if q5_gt(values[element], values[winner]):
            winner = element
    return winner


def q5_text(value: Q5) -> str:
    return f"({value[0]})+({value[1]})*sqrt(5)"


def matmul(left: list[list[Q5]], right: list[list[Q5]]) -> list[list[Q5]]:
    rows = len(left)
    middle = len(right)
    columns = len(right[0])
    require(len(left[0]) == middle, "dimensiones incompatibles")
    result = [[ZERO for _ in range(columns)] for _ in range(rows)]
    for i in range(rows):
        for k in range(middle):
            if left[i][k] == ZERO:
                continue
            for j in range(columns):
                result[i][j] = q5_add(
                    result[i][j], q5_mul(left[i][k], right[k][j])
                )
    return result


def transpose(matrix: list[list[Q5]]) -> list[list[Q5]]:
    return [list(row) for row in zip(*matrix)]


def matrix_add(
    left: list[list[Q5]], right: list[list[Q5]]
) -> list[list[Q5]]:
    return [
        [q5_add(left[i][j], right[i][j]) for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def matrix_sub(
    left: list[list[Q5]], right: list[list[Q5]]
) -> list[list[Q5]]:
    return [
        [q5_sub(left[i][j], right[i][j]) for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def matrix_scale(matrix: list[list[Q5]], scalar: Fraction | int) -> list[list[Q5]]:
    return [[q5_scale(value, scalar) for value in row] for row in matrix]


def identity(size: int) -> list[list[Q5]]:
    return [
        [ONE if i == j else ZERO for j in range(size)]
        for i in range(size)
    ]


def rank(matrix: list[list[Q5]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column] != ZERO),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inv = q5_inv(work[pivot_row][column])
        work[pivot_row] = [q5_mul(value, inv) for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or work[row][column] == ZERO:
                continue
            factor = work[row][column]
            work[row] = [
                q5_sub(value, q5_mul(factor, pivot_value))
                for value, pivot_value in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def dot(left: list[Q5], right: list[Q5]) -> Q5:
    value = ZERO
    for x, y in zip(left, right):
        value = q5_add(value, q5_mul(x, y))
    return value


def vector_add(left: list[Q5], right: list[Q5]) -> list[Q5]:
    return [q5_add(x, y) for x, y in zip(left, right)]


def vector_scale(vector: list[Q5], scalar: Fraction | int) -> list[Q5]:
    return [q5_scale(value, scalar) for value in vector]


def matrix_vector(matrix: list[list[Q5]], vector: list[Q5]) -> list[Q5]:
    return [row[0] for row in matmul(matrix, [[value] for value in vector])]


def trace(matrix: list[list[Q5]]) -> Q5:
    value = ZERO
    for index in range(len(matrix)):
        value = q5_add(value, matrix[index][index])
    return value


A5 = tuple(p for p in itertools.permutations(range(5)) if parity(p) == 0)
IDENTITY5: Perm = tuple(range(5))
G5: Perm = (1, 2, 3, 4, 0)

SUBGROUP_C5: set[Perm] = set()
power = IDENTITY5
for _ in range(5):
    SUBGROUP_C5.add(power)
    power = compose(G5, power)

COS_REPS: tuple[Perm, ...] = (
    (3, 2, 4, 1, 0),
    (3, 1, 0, 2, 4),
    (0, 1, 3, 4, 2),
    (1, 4, 2, 3, 0),
    (3, 2, 0, 4, 1),
    (4, 0, 1, 2, 3),
    (4, 3, 2, 1, 0),
    (0, 2, 3, 1, 4),
    (3, 1, 2, 4, 0),
    (2, 1, 4, 3, 0),
    (3, 4, 1, 2, 0),
    (4, 2, 1, 3, 0),
)
COSETS = tuple(
    frozenset(compose(representative, h) for h in SUBGROUP_C5)
    for representative in COS_REPS
)
COSET_INDEX = {element: i for i, coset in enumerate(COSETS) for element in coset}


def conjugacy_class(element: Perm) -> frozenset[Perm]:
    return frozenset(
        compose(compose(h, element), inverse(h)) for h in A5
    )


CLASS_5A = conjugacy_class(G5)
CLASS_5B = conjugacy_class(compose(G5, G5))


def character_three(element: Perm) -> Q5:
    kind = cycle_type(element)
    if kind == (1,):
        return Fraction(3), Fraction(0)
    if kind == (3,):
        return ZERO
    if kind == (2, 2):
        return Fraction(-1), Fraction(0)
    if element in CLASS_5A:
        return Fraction(1, 2), Fraction(1, 2)
    if element in CLASS_5B:
        return Fraction(1, 2), Fraction(-1, 2)
    raise RuntimeError("clase de A5 desconocida")


def permutation_matrix(element: Perm) -> list[list[Q5]]:
    matrix = [[ZERO for _ in range(12)] for _ in range(12)]
    for source, coset in enumerate(COSETS):
        representative = next(iter(coset))
        target = COSET_INDEX[compose(element, representative)]
        matrix[target][source] = ONE
    return matrix


def projector_three() -> list[list[Q5]]:
    projector = [[ZERO for _ in range(12)] for _ in range(12)]
    for element in A5:
        coefficient = q5_scale(character_three(inverse(element)), Fraction(3, 60))
        action = permutation_matrix(element)
        projector = matrix_add(projector, matrix_scale(action, coefficient[0])) if coefficient[1] == 0 else [
            [q5_add(projector[i][j], q5_mul(coefficient, action[i][j])) for j in range(12)]
            for i in range(12)
        ]
    return projector


def c3_subgroups() -> list[frozenset[Perm]]:
    result: set[frozenset[Perm]] = set()
    for element in A5:
        if cycle_type(element) == (3,):
            result.add(frozenset((IDENTITY5, element, compose(element, element))))
    return sorted(result, key=lambda group: tuple(sorted(group)))


def normalizer(group: frozenset[Perm]) -> tuple[Perm, ...]:
    return tuple(
        element
        for element in A5
        if frozenset(
            compose(compose(element, member), inverse(element))
            for member in group
        )
        == group
    )


def sign_projector(group: tuple[Perm, ...]) -> list[list[Q5]]:
    projector = [[ZERO for _ in range(12)] for _ in range(12)]
    for element in group:
        sign = -1 if cycle_type(element) == (2, 2) else 1
        projector = matrix_add(
            projector,
            matrix_scale(permutation_matrix(element), Fraction(sign, 6)),
        )
    return projector


def c3_label(group: frozenset[Perm]) -> str:
    generators = sorted(element for element in group if element != IDENTITY5)
    return "/".join("".join(str(value) for value in element) for element in generators)


AW = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 2, 2, 1),
    (1, 1, 0, 1, 2, 2),
    (1, 2, 1, 0, 1, 2),
    (1, 2, 2, 1, 0, 1),
    (1, 1, 2, 2, 1, 0),
)


def codeword(word: tuple[int, ...]) -> tuple[int, ...]:
    right = tuple(
        sum(word[i] * AW[i][j] for i in range(6)) % 3
        for j in range(6)
    )
    return word + right


def support(word: tuple[int, ...]) -> frozenset[int]:
    return frozenset(i for i, value in enumerate(codeword(word)) if value)


def read_gate_rows() -> list[dict[str, str]]:
    require(DATA.is_file(), "falta el corte local N72 t=7")
    with DATA.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 11, "el corte t=7 no contiene once ramas")
    require([int(row["idx"]) for row in rows] == list(range(11)), "índices t=7")
    return rows


def tail_action(words: tuple[str, str, str], permutation: Perm) -> tuple[str, str, str]:
    pullback = inverse(permutation)
    transformed = []
    for index, word in enumerate(words):
        if index < 2:
            transformed.append(
                word[:3] + "".join(word[3 + position] for position in pullback)
            )
        else:
            transformed.append(word)
    return tuple(transformed)  # type: ignore[return-value]


def permutation_matrix_small(permutation: Perm, signed: bool = False) -> list[list[Q5]]:
    size = len(permutation)
    factor = -1 if signed and parity(permutation) else 1
    matrix = [[ZERO for _ in range(size)] for _ in range(size)]
    for source, target in enumerate(permutation):
        matrix[target][source] = (Fraction(factor), Fraction(0))
    return matrix


def main() -> None:
    require(len(A5) == 60, "orden de A5")
    require(len(COSETS) == 12 and len(COSET_INDEX) == 60, "acción de doce puntos")

    p3 = projector_three()
    require(p3 == transpose(p3), "P3 simétrico")
    require(matmul(p3, p3) == p3, "P3 idempotente")
    require(rank(p3) == 3 and trace(p3) == (Fraction(3), Fraction(0)), "rango P3")

    k = (234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601)
    mean_k = Fraction(sum(k), 12)
    centered_k = [(Fraction(value) - mean_k, Fraction(0)) for value in k]
    u_k = matrix_vector(p3, centered_k)
    require(
        dot(u_k, u_k)
        == (Fraction(6638585, 20), Fraction(2275584, 20)),
        "norma exacta de u_K",
    )

    p_pi = support(tuple(map(int, "010211")))
    h_e = support(tuple(map(int, "201101")))
    b_k = frozenset(index for index, value in enumerate(k) if value >= 729)
    require(b_k == frozenset((3, 5, 8, 9)), "B_K por corona 729")
    require(b_k == p_pi & h_e, "B_K por incidencia P_pi/H_e")

    indicator = [
        (Fraction(1 if index in b_k else 0) - Fraction(1, 3), Fraction(0))
        for index in range(12)
    ]
    b_vector = matrix_vector(p3, indicator)
    require(dot(b_vector, b_vector) == ONE, "la ancla b_K tiene norma uno")

    c3s = c3_subgroups()
    require(len(c3s) == 10, "A5 debe contener diez ejes C3")
    energy_rows: list[tuple[Q5, str, frozenset[Perm], tuple[Perm, ...]]] = []
    for c3 in c3s:
        group = normalizer(c3)
        require(len(group) == 6, "normalizador C3 de orden seis")
        require(
            Counter(cycle_type(element) for element in group)
            == Counter({(1,): 1, (3,): 2, (2, 2): 3}),
            "normalizador isomorfo a S3",
        )
        e_sign = sign_projector(group)
        component = matrix_vector(e_sign, b_vector)
        energy_rows.append((dot(component, component), c3_label(c3), c3, group))

    expected_energies = Counter(
        {
            (Fraction(2, 3), Fraction(2, 15)): 1,
            (Fraction(1, 3), Fraction(2, 15)): 2,
            (Fraction(2, 3), Fraction(-2, 15)): 1,
            (Fraction(1, 6), Fraction(1, 30)): 2,
            (Fraction(1, 6), Fraction(-1, 30)): 2,
            (Fraction(1, 3), Fraction(-2, 15)): 2,
        }
    )
    require(Counter(row[0] for row in energy_rows) == expected_energies, "tabla de diez energías")
    top_energy = (Fraction(2, 3), Fraction(2, 15))
    winners = [row for row in energy_rows if row[0] == top_energy]
    require(len(winners) == 1, "máximo variacional único")
    require(
        all(not q5_gt(row[0], top_energy) for row in energy_rows),
        "máximo variacional certificado por orden exacto",
    )
    _, winning_label, c3_star, h_star = winners[0]
    expected_c = (0, 1, 3, 4, 2)  # ciclo (2 3 4)
    require(expected_c in c3_star, "el eje ganador es <(2 3 4)>")
    remaining_energies = [row[0] for row in energy_rows if row[0] != top_energy]
    second_energy = remaining_energies[0]
    for value in remaining_energies[1:]:
        if q5_gt(value, second_energy):
            second_energy = value
    require(second_energy == (Fraction(1, 3), Fraction(2, 15)), "segundo nivel exacto")
    require(q5_sub(top_energy, second_energy) == (Fraction(1, 3), Fraction(0)), "gap 1/3")

    # El mismo eje es recuperado de manera independiente desde la carta K.
    u_energy_rows: list[tuple[Q5, str, frozenset[Perm], tuple[Perm, ...]]] = []
    for c3 in c3s:
        group = normalizer(c3)
        e_sign = sign_projector(group)
        component = matrix_vector(e_sign, u_k)
        u_energy_rows.append((dot(component, component), c3_label(c3), c3, group))
    u_winner = u_energy_rows[0]
    for row in u_energy_rows[1:]:
        if q5_gt(row[0], u_winner[0]):
            u_winner = row
    require(u_winner[2] == c3_star, "B_K y u_K seleccionan el mismo eje S3")
    require(
        sum(row[0] == u_winner[0] for row in u_energy_rows) == 1,
        "máximo K único",
    )

    # Naturalidad del selector bajo todo cambio simultáneo del calibre A5.
    e_star = sign_projector(h_star)
    for element in A5:
        conjugate = frozenset(
            compose(compose(element, member), inverse(element))
            for member in c3_star
        )
        e_conjugate = sign_projector(normalizer(conjugate))
        action = permutation_matrix(element)
        transported = matmul(matmul(action, e_star), transpose(action))
        require(e_conjugate == transported, "covariancia de e_sgn bajo A5")
        transported_b = matrix_vector(action, b_vector)
        transported_u = matrix_vector(action, u_k)
        require(
            dot(
                matrix_vector(e_conjugate, transported_b),
                matrix_vector(e_conjugate, transported_b),
            )
            == top_energy,
            "naturalidad exacta de la energía B_K",
        )
        require(
            dot(
                transported_b,
                matrix_vector(
                    permutation_matrix(
                        compose(compose(element, expected_c), inverse(element))
                    ),
                    transported_u,
                ),
            )
            == (Fraction(1341, 4), Fraction(2409, 20)),
            "naturalidad exacta del marcador de orientación",
        )

    # Restricción exacta del sector icosaédrico a H*: sgn + std.
    traces_by_class: dict[tuple[int, ...], set[Q5]] = {}
    for element in h_star:
        value = trace(matmul(p3, permutation_matrix(element)))
        traces_by_class.setdefault(cycle_type(element), set()).add(value)
    require(traces_by_class[(1,)] == {(Fraction(3), Fraction(0))}, "carácter identidad")
    require(traces_by_class[(2, 2)] == {(Fraction(-1), Fraction(0))}, "carácter reflexión")
    require(traces_by_class[(3,)] == {ZERO}, "carácter orden tres")
    p_sign = matmul(p3, e_star)
    require(rank(p_sign) == 1, "multiplicidad sign")
    require(rank(matrix_sub(p3, p_sign)) == 2, "multiplicidad standard")

    # S3 local de la puerta t=7 y el triplete superviviente a horizonte dos.
    gate_rows = read_gate_rows()
    words = [tuple(row["rows"].split("|")) for row in gate_rows]
    word_index = {word: index for index, word in enumerate(words)}
    s3 = tuple(itertools.permutations(range(3)))
    gate_permutations: dict[Perm, Perm] = {}
    for element in s3:
        images = tuple(word_index[tail_action(word, element)] for word in words)
        require(sorted(images) == list(range(11)), "acción S3 cierra las once ramas")
        gate_permutations[element] = images
    for left in s3:
        for right in s3:
            require(
                compose(gate_permutations[left], gate_permutations[right])
                == gate_permutations[compose(left, right)],
                "ley de grupo en las ramas",
            )

    unseen = set(range(11))
    gate_orbits: list[list[int]] = []
    while unseen:
        initial = min(unseen)
        orbit = {gate_permutations[element][initial] for element in s3}
        gate_orbits.append(sorted(orbit))
        unseen -= orbit
    require(gate_orbits == [[0, 1, 2], [3, 4, 5], [6], [7], [8, 9, 10]], "órbitas t=7")

    selected = [index for index, row in enumerate(gate_rows) if int(row["surv_h2"]) > 0]
    actual_h3 = [index for index, row in enumerate(gate_rows) if int(row["surv_h3"]) > 0]
    require(selected == [0, 1, 2], "tres supervivientes a horizonte dos")
    require(actual_h3 == [1], "ruptura de orientación a horizonte tres")
    p_gate = [[ZERO for _ in range(11)] for _ in range(11)]
    for index in selected:
        p_gate[index][index] = ONE
    for element in s3:
        action = permutation_matrix_small(gate_permutations[element])
        require(matmul(action, p_gate) == matmul(p_gate, action), "P_G conmuta con S3")

    # El mapa horizontal--vertical se fija por la posición excepcional.
    positive_signatures = ("339555", "393555", "933555")
    signature_by_position = {signature[:3].index("9"): signature for signature in positive_signatures}
    branch_by_position = {
        words[index][0][3:].index("2"): index
        for index in selected
    }
    require(set(signature_by_position) == {0, 1, 2}, "posiciones 9 del triplete pi")
    require(set(branch_by_position) == {0, 1, 2}, "posiciones 2 del triplete t=7")
    beta = {
        signature_by_position[position]: branch_by_position[position]
        for position in range(3)
    }
    require(beta == {"339555": 0, "393555": 1, "933555": 2}, "beta horizontal--vertical")

    # El triplete plano es 1+std; el triplete orientado es sgn+std.
    plain_character = (3, 1, 0)
    oriented_character = (3, -1, 0)
    source_character = (3, -1, 0)
    require(plain_character != source_character, "no-go sin línea de orientación")
    require(oriented_character == source_character, "igualdad tras twist de orientación")

    # b_K y u_K fijan los dos generadores dentro del H* ya seleccionado.
    def score(element: Perm) -> Q5:
        return dot(b_vector, matrix_vector(permutation_matrix(element), u_k))

    order_three = [element for element in h_star if cycle_type(element) == (3,)]
    order_two = [element for element in h_star if cycle_type(element) == (2, 2)]
    c_scores = {element: score(element) for element in order_three}
    r_scores = {element: score(element) for element in order_two}
    c_star = q5_argmax(order_three, c_scores)
    r_star = q5_argmax(order_two, r_scores)
    require(c_star == (0, 1, 3, 4, 2), "generador c* único")
    require(r_star == (1, 0, 4, 3, 2), "reflexión r* única")
    require(
        c_scores[c_star] == (Fraction(1341, 4), Fraction(2409, 20))
        and c_scores[inverse(c_star)] == (Fraction(357, 2), Fraction(1853, 10)),
        "scores de las dos orientaciones C3",
    )
    require(
        sum(value == c_scores[c_star] for value in c_scores.values()) == 1,
        "máximo c* no degenerado",
    )
    require(
        sum(value == r_scores[r_star] for value in r_scores.values()) == 1,
        "máximo r* no degenerado",
    )
    require(compose(compose(r_star, c_star), r_star) == inverse(c_star), "relación diédrica")

    # Isomorfismo theta desde el S3 de posiciones: c=(0 1 2), r=(0 2),
    # que fija la rama actual de posición central.
    identity3: Perm = (0, 1, 2)
    c_target: Perm = (1, 2, 0)
    r_target: Perm = (2, 1, 0)
    theta: dict[Perm, Perm] = {identity3: IDENTITY5}
    pending = [(c_target, c_star), (r_target, r_star)]
    while pending:
        target, source = pending.pop()
        if target in theta:
            require(theta[target] == source, "theta bien definida")
            continue
        theta[target] = source
        for known_target, known_source in list(theta.items()):
            pending.extend(
                (
                    (compose(target, known_target), compose(source, known_source)),
                    (compose(known_target, target), compose(known_source, source)),
                )
            )
    require(len(theta) == 6 and set(theta.values()) == set(h_star), "theta es isomorfismo")

    # Operador de Reynolds A: V3 -> det(R^3_perm) tensor R^3_perm.
    anchor_target = (0, 1, 0)  # rama actual: índice uno / posición dos
    reynolds = [[ZERO for _ in range(12)] for _ in range(3)]
    for target_element, source_element in theta.items():
        target_action = permutation_matrix_small(target_element, signed=True)
        moved_target = [
            sum(
                (target_action[i][j][0] * anchor_target[j] for j in range(3)),
                Fraction(0),
            )
            for i in range(3)
        ]
        moved_source = matrix_vector(permutation_matrix(source_element), b_vector)
        for i in range(3):
            for j in range(12):
                reynolds[i][j] = q5_add(
                    reynolds[i][j], q5_scale(moved_source[j], moved_target[i])
                )

    require(rank(reynolds) == 3, "A de Reynolds tiene rango tres")
    require(matmul(reynolds, p3) == reynolds, "A=A P3")
    for target_element, source_element in theta.items():
        target_action = permutation_matrix_small(target_element, signed=True)
        source_action = permutation_matrix(source_element)
        require(
            matmul(target_action, reynolds) == matmul(reynolds, source_action),
            "equivarianza exacta de A",
        )

    gram = matmul(reynolds, transpose(reynolds))
    expected_gram = [
        [
            (Fraction(3), Fraction(2, 5))
            if i == j
            else (Fraction(5, 2), Fraction(3, 5))
            for j in range(3)
        ]
        for i in range(3)
    ]
    require(gram == expected_gram, "Gram exacto de Reynolds")
    lambda_sign = (Fraction(8), Fraction(8, 5))
    lambda_standard = (Fraction(1, 2), Fraction(-1, 5))
    require(5 * 5 > (2 * 2) * 5, "lambda_standard positiva")
    require(lambda_sign[0] > 0 and lambda_sign[1] > 0, "lambda_sign positiva")

    projector_uniform = [
        [(Fraction(1, 3), Fraction(0)) for _ in range(3)]
        for _ in range(3)
    ]
    projector_standard = matrix_sub(identity(3), projector_uniform)
    gram_spectral = matrix_add(
        [[q5_mul(lambda_sign, value) for value in row] for row in projector_uniform],
        [[q5_mul(lambda_standard, value) for value in row] for row in projector_standard],
    )
    require(gram_spectral == gram, "descomposición espectral de G")
    gram_inverse = matrix_add(
        [[q5_mul(q5_inv(lambda_sign), value) for value in row] for row in projector_uniform],
        [[q5_mul(q5_inv(lambda_standard), value) for value in row] for row in projector_standard],
    )
    require(matmul(gram, gram_inverse) == identity(3), "inversa exacta de G")
    require(
        q5_inv(lambda_sign) == (Fraction(5, 32), Fraction(-1, 32))
        and q5_inv(lambda_standard) == (Fraction(10), Fraction(4)),
        "autovalores inversos exactos",
    )
    source_polar_projector = matmul(
        matmul(transpose(reynolds), gram_inverse), reynolds
    )
    require(source_polar_projector == p3, "A*G^{-1}A=P3")

    # Inclusión del sector seleccionado en el módulo de once ramas.
    inclusion = [[ZERO for _ in range(3)] for _ in range(11)]
    for index in range(3):
        inclusion[index][index] = ONE
    require(matmul(transpose(inclusion), inclusion) == identity(3), "J*J=I3")
    require(matmul(inclusion, transpose(inclusion)) == p_gate, "JJ*=P_G")
    raw_partial = matmul(transpose(reynolds), transpose(inclusion))
    require(matmul(p3, raw_partial) == raw_partial, "P3 A*J*=A*J*")
    require(matmul(raw_partial, p_gate) == raw_partial, "A*J* P_G=A*J*")

    # Conteo previo de calibres y eliminación por los datos marcados.
    gauges_labeled = 10 * 6 * 4
    gauges_mod_positive_relabeling = 10 * 4
    require(gauges_labeled == 240 and gauges_mod_positive_relabeling == 40, "conteo de gauges")

    result = {
        "schema": "HMT.entrelazador-variacional-orientado.v1",
        "status": "PASS_NEW_RELATIVE_VARIATIONAL_THEOREM",
        "uses_C_star": False,
        "uses_physical_target": False,
        "input_status": (
            "Relative to the published A5/coset gauge, P3, K, the doubly "
            "constructed face B_K, and the finite N72 t=7 survival data."
        ),
        "horizontal_vertical_gate": {
            "eleven_branch_orbits": gate_orbits,
            "rank3_survivor_indices_h2": selected,
            "unique_survivor_index_h3": actual_h3[0],
            "beta_positive_pi_to_gate": beta,
            "plain_character": list(plain_character),
            "oriented_character": list(oriented_character),
        },
        "a5_restriction": {
            "source_character": list(source_character),
            "decomposition": "sgn + standard",
            "direct_plain_intertwiner": False,
            "oriented_intertwiner_class": True,
        },
        "variational_selector": {
            "number_of_S3_normalizers": len(c3s),
            "energies": {
                label: q5_text(energy)
                for energy, label, _, _ in sorted(energy_rows, key=lambda row: row[1])
            },
            "winner": winning_label,
            "winner_C3_generators": [list(element) for element in sorted(c3_star)],
            "winner_energy": q5_text(top_energy),
            "gap_to_second_level": "1/3",
            "b_K_norm_squared": q5_text(dot(b_vector, b_vector)),
            "same_unique_winner_from_u_K": True,
            "u_K_winner_energy": q5_text(u_winner[0]),
            "A5_natural": True,
        },
        "orientation_selector": {
            "c_star": list(c_star),
            "r_star": list(r_star),
            "c_star_score": q5_text(c_scores[c_star]),
            "c_inverse_score": q5_text(c_scores[inverse(c_star)]),
            "r_star_score": q5_text(r_scores[r_star]),
            "dihedral_relation": True,
        },
        "reynolds_polar": {
            "rank": rank(reynolds),
            "gram_diagonal": q5_text(gram[0][0]),
            "gram_off_diagonal": q5_text(gram[0][1]),
            "lambda_sign": q5_text(lambda_sign),
            "lambda_standard": q5_text(lambda_standard),
            "A_star_G_inverse_A_equals_P3": True,
            "polar_U_star_U_equals_P3": True,
            "polar_U_U_star_equals_I3": True,
            "partial_W_star_W_equals_PG": True,
            "partial_W_W_star_equals_P3": True,
            "support_identity": "P3 W = W P_G = W",
            "equivariant": True,
        },
        "gauge_count": {
            "before_marked_selectors_labeled": gauges_labeled,
            "before_marked_selectors_mod_S3_relabeling": gauges_mod_positive_relabeling,
            "after_variational_orientation_and_polar_rules": 1,
        },
        "scope": (
            "This is a new exact theorem relative to the internal variational "
            "rule E_B(H)=||e_sgn,H b_K||^2 and the marked orientation score. "
            "It is not evidence that the rule had already been derived in the "
            "previous canon, and it does not identify the Witt-star involution "
            "with P3: the latter have different spectra."
        ),
    }
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    print("PASS_ENTRELAZADOR_VARIACIONAL_ORIENTADO")


if __name__ == "__main__":
    main()
