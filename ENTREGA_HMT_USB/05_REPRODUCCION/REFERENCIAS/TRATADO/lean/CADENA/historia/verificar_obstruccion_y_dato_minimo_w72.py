#!/usr/bin/env python3
"""Certifica la obstrucción fase--carga y la interfaz mínima W24 -> K -> U12.

El programa separa dos resultados.

1. Recorre las cien fronteras N69 y toda la familia natural de caracteres
   locales obtenida comparando la fase con la carga visible o con la carga
   Witt--dual, admitiendo las tres traslaciones de fase y las dos
   orientaciones. Esa familia no produce el décimo bloque de W72. Un carácter
   afín adicional, rho_W + fase, sí lo produce en t=30. Esto es un resultado
   de cobertura; no inventa una ordenación dodecafásica.

2. Dado el prefijo W24, que fija K_1,K_2,K_3, identifica el dato lineal mínimo
   que reconstruye el sello completo: nueve diferencias orientadas sobre un
   bosque de Cayley de Z/12 generado por los pasos 3 y 4. La carta formada por
   las tres raíces y esas nueve diferencias es unimodular (determinante -1).

Ni K ni alpha intervienen en la definición de los lectores o de la fórmula
de reconstrucción. Las coordenadas canónicas publicadas se usan sólo al final
como control de la evaluación de la interfaz mínima.
"""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
from typing import Iterable


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
CURRENT = PROJECT / "03_PAPER/HMT_MACROPAPER_V3/CURRENT.json"
N69 = PROJECT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_CADENA_VIGENTE/N69_CALENDARIO_TRANSICION/"
    "HMT_N69_ley_transicion_o_axioma_cilindrico_v1/"
    "N69_signatures_t0_t99.csv"
)
OUT = HERE / "RESULTADO_OBSTRUCCION_Y_DATO_MINIMO_W72.json"

W72_BLOCKS = (
    "020022", "222111", "211201", "021101",
    "002001", "020111", "200110", "121012",
    "010122", "001001", "221110", "222110",
)
W24 = "".join(W72_BLOCKS[:4])

A_W = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 1, 2, 2),
    (1, 1, 0, 2, 1, 2),
    (1, 1, 2, 0, 2, 1),
    (1, 2, 1, 2, 0, 1),
    (1, 2, 2, 1, 1, 0),
)

H4 = (
    (1, 1, 1, 1),
    (1, 1, -1, -1),
    (1, -1, 1, -1),
    (1, -1, -1, 1),
)

# Bosque en Cay(Z/12; +3,+4), con raíces 0,1,2. El orden es topológico.
ROOTS = (0, 1, 2)
FOREST = (
    (0, 3, 3),
    (0, 4, 4),
    (3, 6, 3),
    (3, 7, 4),
    (4, 8, 4),
    (6, 9, 3),
    (6, 10, 4),
    (7, 11, 4),
    (1, 5, 4),
)

# Valores de la carta mínima, leídos de las cartas publicadas D3/D4. No se
# presentan como salida de N69: son precisamente el dato que debe emitir un
# agregador dodecafásico para cerrar la flecha.
CANONICAL_EDGE_DATA = (-495, -425, 108, 671, -255, -173, 475, -543, -281)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def transform(word: str, matrix: tuple[tuple[int, ...], ...]) -> str:
    vector = tuple(int(value) for value in word)
    return "".join(
        str(sum(vector[i] * matrix[i][j] for i in range(6)) % 3)
        for j in range(6)
    )


def linear_word(rows: tuple[str, str, str], coefficients: tuple[int, int, int]) -> str:
    return "".join(
        str(sum(coefficients[i] * int(rows[i][j]) for i in range(3)) % 3)
        for j in range(6)
    )


def dual_charge(rows: tuple[str, str, str]) -> tuple[int, int, int]:
    return tuple(sum(int(value) for value in transform(row, A_W)) % 3 for row in rows)  # type: ignore[return-value]


