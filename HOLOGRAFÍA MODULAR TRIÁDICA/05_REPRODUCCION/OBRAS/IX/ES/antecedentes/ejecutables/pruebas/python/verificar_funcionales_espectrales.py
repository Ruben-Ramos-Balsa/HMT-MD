#!/usr/bin/env python3
"""Verificación autocontenida de los funcionales espectrales triádicos.

El programa reconstruye los coeficientes de Laurent de las tres clases
residuales módulo tres, recupera las constantes de Stieltjes de orden cero a
seis y evalúa las especializaciones descritas en el manuscrito.  El producto
local de los primos gemelos se encierra en un intervalo dirigido: el producto
finito se calcula con ``Decimal`` y redondeo hacia fuera, mientras que la cola
se acota mediante un producto telescópico sobre todos los enteros.

Dependencias: biblioteca estándar y mpmath.  No se leen datos externos ni se
emplean valores de las constantes para seleccionar reglas o parámetros.
"""

from __future__ import annotations

import json
import math
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from pathlib import Path
import sys

# Dependencia vendorizada para reproducción bajo ``python -I -S``.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mpmath as mp


OUT = Path(__file__).resolve().parents[2] / "certificados" / "funcionales_espectrales.json"
DECIMAL_PRECISION = 100
TWIN_PRODUCT_LIMIT = 2_000_000
TWIN_COUNT_LIMIT = 1_000_000


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"Fallo en funcionales espectrales: {message}")


def mstr(value: mp.mpf | mp.mpc, digits: int = 75) -> str:
    """Representación decimal estable para el certificado."""

    return mp.nstr(value, digits)


