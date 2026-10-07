#!/usr/bin/env python3
"""Verifica las rotaciones de vacancia y la familia cuadrática dodecafásica.

El programa es autocontenido.  Calcula la densidad de vacancia, recorre de
forma exhaustiva una ventana de cien millones de posiciones y certifica las
separaciones 21/22 y los retornos 6/7.  La parte finita se encierra mediante
la cota de Dirichlet que resulta de la discrepancia menor que uno de la
palabra mecánica.

Las raíces superestables de la familia no deformada se buscan mediante un
selector de rama explícito y no reciben como entrada las constantes de
Feigenbaum. Se comprueba además que el retorno hallado no posee un período
potencia de dos estrictamente menor.

Dependencias: biblioteca estándar y mpmath.  No se leen rutas externas.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys
from typing import Callable

# Dependencia vendorizada para reproducción bajo ``python -I -S``.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mpmath as mp


OUT = Path(__file__).resolve().parents[2] / "certificados" / "vacancias_criticidad.json"
VACANCY_WINDOW = 100_000_000
ROOT_LEVEL = 8


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"Fallo en vacancias o criticidad: {message}")


def mstr(value: mp.mpf, digits: int = 70) -> str:
    return mp.nstr(value, digits)


def event_position(k: int, beta: mp.mpf, beta_float: float) -> tuple[int, bool]:
    """Posición Beatty con recalculo multiprecisión cerca de una frontera."""

    approximate = k * beta_float
    if abs(approximate - round(approximate)) < 1e-6:
        return int(mp.ceil(k * beta) - 1), True
    return math.ceil(approximate) - 1, False


def vacancy_certificate() -> dict[str, object]:
    epsilon = mp.log10(mp.mpf(10) / 9)
    beta = 1 / epsilon
    sigma = 22 - beta
    reciprocal_sigma = 1 / sigma
    event_count = int(mp.floor((VACANCY_WINDOW + 1) * epsilon))
    beta_float = float(beta)

    gap_values: set[int] = set()
    return_values: set[int] = set()
    previous_event: int | None = None
    previous_short_gap_index: int | None = None
    multiprecision_boundary_checks = 0

    float_position_error_bound = (
        event_count * math.ulp(beta_float) / 2
        + math.ulp(event_count * beta_float) / 2
    )
    require(float_position_error_bound < 1e-6, "margen para las fronteras de Beatty")

    def reciprocal_terms():
        nonlocal previous_event
        nonlocal previous_short_gap_index
        nonlocal multiprecision_boundary_checks
        for k in range(1, event_count + 1):
            position, checked = event_position(k, beta, beta_float)
            multiprecision_boundary_checks += int(checked)
            if previous_event is not None:
                gap = position - previous_event
                gap_values.add(gap)
                if gap == 21:
                    # Este intervalo es el (k-1)-ésimo intervalo entre eventos.
                    short_gap_index = k - 1
                    if previous_short_gap_index is not None:
                        return_values.add(short_gap_index - previous_short_gap_index)
                    previous_short_gap_index = short_gap_index
            previous_event = position
            yield 1.0 / position

    reciprocal_sum = math.fsum(reciprocal_terms())

    require(gap_values == {21, 22}, "separaciones primarias")
    require(return_values == {6, 7}, "retornos secundarios")

    # V_N = epsilon*gamma + sum_{n<=N}(z_n-epsilon)/n
    #     = sum_{z_n=1} 1/n - epsilon*psi(N+1).
    partial_finite_part = mp.mpf(repr(reciprocal_sum)) - epsilon * mp.digamma(
        VACANCY_WINDOW + 1
    )
    tail_bound = mp.mpf(1) / (VACANCY_WINDOW + 1)
    # La guarda es muy superior al error de redondeo de math.fsum para esta
    # suma positiva y no altera el orden de magnitud de la cota analítica.
    numerical_guard = mp.mpf("1e-9")
    lower = partial_finite_part - tail_bound - numerical_guard
    upper = partial_finite_part + tail_bound + numerical_guard

    manuscript_lower = mp.mpf("-0.112071094143613634")
    manuscript_upper = mp.mpf("-0.112071055516338732")
    require(
        manuscript_lower < lower < upper < manuscript_upper,
        "el intervalo del manuscrito contiene el intervalo certificado",
    )

    return {
        "epsilon_vacancy": mstr(epsilon),
        "inverse_epsilon": mstr(beta),
        "sigma_short_gap": mstr(sigma),
        "inverse_sigma": mstr(reciprocal_sigma),
        "position_window": VACANCY_WINDOW,
        "events_in_window": event_count,
        "float_position_error_bound": repr(float_position_error_bound),
        "multiprecision_boundary_checks": multiprecision_boundary_checks,
        "primary_gap_set": sorted(gap_values),
        "secondary_return_set": sorted(return_values),
        "gamma_vacancy_partial_finite_part": mstr(partial_finite_part),
        "tail_bound": mstr(tail_bound),
        "numerical_guard": mstr(numerical_guard),
        "certified_interval": {"lower": mstr(lower), "upper": mstr(upper)},
        "manuscript_interval_contains_certificate": True,
    }


def phases() -> list[mp.mpf]:
    return [mp.radians(30 * m - 10) for m in range(1, 13)]


def quadratic_family(eta: mp.mpf) -> tuple[Callable[[mp.mpf], mp.mpf], mp.mpf, list[mp.mpf]]:
    phi = phases()
    weights = [
        (1 + eta * (12 * mp.cos(3 * angle) - mp.cos(4 * angle))) / 12
        for angle in phi
    ]
    require(min(weights) > 0, "positividad de los pesos dodecafásicos")
    require(abs(mp.fsum(weights) - 1) < mp.mpf("1e-90"), "normalización de pesos")
    scale = mp.sqrt(2 / mp.fsum(w * angle**2 for w, angle in zip(weights, phi)))

    def potential(x: mp.mpf) -> mp.mpf:
        return 1 - mp.fsum(
            w * mp.cos(scale * angle * x) for w, angle in zip(weights, phi)
        )

    quadratic_coefficient = (
        scale**2 * mp.fsum(w * angle**2 for w, angle in zip(weights, phi)) / 2
    )
    require(abs(quadratic_coefficient - 1) < mp.mpf("1e-90"), "criticidad cuadrática")
    return potential, scale, weights


def iterate_map(function: Callable[[mp.mpf], mp.mpf], x: mp.mpf, count: int) -> mp.mpf:
    value = mp.mpf(x)
    for _ in range(count):
        value = function(value)
    return value


def superstable_equation(potential: Callable[[mp.mpf], mp.mpf], parameter: mp.mpf, level: int) -> mp.mpf:
    def dynamical_map(x: mp.mpf) -> mp.mpf:
        return 1 - parameter * potential(x)

    return iterate_map(dynamical_map, mp.mpf(0), 2**level)


def next_superstable_root(
    potential: Callable[[mp.mpf], mp.mpf],
    level: int,
    previous: mp.mpf,
    previous_previous: mp.mpf,
) -> mp.mpf:
    separation = previous - previous_previous
    step = max(mp.mpf("1e-6"), min(mp.mpf("0.05"), abs(separation) / 4))
    left = previous + mp.mpf("1e-10") * max(1, abs(previous))
    value_left = superstable_equation(potential, left, level)
    if mp.sign(value_left) == 0:
        left = previous + mp.mpf("1e-8") * max(1, abs(previous))
        value_left = superstable_equation(potential, left, level)
    require(mp.sign(value_left) != 0, f"separación de la raíz heredada, nivel {level}")

    right_limit = previous + max(mp.mpf(1), 40 * abs(separation))
    for _ in range(200_000):
        right = left + step
        if right > right_limit:
            right_limit += max(mp.mpf(1), 40 * abs(separation))
        value_right = superstable_equation(potential, right, level)
        if mp.sign(value_right) == 0:
            return right
        if mp.sign(value_right) != mp.sign(value_left):
            a, b = left, right
            fa = value_left
            for _ in range(400):
                middle = (a + b) / 2
                fm = superstable_equation(potential, middle, level)
                if mp.sign(fm) == 0 or b - a < mp.mpf("1e-50"):
                    return middle
                if mp.sign(fm) == mp.sign(fa):
                    a, fa = middle, fm
                else:
                    b = middle
            return (a + b) / 2
        left, value_left = right, value_right
    raise RuntimeError(f"No se encontró la siguiente raíz superestable de nivel {level}")


def superstable_parameters(
    potential: Callable[[mp.mpf], mp.mpf], level_maximum: int
) -> list[mp.mpf]:
    parameters = [mp.mpf(0)] * (level_maximum + 1)
    parameters[1] = 1 / potential(1)
    for level in range(2, level_maximum + 1):
        parameters[level] = next_superstable_root(
            potential, level, parameters[level - 1], parameters[level - 2]
        )
    require(
        all(parameters[n] > parameters[n - 1] for n in range(2, level_maximum + 1)),
        "orden de las raíces superestables",
    )
    return parameters


def approximants(
    potential: Callable[[mp.mpf], mp.mpf], parameters: list[mp.mpf]
) -> tuple[dict[int, mp.mpf], dict[int, mp.mpf], dict[int, mp.mpf]]:
    x_values: dict[int, mp.mpf] = {}
    for level in range(1, len(parameters)):
        parameter = parameters[level]

        def dynamical_map(x: mp.mpf) -> mp.mpf:
            return 1 - parameter * potential(x)

        x_values[level] = iterate_map(dynamical_map, 0, 2 ** (level - 1))

    delta: dict[int, mp.mpf] = {}
    alpha_f: dict[int, mp.mpf] = {}
    for level in range(2, len(parameters)):
        delta[level] = (parameters[level - 1] - parameters[level - 2]) / (
            parameters[level] - parameters[level - 1]
        )
        alpha_f[level] = abs(x_values[level - 1]) / abs(x_values[level])
    return delta, alpha_f, x_values


def family_certificate(eta: mp.mpf) -> dict[str, object]:
    potential, scale, weights = quadratic_family(eta)
    parameters = superstable_parameters(potential, ROOT_LEVEL)
    delta, alpha_f, x_values = approximants(potential, parameters)
    residuals = {
        level: abs(superstable_equation(potential, parameters[level], level))
        for level in range(1, ROOT_LEVEL + 1)
    }
    require(max(residuals.values()) < mp.mpf("1e-45"), "residuos superestables")
    proper_divisor_returns: dict[int, dict[int, mp.mpf]] = {}
    for level in range(1, ROOT_LEVEL + 1):
        proper_divisor_returns[level] = {
            lower: abs(superstable_equation(potential, parameters[level], lower))
            for lower in range(level)
        }
        require(
            min(proper_divisor_returns[level].values()) > mp.mpf("1e-20"),
            f"el nivel {level} tiene período potencia de dos menor",
        )
    return {
        "eta": mstr(eta),
        "scale": mstr(scale),
        "minimum_weight": mstr(min(weights)),
        "maximum_weight": mstr(max(weights)),
        "superstable_parameters": {
            str(level): mstr(parameters[level]) for level in range(1, ROOT_LEVEL + 1)
        },
        "root_residuals": {
            str(level): mstr(residuals[level], 12) for level in range(1, ROOT_LEVEL + 1)
        },
        "proper_power_of_two_return_residuals": {
            str(level): {
                str(lower): mstr(value, 20)
                for lower, value in proper_divisor_returns[level].items()
            }
            for level in range(1, ROOT_LEVEL + 1)
        },
        "delta": {
            str(level): mstr(delta[level]) for level in range(2, ROOT_LEVEL + 1)
        },
        "alpha_F": {
            str(level): mstr(alpha_f[level]) for level in range(2, ROOT_LEVEL + 1)
        },
        "central_orbit_coordinates": {
            str(level): mstr(x_values[level]) for level in range(1, ROOT_LEVEL + 1)
        },
    }


def criticality_certificate() -> dict[str, object]:
    undeformed = family_certificate(mp.mpf(0))

    return {
        "root_level": ROOT_LEVEL,
        "selection_rule": (
            "primera raíz con cambio de signo encontrada por la malla adaptativa "
            "después del parámetro del nivel anterior, seguida de bisección"
        ),
        "undeformed_eta_zero": undeformed,
        "Feigenbaum_constants_used_as_inputs": False,
        "global_root_uniqueness_claimed": False,
    }


def main() -> None:
    mp.mp.dps = 90
    result = {
        "schema": "hmt.vacancias_y_criticidad_cuadratica",
        "status": "PASS",
        "dependencies": {"python_standard_library": True, "mpmath": mp.__version__},
        "vacancy_rotation": vacancy_certificate(),
        "dodecaphase_quadratic_criticality": criticality_certificate(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    print("PASS_VACANCIAS_CRITICIDAD")


if __name__ == "__main__":
    main()
