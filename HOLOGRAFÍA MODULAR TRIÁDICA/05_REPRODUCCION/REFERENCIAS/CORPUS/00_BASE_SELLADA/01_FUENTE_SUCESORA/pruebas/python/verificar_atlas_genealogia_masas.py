#!/usr/bin/env python3
"""Verifica el atlas de especies y tipa la genealogía de las masas.

Este verificador usa únicamente la biblioteca estándar. No promueve una
lectura física candidata a extractor forward: certifica por separado el
atlas finito, las firmas calibradas, la cuantización residual y la
decodificación inversa acotada.
"""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ATLAS = ROOT / "datos" / "atlas_especies_81_celdas_v11_rescate_tipado.csv"
SIGNATURES = ROOT / "datos" / "firmas_enteras_diez_especies.csv"
STAGES = ROOT / "datos" / "tabla_etapas_caracter_masa.csv"
INVERSE = ROOT / "datos" / "decodificacion_inversa_12_especies.csv"
OUTPUT = ROOT / "certificados" / "atlas_genealogia_masas.json"

COORDINATES = ("nA", "sC", "k_D4", "nu120", "nu270")
RAW_COORDINATES = ("nA", "sC", "kD4", "nu120", "nu270")
SIGMA12 = (1, 1, 1, -1, -1, -1, 1, 1, 1, -1, -1, -1)
CYCLES = ((0, 4, 8), (1, 5, 9), (2, 6, 10), (3, 7, 11))

A_DEG = 7.297352569283802
CSTAR_DEG = 2.123738338968646
ME_EXTERNAL = 0.51099895
ME_INTERNAL = 0.51099892248806607250987087719134943763
ME_CODATA_2022 = 0.51099895069
EXPECTED_ATLAS_SHA256 = (
    "cac4f566c41b46781d6846348bb3a0ddc12edd709ed0336a4dd8d282dabf5b83"
)


class VerificationError(RuntimeError):
    """Fallo tipado de una condición matemática o de integridad."""

    def __init__(self, code: str, details: Any = None) -> None:
        self.code = code
        self.details = details
        super().__init__(code)


def require(condition: bool, code: str, details: Any = None) -> None:
    if not condition:
        raise VerificationError(code, details)


def read_csv(path: Path) -> list[dict[str, str]]:
    require(path.is_file(), "MISSING_INPUT", str(path))
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def determinant(matrix: list[list[int]]) -> int:
    """Determinante exacto mediante eliminación de Bareiss."""
    n = len(matrix)
    require(all(len(row) == n for row in matrix), "NON_SQUARE_MATRIX")
    if n == 0:
        return 1
    work = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for pivot_index in range(n - 1):
        pivot_row = next(
            (row for row in range(pivot_index, n) if work[row][pivot_index]),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = work[pivot_row], work[pivot_index]
            sign = -sign
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, n):
            for column in range(pivot_index + 1, n):
                numerator = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                )
                require(
                    numerator % previous == 0,
                    "BAREISS_NONEXACT_DIVISION",
                    {"numerator": numerator, "denominator": previous},
                )
                work[row][column] = numerator // previous
            work[row][pivot_index] = 0
        previous = pivot
    return sign * work[-1][-1]


def smith_diagonal(generators: list[tuple[int, ...]]) -> list[int]:
    """Factores invariantes mediante divisores determinantales."""
    require(bool(generators), "EMPTY_GENERATOR_SET")
    column_count = len(generators[0])
    require(
        all(len(row) == column_count for row in generators),
        "INCONSISTENT_GENERATOR_WIDTH",
    )
    deltas = [1]
    for order in range(1, column_count + 1):
        divisor = 0
        for row_indices in itertools.combinations(range(len(generators)), order):
            for column_indices in itertools.combinations(range(column_count), order):
                minor = [
                    [generators[row][column] for column in column_indices]
                    for row in row_indices
                ]
                divisor = math.gcd(divisor, abs(determinant(minor)))
                if divisor == 1:
                    break
            if divisor == 1:
                break
        require(divisor != 0, "GENERATOR_RANK_DEFICIENT", {"order": order})
        deltas.append(divisor)
    diagonal = [
        deltas[index] // deltas[index - 1]
        for index in range(1, len(deltas))
    ]
    require(
        all(
            diagonal[index + 1] % diagonal[index] == 0
            for index in range(len(diagonal) - 1)
        ),
        "INVALID_SMITH_DIVISIBILITY",
        diagonal,
    )
    return diagonal