def sieve(limit: int) -> bytearray:
    """Criba de Eratóstenes determinista en memoria compacta."""

    prime = bytearray(b"\x01") * (limit + 1)
    prime[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if prime[p]:
            start = p * p
            prime[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
    return prime


def laurent_coefficient(a: mp.mpf, order: int) -> mp.mpf:
    r"""Coeficiente de z^order en 3^(-1-z) zeta(1+z,a)-1/(3z)."""

    log3 = mp.log(3)
    coefficient = (-log3) ** (order + 1) / mp.factorial(order + 1)
    for k in range(order + 1):
        hurwitz_coefficient = (-1) ** k * mp.stieltjes(k, a) / mp.factorial(k)
        coefficient += (
            hurwitz_coefficient
            * (-log3) ** (order - k)
            / mp.factorial(order - k)
        )
    return coefficient / 3


def laurent_channels() -> dict[str, object]:
    parameters = {
        "divisible_by_three": mp.mpf(1),
        "residue_one": mp.mpf(1) / 3,
        "residue_two": mp.mpf(2) / 3,
    }
    coefficients = {
        name: [laurent_coefficient(a, n) for n in range(7)]
        for name, a in parameters.items()
    }

    reconstructed: list[dict[str, object]] = []
    maximum_error = mp.mpf(0)
    for n in range(7):
        aggregate = mp.fsum(coefficients[name][n] for name in parameters)
        gamma_reconstructed = (-1) ** n * mp.factorial(n) * aggregate
        gamma_direct = mp.stieltjes(n)
        error = abs(gamma_reconstructed - gamma_direct)
        maximum_error = max(maximum_error, error)
        oriented_derivative = mp.factorial(n) * (
            coefficients["residue_one"][n] - coefficients["residue_two"][n]
        )
        reconstructed.append(
            {
                "order": n,
                "stieltjes_direct": mstr(gamma_direct),
                "stieltjes_from_three_channels": mstr(gamma_reconstructed),
                "absolute_error": mstr(error, 12),
                "L_derivative_chi_minus3": mstr(oriented_derivative),
            }
        )

    c0 = coefficients["divisible_by_three"][0]
    c1 = coefficients["residue_one"][0]
    c2 = coefficients["residue_two"][0]
    gamma = mp.euler
    log3 = mp.log(3)
    l_one = mp.pi / (3 * mp.sqrt(3))
    finite_part_errors = {
        "Euler_Mascheroni": abs(c0 + c1 + c2 - gamma),
        "L_one_chi_minus3": abs(c1 - c2 - l_one),
        "log_three": abs(c1 + c2 - 2 * c0 - log3),
    }
    require(maximum_error < mp.mpf("1e-85"), "reconstrucción de Stieltjes")
    require(max(finite_part_errors.values()) < mp.mpf("1e-90"), "partes finitas")

    return {
        "common_residue_at_s_equals_one": "1/3",
        "coefficients_c_r_n": {
            name: [mstr(value) for value in values]
            for name, values in coefficients.items()
        },
        "stieltjes_orders_zero_through_six": reconstructed,
        "finite_parts": {
            "C0": mstr(c0),
            "C1": mstr(c1),
            "C2": mstr(c2),
            "Euler_Mascheroni": mstr(gamma),
            "L_one_chi_minus3": mstr(c1 - c2),
            "log_three": mstr(c1 + c2 - 2 * c0),
        },
        "maximum_stieltjes_reconstruction_error": mstr(maximum_error, 12),
        "finite_part_identity_errors": {
            key: mstr(value, 12) for key, value in finite_part_errors.items()
        },
    }


def apery_interval(terms: int = 1_000_000) -> dict[str, object]:
    """Intervalo por sumas parciales y el criterio integral."""

    partial = mp.fsum(mp.mpf(1) / (n**3) for n in range(1, terms + 1))
    lower = partial + mp.mpf(1) / (2 * (terms + 1) ** 2)
    upper = partial + mp.mpf(1) / (2 * terms**2)
    value = mp.zeta(3)
    require(lower < value < upper, "intervalo racional de Apéry")
    return {
        "terms": terms,
        "lower": mstr(lower),
        "value": mstr(value),
        "upper": mstr(upper),
    }


def special_values(channels: dict[str, object]) -> dict[str, object]:
    glaisher_spectral = mp.exp(mp.mpf(1) / 12 - mp.diff(mp.zeta, -1))
    glaisher_direct = mp.glaisher
    glaisher_error = abs(glaisher_spectral - glaisher_direct)
    require(glaisher_error < mp.mpf("1e-90"), "Glaisher--Kinkelin")

    finite = channels["finite_parts"]
    l_one = mp.mpf(str(finite["L_one_chi_minus3"]))
    # El coeficiente orientado de orden uno es L'(1,chi_-3).
    c1_one = mp.mpf(channels["coefficients_c_r_n"]["residue_one"][1])
    c2_one = mp.mpf(channels["coefficients_c_r_n"]["residue_two"][1])
    l_prime = c1_one - c2_one
    gamma_field = mp.euler + l_prime / l_one

    # Control independiente por diferencia simétrica de las zetas de Hurwitz.
    h = mp.mpf("1e-25")

    def l_function(s: mp.mpf) -> mp.mpf:
        return mp.power(3, -s) * (
            mp.zeta(s, mp.mpf(1) / 3) - mp.zeta(s, mp.mpf(2) / 3)
        )

    l_prime_symmetric = (l_function(1 + h) - l_function(1 - h)) / (2 * h)
    independent_error = abs(l_prime - l_prime_symmetric)
    require(independent_error < mp.mpf("1e-45"), "derivada de L en uno")

    return {
        "Apery_zeta_three": apery_interval(),
        "Glaisher_Kinkelin": {
            "from_zeta_derivative": mstr(glaisher_spectral),
            "direct_mpmath_control": mstr(glaisher_direct),
            "absolute_error": mstr(glaisher_error, 12),
        },
        "Euler_Kronecker_Eisenstein_field": {
            "L_one_chi_minus3": mstr(l_one),
            "L_prime_one_chi_minus3": mstr(l_prime),
            "symmetric_difference_control": mstr(l_prime_symmetric),
            "control_error": mstr(independent_error, 12),
            "gamma_field": mstr(gamma_field),
        },
    }


def outward_decimal(value: Decimal, places: int, rounding: str) -> str:
    quantum = Decimal(1).scaleb(-places)
    with localcontext() as context:
        context.prec = DECIMAL_PRECISION
        context.rounding = rounding
        return format(value.quantize(quantum), "f")


def twin_prime_product() -> dict[str, object]:
    primes = sieve(TWIN_PRODUCT_LIMIT)
    selected = [p for p in range(3, TWIN_PRODUCT_LIMIT + 1) if primes[p]]

    with localcontext() as context:
        context.prec = DECIMAL_PRECISION
        context.rounding = ROUND_FLOOR
        product_lower = Decimal(1)
        for p in selected:
            factor = Decimal(p * (p - 2)) / Decimal((p - 1) ** 2)
            product_lower *= factor
        infinite_lower = product_lower * Decimal(TWIN_PRODUCT_LIMIT - 1) / Decimal(
            TWIN_PRODUCT_LIMIT
        )

    with localcontext() as context:
        context.prec = DECIMAL_PRECISION
        context.rounding = ROUND_CEILING
        product_upper = Decimal(1)
        for p in selected:
            factor = Decimal(p * (p - 2)) / Decimal((p - 1) ** 2)
            product_upper *= factor

    lower_text = outward_decimal(infinite_lower, 55, ROUND_FLOOR)
    upper_text = outward_decimal(product_upper, 55, ROUND_CEILING)
    require(Decimal(lower_text) < Decimal(upper_text), "orientación del intervalo")

    twin_count = sum(
        1
        for p in range(3, TWIN_COUNT_LIMIT - 1)
        if primes[p] and primes[p + 2]
    )
    require(twin_count == 8169, "censo de pares de primos gemelos hasta un millón")

    return {
        "finite_product_prime_limit": TWIN_PRODUCT_LIMIT,
        "number_of_odd_primes_in_finite_product": len(selected),
        "tail_inequality": "(X-1)/X <= product_{p>X}(1-1/(p-1)^2) < 1",
        "directed_interval": {"lower": lower_text, "upper": upper_text},
        "twin_pair_count_limit": TWIN_COUNT_LIMIT,
        "twin_pair_count": twin_count,
        "infinite_twin_prime_conjecture_used": False,
    }


def main() -> None:
    mp.mp.dps = 100
    channels = laurent_channels()
    result = {
        "schema": "hmt.funcionales_espectrales",
        "status": "PASS",
        "dependencies": {"python_standard_library": True, "mpmath": mp.__version__},
        "selection_policy": "Las reglas se fijan antes de evaluar las constantes.",
        "laurent_channels": channels,
        "special_values": special_values(channels),
        "twin_prime_local_product": twin_prime_product(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    print("PASS_FUNCIONALES_ESPECTRALES")


if __name__ == "__main__":
    main()
