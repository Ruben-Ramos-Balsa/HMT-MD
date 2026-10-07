#!/usr/bin/env python3
"""Portable exact verifier for the Article VI longitudinal/gravity delta.

This program verifies only the algebra published in the local manuscript.
It deliberately uses synthetic rational coordinates, no CODATA/PDG values,
no external files, and no network access.  The mass operator is constructed
before the gravitational coefficient.
"""

from fractions import Fraction as F
import json
import sys

STATUS = "PASS_RIGIDEZ_G_MASAS_VI_PORTABLE"
N = 12 * 4 * 120
R_N = F(N - 1, 4 * N)
I2 = ((F(1), F(0)), (F(0), F(1)))
Y = ((F(2), F(1)), (F(1), F(3)))


def mscale(a, matrix):
    return tuple(tuple(a * x for x in row) for row in matrix)


def mmul(a, b):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )


def minverse(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if det == 0:
        raise AssertionError("non-invertible massive test fibre")
    return (
        (a[1][1] / det, -a[0][1] / det),
        (-a[1][0] / det, a[0][0] / det),
    )


def require(name, condition):
    if not condition:
        raise AssertionError(name)


def evaluate(length_section, action_section):
    # Synthetic exact coordinates: they test identities, not metrology.
    alpha_hmt = F(2, 3)
    pi_hmt = F(5, 2)
    c_int = F(17, 19)
    electron_energy = F(23, 29)

    l_alpha = alpha_hmt**16 * R_N * length_section
    t0 = pi_hmt * l_alpha / (54 * c_int)
    omega0 = 2 * pi_hmt / (108 * t0)
    q_l = action_section * c_int / l_alpha
    m_clock = q_l / c_int**2
    b_e = electron_energy / q_l

    # Route operator Y is fixed.  X cotransforms through b_e, while the
    # dimensional mass M = m_clock b_e Y remains invariant.
    x = mscale(b_e, Y)
    mass = mscale(m_clock, x)
    hamiltonian = mscale(c_int**2, mass)
    lambda_action = mscale(l_alpha, minverse(x))
    radial = mscale(l_alpha, x)
    g_coeff = c_int**3 * l_alpha**2 / action_section

    require("N", N == 5760)
    require("r_N", R_N == F(5759, 23040))
    require("clock", omega0 == c_int / l_alpha)
    require("R_108", c_int / omega0 == l_alpha)
    require("electronic cancellation",
            m_clock * b_e == electron_energy / c_int**2)
    require("mass construction",
            mass == mscale(electron_energy / c_int**2, Y))
    require("R01 left",
            mmul(hamiltonian, lambda_action)
            == mscale(action_section * c_int, I2))
    require("R01 right",
            mmul(lambda_action, hamiltonian)
            == mscale(action_section * c_int, I2))
    require("R02 left",
            mmul(radial, lambda_action) == mscale(l_alpha**2, I2))
    require("R02 right",
            mmul(lambda_action, radial) == mscale(l_alpha**2, I2))
    require("unique G realization",
            radial == mscale(g_coeff / c_int**2, mass))
    require("circular corollary",
            g_coeff
            == (F(54) / pi_hmt) ** 2
            * c_int**5 * t0**2 / action_section)

    return {
        "L_alpha": l_alpha,
        "t0": t0,
        "Q_L": q_l,
        "m_clock": m_clock,
        "b_e": b_e,
        "mass": mass,
        "Lambda": lambda_action,
        "R_g": radial,
        "G": g_coeff,
    }


def ratio(a, b):
    return a / b


def serial(value):
    if isinstance(value, tuple):
        return [[serial(x) for x in row] for row in value]
    return f"{value.numerator}/{value.denominator}"


def report():
    base_l = F(7, 5)
    base_h = F(11, 13)
    lambda_l = F(7, 3)
    mu_h = F(11, 5)

    baseline = evaluate(base_l, base_h)
    length_only = evaluate(lambda_l * base_l, base_h)
    action_only = evaluate(base_l, mu_h * base_h)
    combined = evaluate(lambda_l * base_l, mu_h * base_h)

    require("longitudinal L_alpha",
            ratio(length_only["L_alpha"], baseline["L_alpha"]) == lambda_l)
    require("longitudinal Q_L",
            ratio(length_only["Q_L"], baseline["Q_L"]) == 1 / lambda_l)
    require("longitudinal m_clock",
            ratio(length_only["m_clock"], baseline["m_clock"]) == 1 / lambda_l)
    require("longitudinal b_e",
            ratio(length_only["b_e"], baseline["b_e"]) == lambda_l)
    require("longitudinal mass invariant",
            length_only["mass"] == baseline["mass"])
    require("longitudinal G",
            ratio(length_only["G"], baseline["G"]) == lambda_l**2)

    require("action L_alpha invariant",
            action_only["L_alpha"] == baseline["L_alpha"])
    require("action Q_L",
            ratio(action_only["Q_L"], baseline["Q_L"]) == mu_h)
    require("action m_clock",
            ratio(action_only["m_clock"], baseline["m_clock"]) == mu_h)
    require("action b_e",
            ratio(action_only["b_e"], baseline["b_e"]) == 1 / mu_h)
    require("action mass invariant",
            action_only["mass"] == baseline["mass"])
    require("action G",
            ratio(action_only["G"], baseline["G"]) == 1 / mu_h)

    require("combined Q_L",
            ratio(combined["Q_L"], baseline["Q_L"])
            == mu_h / lambda_l)
    require("combined b_e",
            ratio(combined["b_e"], baseline["b_e"])
            == lambda_l / mu_h)
    require("combined mass invariant", combined["mass"] == baseline["mass"])
    require("combined G",
            ratio(combined["G"], baseline["G"])
            == lambda_l**2 / mu_h)

    return {
        "status": STATUS,
        "arithmetic": "exact rational",
        "external_inputs": False,
        "N": N,
        "r_N": serial(R_N),
        "independent_variations": {
            "longitudinal": serial(lambda_l),
            "action": serial(mu_h),
        },
        "checks": [
            "L_alpha precedes t0",
            "R_108 equals L_alpha",
            "Q_L, m_clock, and b_e cotransform",
            "mass operator is invariant under section changes",
            "R01: H Lambda = hbar c I",
            "R02: R_g Lambda = L_alpha^2 I",
            "G = c^3 L_alpha^2 / hbar",
            "circular expression is a corollary",
        ],
    }


if __name__ == "__main__":
    result = report()
    if "--json" in sys.argv[1:]:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(STATUS)

