#!/usr/bin/env python3
"""Small sign/order tests for clock suspension; no physical value fitting."""
import cmath
import importlib.util
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location("suspension_matrices", Path(__file__).with_name("verificar_acoplamiento_finito.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def main():
    checks = []

    def check(name, a, b, unequal=False):
        error = m.residual(a, b)
        passed = error > 1e-8 if unequal else error < 1e-12
        checks.append({"name": name, "passed": passed, "residual": error})
        if not passed:
            raise AssertionError(name)

    # Exact fourth-root fixtures. ET and C do not commute.
    c = [[0, 1], [1, 0]]
    et = m.diag([1, -1])
    ehalf = m.diag([1, 1j])
    u = m.mul(c, et)
    b = m.adj(u)
    check("return_unitary", m.mul(m.adj(u), u), m.eye(2))
    check("noncommuting_clock_and_local_evolution", m.mul(c, et), m.mul(et, c), unequal=True)
    check("physical_boundary_ET_B_equals_C_inverse", m.mul(et, b), m.adj(c))
    check("negative_wrong_twist_B_equals_U", m.mul(et, u), m.adj(c), unequal=True)

    # In the moving frame E(s)^*psi(s), two half-interval step functions
    # form an invariant space of the half-period twisted translation.
    # This is an L2 test, not an evaluation map at a point.
    half = m.zero(4)
    for i in range(2):
        for j in range(2):
            half[i][j + 2] = u[i][j]  # negative crossing uses B^{-1}=U
            half[i + 2][j] = int(i == j)
    check("half_period_translation_unitary", m.mul(m.adj(half), half), m.eye(4))
    check("full_period_translation_is_U_not_inverse", m.mul(half, half), m.direct(u, u))
    check("negative_full_period_wrong_orientation", m.mul(half, half), m.direct(b, b), unequal=True)
    conjugated = m.mul(m.mul(ehalf, u), m.adj(ehalf))
    check("monodromy_at_other_phase_is_conjugated", conjugated, u, unequal=True)
    check("two_periods_respect_order", m.mul(conjugated, conjugated), m.mul(m.mul(ehalf, m.mul(u, u)), m.adj(ehalf)))

    # A common change of clock units T'=aT, H'=H/a leaves U unchanged.
    # Values below are test units, not HMT time/action/energy predictions.
    period, hbar, scale = 2., 3., 7.
    energies = [0., -math.pi * hbar / period]
    et_numeric = m.diag([cmath.exp(-1j * period * e / hbar) for e in energies])
    et_rescaled = m.diag([cmath.exp(-1j * (scale * period) * (e / scale) / hbar) for e in energies])
    check("common_clock_energy_rescaling", et_rescaled, et_numeric)
    check("root_fixture_matches_continuous_phase", et_numeric, et)

    print(json.dumps({
        "status": "PASS_CLOCK_SUSPENSION_SIGNS_ORDER_SCALE",
        "checks_passed": len(checks),
        "scope": "Exact-root finite sign and boundary fixtures, generic-L2 step-function translation and common clock-unit scaling; operator domains proved in the note.",
        "checks": checks,
    }, indent=2))


if __name__ == "__main__":
    main()