def belongs_to_basis(vector: tuple[int, ...], basis: list[tuple[int, ...]]) -> bool:
    """Pertenencia exacta al retículo fila por la regla de Cramer."""
    det_basis = determinant([list(row) for row in basis])
    require(det_basis != 0, "SINGULAR_LATTICE_BASIS")
    for index in range(len(basis)):
        replaced = [list(row) for row in basis]
        replaced[index] = list(vector)
        if determinant(replaced) % det_basis != 0:
            return False
    return True


def raw_vector(row: dict[str, str]) -> tuple[int, ...]:
    return tuple(int(row[column]) for column in RAW_COORDINATES)


def mass_vector(row: dict[str, str]) -> tuple[int, ...]:
    return tuple(int(row[column]) for column in COORDINATES)


def verify_atlas() -> tuple[dict[str, Any], list[dict[str, str]]]:
    rows = read_csv(ATLAS)
    require(sha256(ATLAS) == EXPECTED_ATLAS_SHA256, "ATLAS_COPY_HASH_MISMATCH")
    require(len(rows) == 81, "ATLAS_CELL_COUNT", len(rows))
    by_cell = {(int(row["r"]), int(row["c"])): row for row in rows}
    require(len(by_cell) == 81, "ATLAS_DUPLICATE_CELL")
    require(
        set(by_cell) == {(r, c) for r in range(1, 10) for c in range(1, 10)},
        "ATLAS_NOT_FULL_I9_SQUARE",
    )
    require(
        sorted(int(row["cell_id"]) for row in rows) == list(range(1, 82)),
        "ATLAS_CELL_ID_RANGE",
    )

    sector_counts = Counter(row["sector"] for row in rows)
    family_counts = Counter(row["family"] for row in rows)
    expected_sectors = {"lepton": 45, "quark": 36}
    expected_families = {
        "charged_lepton": 25,
        "neutrino": 20,
        "quark_down": 20,
        "quark_up": 16,
    }
    require(dict(sector_counts) == expected_sectors, "ATLAS_SECTOR_COUNTS", sector_counts)
    require(dict(family_counts) == expected_families, "ATLAS_FAMILY_COUNTS", family_counts)

    generation_profiles: dict[str, Counter[int]] = {}
    for family in expected_families:
        generation_profiles[family] = Counter(
            int(row["generation"]) for row in rows if row["family"] == family
        )
    expected_profiles = {
        "charged_lepton": Counter({0: 1, 2: 8, 4: 16}),
        "neutrino": Counter({1: 2, 2: 4, 3: 6, 4: 8}),
        "quark_down": Counter({1: 2, 2: 4, 3: 6, 4: 8}),
        "quark_up": Counter({1: 4, 3: 12}),
    }
    require(generation_profiles == expected_profiles, "ATLAS_GENERATION_PROFILES")

    center = by_cell[(5, 5)]
    require(center["HMT_species_label"] == "e_core[5,5]", "ATLAS_CENTER_LABEL")
    require(center["generation_label"] == "G0_center", "ATLAS_CENTER_GENERATION")

    color_rule = {0: "R", 1: "G", 2: "B"}
    conjugate_color = {"R": "R", "G": "B", "B": "G"}
    color_counts: Counter[str] = Counter()
    for (r, c), row in by_cell.items():
        partner = by_cell[(10 - r, 10 - c)]
        require(int(row["rho_r"]) == 10 - r, "ATLAS_RHO_R", (r, c))
        require(int(row["rho_c"]) == 10 - c, "ATLAS_RHO_C", (r, c))
        require(row["rho_family"] == partner["family"], "ATLAS_RHO_FAMILY", (r, c))
        require(
            int(row["rho_generation"]) == int(partner["generation"]),
            "ATLAS_RHO_GENERATION",
            (r, c),
        )
        require(row["family"] == partner["family"], "ATLAS_FAMILY_NOT_RHO_INVARIANT", (r, c))
        require(
            row["generation"] == partner["generation"],
            "ATLAS_GENERATION_NOT_RHO_INVARIANT",
            (r, c),
        )
        if row["sector"] == "quark":
            color = color_rule[(r - c) % 3]
            require(row["color_r_minus_c"] == color, "ATLAS_COLOR_RULE", (r, c))
            require(
                partner["color_r_minus_c"] == conjugate_color[color],
                "ATLAS_COLOR_CONJUGATION",
                (r, c),
            )
            require(
                row["rho_color_r_minus_c"] == partner["color_r_minus_c"],
                "ATLAS_RHO_COLOR_FIELD",
                (r, c),
            )
            color_counts[color] += 1
    require(dict(color_counts) == {"G": 12, "R": 12, "B": 12}, "ATLAS_COLOR_COUNTS")

    vectors = [raw_vector(row) for row in rows]
    vector_set = set(vectors)
    basis_raw_ids = (22, 23, 39, 56, 57)
    basis_raw = [vectors[index - 1] for index in basis_raw_ids]
    require(abs(determinant([list(row) for row in basis_raw])) == 192, "RAW_BASIS_INDEX")
    require(all(belongs_to_basis(vector, basis_raw) for vector in vectors), "RAW_BASIS_NOT_GENERATING")
    raw_smith = smith_diagonal(basis_raw)
    require(raw_smith == [2, 2, 2, 2, 12], "RAW_SMITH", raw_smith)

    center_vector = raw_vector(center)
    centered = [tuple(a - b for a, b in zip(vector, center_vector)) for vector in vectors]
    basis_centered_ids = (13, 14, 37, 54, 74)
    basis_centered = [centered[index - 1] for index in basis_centered_ids]
    require(
        abs(determinant([list(row) for row in basis_centered])) == 192,
        "CENTERED_BASIS_INDEX",
    )
    require(
        all(belongs_to_basis(vector, basis_centered) for vector in centered),
        "CENTERED_BASIS_NOT_GENERATING",
    )
    centered_smith = smith_diagonal(basis_centered)
    require(centered_smith == [2, 2, 2, 2, 12], "CENTERED_SMITH", centered_smith)

    return {
        "status": "VERIFIED_FINITE_ATLAS_NOT_PHYSICAL_SELECTOR",
        "cells": len(rows),
        "rho_orbits": sum(1 for r, c in by_cell if (r, c) <= (10 - r, 10 - c)),
        "center": {"r": 5, "c": 5, "label": center["HMT_species_label"]},
        "sector_counts": dict(sorted(sector_counts.items())),
        "family_counts": dict(sorted(family_counts.items())),
        "generation_profiles": {
            family: dict(sorted(profile.items()))
            for family, profile in sorted(generation_profiles.items())
        },
        "quark_color_counts": dict(sorted(color_counts.items())),
        "raw_signature_vectors": len(vector_set),
        "raw_lattice_smith_diagonal": raw_smith,
        "raw_centered_lattice_smith_diagonal": centered_smith,
        "raw_basis_cell_ids": list(basis_raw_ids),
        "centered_basis_cell_ids": list(basis_centered_ids),
        "epistemic_role": "COARSE_CELL_ATLAS_AND_RAW_ROUTE_SIGNATURES",
    }, rows


