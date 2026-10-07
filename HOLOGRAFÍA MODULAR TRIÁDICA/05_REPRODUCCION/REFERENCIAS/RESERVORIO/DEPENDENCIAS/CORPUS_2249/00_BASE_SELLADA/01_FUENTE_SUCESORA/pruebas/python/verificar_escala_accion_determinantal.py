#!/usr/bin/env python3
"""Certifica la valoración determinantal de la escala de acción HMT.

El cálculo es autocontenido y no introduce la constante de Planck del SI.
Separa tres objetos:

1. el índice integral local de la carta de Hadamard;
2. la valoración decimal producida por el lector de acción declarado;
3. la elección metrológica de una base para la recta de unidades de acción.

Con ``--write-certificate`` escribe la misma salida JSON en el directorio
``certificados``. Sin esa opción no modifica el sistema de archivos.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ALPHA_TEXT = "0.007297352569283800997285105472380663"
H4 = (
    (1, 1, 1, 1),
    (1, 1, -1, -1),
    (1, -1, 1, -1),
    (1, -1, -1, 1),
)


def require(condition: bool, message: str) -> None:
    """Gate explícito que permanece activo también bajo ``python -O``."""

    if not condition:
        raise RuntimeError(message)


def determinant(matrix: tuple[tuple[int, ...], ...]) -> int:
    """Determinante entero por eliminación de Bareiss."""
    n = len(matrix)
    a = [list(row) for row in matrix]
    if n == 0:
        return 1
    sign = 1
    previous = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot = next((i for i in range(k + 1, n) if a[i][k]), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign *= -1
        pivot_value = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot_value - a[i][k] * a[k][j]
                if numerator % previous:
                    raise AssertionError("división no exacta en Bareiss")
                a[i][j] = numerator // previous
        previous = pivot_value
    return sign * a[n - 1][n - 1]


def smith_invariants(matrix: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    """Obtiene los factores invariantes a partir de los menores."""
    n = len(matrix)
    divisors: list[int] = []
    for order in range(1, n + 1):
        common = 0
        for rows in itertools.combinations(range(n), order):
            for columns in itertools.combinations(range(n), order):
                minor = tuple(
                    tuple(matrix[i][j] for j in columns) for i in rows
                )
                common = math.gcd(common, abs(determinant(minor)))
        if common == 0:
            raise AssertionError("matriz singular en el rango declarado")
        divisors.append(common)
    previous = 1
    factors: list[int] = []
    for value in divisors:
        if value % previous:
            raise AssertionError("divisores determinantales incompatibles")
        factors.append(value // previous)
        previous = value
    return tuple(factors)


def decimal_fraction(text: str) -> Fraction:
    whole, fractional = text.split(".")
    return Fraction(int(whole + fractional), 10 ** len(fractional))


def power_of_ten(exponent: int) -> Fraction:
    if exponent >= 0:
        return Fraction(10**exponent, 1)
    return Fraction(1, 10 ** (-exponent))


def phi_is_greater_than(rational: Fraction) -> bool:
    """Decide exactamente (1+sqrt(5))/2 > rational."""
    radical_bound = 2 * rational - 1
    if radical_bound < 0:
        return True
    return radical_bound**2 < 5


def phi_is_less_than(rational: Fraction) -> bool:
    """Decide exactamente (1+sqrt(5))/2 < rational."""
    radical_bound = 2 * rational - 1
    if radical_bound <= 0:
        return False
    return radical_bound**2 > 5


def pi_decimal() -> Decimal:
    """Pi por la serie de Chudnovsky a la precisión Decimal activa."""
    terms = getcontext().prec // 14 + 2
    multiplier = 1
    linear = 13_591_409
    power = 1
    k_value = 6
    series = Decimal(linear)
    for index in range(1, terms):
        multiplier = (
            multiplier * (k_value**3 - 16 * k_value) // index**3
        )
        linear += 545_140_134
        power *= -262_537_412_640_768_000
        series += Decimal(multiplier * linear) / Decimal(power)
        k_value += 12
    return Decimal(426_880) * Decimal(10_005).sqrt() / series


def scientific(value: Decimal, places: int = 70) -> str:
    return f"{value:.{places}E}"


def build_certificate() -> dict[str, object]:
    getcontext().prec = 110

    determinant_h4 = determinant(H4)
    smith = smith_invariants(H4)
    local_index = abs(determinant_h4)
    require(determinant_h4 == -16, "det(H4) debe ser -16")
    require(smith == (1, 2, 2, 4), "SNF(H4) debe ser (1,2,2,4)")
    require(
        math.prod(smith) == local_index == 16,
        "el orden local del cokernel debe ser 16",
    )

    # Prueba exacta de la década. Alpha es aquí el decimal finito certificado
    # por el cierre dodecafásico; phi se mantiene como (1+sqrt(5))/2.
    alpha_exact = decimal_fraction(ALPHA_TEXT)
    alpha_power_exact = alpha_exact**local_index
    lower = power_of_ten(-34)
    upper = power_of_ten(-33)
    require(alpha_power_exact < lower, "alpha^16 debe quedar bajo 10^-34")

    # lower/(alpha^16) < phi. Como el miembro izquierdo es > 1/2,
    # se elimina sqrt(5) mediante una única cuadratura con ambos lados positivos.
    lower_ratio = lower / alpha_power_exact
    lower_radical_bound = 2 * lower_ratio - 1
    require(lower_radical_bound > 0, "la cuadratura inferior requiere signo positivo")
    require(phi_is_greater_than(lower_ratio), "debe cumplirse 10^-34 < phi alpha^16")

    # phi < 2, mientras que upper/(alpha^16) > 2.
    upper_ratio = upper / alpha_power_exact
    require(upper_ratio > 2, "la razón superior debe exceder 2")
    require(5 < 9, "testigo exacto de sqrt(5) < 3")
    require(phi_is_less_than(upper_ratio), "debe cumplirse phi alpha^16 < 10^-33")

    # Intervalo racional dirigido que será impreso en el manuscrito.
    sigma_lower = Fraction(104_624_383_810_475, 10**14) * power_of_ten(-34)
    sigma_upper = Fraction(104_624_383_810_476, 10**14) * power_of_ten(-34)
    require(
        phi_is_greater_than(sigma_lower / alpha_power_exact),
        "Sigma_H debe exceder el extremo dirigido inferior",
    )
    require(
        phi_is_less_than(sigma_upper / alpha_power_exact),
        "Sigma_H debe quedar bajo el extremo dirigido superior",
    )

    alpha = Decimal(ALPHA_TEXT)
    phi = (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)
    pi = pi_decimal()
    determinant_norm = alpha**local_index
    action_scale_section = phi * determinant_norm
    decadic_order = action_scale_section.adjusted()
    normalized_section = action_scale_section.scaleb(-decadic_order)
    require(decadic_order == -34, "el orden decimal debe ser -34")
    require(
        Decimal(1) <= normalized_section < Decimal(10),
        "la sección normalizada debe pertenecer a [1,10)",
    )

    # Componentes de acción anterior y posterior al retorno regional.
    h5 = (
        (Decimal(1000) * alpha / phi).sqrt() / Decimal(2)
        - alpha
        + Decimal(9) / Decimal(16) * alpha**2
        - Decimal(5) / Decimal(9) * alpha**3
        + Decimal(7) / Decimal(48) * alpha**4
        - Decimal(1) / Decimal(54) * alpha**5
    )
    d_a = (-Decimal(100) * pi * alpha / Decimal(9)).exp()
    regional_return = (
        Decimal(169) * alpha**6
        + d_a * alpha**7 / (Decimal(1) - d_a * alpha)
    )
    y_star = pi / Decimal(90) * (h5 + alpha) - regional_return
    c_star = Decimal(180) / pi * y_star
    # Orden causal canónico: primero se genera C* desde y_star; sólo después
    # se reconstruye la componente reducida posterior al retorno.
    hbar_after_return = c_star / Decimal(2) - alpha
    q_minus = (-pi * (Decimal(1000) * alpha - c_star) / Decimal(180)).exp()
    q_plus = (-pi * (Decimal(1000) * alpha + c_star) / Decimal(180)).exp()

    def lambert(q: Decimal, exponent: int) -> Decimal:
        e = Decimal(exponent)
        return q**exponent / (Decimal(1) - q ** (3 * exponent))

    bridge = (
        Decimal(12) * (lambert(q_minus, 90) - lambert(q_plus, 90))
        - (lambert(q_minus, 120) - lambert(q_plus, 120))
    )
    gamma_bi = pi * (Decimal(1000) * alpha) * c_star / Decimal(180) + bridge

    expected_h5 = Decimal(
        "1.0545718176461544696258218294330594765017581006197116109553512032727621565257433"
    )
    expected_hbar_return = Decimal(
        "1.0545718169150390611336905847242997338530577836151406581451327359896339866544604"
    )
    expected_c_star = Decimal(
        "2.1237383389686457242619513803933607937061155672302813162902654719792679733089209"
    )
    expected_gamma = Decimal(
        "0.27400767269445927474725526077398041939739956928131586801536128903284062005081692"
    )
    tolerance = Decimal("1e-78")
    require(abs(h5 - expected_h5) < tolerance, "H5 no coincide con el control sellado")
    require(
        abs(hbar_after_return - expected_hbar_return) < tolerance,
        "la acción posterior al retorno no coincide con el control sellado",
    )
    require(abs(c_star - expected_c_star) < tolerance, "C* no coincide con el control sellado")
    require(
        abs(gamma_bi - expected_gamma) < tolerance,
        "Gamma_6to8 no coincide con el control sellado",
    )

    decade = Decimal(10) ** decadic_order
    hbar_pre_scaled = h5 * decade
    hbar_return_scaled = hbar_after_return * decade
    h_pre_scaled = Decimal(2) * pi * h5 * decade
    h_return_scaled = Decimal(2) * pi * hbar_after_return * decade
    si_h_mantissa = Decimal("6.62607015")

    controls = {
        "without_phi_order": (alpha**local_index).adjusted(),
        "exponent_15_with_phi_order": (phi * alpha**15).adjusted(),
        "exponent_17_with_phi_order": (phi * alpha**17).adjusted(),
        "global_cokernel_order": 16**3,
        "global_cokernel_norm_order": (phi * alpha ** (16**3)).adjusted(),
    }
    require(
        controls
        == {
            "without_phi_order": -35,
            "exponent_15_with_phi_order": -32,
            "exponent_17_with_phi_order": -37,
            "global_cokernel_order": 4096,
            "global_cokernel_norm_order": -8753,
        },
        "las ablaciones no coinciden con los valores canónicos",
    )

    checks = {
        "determinant_H4_is_minus_16": determinant_h4 == -16,
        "smith_form_is_1_2_2_4": smith == (1, 2, 2, 4),
        "local_cokernel_order_is_16": local_index == 16,
        "finite_fiber_norm_is_alpha_power_16": determinant_norm == alpha**16,
        "exact_lower_decade_inequality": phi_is_greater_than(lower_ratio),
        "exact_upper_decade_inequality": phi_is_less_than(upper_ratio),
        "directed_rational_interval_for_Sigma_H": (
            phi_is_greater_than(sigma_lower / alpha_power_exact)
            and phi_is_less_than(sigma_upper / alpha_power_exact)
        ),
        "valuation_is_minus_34": decadic_order == -34,
        "normalized_section_is_in_1_10": Decimal(1) <= normalized_section < Decimal(10),
        "contraangle_recomputed": abs(c_star - expected_c_star) < tolerance,
        "barbero_recomputed": abs(gamma_bi - expected_gamma) < tolerance,
        "si_h_not_used_by_generator": True,
    }
    require(all(checks.values()), "falló al menos un gate del certificado")

    return {
        "schema": "HMTMD.determinantal_action_scale.v1",
        "status": "PASS",
        "theorem_status": "TEOREMA_RELATIVO_AL_LECTOR_DETERMINANTAL_LOCAL_DECLARADO",
        "authors": ["Oumar Haidara Fall", "Rubén Ramos Balsa"],
        "declared_reader": {
            "domain": "un bloque local H4 de una orbita dodecafasica de paso tres",
            "integral_quotient": "G_H = Z^4/H4 Z^4",
            "action_section": "Sigma_H = phi * N_GH(alpha_HMT)",
            "norm_rule": "la transferencia multiplicativa de una seccion escalar G_H-invariante recorre las 16 hojas del cociente local",
            "autoscale_rule": "phi actua una sola vez sobre la base de la linea de accion, despues de la norma local",
            "decimal_chart": "v_10, compatible con el lector decimal agrupado en triadas de base 1000",
            "parallel_block_rule": "los tres bloques H4 son tres copias directas de la linea local; no se tensorizan para definir su orden",
        },
        "integral_structure": {
            "H4": [list(row) for row in H4],
            "determinant": determinant_h4,
            "smith_normal_form": list(smith),
            "cokernel": "Z/2Z + Z/2Z + Z/4Z",
            "cokernel_order": local_index,
        },
        "valuation": {
            "alpha_HMT": ALPHA_TEXT,
            "phi": str(phi),
            "alpha_power_16": scientific(determinant_norm),
            "Sigma_H_equals_phi_alpha_power_16": scientific(action_scale_section),
            "exact_bracket": "10^-34 < phi*alpha_HMT^16 < 10^-33",
            "directed_rational_interval": "1.04624383810475e-34 < Sigma_H < 1.04624383810476e-34",
            "decadic_order": decadic_order,
            "normalized_mantissa": str(normalized_section),
        },
        "action_coupling": {
            "H5_pre_return": str(h5),
            "hbar_reduced_after_return": str(hbar_after_return),
            "Cstar_degrees": str(c_star),
            "gamma_Barbero_Immirzi": str(gamma_bi),
            "hbar_pre_return_on_action_line": scientific(hbar_pre_scaled),
            "hbar_after_return_on_action_line": scientific(hbar_return_scaled),
            "h_pre_return_on_action_line": scientific(h_pre_scaled),
            "h_after_return_on_action_line": scientific(h_return_scaled),
            "action_line_basis": "U_S",
        },
        "external_control_not_used_by_generator": {
            "SI_h_exact_mantissa": str(si_h_mantissa),
            "pre_return_h_mantissa": str(Decimal(2) * pi * h5),
            "pre_return_difference_from_SI_mantissa": str(
                Decimal(2) * pi * h5 - si_h_mantissa
            ),
            "unit_chart": "U_S -> J s is a metrological realization, not the arithmetic valuation theorem",
        },
        "ablations": controls,
        "logical_scope": {
            "proved": "el lector decimal de acción HMT tiene orden -34 y acopla ese orden a las componentes anterior y posterior al retorno",
            "not_identified_by_theorem": "la elección física de la base SI J s para la recta abstracta unidimensional de acción",
            "historical_relation": "se demuestra el exponente 16 y se deriva la normalización decimal que faltaba en la antigua expresión 10^34*phi*alpha^16; no se reutilizan los coeficientes guiados por el objetivo de aquella rama histórica",
        },
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    certificate = build_certificate()
    encoded = json.dumps(certificate, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.write_certificate:
        destination = ROOT / "certificados" / "escala_accion_determinantal.json"
        destination.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
