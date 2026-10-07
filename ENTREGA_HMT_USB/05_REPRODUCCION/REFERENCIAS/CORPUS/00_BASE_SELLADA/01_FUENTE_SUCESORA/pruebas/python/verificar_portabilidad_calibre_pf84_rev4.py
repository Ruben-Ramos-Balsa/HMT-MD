#!/usr/bin/env python3
"""Verifica el transporte de calibre PF84→REV.4 y los periodos de T1.

No usa ``assert``. La salida JSON es determinista y coincide bajo Python
normal y ``-O``. Las matrices actúan sobre vectores fila a la derecha.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


P = 3
N = 6
ROOT = Path(__file__).resolve().parents[2]
PALEY_WITT_PATH = ROOT / "manuscrito/sections/hmt/09a_paley_codigo_witt.tex"
READER_CHART_PATH = ROOT / "manuscrito/sections/hmt/06_regiones_constantes.tex"
PERMUTATION_ONE_BASED = (1, 2, 3, 5, 6, 4)

T0_84 = (
    (2, 2, 2, 1, 2, 1),
    (2, 1, 2, 2, 1, 1),
    (1, 0, 0, 1, 0, 2),
    (0, 0, 1, 1, 1, 0),
    (2, 2, 2, 0, 2, 1),
    (2, 1, 2, 1, 0, 0),
)
T1_84 = (
    (2, 1, 2, 0, 2, 2),
    (1, 2, 1, 1, 2, 0),
    (1, 2, 1, 1, 1, 2),
    (0, 1, 0, 0, 2, 1),
    (2, 0, 2, 1, 0, 1),
    (0, 2, 2, 2, 1, 1),
)
A_W_84 = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 1, 2, 2),
    (1, 1, 0, 2, 1, 2),
    (1, 1, 2, 0, 2, 1),
    (1, 2, 1, 2, 0, 1),
    (1, 2, 2, 1, 1, 0),
)

VECTOR_CASES = {
    "w_pi": ((0, 1, 0, 2, 1, 1), (0, 1, 0, 1, 1, 2)),
    "w_e": ((2, 0, 1, 1, 0, 1), (2, 0, 1, 0, 1, 1)),
    "w_phi": ((1, 2, 1, 2, 0, 0), (1, 2, 1, 0, 0, 2)),
    "q_phi": ((1, 2, 2, 1, 2, 0), (1, 2, 2, 2, 0, 1)),
    "q_hol": ((1, 2, 2, 0, 1, 1), (1, 2, 2, 1, 1, 0)),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def identity() -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(1 if row == column else 0 for column in range(N))
        for row in range(N)
    )


def transpose(matrix: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(matrix[row][column] for row in range(N)) for column in range(N))


def matmul(
    left: tuple[tuple[int, ...], ...],
    right: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            sum(left[row][inner] * right[inner][column] for inner in range(N))
            % P
            for column in range(N)
        )
        for row in range(N)
    )


def matpow(
    matrix: tuple[tuple[int, ...], ...], exponent: int
) -> tuple[tuple[int, ...], ...]:
    require(exponent >= 0, "exponente negativo")
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
    row: tuple[int, ...], matrix: tuple[tuple[int, ...], ...]
) -> tuple[int, ...]:
    return tuple(
        sum(row[inner] * matrix[inner][column] for inner in range(N)) % P
        for column in range(N)
    )


def scale_matrix(
    scalar: int, matrix: tuple[tuple[int, ...], ...]
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple((scalar * entry) % P for entry in row)
        for row in matrix
    )


def permutation_matrix() -> tuple[tuple[int, ...], ...]:
    # Para vectores fila, (vP)_j=v_{p_j}.
    result = [[0] * N for _ in range(N)]
    for column, source_one_based in enumerate(PERMUTATION_ONE_BASED):
        result[source_one_based - 1][column] = 1
    return tuple(tuple(row) for row in result)


def matrix_order(matrix: tuple[tuple[int, ...], ...], limit: int = 2000) -> int:
    current = identity()
    for exponent in range(1, limit + 1):
        current = matmul(current, matrix)
        if current == identity():
            return exponent
    raise RuntimeError(f"orden no hallado antes de {limit}")


def vector_period(row: tuple[int, ...], matrix: tuple[tuple[int, ...], ...]) -> int:
    current = row
    for exponent in range(1, 2000):
        current = row_times(current, matrix)
        if current == row:
            return exponent
    raise RuntimeError("periodo vectorial no hallado")


def stable_json(payload: object) -> str:
    return json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fragment_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    require(1 <= first <= last <= len(lines), f"rango inválido {path}:{first}-{last}")
    return hashlib.sha256("".join(lines[first - 1 : last]).encode("utf-8")).hexdigest()


def extract_pmatrix(
    path: Path, marker: str
) -> tuple[tuple[int, ...], ...]:
    text = path.read_text(encoding="utf-8")
    marker_at = text.find(marker)
    require(marker_at >= 0, f"marcador ausente en {path.name}: {marker}")
    begin = text.find(r"\begin{pmatrix}", marker_at)
    end = text.find(r"\end{pmatrix}", begin)
    require(begin >= 0 and end > begin, f"pmatrix ausente tras {marker}")
    body = text[begin + len(r"\begin{pmatrix}") : end]
    rows = []
    for raw_row in re.split(r"\\\\", body):
        entries = re.findall(r"(?<![A-Za-z])[-]?\d+", raw_row)
        if entries:
            rows.append(tuple(int(entry) % P for entry in entries))
    matrix = tuple(rows)
    require(
        len(matrix) == N and all(len(row) == N for row in matrix),
        f"matriz {marker} no es {N}x{N}",
    )
    return matrix


def extract_word(path: Path, marker: str) -> tuple[int, ...]:
    text = path.read_text(encoding="utf-8")
    marker_at = text.find(marker)
    require(marker_at >= 0, f"palabra ausente en {path.name}: {marker}")
    match = re.search(r"[012]{6}", text[marker_at + len(marker) :])
    require(match is not None, f"valor ternario ausente tras {marker}")
    return tuple(int(digit) for digit in match.group(0))


def verify() -> dict[str, object]:
    require(PALEY_WITT_PATH.is_file(), "residencia Paley-Witt ausente")
    require(READER_CHART_PATH.is_file(), "residencia del lector ausente")
    permutation = permutation_matrix()
    permutation_t = transpose(permutation)
    require(matmul(permutation_t, permutation) == identity(), "P no es ortogonal")

    transported_vectors: dict[str, list[int]] = {}
    for name, (source, expected) in VECTOR_CASES.items():
        transported = row_times(source, permutation)
        require(transported == expected, f"transporte incorrecto de {name}")
        transported_vectors[name] = list(transported)

    a_w_rev4 = matmul(matmul(permutation_t, A_W_84), permutation)
    t0_rev4 = matmul(matmul(permutation_t, T0_84), permutation)
    t1_rev4 = matmul(matmul(permutation_t, T1_84), permutation)
    active_a_w = extract_pmatrix(PALEY_WITT_PATH, "A_W=")
    active_l0 = extract_pmatrix(READER_CHART_PATH, "L_0=")
    active_l1 = extract_pmatrix(READER_CHART_PATH, "L_1=")
    require(active_a_w == a_w_rev4, "A_W transportada no coincide con REV.4")
    require(active_l0 == T0_84, "L_0 activo no coincide con el calibre lector")
    require(active_l1 == T1_84, "L_1 activo no coincide con el calibre lector")
    active_reader_words = {
        "w_pi": extract_word(READER_CHART_PATH, r"w_\pi="),
        "w_e": extract_word(READER_CHART_PATH, r"w_e="),
        "w_phi": extract_word(READER_CHART_PATH, r"w_\varphi="),
    }
    for name, active_word in active_reader_words.items():
        require(
            active_word == VECTOR_CASES[name][0],
            f"{name} activo no coincide con el calibre lector publicado",
        )
    require(
        matmul(A_W_84, A_W_84) == scale_matrix(2, identity()),
        "A_W^2 no es -I",
    )
    a_w_inv_84 = scale_matrix(2, A_W_84)
    a_w_inv_rev4 = scale_matrix(2, a_w_rev4)
    require(matmul(a_w_rev4, a_w_inv_rev4) == identity(), "inversa REV.4")

    q_phi_84 = VECTOR_CASES["q_phi"][0]
    q_hol_84 = row_times(row_times(q_phi_84, matpow(T1_84, 6)), a_w_inv_84)
    require(q_hol_84 == VECTOR_CASES["q_hol"][0], "holonomía PF84")

    q_phi_rev4 = VECTOR_CASES["q_phi"][1]
    q_hol_rev4 = row_times(
        row_times(q_phi_rev4, matpow(t1_rev4, 6)), a_w_inv_rev4
    )
    require(q_hol_rev4 == VECTOR_CASES["q_hol"][1], "holonomía REV.4")

    order_t1 = matrix_order(T1_84)
    period_q_phi = vector_period(q_phi_84, T1_84)
    require(order_t1 == 26, f"ord(T1)={order_t1}, no 26")
    require(period_q_phi == 13, f"periodo q_phi={period_q_phi}, no 13")
    matches = [
        exponent
        for exponent in range(1, 53)
        if row_times(
            row_times(q_phi_84, matpow(T1_84, exponent)), a_w_inv_84
        )
        == q_hol_84
    ]
    require(matches == [6, 19, 32, 45], f"clase periódica inesperada: {matches}")

    script_path = Path(__file__).resolve()
    return {
        "status": "PASS_PORTABILIDAD_CALIBRE_PF84_REV4",
        "field": "F3",
        "row_vector_convention": True,
        "permutation_one_based": list(PERMUTATION_ONE_BASED),
        "transport_formula": "A_REV4=P^T A_PF84 P; v_REV4=v_PF84 P",
        "chart_roles": {
            "pf84_orbital_source": (
                "A_W^PF84, T0^PF84, T1^PF84 y vectores fuente "
                "en el calibre orbital del volumen PF84"
            ),
            "rev4_reader_published": (
                "L0, L1 y w_pi,w_e,w_phi publicados sin permutar; "
                "constituyen la carta activa del lector"
            ),
            "rev4_paley_witt": (
                "A_W activo de Paley-Witt; es el destino de "
                "P^T A_W^PF84 P"
            ),
            "transported_witt_chart": (
                "T0,T1 y vectores conjugados por P son una carta "
                "transportada calculada, no una sustitución silenciosa "
                "de L0,L1 y palabras publicadas"
            ),
        },
        "active_source_locators": {
            "rev4_paley_witt": (
                "manuscrito/sections/hmt/09a_paley_codigo_witt.tex:65-91"
            ),
            "rev4_reader_matrices": (
                "manuscrito/sections/hmt/06_regiones_constantes.tex:252-278"
            ),
            "rev4_reader_words": (
                "manuscrito/sections/hmt/06_regiones_constantes.tex:303-323"
            ),
        },
        "active_source_sha256s": {
            "rev4_paley_witt_file": sha256(PALEY_WITT_PATH),
            "rev4_paley_witt_fragment_65_91": fragment_sha256(
                PALEY_WITT_PATH, 65, 91
            ),
            "rev4_reader_file": sha256(READER_CHART_PATH),
            "rev4_reader_matrices_fragment_252_278": fragment_sha256(
                READER_CHART_PATH, 252, 278
            ),
            "rev4_reader_words_fragment_303_323": fragment_sha256(
                READER_CHART_PATH, 303, 323
            ),
        },
        "active_reader_chart": {
            "L0": [list(row) for row in active_l0],
            "L1": [list(row) for row in active_l1],
            "words": {
                name: list(word) for name, word in active_reader_words.items()
            },
        },
        "active_paley_witt_matrix": [list(row) for row in active_a_w],
        "transported_vectors": transported_vectors,
        "q_hol_pf84": list(q_hol_84),
        "q_hol_rev4": list(q_hol_rev4),
        "t1_matrix_order": order_t1,
        "q_phi_orbit_period": period_q_phi,
        "holonomy_match_exponents_1_to_52": matches,
        "unique_match_in_window_1_to_12": matches[:1] == [6],
        "verifier_sha256": sha256(script_path),
        "computed_transported_witt_chart_matrices": {
            "A_W": [list(row) for row in a_w_rev4],
            "T0": [list(row) for row in t0_rev4],
            "T1": [list(row) for row in t1_rev4],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-certificate",
        type=Path,
        help="Escribe el mismo JSON determinista en esta ruta.",
    )
    args = parser.parse_args()
    payload = verify()
    rendered = stable_json(payload) + "\n"
    if args.write_certificate is not None:
        args.write_certificate.parent.mkdir(parents=True, exist_ok=True)
        args.write_certificate.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
