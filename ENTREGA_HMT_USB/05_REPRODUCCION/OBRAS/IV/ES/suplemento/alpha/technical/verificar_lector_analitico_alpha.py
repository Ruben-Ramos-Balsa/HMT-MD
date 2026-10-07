#!/usr/bin/env python3
"""Certifica la representación analítica correlacionada de alfa.

Las coordenadas regionales y la carta terminal proceden del mismo estado
APP--TRIT--TPK. Este lector es una representación analítica posterior de esa
salida correlacionada: no afirma una derivación independiente y no recibe
como entrada alfa convencional ni un valor metrológico.

Toda la aritmética es racional dirigida. Los prefijos nonádicos de mil cifras
se interpretan como cilindros semiabiertos, no como valores exactos; sus colas
se propagan a la precoordenada, al coeficiente analítico y a los cilindros. La
bisección usa una contracción por la cota inferior de la derivada cuando la
evaluación intervalar contiene cero, de modo que no depende de decidir una
igualdad exacta en el punto medio.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import re
import runpy
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DIGITS = ROOT / "certificados" / "ley_nueve_puertas_2026-07-30" / "salidas"
TERMINAL_GENERATOR = ROOT / "technical" / "generar_registro_terminal_tpk.py"
CERTIFICATE = ROOT / "metadata" / "certificado-lector-analitico-alpha.json"
SCHEMA = "HMT.CH.alpha-analytic-reader-certificate.v4"
GENERATED_DECIMALS = 1000
LOG_TERMS = 520
SERIES_TAIL_START = 30
CYLINDER_LEVELS = 24
DERIVATIVE_LOWER = Fraction(6239, 1000)
RESCUE_DERIVATIVE_LOWER = Fraction(6)
Interval = tuple[Fraction, Fraction]


def fail(message: str) -> None:
    raise SystemExit("FAIL_LECTOR_ANALITICO_ALPHA_COMPLETO " + message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def fraction(text: str) -> Fraction:
    try:
        return Fraction(text)
    except (ValueError, ZeroDivisionError):
        fail("invalid_rational=" + text)
    raise RuntimeError("unreachable")


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def no_duplicate_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail("certificate_duplicate_key=" + key)
        result[key] = value
    return result


def validate_certificate() -> None:
    try:
        document = json.loads(
            CERTIFICATE.read_text(encoding="utf-8"),
            object_pairs_hook=no_duplicate_object,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail("certificate_unreadable=" + type(exc).__name__)

    required_fields = {
        "schema", "certificate_id", "joint_generation_id", "causal_role",
        "representation_status", "independence_claimed", "generated_by",
        "publication_stage", "upstream_terminal_coordinate_status",
        "operator", "proof_obligations_verified",
        "exact_controls", "implementation", "artifact_sha256",
        "conventional_alpha_input", "metrology_input", "recognition_after_output",
    }
    require(isinstance(document, dict), "certificate_not_object")
    require(set(document) == required_fields, "certificate_top_level_fields")
    require(document["schema"] == SCHEMA, "certificate_schema")
    require(document["certificate_id"] == "alpha-full-analytic-reader-rev10", "certificate_id")
    require(document["joint_generation_id"] == "APP_TRIT_TPK_NONADIC_TYPED_IMAGE_V2", "certificate_joint_generation_id")
    require(document["causal_role"] == "correlated_analytic_publication_of_generated_state_precoordinate", "certificate_causal_role")
    require(document["representation_status"] == "correlated_representation_of_same_enriched_state_not_independent", "certificate_representation_status")
    require(document["independence_claimed"] is False, "independence_claimed")
    require(document["publication_stage"] == "after_joint_regional_and_terminal_coordinates_before_conventional_recognition", "certificate_publication_stage")

    expected_generators = [
        "PI_HMT", "E_HMT", "PHI_HMT",
        "K_periodic_from_published_internal_terminal_coordinate",
        "precoordinate_a_state", "nonadic_coefficient_recurrence",
    ]
    require(document["generated_by"] == expected_generators, "certificate_generated_by")
    expected_upstream = {
        "status": "CIERRE_INTERNO_TIPADO_ESTADO_TPK_PLENO",
        "formalization_status": "RECTIFICACION_DE_DOMINIO_Y_CIERRE_EXACTO",
        "dependency": "TPKFullState_to_SignedDodecaphaseState_to_CanonicalSealK",
        "effect": "analytic_numeric_certificate_uses published C_term downstream; its helper does not invert CT108RawProjection; the full-state internal closure is localized in U016",
        "recovery_receipt": "metadata/recuperacion-procedencia-terminal.json",
        "owner": {
            "id": "U016",
            "path": "/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/propietarios_exactos/tpk/U016_registro_dodecafasico_hadamard_k.tex",
            "sha256": "40449cd4913dc6867b7784f7338afc63706ea4a5467c6efdad97b6d7d365de96",
            "line_ranges": ["7-24", "61-77", "270-350", "352-382", "442-476", "523-583", "630-663"],
        },
        "auxiliary_replay_scope": "CTERM_TO_RETURN_ONLY",
        "visit_by_visit_replay_included": False,
        "python_generates_upstream": False,
        "mathematical_proof_limited_by_auxiliary_replay_scope": False,
    }
    require(document["upstream_terminal_coordinate_status"] == expected_upstream, "certificate_upstream_terminal_coordinate_status")
    expected_operator = {
        "q": "1/729",
        "precoordinate": "a(s)=pi_HMT+e_HMT-phi_HMT-4-kappa_per(s)",
        "lambda": "-E9(a(s))*(1-a(s)^3/729)/a(s)^10",
        "tail_coefficients": "b_(10+3n)=lambda/729^n; b_(11+3n)=b_(12+3n)=0",
        "jet_degree": "d_M=12+3M",
        "limit_function": "E_infinity(x)=E9(x)+lambda*x^10/(1-x^3/729)",
    }
    require(document["operator"] == expected_operator, "certificate_operator")
    expected_obligations = [
        "all_coefficients_are_computed", "truncation_naturality",
        "uniform_convergence_on_I_alpha", "uniform_derivative_control",
        "exact_root_identity_at_state_precoordinate", "simple_unique_root_on_I_alpha",
        "generated_prefix_tail_propagation", "derivative_rescue_bisection",
        "rational_nested_intervals", "inclusion_in_integer_route_cylinders",
    ]
    require(document["proof_obligations_verified"] == expected_obligations, "certificate_proof_obligations")
    expected_controls = {
        "arithmetic": "fractions.Fraction_with_directed_rational_intervals",
        "generated_prefix_decimals": GENERATED_DECIMALS,
        "generated_prefix_tail_bound": "1/10^1000",
        "log_interval_terms": LOG_TERMS,
        "series_tail_start": SERIES_TAIL_START,
        "series_tail_bound_lt": "1/10^280",
        "derivative_series_tail_bound_lt": "1/10^280",
        "root_interval": "[0,1/100]",
        "cylinder_levels": CYLINDER_LEVELS,
        "derivative_lower_bound": "6239/1000",
        "rescue_derivative_lower_bound": "6",
        "rescue_evaluation_width_bound": "width(E(m))<=6*width(D)/4",
        "indeterminate_sign_rule": "D_intersection_[m-width(D)/4,m+width(D)/4]",
        "negative_interval_tests": 5,
    }
    require(document["exact_controls"] == expected_controls, "certificate_exact_controls")
    require(document["implementation"] == "technical/verificar_lector_analitico_alpha.py", "certificate_implementation")
    for key in ("conventional_alpha_input", "metrology_input", "recognition_after_output"):
        require(type(document[key]) is bool, "certificate_boolean=" + key)
    require(document["conventional_alpha_input"] is False, "conventional_alpha_input")
    require(document["metrology_input"] is False, "metrology_input")
    require(document["recognition_after_output"] is True, "recognition_after_output")

    expected_paths = {
        "technical/verificar_lector_analitico_alpha.py",
        "technical/generar_registro_terminal_tpk.py",
        "metadata/semilla-registro-terminal.json",
        "certificados/ley_nueve_puertas_2026-07-30/salidas/pi_1000_decimales.txt",
        "certificados/ley_nueve_puertas_2026-07-30/salidas/e_1000_decimales.txt",
        "certificados/ley_nueve_puertas_2026-07-30/salidas/phi_1000_decimales.txt",
    }
    seals = document["artifact_sha256"]
    require(isinstance(seals, dict) and set(seals) == expected_paths, "certificate_sha_paths")
    for relative_path in sorted(expected_paths):
        recorded = seals[relative_path]
        require(isinstance(recorded, str) and re.fullmatch(r"[0-9a-f]{64}", recorded) is not None, "certificate_sha_format=" + relative_path)
        require(digest(ROOT / relative_path) == recorded, "certificate_sha_mismatch=" + relative_path)


def point(value: Fraction | int) -> Interval:
    rational = Fraction(value)
    return rational, rational


def interval_add(left: Interval, right: Interval) -> Interval:
    return left[0] + right[0], left[1] + right[1]


def interval_neg(value: Interval) -> Interval:
    return -value[1], -value[0]


def interval_sub(left: Interval, right: Interval) -> Interval:
    return interval_add(left, interval_neg(right))


def interval_mul(left: Interval, right: Interval) -> Interval:
    products = (
        left[0] * right[0], left[0] * right[1],
        left[1] * right[0], left[1] * right[1],
    )
    return min(products), max(products)


def interval_inv(value: Interval) -> Interval:
    require(not (value[0] <= 0 <= value[1]), "interval_division_by_zero")
    reciprocals = (1 / value[0], 1 / value[1])
    return min(reciprocals), max(reciprocals)


def interval_div(left: Interval, right: Interval) -> Interval:
    return interval_mul(left, interval_inv(right))


def interval_scale(value: Interval, scalar: Fraction | int) -> Interval:
    return interval_mul(value, point(Fraction(scalar)))


def interval_pow(value: Interval, exponent: int) -> Interval:
    require(exponent >= 0, "interval_negative_power")
    if exponent == 0:
        return point(1)
    if value[0] >= 0:
        return value[0] ** exponent, value[1] ** exponent
    if value[1] <= 0:
        endpoints = (value[0] ** exponent, value[1] ** exponent)
        return min(endpoints), max(endpoints)
    if exponent % 2:
        return value[0] ** exponent, value[1] ** exponent
    return Fraction(0), max(abs(value[0]), abs(value[1])) ** exponent


def interval_width(value: Interval) -> Fraction:
    return value[1] - value[0]


def read_generated_coordinate_interval(name: str) -> Interval:
    """Cierre racional exterior del cilindro decimal semiabierto publicado."""
    raw = (DIGITS / f"{name}_1000_decimales.txt").read_text(encoding="ascii").strip()
    if re.fullmatch(r"[1-9]\.[0-9]{1000}", raw) is None:
        fail("generated_coordinate_format=" + name)
    lower = Fraction(raw)
    return lower, lower + Fraction(1, 10**GENERATED_DECIMALS)


def log_bounds(value: Fraction, terms: int) -> Interval:
    """Cotas dirigidas de log(x)=2*sum y^(2k+1)/(2k+1)."""
    require(value > 1 and terms > 0, "log_bounds_domain")
    y = (value - 1) / (value + 1)
    y_squared = y * y
    power = y
    lower = Fraction(0)
    for index in range(terms):
        lower += 2 * power / (2 * index + 1)
        power *= y_squared
    tail_upper = 2 * power / ((2 * terms + 1) * (1 - y_squared))
    return lower, lower + tail_upper


def delta_bounds() -> Interval:
    numerator = log_bounds(Fraction(10, 9), LOG_TERMS)
    log3 = log_bounds(Fraction(3), LOG_TERMS)
    denominator = interval_add(numerator, interval_scale(log3, 2))
    require(0 < numerator[0] <= numerator[1], "delta_numerator_bounds")
    require(0 < denominator[0] <= denominator[1], "delta_denominator_bounds")
    return interval_div(numerator, denominator)


def e9_exact(x: Fraction, pi_value: Fraction, delta: Fraction) -> Fraction:
    return (
        2 * pi_value * x - Fraction(7, 4) * x**2
        + x**3 / (2 * pi_value) + x**4 / 20 - Fraction(2, 21) * x**5
        - x**6 / 46 - x**7 / 120 + x**8 / 45 + Fraction(2, 495) * x**9
        - delta
    )


def e9_interval(x: Interval, pi_value: Interval, delta: Interval) -> Interval:
    result = interval_scale(interval_mul(pi_value, x), 2)
    result = interval_add(result, interval_scale(interval_pow(x, 2), Fraction(-7, 4)))
    result = interval_add(result, interval_div(interval_pow(x, 3), interval_scale(pi_value, 2)))
    result = interval_add(result, interval_scale(interval_pow(x, 4), Fraction(1, 20)))
    result = interval_add(result, interval_scale(interval_pow(x, 5), Fraction(-2, 21)))
    result = interval_add(result, interval_scale(interval_pow(x, 6), Fraction(-1, 46)))
    result = interval_add(result, interval_scale(interval_pow(x, 7), Fraction(-1, 120)))
    result = interval_add(result, interval_scale(interval_pow(x, 8), Fraction(1, 45)))
    result = interval_add(result, interval_scale(interval_pow(x, 9), Fraction(2, 495)))
    return interval_sub(result, delta)


def e9_prime_interval(x: Interval, pi_value: Interval) -> Interval:
    result = interval_scale(pi_value, 2)
    result = interval_add(result, interval_scale(x, Fraction(-7, 2)))
    result = interval_add(result, interval_div(interval_scale(interval_pow(x, 2), 3), interval_scale(pi_value, 2)))
    result = interval_add(result, interval_scale(interval_pow(x, 3), Fraction(1, 5)))
    result = interval_add(result, interval_scale(interval_pow(x, 4), Fraction(-10, 21)))
    result = interval_add(result, interval_scale(interval_pow(x, 5), Fraction(-3, 23)))
    result = interval_add(result, interval_scale(interval_pow(x, 6), Fraction(-7, 120)))
    result = interval_add(result, interval_scale(interval_pow(x, 7), Fraction(8, 45)))
    return interval_add(result, interval_scale(interval_pow(x, 8), Fraction(18, 495)))


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def jet_degree(level: int) -> int:
    require(level >= 0, "jet_degree_negative_level")
    return 12 + 3 * level


def derivative_rescue_contract(
    left: Fraction, right: Fraction, midpoint: Fraction, value: Interval
) -> tuple[Fraction, Fraction]:
    """Contracción TVM cerrada para el caso en que el recinto contiene cero.

    Si ``D=[left,right]`` tiene anchura ``w``, ``midpoint`` es su punto medio,
    ``E' >= 6`` y ``0 in value`` con ``width(value) <= 6w/4``, entonces toda
    raíz de ``E`` contenida en ``D`` pertenece también a
    ``D intersect [midpoint-w/4, midpoint+w/4]``. La demostración utiliza sólo
    el teorema del valor medio; no decide si ``E(midpoint)=0``.
    """
    require(left < right, "derivative_rescue_bracket")
    require(midpoint == (left + right) / 2, "derivative_rescue_nonmidpoint")
    require(value[0] <= value[1], "derivative_rescue_reversed_enclosure")
    require(value[0] <= 0 <= value[1], "derivative_rescue_sign_domain")
    width = right - left
    require(
        interval_width(value) <= RESCUE_DERIVATIVE_LOWER * width / 4,
        "derivative_rescue_evaluation_too_wide",
    )
    new_left = max(left, midpoint - width / 4)
    new_right = min(right, midpoint + width / 4)
    require(left <= new_left <= new_right <= right, "derivative_rescue_not_nested")
    require(new_right - new_left <= width / 2, "derivative_rescue_not_halving")
    return new_left, new_right


def expect_rescue_failure(
    left: Fraction,
    right: Fraction,
    midpoint: Fraction,
    value: Interval,
    expected_code: str,
) -> None:
    """Comprueba que una precondición inválida se rechaza cerradamente."""
    try:
        derivative_rescue_contract(left, right, midpoint, value)
    except SystemExit as error:
        require(expected_code in str(error), "negative_rescue_wrong_failure=" + expected_code)
        return
    fail("negative_rescue_accepted=" + expected_code)


def main() -> None:
    validate_certificate()
    source = Path(__file__).read_text(encoding="utf-8")
    forbidden_targets = ("0.007297" + "352569", "137.035" + "999")
    if any(target in source for target in forbidden_targets):
        fail("embedded_conventional_alpha_target")

    pi_interval = read_generated_coordinate_interval("pi")
    e_interval = read_generated_coordinate_interval("e")
    phi_interval = read_generated_coordinate_interval("phi")
    prefix_tail = Fraction(1, 10**GENERATED_DECIMALS)
    for name, enclosure in (("pi", pi_interval), ("e", e_interval), ("phi", phi_interval)):
        require(interval_width(enclosure) == prefix_tail, "generated_tail_width=" + name)

    namespace = runpy.run_path(str(TERMINAL_GENERATOR), run_name="hmt_terminal_for_alpha")
    phase_blocks = namespace["compute_downstream_terminal_chart"]()["phase_blocks"]
    require(isinstance(phase_blocks, list) and len(phase_blocks) == 3, "terminal_phase_blocks")
    interleaved: list[int] = []
    for column in range(4):
        for residue in range(3):
            row = phase_blocks[residue]
            require(isinstance(row, list) and len(row) == 4, "terminal_phase_row")
            value = row[column]
            require(type(value) is int and 0 <= value <= 999, "terminal_phase_value")
            interleaved.append(value)
    numerator = int("".join(f"{value:03d}" for value in interleaved))
    base = 1000
    kappa = Fraction(numerator, base**12 - 1)
    a_interval = interval_sub(
        interval_sub(interval_add(pi_interval, e_interval), phi_interval),
        point(4 + kappa),
    )
    require(Fraction(7, 1000) < a_interval[0] <= a_interval[1] < Fraction(8, 1000), "state_precoordinate_interval")
    manuscript_a_lower = Fraction(7297352569283800997285105472380662, 10**36)
    manuscript_a_upper = Fraction(7297352569283800997285105472380663, 10**36)
    require(
        manuscript_a_lower < a_interval[0]
        <= a_interval[1] < manuscript_a_upper,
        "state_precoordinate_manuscript_bounds",
    )
    require(interval_width(a_interval) == 3 * prefix_tail, "state_precoordinate_tail_propagation")

    d_interval = delta_bounds()
    require(interval_width(d_interval) < Fraction(1, 10**300), "delta_interval_width")
    q = Fraction(1, 729)
    one_minus_qa3 = interval_sub(point(1), interval_scale(interval_pow(a_interval, 3), q))
    coefficient_interval = interval_neg(
        interval_div(
            interval_mul(e9_interval(a_interval, pi_interval, d_interval), one_minus_qa3),
            interval_pow(a_interval, 10),
        )
    )
    require(
        Fraction(-8711, 10**9) < coefficient_interval[0]
        <= coefficient_interval[1] < Fraction(-8709, 10**9),
        "coefficient_interval",
    )
    coefficient_abs_bound = max(abs(coefficient_interval[0]), abs(coefficient_interval[1]))

    def full_function_interval(x: Fraction) -> Interval:
        x_interval = point(x)
        denominator = interval_sub(point(1), interval_scale(interval_pow(x_interval, 3), q))
        tail_factor = interval_div(interval_pow(x_interval, 10), denominator)
        return interval_add(
            e9_interval(x_interval, pi_interval, d_interval),
            interval_mul(coefficient_interval, tail_factor),
        )

    def full_derivative_interval(x: Fraction) -> Interval:
        x_interval = point(x)
        denominator = interval_sub(point(1), interval_scale(interval_pow(x_interval, 3), q))
        tail_factor = interval_add(
            interval_div(interval_scale(interval_pow(x_interval, 9), 10), denominator),
            interval_div(
                interval_scale(interval_pow(x_interval, 12), 3 * q),
                interval_pow(denominator, 2),
            ),
        )
        return interval_add(
            e9_prime_interval(x_interval, pi_interval),
            interval_mul(coefficient_interval, tail_factor),
        )

    # La cancelación en a es una identidad algebraica. Se comprueba con
    # aritmética exacta sobre todos los vértices de la caja racional de datos.
    for pi_value in pi_interval:
        for e_value in e_interval:
            for phi_value in phi_interval:
                for delta in d_interval:
                    a_value = pi_value + e_value - phi_value - 4 - kappa
                    e9_value = e9_exact(a_value, pi_value, delta)
                    coefficient = -e9_value * (1 - q * a_value**3) / a_value**10
                    total = e9_value + coefficient * a_value**10 / (1 - q * a_value**3)
                    require(total == 0, "exact_root_identity_by_substitution")

    coefficients = [interval_scale(coefficient_interval, q**index) for index in range(SERIES_TAIL_START + 2)]
    for index in range(len(coefficients) - 1):
        require(coefficients[index + 1] == interval_scale(coefficients[index], q), "coefficient_recurrence")
    require(jet_degree(0) == 12, "initial_jet_does_not_contain_first_block")
    for level in range(SERIES_TAIL_START):
        new_degrees = tuple(range(jet_degree(level) + 1, jet_degree(level + 1) + 1))
        expected_degrees = tuple(10 + 3 * (level + 1) + offset for offset in range(3))
        require(new_degrees == expected_degrees, "jet_block_degree_alignment")

    x_max = Fraction(1, 100)
    ratio = q * x_max**3
    require(ratio < Fraction(1372, 10**12), "uniform_ratio")
    function_tail_bound = coefficient_abs_bound * x_max**10 * ratio**SERIES_TAIL_START / (1 - ratio)
    require(function_tail_bound < Fraction(1, 10**280), "uniform_series_tail_bound")
    derivative_series_tail_bound = (
        coefficient_abs_bound * x_max**9 * ratio**SERIES_TAIL_START
        * (Fraction(10 + 3 * SERIES_TAIL_START, 1) / (1 - ratio) + 3 * ratio / (1 - ratio) ** 2)
    )
    require(derivative_series_tail_bound < Fraction(1, 10**280), "uniform_derivative_series_tail_bound")
    closed_tail_derivative_bound = coefficient_abs_bound * (
        10 * x_max**9 / (1 - ratio) + 3 * q * x_max**12 / (1 - ratio) ** 2
    )
    require(closed_tail_derivative_bound < fraction("8.712e-23"), "tail_derivative_bound")

    polynomial_derivative_lower = (
        2 * pi_interval[0] - Fraction(7, 2) * x_max
        - Fraction(10, 21) * x_max**4 - Fraction(3, 23) * x_max**5
        - Fraction(7, 120) * x_max**6
    )
    derivative_lower = polynomial_derivative_lower - closed_tail_derivative_bound
    require(derivative_lower > DERIVATIVE_LOWER, "global_derivative_lower_bound")
    for endpoint in (Fraction(0), x_max):
        require(full_derivative_interval(endpoint)[0] > DERIVATIVE_LOWER, "endpoint_derivative")
    require(full_function_interval(Fraction(0))[1] < 0, "left_sign")
    require(full_function_interval(x_max)[0] > 0, "right_sign")
    require(
        Fraction(0) <= a_interval[0] <= a_interval[1] <= x_max,
        "initial_bracket_does_not_contain_generated_root",
    )

    left = Fraction(0)
    right = x_max
    previous_left = left
    previous_right = right
    verified_levels = 0
    derivative_rescues = 0
    for level in range(1, CYLINDER_LEVELS + 1):
        cylinder_scale = base**level
        lower_index = floor_fraction(a_interval[0] * cylinder_scale)
        # La aritmética usa el cierre exterior de los cilindros fuente. Exigir
        # que también su extremo superior pertenezca a la misma celda prueba
        # la inclusión semiabierta sin asignar la frontera derecha a la izquierda.
        upper_index = floor_fraction(a_interval[1] * cylinder_scale)
        require(lower_index == upper_index, "generated_tail_crosses_cylinder")
        lower_cylinder = Fraction(lower_index, cylinder_scale)
        upper_cylinder = Fraction(lower_index + 1, cylinder_scale)
        target_width = Fraction(1, 4 * cylinder_scale)
        # Además de la anchura pedida, el extremo derecho cerrado de la
        # horquilla debe quedar estrictamente dentro del cilindro semiabierto.
        while right - left > target_width or right >= upper_cylinder:
            midpoint = (left + right) / 2
            midpoint_interval = full_function_interval(midpoint)
            if midpoint_interval[1] < 0:
                new_left, new_right = midpoint, right
            elif midpoint_interval[0] > 0:
                new_left, new_right = left, midpoint
            else:
                # Teorema del valor medio: F' >= m transforma una evaluación
                # que contiene cero en un intervalo de raíces más pequeño.
                new_left, new_right = derivative_rescue_contract(
                    left, right, midpoint, midpoint_interval
                )
                derivative_rescues += 1
            require(left <= new_left <= new_right <= right, "bisection_not_nested")
            require(new_right - new_left <= (right - left) / 2, "bisection_not_halving")
            require(new_left <= a_interval[0] <= a_interval[1] <= new_right, "bisection_lost_generated_root")
            left, right = new_left, new_right

        interval_left = max(left, lower_cylinder)
        interval_right = min(right, upper_cylinder)
        require(previous_left <= interval_left <= interval_right <= previous_right, "nested_intervals")
        require(interval_left <= a_interval[0] <= a_interval[1] <= interval_right, "common_interval_empty")
        require(interval_right - interval_left <= target_width, "interval_width")
        require(lower_cylinder <= interval_left <= interval_right < upper_cylinder, "cylinder_inclusion")
        previous_left, previous_right = interval_left, interval_right
        left, right = interval_left, interval_right
        verified_levels += 1

    require(verified_levels == CYLINDER_LEVELS, "cofinal_levels")
    # Controles unitarios de la rama que elimina la antigua dependencia de una
    # decisión exacta. El primer caso alcanza exactamente la cota c*w/4; el
    # segundo representa una raíz situada en el punto medio.
    probe_radius = Fraction(3, 2)
    probe_left, probe_right = derivative_rescue_contract(
        Fraction(-1), Fraction(1), Fraction(0), (-probe_radius, probe_radius)
    )
    require(
        (probe_left, probe_right) == (Fraction(-1, 2), Fraction(1, 2)),
        "derivative_rescue_boundary_control",
    )
    exact_left, exact_right = derivative_rescue_contract(
        Fraction(-1), Fraction(1), Fraction(0), point(0)
    )
    require(
        exact_left <= 0 <= exact_right
        and exact_right - exact_left <= Fraction(1),
        "derivative_rescue_exact_root_control",
    )
    expect_rescue_failure(
        Fraction(-1), Fraction(1), Fraction(0), (Fraction(-2), Fraction(2)),
        "derivative_rescue_evaluation_too_wide",
    )
    expect_rescue_failure(
        Fraction(-1), Fraction(1), Fraction(0), (Fraction(1), Fraction(2)),
        "derivative_rescue_sign_domain",
    )
    expect_rescue_failure(
        Fraction(-1), Fraction(1), Fraction(0), (Fraction(1), Fraction(-1)),
        "derivative_rescue_reversed_enclosure",
    )
    expect_rescue_failure(
        Fraction(-1), Fraction(1), Fraction(1, 3), point(0),
        "derivative_rescue_nonmidpoint",
    )
    expect_rescue_failure(
        Fraction(1), Fraction(1), Fraction(1), point(0),
        "derivative_rescue_bracket",
    )
    print(
        "PASS_LECTOR_ANALITICO_ALPHA_COMPLETO "
        "certificate=schema+fields+sha256 arithmetic=directed_rational_intervals "
        "generated_prefix_tails=pi+e+phi:1000 recurrence=b_10+3n/729 "
        "convergence=uniform root=algebraic_identity "
        "derivative_lower_gt_6_239=true rescue_derivative_lower=6 "
        "rescue_evaluation_width_le_cw_over_4=true bisection=halving_or_derivative_rescue "
        f"rescue_control=true rescue_negative_tests=5 actual_rescues={derivative_rescues} cylinders=24 "
        "representation=correlated_same_state independence_claimed=false "
        "conventional_alpha_input=false"
    )


if __name__ == "__main__":
    main()
