#!/usr/bin/env python3
"""Verifica cancelaciones, costura y completación cúbica tipada de VI."""

from fractions import Fraction
import hashlib
from itertools import product
from math import comb
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def eta(a: int, b: int) -> int:
    return 1 + 3 * (a % 3) + (b % 3)


def threshold(values: list[int], n: int) -> int:
    return values[n + 1] - values[n]


def main() -> None:
    previous = runpy.run_path(str(ROOT / "technical" / "verificar_antipodal_costura.py"))
    previous["verify_antipodal"]()
    previous["verify_seams"]()

    image = {
        (eta(*word[0:2]), eta(*word[2:4]), eta(*word[4:6]))
        for word in product(range(3), repeat=6)
    }
    assert len(image) == 729
    assert image == set(product(range(1, 10), repeat=3))
    strata = [comb(3, r) * 9 ** (3 - r) for r in range(4)]
    assert strata == [729, 243, 27, 1]
    assert sum(strata) == 1000
    assert sum(strata[:-1]) == 999
    assert sum(strata[1:]) == 271
    assert 9**3 - 7**3 == 386
    assert sum(Fraction(value, 1000) for value in strata) == 1
    assert Fraction(strata[-1], 1000) == Fraction(1, 1000)
    for dimension in range(1, 9):
        assert sum(comb(dimension, r) * 9 ** (dimension - r)
                   for r in range(dimension + 1)) == 10**dimension
        for n in range(1, 12):
            assert (n + 1) ** dimension - n**dimension == sum(
                comb(dimension, r) * n ** (dimension - r)
                for r in range(1, dimension + 1)
            )

    f = [n * n + 2 for n in range(14)]
    g = [3 * n + 1 for n in range(14)]
    fg = [left * right for left, right in zip(f, g)]
    for n in range(12):
        assert threshold(fg, n) == (
            f[n + 1] * threshold(g, n) + g[n] * threshold(f, n)
        )

    section = (ROOT / "sections" / "14a_completacion_cubica.tex").read_text(encoding="utf-8")
    threshold_source = (ROOT / "sections" / "14a_diferencia_umbral.tex").read_text(encoding="utf-8")
    parent = (ROOT / "sections" / "14_generacion_regional.tex").read_text(encoding="utf-8")
    figure = (ROOT / "figures" / "cubo_completacion.tex").read_text(encoding="utf-8")
    historical_pdf = ROOT / "figures" / "cubo_emrh_original.pdf"
    historical_source = ROOT / "figures" / "cubo_emrh_original.tex"
    compact_section = "".join(section.split())
    assert "\\input{sections/14a_completacion_cubica.tex}" in parent
    assert "\\input{sections/14a_diferencia_umbral.tex}" in section
    assert "vi:cubo:mg07:binomio" in threshold_source
    assert "D_\\#f_d(n)=(n+1)^d-n^d" in threshold_source
    assert "\\beta(w_1,\\ldots,w_6)" in section
    assert "729+243+27=999" in section
    assert "999+1=729+271=1000" in compact_section
    assert "\\includegraphics[width=\\textwidth]{figures/cubo_emrh_original.pdf}" in figure
    assert "vi:cubo:completacion-3d" in figure
    assert sha256(historical_pdf) == "bd3842ba33de08b72ca24881dfc383da7eec8a81921983e5fe93702b5860daf5"
    assert sha256(historical_source) == "03eff9b05c325af9a20875893149a96d3737b3c20c7ebc33237dd5b863d00330"
    print("PASS_VI_ANTIPODAL_SEAM_CUBIC_COMPLETION")


if __name__ == "__main__":
    main()
