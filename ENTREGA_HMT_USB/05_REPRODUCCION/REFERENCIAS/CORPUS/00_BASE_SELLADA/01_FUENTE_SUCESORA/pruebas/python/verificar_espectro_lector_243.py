#!/usr/bin/env python3
"""Auditoría algebraica independiente de los operadores L0 y L1 sobre F3.

El programa usa únicamente la biblioteca estándar.  No importa código HMT ni
ningún sistema de álgebra computacional.  Recalcula polinomios característicos
y mínimos, factores irreducibles, órdenes de raíces, descomposiciones
primarias, proyectores, órbitas y la relación con el catálogo N33 y su acción
diedral D3^cat.

La salida es un certificado JSON reproducible situado junto a este programa.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from itertools import permutations, product
from pathlib import Path
from typing import Iterable, Sequence


P = 3
N = 6
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CATALOG = ROOT / "datos/n33_uid_catalog.csv"
N33_SOURCE = HERE / "hmt_n33_pi_e_phi_closeout.py"
SELECTOR_SOURCE = HERE / "verificar_selector_orbital_constantes.py"
OUTPUT = ROOT / "certificados/CERTIFICADO_ESPECTRO_LECTOR_243.json"

EXPECTED_HASHES = {
    N33_SOURCE: "07f273a1955c9e4c58986f98624ba039ed259ecba7e10e05a99f11c4149d0478",
    CATALOG: "968576e9d524de977f22b0f3dafa381b76037d68f81843029438150556214554",
    SELECTOR_SOURCE: "da58c96bf8c44eecb98e3fa06ec16e68308bd532db5f6e9413c4f2987b7d67ef",
}

L0 = [
    [2, 2, 2, 1, 2, 1],
    [2, 1, 2, 2, 1, 1],
    [1, 0, 0, 1, 0, 2],
    [0, 0, 1, 1, 1, 0],
    [2, 2, 2, 0, 2, 1],
    [2, 1, 2, 1, 0, 0],
]

L1 = [
    [2, 1, 2, 0, 2, 2],
    [1, 2, 1, 1, 2, 0],
    [1, 2, 1, 1, 1, 2],
    [0, 1, 0, 0, 2, 1],
    [2, 0, 2, 1, 0, 1],
    [0, 2, 2, 2, 1, 1],
]

NAMED_WORDS = {
    "pi": (0, 1, 0, 2, 1, 1),
    "e": (2, 0, 1, 1, 0, 1),
    "phi": (1, 2, 1, 2, 0, 0),
}

# r(abc|def)=cab|efd, s(abc|def)=def|abc: convención de la acción
# D3^cat certificada en la publicación activa del 2026-07-21.
R_PERMUTATION = (2, 0, 1, 4, 5, 3)
S_PERMUTATION = (3, 4, 5, 0, 1, 2)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"ESPECTRO LECTOR FAIL: {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def eye() -> list[list[int]]:
    return [[int(i == j) for j in range(N)] for i in range(N)]


def matrix_add(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]) -> list[list[int]]:
    return [[(a[i][j] + b[i][j]) % P for j in range(N)] for i in range(N)]


def matrix_scale(c: int, a: Sequence[Sequence[int]]) -> list[list[int]]:
    return [[c * a[i][j] % P for j in range(N)] for i in range(N)]


def matrix_sub(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]) -> list[list[int]]:
    return matrix_add(a, matrix_scale(-1, b))


def matmul(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]) -> list[list[int]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(N)) % P for j in range(N)]
        for i in range(N)
    ]


def matrix_power(a: Sequence[Sequence[int]], exponent: int) -> list[list[int]]:
    result = eye()
    base = [list(row) for row in a]
    while exponent:
        if exponent & 1:
            result = matmul(result, base)
        base = matmul(base, base)
        exponent //= 2
    return result


def row_times(row: Sequence[int], matrix: Sequence[Sequence[int]]) -> tuple[int, ...]:
    return tuple(sum(row[k] * matrix[k][j] for k in range(N)) % P for j in range(N))


def rank_mod3(matrix: Sequence[Sequence[int]]) -> int:
    work = [[x % P for x in row] for row in matrix]
    if not work:
        return 0
    rows, cols = len(work), len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if work[r][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inv = pow(work[pivot_row][col], -1, P)
        work[pivot_row] = [(inv * x) % P for x in work[pivot_row]]
        for row in range(rows):
            if row != pivot_row and work[row][col]:
                c = work[row][col]
                work[row] = [(x - c * y) % P for x, y in zip(work[row], work[pivot_row])]
        pivot_row += 1
    return pivot_row


def solve_mod3(matrix: Sequence[Sequence[int]], rhs: Sequence[int]) -> list[int] | None:
    """Devuelve una solución, con variables libres nulas, o None."""
    work = [[x % P for x in row] + [b % P] for row, b in zip(matrix, rhs)]
    rows = len(work)
    cols = len(matrix[0]) if matrix else 0
    pivot_row = 0
    pivots: list[int] = []
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if work[r][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inv = pow(work[pivot_row][col], -1, P)
        work[pivot_row] = [(inv * x) % P for x in work[pivot_row]]
        for row in range(rows):
            if row != pivot_row and work[row][col]:
                c = work[row][col]
                work[row] = [(x - c * y) % P for x, y in zip(work[row], work[pivot_row])]
        pivots.append(col)
        pivot_row += 1
    for row in range(pivot_row, rows):
        if all(work[row][col] == 0 for col in range(cols)) and work[row][-1]:
            return None
    solution = [0] * cols
    for row, col in enumerate(pivots):
        solution[col] = work[row][-1]
    return solution


# Polinomios en orden ascendente: [a0,a1,...,ad].
def poly_trim(a: Sequence[int]) -> list[int]:
    out = [x % P for x in a]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_add(a: Sequence[int], b: Sequence[int]) -> list[int]:
    out = [0] * max(len(a), len(b))
    for i in range(len(out)):
        out[i] = ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % P
    return poly_trim(out)


def poly_mul(a: Sequence[int], b: Sequence[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % P
    return poly_trim(out)


def poly_divmod(a: Sequence[int], b: Sequence[int]) -> tuple[list[int], list[int]]:
    numerator = poly_trim(a)
    divisor = poly_trim(b)
    require(divisor != [0], "división por el polinomio cero")
    quotient = [0] * max(1, len(numerator) - len(divisor) + 1)
    inv = pow(divisor[-1], -1, P)
    while len(numerator) >= len(divisor) and numerator != [0]:
        degree = len(numerator) - len(divisor)
        coefficient = numerator[-1] * inv % P
        quotient[degree] = coefficient
        for i, value in enumerate(divisor):
            numerator[degree + i] = (numerator[degree + i] - coefficient * value) % P
        numerator = poly_trim(numerator)
    return poly_trim(quotient), numerator


def poly_mod(a: Sequence[int], modulus: Sequence[int]) -> list[int]:
    return poly_divmod(a, modulus)[1]


def poly_power_mod(base: Sequence[int], exponent: int, modulus: Sequence[int]) -> list[int]:
    result = [1]
    value = poly_mod(base, modulus)
    while exponent:
        if exponent & 1:
            result = poly_mod(poly_mul(result, value), modulus)
        value = poly_mod(poly_mul(value, value), modulus)
        exponent //= 2
    return result


def is_irreducible(f: Sequence[int]) -> bool:
    f = poly_trim(f)
    degree = len(f) - 1
    require(degree >= 1 and f[-1] == 1, "irreducibilidad requiere polinomio mónico")
    for d in range(1, degree // 2 + 1):
        for coefficients in product(range(P), repeat=d):
            candidate = list(coefficients) + [1]
            if poly_divmod(f, candidate)[1] == [0]:
                return False
    return True


def root_order(f: Sequence[int]) -> int:
    """Orden de la clase de x en F3[x]/(f), para f irreducible y f(0)!=0."""
    degree = len(poly_trim(f)) - 1
    require(is_irreducible(f) and f[0] % P, "factor inválido para orden multiplicativo")
    for exponent in range(1, P**degree):
        if poly_power_mod([0, 1], exponent, f) == [1]:
            return exponent
    raise RuntimeError("no se encontró el orden de la raíz")


def permutation_sign(perm: Sequence[int]) -> int:
    inversions = sum(
        perm[i] > perm[j]
        for i in range(len(perm))
        for j in range(i + 1, len(perm))
    )
    return 2 if inversions % 2 else 1


def characteristic_polynomial(matrix: Sequence[Sequence[int]]) -> list[int]:
    result = [0]
    for perm in permutations(range(N)):
        term = [1]
        for i, j in enumerate(perm):
            factor = [(-matrix[i][j]) % P, 1] if i == j else [(-matrix[i][j]) % P]
            term = poly_mul(term, factor)
        sign = permutation_sign(perm)
        result = poly_add(result, [(sign * x) % P for x in term])
    return result


def minimum_polynomial(matrix: Sequence[Sequence[int]]) -> list[int]:
    powers: list[list[int]] = []
    value = eye()
    for degree in range(N * N + 1):
        vector = [x for row in value for x in row]
        if powers:
            design = [[powers[col][row] for col in range(len(powers))] for row in range(N * N)]
            solution = solve_mod3(design, [(-x) % P for x in vector])
            if solution is not None:
                return poly_trim(solution + [1])
        powers.append(vector)
        value = matmul(value, matrix)
    raise RuntimeError("no se encontró el polinomio mínimo")


def evaluate_matrix_polynomial(polynomial: Sequence[int], matrix: Sequence[Sequence[int]]) -> list[list[int]]:
    result = [[0] * N for _ in range(N)]
    power = eye()
    for coefficient in polynomial:
        result = matrix_add(result, matrix_scale(coefficient, power))
        power = matmul(power, matrix)
    return result


def matrix_order(matrix: Sequence[Sequence[int]], limit: int = 10_000) -> int:
    value = eye()
    for exponent in range(1, limit + 1):
        value = matmul(value, matrix)
        if value == eye():
            return exponent
    raise RuntimeError("orden matricial no encontrado")


def orbit_lengths(matrix: Sequence[Sequence[int]]) -> Counter[int]:
    unseen = set(product(range(P), repeat=N))
    lengths: Counter[int] = Counter()
    while unseen:
        start = next(iter(unseen))
        current = start
        orbit: set[tuple[int, ...]] = set()
        while current not in orbit:
            orbit.add(current)
            current = row_times(current, matrix)
        require(current == start, "la órbita no cerró en su origen")
        unseen -= orbit
        lengths[len(orbit)] += 1
    return lengths


def permute(values: Sequence[int], permutation: Sequence[int]) -> tuple[int, ...]:
    return tuple(values[index] for index in permutation)


def d3_orbit(word: tuple[int, ...]) -> frozenset[tuple[int, ...]]:
    orbit: set[tuple[int, ...]] = set()
    current = word
    for _ in range(3):
        orbit.add(current)
        orbit.add(permute(current, S_PERMUTATION))
        current = permute(current, R_PERMUTATION)
    return frozenset(orbit)


def permutation_matrix(permutation: Sequence[int]) -> list[list[int]]:
    result = [[0] * N for _ in range(N)]
    for output_position, input_position in enumerate(permutation):
        result[input_position][output_position] = 1
    return result


def read_catalogue() -> tuple[list[dict[str, object]], set[tuple[int, ...]]]:
    rows: list[dict[str, object]] = []
    words: set[tuple[int, ...]] = set()
    with CATALOG.open(encoding="utf-8", newline="") as stream:
        for raw in csv.DictReader(stream):
            u6 = tuple(int(value) for value in raw["U6"].split("|"))
            word = tuple(int(value) for value in raw["w6"])
            require(word == tuple((-value) % P for value in u6), "fila N33 mal reducida")
            rows.append({"u6": u6, "word": word, "count": int(raw["count"])})
            words.add(word)
    require(len(rows) == 468 and len(words) == 243, "censos N33 inesperados")
    return rows, words


def vector_difference(word: Sequence[int], step: int) -> tuple[int, ...]:
    return tuple((word[i] - word[(i + step) % N]) % P for i in range(N))


def counter_json(counter: Counter[object]) -> dict[str, int]:
    return {str(key): value for key, value in sorted(counter.items(), key=lambda item: str(item[0]))}


def main() -> None:
    for path, expected in EXPECTED_HASHES.items():
        require(path.is_file(), f"falta la fuente {path}")
        require(sha256(path) == expected, f"hash inesperado para {path}")

    identity = eye()
    zero_matrix = [[0] * N for _ in range(N)]
    m = matmul(L0, L1)
    calendar = matmul(matmul(matmul(L0, L0), L1), L1)

    q4 = [2, 1, 0, 0, 1]          # x^4+x+2
    q3_l1 = [2, 0, 1, 1]          # x^3+x^2+2
    q5 = [1, 0, 1, 2, 0, 1]       # x^5+2x^3+x^2+1
    q3_calendar = [1, 2, 0, 1]    # x^3+2x+1
    factors = {
        "L0": [[1, 1], [2, 1], q4],
        "L1_characteristic": [[1, 1], [2, 1], [2, 1], q3_l1],
        "L1_minimum": [[1, 1], [2, 1], q3_l1],
        "M": [[2, 1], q5],
        "calendar": [[1, 1], [2, 1], [2, 1], q3_calendar],
    }

    matrices = {"L0": L0, "L1": L1, "M=L0L1": m, "C=L0^2L1^2": calendar}
    charpolys = {name: characteristic_polynomial(value) for name, value in matrices.items()}
    minpolys = {name: minimum_polynomial(value) for name, value in matrices.items()}
    expected_charpolys = {
        "L0": [1, 2, 2, 1, 2, 0, 1],
        "L1": [2, 1, 2, 2, 1, 0, 1],
        "M=L0L1": [2, 1, 2, 2, 2, 2, 1],
        "C=L0^2L1^2": [1, 1, 0, 0, 1, 2, 1],
    }
    expected_minpolys = {
        "L0": expected_charpolys["L0"],
        "L1": [1, 0, 1, 2, 1, 1],
        "M=L0L1": expected_charpolys["M=L0L1"],
        "C=L0^2L1^2": expected_charpolys["C=L0^2L1^2"],
    }
    require(charpolys == expected_charpolys, f"polinomios característicos: {charpolys}")
    require(minpolys == expected_minpolys, f"polinomios mínimos: {minpolys}")

    for factor_list, expected in (
        (factors["L0"], charpolys["L0"]),
        (factors["L1_characteristic"], charpolys["L1"]),
        (factors["L1_minimum"], minpolys["L1"]),
        (factors["M"], charpolys["M=L0L1"]),
        (factors["calendar"], charpolys["C=L0^2L1^2"]),
    ):
        value = [1]
        for factor in factor_list:
            value = poly_mul(value, factor)
        require(value == expected, f"factorización incorrecta: {factor_list}")

    irreducible_orders = {
        "x^4+x+2": root_order(q4),
        "x^3+x^2+2": root_order(q3_l1),
        "x^5+2x^3+x^2+1": root_order(q5),
        "x^3+2x+1": root_order(q3_calendar),
    }
    require(irreducible_orders == {
        "x^4+x+2": 80,
        "x^3+x^2+2": 13,
        "x^5+2x^3+x^2+1": 242,
        "x^3+2x+1": 26,
    }, f"órdenes de raíces inesperados: {irreducible_orders}")

    orders = {name: matrix_order(value) for name, value in matrices.items()}
    require(orders == {"L0": 80, "L1": 26, "M=L0L1": 242, "C=L0^2L1^2": 78},
            f"órdenes matriciales: {orders}")

    # Descomposición canónica para M=(L0L1).  Como chi_M=(x-1)q5 y
    # q5(1)=2, P_F=2q5(M) proyecta sobre Fix(M), y P_W=I-P_F sobre el
    # sector irreducible de dimensión cinco.
    p_fixed = matrix_scale(2, evaluate_matrix_polynomial(q5, m))
    p_singer = matrix_sub(identity, p_fixed)
    require(matmul(p_fixed, p_fixed) == p_fixed, "P_F no es idempotente")
    require(matmul(p_singer, p_singer) == p_singer, "P_W no es idempotente")
    require(matmul(p_fixed, p_singer) == zero_matrix, "los proyectores no son ortogonales")
    require(matrix_add(p_fixed, p_singer) == identity, "los proyectores no suman I")
    require(rank_mod3(p_fixed) == 1 and rank_mod3(p_singer) == 5, "rangos de proyectores")
    require(matmul(m, p_fixed) == p_fixed, "M no fija el sector lineal")
    require(matmul(m, p_singer) == matmul(p_singer, m), "P_W no conmuta con M")

    fixed_left_generator = (2, 2, 2, 1, 1, 1)
    fixed_right_generator = (1, 0, 0, 2, 0, 1)
    require(row_times(fixed_left_generator, m) == fixed_left_generator, "generador fijo izquierdo")
    require(tuple(sum(m[i][j] * fixed_right_generator[j] for j in range(N)) % P for i in range(N))
            == fixed_right_generator, "generador fijo derecho")
    require(sum(x * y for x, y in zip(fixed_left_generator, fixed_right_generator)) % P == 2,
            "normalización de los generadores fijos")

    all_vectors = set(product(range(P), repeat=N))
    singer_space = {row_times(vector, p_singer) for vector in all_vectors}
    fixed_space = {row_times(vector, p_fixed) for vector in all_vectors}
    require(len(singer_space) == 243 and len(fixed_space) == 3, "tamaños de la descomposición")
    require(orbit_lengths(m) == Counter({1: 3, 242: 3}), "órbitas de M en F3^6")
    singer_orbit_lengths = Counter()
    unseen_singer = set(singer_space)
    while unseen_singer:
        start = next(iter(unseen_singer))
        current = start
        orbit: set[tuple[int, ...]] = set()
        while current not in orbit:
            orbit.add(current)
            current = row_times(current, m)
        require(current == start, "órbita del sector Singer")
        unseen_singer -= orbit
        singer_orbit_lengths[len(orbit)] += 1
    require(singer_orbit_lengths == Counter({1: 1, 242: 1}), "órbitas del sector Singer")

    rows, catalogue = read_catalogue()
    require((0,) * N not in catalogue, "cero apareció en el catálogo")
    require(rank_mod3(catalogue) == 6, "rango de la envolvente del catálogo")
    affine_basepoint = min(catalogue)
    affine_differences = {
        tuple((x - y) % P for x, y in zip(word, affine_basepoint))
        for word in catalogue
    }
    affine_hull_rank = rank_mod3(affine_differences)
    require(affine_hull_rank == 6, "rango de la envolvente afín del catálogo")
    addition_witness = None
    for a in sorted(catalogue):
        for b in sorted(catalogue):
            c = tuple((x + y) % P for x, y in zip(a, b))
            if c not in catalogue:
                addition_witness = {"a": a, "b": b, "a_plus_b": c}
                break
        if addition_witness:
            break
    require(addition_witness is not None, "el catálogo resultó aditivo")

    m_image_catalogue = {row_times(word, m) for word in catalogue}
    projected_catalogue = [row_times(word, p_singer) for word in catalogue]
    projected_multiplicity = Counter(projected_catalogue)
    fixed_coordinate_distribution: Counter[int] = Counter()
    for word in catalogue:
        # P_F(v)=a f y f.h=2; por tanto a=2(v.h).
        coefficient = 2 * sum(x * y for x, y in zip(word, fixed_right_generator)) % P
        require(row_times(word, p_fixed) == tuple(coefficient * x % P for x in fixed_left_generator),
                "coordenada fija mal normalizada")
        fixed_coordinate_distribution[coefficient] += 1

    require(len(catalogue & singer_space) == 82, "intersección catálogo/Singer")
    require(len(m_image_catalogue & catalogue) == 83, "intersección M(C)/C")
    require(len(set(projected_catalogue)) == 171, "imagen proyectada del catálogo")
    require(Counter(projected_multiplicity.values()) == Counter({1: 117, 2: 36, 3: 18}),
            "fibras de la proyección del catálogo")
    require(fixed_coordinate_distribution == Counter({0: 82, 1: 84, 2: 77}),
            "distribución de coordenada fija")

    # Acción D3^cat sobre el mismo conjunto de 243 palabras.
    r_matrix = permutation_matrix(R_PERMUTATION)
    s_matrix = permutation_matrix(S_PERMUTATION)
    d3_group = {
        tuple(tuple(x for x in row) for row in value)
        for exponent in range(3)
        for value in (matrix_power(r_matrix, exponent), matmul(matrix_power(r_matrix, exponent), s_matrix))
    }
    require(len(d3_group) == 6, "la representación D3 no tiene seis elementos")
    require(matmul(matmul(s_matrix, r_matrix), s_matrix) == matrix_power(r_matrix, 2), "srs != r^-1")
    require(all(permute(word, R_PERMUTATION) in catalogue for word in catalogue), "C no es r-invariante")
    require(all(permute(word, S_PERMUTATION) in catalogue for word in catalogue), "C no es s-invariante")
    d3_orbits = {d3_orbit(word) for word in catalogue}
    d3_histogram = Counter(len(orbit) for orbit in d3_orbits)
    require(len(d3_orbits) == 43 and d3_histogram == Counter({6: 38, 3: 5}), "órbitas D3^cat")

    singer_r_intersection = len(singer_space & {row_times(word, r_matrix) for word in singer_space})
    singer_s_intersection = len(singer_space & {row_times(word, s_matrix) for word in singer_space})
    require((singer_r_intersection, singer_s_intersection) == (81, 81),
            "intersecciones del sector Singer con sus imágenes D3")
    require(
        {row_times(word, r_matrix) for word in singer_space} != singer_space
        and {row_times(word, s_matrix) for word in singer_space} != singer_space,
        "el sector Singer resultó inesperadamente D3-invariante",
    )

    m_inverse = matrix_power(m, 241)
    conjugates = {
        "M^-1 r M": matmul(matmul(m_inverse, r_matrix), m),
        "M^-1 s M": matmul(matmul(m_inverse, s_matrix), m),
    }
    d3_group_lists = {tuple(tuple(row) for row in matrix) for matrix in d3_group}
    require(all(tuple(tuple(row) for row in value) not in d3_group_lists for value in conjugates.values()),
            "M normaliza inesperadamente D3^cat")
    orbit_internal_counts = Counter(
        sum(row_times(word, m) in catalogue for word in orbit)
        for orbit in d3_orbits
    )
    require(orbit_internal_counts == Counter({0: 6, 1: 11, 2: 12, 3: 9, 4: 4, 5: 1}),
            "distribución de retornos M por órbita D3")
    require(all(sum(row_times(word, m) in catalogue for word in orbit) < len(orbit) for orbit in d3_orbits),
            "alguna órbita D3 fue transportada íntegramente por M dentro de C")

    # Las tres palabras orientadas ya seleccionadas por D3^cat pertenecen a
    # una misma rebanada afín y a un mismo ciclo de longitud 242 de M.
    named_fixed_coordinates: dict[str, int] = {}
    for name, word in NAMED_WORDS.items():
        require(word in catalogue, f"{name} no está en el catálogo")
        coefficient = 2 * sum(x * y for x, y in zip(word, fixed_right_generator)) % P
        named_fixed_coordinates[name] = coefficient
    require(set(named_fixed_coordinates.values()) == {1}, "las tres palabras no comparten rebanada afín")

    def directed_distance(source: tuple[int, ...], target: tuple[int, ...]) -> int:
        current = source
        for exponent in range(242):
            if current == target:
                return exponent
            current = row_times(current, m)
        raise RuntimeError("dos palabras no pertenecen al mismo ciclo de M")

    named_gaps = {
        "pi_to_e": directed_distance(NAMED_WORDS["pi"], NAMED_WORDS["e"]),
        "e_to_phi": directed_distance(NAMED_WORDS["e"], NAMED_WORDS["phi"]),
        "phi_to_pi": directed_distance(NAMED_WORDS["phi"], NAMED_WORDS["pi"]),
    }
    require(named_gaps == {"pi_to_e": 34, "e_to_phi": 113, "phi_to_pi": 95},
            f"distancias Singer nombradas: {named_gaps}")
    require(sum(named_gaps.values()) == 242, "las tres distancias no cierran el ciclo")

    # Firmas de diferencias cíclicas: D_3 e D_4 no son el grupo D3^cat.
    difference_data: dict[str, object] = {}
    for step, expected_size, expected_kernel_rows in ((3, 27, 20), (4, 81, 4)):
        word_fibers = Counter(vector_difference(word, step) for word in catalogue)
        state_fibers = Counter(vector_difference(row["word"], step) for row in rows)
        require(len(word_fibers) == expected_size and len(state_fibers) == expected_size,
                f"imagen D_{step}")
        require(state_fibers[(0,) * N] == expected_kernel_rows, f"núcleo de estados D_{step}")
        difference_data[f"D{step}"] = {
            "ambient_rank": 3 if step == 3 else 4,
            "ambient_image_cardinality": expected_size,
            "catalogue_image_cardinality": len(word_fibers),
            "catalogue_word_fiber_size_histogram": counter_json(Counter(word_fibers.values())),
            "catalogue_state_kernel_count": state_fibers[(0,) * N],
        }

    d3_difference_matrix = matrix_sub(identity, permutation_matrix((3, 4, 5, 0, 1, 2)))
    d4_difference_matrix = matrix_sub(identity, permutation_matrix((4, 5, 0, 1, 2, 3)))
    commutator_ranks = {
        "[M,D3_difference]": rank_mod3(matrix_sub(matmul(m, d3_difference_matrix), matmul(d3_difference_matrix, m))),
        "[M,D4_difference]": rank_mod3(matrix_sub(matmul(m, d4_difference_matrix), matmul(d4_difference_matrix, m))),
    }
    require(commutator_ranks == {"[M,D3_difference]": 4, "[M,D4_difference]": 5},
            "conmutadores con diferencias cíclicas")

    result = {
        "status": "PASS_EXACT_SPECTRAL_ANATOMY_WITH_TYPE_SEPARATION",
        "field": "F3",
        "source_hashes": {str(path.relative_to(ROOT)): expected for path, expected in EXPECTED_HASHES.items()},
        "matrix_orders": orders,
        "characteristic_polynomials_coefficients_low_to_high": charpolys,
        "minimum_polynomials_coefficients_low_to_high": minpolys,
        "irreducible_factor_root_orders": irreducible_orders,
        "module_decompositions": {
            "L0": "F3_(+1) direct_sum F3_(-1) direct_sum F81; cyclic and semisimple",
            "L1": "F3_(+1)^2 direct_sum F3_(-1) direct_sum F27; semisimple; F27 root order 13, not 26",
            "M=L0L1": "F3_fixed direct_sum F243; cyclic and semisimple; primitive degree-five sector",
            "C=L0^2L1^2": "one (-1)-line, one size-two Jordan block at +1, and a primitive F27 sector",
            "L1_invariant_factors": ["x-1", "(x-1)(x+1)(x^3+x^2+2)"],
        },
        "correction": {
            "claim_corrected": "the cubic factor x^3+x^2+2 of L1 is primitive of order 26",
            "exact_result": "it is irreducible with root order 13; ord(L1)=26 comes from lcm(13,2)",
        },
        "calendar_distinction": {
            "alternating_product_M": "L0L1 has order 242 and the F243 Singer sector",
            "published_four_step_total": "L0^2L1^2 has order 78 and is not semisimple",
            "conclusion": "the Singer cycle is an exact joint coordinate of L0,L1, not the total 0011 calendar map",
        },
        "M_degree_five_sector": {
            "fixed_projector": p_fixed,
            "singer_projector": p_singer,
            "fixed_left_generator": fixed_left_generator,
            "fixed_right_generator": fixed_right_generator,
            "singer_hyperplane_equation": "v1 + 2*v4 + v6 = 0 in F3",
            "cardinality": len(singer_space),
            "orbit_histogram_on_F3^6": counter_json(orbit_lengths(m)),
            "orbit_histogram_on_singer_sector": counter_json(singer_orbit_lengths),
        },
        "catalogue_243_comparison": {
            "catalogue_cardinality": len(catalogue),
            "zero_present": False,
            "linear_span_rank": 6,
            "affine_hull_rank": affine_hull_rank,
            "affine_basepoint_for_certificate": affine_basepoint,
            "addition_counterexample": addition_witness,
            "intersection_with_linear_singer_sector": len(catalogue & singer_space),
            "intersection_M_catalogue_with_catalogue": len(m_image_catalogue & catalogue),
            "singer_projection_image_cardinality": len(set(projected_catalogue)),
            "singer_projection_fiber_histogram": counter_json(Counter(projected_multiplicity.values())),
            "fixed_coordinate_distribution": counter_json(fixed_coordinate_distribution),
            "coset_intersections_a_f_plus_W": counter_json(fixed_coordinate_distribution),
        },
        "D3_catalogue_action": {
            "group_order": len(d3_group),
            "catalogue_invariant": True,
            "orbit_count": len(d3_orbits),
            "orbit_size_histogram": counter_json(d3_histogram),
            "singer_sector_invariant_under_r_or_s": False,
            "singer_intersection_with_r_image": singer_r_intersection,
            "singer_intersection_with_s_image": singer_s_intersection,
            "M_normalizes_D3": False,
            "M_maps_no_complete_D3_orbit_inside_catalogue": True,
            "M_internal_return_count_per_D3_orbit_histogram": counter_json(orbit_internal_counts),
        },
        "named_words_in_M_cycle": {
            "fixed_coordinates": named_fixed_coordinates,
            "directed_gaps": named_gaps,
            "gap_sum": sum(named_gaps.values()),
            "interpretation": (
                "after the D3 catalogue selector has named the oriented words, M orders them on one affine "
                "Singer cycle; this is an exact cross-coordinate relation, not an independent selector"
            ),
        },
        "cyclic_difference_signatures": difference_data,
        "commutator_ranks_with_cyclic_differences": commutator_ranks,
        "logical_conclusion": {
            "new_exact_structure": (
                "L0L1 canonically splits F3^6 into a fixed line and a primitive five-dimensional sector "
                "isomorphic as an F3[x]-module to F243; its nonzero vectors form one 242-cycle"
            ),
            "not_a_selector": (
                "the 243 N33 words are neither that linear sector nor an invariant orbit of L0L1; the "
                "Singer construction therefore coordinates the ambient space but does not select the "
                "catalogue or pi/e/phi from APP independently"
            ),
        },
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "output": OUTPUT.relative_to(ROOT).as_posix(),
        "orders": orders,
        "root_orders": irreducible_orders,
        "catalogue_intersection_singer": len(catalogue & singer_space),
        "named_gaps": named_gaps,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
