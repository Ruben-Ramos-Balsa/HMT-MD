#!/usr/bin/env python3
"""Certifica el carácter fase--dual que prolonga el cilindro hasta K_3.

El cálculo separa estrictamente dos etapas. Primero construye, sin consultar
el sello K, una palabra de 24 trits a partir del rombo N72, el retorno N74 y
el carácter fase--dual de la rama superviviente inmediatamente anterior.
Después reconoce qué celda decimal fuerza ese cilindro y la compara con el
sello vigente. También ejecuta controles negativos sobre todas las ramas,
todos los caracteres lineales y la ventana N69 de cien estados.

Sólo usa la biblioteca estándar y no emplea aserciones desactivables.
"""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

CURRENT = ROOT / "03_PAPER/HMT_MACROPAPER_V3/CURRENT.json"
N72_DIR = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_N72_N75/HMT_N72_supervivencia_coinductiva_novena_puerta_v1"
)
N72_BRANCHES = N72_DIR / "N72_selected_branches_survival_details.csv"
N72_PROFILE = N72_DIR / "N72_coinductive_survival_profile_t5_t25_h9.csv"
N74_RETURN = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_N72_N75/HMT_N74_monodromia_nueve_puertas_v1/"
    "N74_monodromy_return_t_to_t_plus_9.csv"
)
N69_SIGNATURES = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_CADENA_VIGENTE/N69_CALENDARIO_TRANSICION/"
    "HMT_N69_ley_transicion_o_axioma_cilindrico_v1/"
    "N69_signatures_t0_t99.csv"
)
N33_INDEX = ROOT / (
    "06_NUEVOS_PAQUETES/HMT_N33_PI_E_PHI_CLOSEOUT_v3/"
    "HMT_N33_PI_PHI_E_CLOSEOUT/n33_w6_index.json"
)
HISTORICAL_ALPHA = ROOT / "01_ORIGINALES/2026-01/F004_3.0.alfa.txt"
ROMBO_CERTIFICATE = ROOT / (
    "16_CIERRE_GLOBAL_HMT_MD_2026-07-22/02_LECTURA_DODECAFASICA/"
    "rombo_nueve_fases/CERTIFICADO_ROMBO_NUEVE_FASES.json"
)
CERTIFICATE = HERE / "RESULTADO_CARACTER_FASE_DUAL.json"


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def split_rows(value: str) -> tuple[str, str, str]:
    rows = tuple(part.zfill(6) for part in value.split("|"))
    require(len(rows) == 3 and all(len(row) == 6 for row in rows), "terna mal tipada")
    return rows  # type: ignore[return-value]


def linear_word(rows: tuple[str, str, str], coefficients: tuple[int, int, int]) -> str:
    return "".join(
        str(sum(coefficients[i] * int(rows[i][j]) for i in range(3)) % 3)
        for j in range(6)
    )


def add_word(a: str, b: str) -> str:
    require(len(a) == len(b), "longitudes incompatibles")
    return "".join(str((int(x) + int(y)) % 3) for x, y in zip(a, b))


def subtract_word(a: str, b: str) -> str:
    require(len(a) == len(b), "longitudes incompatibles")
    return "".join(str((int(x) - int(y)) % 3) for x, y in zip(a, b))


def negative_word(value: str) -> str:
    return "".join(str((-int(digit)) % 3) for digit in value)


def aw_transform(value: str) -> str:
    vector = tuple(int(digit) for digit in value)
    return "".join(
        str(sum(vector[i] * A_W[i][j] for i in range(6)) % 3)
        for j in range(6)
    )


def dual_charge(rows: tuple[str, str, str]) -> tuple[int, int, int]:
    return tuple(sum(int(digit) for digit in aw_transform(row)) % 3 for row in rows)  # type: ignore[return-value]


def phase_dual_coefficients(rho: tuple[int, int, int], phase: int) -> tuple[int, int, int]:
    """+1 en la carga que coincide con la fase y -1 en su complemento."""
    phase %= 3
    return tuple(1 if charge == phase else 2 for charge in rho)  # type: ignore[return-value]


