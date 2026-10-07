#!/usr/bin/env python3
"""Certificado exacto del rombo especular, las nueve fases y la frontera CT108 -> K.

El programa usa sólo la biblioteca estándar. Distingue tres cuestiones:

1. hechos finitos de las tablas N69--N74;
2. reconocimiento del comienzo ternario del sello dodecafásico K;
3. suficiencia (o insuficiencia) de las rutas cardinales publicadas para
   reconstruir K sin introducirlo como dato.

No usa alpha, CODATA ni valores físicos como entradas de ninguna selección.
La comparación con K se ejecuta únicamente después de construir el descriptor
del rombo a partir de las tablas de ramas.
"""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import itertools
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

CURRENT = ROOT / "03_PAPER/HMT_MACROPAPER_V3/CURRENT.json"

N69_DIR = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_CADENA_VIGENTE/N69_CALENDARIO_TRANSICION/"
    "HMT_N69_ley_transicion_o_axioma_cilindrico_v1"
)
N69_STUTTER = N69_DIR / "N69_stutter_schedule_summary.csv"

N71_DIR = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_N57_N71/HMT_N71_selector_pares_udelta_frontera_v1"
)
N71_EDGES = N71_DIR / "N71_one_step_survival_of_pair_selector.csv"

N72_DIR = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_N72_N75/HMT_N72_supervivencia_coinductiva_novena_puerta_v1"
)
N72_BRANCHES = N72_DIR / "N72_selected_branches_survival_details.csv"
N72_PROFILE = N72_DIR / "N72_coinductive_survival_profile_t5_t25_h9.csv"

N74_DIR = ROOT / (
    "03_PAPER/HMT_CIERRE_HOLOGRAFICO_V2_RECTOR/certificados/"
    "G9_N72_N75/HMT_N74_monodromia_nueve_puertas_v1"
)
N74_RETURN = N74_DIR / "N74_monodromy_return_t_to_t_plus_9.csv"

N33_INDEX = ROOT / (
    "06_NUEVOS_PAQUETES/HMT_N33_PI_E_PHI_CLOSEOUT_v3/"
    "HMT_N33_PI_PHI_E_CLOSEOUT/n33_w6_index.json"
)

N38_DATA = ROOT / (
    "02_LECTURA/paquetes_descomprimidos/F081_archivador-Feigenbaum-perme/"
    "archivador-Feigenbaum-perme/__extraido__/HMT_N38_HENSEL_LIFT_FLOW_PACK/"
    "n38_lift_data.json"
)
ORIENTATION_SOURCE = ROOT / (
    "02_LECTURA/paquetes_descomprimidos/F081_archivador-Feigenbaum-perme/"
    "archivador-Feigenbaum-perme/hmt_puerta_orientacion01_reflection_family.py"
)

ROUTES_DIR = ROOT / (
    "02_LECTURA/ingesta_usuario_2026-07-19_enero_stale/EXTRACTED/"
    "2026-01-14/14-enero-26"
)
ROUTES_CLOCK = ROUTES_DIR / "TPK_K27_routes_CT108_NEWSO.csv"
ROUTES_ROTOR = ROUTES_DIR / "K27_TPK_rotor_routes_NEWSO_108.csv"
ROUTES_CLOCK_SOURCE = ROUTES_DIR / "run_hmt_app_tpk_pi_e_phi_routes_and_triads.py"
ROUTES_ROTOR_SOURCE = ROUTES_DIR / "hmt_APP_TPK_motor_and_carry_lector_FINAL.py"

HISTORICAL_TEXT = ROOT / "01_ORIGINALES/2026-01/F007_rutas y más.txt"
PRIOR_AUDIT = ROOT / "03_PAPER/HMT_MACROPAPER_V3/tools/verificar_procedencia_app_lifts_k.py"
TRANSDUCTOR_RESULT = ROOT / (
    "16_CIERRE_GLOBAL_HMT_MD_2026-07-22/08_TRANSDUCTOR_729_1000/"
    "RESULTADO_TRANSDUCTOR_Y_DIAMANTE.json"
)

CERTIFICATE = HERE / "CERTIFICADO_ROMBO_NUEVE_FASES.json"


K_SEAL = [234, 543, 140, 729, 659, 824, 621, 58, 914, 794, 146, 601]
U12_SIGNED = [2378, 1406, 2479, -452, 998, -551, -668, -204, -371, -322, -28, -997]
K_DECIMAL_DIGITS = "".join(f"{value:03d}" for value in K_SEAL)

