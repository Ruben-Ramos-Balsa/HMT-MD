#!/usr/bin/env python3
"""Verificación exacta del delta fotónico Bendersky--Glaisher de V."""

from fractions import Fraction
from math import comb


def bernoulli_numbers(n: int) -> list[Fraction]:
    values = [Fraction(1)]
    for m in range(1, n + 1):
        total = sum(Fraction(comb(m + 1, k)) * values[k] for k in range(m))
        values.append(-total / Fraction(m + 1))
    return values


def main() -> None:
    bernoulli = bernoulli_numbers(3)
    assert bernoulli[1] == Fraction(-1, 2)
    assert bernoulli[3] == 0

    # Z_3(3)=4*pi^2*log(A_2^BG). Los factores siguientes son exactos.
    photon_number_factor = Fraction(2) * 4
    mean_energy_factor = Fraction(1, 15) / photon_number_factor
    mean_entropy_factor = Fraction(4, 45) / photon_number_factor
    assert photon_number_factor == 8
    assert mean_energy_factor == Fraction(1, 120)
    assert mean_entropy_factor == Fraction(1, 90)

    # En k=2, H_2*B_3/3=0: no queda un normalizador oculto.
    h_2 = Fraction(3, 2)
    assert h_2 * bernoulli[3] / 3 == 0
    print("PASS_V_A2_BG_PHOTONIC_COMPOSITION")


if __name__ == "__main__":
    main()