def determinant_mod3(matrix: list[list[int]]) -> int:
    a, b, c = matrix
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    ) % 3


def ternary_fraction_digits(numerator: int, denominator: int, length: int) -> str:
    require(0 <= numerator < denominator, "se esperaba una fracción propia")
    remainder = numerator
    output: list[str] = []
    for _ in range(length):
        remainder *= 3
        digit, remainder = divmod(remainder, denominator)
        require(digit in (0, 1, 2), "trit fuera de rango")
        output.append(str(digit))
    return "".join(output)


def cylinder_audit(word: str) -> dict[str, object]:
    require(word and set(word) <= {"0", "1", "2"}, "palabra ternaria inválida")
    numerator = int(word, 3)
    denominator = 3 ** len(word)
    depth = 0
    decimal_integer = 0
    for candidate_depth in range(1, 13):
        scale = 1000 ** candidate_depth
        lower = numerator * scale // denominator
        upper = ((numerator + 1) * scale - 1) // denominator
        if lower != upper:
            break
        depth = candidate_depth
        decimal_integer = lower
    result: dict[str, object] = {
        "word": word,
        "trits": len(word),
        "base3_integer": numerator,
        "denominator": denominator,
        "cylinder": [str(Fraction(numerator, denominator)), str(Fraction(numerator + 1, denominator))],
        "forced_decimal_triads": depth,
    }
    if depth:
        rendered = f"{decimal_integer:0{3 * depth}d}"
        blocks = [rendered[index:index + 3] for index in range(0, len(rendered), 3)]
        residual_lower = numerator * (1000 ** depth) - decimal_integer * denominator
        residual_upper = (numerator + 1) * (1000 ** depth) - decimal_integer * denominator
        result.update(
            {
                "forced_decimal_prefix": rendered,
                "forced_decimal_blocks": blocks,
                "residual_after_forced_blocks": [
                    str(Fraction(residual_lower, denominator)),
                    str(Fraction(residual_upper, denominator)),
                ],
                "possible_next_decimal_triads": list(
                    range(
                        residual_lower * 1000 // denominator,
                        (residual_upper * 1000 - 1) // denominator + 1,
                    )
                ),
            }
        )
    return result


def build_rombo_prefix() -> dict[str, object]:
    branches = read_csv(N72_BRANCHES)
    t20 = [row for row in branches if row["t"] == "20"]
    actual = split_rows(next(row["rows"] for row in t20 if row["is_actual"] == "True"))
    selected: list[tuple[dict[str, str], tuple[str, str, str], str, str]] = []
    for row in t20:
        if row["is_actual"] == "True":
            continue
        candidate = split_rows(row["rows"])
        delta_pi = subtract_word(candidate[0], actual[0])
        delta_e = subtract_word(candidate[1], actual[1])
        if (
            candidate[2] == actual[2]
            and add_word(candidate[0], candidate[1]) == add_word(actual[0], actual[1])
            and delta_pi == "000111"
            and delta_e == "000222"
        ):
            selected.append((row, candidate, delta_pi, delta_e))
    require(len(selected) == 1, "la rama especular saturada dejó de ser única")
    row, mirror, delta_pi, delta_e = selected[0]
    descriptor_12 = mirror[1] + delta_e[3:] + delta_pi[3:]

    returns = read_csv(N74_RETURN)
    return_row = next(item for item in returns if item["t"] == "11" and item["t_plus_9"] == "20")
    predecessor_sum = return_row["pi_plus_e_t"].zfill(6)
    descriptor_18 = descriptor_12 + predecessor_sum
    require(return_row["phase_K_mod9"] == "2", "la clase de retorno 11 -> 20 cambió")
    require(descriptor_12 == "020022222111", "descriptor del rombo alterado")
    require(predecessor_sum == "211201", "bloque del retorno alterado")

    previous = json.loads(ROMBO_CERTIFICATE.read_text(encoding="utf-8"))
    require(previous["K_recognition"]["retrospective_descriptor_18"] == descriptor_18,
            "el certificado previo y la reconstrucción ya no coinciden")
    return {
        "t20_actual": list(actual),
        "t20_saturated_mirror": list(mirror),
        "t20_mirror_index": int(row["idx"]),
        "oriented_defects": {"pi": delta_pi, "e": delta_e},
        "descriptor_12": descriptor_12,
        "same_phase_predecessor_t11": predecessor_sum,
        "descriptor_18": descriptor_18,
        "chronological_next_source": "la fase t=10 es el predecesor inmediato y único de t=11",
    }