def visible_charge(rows: tuple[str, str, str]) -> tuple[int, int, int]:
    return tuple(sum(int(value) for value in row) % 3 for row in rows)  # type: ignore[return-value]


def comparison_coefficients(
    charge: tuple[int, int, int], phase: int, offset: int, orientation: int
) -> tuple[int, int, int]:
    """Orientación por coincidencia fase--carga, con traslación de fase."""
    selected = (phase + offset) % 3
    return tuple(
        orientation * (1 if value == selected else -1) % 3 for value in charge
    )  # type: ignore[return-value]


def read_n69() -> list[dict[str, str]]:
    with N69.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 100, "N69 ya no contiene cien fronteras")
    return rows


def phase_character_audit(rows: list[dict[str, str]]) -> dict[str, object]:
    coverage: dict[str, set[int]] = {"visible": set(), "Witt-dual": set()}
    hits: list[dict[str, object]] = []

    for row in rows:
        bands = tuple(row["B"].split("|"))
        require(len(bands) == 3, "frontera N69 mal formada")
        bands = (bands[0], bands[1], bands[2])
        phase = (int(row["t"]) - 1) % 3
        charges = {
            "visible": visible_charge(bands),
            "Witt-dual": dual_charge(bands),
        }
        require("".join(map(str, charges["visible"])) == row["r"].zfill(3),
                "carga visible N69 inconsistente")
        require("".join(map(str, charges["Witt-dual"])) == row["dual"].zfill(3),
                "carga Witt-dual N69 inconsistente")

        for charge_name, charge in charges.items():
            for offset in range(3):
                for orientation in (1, -1):
                    coefficients = comparison_coefficients(charge, phase, offset, orientation)
                    output = linear_word(bands, coefficients)
                    if output in W72_BLOCKS:
                        position = W72_BLOCKS.index(output) + 1
                        coverage[charge_name].add(position)
                        hits.append({
                            "t": int(row["t"]),
                            "charge": charge_name,
                            "phase_offset": offset,
                            "orientation": orientation,
                            "coefficients": list(coefficients),
                            "output": output,
                            "position_W72": position,
                        })

    union = coverage["visible"] | coverage["Witt-dual"]
    require(coverage["Witt-dual"] == {4, 5, 6, 7, 9, 11, 12},
            "cobertura Witt-dual inesperada")
    require(coverage["visible"] == {5, 6, 7, 8, 12},
            "cobertura visible inesperada")
    require(union == {4, 5, 6, 7, 8, 9, 11, 12},
            "unión de caracteres fase--carga inesperada")
    require(10 not in union, "el lector local produjo inesperadamente el bloque décimo")

    # El único bloque ausente del sufijo W5,...,W12 tiene una realización
    # afín simple en t=30: coeficientes rho_W + fase.
    row30 = next(row for row in rows if int(row["t"]) == 30)
    bands30_raw = tuple(row30["B"].split("|"))
    bands30 = (bands30_raw[0], bands30_raw[1], bands30_raw[2])
    rho30 = dual_charge(bands30)
    phase30 = (30 - 1) % 3
    affine_coefficients = tuple((value + phase30) % 3 for value in rho30)
    affine_output = linear_word(bands30, affine_coefficients)  # type: ignore[arg-type]
    require(rho30 == (0, 1, 2), "carga dual t=30 alterada")
    require(phase30 == 2 and affine_coefficients == (2, 0, 1),
            "carácter afín t=30 alterado")
    require(affine_output == W72_BLOCKS[9] == "001001",
            "el carácter afín ya no produce el bloque décimo")

    return {
        "family": (
            "c_i = epsilon if charge_i = phase+delta; c_i = -epsilon otherwise, "
            "charge in {visible, Witt-dual}, delta in F3, epsilon in {+1,-1}"
        ),
        "Witt_dual_coverage_positions": sorted(coverage["Witt-dual"]),
        "visible_coverage_positions": sorted(coverage["visible"]),
        "union_coverage_positions": sorted(union),
        "missing_suffix_position_before_affine_extension": 10,
        "hits": sorted(hits, key=lambda item: (
            int(item["position_W72"]), int(item["t"]), str(item["charge"]),
            int(item["phase_offset"]), int(item["orientation"])
        )),
        "affine_extension": {
            "t": 30,
            "charge": "Witt-dual",
            "formula": "c_i = rho_W,i + phase (mod 3)",
            "rho_W": list(rho30),
            "phase": phase30,
            "coefficients": list(affine_coefficients),
            "output": affine_output,
            "position_W72": 10,
        },
        "exact_conclusion": (
            "la familia local de comparación no puede prolongar W24 a W72, porque "
            "001001 no pertenece a su imagen; un único carácter afín rompe la "
            "obstrucción de cobertura, pero no suministra por sí solo el orden de "
            "los ocho bloques del sufijo"
        ),
    }