def sign(value: int) -> int:
    return (value > 0) - (value < 0)


def dr9(value: int) -> int:
    residue = value % 9
    return 9 if residue == 0 else residue


def unifilar_digits(seed_r: int, seed_c: int, h0: int, v0: int) -> tuple[int, ...]:
    r, c, h, v = seed_r, seed_c, h0, v0
    digits: list[int] = []
    for tick in range(1, 109):
        rho = 1 + (tick - 1) % 9
        if rho in (1, 4, 7):
            digit = dr9(r + c)
            c = 1 + (c - 1 + h) % 9
        elif rho in (2, 5, 8):
            digit = dr9(r * c)
            r = 1 + (r - 1 + v) % 9
        else:
            digit = 9
        if tick % 27 == 0 and tick < 108:
            h, v = -h, -v
        digits.append(digit)
    return tuple(digits)


def unifilar_observable(digits: tuple[int, ...]) -> tuple[int, ...]:
    odds = {1, 3, 5, 7}
    evens = {2, 4, 6, 8}
    n_a = sum(digit in odds for digit in digits)
    s_c = sum(
        1 if (tick - 1) // 27 in (0, 2) else -1
        for tick, digit in enumerate(digits, 1)
        if digit in evens
    )
    block_values = tuple(
        SIGMA12[block]
        * sum(digit in evens for digit in digits[9 * block : 9 * (block + 1)])
        for block in range(12)
    )
    tau = tuple(sign(value) for value in block_values)
    k_d4 = sum(SIGMA12[block] for block in range(12) if tau[block] == 0)
    nu120 = sum(
        sign(sum(block_values[index] for index in cycle)) for cycle in CYCLES
    )
    nu270 = sum(tau[block] * tau[(block + 3) % 12] for block in range(12))
    return n_a, s_c, k_d4, nu120, nu270


