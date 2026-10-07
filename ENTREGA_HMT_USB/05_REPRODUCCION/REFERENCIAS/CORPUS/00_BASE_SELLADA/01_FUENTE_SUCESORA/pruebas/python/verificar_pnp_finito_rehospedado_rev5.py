#!/usr/bin/env python3
"""Rehospeda sin ``assert`` los controles finitos PNP-08--PNP-16.

La salida es determinista y el programa es de sólo lectura salvo que se
proporcione explícitamente ``--write-certificate``. Las matrices actúan
sobre vectores fila a la derecha.
"""

from __future__ import annotations

import argparse
from collections import deque
import hashlib
import json
from pathlib import Path


MODULUS = 3
DIMENSION = 6
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CERTIFICATE = ROOT / "certificados/pnp_finito_rehospedado_rev5.json"

T0 = (
    (2, 2, 2, 1, 2, 1),
    (2, 1, 2, 2, 1, 1),
    (1, 0, 0, 1, 0, 2),
    (0, 0, 1, 1, 1, 0),
    (2, 2, 2, 0, 2, 1),
    (2, 1, 2, 1, 0, 0),
)
T1 = (
    (2, 1, 2, 0, 2, 2),
    (1, 2, 1, 1, 2, 0),
    (1, 2, 1, 1, 1, 2),
    (0, 1, 0, 0, 2, 1),
    (2, 0, 2, 1, 0, 1),
    (0, 2, 2, 2, 1, 1),
)
A_W_ORBITAL = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 1, 2, 2),
    (1, 1, 0, 2, 1, 2),
    (1, 1, 2, 0, 2, 1),
    (1, 2, 1, 2, 0, 1),
    (1, 2, 2, 1, 1, 0),
)
PERMUTATION_ONE_BASED = (1, 2, 3, 5, 6, 4)

W_PI = (0, 1, 0, 2, 1, 1)
W_E = (2, 0, 1, 1, 0, 1)
W_PHI = (1, 2, 1, 2, 0, 0)
Q_PHI = (1, 2, 2, 1, 2, 0)
Q_HOL_ORBITAL = (1, 2, 2, 0, 1, 1)
Q_HOL_REV4 = (1, 2, 2, 1, 1, 0)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def identity() -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(1 if row == column else 0 for column in range(DIMENSION))
        for row in range(DIMENSION)
    )


def transpose(
    matrix: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(matrix[row][column] for row in range(DIMENSION))
        for column in range(DIMENSION)
    )


def matmul(
    left: tuple[tuple[int, ...], ...],
    right: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            sum(left[row][inner] * right[inner][column]
                for inner in range(DIMENSION))
            % MODULUS
            for column in range(DIMENSION)
        )
        for row in range(DIMENSION)
    )


def matpow(
    matrix: tuple[tuple[int, ...], ...],
    exponent: int,
) -> tuple[tuple[int, ...], ...]:
    require(exponent >= 0, "exponente matricial negativo")
    result = identity()
    factor = matrix
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = matmul(result, factor)
        factor = matmul(factor, factor)
        remaining >>= 1
    return result