H4 = (
    (1, 1, 1, 1),
    (1, 1, -1, -1),
    (1, -1, 1, -1),
    (1, -1, -1, 1),
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


def ternary_fraction_digits(numerator: int, denominator: int, length: int) -> str:
    """Primeros ``length`` trits de numerator/denominator, sin redondeo."""
    require(0 <= numerator < denominator, "se esperaba una fracción propia")
    out: list[str] = []
    remainder = numerator
    for _ in range(length):
        remainder *= 3
        digit, remainder = divmod(remainder, denominator)
        require(digit in (0, 1, 2), "dígito ternario fuera de rango")
        out.append(str(digit))
    return "".join(out)


def fraction_text(numerator: int, denominator: int) -> str:
    return str(Fraction(numerator, denominator))


def ternary_cylinder_decimal_audit(word_value: str) -> dict[str, object]:
    """Determina, por extremos racionales, las tríadas decimales forzadas.

    El cilindro es [N/3^ell,(N+1)/3^ell). Una profundidad decimal m
    queda fijada exactamente cuando ambos extremos pertenecen al mismo
    cilindro de base 1000 y profundidad m.
    """
    require(word_value and set(word_value) <= {"0", "1", "2"}, "palabra ternaria inválida")
    numerator = int(word_value, 3)
    denominator = 3 ** len(word_value)
    forced_depth = 0
    forced_integer = 0
    for depth in range(1, 13):
        scale = 1000 ** depth
        lower_cell = numerator * scale // denominator
        upper_cell = ((numerator + 1) * scale - 1) // denominator
        if lower_cell != upper_cell:
            break
        forced_depth = depth
        forced_integer = lower_cell

    possible_first = list(
        range(
            numerator * 1000 // denominator,
            ((numerator + 1) * 1000 - 1) // denominator + 1,
        )
    )
    result: dict[str, object] = {
        "word": word_value,
        "trits": len(word_value),
        "base3_integer": numerator,
        "cylinder": [
            fraction_text(numerator, denominator),
            fraction_text(numerator + 1, denominator),
        ],
        "forced_decimal_triads": forced_depth,
        "possible_first_decimal_triads": possible_first,
    }
    if forced_depth:
        rendered = f"{forced_integer:0{3 * forced_depth}d}"
        blocks = [rendered[index:index + 3] for index in range(0, len(rendered), 3)]
        scale = 1000 ** forced_depth
        residual_lower_num = numerator * scale - forced_integer * denominator
        residual_upper_num = (numerator + 1) * scale - forced_integer * denominator
        result.update(
            {
                "forced_decimal_prefix": rendered,
                "forced_decimal_blocks": blocks,
                "residual_after_forced_blocks": [
                    fraction_text(residual_lower_num, denominator),
                    fraction_text(residual_upper_num, denominator),
                ],
                "possible_next_decimal_triads": list(
                    range(
                        residual_lower_num * 1000 // denominator,
                        (residual_upper_num * 1000 - 1) // denominator + 1,
                    )
                ),
            }
        )
    return result


def add_word(a: str, b: str) -> str:
    require(len(a) == len(b), "palabras de longitudes distintas")
    return "".join(str((int(x) + int(y)) % 3) for x, y in zip(a, b))


def subtract_word(a: str, b: str) -> str:
    require(len(a) == len(b), "palabras de longitudes distintas")
    return "".join(str((int(x) - int(y)) % 3) for x, y in zip(a, b))


def split_rows(value: str) -> tuple[str, str, str]:
    rows = tuple(value.split("|"))
    require(len(rows) == 3 and all(len(row) == 6 for row in rows), "fila ternaria mal tipada")
    return rows  # type: ignore[return-value]


def choose_saturated_mirror(rows_t20: list[dict[str, str]]) -> dict[str, object]:
    """Selecciona la vacancia saturada sin consultar K.

    El criterio es interno a la familia especular: phi fijo, suma pi+e fija,
    defecto soportado sólo en la semipalabra terminal y valores constantes
    111/222 en las dos orientaciones.
    """
    actual_rows = [row for row in rows_t20 if row["is_actual"] == "True"]
    require(len(actual_rows) == 1, "t=20 no tiene una única rama actual")
    actual = split_rows(actual_rows[0]["rows"])
    selected: list[tuple[dict[str, str], tuple[str, str, str], str, str]] = []
    for row in rows_t20:
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
    require(len(selected) == 1, "el criterio saturado no seleccionó una única rama")
    row, candidate, delta_pi, delta_e = selected[0]

    # Lector de vacancia orientada: hoja e visible, defecto terminal e -> pi.
    # Su canonicidad global NO se presupone; se audita después como lector nuevo.
    descriptor = candidate[1] + delta_e[3:] + delta_pi[3:]
    return {
        "actual": list(actual),
        "mirror": list(candidate),
        "mirror_index": int(row["idx"]),
        "delta_pi": delta_pi,
        "delta_e": delta_e,
        "descriptor_12": descriptor,
        "survival": [int(row[f"surv_h{i}"]) for i in range(1, 10)],
    }


def branch_and_diamond_audit() -> dict[str, object]:
    branches = read_csv(N72_BRANCHES)
    t20 = [row for row in branches if row["t"] == "20"]
    t21 = [row for row in branches if row["t"] == "21"]
    t22 = [row for row in branches if row["t"] == "22"]
    require((len(t20), len(t21), len(t22)) == (5, 2, 1), "cardinales 5 -> 2 -> 1 alterados")

    mirror = choose_saturated_mirror(t20)
    require(mirror["mirror"] == ["221100", "020022", "211021"], "rama saturada alterada")
    require(mirror["survival"] == [1, 2, 0, 0, 0, 0, 0, 0, 0], "supervivencia alterada")

    actual20 = split_rows(next(row["rows"] for row in t20 if row["is_actual"] == "True"))
    mirror20 = tuple(mirror["mirror"])
    require(int(actual20[0], 3) == 683 and int(actual20[1], 3) == 171, "enteros actuales alterados")
    require(int(mirror20[0], 3) == 684 and int(mirror20[1], 3) == 170, "transferencia espejo alterada")

    edges = read_csv(N71_EDGES)
    edges20 = [row for row in edges if row["t"] == "20"]
    edges21 = [row for row in edges if row["t"] == "21"]
    expected_middle = {
        "201100|001211|101021",
        "201211|001100|101021",
    }
    require(len(edges20) == 5, "faltan ramas de origen del rombo")
    for row in edges20:
        extensions = {value.strip() for value in row["first_extension_rows"].split(";")}
        require(int(row["extension_count"]) == 2 and extensions == expected_middle,
                "una rama t=20 no alcanza ambos vértices t=21")
    require(len(edges21) == 2, "faltan los dos vértices intermedios")
    for row in edges21:
        require(
            int(row["extension_count"]) == 1
            and row["first_extension_rows"] == "101110|101012|112120",
            "el rombo no cierra en el único vértice t=22",
        )

    # El mismo defecto saturado persiste una fase y se aniquila en el vértice común.
    actual21 = split_rows(next(row["rows"] for row in t21 if row["is_actual"] == "True"))
    mirror21 = split_rows(next(row["rows"] for row in t21 if row["is_actual"] == "False"))
    require(subtract_word(mirror21[0], actual21[0]) == "000111", "defecto pi t=21 alterado")
    require(subtract_word(mirror21[1], actual21[1]) == "000222", "defecto e t=21 alterado")

    profile = read_csv(N72_PROFILE)
    profile20 = next(row for row in profile if row["t"] == "20")
    profile21 = next(row for row in profile if row["t"] == "21")
    profile22 = next(row for row in profile if row["t"] == "22")
    require(
        (profile20["K_t"], profile20["dK"], profile20["resolution_depth"]) == ("20", "0", "3"),
        "perfil de stutter t=20 alterado",
    )
    require(profile21["K_t"] == "20" and profile22["K_t"] == "21", "calendario local alterado")

    return {
        "status": "PASS_EXACTO_INTERNO",
        "cardinalities_t20_t21_t22": [5, 2, 1],
        "stutter_t20": {"K_t": 20, "dK": 0, "resolution_depth": 3},
        "saturated_mirror": mirror,
        "integer_transfer_pi_e": {"actual": [683, 171], "mirror": [684, 170], "delta": [1, -1]},
        "diamond": {
            "all_five_t20_reach_both_t21": True,
            "both_t21_reach_unique_t22": True,
            "t21_vertices": sorted(expected_middle),
            "t22_vertex": "101110|101012|112120",
        },
        "interpretation": (
            "la proyección visible olvida la ascendencia: cinco ramas confluyen en dos y después en una; "
            "el estado enriquecido debe conservar la historia"
        ),
    }


def n33_audit() -> dict[str, object]:
    data = json.loads(N33_INDEX.read_text(encoding="utf-8"))
    require(data["schema"] == "HMT.N33.complete-w6-index.v3", "esquema N33 inesperado")
    require(data["num_w6"] == 243 and data["num_U6_preimages"] == 468, "censo N33 alterado")
    entry = data["words"]["020022"]
    preimage = entry["canonical_preimage"]
    require(entry["num_U6_preimages"] == 1, "020022 dejó de tener preimagen única")
    require(preimage["U6"] == [252, 109, 252, 903, 850, 850], "preimagen U6 alterada")
    require(preimage["multiplicity"] == 144, "multiplicidad alterada")
    require(entry["w30"] == "020022020001000222102000121210", "lift N33 alterado")
    return {
        "status": "PASS_RESULTADO_RECUPERADO",
        "catalogue": "104976 -> 468 U6 -> 243 w6",
        "word": "020022",
        "unique_U6_preimage": preimage,
        "frozen_w30": entry["w30"],
        "triads_4": entry["triads_4"],
    }


def k_recognition_audit(descriptor_12: str) -> dict[str, object]:
    numerator = int(K_DECIMAL_DIGITS)
    denominator = 10 ** len(K_DECIMAL_DIGITS)
    ternary = ternary_fraction_digits(numerator, denominator, 72)
    blocks = [ternary[index:index + 6] for index in range(0, 72, 6)]
    require(
        ternary
        == "020022222111211201021101002001020111200110121012010122001001221110222110",
        "expansión ternaria de K alterada",
    )
    require(descriptor_12 == ternary[:12], "el descriptor del rombo ya no coincide con K[0:12]")

    returns = read_csv(N74_RETURN)
    return_11_20 = next(row for row in returns if row["t"] == "11" and row["t_plus_9"] == "20")
    require(return_11_20["phase_K_mod9"] == "2", "fase 11 -> 20 alterada")
    require(return_11_20["pi_plus_e_t"].zfill(6) == "211201", "suma pi+e de t=11 alterada")
    require(return_11_20["same_phi"] == "False" and return_11_20["same_pi_plus_e"] == "False",
            "se confundió retorno de fase con retorno de estado")
    descriptor_18 = descriptor_12 + return_11_20["pi_plus_e_t"].zfill(6)
    require(descriptor_18 == ternary[:18], "el rombo retrospectivo ya no coincide en 18 trits")

    n33 = json.loads(N33_INDEX.read_text(encoding="utf-8"))["words"]["020022"]
    require(n33["w30"][:6] == ternary[:6], "raíz N33 y K ya no comparten w6")
    require(n33["w30"][6:12] != ternary[6:12], "el lift N33 coincidió inesperadamente con K")

    d3 = [K_SEAL[i] - K_SEAL[(i + 3) % 12] for i in range(12)]
    d4 = [K_SEAL[i] - K_SEAL[(i + 4) % 12] for i in range(12)]
    sequences = {"K": K_SEAL, "U12": U12_SIGNED, "D3K": d3, "D4K": d4}

    def orbit_mod3(sequence: list[int]) -> set[str]:
        base = [value % 3 for value in sequence]
        out: set[str] = set()
        for scalar in (1, 2):
            scaled = [(scalar * value) % 3 for value in base]
            for reverse in (False, True):
                oriented = list(reversed(scaled)) if reverse else scaled
                for step in (1, 5, 7, 11):
                    for shift in range(12):
                        out.add("".join(str(oriented[(shift + step * i) % 12]) for i in range(12)))
        return out

    orbit_matches = {name: descriptor_12 in orbit_mod3(values) for name, values in sequences.items()}
    require(not any(orbit_matches.values()), "apareció una identificación coordenada elemental")

    linear_matches = 0
    for coefficients in itertools.product(range(3), repeat=4):
        if coefficients == (0, 0, 0, 0):
            continue
        combined = [
            sum(coefficients[j] * list(sequences.values())[j][i] for j in range(4))
            for i in range(12)
        ]
        if descriptor_12 in orbit_mod3(combined):
            linear_matches += 1
    require(linear_matches == 0, "el descriptor apareció como combinación lineal coordenada")

    return {
        "status": "PASS_RECONOCIMIENTO_EXTERNO_TIPADO",
        "K_base1000": K_SEAL,
        "K_decimal_concatenation": "0." + K_DECIMAL_DIGITS,
        "ternary_first_72": ternary,
        "ternary_blocks_6": blocks,
        "rombo_descriptor_12": descriptor_12,
        "phase_predecessor_t11_pi_plus_e": "211201",
        "retrospective_descriptor_18": descriptor_18,
        "matches_K_first_12": True,
        "matches_K_first_18": True,
        "N33_lift_diverges_at_digit": 7,
        "coordinatewise_mod3_orbit_matches": orbit_matches,
        "linear_combination_orbit_matches": linear_matches,
        "scope": (
            "identidad exacta relativa al lector de vacancia orientada recién formalizado; "
            "no prueba todavía que ese lector sea la proyección canónica única del registro enriquecido"
        ),
    }


def residual_transport_audit(descriptor_12: str, descriptor_18: str) -> dict[str, object]:
    """Cruza el rombo N72/N74 con el transductor exacto 729 -> 1000.

    La comparación decisiva se hace por intervalos, no por proximidad
    decimal. En particular, distingue una palabra compatible con K de una
    palabra que fuerza efectivamente una o más tríadas decimales.
    """
    require(descriptor_12 == "020022222111", "descriptor N72 inesperado")
    require(descriptor_18 == descriptor_12 + "211201", "transporte N74 inesperado")

    cylinder_6 = ternary_cylinder_decimal_audit(descriptor_12[:6])
    cylinder_12 = ternary_cylinder_decimal_audit(descriptor_12)
    cylinder_18 = ternary_cylinder_decimal_audit(descriptor_18)
    require(cylinder_6["forced_decimal_triads"] == 0, "020022 forzó una tríada inesperadamente")
    require(cylinder_6["possible_first_decimal_triads"] == [233, 234], "frontera 233/234 alterada")
    require(cylinder_12["forced_decimal_triads"] == 1, "el rombo de 12 trits no fuerza K1")
    require(cylinder_12["forced_decimal_blocks"] == ["234"], "K1 del rombo alterado")
    require(cylinder_18["forced_decimal_triads"] == 2, "los 18 trits no fuerzan dos tríadas")
    require(cylinder_18["forced_decimal_blocks"] == ["234", "543"], "K1,K2 alterados")
    require(cylinder_18["possible_next_decimal_triads"] == [140, 141, 142],
            "abanico residual tras K2 alterado")

    # Estado residual una vez emitido K1. El bloque de retorno 211201
    # contrae este intervalo hasta la celda 543; después transporta el
    # nuevo resto hacia el abanico 140--142.
    n12, d12 = int(descriptor_12, 3), 3 ** len(descriptor_12)
    n18, d18 = int(descriptor_18, 3), 3 ** len(descriptor_18)
    residual_k1_w12 = [
        fraction_text(n12 * 1000 - 234 * d12, d12),
        fraction_text((n12 + 1) * 1000 - 234 * d12, d12),
    ]
    residual_k1_w18 = [
        fraction_text(n18 * 1000 - 234 * d18, d18),
        fraction_text((n18 + 1) * 1000 - 234 * d18, d18),
    ]
    require(residual_k1_w12 == ["287806/531441", "288806/531441"],
            "resto W12 tras K1 alterado")
    require(residual_k1_w18 == ["210423574/387420489", "210424574/387420489"],
            "resto W18 tras K1 alterado")

    transductor = json.loads(TRANSDUCTOR_RESULT.read_text(encoding="utf-8"))
    require(transductor["estado"] == "PASS_TRANSDUCTOR_EXACTO_Y_DIAMANTE_INICIAL",
            "el transductor 729->1000 no está certificado")
    initial = transductor["diamante_inicial"]
    require(initial["raices_base729"] == {"pi": 103, "e": 523, "phi": 450},
            "raíces del diamante inicial alteradas")
    require(initial["cocientes_de_enlace"] == {"pi": 38, "e": 195, "phi": 168},
            "cocientes del diamante inicial alterados")
    require(initial["K1_generado"] == 234 and not initial["uso_de_alpha_o_K_en_la_generacion"],
            "K1 no fue generado independientemente del objetivo")
    require(initial["A1_generado"] == 7, "A1 del diamante inicial alterado")

    return {
        "status": "PASS_TRANSPORTE_RESIDUAL_Y_DOS_TRIADAS_FORZADAS",
        "ternary_blocks": {
            "mirror_visible": descriptor_12[:6],
            "oriented_terminal_defect": descriptor_12[6:12],
            "same_phase_predecessor_sum": descriptor_18[12:18],
            "base3_values": [
                int(descriptor_12[:6], 3),
                int(descriptor_12[6:12], 3),
                int(descriptor_18[12:18], 3),
            ],
        },
        "cylinders": {
            "six_trits": cylinder_6,
            "twelve_trits": cylinder_12,
            "eighteen_trits": cylinder_18,
        },
        "exact_emission_sequence": [
            "020022 cruza la frontera decimal 233/234 y no fuerza K1",
            "020022|222111 queda contenido en la celda 234 y fuerza K1=234",
            "020022|222111|211201 queda contenido en la celda 234|543 y fuerza K2=543",
        ],
        "residual_after_K1": {
            "before_211201": residual_k1_w12,
            "after_211201": residual_k1_w18,
        },
        "residual_after_K2": cylinder_18["residual_after_forced_blocks"],
        "possible_K3_from_18_trits": cylinder_18["possible_next_decimal_triads"],
        "does_211201_transport_the_next_residual_state": True,
        "precise_meaning": (
            "211201 refina el resto posterior a K1 hasta emitir K2=543 y deja un nuevo intervalo residual; "
            "no fija por sí solo K3, que todavía puede ser 140, 141 o 142"
        ),
        "independent_first_component_bridge": {
            "roots_base729": initial["raices_base729"],
            "regional_selector": transductor["selector_regional"]["coordenada_singleton"],
            "A1_formula": initial["formula_A1"],
            "seams_729_to_1000": initial["cocientes_de_enlace"],
            "K1_formula": initial["formula_K1"],
            "generated_without_alpha_or_K_target": True,
            "same_K1_forced_by_N72_cylinder": 234,
        },
        "scope": (
            "dos tríadas decimales quedan forzadas por el cilindro de 18 trits; la tercera queda localizada "
            "en tres celdas y requiere el siguiente refinamiento del estado enriquecido"
        ),
    }


def floor_log1000_power3(length: int) -> int:
    """floor(log_1000(3**length)) sin coma flotante."""
    value = 3 ** length
    power = 1
    result = 0
    while power * 1000 <= value:
        power *= 1000
        result += 1
    return result


def integer_from_digits(digits: list[int], base: int) -> int:
    value = 0
    for digit in digits:
        value = base * value + int(digit)
    return value


def ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def emit_hensel_blocks(matrix: list[list[int]], x0: list[int], steps: int = 180) -> list[tuple[int, ...]]:
    state = [int(value) for value in x0]
    blocks: list[tuple[int, ...]] = []
    for _ in range(steps):
        lifted = [sum(state[i] * int(matrix[i][j]) for i in range(6)) for j in range(6)]
        visible = tuple(value % 3 for value in lifted)
        blocks.append(visible)
        state = [(lifted[j] - visible[j]) // 3 for j in range(6)]
    return blocks


def cylinder_candidates(prefix: list[int], triads: list[int]) -> set[tuple[int, ...]]:
    length = len(prefix) + 6
    k = floor_log1000_power3(length)
    decimal_prefix = integer_from_digits(triads[:k], 1000)
    modulus = 1000 ** k
    power3 = 3 ** length
    base = integer_from_digits(prefix, 3) * (3 ** 6)
    upper = ((decimal_prefix + 1) * power3 - 1) // modulus - base
    lower = ceil_div(decimal_prefix * power3 + 1, modulus) - 1 - base
    lower = max(lower, 0)
    upper = min(upper, 3 ** 6 - 1)
    if upper < lower:
        return set()
    out: set[tuple[int, ...]] = set()
    for number in range(lower, upper + 1):
        out.add(tuple((number // (3 ** (5 - i))) % 3 for i in range(6)))
    return out


A_W = (
    (0, 1, 1, 1, 1, 1),
    (1, 0, 1, 1, 2, 2),
    (1, 1, 0, 2, 1, 2),
    (1, 1, 2, 0, 2, 1),
    (1, 2, 1, 2, 0, 1),
    (1, 2, 2, 1, 1, 0),
)


def dot_mod3(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(x * y for x, y in zip(a, b)) % 3


def orientation_signature(block: tuple[tuple[int, ...], ...]) -> tuple[object, ...]:
    q = tuple(sum(block[i][j] for i in range(3)) % 3 for j in range(6))
    a = tuple((block[0][j] + block[1][j] - block[2][j]) % 3 for j in range(6))
    c = tuple((sum(block[i][j] for i in range(3)) - q[j]) // 3 for j in range(6))
    r = tuple(sum(row) % 3 for row in block)
    rho_w = tuple(
        sum(dot_mod3(row, tuple(A_W[i][j] for i in range(6))) for j in range(6)) % 3
        for row in block
    )
    column_weight = tuple(sum(block[i][j] != 0 for i in range(3)) for j in range(6))
    return q, a, c, r, rho_w, column_weight


def filter_orientation_candidates(
    candidate_sets: dict[str, set[tuple[int, ...]]],
    target_signature: tuple[object, ...],
) -> list[tuple[tuple[int, ...], ...]]:
    all_columns = itertools.product(range(3), repeat=3)
    columns: list[list[tuple[int, int, int]]] = []
    for j in range(6):
        allowed: list[tuple[int, int, int]] = []
        for pi_value, e_value, phi_value in all_columns:
            q = (pi_value + e_value + phi_value) % 3
            a = (pi_value + e_value - phi_value) % 3
            c = (pi_value + e_value + phi_value - q) // 3
            weight = int(pi_value != 0) + int(e_value != 0) + int(phi_value != 0)
            if (q, a, c, weight) == (
                target_signature[0][j],
                target_signature[1][j],
                target_signature[2][j],
                target_signature[5][j],
            ):
                allowed.append((pi_value, e_value, phi_value))
        columns.append(allowed)
        all_columns = itertools.product(range(3), repeat=3)

    results: list[tuple[tuple[int, ...], ...]] = []
    for choices in itertools.product(*columns):
        block = (
            tuple(choice[0] for choice in choices),
            tuple(choice[1] for choice in choices),
            tuple(choice[2] for choice in choices),
        )
        if any(block[i] not in candidate_sets[channel] for i, channel in enumerate(("pi", "e", "phi"))):
            continue
        signature = orientation_signature(block)
        if signature[3] == target_signature[3] and signature[4] == target_signature[4]:
            results.append(block)
    return results


def word(block: tuple[int, ...]) -> str:
    return "".join(str(value) for value in block)


def recurrence_negative_control() -> dict[str, object]:
    """Comprueba los cinco stutters de N69 en la familia histórica de cilindros.

    Esta prueba es RELATIVA A PRIMITIVAS: N38 contiene lifts reconstruidos desde
    los tres canales y sus prefijos decimales. Sirve como ablación del supuesto
    de repetición del rombo, no como generador autónomo de dichos canales.
    """
    data = json.loads(N38_DATA.read_text(encoding="utf-8"))
    matrix = data["A"]
    channels = ("pi", "e", "phi")
    blocks = {
        channel: emit_hensel_blocks(matrix, data["channels"][channel]["x0_mod_3^180"])
        for channel in channels
    }
    triads = {
        channel: data["channels"][channel]["triads_171_from_1080trits"]
        for channel in channels
    }

    # N69 usa t=20,42,... para K_t=K_{t+1}; el script de cilindros indexa
    # el bloque siguiente como 21,43,...
    stutters = [20, 42, 64, 86, 108]
    block_indices = [value + 1 for value in stutters]
    rows: list[dict[str, object]] = []
    for stutter, t in zip(stutters, block_indices):
        candidate_sets = {
            channel: cylinder_candidates(
                [digit for block in blocks[channel][:t] for digit in block],
                triads[channel],
            )
            for channel in channels
        }
        actual = tuple(blocks[channel][t] for channel in channels)
        signature = orientation_signature(actual)
        local = filter_orientation_candidates(candidate_sets, signature)
        is_orientation_door = (
            len(local) > 1
            and len({candidate[2] for candidate in local}) == 1
            and len({(candidate[0], candidate[1]) for candidate in local}) == len(local)
        )
        saturated = []
        for candidate in local:
            if candidate == actual:
                continue
            delta_pi = subtract_word(word(candidate[0]), word(actual[0]))
            delta_e = subtract_word(word(candidate[1]), word(actual[1]))
            if delta_pi == "000111" and delta_e == "000222":
                saturated.append([word(row) for row in candidate])
        rows.append(
            {
                "N69_stutter": stutter,
                "cylinder_block_index": t,
                "candidate_counts_pi_e_phi": [len(candidate_sets[channel]) for channel in channels],
                "local_signature_solutions": len(local),
                "orientation_door": is_orientation_door,
                "saturated_000111_000222_count": len(saturated),
                "actual": [word(row) for row in actual],
            }
        )

    require([row["local_signature_solutions"] for row in rows] == [5, 3, 3, 1, 3],
            "cambió la familia de stutters profundos")
    require([row["saturated_000111_000222_count"] for row in rows] == [1, 0, 0, 0, 0],
            "el defecto saturado dejó de ser exclusivo del primer stutter")

    schedule = read_csv(N69_STUTTER)
    require(len(schedule) == 1, "resumen N69 inesperado")
    schedule_stutters = [int(value) for value in schedule[0]["first_stutters"].split(",")]
    schedule_gaps = [int(value) for value in schedule[0]["stutter_gaps"].split(",")]
    require(schedule_stutters == stutters, "stutters N69 alterados")
    require(schedule_gaps == [22, 22, 22, 22], "paso 22 ausente o alterado")

    return {
        "status": "PASS_RELATIVO_A_PRIMITIVAS_CONTROL_NEGATIVO",
        "N69_first_stutters": stutters,
        "gap": 22,
        "conditioned_cylinder_rows": rows,
        "conclusion": (
            "el rombo saturado 000111/000222 de t=20 no se repite por una ley de nueve fases "
            "en los cuatro stutters siguientes; una prolongación de K requiere más estado que la fase y el stutter"
        ),
    }


def dr9(value: int) -> int:
    residue = value % 9
    return 9 if residue == 0 else residue


def historical_four_cursor_mask(weight_a: int = 2, weight_c: int = 5, additive_offset: int = 0) -> list[int]:
    plus = [[dr9(i + j + additive_offset) for j in range(9)] for i in range(9)]
    times = [[dr9((i + 1) * (j + 1)) for j in range(9)] for i in range(9)]
    heads = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "O": (0, -1)}
    positions = {"N": [0, 0], "E": [0, 3], "S": [3, 0], "O": [3, 3]}
    parity = 0
    digits: list[int] = []
    result: list[int] = []
    order = ("N", "E", "S", "O")
    for tick in range(1, 109):
        residue = ((tick - 1) % 9) + 1
        movement = 1 if residue in (1, 4, 7) else -1 if residue in (2, 5, 8) else 0
        for route in positions:
            di, dj = heads[route]
            i, j = positions[route]
            positions[route] = [(i + movement * di) % 9, (j + movement * dj) % 9]
        if residue in (3, 6, 9):
            additive = sum(plus[positions[route][0]][positions[route][1]] for route in order) % 10
            multiplicative = 1
            for route in order:
                value = times[positions[route][0]][positions[route][1]]
                multiplicative = multiplicative * (value % 9) % 9
            multiplicative = 9 if multiplicative == 0 else multiplicative
            digits.append((weight_a * additive + weight_c * multiplicative + parity) % 10)
        if tick in (27, 54, 81, 108):
            parity = 1 - parity
        if tick % 9 == 0:
            result.append(100 * digits[-3] + 10 * digits[-2] + digits[-1])
    return result


def route_a_digits(path: Path, digit_column: str) -> tuple[list[int], dict[tuple[str, int], int], list[str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    table = {(row["route"], int(row["tick"])): int(row[digit_column]) for row in rows}
    require(len(table) == 432, f"{path.name}: se esperaban 432 pares ruta/tick")
    output: list[int] = []
    for event in range(12):
        count = 0
        for route in "NESO":
            for tick in range(9 * event + 1, 9 * event + 10):
                count += table[(route, tick)] in {1, 3, 5, 7}
        output.append(count % 10)
    return output, table, fieldnames


def routes_no_go_audit() -> dict[str, object]:
    clock_a, clock_table, clock_fields = route_a_digits(ROUTES_CLOCK, "digit_d")
    rotor_a, rotor_table, rotor_fields = route_a_digits(ROUTES_ROTOR, "digit")
    differing = sum(clock_table[key] != rotor_table[key] for key in clock_table)
    require(differing == 391, "cambió la incompatibilidad entre las dos tablas de rutas")
    require(clock_a == [1, 7, 9, 0, 7, 0, 1, 7, 9, 0, 7, 0], "conteo A relojado alterado")
    require(rotor_a == [9, 6, 7, 6, 9, 6, 7, 6, 9, 6, 7, 6], "conteo A rotor alterado")
    target_hundreds = [value // 100 for value in K_SEAL]
    require(clock_a != target_hundreds and rotor_a != target_hundreds, "una tabla reprodujo los cientos de K")

    literal = historical_four_cursor_mask()
    require(literal == [222, 222, 222, 333, 333, 333] * 2, "pseudocódigo histórico dejó de colapsar")
    weight_hits = [
        [weight_a, weight_c]
        for weight_a in range(10)
        for weight_c in range(10)
        if historical_four_cursor_mask(weight_a, weight_c) == K_SEAL
    ]
    require(weight_hits == [], "un par de pesos produjo K inesperadamente")
    chart_outputs = {str(offset): historical_four_cursor_mask(additive_offset=offset) for offset in range(3)}
    require(all(output != K_SEAL for output in chart_outputs.values()), "una carta aditiva produjo K")

    # Se usan nombres semánticos deliberadamente explícitos: la columna ``j``
    # del CSV rotor es una coordenada de celda, no la clase longitudinal j de
    # una traza 120(1+3j), y ``residue_rho`` tampoco es su clase r tipada.
    trace_fields = {
        "trace_id",
        "trace_class_r",
        "trace_length_j",
        "orientation_sign",
        "boundary_type",
        "weight",
    }
    missing_clock = sorted(trace_fields - set(clock_fields))
    missing_rotor = sorted(trace_fields - set(rotor_fields))
    require(missing_clock == sorted(trace_fields) and missing_rotor == sorted(trace_fields),
            "alguna tabla adquirió los campos de la traza enriquecida")

    return {
        "status": "PASS_NO_IDENTIFICABILIDAD_DESDE_LAS_TABLAS_PUBLICADAS",
        "route_tables": {
            ROUTES_CLOCK.name: {
                "A_digit_by_event": clock_a,
                "fields": clock_fields,
                "missing_enriched_trace_fields": missing_clock,
            },
            ROUTES_ROTOR.name: {
                "A_digit_by_event": rotor_a,
                "fields": rotor_fields,
                "missing_enriched_trace_fields": missing_rotor,
            },
        },
        "different_local_digits_out_of_432": differing,
        "K_hundreds": target_hundreds,
        "historical_four_cursor_output": literal,
        "weight_pairs_0_to_9_returning_K": weight_hits,
        "three_additive_chart_outputs": chart_outputs,
        "positive_theorem": (
            "cada CSV define una dinámica finita reproducible y fija su propio primer dígito de conteo por evento"
        ),
        "no_go_theorem": (
            "las dos dinámicas son incompatibles y ninguna determina siquiera los cientos de K; además omiten "
            "identidad de traza, clase 120(1+3j), signo bidireccional y predicado de frontera, por lo que no identifican K"
        ),
        "minimal_missing_datum": (
            "un registro enriquecido ejecutable con estado inicial, dinámica elegida, identificador y extremos de cada traza, "
            "clase (r,j), signo inducido por la orientación TRIT, predicado corona/interior, fase y regla de agregación"
        ),
    }


def source_hashes() -> dict[str, str]:
    paths = (
        CURRENT,
        N69_STUTTER,
        N71_EDGES,
        N72_BRANCHES,
        N72_PROFILE,
        N74_RETURN,
        N33_INDEX,
        N38_DATA,
        ORIENTATION_SOURCE,
        ROUTES_CLOCK,
        ROUTES_ROTOR,
        ROUTES_CLOCK_SOURCE,
        ROUTES_ROTOR_SOURCE,
        HISTORICAL_TEXT,
        PRIOR_AUDIT,
        TRANSDUCTOR_RESULT,
    )
    return {str(path.relative_to(ROOT)): sha256(path) for path in paths}


def build_result() -> dict[str, object]:
    current = json.loads(CURRENT.read_text(encoding="utf-8"))
    require(current["revision"] == "2026-07-22.2", "revisión CURRENT distinta de 2026-07-22.2")

    branch = branch_and_diamond_audit()
    n33 = n33_audit()
    recognition = k_recognition_audit(branch["saturated_mirror"]["descriptor_12"])
    residual_transport = residual_transport_audit(
        recognition["rombo_descriptor_12"],
        recognition["retrospective_descriptor_18"],
    )
    recurrence = recurrence_negative_control()
    routes = routes_no_go_audit()

    return {
        "schema": "HMT.rombo-nueve-fases-K.v1",
        "current_revision": current["revision"],
        "overall_status": "PASS_CIERRE_FINITO_Y_FRONTERA_EXACTA",
        "provenance_status": {
            "mirror_gates_and_nine_phase_return": "ARQUITECTURA_AUTORAL_PREEXISTENTE",
            "unique_020022_preimage": "RESULTADO_RECUPERADO",
            "oriented_vacancy_reader": "FORMALIZACION_NUEVA",
            "exact_18_trit_identity_and_no_go": "CERTIFICADO_NUEVO",
            "residual_transport_and_two_forced_triads": "CERTIFICADO_NUEVO",
        },
        "probative_layers": {
            "EXACTO_INTERNO": [
                "rombo 5->2->1",
                "transferencia (683,171)->(684,170)",
                "defectos 000111/000222",
                "censo y preimagen única N33",
                "colapso del pseudocódigo histórico",
                "incompatibilidad de las dos tablas 108",
                "los 18 trits fuerzan exactamente K1=234 y K2=543",
                "el bloque 211201 transporta el resto de K1 a K2 sin fijar todavía K3",
            ],
            "RELATIVO_A_PRIMITIVAS": [
                "ablación de los stutters posteriores sobre los cilindros N38 condicionados",
            ],
            "RECONOCIMIENTO_EXTERNO": [
                "descriptor retrospectivo de 18 trits = prefijo ternario de la concatenación base-1000 de K",
            ],
            "PROGRAMA_ABIERTO": [
                "probar que el lector de vacancia orientada es canónico y no una elección de representación",
                "construir el registro enriquecido que prolongue el lector a los doce bloques",
                "realizar semilla -> registro 108 -> agregador -> U12/K sin introducir U12 o K",
            ],
        },
        "branch_diamond": branch,
        "N33_243_catalogue": n33,
        "K_recognition": recognition,
        "residual_transport_729_to_1000": residual_transport,
        "later_stutters_ablation": recurrence,
        "CT108_routes": routes,
        "dictum": (
            "El rombo de t=20 contiene una identidad finita genuina de 18 trits con K. Esos 18 trits fuerzan "
            "exactamente las dos primeras tríadas 234|543, y el bloque de retorno 211201 transporta el estado "
            "residual de la primera a la segunda. La información vive en la orientación especular y la memoria "
            "de fase. Las rutas cardinales publicadas no bastan para "
            "prolongarla: la pieza mínima que falta no es otro valor objetivo, sino la tabla/generador tipado de trazas "
            "bidireccionales del registro enriquecido."
        ),
        "source_sha256": source_hashes(),
    }


def main() -> None:
    result = build_result()
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if "--write-certificate" in sys.argv:
        CERTIFICATE.write_text(rendered, encoding="utf-8")
    if "--check-certificate" in sys.argv:
        require(CERTIFICATE.exists(), f"no existe {CERTIFICATE}")
        stored = CERTIFICATE.read_text(encoding="utf-8")
        require(stored == rendered, "el certificado almacenado no coincide byte a byte")
    sys.stdout.write(rendered)


if __name__ == "__main__":
    main()