def phase_dual_construction() -> dict[str, object]:
    profile = read_csv(N72_PROFILE)
    branches = read_csv(N72_BRANCHES)
    row10 = next(row for row in profile if row["t"] == "10")
    rows = split_rows(row10["actual_rows"])
    actual_branch = next(row for row in branches if row["t"] == "10" and row["is_actual"] == "True")
    require(actual_branch["rows"] == row10["actual_rows"], "perfil y ramas discrepan en t=10")
    require(rows == ("022212", "110001", "100021"), "terna superviviente t=10 alterada")
    require(row10["actual_idx"] == "10" and row10["survivors_h9"] == "1",
            "la selección coinductiva de t=10 dejó de ser única")

    rho = dual_charge(rows)
    phase = int(row10["t"]) % 3
    coefficients = phase_dual_coefficients(rho, phase)
    raw_word = linear_word(rows, coefficients)
    require(rho == (0, 1, 2), "la carga dual de t=10 alteró su carta")
    require(phase == 1 and coefficients == (2, 1, 2), "el carácter fase--dual alterado")
    require(raw_word == "021101", "la palabra fase--dual alterada")

    # Unicidad algebraica del coeficiente: las tres primeras columnas forman
    # un menor invertible, por lo que el mapa de coeficientes a palabras es inyectivo.
    minor = [[int(rows[i][j]) for j in range(3)] for i in range(3)]
    determinant = determinant_mod3(minor)
    require(determinant == 1, "el menor de rango tres dejó de ser invertible")
    matches = [
        coefficient
        for coefficient in itertools.product(range(3), repeat=3)
        if linear_word(rows, coefficient) == raw_word
    ]
    require(matches == [(2, 1, 2)], "el carácter no es único sobre la terna t=10")

    # Naturalidad: permutar simultáneamente canales, cargas y coeficientes no
    # cambia la palabra; renombrar afínmente las cargas conserva la igualdad.
    permutation_checks = 0
    for permutation in itertools.permutations(range(3)):
        permuted_rows = tuple(rows[index] for index in permutation)
        permuted_rho = tuple(rho[index] for index in permutation)
        permuted_coefficients = phase_dual_coefficients(permuted_rho, phase)
        require(linear_word(permuted_rows, permuted_coefficients) == raw_word,
                "falló la covariancia por permutación simultánea")
        permutation_checks += 1
    affine_label_checks = 0
    for scale in (1, 2):
        for translation in range(3):
            transformed_rho = tuple((scale * value + translation) % 3 for value in rho)
            transformed_phase = (scale * phase + translation) % 3
            require(phase_dual_coefficients(transformed_rho, transformed_phase) == coefficients,
                    "falló la naturalidad por renombrado afín")
            affine_label_checks += 1

    q = linear_word(rows, (1, 1, 1))
    a = linear_word(rows, (1, 1, 2))
    chi_e = linear_word(rows, (1, 2, 1))
    fourth_walsh = linear_word(rows, (1, 2, 2))
    sums = [sum(int(rows[i][j]) for i in range(3)) for j in range(6)]
    carry = "".join(str(value // 3) for value in sums)
    column_weight = "".join(str(sum(rows[i][j] != "0" for i in range(3))) for j in range(6))
    column_weight_mod3 = "".join(str(int(value) % 3) for value in column_weight)
    row_charge = "".join(str(sum(int(digit) for digit in row) % 3) for row in rows)
    published = {
        "pi": rows[0],
        "e": rows[1],
        "phi": rows[2],
        "q_pi_plus_e_plus_phi": q,
        "a_pi_plus_e_minus_phi": a,
        "carry": carry,
        "column_weight_mod3": column_weight_mod3,
        "row_charge": row_charge,
        "q_times_AW": aw_transform(q),
        "a_times_AW": aw_transform(a),
    }
    require(raw_word not in published.values(), "un observable publicado ya era la palabra cruda")

    n69 = next(row for row in read_csv(N69_SIGNATURES) if row["t"] == "11")
    require(split_rows(n69["B"]) == rows, "N69 t=11 no coincide con N72 t=10")
    require(
        (n69["q"], n69["a"], n69["c"], n69["colw_mod"], n69["dual"], n69["r"])
        == (q, a, carry, column_weight_mod3, "012", row_charge),
        "las firmas N69 no se reprodujeron desde la terna",
    )

    return {
        "source_phase_N72": 10,
        "corresponding_row_N69": 11,
        "surviving_rows_pi_e_phi": list(rows),
        "survival_h1_to_h9": [int(actual_branch[f"surv_h{i}"]) for i in range(1, 10)],
        "phase_mod3": phase,
        "witt_dual_charge_rhoW": list(rho),
        "definition": "epsilon_i=+1 si rhoW_i coincide con la fase; epsilon_i=-1 en caso contrario",
        "coefficients_F3_pi_e_phi": list(coefficients),
        "integer_notation": "-pi + e - phi",
        "raw_word": raw_word,
        "visible_word_under_Psi_equals_minus_raw": negative_word(raw_word),
        "rank_certificate": {
            "minor_columns_zero_one_two": minor,
            "determinant_mod3": determinant,
            "unique_coefficient_for_raw_word": list(matches[0]),
        },
        "naturality": {
            "simultaneous_channel_permutations_checked": permutation_checks,
            "affine_relabellings_of_F3_checked": affine_label_checks,
        },
        "walsh_H4_with_zero_vacancy": {
            "row_1": {"coefficients": [1, 1, 1], "word": q},
            "row_2": {"coefficients": [1, 1, 2], "word": a},
            "row_3_e_odd": {"coefficients": [1, 2, 1], "word": chi_e},
            "row_4": {"coefficients": [1, 2, 2], "word": fourth_walsh},
            "raw_word_relation": "021101 = -(012202), la orientación opuesta de la fila e-impar",
        },
        "published_frontier_observables": published,
        "uses_K_alpha_or_CODATA_for_selection": False,
        "canonicity_status": (
            "CANONICIDAD_RELATIVA_PROBADA: única bajo coincidencia fase--carga, "
            "signo orientado y naturalidad por renombrado; la adopción global del lector es una formalización nueva"
        ),
    }


def catalogue_bridge(raw_word: str) -> dict[str, object]:
    data = json.loads(N33_INDEX.read_text(encoding="utf-8"))
    visible = negative_word(raw_word)
    entry = data["words"][visible]
    require(visible == "012202", "proyección visible alterada")
    require(entry["num_U6_preimages"] == 1, "la palabra visible dejó de tener preimagen única")
    preimage = entry["canonical_preimage"]
    raw_residue = "".join(str(int(value) % 3) for value in preimage["U6"])
    require(raw_residue == raw_word, "la preimagen U6 no reproduce la palabra cruda")
    require(preimage["U6"] == [963, 890, 850, 292, 129, 292], "preimagen U6 alterada")
    require(preimage["multiplicity"] == 144, "multiplicidad alterada")

    historical_line = (
        "7,1,7,7,1,7\tB4-o2\t144\tB\t4\t2\t0,4\t0,5\t021101\t"
        "963|890|850|292|129|292"
    )
    require(historical_line in HISTORICAL_ALPHA.read_text(encoding="utf-8"),
            "el testigo histórico B4-o2 no fue localizado")
    return {
        "raw_U6_residue": raw_word,
        "visible_catalogue_word_Psi": visible,
        "Psi_rule": "Psi(U6)=-U6 mod 3",
        "unique_U6_preimage": preimage,
        "historical_classification": {
            "status": "RESULTADO_RECUPERADO_STALE_NO_NORMATIVO",
            "class": "B4-o2",
            "energy_signature": [7, 1, 7, 7, 1, 7],
        },
    }


def k_recognition(prefix_18: str, raw_word: str, current: dict[str, object]) -> dict[str, object]:
    candidate_24 = prefix_18 + raw_word
    cylinder = cylinder_audit(candidate_24)
    require(candidate_24 == "020022222111211201021101", "palabra de 24 trits alterada")
    require(cylinder["forced_decimal_triads"] == 3, "el cilindro no fuerza tres tríadas")
    require(cylinder["forced_decimal_blocks"] == ["234", "543", "140"],
            "las tres tríadas forzadas cambiaron")

    seal = current["state_types"]["CanonicalSealK"]["coordinates"]
    require(isinstance(seal, list) and len(seal) == 12, "sello vigente mal tipado")
    digits = "".join(f"{int(value):03d}" for value in seal)
    ternary = ternary_fraction_digits(int(digits), 10 ** len(digits), 72)
    blocks = [ternary[index:index + 6] for index in range(0, 72, 6)]
    require(candidate_24 == ternary[:24], "la construcción no coincide con el sello vigente")
    require([int(value) for value in cylinder["forced_decimal_blocks"]] == seal[:3],
            "el reconocimiento decimal no coincide con K1,K2,K3")

    d3 = [int(seal[i]) - int(seal[(i + 3) % 12]) for i in range(12)]
    d4 = [int(seal[i]) - int(seal[(i + 4) % 12]) for i in range(12)]
    return {
        "candidate_word_24_constructed_before_recognition": candidate_24,
        "exact_cylinder": cylinder,
        "recognized_K_prefix": [int(value) for value in seal[:3]],
        "matches_first_four_K_ternary_blocks": True,
        "K_ternary_blocks_for_later_ablations": blocks,
        "D3_D4_type_check": {
            "D3K": d3,
            "D4K": d4,
            "K3_affects_D3_positions_one_based": [3, 12],
            "K3_affects_D4_positions_one_based": [3, 11],
            "conclusion": (
                "D3 y D4 son cartas posteriores sobre K completo; usarlas para elegir 021101 "
                "sin un mapa de fase independiente introduciría el dato que se pretende construir"
            ),
        },
        "recognition_uses_K_only_after_candidate_is_fixed": True,
    }


def continuation_and_ablations(k_blocks: list[str]) -> dict[str, object]:
    profile = read_csv(N72_PROFILE)
    branches = read_csv(N72_BRANCHES)
    target_set = set(k_blocks)

    actual_outputs: list[dict[str, object]] = []
    actual_hits: list[dict[str, object]] = []
    for row in profile:
        rows = split_rows(row["actual_rows"])
        rho = dual_charge(rows)
        phase = int(row["t"]) % 3
        coefficients = phase_dual_coefficients(rho, phase)
        output = linear_word(rows, coefficients)
        hit_indices = [index + 1 for index, value in enumerate(k_blocks) if value == output]
        record = {
            "t": int(row["t"]),
            "phase": phase,
            "rhoW": "".join(str(value) for value in rho),
            "coefficients": "".join(str(value) for value in coefficients),
            "output": output,
            "K_block_hits": hit_indices,
        }
        actual_outputs.append(record)
        if hit_indices:
            actual_hits.append(record)
    require(len(actual_hits) == 1 and actual_hits[0]["t"] == 10
            and actual_hits[0]["K_block_hits"] == [4],
            "el lector congelado dejó de aislar K4 en la ventana actual")

    all_branch_hits: list[dict[str, object]] = []
    character_match_counts = [0] * 12
    for row in branches:
        rows = split_rows(row["rows"])
        phase = int(row["t"]) % 3
        rho = dual_charge(rows)
        output = linear_word(rows, phase_dual_coefficients(rho, phase))
        indices = [index + 1 for index, value in enumerate(k_blocks) if value == output]
        if indices:
            all_branch_hits.append(
                {
                    "t": int(row["t"]),
                    "branch_index": int(row["idx"]),
                    "is_actual": row["is_actual"] == "True",
                    "output": output,
                    "K_block_hits": indices,
                }
            )
        for coefficients in itertools.product(range(3), repeat=3):
            if coefficients == (0, 0, 0):
                continue
            word = linear_word(rows, coefficients)
            for index, target in enumerate(k_blocks):
                if word == target:
                    character_match_counts[index] += 1
    require(character_match_counts[9] == 0, "K10 apareció en la ventana N72 contra el control")

    fixed_character_coverages: list[dict[str, object]] = []
    for coefficients in itertools.product(range(3), repeat=3):
        if coefficients == (0, 0, 0):
            continue
        outputs = {
            linear_word(split_rows(row["actual_rows"]), coefficients)
            for row in profile
        }
        hits = sorted(index + 1 for index, target in enumerate(k_blocks) if target in outputs)
        fixed_character_coverages.append(
            {"coefficients": list(coefficients), "distinct_K_blocks": hits}
        )
    maximum_fixed_coverage = max(len(item["distinct_K_blocks"]) for item in fixed_character_coverages)
    require(maximum_fixed_coverage == 1, "un carácter lineal fijo cubrió más bloques de lo esperado")

    # N69 prolonga la ablación a cien estados. En el solapamiento, N69(t+1)
    # coincide con N72(t); por eso su fase física se lee como (t-1) mod 3.
    n69_rows = read_csv(N69_SIGNATURES)
    for row in profile:
        aligned = next(item for item in n69_rows if int(item["t"]) == int(row["t"]) + 1)
        require(split_rows(aligned["B"]) == split_rows(row["actual_rows"]),
                "falló el alineamiento N72(t) = N69(t+1)")

    n69_all_character_counts = [0] * 12
    n69_phase_dual_hits: list[dict[str, object]] = []
    for row in n69_rows:
        rows = split_rows(row["B"])
        for coefficients in itertools.product(range(3), repeat=3):
            if coefficients == (0, 0, 0):
                continue
            output = linear_word(rows, coefficients)
            for index, target in enumerate(k_blocks):
                if output == target:
                    n69_all_character_counts[index] += 1
        rho = tuple(int(value) for value in row["dual"].zfill(3))
        physical_phase = (int(row["t"]) - 1) % 3
        output = linear_word(rows, phase_dual_coefficients(rho, physical_phase))
        indices = [index + 1 for index, target in enumerate(k_blocks) if target == output]
        if indices:
            n69_phase_dual_hits.append(
                {"t_N69": int(row["t"]), "physical_phase": physical_phase,
                 "output": output, "K_block_hits": indices}
            )
    require(all(value > 0 for value in n69_all_character_counts),
            "la búsqueda libre N69 dejó de contener algún bloque de K")
    require(n69_phase_dual_hits == [
        {"t_N69": 11, "physical_phase": 1, "output": "021101", "K_block_hits": [4]},
        {"t_N69": 81, "physical_phase": 2, "output": "020111", "K_block_hits": [6]},
    ], "la ablación fase--dual N69 cambió")

    row10 = split_rows(next(row["actual_rows"] for row in profile if row["t"] == "10"))
    phase_offset_outputs = {
        str(offset): linear_word(row10, phase_dual_coefficients(dual_charge(row10), (1 + offset) % 3))
        for offset in (0, 1, 2)
    }
    require(phase_offset_outputs == {"0": "021101", "1": "001111", "2": "112220"},
            "ablación de fase alterada")

    return {
        "frozen_phase_dual_rule_on_all_actual_N72_rows": actual_outputs,
        "actual_hits_against_twelve_K_blocks": actual_hits,
        "all_N72_branch_hits": all_branch_hits,
        "all_linear_characters_on_all_N72_branches_match_counts_by_K_block": character_match_counts,
        "fixed_phase_independent_character_maximum_distinct_K_blocks_on_actual_rows": maximum_fixed_coverage,
        "N69_all_character_match_counts_by_K_block": n69_all_character_counts,
        "N69_frozen_phase_dual_hits": n69_phase_dual_hits,
        "ablations": {
            "phase_offsets_at_t10": phase_offset_outputs,
            "opposite_orientation": negative_word("021101"),
            "canonical_frontier_a_instead": linear_word(row10, (1, 1, 2)),
            "successor_t11_instead_of_predecessor_t10": next(
                item["output"] for item in actual_outputs if item["t"] == 11
            ),
        },
        "conclusion": (
            "la regla fase--dual congelada certifica el cuarto bloque ternario y, con él, K3=140; "
            "no emite por sí sola los ocho bloques ternarios restantes. La presencia de todos ellos bajo "
            "búsqueda libre de caracteres en N69 es existencia de coincidencias, no una selección."
        ),
    }


def build_result() -> dict[str, object]:
    current = json.loads(CURRENT.read_text(encoding="utf-8"))
    require(current["revision"] == "2026-07-22.2", "revisión canónica inesperada")
    rombo = build_rombo_prefix()
    phase_dual = phase_dual_construction()
    raw_word = str(phase_dual["raw_word"])
    catalogue = catalogue_bridge(raw_word)
    recognition = k_recognition(str(rombo["descriptor_18"]), raw_word, current)
    k_blocks = recognition["K_ternary_blocks_for_later_ablations"]
    require(isinstance(k_blocks, list), "bloques K mal tipados")
    continuation = continuation_and_ablations([str(value) for value in k_blocks])

    source_paths = [
        CURRENT,
        N72_BRANCHES,
        N72_PROFILE,
        N74_RETURN,
        N69_SIGNATURES,
        N33_INDEX,
        HISTORICAL_ALPHA,
        ROMBO_CERTIFICATE,
    ]
    return {
        "schema": "HMT.phase-dual-K3-certificate.v1",
        "status": "PASS_CARACTER_FASE_DUAL_Y_K3_FORZADO",
        "current_revision": current["revision"],
        "authors": ["Oumar Haidara Fall", "Rubén Ramos Balsa"],
        "rombo_and_return": rombo,
        "phase_dual_character": phase_dual,
        "N33_raw_visible_bridge": catalogue,
        "exact_decimal_recognition": recognition,
        "continuation_and_ablations": continuation,
        "provenance": {
            "architecture": "ARQUITECTURA_AUTORAL_PREEXISTENTE: N69--N74, rhoW, G9 y orientación TRIT",
            "recovered": "RESULTADO_RECUPERADO: 021101 y su preimagen U6 ya estaban en N33 y en F004",
            "formalization": "FORMALIZACION_NUEVA: carácter natural fase--carga aplicado al predecesor t=10",
            "certificate": "CERTIFICADO_NUEVO: cilindro de 24 trits, unicidad, naturalidad y ablaciones",
            "not_claimed": "no se declara que esta única regla genere todavía los doce bloques de K",
        },
        "dictum": (
            "El rombo y el retorno fijan 020022|222111|211201. El predecesor t=10, seleccionado por "
            "supervivencia, tiene carga dual 012 y fase 1; el carácter natural +1 sobre la carga coincidente "
            "y -1 sobre el complemento produce -pi+e-phi=021101 sin consultar K. El cilindro de 24 trits "
            "queda contenido íntegramente en la celda decimal 234|543|140. Por tanto K3=140 queda forzado "
            "relativamente a este lector interno. La misma regla no prolonga aún todo el sello."
        ),
        "source_sha256": {relative(path): sha256(path) for path in source_paths},
    }


def render(result: dict[str, object]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--check-certificate", action="store_true")
    args = parser.parse_args(argv)
    result = build_result()
    text = render(result)
    if args.write_certificate:
        CERTIFICATE.write_text(text, encoding="utf-8")
    if args.check_certificate:
        require(CERTIFICATE.exists(), "falta el certificado congelado")
        require(CERTIFICATE.read_text(encoding="utf-8") == text, "el certificado congelado no coincide")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