def cylinder_roots() -> tuple[int, int, int]:
    numerator = int(W24, 3)
    denominator = 3 ** len(W24)
    forced: list[int] = []
    for depth in range(1, 13):
        scale = 1000 ** depth
        lower = numerator * scale // denominator
        upper = ((numerator + 1) * scale - 1) // denominator
        if lower != upper:
            break
        rendered = f"{lower:0{3 * depth}d}"
        forced = [int(rendered[3 * index:3 * index + 3]) for index in range(depth)]
    require(forced == [234, 543, 140], "W24 ya no fija las tres raíces esperadas")
    return forced[0], forced[1], forced[2]


def reconstruct_from_forest(
    roots: tuple[int, int, int], edge_data: Iterable[int]
) -> tuple[int, ...]:
    values: list[int | None] = [None] * 12
    for index, value in zip(ROOTS, roots):
        values[index] = value
    data = tuple(edge_data)
    require(len(data) == len(FOREST), "se esperaban nueve diferencias de bosque")
    for (source, target, _step), difference in zip(FOREST, data):
        require(values[source] is not None, "orden no topológico del bosque")
        require(values[target] is None, "el bosque contiene un ciclo")
        values[target] = int(values[source]) - difference  # type: ignore[arg-type]
    require(all(value is not None for value in values), "el bosque no cubre los doce sectores")
    return tuple(int(value) for value in values)


def rank_q(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    work = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        divisor = work[rank][column]
        work[rank] = [value / divisor for value in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][column]:
                factor = work[row][column]
                work[row] = [a - factor * b for a, b in zip(work[row], work[rank])]
        rank += 1
    return rank


def determinant_bareiss(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for pivot_index in range(len(work) - 1):
        pivot_row = next(
            (row for row in range(pivot_index, len(work)) if work[row][pivot_index]),
            None,
        )
        require(pivot_row is not None, "matriz singular en Bareiss")
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = work[pivot_row], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, len(work)):
            for column in range(pivot_index + 1, len(work)):
                work[row][column] = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                ) // previous
        previous = pivot
    return sign * work[-1][-1]


def coordinate_matrix() -> list[list[int]]:
    matrix: list[list[int]] = []
    for root in ROOTS:
        row = [0] * 12
        row[root] = 1
        matrix.append(row)
    for source, target, _step in FOREST:
        row = [0] * 12
        row[source] = 1
        row[target] = -1
        matrix.append(row)
    return matrix


def k_to_u(k: tuple[int, ...]) -> tuple[int, ...]:
    output = [0] * 12
    for residue in range(3):
        block = [k[residue + 3 * index] for index in range(4)]
        transformed = [sum(row[index] * block[index] for index in range(4)) for row in H4]
        for index, value in enumerate(transformed):
            output[residue + 3 * index] = value
    return tuple(output)