def row_times(
    vector: tuple[int, ...],
    matrix: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    return tuple(
        sum(vector[inner] * matrix[inner][column]
            for inner in range(DIMENSION))
        % MODULUS
        for column in range(DIMENSION)
    )


def scale(
    scalar: int,
    matrix: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple((scalar * entry) % MODULUS for entry in row)
        for row in matrix
    )


def determinant(matrix: tuple[tuple[int, ...], ...]) -> int:
    work = [list(row) for row in matrix]
    result = 1
    for column in range(DIMENSION):
        pivot = next(
            (row for row in range(column, DIMENSION)
             if work[row][column] % MODULUS),
            None,
        )
        require(pivot is not None, "matriz singular")
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        pivot_value = work[column][column] % MODULUS
        result = (result * pivot_value) % MODULUS
        inverse = pow(pivot_value, -1, MODULUS)
        work[column] = [(entry * inverse) % MODULUS for entry in work[column]]
        for row in range(column + 1, DIMENSION):
            factor = work[row][column] % MODULUS
            if factor:
                work[row] = [
                    (left - factor * right) % MODULUS
                    for left, right in zip(work[row], work[column])
                ]
    return result % MODULUS


def permutation_matrix() -> tuple[tuple[int, ...], ...]:
    result = [[0] * DIMENSION for _ in range(DIMENSION)]
    for column, source_one_based in enumerate(PERMUTATION_ONE_BASED):
        result[source_one_based - 1][column] = 1
    return tuple(tuple(row) for row in result)


def orbit(seed: tuple[int, ...]) -> set[tuple[int, ...]]:
    seen = {seed}
    queue = deque([seed])
    while queue:
        current = queue.popleft()
        for generator in (T0, T1):
            following = row_times(current, generator)
            if following not in seen:
                seen.add(following)
                queue.append(following)
    return seen


def matrix_order(matrix: tuple[tuple[int, ...], ...]) -> int:
    current = identity()
    for exponent in range(1, 2000):
        current = matmul(current, matrix)
        if current == identity():
            return exponent
    raise RuntimeError("orden matricial no hallado")


def vector_period(
    vector: tuple[int, ...],
    matrix: tuple[tuple[int, ...], ...],
) -> int:
    current = vector
    for exponent in range(1, 2000):
        current = row_times(current, matrix)
        if current == vector:
            return exponent
    raise RuntimeError("periodo vectorial no hallado")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify() -> dict[str, object]:
    negative_identity = scale(2, identity())
    require(determinant(T0) == 1, "det(T0) no es uno")
    require(determinant(T1) == 2, "det(T1) no es dos")
    require(determinant(A_W_ORBITAL) == 1, "det(A_W) no es uno")
    require(
        matmul(A_W_ORBITAL, A_W_ORBITAL) == negative_identity,
        "A_W^2 no es -I",
    )
    a_w_inverse = scale(2, A_W_ORBITAL)
    require(row_times(Q_PHI, A_W_ORBITAL) == W_PHI, "q_phi A_W != w_phi")

    nonzero_orbit = orbit(Q_PHI)
    require(len(nonzero_orbit) == 728, "la órbita no tiene 728 estados")
    require((0,) * DIMENSION not in nonzero_orbit, "la órbita contiene cero")

    after_six = row_times(Q_PHI, matpow(T1, 6))
    q_hol = row_times(after_six, a_w_inverse)
    require(q_hol == Q_HOL_ORBITAL, "holonomía orbital incorrecta")

    q_pi = row_times(W_PI, a_w_inverse)
    q_e = row_times(W_E, a_w_inverse)
    ablations = {
        "without_witt_closure": after_six,
        "with_A_W_not_inverse": row_times(after_six, A_W_ORBITAL),
        "with_T0": row_times(row_times(Q_PHI, matpow(T0, 6)), a_w_inverse),
        "with_q_pi": row_times(row_times(q_pi, matpow(T1, 6)), a_w_inverse),
        "with_q_e": row_times(row_times(q_e, matpow(T1, 6)), a_w_inverse),
    }
    require(
        all(value != Q_HOL_ORBITAL for value in ablations.values()),
        "una ablación reproduce la holonomía",
    )

    matches = [
        exponent
        for exponent in range(1, 53)
        if row_times(
            row_times(Q_PHI, matpow(T1, exponent)),
            a_w_inverse,
        )
        == Q_HOL_ORBITAL
    ]
    require(matches[:1] == [6], "k=6 no es la primera coincidencia")
    require(
        [value for value in matches if value <= 12] == [6],
        "k=6 no es único en la ventana 1..12",
    )
    period = vector_period(Q_PHI, T1)
    order = matrix_order(T1)
    require(period == 13, "el periodo de q_phi no es 13")
    require(order == 26, "el orden de T1 no es 26")
    require(matches == [6, 19, 32, 45], "clase k=6 mod 13 incorrecta")

    permutation = permutation_matrix()
    permutation_t = transpose(permutation)
    require(matmul(permutation_t, permutation) == identity(), "P no es ortogonal")
    a_w_rev4 = matmul(
        matmul(permutation_t, A_W_ORBITAL),
        permutation,
    )
    transported_q_hol = row_times(Q_HOL_ORBITAL, permutation)
    require(transported_q_hol == Q_HOL_REV4, "q_hol REV.4 incorrecto")

    script = Path(__file__).resolve()
    return {
        "status": "PASS_PNP_FINITO_REHOSPEDADO_REV5",
        "field": "F3",
        "row_vector_convention": True,
        "determinants": {"T0": 1, "T1": 2, "A_W_orbital": 1},
        "A_W_squared": "-I",
        "q_phi": list(Q_PHI),
        "q_hol_orbital": list(q_hol),
        "q_hol_rev4": list(transported_q_hol),
        "orbit_nonzero_size": len(nonzero_orbit),
        "ablations": {key: list(value) for key, value in sorted(ablations.items())},
        "matches_1_to_52": matches,
        "unique_match_1_to_12": True,
        "q_phi_period": period,
        "T1_order": order,
        "permutation_one_based": list(PERMUTATION_ONE_BASED),
        "transport_formula": "A_REV4=P^T A_orb P; v_REV4=v_orb P",
        "A_W_rev4": [list(row) for row in a_w_rev4],
        "script_sha256": sha256(script),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-certificate",
        nargs="?",
        const=DEFAULT_CERTIFICATE,
        type=Path,
        help=(
            "Escribe la salida determinista; sin ruta usa la residencia "
            "canónica. Por defecto el verificador es de sólo lectura."
        ),
    )
    args = parser.parse_args()
    payload = verify()
    rendered = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ) + "\n"
    if args.write_certificate is not None:
        args.write_certificate.parent.mkdir(parents=True, exist_ok=True)
        args.write_certificate.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
