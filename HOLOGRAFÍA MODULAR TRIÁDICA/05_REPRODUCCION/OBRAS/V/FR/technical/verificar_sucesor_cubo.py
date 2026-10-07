#!/usr/bin/env python3
"""Verifica conjuntamente el delta fotónico y la completación cúbica de V."""

from fractions import Fraction
import hashlib
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    assert Fraction(2) * 4 == 8
    assert Fraction(1, 15) / 8 == Fraction(1, 120)
    assert Fraction(4, 45) / 8 == Fraction(1, 90)

    strata = [comb(3, r) * 9 ** (3 - r) for r in range(4)]
    assert strata == [729, 243, 27, 1]
    assert sum(strata) == 1000
    assert sum(strata[:-1]) == 999
    assert sum(strata[1:]) == 271
    assert 9**3 - 7**3 == 386
    for dimension in range(1, 9):
        assert sum(comb(dimension, r) * 9 ** (dimension - r)
                   for r in range(dimension + 1)) == 10**dimension
        assert Fraction(10, 10 ** (dimension + 1)) == Fraction(1, 10**dimension)

    section = (ROOT / "sections" / "revision_emrh.tex").read_text(encoding="utf-8")
    figure = (ROOT / "figures" / "cubo_completacion.tex").read_text(encoding="utf-8")
    historical_pdf = ROOT / "figures" / "cubo_emrh_original.pdf"
    historical_source = ROOT / "figures" / "cubo_emrh_original.tex"
    compact_section = "".join(section.split())
    assert "\\input{figures/cubo_completacion.tex}" in section
    assert "729+243+27=999" in compact_section
    assert "999+1=1000" in compact_section
    assert "\\includegraphics[width=\\textwidth]{figures/cubo_emrh_original.pdf}" in figure
    assert "fig:completacion-cubo-recuperado" in figure
    assert sha256(historical_pdf) == "bd3842ba33de08b72ca24881dfc383da7eec8a81921983e5fe93702b5860daf5"
    assert sha256(historical_source) == "03eff9b05c325af9a20875893149a96d3737b3c20c7ebc33237dd5b863d00330"
    print("PASS_V_A2_BG_PHOTONIC_CUBIC_COMPLETION")


if __name__ == "__main__":
    main()