def minimal_interface_audit(current: dict[str, object]) -> dict[str, object]:
    roots = cylinder_roots()
    matrix = coordinate_matrix()
    forest_matrix = matrix[3:]
    determinant = determinant_bareiss(matrix)
    require(rank_q(forest_matrix) == 9, "el bosque no tiene rango nueve")
    require(determinant == -1, "la carta raíz--bosque dejó de ser unimodular")

    reconstructed = reconstruct_from_forest(roots, CANONICAL_EDGE_DATA)
    expected_k = tuple(current["state_types"]["CanonicalSealK"]["coordinates"])  # type: ignore[index]
    expected_u = tuple(current["state_types"]["SignedDodecaphaseState"]["coordinates"])  # type: ignore[index]
    require(reconstructed == expected_k, "la interfaz mínima no reconstruye el sello canónico")
    require(k_to_u(reconstructed) == expected_u, "H4 no reconstruye U12 firmado")

    # Prueba independiente de la fórmula sobre 250 vectores enteros.
    state = 0x5A17
    for _ in range(250):
        vector: list[int] = []
        for _coordinate in range(12):
            state = (1103515245 * state + 12345) % (2 ** 31)
            vector.append(state % 4001 - 2000)
        roots_test = tuple(vector[index] for index in ROOTS)
        differences = tuple(vector[source] - vector[target] for source, target, _ in FOREST)
        require(reconstruct_from_forest(roots_test, differences) == tuple(vector),
                "falló una prueba general de reconstrucción")

    return {
        "W24": W24,
        "forced_base1000_roots": list(roots),
        "forest": [
            {"source": source + 1, "target": target + 1, "step": step,
             "difference": difference}
            for (source, target, step), difference in zip(FOREST, CANONICAL_EDGE_DATA)
        ],
        "rank_of_nine_edge_differences": 9,
        "determinant_roots_plus_edges": determinant,
        "unimodular": True,
        "reconstructed_K": list(reconstructed),
        "reconstructed_U12_signed": list(k_to_u(reconstructed)),
        "general_integer_tests": 250,
        "minimality": (
            "fijadas K1,K2,K3, el espacio afín restante tiene dimensión 9; "
            "menos de nueve observables lineales escalares no pueden ser inyectivos. "
            "Las nueve diferencias del bosque alcanzan ese mínimo y, junto con las "
            "raíces, forman una carta integral unimodular"
        ),
        "missing_map": (
            "estado TPK enriquecido -> nueve cociclos orientados del bosque. "
            "R36 y los caracteres fase--carga locales no contienen todavía esa "
            "aplicación; D3/D4 la contienen sólo como carta posterior del sello"
        ),
    }


def build_result() -> dict[str, object]:
    current = json.loads(CURRENT.read_text(encoding="utf-8"))
    require(current["revision"] == "2026-07-22.2", "revisión canónica inesperada")
    n69_rows = read_n69()
    phase_audit = phase_character_audit(n69_rows)
    interface = minimal_interface_audit(current)
    return {
        "schema": "HMT.W24-W72.phase-obstruction-minimal-interface.v1",
        "authority_revision": current["revision"],
        "status": "PASS_EXACT_NO_GO_AND_MINIMAL_INTERFACE",
        "phase_charge_reader": phase_audit,
        "minimal_dodecaphase_interface": interface,
        "proof_strength": {
            "phase_reader_no_go": "EXACTO_INTERNO para la familia declarada y las cien fronteras N69",
            "affine_t30": "EXACTO_INTERNO como incidencia; no es una ordenación global",
            "forest_reconstruction": "EXACTO_INTERNO y general sobre Z^12",
            "canonical_evaluation": "RELATIVO_A_PRIMITIVAS: usa las nueve diferencias publicadas",
            "global_generator": "no declarado: falta producir esas nueve diferencias desde el estado enriquecido",
        },
        "source_sha256": {
            str(CURRENT.relative_to(PROJECT)): file_sha256(CURRENT),
            str(N69.relative_to(PROJECT)): file_sha256(N69),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-certificate", action="store_true")
    args = parser.parse_args()
    result = build_result()
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.check_certificate:
        require(OUT.exists(), "no existe el certificado congelado")
        require(OUT.read_text(encoding="utf-8") == rendered, "el certificado no coincide")
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(result["status"])


if __name__ == "__main__":
    main()