def verify_signatures_and_obstructions(
    atlas_rows: list[dict[str, str]],
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    rows = read_csv(SIGNATURES)
    require(len(rows) == 10, "CALIBRATED_SIGNATURE_COUNT", len(rows))
    expected_species = (
        "mu", "pi0", "pi_plus", "K_plus", "K0", "p", "n", "tau", "W", "Z"
    )
    require(tuple(row["species"] for row in rows) == expected_species, "SIGNATURE_SPECIES_ORDER")
    vectors = [mass_vector(row) for row in rows]
    require(len(set(vectors)) == 10, "DUPLICATE_CALIBRATED_SIGNATURE")

    raw_image = {raw_vector(row) for row in atlas_rows}
    raw_matches = [
        row["species"] for row, vector in zip(rows, vectors) if vector in raw_image
    ]
    require(raw_matches == [], "RAW_ATLAS_DIRECT_MATCH", raw_matches)

    unifilar_rows = []
    for r in range(1, 10):
        for c in range(1, 10):
            for h in (-1, 1):
                for v in (-1, 1):
                    unifilar_rows.append(unifilar_observable(unifilar_digits(r, c, h, v)))
    require(len(unifilar_rows) == 324, "UNIFILAR_INITIAL_CONDITIONS")
    unifilar_image = set(unifilar_rows)
    require(len(unifilar_image) == 53, "UNIFILAR_IMAGE_SIZE", len(unifilar_image))
    unifilar_matches = [
        row["species"] for row, vector in zip(rows, vectors) if vector in unifilar_image
    ]
    require(unifilar_matches == [], "UNIFILAR_DIRECT_MATCH", unifilar_matches)

    base = vectors[0]
    differences = [
        tuple(value - origin for value, origin in zip(vector, base))
        for vector in vectors[1:]
    ]
    mass_smith = smith_diagonal(differences)
    require(mass_smith == [1, 1, 1, 1, 2], "MASS_DIFFERENCE_SMITH", mass_smith)
    electron_edges_smith = smith_diagonal(vectors)
    require(
        electron_edges_smith == [1, 1, 1, 1, 1],
        "ELECTRON_EDGE_SMITH",
        electron_edges_smith,
    )
    parities = [(vector[1] + vector[3]) % 2 for vector in vectors]
    require(parities == [1] * 10, "NON_ELECTRON_PARITY", parities)

    electron_values = {float(row["m_e_HMT_MeV"]) for row in rows}
    require(len(electron_values) == 1, "INCONSISTENT_INTERNAL_ELECTRON_SCALE")
    electron_value = electron_values.pop()
    require(
        math.isclose(electron_value, ME_INTERNAL, rel_tol=0.0, abs_tol=1e-15),
        "INTERNAL_ELECTRON_VALUE",
        electron_value,
    )
    electron_delta = electron_value - ME_CODATA_2022

    return {
        "status": "CONDITIONAL_EXACT_EVALUATION_WITH_FORWARD_OBSTRUCTION",
        "calibrated_species": list(expected_species),
        "calibrated_signatures": {
            row["species"]: list(vector) for row, vector in zip(rows, vectors)
        },
        "raw_atlas_exact_matches": raw_matches,
        "unifilar_initial_conditions": len(unifilar_rows),
        "unifilar_signature_vectors": len(unifilar_image),
        "unifilar_exact_matches": unifilar_matches,
        "factorization_result": "NO_FACTORIZATION_FOR_CURRENT_RAW_OR_UNIFILAR_MAPS_0_OF_10",
        "mass_difference_smith_diagonal": mass_smith,
        "electron_edge_smith_diagonal": electron_edges_smith,
        "all_non_electron_parity": 1,
        "electron_internal_value": electron_value,
        "electron_minus_CODATA_2022_MeV": electron_delta,
        "electron_relative_difference_CODATA_2022": electron_delta / ME_CODATA_2022,
        "signature_table_role": "CALIBRATED_ASSIGNMENT_NOT_FORWARD_EXTRACTOR",
    }, rows


def rms(values: list[float]) -> float:
    require(bool(values), "EMPTY_RMS_INPUT")
    return math.sqrt(sum(value * value for value in values) / len(values))


def verify_stages(signature_rows: list[dict[str, str]]) -> dict[str, Any]:
    rows = read_csv(STAGES)
    require(len(rows) == 10, "MASS_STAGE_ROW_COUNT", len(rows))
    require(
        [row["species"] for row in rows] == [row["species"] for row in signature_rows],
        "MASS_STAGE_SPECIES_ORDER",
    )
    rms_values = [
        rms([float(row[f"rel{stage}_HMTscale_calibration"]) for row in rows])
        for stage in range(5)
    ]
    expected_rms = (
        2.224237203948622e-3,
        2.762046114809764e-5,
        4.777221368999134e-6,
        4.795312133659499e-7,
        2.2292793901731056e-8,
    )
    require(
        all(
            math.isclose(value, expected, rel_tol=2e-13, abs_tol=1e-18)
            for value, expected in zip(rms_values, expected_rms)
        ),
        "MASS_STAGE_RMS",
        rms_values,
    )
    alpha = 1.0 / 137.035999084
    a_rad = math.radians(1000.0 * alpha)
    cstar_rad = math.radians(CSTAR_DEG)
    delta4 = (math.pi - math.e * math.log(math.pi)) / 270.0 * (1.0 + math.pi / 729.0)
    q_plus = math.exp(-a_rad - cstar_rad)
    q_minus = math.exp(-a_rad + cstar_rad)
    s120 = q_minus**120 - q_plus**120
    zeta270 = 135.0 * delta4**2
    s180 = q_minus**180 - q_plus**180
    s180_values = []
    inferred = []
    declared = []
    for row in rows:
        m3 = float(row["m3_HMTscale_MeV"])
        m4 = float(row["m4_HMTscale_MeV"])
        n180 = int(row["nu180_audit"])
        if n180 != 0:
            s180_values.append(math.log(m4 / m3) / n180)
        reference = float(row["m_ref_calibration_MeV"])
        exponent3 = (
            int(row["nA"]) * a_rad
            + int(row["sC"]) * cstar_rad / 6.0
            + int(row["k_Delta4"]) * delta4
            + int(row["nu120"]) * s120
            + int(row["nu270_corr"]) * zeta270
        )
        inferred.append(round(math.log(reference / (ME_INTERNAL * math.exp(exponent3))) / s180))
        declared.append(n180)
    require(max(s180_values) - min(s180_values) < 5e-16, "NON_GLOBAL_S180")
    expected_nu180 = [2, 7, -7, -1, -4, 5, -4, -5, 6, 9]
    require(declared == expected_nu180, "NU180_DECLARED_VECTOR", declared)
    require(inferred == expected_nu180, "NU180_NOT_INVERSE_RESIDUAL", inferred)
    s180_global = math.fsum(s180_values) / len(s180_values)
    require(
        s180_global.hex() == "0x1.7725cd3f7236fp-24",
        "S180_GLOBAL_BINARY64_DRIFT",
        {"decimal": s180_global, "hex": s180_global.hex()},
    )
    return {
        "status": "E0_E3_CONDITIONAL_E4_INVERSE_RESIDUAL_QUANTIZATION",
        "rms_relative_internal_scale": {
            f"E{stage}": value for stage, value in enumerate(rms_values)
        },
        "nu180": declared,
        "nu180_typing": "INVERSE_RESIDUAL_QUANTIZATION_FROM_REFERENCE_MASSES",
        # ``sum`` acumulaba un último bit distinto entre CPython 3.9 y 3.12
        # aunque los diez sumandos fueran byte a byte los mismos.  ``fsum``
        # realiza una suma compensada y correctamente redondeada, de modo que
        # el certificado expresa el mismo promedio matemático en ambos
        # runtimes.
        "s180_global_reconstructed": s180_global,
    }


def verify_inverse_decoder() -> dict[str, Any]:
    rows = read_csv(INVERSE)
    require(len(rows) == 12, "INVERSE_DECODER_ROW_COUNT", len(rows))
    require(
        all(row["epistemic_role"] == "INVERSE_TARGET_DEPENDENT" for row in rows),
        "INVERSE_DECODER_ROLE",
    )
    a_rad = A_DEG * math.pi / 180.0
    cstar_rad = CSTAR_DEG * math.pi / 180.0
    results: dict[str, Any] = {}
    for row in rows:
        species = row["species"]
        declared = (int(row["nA"]), int(row["sC"]))
        reference = float(row["reference_MeV"])
        target_log = math.log(reference / ME_EXTERNAL)
        candidates = sorted(
            (
                abs(target_log - (n_a * a_rad + (s_c / 6.0) * cstar_rad)),
                n_a,
                s_c,
            )
            for n_a in range(121)
            for s_c in range(-12, 13)
        )
        best, second = candidates[0], candidates[1]
        require((best[1], best[2]) == declared, "INVERSE_DECODER_BEST_POINT", species)
        require(best[0] < second[0], "INVERSE_DECODER_NOT_UNIQUE", species)
        recomputed_mass = ME_EXTERNAL * math.exp(
            declared[0] * a_rad + (declared[1] / 6.0) * cstar_rad
        )
        require(
            math.isclose(
                recomputed_mass,
                float(row["declared_mass_MeV"]),
                rel_tol=2e-15,
                abs_tol=2e-12,
            ),
            "INVERSE_DECODER_MASS_RECOMPUTATION",
            species,
        )
        results[species] = {
            "decoded_pair": list(declared),
            "target_MeV": reference,
            "mass_at_pair_MeV": recomputed_mass,
            "best_log_distance": best[0],
            "second_best_pair": [second[1], second[2]],
            "uniqueness_margin": second[0] - best[0],
        }
    return {
        "status": "UNIQUE_BOUNDED_VORONOI_DECODING_NOT_FORWARD_DERIVATION",
        "window": {"nA": [0, 120], "sC": [-12, 12]},
        "metric": "absolute_log_mass_residual",
        "electron_scale": {
            "value_MeV": ME_EXTERNAL,
            "role": "EXTERNAL_SCALE_USED_BY_HISTORICAL_TABLE",
        },
        "species": results,
    }


def build_result() -> dict[str, Any]:
    atlas_result, atlas_rows = verify_atlas()
    signature_result, signature_rows = verify_signatures_and_obstructions(atlas_rows)
    stages_result = verify_stages(signature_rows)
    inverse_result = verify_inverse_decoder()
    return {
        "status": "PASS_TYPED_ATLAS_AND_GENEALOGY_AUDIT",
        "verifier": "pruebas/python/verificar_atlas_genealogia_masas.py",
        "epistemic_contract": {
            "exact_finite_atlas": True,
            "candidate_physical_projection_is_forward_selector": False,
            "calibrated_signature_table_is_forward_extractor": False,
            "E4_is_prospective_prediction": False,
            "bounded_12_species_decoder_is_forward_derivation": False,
        },
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (ATLAS, SIGNATURES, STAGES, INVERSE)
        },
        "atlas": atlas_result,
        "signatures_and_forward_obstruction": signature_result,
        "mass_stages": stages_result,
        "inverse_decoder_12_species": inverse_result,
    }


def main() -> int:
    try:
        result = build_result()
    except VerificationError as exc:
        failure = {
            "status": "FAIL",
            "code": exc.code,
            "details": exc.details,
        }
        print(json.dumps(failure, sort_keys=True, indent=2), file=sys.stderr)
        return 1
    serialized = json.dumps(result, sort_keys=True, indent=2) + "\n"
    OUTPUT.write_text(serialized, encoding="utf-8")
    print(serialized, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
