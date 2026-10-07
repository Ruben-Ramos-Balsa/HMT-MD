#!/usr/bin/env python3
"""Certifica la estratificación del sello bajo la rotación interna de Witt.

El sello sólo se usa como objeto de contraste ya fijado. El programa no
presenta la estratificación como generador de K: calcula, para cada bloque,
su primera entrada en el catálogo de 243 palabras bajo J=A_W y conserva las
superposiciones entre hojas que impiden deducir una selección por cardinalidad.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CURRENT = ROOT / "03_PAPER/HMT_MACROPAPER_V3/CURRENT.json"
N33_INDEX = ROOT / (
    "06_NUEVOS_PAQUETES/HMT_N33_PI_E_PHI_CLOSEOUT_v3/"
    "HMT_N33_PI_PHI_E_CLOSEOUT/n33_w6_index.json"
)
DIRECTIONAL_CERTIFICATE = HERE / "RESULTADO_REGISTRO_DIRECCIONAL_108.json"
CERTIFICATE = HERE / "RESULTADO_ESTRATIFICACION_WITT_SELLO.json"

A_W = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 1, 2, 2),
    (1, 1, 0, 2, 1, 2),
    (1, 1, 2, 0, 2, 1),
    (1, 2, 1, 2, 0, 1),
    (1, 2, 2, 1, 1, 0),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def matrix_product(a: tuple[tuple[int, ...], ...], b: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(6)) % 3 for j in range(6))
        for i in range(6)
    )


def transform(word: str) -> str:
    vector = tuple(int(digit) for digit in word)
    return "".join(
        str(sum(vector[i] * A_W[i][j] for i in range(6)) % 3)
        for j in range(6)
    )


def negative(word: str) -> str:
    return "".join(str((-int(digit)) % 3) for digit in word)


def ternary_fraction_digits(numerator: int, denominator: int, length: int) -> str:
    remainder = numerator
    digits: list[str] = []
    for _ in range(length):
        remainder *= 3
        digit, remainder = divmod(remainder, denominator)
        require(digit in (0, 1, 2), "dígito ternario fuera de rango")
        digits.append(str(digit))
    return "".join(digits)


def orbit(word: str) -> list[str]:
    values = [word]
    for _ in range(3):
        values.append(transform(values[-1]))
    require(transform(values[-1]) == word, "la órbita de Witt no cerró en cuatro pasos")
    return values


def first_entry(word: str, catalogue: set[str]) -> tuple[int | None, list[int], list[str]]:
    values = orbit(word)
    memberships = [index for index, value in enumerate(values) if value in catalogue]
    return (memberships[0] if memberships else None, memberships, values)


def build() -> dict[str, object]:
    current = json.loads(CURRENT.read_text(encoding="utf-8"))
    require(current["revision"] == "2026-07-22.2", "revisión canónica inesperada")
    catalogue_data = json.loads(N33_INDEX.read_text(encoding="utf-8"))
    catalogue = set(catalogue_data["words"])
    require(len(catalogue) == 243, "el catálogo visible dejó de contener 243 palabras")

    identity = tuple(tuple(int(i == j) for j in range(6)) for i in range(6))
    minus_identity = tuple(tuple((2 if i == j else 0) for j in range(6)) for i in range(6))
    aw2 = matrix_product(A_W, A_W)
    aw4 = matrix_product(aw2, aw2)
    require(aw2 == minus_identity, "A_W^2 dejó de ser -I")
    require(aw4 == identity, "A_W^4 dejó de ser I")

    all_depths: Counter[str] = Counter()
    for digits in itertools.product("012", repeat=6):
        word = "".join(digits)
        depth, _, _ = first_entry(word, catalogue)
        all_depths["none" if depth is None else str(depth)] += 1
    require(all_depths == Counter({"0": 243, "1": 163, "2": 130, "3": 88, "none": 105}),
            "la estratificación global de F3^6 cambió")

    seal = [int(value) for value in current["state_types"]["CanonicalSealK"]["coordinates"]]
    decimal_word = "".join(f"{value:03d}" for value in seal)
    ternary72 = ternary_fraction_digits(int(decimal_word), 10 ** len(decimal_word), 72)
    blocks = [ternary72[index:index + 6] for index in range(0, 72, 6)]
    require(len(blocks) == 12, "el sello no produjo doce bloques ternarios")

    records: list[dict[str, object]] = []
    first_depths: list[int] = []
    psi_visible_positions: list[int] = []
    overlaps: list[int] = []
    for position, word in enumerate(blocks, start=1):
        depth, memberships, values = first_entry(word, catalogue)
        require(depth is not None, f"el bloque {position} no entra en la órbita saturada")
        first_depths.append(depth)
        if 2 in memberships:
            psi_visible_positions.append(position)
        if len(memberships) > 1:
            overlaps.append(position)
        records.append({
            "position_one_based": position,
            "raw_block": word,
            "Witt_orbit_J0_J1_J2_J3": values,
            "catalogue_membership_exponents": memberships,
            "first_entry_depth": depth,
            "Psi_minus_raw": negative(word),
        })

    expected_depths = [0, 1, 0, 2, 0, 2, 2, 0, 2, 1, 2, 0]
    require(first_depths == expected_depths, "cambió la estratificación del sello")
    depth_positions = {
        str(depth): [index + 1 for index, value in enumerate(first_depths) if value == depth]
        for depth in range(4)
    }
    require(depth_positions == {
        "0": [1, 3, 5, 8, 12],
        "1": [2, 10],
        "2": [4, 6, 7, 9, 11],
        "3": [],
    }, "cambiaron los estratos 5+2+5")
    require(psi_visible_positions == [1, 4, 5, 6, 7, 9, 11],
            "cambió el soporte 7/5 de Psi=-")
    require(overlaps == [1, 3, 4, 5, 6, 8], "cambiaron las superposiciones de hojas")

    directional = json.loads(DIRECTIONAL_CERTIFICATE.read_text(encoding="utf-8"))
    require(directional["exact_periodicity"]["period_in_nine_step_windows"] == 6,
            "el certificado direccional dejó de probar período seis")
    require(any(first_depths[index] != first_depths[index + 6] for index in range(6)),
            "la profundidad Witt se volvió de período seis")
    require(all(first_depths[index] != first_depths[index + 6] for index in range(6)),
            "alguna pareja antipodal dejó de distinguirse")

    return {
        "schema": "HMT.Witt-stratification-of-seal.v1",
        "status": "PASS_ESTRATIFICACION_WITT_5_2_5_Y_LIMITE_SELECTOR",
        "current_revision": current["revision"],
        "authors": ["Oumar Haidara Fall", "Rubén Ramos Balsa"],
        "source_sha256": {
            relative(CURRENT): sha256(CURRENT),
            relative(N33_INDEX): sha256(N33_INDEX),
            relative(DIRECTIONAL_CERTIFICATE): sha256(DIRECTIONAL_CERTIFICATE),
        },
        "fixed_Witt_operator": {
            "A_W": [list(row) for row in A_W],
            "A_W_squared": "-I sobre F3",
            "A_W_order": 4,
        },
        "catalogue": {
            "size": len(catalogue),
            "ambient_size": 729,
            "first_entry_stratum_sizes_on_all_F3_6": dict(sorted(all_depths.items())),
        },
        "seal_as_posterior_object": {
            "decimal_coordinates": seal,
            "first_72_ternary_digits": ternary72,
            "blocks": blocks,
            "records": records,
        },
        "exact_results": {
            "Psi_equals_minus_membership_positions": psi_visible_positions,
            "Psi_equals_minus_complement_positions": [
                position for position in range(1, 13) if position not in psi_visible_positions
            ],
            "first_entry_depth_sequence": first_depths,
            "first_entry_positions": depth_positions,
            "first_entry_profile": [5, 2, 5, 0],
            "positions_with_multiple_admissible_Witt_exponents": overlaps,
            "all_twelve_enter_by_J_squared": True,
        },
        "selector_diagnosis": {
            "what_is_exact": (
                "El operador J previamente fijado estratifica palabra por palabra los doce bloques "
                "en 5 entradas inmediatas, 2 tras un cuarto de vuelta y 5 tras media vuelta."
            ),
            "why_7_plus_5_is_not_enough": (
                "La pertenencia a la hoja Psi=- define el soporte 7/5, pero seis posiciones "
                "pertenecen a varias hojas de la órbita; la cardinalidad no fija un exponente único."
            ),
            "why_this_is_not_a_generator": (
                "La profundidad se calcula después de suministrar cada bloque del sello. "
                "No produce el siguiente bloque ni su orden dodecafásico."
            ),
            "directional_book_cannot_select_the_depth_sequence": (
                "El libro N/E/S/O tiene período seis y la secuencia de profundidades distingue "
                "las seis parejas m,m+6; ningún lector local equivariante de ese libro la produce."
            ),
        },
        "provenance": {
            "architecture": "ARQUITECTURA_AUTORAL_PREEXISTENTE: A_W, Psi=- y catálogo N33",
            "formalization": "FORMALIZACION_NUEVA: profundidad mínima de entrada en el catálogo bajo J",
            "certificate": "CERTIFICADO_NUEVO: estratos globales 243/163/130/88/105 y perfil del sello 5/2/5",
            "strength": "RECONOCIMIENTO_ESTRUCTURAL_POSTERIOR; no selector generativo de K",
        },
    }


def render(result: dict[str, object]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--check-certificate", action="store_true")
    args = parser.parse_args(argv)
    text = render(build())
    if args.write_certificate:
        CERTIFICATE.write_text(text, encoding="utf-8")
    if args.check_certificate:
        require(CERTIFICATE.exists(), "falta el certificado congelado")
        require(CERTIFICATE.read_text(encoding="utf-8") == text, "el certificado congelado no coincide")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
